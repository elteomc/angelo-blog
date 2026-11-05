"""Verify Gaussian response, slow feature drift, and archived network controls."""
from pathlib import Path
import json
import math
import unittest

import numpy as np


def record():
    root = Path(__file__).resolve().parents[1]
    return json.loads((root/'specs/011-stochastic-feature-response/experiment-record.json').read_text())


def features(theta):
    first = 2 / (1 + 100 * math.exp(1.05 * (theta - 0.2)))
    energy = np.array([first, 2-first])
    slope = 1.05 * energy[0]*energy[1]/2
    return energy, np.array([-slope,slope])


def normal_integral(function, sigma=1, mean=0, nodes=96):
    x, weight = np.polynomial.legendre.leggauss(nodes)
    answer = 0.0
    for left,right in [(-12*sigma,0),(0,12*sigma)]:
        samples = (right+left)/2 + (right-left)*x/2
        density = np.exp(-0.5*((samples-mean)/sigma)**2)/(math.sqrt(2*math.pi)*sigma)
        answer += np.sum(weight*function(samples)*density)*(right-left)/2
    return float(answer)


def polar(matrix):
    u, _, vh = np.linalg.svd(matrix,full_matrices=False)
    return u @ vh


def mean_and_se(values):
    values = np.asarray(values,dtype=float)
    return float(values.mean()),float(values.std(ddof=1)/math.sqrt(len(values)))


def seed_metrics(phase,arm,metric):
    rows = [r for r in record()['network'] if r['phase']==phase]
    return [np.mean([r['arms'][arm][metric] for r in rows if r['seed']==seed])
            for seed in sorted({r['seed'] for r in rows})]


def paired_metrics(phase,arm,metric='ood_mse'):
    return np.array(seed_metrics(phase,'polar',metric))-np.array(seed_metrics(phase,arm,metric))


class GaussianResponseChecks(unittest.TestCase):
    def test_sign_mean_against_split_quadrature(self):
        for sigma in [0.5,1,2]:
            for signal in [-0.3,0,0.4]:
                numerical = normal_integral(np.sign,sigma,signal)
                self.assertAlmostEqual(numerical,math.erf(signal/(math.sqrt(2)*sigma)),places=12)

    def test_sign_score_and_mean_derivative(self):
        for sigma in [0.5,1,2]:
            score = normal_integral(lambda x: np.sign(x)*x/sigma**2,sigma)
            finite = (normal_integral(np.sign,sigma,1e-5)-normal_integral(np.sign,sigma,-1e-5))/2e-5
            self.assertAlmostEqual(score,math.sqrt(2/math.pi)/sigma,places=12)
            self.assertAlmostEqual(score,finite,places=9)

    def test_residual_orthogonality_and_covariance(self):
        j = math.sqrt(2/math.pi)
        residual = lambda x: np.sign(x)-j*x
        self.assertAlmostEqual(normal_integral(residual),0,places=13)
        self.assertAlmostEqual(normal_integral(lambda x: residual(x)*x),0,places=12)
        variance = normal_integral(lambda x: residual(x)**2)
        self.assertAlmostEqual(variance,1-2/math.pi,places=12)
        self.assertAlmostEqual(variance+j*j,1,places=12)

    def test_multivariate_score_for_cubic_map(self):
        covariance = np.array([[1.0,0.3],[0.3,2]])
        nodes,weights = np.polynomial.hermite.hermgauss(12)
        grid = np.array(np.meshgrid(nodes,nodes,indexing='ij')).reshape(2,-1).T * math.sqrt(2)
        probability = np.outer(weights,weights).reshape(-1)/math.pi
        samples = grid @ np.linalg.cholesky(covariance).T
        mapped = np.column_stack([samples[:,0]**3,samples[:,1]**3])
        score = np.einsum('ni,nj,n->ij',mapped,samples,probability) @ np.linalg.inv(covariance)
        np.testing.assert_allclose(score,np.diag(3*np.diag(covariance)),atol=1e-12)
        residual = mapped-samples @ score.T
        np.testing.assert_allclose(np.einsum('ni,nj,n->ij',residual,samples,probability),0,atol=1e-12)

    def test_nongaussian_regression_is_not_mean_derivative(self):
        noise = np.array([-1.0,1])
        response = ((1e-5+noise)**3-(-1e-5+noise)**3).mean()/2e-5
        regression = np.mean(noise**4)/np.mean(noise**2)
        self.assertAlmostEqual(response,3,places=8)
        self.assertEqual(regression,1)

    def test_normalization_changes_jacobian(self):
        value = np.array([0.4,0.8,-0.2])
        matrix = np.array([[1,0.2],[0.3,-0.1],[0.2,0.7]])
        norm = np.linalg.norm(value)
        q = value/norm
        expected = (np.eye(3)-np.outer(q,q)) @ matrix/norm
        fn = lambda h: (value+matrix @ h)/np.linalg.norm(value+matrix @ h)
        observed = np.column_stack([(fn(1e-6*e)-fn(-1e-6*e))/2e-6 for e in np.eye(2)])
        np.testing.assert_allclose(observed,expected,atol=1e-10)
        self.assertGreater(np.linalg.norm(expected-matrix),0.1)

    def test_polar_column_noise_and_response_ordering(self):
        energy,_ = features(0.2)
        noise = np.random.default_rng(25).normal(size=(8192,2,2))*np.sqrt(energy)
        direction = polar(noise)/math.sqrt(2)
        v = np.mean(np.sum(direction*direction,axis=1),axis=0)/2
        k = np.mean(np.sum(direction*noise,axis=1),axis=0)/2
        np.testing.assert_allclose(v,[0.25,0.25],atol=1e-14)
        self.assertGreater(k[1],k[0]+0.4)
        np.testing.assert_allclose(np.swapaxes(direction,-2,-1) @ direction,np.broadcast_to(np.eye(2)/2,(8192,2,2)),atol=1e-14)

    def test_frozen_surrogate_variance_ratio(self):
        eta,c = 0.1,2
        denominator = 2*c-eta*c*c
        nonlinear,linear = eta/denominator,eta*(2/math.pi)/denominator
        self.assertAlmostEqual(nonlinear/linear,math.pi/2)
        rho = 1-eta*c
        summed = eta**2*sum(rho**(2*i) for i in range(1000))
        self.assertAlmostEqual(summed,nonlinear)


class FeatureSelectionChecks(unittest.TestCase):
    def test_energy_normalization_and_derivative(self):
        for theta in [-0.4,0.2,0.8]:
            a,derivative = features(theta)
            self.assertAlmostEqual(a.sum(),2)
            self.assertAlmostEqual(derivative.sum(),0)
            observed = (features(theta+1e-5)[0]-features(theta-1e-5)[0])/2e-5
            np.testing.assert_allclose(observed,derivative,atol=1e-10)

    def test_coupled_scalar_gradient(self):
        theta = 0.2
        z = np.array([[0.1,-0.2],[0.3,0.05]])
        xi = np.array([[0.5,0.1],[-0.7,0.2]])
        a,derivative = features(theta)
        loss = lambda t: np.sum((z*np.sqrt(features(t)[0])-xi)**2)/2
        expected = np.sum(derivative*np.sum(z*z,axis=0))/2-np.sum(derivative/(2*np.sqrt(a))*np.sum(xi*z,axis=0))
        self.assertAlmostEqual((loss(theta+1e-5)-loss(theta-1e-5))/2e-5,expected,places=10)

    def test_clean_hessian_trace_and_spectrum(self):
        for theta in [-0.2,0.2,0.7]:
            a,_ = features(theta)
            hessian = np.diag([a[0],a[1],a[0],a[1],0])
            self.assertAlmostEqual(np.trace(hessian),4)
            self.assertAlmostEqual(max(np.linalg.eigvalsh(hessian)),max(a))
        self.assertNotEqual(max(features(-0.2)[0]),max(features(0.7)[0]))

    def test_ar_variance_and_small_rate_limit(self):
        contraction,variance,eta = 0.7,0.25,0.02
        rho = 1-eta*contraction
        current = 0.0
        for _ in range(3000):
            current = rho*rho*current+eta*eta*variance
        exact = eta*variance/(2*contraction-eta*contraction**2)
        self.assertAlmostEqual(current,exact,places=13)
        for eta in [0.02,0.01,0.005]:
            exact = eta*variance/(2*contraction-eta*contraction**2)
            leading = eta*variance/(2*contraction)
            self.assertLess(abs(exact-leading),eta**2)

    def test_raw_gradient_drift_sign_and_zero_decay(self):
        for theta in [-0.2,0.2,0.7]:
            a,derivative = features(theta)
            c = 0.5
            kappa,variance = c*a,c*c*a
            drift = -0.5*np.sum(derivative*variance/(kappa+0.1))
            zero = -0.5*np.sum(derivative*variance/kappa)
            self.assertLess(drift,0)
            self.assertAlmostEqual(zero,0)

    def test_archived_polar_initial_drift(self):
        data = record()['feature']
        derivative = features(0.2)[1]
        for row in data['predictions']:
            calculated = -0.5*np.sum(derivative*np.array(row['variance'])/(np.array(row['kappa'])+0.1))
            self.assertAlmostEqual(calculated,row['initial_drift'],places=14)
        polar_row = next(r for r in data['predictions'] if r['mode']=='polar')
        self.assertGreater(polar_row['initial_drift'],0)
        self.assertLess(polar_row['kappa'][0],polar_row['kappa'][1])

    def test_output_graft_and_simultaneous_step_boundary(self):
        a,_ = features(0.2)
        b = np.sqrt(a)
        matrix = np.array([[0.2,0.3],[-0.5,0.4]])
        for d in [matrix,polar(matrix),matrix/np.linalg.norm(matrix)]:
            matched = d/np.linalg.norm(d*b)
            self.assertAlmostEqual(np.linalg.norm(matched*b),1)
        z = np.array([[0.1,0.2],[0.3,-0.1]])
        direction = polar(matrix)/math.sqrt(2)
        eta = 0.01
        complete = ((1-eta*0.1)*z-eta*direction)*np.sqrt(features(0.21)[0])-z*b
        self.assertGreater(np.linalg.norm(complete-(-eta*direction*b)),1e-5)

    def test_feature_function_tie_is_visible_only_off_design(self):
        for x in [np.array([1.0,0]),np.array([0.0,1])]:
            self.assertEqual(x[0]*x[1],0)
        mixed = np.array([1.0,1])
        self.assertEqual(mixed[0]*mixed[1],1)

    def test_archived_slow_horizon_and_copy_counts(self):
        data = record()['feature']
        for row in data['measured']:
            self.assertAlmostEqual(row['rate']**2*row['steps'],16)
            self.assertEqual(row['copies'],128 if row['rate']==0.02 else 64)
            self.assertAlmostEqual(row['mean_feature_energy'],2,places=12)
            self.assertGreater(row['se_theta_change'],0)


class NetworkControlChecks(unittest.TestCase):
    def test_sphere_step_has_declared_radius_and_angle(self):
        u = np.array([0.6,0.8,0.0])
        tangent = np.array([-0.8,0.6,0.0])
        alpha,radius = 0.03,2
        updated = radius*(math.cos(alpha)*u-math.sin(alpha)*tangent)
        self.assertAlmostEqual(np.linalg.norm(updated),radius)
        self.assertAlmostEqual(math.atan2(np.linalg.norm(np.cross(u,updated)),u @ updated),alpha)

    def test_finite_batch_affine_response_and_normalization(self):
        inputs = np.array([[1.0,0.3],[0.2,1.2],[-0.7,0.5]])
        directions = inputs/np.linalg.norm(inputs,axis=1)[:,None]
        derivatives = [(np.eye(2)-np.outer(q,q))/np.linalg.norm(g) for g,q in zip(inputs,directions)]
        j = np.mean(derivatives,axis=0)
        center,mean = inputs.mean(axis=0),directions.mean(axis=0)
        affine = mean+(inputs-center) @ j.T
        np.testing.assert_allclose(affine.mean(axis=0),mean)
        h = np.array([0.3,-0.1])*1e-5
        true = lambda t: ((inputs+t)/np.linalg.norm(inputs+t,axis=1)[:,None]).mean(axis=0)
        np.testing.assert_allclose(true(h)-true(-h),2*j @ h,atol=1e-14)
        normalized = affine/np.linalg.norm(affine,axis=1)[:,None]
        self.assertGreater(np.linalg.norm(normalized.mean(axis=0)-mean),0.01)

    def test_twelve_centered_batches_have_rank_at_most_eleven(self):
        inputs = np.random.default_rng(27).normal(size=(12,72))
        centered = inputs-inputs.mean(axis=0)
        self.assertLessEqual(np.linalg.matrix_rank(centered),11)

    def test_effective_rank_limits_and_scale(self):
        rank = lambda eigen: math.exp(-sum(p*math.log(p) for p in np.asarray(eigen)/sum(eigen) if p>0))
        self.assertAlmostEqual(rank([1,0,0]),1)
        self.assertAlmostEqual(rank([1,1,1]),3)
        self.assertAlmostEqual(rank([1,2,3]),rank([10,20,30]))

    def test_within_seed_pairing_and_standard_error(self):
        expected = {('fresh','angular_sgd'):(0.012163,0.003785),
                    ('fresh','response'):(-0.000010,0.000453),
                    ('exact','angular_sgd'):(0.006329,0.002593),
                    ('exact','response'):(0.000247,0.000407)}
        for (phase,arm),(mean,se) in expected.items():
            values = paired_metrics(phase,arm)
            self.assertEqual(len(values),4)
            actual_mean,actual_se = mean_and_se(values)
            self.assertAlmostEqual(actual_mean,mean,places=6)
            self.assertAlmostEqual(actual_se,se,places=6)

    def test_noisy_and_clean_article_table_means(self):
        expected = {'fresh':{'polar':(0.08083,6.3959),'angular_sgd':(0.06867,6.3001),'response':(0.08084,6.4308)},
                    'exact':{'polar':(0.055550,5.18060),'angular_sgd':(0.049221,4.99908),'response':(0.055303,5.17852)}}
        for phase,arms in expected.items():
            for arm,(loss,rank) in arms.items():
                self.assertAlmostEqual(np.mean(seed_metrics(phase,arm,'ood_mse')),loss,places=5)
                self.assertAlmostEqual(np.mean(seed_metrics(phase,arm,'effective_rank')),rank,places=4)

    def test_rank_prediction_and_clean_response_signs(self):
        rank = paired_metrics('fresh','angular_sgd','effective_rank')
        self.assertTrue(np.any(rank>0) and np.any(rank<0))
        self.assertAlmostEqual(mean_and_se(rank)[0],0.0958673509058694)
        loss = paired_metrics('exact','response')
        self.assertTrue(np.any(loss>0) and np.any(loss<0))

    def test_archive_protocol_and_stale_control(self):
        data = record()
        for row in data['network']:
            self.assertEqual(row['steps'],1024)
            self.assertEqual(row['pretrain'],2000)
            self.assertEqual(row['beta'],0)
            self.assertEqual(row['recalibrate'],{'main':128,'fresh':8,'exact':1}[row['phase']])
        stale = np.mean(seed_metrics('main','local_linear','ood_mse'))
        fresh = np.mean(seed_metrics('fresh','local_linear','ood_mse'))
        self.assertAlmostEqual(stale,0.18915,places=5)
        self.assertAlmostEqual(fresh,0.08242,places=5)
        self.assertGreater(stale,fresh+0.1)


if __name__ == '__main__':
    unittest.main()
