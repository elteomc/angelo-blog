"""Check the explicit stability, feedback, and averaging examples."""
from pathlib import Path
import argparse
import json
import math
import unittest

import numpy as np


ETA = 1.0
GAMMA = 0.2
TARGET = 1.1
INITIAL = np.array([0.001,0.4])


def loss(w):
    x,y = np.asarray(w)
    return (1+y)*x*x/2+GAMMA*(y-TARGET)**2/2


def gradient(w):
    x,y = np.asarray(w)
    return np.array([(1+y)*x,x*x/2+GAMMA*(y-TARGET)])


def hessian(w):
    x,y = np.asarray(w)
    return np.array([[1+y,x],[x,GAMMA]])


def step(w):
    return np.asarray(w)-ETA*gradient(w)


def trajectory(initial=INITIAL,steps=400):
    values = [np.array(initial,dtype=float)]
    for _ in range(steps):
        values.append(step(values[-1]))
    return np.array(values)


def cycle():
    center_y = 2/ETA-1
    amplitude = math.sqrt(2*GAMMA*(TARGET-center_y))
    return amplitude,center_y


def central_y(t):
    return np.minimum(1,TARGET-(TARGET-INITIAL[1])*np.exp(-GAMMA*ETA*np.asarray(t)))


def boundary_variance(a,g):
    denominator = np.dot(a,a)
    if denominator==0:
        raise ValueError('Degenerate curvature response needs separate analysis')
    return max(0,-2*np.dot(a,g)/denominator)


def numerical_jacobian(fn,w,epsilon=1e-6):
    w = np.asarray(w,dtype=float)
    return np.column_stack([(fn(w+epsilon*e)-fn(w-epsilon*e))/(2*epsilon) for e in np.eye(len(w))])


def results():
    amp,y = cycle()
    trace = trajectory()
    k,h = ETA*amp,ETA*GAMMA
    matrix = np.array([[1-k*k,k*(2-h)],[-k*(2-h),(1-h)**2-k*k]])
    return {
        'scope': 'Finite evaluation of explicit low-dimensional examples. No neural-network training.',
        'parameters': {'eta': ETA,'a': 1,'b': 1,'gamma': GAMMA,'target_y': TARGET,'initial': INITIAL.tolist(),'steps': 400},
        'cycle': {'amplitude': amp,'center_y': y,'loss': float(loss([amp,y])),
                  'center_loss': float(loss([0,y])), 'full_sharpness': float(np.linalg.eigvalsh(hessian([amp,y]))[-1]),
                  'return_matrix': matrix.tolist(),'return_multiplier_moduli': np.abs(np.linalg.eigvals(matrix)).tolist()},
        'trajectory': {'final': trace[-1].tolist(),'maximum_absolute_x': float(np.max(np.abs(trace[:,0]))),
                       'initial_loss': float(loss(trace[0])),'maximum_loss': float(max(map(loss,trace))),
                       'minimum_loss': float(min(map(loss,trace)))},
        'central': {'contact_time': math.log(7)/GAMMA,'boundary_variance': boundary_variance(np.array([0.,1]),np.array([0.,-0.02]))},
    }


class QuadraticStabilityChecks(unittest.TestCase):
    def test_scalar_modes_and_closed_form(self):
        for curvature in [0.2,1,1.8,2,2.2]:
            value = 0.3
            for t in range(1,21):
                value -= curvature*value
                self.assertAlmostEqual(value,0.3*(1-curvature)**t,places=12)

    def test_symmetric_modes_recover_vector_update(self):
        q,_ = np.linalg.qr(np.array([[1.,2],[3,1]]))
        eigen = np.array([0.2,2.2])
        h = q @ np.diag(eigen) @ q.T
        w = np.array([0.3,-0.1])
        for t in [1,4,9]:
            predicted = q @ ((1-eigen)**t*(q.T @ w))
            np.testing.assert_allclose(np.linalg.matrix_power(np.eye(2)-h,t) @ w,predicted,atol=1e-13)

    def test_unexcited_negative_and_flat_modes(self):
        self.assertEqual((1-4)*0,0)
        self.assertGreater(abs(1-(-0.5)),1)
        self.assertEqual(1-0,1)

    def test_mixed_loss_falls_before_instability_dominates(self):
        times = np.arange(61)
        stable = 0.1*(2*0.8**times)**2
        unstable = 1.1*(1e-4*1.2**times)**2
        total = stable+unstable
        self.assertLess(total[10],total[0])
        self.assertGreater(total[-1],10*total[0])
        self.assertTrue(np.all(np.diff(unstable)>0))

    def test_exact_flow_and_euler_have_different_amplification(self):
        for curvature in [0.2,1.8,2.2]:
            self.assertGreater(math.exp(-curvature),0)
            self.assertLess(math.exp(-curvature),1)
        self.assertLess(1-2.2,-1)
        small = 1e-4
        self.assertLess(abs(math.exp(-small)-(1-small)),small*small)

    def test_segment_integral_counterexample(self):
        polynomial = lambda x: x+x*x/2+10*x**4
        curvature = lambda x: 1+120*x*x
        nodes,weights = np.polynomial.legendre.leggauss(8)
        s = (nodes+1)/2
        integral = np.sum(weights*(1-s)*curvature(-s))/2
        self.assertEqual(curvature(0),1)
        self.assertAlmostEqual(polynomial(-1)-polynomial(0),9.5)
        self.assertAlmostEqual(-1+integral,9.5)

    def test_simple_eigenvalue_derivative(self):
        w = np.array([0.07,0.8])
        eigen,u = np.linalg.eigh(hessian(w))
        top = u[:,-1]
        derivative = np.array([2*top[0]*top[1],top[0]**2])
        numeric = numerical_jacobian(lambda x: np.array([np.linalg.eigvalsh(hessian(x))[-1]]),w)[0]
        np.testing.assert_allclose(numeric,derivative,atol=1e-9)

    def test_progressive_sharpening_has_no_fixed_sign(self):
        quartic_drift = -6*1**4
        cubic_drift = -(1)*(-1+1**2/2)
        self.assertEqual(quartic_drift,-6)
        self.assertEqual(cubic_drift,0.5)


class SelfStabilizationChecks(unittest.TestCase):
    def test_gradient_against_loss_differences(self):
        for w in [[0.1,0.7],[-0.2,1.0],[0.001,0.4]]:
            numeric = numerical_jacobian(lambda x: np.array([loss(x)]),w)[0]
            np.testing.assert_allclose(numeric,gradient(w),atol=1e-11)

    def test_hessian_against_gradient_differences(self):
        np.testing.assert_allclose(numerical_jacobian(gradient,[0.1,0.7]),hessian([0.1,0.7]),atol=1e-10)

    def test_mixed_cubic_derivatives_have_both_coefficients(self):
        w = np.array([0.3,0.2])
        mixed = lambda z: np.array([z[1]*z[0],z[0]*z[0]/2])
        expected = np.array([[w[1],w[0]],[w[0],0]])
        np.testing.assert_allclose(numerical_jacobian(mixed,w),expected,atol=1e-10)

    def test_exact_cycle_and_losses(self):
        amp,y = cycle()
        np.testing.assert_allclose(step([amp,y]),[-amp,y],atol=1e-15)
        np.testing.assert_allclose(step([-amp,y]),[amp,y],atol=1e-15)
        self.assertAlmostEqual(amp,0.2)
        self.assertAlmostEqual(loss([amp,y]),0.041)
        self.assertAlmostEqual(loss([0,y]),0.001)

    def test_return_map_in_trajectory_order(self):
        amp,y = cycle()
        first = np.eye(2)-hessian([amp,y])
        second = np.eye(2)-hessian([-amp,y])
        expected = np.array([[0.96,0.36],[-0.36,0.60]])
        np.testing.assert_allclose(second @ first,expected,atol=1e-15)
        np.testing.assert_allclose(numerical_jacobian(lambda w: step(step(w)),[amp,y]),expected,atol=1e-10)

    def test_return_multipliers_and_nearby_attraction(self):
        matrix = np.array([[0.96,0.36],[-0.36,0.60]])
        np.testing.assert_allclose(np.abs(np.linalg.eigvals(matrix)),[0.84,0.84],atol=1e-14)
        w = np.array([0.20001,0.99999])
        for _ in range(100):
            w = step(step(w))
        np.testing.assert_allclose(w,[0.2,1],atol=1e-11)

    def test_declared_finite_trajectory_and_loss_window(self):
        values = trajectory()
        np.testing.assert_allclose(values[-1],[0.2,1],atol=1e-9)
        self.assertLess(np.max(np.abs(values[:,0])),0.225)
        self.assertGreater(loss(values[0]),loss(values[-1]))
        self.assertLess(min(map(loss,values)),1e-6)
        self.assertGreater(max(map(loss,values)),0.05)

    def test_invariant_axis_remains_unexcited(self):
        values = trajectory([0,0.4],steps=400)
        np.testing.assert_array_equal(values[:,0],0)
        self.assertAlmostEqual(values[-1,1],1.1)
        self.assertGreater(abs(1-(1+values[-1,1])),1)

    def test_full_cycle_sharpness_exceeds_coordinate_curvature(self):
        amp,y = cycle()
        sharpness = np.linalg.eigvalsh(hessian([amp,y]))[-1]
        expected = (2.2+math.sqrt(1.8**2+4*0.2**2))/2
        self.assertAlmostEqual(sharpness,expected)
        self.assertAlmostEqual(sharpness,2.0219544457292886)
        self.assertGreater(sharpness,2)


class CentralFlowChecks(unittest.TestCase):
    def test_frozen_window_is_centered_and_covariance_psd(self):
        samples = np.array([[0.1,0.2],[-0.2,0.3],[0.4,-0.1]])
        weights = np.array([0.2,0.3,0.5])
        center = weights @ samples
        delta = samples-center
        np.testing.assert_allclose(weights @ delta,0,atol=1e-15)
        covariance = np.einsum('n,ni,nj->ij',weights,delta,delta)
        self.assertGreaterEqual(min(np.linalg.eigvalsh(covariance)),0)

    def test_cubic_average_gradient_correction_is_exact(self):
        center = np.array([0.,0.9])
        amplitude = 0.13
        observed = (gradient(center+[amplitude,0])+gradient(center-[amplitude,0]))/2
        expected = gradient(center)+np.array([0,amplitude**2/2])
        np.testing.assert_allclose(observed,expected,atol=1e-15)
        self.assertGreater(np.linalg.norm(observed-gradient(center)),0.008)

    def test_scalar_covariance_complementarity(self):
        a = np.array([0.,1])
        for g in [np.array([0.,-0.02]),np.array([0.,0.02]),np.array([0.,0.])]:
            q = boundary_variance(a,g)
            y = np.dot(a,g)+q*np.dot(a,a)/2
            self.assertGreaterEqual(q,0)
            self.assertGreaterEqual(y,-1e-15)
            self.assertAlmostEqual(q*y,0)
        self.assertAlmostEqual(boundary_variance(a,[0,-0.02]),0.04)
        self.assertEqual(boundary_variance(a,[0,0.02]),0)
        with self.assertRaises(ValueError):
            boundary_variance(np.zeros(2),[0,-0.02])

    def test_central_contact_time_and_interior_equation(self):
        contact = math.log(7)/GAMMA
        self.assertAlmostEqual(contact,9.729550745276565)
        self.assertAlmostEqual(float(central_y(contact)),1)
        self.assertEqual(float(central_y(contact+100)),1)
        for t in [0,2,5]:
            numerical = (central_y(t+1e-5)-central_y(t-1e-5))/2e-5
            self.assertAlmostEqual(float(numerical),GAMMA*(TARGET-central_y(t)),places=10)

    def test_cycle_average_loss_needs_variance_term(self):
        amp,y = cycle()
        center = np.array([0.,y])
        sigma = np.diag([amp*amp,0])
        predicted = loss(center)+np.trace(hessian(center) @ sigma)/2
        observed = (loss([amp,y])+loss([-amp,y]))/2
        self.assertAlmostEqual(predicted,observed)
        self.assertAlmostEqual(predicted,0.041)
        self.assertAlmostEqual(np.trace(sigma)/ETA,0.04)

    def test_projection_velocity_and_center_loss_identity(self):
        a = np.array([1.,2])
        for g in [np.array([-2.,1]),np.array([-1.,-1]),np.array([1.,1])]:
            free = -g
            p = free-max(0,a @ free)/(a @ a)*a
            self.assertLessEqual(a @ p,1e-15)
            self.assertAlmostEqual(g @ p,-p @ p)

    def test_matrix_support_and_critical_basis_rotation(self):
        sigma = np.array([[0.1,0.04],[0.04,0.2]])
        curvature_response = np.array([[1.,0.5],[0.5,1]])
        rotation = np.array([[math.cos(.4),-math.sin(.4)],[math.sin(.4),math.cos(.4)]])
        observed = np.trace(curvature_response @ sigma)
        transformed = np.trace((rotation.T @ curvature_response @ rotation) @ (rotation.T @ sigma @ rotation))
        self.assertAlmostEqual(observed,transformed)
        self.assertNotAlmostEqual(observed,np.trace(curvature_response @ np.diag(np.diag(sigma))))
        ambient = np.zeros((3,3))
        ambient[:2,:2] = sigma
        np.testing.assert_allclose(np.diag([0,0,2]) @ ambient,0)

    def test_static_support_does_not_fix_variance(self):
        g = np.array([0.,-0.02])
        a = np.array([0.,1])
        self.assertGreater(-a @ g,0)
        self.assertEqual(np.trace(np.diag([0.,1]) @ np.zeros((2,2))),0)
        self.assertGreater(boundary_variance(a,g),0)

    def test_semidefinite_response_can_have_nonunique_covariance(self):
        first = np.diag([0.04,0])
        second = np.diag([0.02,0.02])
        for x in [first,second]:
            y = (-0.02+np.trace(x)/2)*np.eye(2)
            np.testing.assert_allclose(y,0,atol=1e-15)
            self.assertGreaterEqual(min(np.linalg.eigvalsh(x)),0)
            self.assertAlmostEqual(np.trace(x @ y),0)
        self.assertGreater(np.linalg.norm(first-second),0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--results',type=Path)
    args,remaining = parser.parse_known_args()
    if args.results:
        args.results.write_text(json.dumps(results(),indent=2)+'\n')
    else:
        unittest.main(argv=[__file__]+remaining)
