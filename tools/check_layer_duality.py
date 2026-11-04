"""Verify the activation geometry and dual support calculations in parts 5 and 6."""
import unittest
import numpy as np


def pairing(left, right):
    return float(np.sum(left * right))


def op(matrix):
    return float(np.linalg.norm(matrix, ord=2))


def fro(matrix):
    return float(np.linalg.norm(matrix, ord='fro'))


def nuclear(matrix):
    return float(np.linalg.norm(matrix, ord='nuc'))


def polar(matrix):
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    if not singular.size or singular[0] == 0:
        return np.zeros_like(matrix)
    active = singular > np.finfo(float).eps * max(matrix.shape) * singular[0]
    return u[:, active] @ vh[active, :]


class LayerDualityChecks(unittest.TestCase):
    def test_equal_frobenius_sizes_differ_in_worst_case(self):
        a = np.diag([1.0, 0.0])
        b = np.eye(2) / np.sqrt(2)
        self.assertAlmostEqual(fro(a), 1)
        self.assertAlmostEqual(fro(b), 1)
        self.assertAlmostEqual(op(a), 1)
        self.assertAlmostEqual(op(b), 1 / np.sqrt(2))
        theta = np.arange(2048) * (2 * np.pi / 2048)
        inputs = np.vstack([np.cos(theta), np.sin(theta)])
        for matrix in (a, b):
            self.assertAlmostEqual(np.mean(np.sum((matrix @ inputs)**2, axis=0)), 0.5)
        a4 = np.diag([1.0, 0.0, 0.0, 0.0])
        b4 = np.eye(4) / 2
        self.assertAlmostEqual(op(a4), 1)
        self.assertAlmostEqual(op(b4), 0.5)
        self.assertAlmostEqual(fro(a4)**2 / 4, 0.25)
        self.assertAlmostEqual(fro(b4)**2 / 4, 0.25)

    def test_second_moment_identity_with_a_nonzero_mean(self):
        matrix = np.array([[2.0, -0.5], [1.0, 1.0]])
        samples = np.array([[2.0, 1.0], [-1.0, 3.0], [0.5, -2.0]])
        second_moment = samples.T @ samples / len(samples)
        direct = np.mean(np.sum((samples @ matrix.T)**2, axis=1))
        self.assertAlmostEqual(direct, np.trace(matrix @ second_moment @ matrix.T))
        mean = samples.mean(axis=0)
        covariance = second_moment - np.outer(mean, mean)
        self.assertGreater(abs(direct - np.trace(matrix @ covariance @ matrix.T)), 0.1)

    def test_rms_width_factors_and_their_attaining_inputs(self):
        for n, m, expected in [(4, 16, 0.5), (16, 4, 2.0), (9, 4, 1.5)]:
            matrix = np.zeros((m, n))
            matrix[0, 0] = 1
            x = np.zeros(n)
            x[0] = np.sqrt(n)
            self.assertAlmostEqual(np.linalg.norm(x) / np.sqrt(n), 1)
            self.assertAlmostEqual(np.linalg.norm(matrix @ x) / np.sqrt(m), expected)
            self.assertAlmostEqual(np.sqrt(n / m) * op(matrix), expected)
        self.assertAlmostEqual(0.1 * np.sqrt(4 / 9), 1 / 15)

    def test_embedding_and_dense_domains_answer_different_questions(self):
        matrix = np.array([[1.0, 1.0], [0.0, 0.0]])
        self.assertAlmostEqual(np.max(np.linalg.norm(matrix, axis=0)), 1)
        self.assertAlmostEqual(op(matrix), np.sqrt(2))
        self.assertAlmostEqual(np.linalg.norm(matrix @ (np.ones(2) / np.sqrt(2))), np.sqrt(2))
        self.assertAlmostEqual(np.max(np.linalg.norm(matrix, axis=0)) / np.sqrt(2), 1 / np.sqrt(2))
        rng = np.random.default_rng(47)
        for _ in range(80):
            x = rng.normal(size=2)
            self.assertLessEqual(np.linalg.norm(matrix @ x), np.linalg.norm(x, 1) + 1e-12)

    def test_moving_input_requires_the_cross_term(self):
        w = np.array([[1.0, 2.0], [-0.5, 0.3]])
        delta = np.array([[0.2, -0.1], [0.4, 0.2]])
        x = np.array([0.4, -0.6])
        dx = np.array([0.3, 0.1])
        change = (w + delta) @ (x + dx) - w @ x
        differential = delta @ x + w @ dx
        np.testing.assert_allclose(change - differential, delta @ dx)
        self.assertGreater(np.linalg.norm(change - differential), 0.01)
        bound = op(delta) * np.linalg.norm(x) + op(w) * np.linalg.norm(dx) + op(delta) * np.linalg.norm(dx)
        self.assertLessEqual(np.linalg.norm(change), bound)

    def test_polar_support_for_rectangular_matrices(self):
        rng = np.random.default_rng(48)
        for shape in [(2, 5), (5, 2), (3, 3), (4, 7)]:
            g = rng.normal(size=shape)
            direction = polar(g)
            self.assertAlmostEqual(op(direction), 1)
            self.assertAlmostEqual(pairing(g, direction), nuclear(g))
            for _ in range(40):
                candidate = rng.normal(size=shape)
                candidate /= op(candidate)
                self.assertLessEqual(pairing(g, candidate), nuclear(g) + 1e-10)

    def test_frobenius_and_nuclear_support(self):
        rng = np.random.default_rng(49)
        for shape in [(2, 5), (5, 2), (3, 3)]:
            g = rng.normal(size=shape)
            d_f = g / fro(g)
            u, singular, vh = np.linalg.svd(g, full_matrices=False)
            d_n = np.outer(u[:, 0], vh[0, :])
            self.assertAlmostEqual(fro(d_f), 1)
            self.assertAlmostEqual(pairing(g, d_f), fro(g))
            self.assertAlmostEqual(nuclear(d_n), 1)
            self.assertAlmostEqual(pairing(g, d_n), singular[0])
            for _ in range(40):
                candidate = rng.normal(size=shape)
                self.assertLessEqual(pairing(g, candidate / fro(candidate)), fro(g) + 1e-10)
                self.assertLessEqual(pairing(g, candidate / nuclear(candidate)), op(g) + 1e-10)

    def test_printed_three_budget_example(self):
        g = np.diag([3.0, 1.0])
        f_step = -0.1 * g / fro(g)
        op_step = -0.1 * polar(g)
        n_step = -0.1 * np.diag([1.0, 0.0])
        self.assertAlmostEqual(pairing(g, f_step), -0.1 * np.sqrt(10))
        self.assertAlmostEqual(pairing(g, op_step), -0.4)
        self.assertAlmostEqual(pairing(g, n_step), -0.3)
        self.assertAlmostEqual(fro(op_step), 0.1 * np.sqrt(2))
        self.assertAlmostEqual(pairing(g, g / op(g)), 10 / 3)
        self.assertLess(pairing(g, g / op(g)), pairing(g, polar(g)))

    def test_rank_deficient_and_zero_gradients(self):
        g = np.diag([3.0, 0.0])
        np.testing.assert_allclose(polar(g), np.diag([1.0, 0.0]))
        self.assertAlmostEqual(pairing(g, np.eye(2)), pairing(g, polar(g)))
        self.assertAlmostEqual(op(np.eye(2)), 1)
        np.testing.assert_array_equal(polar(np.zeros((2, 4))), np.zeros((2, 4)))
        rectangular = np.outer([1.0, 2.0, -1.0], [2.0, 0.5])
        self.assertAlmostEqual(fro(polar(rectangular)), 1)
        self.assertAlmostEqual(pairing(rectangular, polar(rectangular)), nuclear(rectangular))

    def test_scaled_norm_uses_the_reciprocal_in_its_dual(self):
        rng = np.random.default_rng(50)
        for m, n in [(4, 9), (9, 4), (2, 2)]:
            g = rng.normal(size=(m, n))
            k = np.sqrt(n / m)
            d = polar(g) / k
            self.assertAlmostEqual(k * op(d), 1)
            self.assertAlmostEqual(pairing(g, d), nuclear(g) / k)

    def test_embedding_duality_normalizes_each_column(self):
        g = np.array([[3.0, 0.0, 0.0], [4.0, 2.0, 0.0]])
        lengths = np.linalg.norm(g, axis=0)
        d = np.divide(g, lengths, out=np.zeros_like(g), where=lengths > 0)
        self.assertAlmostEqual(pairing(g, d), 7)
        np.testing.assert_allclose(d[:, 0], [0.6, 0.8])
        np.testing.assert_allclose(d[:, 1], [0, 1])
        np.testing.assert_allclose(d[:, 2], [0, 0])
        self.assertAlmostEqual(np.max(np.linalg.norm(d, axis=0)), 1)
        rms_direction = np.sqrt(2) * d
        self.assertAlmostEqual(np.max(np.linalg.norm(rms_direction, axis=0)) / np.sqrt(2), 1)
        self.assertAlmostEqual(pairing(g, rms_direction), 7 * np.sqrt(2))

    def test_squared_norm_model_and_finite_step_overshoot(self):
        g = np.diag([3.0, 1.0])
        eta = 0.2
        rng = np.random.default_rng(51)
        for size, dual, d in [(fro, fro, g / fro(g)), (op, nuclear, polar(g))]:
            optimum = -eta * dual(g) * d
            objective = lambda delta: pairing(g, delta) + size(delta)**2 / (2 * eta)
            expected = -eta * dual(g)**2 / 2
            self.assertAlmostEqual(objective(optimum), expected)
            for _ in range(100):
                candidate = rng.normal(size=g.shape)
                self.assertGreaterEqual(objective(candidate), expected - 1e-10)
        delta = -5 * np.eye(2)
        self.assertAlmostEqual((fro(g + delta)**2 - fro(g)**2) / 2, 5)
        self.assertAlmostEqual(pairing(g, delta), -20)
        self.assertGreater(pairing(g, -0.1 * polar(-g)), 0)


if __name__ == '__main__':
    unittest.main()
