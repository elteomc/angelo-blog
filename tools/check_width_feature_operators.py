"""Verify fixed kernels, shallow width scaling, and nonlinear frozen operators."""
from pathlib import Path
import argparse
import itertools
import json
import math
import unittest

import numpy as np


Z = np.array([[1.,0],[0,1],[1,1]])
R0 = np.array([1.,-1,1])
RATE = 0.5
EPSILON = 0.2


def frozen_residuals(steps=60):
    values = [R0.copy()]
    kernel = Z @ Z.T
    for _ in range(steps):
        values.append(values[-1]-RATE/len(Z)*kernel @ values[-1])
    return np.array(values)


def scaling_step(width,beta,gamma,rate=0.2):
    p = math.tanh(1)
    d = 1-p*p
    scale = rate*width**(gamma-beta)
    a,w = 1+scale*p,1+scale*d
    return {'width': int(width),'beta': beta,'gamma': gamma,
            'feature_change': math.tanh(w)-p,
            'output_change': width**(1-beta)*(a*math.tanh(w)-p),
            'preactivation_change': scale*d}


def q(value,epsilon=EPSILON):
    return value/np.sqrt(value*value+epsilon*epsilon)


def operator(residual,epsilon=EPSILON):
    return Z @ q(Z.T @ residual/len(Z),epsilon)


def operator_jacobian(residual,epsilon=EPSILON):
    u = Z.T @ residual/len(Z)
    slope = epsilon**2/(u*u+epsilon**2)**1.5
    return (Z*slope) @ Z.T/len(Z)


def moment_path(initial):
    beta1,beta2,epsilon = 0.9,0.99,0.1
    rate = math.sqrt(1-beta2+epsilon**2)/(1-beta1)
    theta,m,v = float(initial),0.,0.
    states = [{'theta':theta,'first':m,'second':v}]
    for _ in range(2):
        g = theta
        m = beta1*m+(1-beta1)*g
        v = beta2*v+(1-beta2)*g*g
        theta -= rate*m/math.sqrt(v+epsilon**2)
        states.append({'theta':theta,'first':m,'second':v})
    return states


def numerical_jacobian(fn,w,epsilon=1e-6):
    w = np.asarray(w,dtype=float)
    return np.column_stack([(fn(w+epsilon*e)-fn(w-epsilon*e))/(2*epsilon) for e in np.eye(len(w))])


def results():
    kernel = Z @ Z.T
    floor = (np.eye(3)-kernel @ np.linalg.pinv(kernel)) @ R0
    return {
        'scope': 'Explicit finite linear models and one-step centered-neuron calculations. No benchmark training.',
        'kernel': {'features': Z.tolist(),'initial_residual': R0.tolist(),'rate': RATE,
                   'eigenvalues': np.linalg.eigvalsh(kernel).tolist(),'limiting_residual': floor.tolist(),
                   'loss_floor': float(floor @ floor/6)},
        'width': {'initial_a': 1,'initial_w': 1,'input': 1,'target': 1,'activation': 'tanh',
                  'centered_initial_output': True,'rate_constant': 0.2,
                  'steps': [scaling_step(n,b,g) for n in [16,64,256,1024,4096] for b,g in [(0.5,0),(1,0),(1,1)]]},
        'operator': {'epsilon': EPSILON,'ray': [1,0.5,-0.25]},
        'memory': {'beta1': 0.9,'beta2': 0.99,'epsilon': 0.1,'bias_correction': False,
                   'positive_path': moment_path(1),'negative_path': moment_path(-1)},
    }


class FrozenKernelChecks(unittest.TestCase):
    def test_parameter_and_output_recurrences_match(self):
        theta = np.zeros(2)
        values = frozen_residuals()
        for residual in values:
            np.testing.assert_allclose(Z @ theta+R0,residual,atol=2e-15)
            theta -= RATE/len(Z)*Z.T @ residual

    def test_spectrum_and_fitting_floor(self):
        kernel = Z @ Z.T
        np.testing.assert_allclose(np.linalg.eigvalsh(kernel),[0,1,3],atol=1e-14)
        floor = (np.eye(3)-kernel @ np.linalg.pinv(kernel)) @ R0
        np.testing.assert_allclose(floor,[-1/3,-1/3,1/3],atol=2e-15)
        self.assertAlmostEqual(floor @ floor/6,1/18)
        np.testing.assert_allclose(frozen_residuals(300)[-1],floor,atol=2e-14)

    def test_psd_identity_and_nullspace_preservation(self):
        kernel = Z @ Z.T
        for v in [R0,np.array([0.2,-0.7,0.3])]:
            self.assertAlmostEqual(v @ kernel @ v,np.linalg.norm(Z.T @ v)**2)
        null = np.array([-1.,-1,1])/math.sqrt(3)
        values = frozen_residuals()
        np.testing.assert_allclose(values @ null,np.full(len(values),R0 @ null),atol=1e-14)

    def test_test_input_pseudoinverse_prediction(self):
        j = np.array([0.3,-0.2])
        theta = np.zeros(2)
        for _ in range(300):
            theta -= RATE/len(Z)*Z.T @ (Z @ theta+R0)
        predicted = -(Z @ j) @ np.linalg.pinv(Z @ Z.T) @ R0
        self.assertAlmostEqual(j @ theta,predicted)

    def test_two_layer_tangent_kernel_matches_finite_derivative(self):
        inputs = np.array([[1.,0.2],[-0.3,0.5],[0.7,-0.8]])
        a = np.array([0.2,-0.7,0.3,0.8])
        w = np.array([[0.2,0.1],[-0.3,0.7],[0.4,-0.6],[0.5,0.2]])
        phi = np.tanh(inputs @ w.T)
        derivative = 1-phi*phi
        readout = phi @ phi.T/len(a)
        body = ((derivative*a*a) @ derivative.T)*(inputs @ inputs.T)/len(a)
        fn = lambda theta: np.tanh(inputs @ theta[4:].reshape(4,2).T) @ theta[:4]/2
        j = numerical_jacobian(fn,np.concatenate([a,w.ravel()]))
        np.testing.assert_allclose(j @ j.T,readout+body,atol=5e-11)
        self.assertGreater(np.linalg.norm(body),0.01)

    def test_rms_motion_and_growing_horizon_are_distinct(self):
        for n in [16,64,256]:
            movement = np.full(n,1/math.sqrt(n))
            self.assertAlmostEqual(np.linalg.norm(movement),1)
            self.assertAlmostEqual(np.sqrt(np.mean(movement**2)),1/math.sqrt(n))
            self.assertAlmostEqual(math.sqrt(n)/math.sqrt(n),1)

    def test_deterministic_kernel_can_have_random_initial_output(self):
        signs = np.array(list(itertools.product([-1.,1],repeat=4)))
        output = signs.sum(axis=1)/2
        tangent = np.ones((1,4))/2
        self.assertAlmostEqual(float((tangent @ tangent.T)[0,0]),1)
        self.assertAlmostEqual(output.var(),1)

    def test_output_space_stability_uses_loss_normalization(self):
        largest = 3
        self.assertAlmostEqual(1-RATE*largest/len(Z),0.5)
        self.assertGreater(abs(1-2.1*largest/len(Z)),1)


class WidthScalingChecks(unittest.TestCase):
    def test_individual_neuron_gradients_before_symmetry_reduction(self):
        n = 5
        coefficient = 1/n
        p = math.tanh(1)
        fn = lambda theta: np.array([(coefficient*np.sum(theta[:n]*np.tanh(theta[n:])-p)-1)**2/2])
        numeric = numerical_jacobian(fn,np.ones(2*n))[0]
        expected = np.concatenate([np.full(n,-coefficient*p),np.full(n,-coefficient*(1-p*p))])
        np.testing.assert_allclose(numeric,expected,atol=1e-10)

    def test_power_count_constraints_and_three_conventions(self):
        expected = {(0.5,0):(-0.5,0),(1,0):(-1,-1),(1,1):(0,0)}
        for (beta,gamma),powers in expected.items():
            self.assertEqual((gamma-beta,1+gamma-2*beta),powers)
        for beta in [0.5,0.75,1]:
            gamma = 2*beta-1
            self.assertEqual(1+gamma-2*beta,0)
            self.assertEqual(gamma-beta,beta-1)

    def test_exact_formula_matches_full_neuron_update(self):
        n = 64
        for beta,gamma in [(0.5,0),(1,0),(1,1)]:
            c = n**(-beta)
            a,w = np.ones(n),np.ones(n)
            phi = np.tanh(w)
            a_new = a+0.2*n**gamma*c*phi
            w_new = w+0.2*n**gamma*c*a*(1-phi*phi)
            output = c*np.sum(a_new*np.tanh(w_new)-phi)
            self.assertAlmostEqual(output,scaling_step(n,beta,gamma)['output_change'])

    def test_feature_learning_changes_are_width_independent(self):
        first = scaling_step(16,1,1)
        for n in [64,256,4096]:
            row = scaling_step(n,1,1)
            self.assertAlmostEqual(row['feature_change'],first['feature_change'])
            self.assertAlmostEqual(row['output_change'],first['output_change'])
        self.assertAlmostEqual(first['feature_change'],0.03308169161738794)
        self.assertAlmostEqual(first['output_change'],0.1541257878955694)

    def test_tangent_limit_retains_output_but_loses_feature_motion(self):
        p = math.tanh(1)
        expected = 0.2*(p*p+(1-p*p)**2)
        coarse,fine = scaling_step(16,0.5,0),scaling_step(65536,0.5,0)
        self.assertLess(fine['feature_change'],coarse['feature_change']/50)
        self.assertLess(abs(fine['output_change']-expected),abs(coarse['output_change']-expected)/50)

    def test_unadjusted_mean_output_freezes(self):
        p = math.tanh(1)
        expected = 0.2*(p*p+(1-p*p)**2)
        for n in [1024,4096,16384]:
            row = scaling_step(n,1,0)
            self.assertLess(abs(n*row['output_change']-expected),1/n)
            self.assertLess(row['feature_change'],1/n)

    def test_raw_and_effective_coordinates_give_same_finite_trajectory(self):
        n,rate = 7,0.05
        rng = np.random.default_rng(32)
        a,w = rng.normal(size=n),rng.normal(size=n)
        u,v = w/math.sqrt(n),a/math.sqrt(n)
        for _ in range(5):
            phi = np.tanh(w)
            residual = a @ phi/n+0.2
            a_new = a-rate*residual*phi
            w_new = w-rate*residual*a*(1-phi*phi)
            raw_phi = np.tanh(math.sqrt(n)*u)
            raw_residual = v @ raw_phi/math.sqrt(n)+0.2
            u_new = u-rate*raw_residual*v*(1-raw_phi*raw_phi)
            v_new = v-rate*raw_residual*raw_phi/math.sqrt(n)
            a,w,u,v = a_new,w_new,u_new,v_new
            np.testing.assert_allclose(a,math.sqrt(n)*v,atol=1e-15)
            np.testing.assert_allclose(w,math.sqrt(n)*u,atol=1e-15)

    def test_initial_random_variance_uses_square_root_width(self):
        signs = np.array(list(itertools.product([-1.,1],repeat=8)))
        for beta in [0.5,1]:
            output = signs.sum(axis=1)*8**(-beta)
            self.assertAlmostEqual(output.var(),8**(1-2*beta))


class NonlinearOperatorChecks(unittest.TestCase):
    def test_identity_processing_recovers_kernel(self):
        r = np.array([1.,0.5,-0.25])
        np.testing.assert_allclose(Z @ (Z.T @ r/3),(Z @ Z.T) @ r/3)

    def test_response_is_not_homogeneous(self):
        r = np.array([1.,0.5,-0.25])
        self.assertGreater(np.linalg.norm(operator(2*r)-2*operator(r)),0.1)

    def test_jacobian_is_psd_but_state_dependent(self):
        r = np.array([1.,0.5,-0.25])
        np.testing.assert_allclose(numerical_jacobian(operator,r),operator_jacobian(r),atol=1e-10)
        self.assertGreaterEqual(min(np.linalg.eigvalsh(operator_jacobian(r))),-1e-14)
        self.assertGreater(np.linalg.norm(operator_jacobian(r)-operator_jacobian(np.zeros(3))),0.1)

    def test_potential_gradient(self):
        potential = lambda r: np.array([3*np.sqrt((Z.T @ r/3)**2+EPSILON**2).sum()])
        r = np.array([1.,0.5,-0.25])
        np.testing.assert_allclose(numerical_jacobian(potential,r)[0],operator(r),atol=1e-10)

    def test_finite_step_loss_identity_and_large_rate_failure(self):
        r = np.array([1.,0.5,-0.25])
        direction = operator(r)
        self.assertGreater(r @ direction,0)
        for rate in [0.1,10]:
            observed = ((r-rate*direction) @ (r-rate*direction)-r @ r)/6
            expected = -rate*(r @ direction)/3+rate*rate*(direction @ direction)/6
            self.assertAlmostEqual(observed,expected)
        self.assertGreater(np.linalg.norm(r-10*direction),np.linalg.norm(r))

    def test_scaled_tangent_update_preserves_nonlinear_response(self):
        r = np.array([1.,0.5,-0.25])
        expected = -0.2*operator(r)/2
        for repeat in [1,4,16]:
            features = np.tile(Z,(1,repeat))
            n = features.shape[1]
            raw_gradient = features.T @ r/(3*math.sqrt(n))
            delta = -0.2/math.sqrt(n)*q(math.sqrt(n)*raw_gradient)
            np.testing.assert_allclose(features @ delta/math.sqrt(n),expected,atol=1e-15)

    def test_scaled_and_fixed_epsilon_have_different_limits(self):
        u = np.array([-0.3,0.2,0.5])
        for n in [16,256,4096]:
            raw = u/math.sqrt(n)
            np.testing.assert_allclose(q(raw,EPSILON/math.sqrt(n)),q(u),atol=1e-15)
        n = 10**8
        raw = u/math.sqrt(n)
        np.testing.assert_allclose(math.sqrt(n)*q(raw),u/EPSILON,rtol=1e-7)

    def test_actual_histories_meet_then_separate(self):
        positive,negative = moment_path(1),moment_path(-1)
        self.assertEqual(positive[1]['theta'],0)
        self.assertEqual(negative[1]['theta'],0)
        self.assertAlmostEqual(positive[1]['first'],0.1)
        self.assertAlmostEqual(negative[1]['first'],-0.1)
        self.assertAlmostEqual(positive[2]['theta'],-0.9022584728107539)
        self.assertAlmostEqual(negative[2]['theta'],0.9022584728107539)

    def test_resampling_changes_temporal_moment_correlations(self):
        beta = 0.9
        reused = [(1-beta)*(beta*z+z) for z in [-1,1]]
        independent = [(1-beta)*(beta*z0+z1) for z0,z1 in itertools.product([-1,1],repeat=2)]
        self.assertAlmostEqual(np.mean(np.square(reused)),(1-beta)**2*(1+beta)**2)
        self.assertAlmostEqual(np.mean(np.square(independent)),(1-beta)**2*(1+beta*beta))
        self.assertGreater(np.mean(np.square(reused)),np.mean(np.square(independent)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--results',type=Path)
    args,remaining = parser.parse_known_args()
    if args.results:
        args.results.write_text(json.dumps(results(),indent=2)+'\n')
    else:
        unittest.main(argv=[__file__]+remaining)
