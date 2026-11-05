"""Check the intrinsic-noise, spherical-valley, and optimizer-state examples."""
import math
import unittest
import numpy as np


def gamma_solution(time, delta, trace=1, initial_multiple=4):
    equilibrium = trace / (2 * delta)
    return equilibrium * (1 + (initial_multiple - 1) * np.exp(-4 * delta * np.asarray(time)))


def valley_loss(weight):
    u = weight / np.linalg.norm(weight)
    return 0.5 * (2 + 0.8 * (u[0]**2 - u[1]**2)) * u[2]**2


def valley_gradient(weight):
    radius = np.linalg.norm(weight)
    u = weight / radius
    a = 2 + 0.8 * (u[0]**2 - u[1]**2)
    ambient = np.array([0.8 * u[0] * u[2]**2, -0.8 * u[1] * u[2]**2, a * u[2]])
    return (ambient - u * (u @ ambient)) / radius


def valley_run(decay=0.01, steps=3000):
    eta, phi0, z0 = 0.1, 0.3, 0.03
    a0 = 2 + 0.8 * math.cos(2 * phi0)
    radius = math.sqrt(eta / ((1 - eta * 0.01) * (2 / a0)))
    w = radius * np.array([math.sqrt(1 - z0**2) * math.cos(phi0),
                           math.sqrt(1 - z0**2) * math.sin(phi0), z0])
    result = []
    for step in range(steps + 1):
        u = w / np.linalg.norm(w)
        phi = math.atan2(u[1], u[0])
        result.append((step, phi, u[2], 2 + 0.8 * math.cos(2 * phi), valley_loss(w), np.linalg.norm(w)))
        if step < steps:
            w = (1 - eta * decay) * w - eta * valley_gradient(w)
    return np.array(result)


def rotation(angle):
    return np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])


def moment_direction(moment, second, epsilon=0):
    values, vectors = np.linalg.eigh(second)
    return (vectors * (1 / (np.sqrt(np.maximum(values, 0)) + epsilon))) @ vectors.T @ moment


def rotation_defects(angles):
    m, c = np.array([0.5, 1]), np.diag([1.0, 9])
    original = m / np.sqrt(np.diag(c))
    diagonal, full = [], []
    for angle in angles:
        o = rotation(angle)
        rotated_m, rotated_c = o @ m, o @ c @ o.T
        d = rotated_m / np.sqrt(np.diag(rotated_c))
        f = moment_direction(rotated_m, rotated_c)
        diagonal.append(np.linalg.norm(o.T @ d - original) / np.linalg.norm(original))
        full.append(np.linalg.norm(o.T @ f - original) / np.linalg.norm(original))
    return np.array(diagonal), np.array(full)


def softmax(values):
    e = np.exp(values - np.max(values))
    return e / e.sum()


class IntrinsicNoiseChecks(unittest.TestCase):
    def test_sampled_loss_covariance_and_homogeneity(self):
        u = np.array([0.3, -0.4, math.sqrt(0.75)])
        p = np.eye(3) - np.outer(u, u)
        samples = np.vstack([math.sqrt(3) * np.eye(3), -math.sqrt(3) * np.eye(3)])
        gradients = samples @ p
        np.testing.assert_allclose(gradients.mean(axis=0), 0, atol=1e-14)
        np.testing.assert_allclose(gradients.T @ gradients / 6, p, atol=1e-14)
        self.assertAlmostEqual(np.trace(gradients.T @ gradients / 6), 2)
        for xi in samples:
            loss = lambda w: xi @ w / np.linalg.norm(w)
            w = 1.7 * u
            g = p @ xi / 1.7
            observed = [(loss(w + 1e-6 * e) - loss(w - 1e-6 * e)) / 2e-6 for e in np.eye(3)]
            np.testing.assert_allclose(observed, g, atol=1e-9)
            self.assertAlmostEqual(loss(w), loss(4 * w))

    def test_exact_discrete_fourth_moment_identity(self):
        u, radius, eta, decay = np.array([0.6, 0.8]), 1.7, 0.2, 0.1
        tangent = np.array([-0.8, 0.6])
        a = 1 - eta * decay
        gamma = radius**4 / eta**2
        values, predicted = [], []
        for scalar in [-2, 0.5, 3]:
            g = scalar * tangent
            updated = a * radius * u - eta * g / radius
            z = g @ g
            values.append(np.linalg.norm(updated)**4 / eta**2)
            predicted.append(a**4 * gamma + 2 * a*a * z + z*z / gamma)
        np.testing.assert_allclose(values, predicted, rtol=1e-14)
        self.assertAlmostEqual(np.mean(values), np.mean(predicted))

    def test_ito_correction_by_directional_hessian(self):
        u, radius, eta = np.array([0.6, 0.8, 0.0]), 1.7, 0.1
        p = np.eye(3) - np.outer(u, u)
        diffusion = eta * p / radius
        w = radius * u
        unit = lambda x: x / np.linalg.norm(x)
        observed = np.zeros(3)
        h = 0.001
        for direction in diffusion.T:
            observed += (unit(w + h * direction) - 2 * u + unit(w - h * direction)) / (2 * h*h)
        expected = -eta**2 * np.trace(p) / (2 * radius**4) * u
        np.testing.assert_allclose(observed, expected, atol=1e-9)

    def test_unit_norm_balance_for_direction_sde(self):
        u, gamma = np.array([0.6, 0.8, 0.0]), 5.0
        p = np.eye(3) - np.outer(u, u)
        c = p @ np.diag([0.2, 0.5, 1.0]) @ p
        g = p @ np.array([1, -1, 0.2])
        drift = -g / math.sqrt(gamma) - np.trace(c) * u / (2 * gamma)
        self.assertAlmostEqual(2 * u @ drift + np.trace(c) / gamma, 0)

    def test_gamma_solution_against_independent_rk4(self):
        delta, trace = 0.001, 1.0
        value = 2000.0
        derivative = lambda x: -4 * delta * x + 2 * trace
        dt = 0.5
        for _ in range(2000):
            k1 = derivative(value)
            k2 = derivative(value + dt * k1 / 2)
            k3 = derivative(value + dt * k2 / 2)
            k4 = derivative(value + dt * k3)
            value += dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        self.assertAlmostEqual(value, float(gamma_solution(1000, delta)), places=9)

    def test_equilibrium_reciprocal_and_half_life(self):
        delta, trace = 0.001, 1
        equilibrium = trace / (2 * delta)
        q = 1 / math.sqrt(equilibrium)
        self.assertAlmostEqual(q, 0.044721359549995794)
        self.assertAlmostEqual(q*q * trace, 2 * delta)
        half = math.log(2) / (4 * delta)
        initial = float(gamma_solution(0, delta))
        self.assertAlmostEqual(float(gamma_solution(half, delta)) - equilibrium, (initial - equilibrium) / 2)

    def test_rescaled_clock_and_initialization(self):
        for tau in np.linspace(0, 2, 20):
            first = gamma_solution(tau / 0.001, 0.001) / 500
            second = gamma_solution(tau / 0.002, 0.002) / 250
            self.assertAlmostEqual(first, second)
        radius, eta = 1.4, 0.1
        gamma = radius**4 / eta**2
        self.assertAlmostEqual((radius / math.sqrt(2))**4 / (eta / 2)**2, gamma)

    def test_equal_trace_does_not_determine_directional_noise(self):
        c1, c2 = np.diag([1.0, 0, 0]), np.diag([0.5, 0.5, 0])
        self.assertEqual(np.trace(c1), np.trace(c2))
        self.assertNotEqual(c1[1, 1], c2[1, 1])
        self.assertEqual(c1[2, 2], c2[2, 2])

    def test_deterministic_finite_step_has_radius_kick(self):
        w = np.array([1.0, 0, 0])
        gradient = np.array([0, 1.0, 0])
        eta, delta = 0.1, 0.001
        updated = (1 - delta) * w - eta * gradient
        self.assertAlmostEqual(updated @ updated, (1 - delta)**2 + eta**2)
        self.assertGreater(updated @ updated, (1 - delta)**2)


class SphericalSharpnessChecks(unittest.TestCase):
    def test_valley_gradient_by_finite_difference(self):
        for w in [np.array([1.0, 0.3, 0.02]), np.array([0.2, 0.7, -0.1]), np.array([-1, 0.5, 0.3])]:
            observed = [(valley_loss(w + 1e-6 * e) - valley_loss(w - 1e-6 * e)) / 2e-6 for e in np.eye(3)]
            np.testing.assert_allclose(observed, valley_gradient(w), atol=1e-10)
            self.assertAlmostEqual(w @ valley_gradient(w), 0)
            np.testing.assert_allclose(valley_gradient(3*w), valley_gradient(w) / 3, atol=1e-14)

    def test_equatorial_curvature_and_radial_scaling(self):
        for phi in [0, 0.3, 1.2, math.pi / 2]:
            u = np.array([math.cos(phi), math.sin(phi), 0.0])
            hessian = np.column_stack([(valley_gradient(u + 1e-5 * e) - valley_gradient(u - 1e-5 * e)) / 2e-5 for e in np.eye(3)])
            a = 2 + 0.8 * math.cos(2 * phi)
            np.testing.assert_allclose(np.linalg.eigvalsh(hessian), [0, 0, a], atol=1e-9)
            scaled = np.column_stack([(valley_gradient(3*u + 1e-5 * e) - valley_gradient(3*u - 1e-5 * e)) / 2e-5 for e in np.eye(3)])
            np.testing.assert_allclose(9 * scaled, hessian, atol=1e-9)

    def test_exact_spherical_update_and_longitude(self):
        phi, z, eta, decay, radius = 0.3, 0.02, 0.1, 0.01, 0.5
        u = np.array([math.sqrt(1-z*z) * math.cos(phi), math.sqrt(1-z*z) * math.sin(phi), z])
        g = valley_gradient(u)
        a = 1 - eta * decay
        q = eta / (a * radius**2)
        raw = a * radius * u - eta * valley_gradient(radius*u)
        expected = (u - q*g) / math.sqrt(1 + q*q * (g @ g))
        np.testing.assert_allclose(raw / np.linalg.norm(raw), expected, atol=1e-14)
        curvature = 2 + 0.8 * math.cos(2*phi)
        derivative = -1.6 * math.sin(2*phi)
        d = curvature - 1.6 * math.cos(2*phi) * z*z
        angular = math.atan2(-0.5*q*derivative*z*z, 1 + q*d*z*z)
        self.assertAlmostEqual(math.atan2(expected[1], expected[0]) - phi, angular, places=14)

    def test_normal_linearization_and_even_longitude_drift(self):
        phi, q = 0.3, 0.5
        outcomes = []
        for z in [1e-5, -1e-5]:
            u = np.array([math.sqrt(1-z*z) * math.cos(phi), math.sqrt(1-z*z) * math.sin(phi), z])
            v = u - q * valley_gradient(u)
            v /= np.linalg.norm(v)
            expected = 1 - q * (2 + 0.8 * math.cos(2*phi))
            self.assertAlmostEqual(v[2] / z, expected, places=8)
            outcomes.append(math.atan2(v[1], v[0]) - phi)
        self.assertAlmostEqual(outcomes[0], outcomes[1], places=14)
        self.assertGreater(outcomes[0], 0)

    def test_finite_valley_controls(self):
        decayed, plain = valley_run(), valley_run(0)
        self.assertAlmostEqual(decayed[0, 3], 2.6602684919277424)
        self.assertAlmostEqual(decayed[-1, 3], 1.43613, places=5)
        self.assertAlmostEqual(plain[-1, 3], 2.65708, places=5)
        self.assertLess(np.max(abs(decayed[:, 2])), 0.037)
        self.assertLess(np.max(decayed[:, 4]), 0.002)
        self.assertTrue(np.all(decayed[:, 5] > 0))
        self.assertTrue(np.all(decayed[1:51, 2] * decayed[:50, 2] < 0))
        self.assertLess(np.max(abs(decayed[:50, 2])), 0.031)

    def test_exact_minimizer_stays_on_its_ray(self):
        original = np.array([math.cos(0.3), math.sin(0.3), 0.0])
        w = original.copy()
        for _ in range(100):
            w = 0.999 * w - 0.1 * valley_gradient(w)
        np.testing.assert_allclose(w, 0.999**100 * original, atol=1e-14)

    def test_gradient_flow_time_change(self):
        z = np.array([1.0, 0.3, 0.02])
        t, decay = 0.7, 0.2
        w = math.exp(-decay * t) * z
        wdot = -valley_gradient(w) - decay*w
        zdot = math.exp(decay*t) * (wdot + decay*w)
        np.testing.assert_allclose(zdot, -math.exp(2*decay*t) * valley_gradient(z), atol=1e-14)

    def test_sharpness_flow_chain_rule(self):
        for phi in np.linspace(0.1, 1.4, 20):
            a = 2 + 0.8 * math.cos(2*phi)
            log_derivative = -1.6 * math.sin(2*phi) / a
            velocity = -2 * log_derivative / (4 + log_derivative**2)
            decrease = log_derivative * velocity
            self.assertAlmostEqual(decrease, -2 * log_derivative**2 / (4 + log_derivative**2))
            self.assertTrue(-2 < decrease <= 0)


class OptimizerSymmetryChecks(unittest.TestCase):
    def test_covector_vector_and_mobility_transform(self):
        t = np.array([[2.0, 0.5], [0, 0.4]])
        g, mobility = np.array([0.3, -0.7]), np.array([[2.0, 0.2], [0.2, 1]])
        transformed_g = np.linalg.solve(t.T, g)
        transformed_p = t @ mobility @ t.T
        np.testing.assert_allclose(-transformed_p @ transformed_g, t @ (-mobility @ g))
        self.assertGreater(np.linalg.norm(-transformed_g - t @ (-g)), 0.1)

    def test_sgd_ema_scale_covariance_over_a_sequence(self):
        eta, decay, c = 0.01, 0.02, 3.0
        w, m = np.array([1.0, 0.3, 0.02]), np.array([0.01, -0.02, 0.03])
        transformed, transformed_m = c*w, m/c
        for _ in range(30):
            m = 0.9*m + 0.1*valley_gradient(w)
            transformed_m = 0.9*transformed_m + 0.1*valley_gradient(transformed)
            w = (1-eta*decay)*w - eta*m
            transformed = (1-eta*decay)*transformed - c*c*eta*transformed_m
            np.testing.assert_allclose(transformed, c*w, atol=1e-13)
            np.testing.assert_allclose(transformed_m, m/c, atol=1e-14)

    def test_adam_moments_damping_and_rate_scale(self):
        m, v, eps, c = np.array([0.1, -0.2]), np.array([0.04, 0.25]), 0.03, 3
        original = m / (np.sqrt(v) + eps)
        matched = (m/c) / (np.sqrt(v/c**2) + eps/c)
        np.testing.assert_allclose(matched, original)
        unmatched = (m/c) / (np.sqrt(v/c**2) + eps)
        self.assertGreater(np.linalg.norm(unmatched-original), 0.02)
        w, eta, a = np.array([1.0, 0.4]), 0.01, 0.999
        np.testing.assert_allclose(a*c*w - c*eta*matched, c*(a*w-eta*original))

    def test_rotation_example_and_realizable_second_moment(self):
        m, c = np.array([0.5, 1]), np.diag([1.0, 9])
        self.assertGreater(np.linalg.eigvalsh(c-np.outer(m,m)).min(), 0)
        diagonal, full = rotation_defects([0, math.pi/4, math.pi/2])
        self.assertAlmostEqual(diagonal[1], 0.4974573030771096)
        np.testing.assert_allclose(diagonal[[0, 2]], 0, atol=1e-14)
        np.testing.assert_allclose(full, 0, atol=1e-14)

    def test_full_moment_ema_rotation_covariance(self):
        rng = np.random.default_rng(24)
        o = rotation(0.7)
        m, c = np.zeros(2), np.eye(2)
        rotated_m, rotated_c = np.zeros(2), np.eye(2)
        for _ in range(30):
            g = rng.normal(size=2)
            m, c = 0.8*m + 0.2*g, 0.9*c + 0.1*np.outer(g,g)
            rg = o @ g
            rotated_m = 0.8*rotated_m + 0.2*rg
            rotated_c = 0.9*rotated_c + 0.1*np.outer(rg,rg)
            np.testing.assert_allclose(rotated_c, o @ c @ o.T, atol=1e-14)
            np.testing.assert_allclose(moment_direction(rotated_m,rotated_c,0.01), o @ moment_direction(m,c,0.01), atol=1e-13)

    def test_diagonal_state_loses_rotated_correlations(self):
        c1, c2 = np.array([[2.0, 0.7], [0.7, 2]]), np.array([[2.0, -0.7], [-0.7, 2]])
        np.testing.assert_allclose(np.diag(c1), np.diag(c2))
        o = rotation(math.pi/4)
        self.assertGreater(np.linalg.norm(np.diag(o @ c1 @ o.T)-np.diag(o @ c2 @ o.T)), 1)

    def test_translation_equivariance_is_not_horizontality(self):
        logits = np.zeros(3)
        labels = np.array([1,0,0])
        g = softmax(logits) - labels
        direction = -np.sign(g)
        self.assertAlmostEqual(direction.sum(), -1)
        horizontal = direction - direction.mean()
        self.assertAlmostEqual(horizontal.sum(), 0)
        np.testing.assert_allclose(softmax(logits+0.1*direction), softmax(logits+0.1*horizontal), atol=1e-14)
        shifted = logits+4
        shifted_g = softmax(shifted)-labels
        np.testing.assert_allclose(shifted-0.1*np.sign(shifted_g), logits+0.1*direction+4)

    def test_attention_rotation_and_position_operator_boundary(self):
        rng = np.random.default_rng(240)
        q, k = rng.normal(size=(3,4)), rng.normal(size=(3,4))
        o = np.eye(4)
        o[np.ix_([0,2],[0,2])] = rotation(0.6)
        np.testing.assert_allclose((q @ o) @ (k @ o).T, q @ k.T, atol=1e-14)
        positional = np.zeros((4,4))
        positional[:2,:2], positional[2:,2:] = rotation(0.2), rotation(0.7)
        self.assertGreater(np.linalg.norm(o @ positional - positional @ o), 0.1)
        self.assertGreater(np.linalg.norm((q @ o) @ positional @ (k @ o).T-q @ positional @ k.T), 0.1)


if __name__ == '__main__':
    unittest.main()
