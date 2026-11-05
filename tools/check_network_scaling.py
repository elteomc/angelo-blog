"""Verify the residual, width-scaling, and normalized-head worked examples."""
import math
import unittest

import numpy as np


def residual_value(depth, t, weight=0.5, step=0.2):
    return (1 + (weight - 1 + t * step) / depth) ** depth


def residual_rows():
    rows = []
    for depth in [1, 2, 4, 8, 16, 32, 64, 128]:
        derivative = 0.2 * (1 - 0.5 / depth) ** (depth - 1)
        remainder = residual_value(depth, 1) - residual_value(depth, 0) - derivative
        rows.append((depth, remainder, 0.02 * (1 - 1 / depth)))
    return rows


def packed_rotation(alpha, dimension=4):
    matrix = np.eye(dimension)
    matrix[1:3, 1:3] = [[math.cos(alpha), math.sin(alpha)],
                        [-math.sin(alpha), math.cos(alpha)]]
    return matrix


def unit(vector):
    return vector / np.linalg.norm(vector)


def angle(left, right):
    return math.acos(float(np.clip(unit(left) @ unit(right), -1, 1)))


def projection_kappa(matrix, feature):
    return np.linalg.norm(matrix, 2) * np.linalg.norm(feature) / np.linalg.norm(matrix @ feature)


def normalization_jacobian(vector, epsilon=0):
    size = math.sqrt(vector @ vector + epsilon)
    return np.eye(len(vector)) / size - np.outer(vector, vector) / size**3


class NetworkScalingChecks(unittest.TestCase):
    def test_composition_budget_and_mixed_curvature(self):
        x, w1, w2, d1, d2 = 0.7, 0.4, 0.6, 0.03, -0.08
        fn = lambda t: (w2 + t * d2) * (w1 + t * d1) * x
        step = 1e-4
        derivative = w2 * d1 * x + d2 * w1 * x
        self.assertAlmostEqual((fn(step) - fn(-step)) / (2 * step), derivative, places=10)
        second = (fn(step) - 2 * fn(0) + fn(-step)) / step**2
        self.assertAlmostEqual(second, 2 * d1 * d2 * x, places=7)
        self.assertNotEqual(second, 0)

    def test_residual_derivatives_against_polynomial(self):
        for depth in [1, 2, 4, 17]:
            base = 1 - 0.5 / depth
            coefficients = [math.comb(depth, k) * base**(depth - k) * (0.2 / depth)**k
                            for k in range(depth + 1)]
            first = coefficients[1]
            self.assertAlmostEqual(first, 0.2 * base**(depth - 1), places=13)
            second = 2 * coefficients[2] if depth > 1 else 0
            expected = 0.04 * (depth - 1) / depth * base**(depth - 2)
            self.assertAlmostEqual(second, expected, places=13)
            self.assertAlmostEqual(sum(coefficients), residual_value(depth, 1), places=13)

    def test_heterogeneous_stack_against_product_rule(self):
        rng = np.random.default_rng(16)
        for depth in [2, 5, 20]:
            weights = rng.uniform(0.1, 0.7, depth)
            changes = rng.uniform(-0.05, 0.05, depth)
            for t in [0, 0.4, 1]:
                factors = 1 + (weights + t * changes - 1) / depth
                derivatives = changes / depth
                value, first, second = 1.0, 0.0, 0.0
                for factor, d in zip(factors, derivatives):
                    value, first, second = (factor * value,
                                            factor * first + d * value,
                                            factor * second + 2 * d * first)
                ratios = derivatives / factors
                expected_first = np.prod(factors) * sum(ratios)
                expected_second = np.prod(factors) * (sum(ratios)**2 - sum(ratios**2))
                self.assertAlmostEqual(first, expected_first, places=13)
                self.assertAlmostEqual(second, expected_second, places=13)
                self.assertLessEqual(abs(first), max(abs(changes)) + 1e-14)
                self.assertLessEqual(abs(second), (1 - 1 / depth) * max(abs(changes))**2 + 1e-14)

    def test_curvature_finite_sums(self):
        for depth in [1, 2, 7, 100]:
            a, b, c = 0.3, 0.7, 1.2
            direct = sum((a + 2 * b * j / depth + c * (j / depth)**2) / depth
                         for j in range(depth))
            closed = a + b * (depth - 1) / depth + c * (depth - 1) * (2 * depth - 1) / (6 * depth**2)
            self.assertAlmostEqual(direct, closed, places=13)
            self.assertLessEqual(closed, a + b + c / 3)

    def test_residual_remainder_and_region(self):
        for depth, remainder, bound in residual_rows():
            self.assertGreaterEqual(remainder, -1e-14)
            self.assertLessEqual(remainder, bound + 1e-13)
            for t in np.linspace(0, 1, 21):
                self.assertTrue(0 <= 0.5 + 0.2 * t <= 1)
                self.assertTrue(0 <= residual_value(depth, t) <= 1)
        self.assertAlmostEqual(residual_rows()[1][1], 0.01)
        self.assertAlmostEqual(math.exp(-0.3) - 1.2 * math.exp(-0.5), 0.0129814290265578)

    def test_loss_chain_rule_and_taylor_bound(self):
        for depth in [1, 2, 8, 64]:
            target = 0.3
            y0, y1 = residual_value(depth, 0), residual_value(depth, 1)
            yprime = 0.2 * (1 - 0.5 / depth)**(depth - 1)
            loss = lambda t: 0.5 * (residual_value(depth, t) - target)**2
            ysecond = 0.04 * (depth - 1) / depth * (1 - 0.5 / depth)**(depth - 2)
            expected = yprime**2 + (y0 - target) * ysecond
            dt = 1e-4
            self.assertAlmostEqual((loss(dt) - 2 * loss(0) + loss(-dt)) / dt**2, expected, places=6)
            remainder = 0.5 * (y1 - target)**2 - loss(0) - (y0 - target) * yprime
            self.assertLessEqual(abs(remainder), 0.5 * (1 + 1 - 1 / depth) * 0.2**2 + 1e-13)

    def test_averaged_periodic_convolution_bound(self):
        rng = np.random.default_rng(160)
        x = rng.normal(size=(3, 11))
        slices = rng.normal(size=(5, 2, 3))
        result = sum(slices[k] @ np.roll(x, k - 2, axis=1) for k in range(5)) / 5
        budget = max(np.linalg.norm(s, 2) for s in slices)
        self.assertLessEqual(np.linalg.norm(result), budget * np.linalg.norm(x))

    def test_equal_operator_norms_different_feature_action(self):
        v, z = np.eye(4)[:2]
        u = np.array([0.6, 0.8])
        aligned, orthogonal = np.outer(u, v), np.outer(u, z)
        self.assertAlmostEqual(np.linalg.norm(aligned, 2), np.linalg.norm(orthogonal, 2))
        self.assertAlmostEqual(np.linalg.norm(aligned @ (2 * v)), 2)
        np.testing.assert_allclose(orthogonal @ (2 * v), 0)

    def test_single_example_gradient_alignment(self):
        h, delta = np.array([1, 2, -3.0]), np.array([0.2, -0.7])
        g = np.outer(delta, h)
        self.assertAlmostEqual(np.linalg.norm(g @ h), np.linalg.norm(g, 2) * np.linalg.norm(h))
        other = np.cross(h, [1, 0, 0])
        np.testing.assert_allclose(g @ other, 0, atol=1e-14)

    def test_moving_feature_cancellation(self):
        w, h, dw, dh = 1.0, 1.0, 0.1, -1 / 11
        self.assertAlmostEqual(dw * h + w * dh + dw * dh, 0)
        self.assertNotEqual(dw * h, 0)

    def test_square_width_table(self):
        for width in [16, 64, 256, 1024]:
            h = np.ones(width)
            g = np.ones((width, width)) / width
            rms = lambda x: np.linalg.norm(x) / math.sqrt(width)
            self.assertAlmostEqual(rms(0.01 * g @ h), 0.01)
            self.assertAlmostEqual(rms(0.01 * np.sign(g) @ h), 0.01 * width)
            self.assertAlmostEqual(rms(0.01 / width * np.sign(g) @ h), 0.01)
        u, singular, vh = np.linalg.svd(np.ones((16, 16)) / 16, full_matrices=False)
        polar = u[:, singular > 1e-10] @ vh[singular > 1e-10]
        np.testing.assert_allclose(polar, np.ones((16, 16)) / 16, atol=1e-14)

    def test_rectangular_rates_and_quotient(self):
        for m, n in [(8, 32), (32, 8), (7, 7)]:
            g, h = np.ones((m, n)) / m, np.ones(n)
            polar = np.ones((m, n)) / math.sqrt(m * n)
            for proposal, rate in [(g, 0.01 * m / n),
                                   (polar, 0.01 * math.sqrt(m / n)),
                                   (np.sign(g), 0.01 / n)]:
                raw_from_norm = 0.01 * math.sqrt(m / n) / np.linalg.norm(proposal, 2)
                self.assertAlmostEqual(rate, raw_from_norm)
                self.assertAlmostEqual(np.linalg.norm(rate * proposal @ h) / math.sqrt(m), 0.01)

    def test_stabilized_sign_regimes(self):
        for width in [16, 64, 256]:
            g = np.ones((width, width)) / width
            for eps in [0.01, 0.16 / width]:
                proposal = g / (abs(g) + eps)
                actual = np.linalg.norm(0.01 / width * proposal @ np.ones(width)) / math.sqrt(width)
                self.assertAlmostEqual(actual, 0.01 / (1 + width * eps))
            self.assertAlmostEqual(0.01 / (1 + width * (0.16 / width)), 0.01 / 1.16)

    def test_normalization_jacobian_by_finite_difference(self):
        z, direction = np.array([0.3, -0.4, 0.8]), np.array([0.2, 0.1, -0.5])
        dt = 1e-6
        observed = (unit(z + dt * direction) - unit(z - dt * direction)) / (2 * dt)
        np.testing.assert_allclose(observed, normalization_jacobian(z) @ direction, atol=1e-9)
        np.testing.assert_allclose(normalization_jacobian(z) @ z, 0, atol=1e-14)

    def test_spectral_witness_attains_sensitivity(self):
        a = np.array([[1, 0, 0], [0, 1, 0.0]])
        h = np.array([0.02, 0, math.sqrt(1 - 0.02**2)])
        eta, transverse = 0.003, np.array([0, 1.0])
        da = eta * np.linalg.norm(a, 2) * np.outer(transverse, unit(h))
        self.assertAlmostEqual(np.linalg.norm(da, 2), eta * np.linalg.norm(a, 2))
        actual = np.linalg.norm(normalization_jacobian(a @ h) @ da @ h)
        self.assertAlmostEqual(actual, eta * projection_kappa(a, h))

    def test_projection_margin_and_scale_invariance(self):
        a = np.eye(3)[:2]
        np.testing.assert_allclose(a @ a.T, np.eye(2))
        for eps in [0.01, 0.2, 1]:
            h = np.array([eps, 0, math.sqrt(1 - eps**2)])
            self.assertAlmostEqual(projection_kappa(a, h), 1 / eps)
            self.assertAlmostEqual(projection_kappa(10 * a, h), projection_kappa(a, h))

    def test_packed_rotation_exact_angles(self):
        alpha = 0.01
        q = packed_rotation(alpha)
        np.testing.assert_allclose(q.T @ q, np.eye(4), atol=1e-14)
        self.assertAlmostEqual(np.linalg.norm(q - np.eye(4), 2), 2 * math.sin(alpha / 2))
        matrix_angle = angle(np.eye(4).ravel(), q.ravel())
        self.assertAlmostEqual(matrix_angle, math.acos((2 + 2 * math.cos(alpha)) / 4))
        for kappa in [1, 10, 100, 1000]:
            eps = 1 / kappa
            h = np.array([eps, 0, math.sqrt(1 - eps**2), 0])
            expected = math.atan(abs(math.sin(alpha)) * math.sqrt(kappa**2 - 1))
            self.assertAlmostEqual(angle(h[:2], (q @ h)[:2]), expected, places=10)

    def test_tangent_support_and_polar_retraction(self):
        j = np.zeros((4, 4))
        j[1, 2], j[2, 1] = 1, -1
        np.testing.assert_allclose(j + j.T, 0)
        self.assertAlmostEqual(np.linalg.norm(j, 2), 1)
        self.assertAlmostEqual(np.sum((-j) * j), -np.linalg.svd(j, compute_uv=False).sum())
        for t in [0.01, 0.2]:
            u, _, vh = np.linalg.svd(np.eye(4) + t * j)
            np.testing.assert_allclose(u @ vh, packed_rotation(math.atan(t)), atol=1e-14)

    def test_finite_angle_bound_and_sharpness(self):
        z = np.array([1.0, 0])
        for bound in [0.01, 0.2, 0.8]:
            tangent_point = np.array([1 - bound**2, bound * math.sqrt(1 - bound**2)])
            self.assertAlmostEqual(np.linalg.norm(tangent_point - z), bound)
            self.assertAlmostEqual(angle(z, tangent_point), math.asin(bound))
            for theta in np.linspace(0, 2 * math.pi, 101):
                zp = z + bound * np.array([math.cos(theta), math.sin(theta)])
                self.assertLessEqual(angle(z, zp), math.asin(bound) + 1e-12)

    def test_moving_input_finite_bound(self):
        rng = np.random.default_rng(18)
        a = np.array([[1, 0.1, 0], [0, 1, 0.2]])
        for _ in range(50):
            h = rng.normal(size=3)
            eta, tau = 0.01, 0.02
            da = rng.normal(size=a.shape)
            da *= eta * np.linalg.norm(a, 2) / np.linalg.norm(da, 2)
            dh = tau * np.linalg.norm(h) * unit(rng.normal(size=3))
            before, after = a @ h, (a + da) @ (h + dh)
            bound = projection_kappa(a, h) * (eta + tau + eta * tau)
            self.assertLessEqual(np.linalg.norm(after - before) / np.linalg.norm(before), bound + 1e-14)
            if bound < 1:
                self.assertLessEqual(angle(before, after), math.asin(bound) + 1e-12)

    def test_cross_term_is_required(self):
        eta, tau = 0.1, 0.2
        relative = (1 + eta) * (1 + tau) - 1
        self.assertGreater(relative, eta + tau)
        self.assertAlmostEqual(relative, eta + tau + eta * tau)
        self.assertAlmostEqual(5 * (0.01 + 0.02 + 0.01 * 0.02), 0.151)

    def test_stabilized_jacobian_eigenvalues(self):
        z, eps = np.array([0.3, 0.4]), 0.01
        jac = normalization_jacobian(z, eps)
        s = math.sqrt(z @ z + eps)
        np.testing.assert_allclose(jac @ unit(z), eps / s**3 * unit(z), atol=1e-14)
        np.testing.assert_allclose(jac @ np.array([-0.8, 0.6]), np.array([-0.8, 0.6]) / s)
        np.testing.assert_allclose(normalization_jacobian(np.zeros(2), eps), np.eye(2) / math.sqrt(eps))
        fn = lambda v: v / math.sqrt(v @ v + eps)
        d = np.array([0.2, -0.1])
        observed = (fn(z + 1e-6 * d) - fn(z - 1e-6 * d)) / 2e-6
        np.testing.assert_allclose(observed, jac @ d, atol=1e-9)

    def test_scalar_normalization_has_no_transverse_direction(self):
        np.testing.assert_allclose(normalization_jacobian(np.array([0.3])), 0, atol=1e-14)
        self.assertEqual(float(unit(np.array([0.3]))[0]), 1)
        self.assertEqual(float(unit(np.array([-0.3]))[0]), -1)


if __name__ == '__main__':
    unittest.main()
