"""Check the numerical examples for practical polar, averaging, and norm budgets."""
import itertools
import math
import unittest
import numpy as np


def cubic(x):
    return 1.5 * x - 0.5 * x**3


def quintic(x):
    return (15 * x - 10 * x**3 + 3 * x**5) / 8


def scalar_trace(singular, steps=24, degree=3):
    singular = np.asarray(singular, dtype=float)
    size = np.linalg.norm(singular)
    values = singular / size if size else np.zeros_like(singular)
    records = [values.copy()]
    transform = cubic if degree == 3 else quintic
    for _ in range(steps):
        values = transform(values)
        records.append(values.copy())
    return np.array(records)


def matrix_iteration(matrix, steps, degree=3, side='smaller'):
    matrix = np.asarray(matrix, dtype=float)
    size = np.linalg.norm(matrix)
    if not size:
        return np.zeros_like(matrix)
    x = matrix / size
    left = matrix.shape[0] <= matrix.shape[1] if side == 'smaller' else side == 'left'
    for _ in range(steps):
        gram = x @ x.T if left else x.T @ x
        if degree == 3:
            x = 1.5 * x - 0.5 * (gram @ x if left else x @ gram)
        else:
            poly = -1.25 * gram + 0.375 * (gram @ gram)
            x = 1.875 * x + (poly @ x if left else x @ poly)
    return x


def partial_polar(matrix):
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    if not singular.size or singular[0] == 0:
        return np.zeros_like(matrix)
    active = singular > np.finfo(float).eps * max(matrix.shape) * singular[0]
    return u[:, active] @ vh[active]


def expected_unit_step(batch):
    value = 0.0
    for count in range(batch + 1):
        probability = math.comb(batch, count) * 0.25**count * 0.75**(batch - count)
        sign = 1 if 5 * count < batch else -1 if 5 * count > batch else 0
        value += sign * probability
    return value


def polar_rows():
    singular = np.array([1, 0.1, 0.001, 0.0])
    traces = scalar_trace(singular)
    return [(k, float(max(abs(1 - traces[k, :3]))), float(singular @ traces[k] / singular.sum())) for k in [0, 5, 10, 20, 24]]


class PracticalFollowupChecks(unittest.TestCase):
    def test_classical_scalar_maps_and_local_errors(self):
        grid = np.linspace(0, 1, 1001)
        for transform in [cubic, quintic]:
            values = transform(grid)
            self.assertGreaterEqual(values.min(), 0)
            self.assertLessEqual(values.max(), 1 + 1e-14)
            self.assertTrue(np.all(values >= grid - 1e-14))
        e = np.linspace(0, 1, 21)
        np.testing.assert_allclose(1 - cubic(1 - e), 1.5 * e**2 - 0.5 * e**3, atol=1e-14)
        np.testing.assert_allclose(1 - quintic(1 - e), 2.5 * e**3 - 15 / 8 * e**4 + 3 / 8 * e**5, atol=1e-14)
        self.assertEqual(cubic(0.5), 11 / 16)
        self.assertEqual(cubic(0), 0)

    def test_rectangular_matrix_iterations_match_scalar_svd(self):
        rng = np.random.default_rng(1315)
        for shape in [(3, 7), (7, 3), (4, 4)]:
            matrix = rng.normal(size=shape)
            u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
            for degree in [3, 5]:
                for steps in [1, 5, 12]:
                    amplitudes = scalar_trace(singular, steps, degree)[-1]
                    reference = (u * amplitudes) @ vh
                    for side in ['left', 'right', 'smaller']:
                        np.testing.assert_allclose(matrix_iteration(matrix, steps, degree, side), reference, atol=2e-13)

    def test_rank_and_zero_conventions(self):
        matrix = np.diag([1.0, 0.1, 0.001, 0])
        target = np.diag([1.0, 1, 1, 0])
        np.testing.assert_array_equal(partial_polar(matrix), target)
        for degree in [3, 5]:
            result = matrix_iteration(matrix, 30, degree)
            np.testing.assert_allclose(result, target, atol=1e-12)
            self.assertEqual(result[-1, -1], 0)
            np.testing.assert_array_equal(matrix_iteration(np.zeros((2, 5)), 8, degree), np.zeros((2, 5)))
        self.assertEqual(np.linalg.norm(target.T @ target - np.eye(4), 2), 1)

    def test_finite_polar_table_and_budget(self):
        for k, error, support in polar_rows():
            self.assertGreaterEqual(error, -1e-12)
            self.assertLessEqual(support, 1 + 1e-12)
            self.assertLessEqual(np.linalg.norm(matrix_iteration(np.diag([1.0, 0.1, 0.001, 0]), k), 2), 1 + 1e-12)
        self.assertGreater(polar_rows()[1][1], 0.99)
        self.assertLess(polar_rows()[-1][1], 1e-10)

    def test_support_error_and_current_gradient_differ(self):
        epsilon = 0.001
        m = np.diag([1.0, epsilon])
        p = np.eye(2)
        d = np.diag([1.0, 0])
        self.assertEqual(np.linalg.norm(p - d, 2), 1)
        self.assertAlmostEqual(np.sum(m * (p - d)), epsilon)
        g = np.diag([0.0, 1])
        self.assertEqual(np.sum(g * p), 1)
        self.assertEqual(np.sum(g * d), 0)

    def test_gram_sizes_and_illustrative_overshoot(self):
        self.assertEqual(2048**2 / 512**2, 16)
        self.assertEqual(1024**2 / 128**2, 64)
        self.assertAlmostEqual(2 * 0.8 - 0.8**3, 1.088)

    def test_unbiased_gradient_and_exact_quadratic_increase(self):
        gradients = np.array([4.0, -1])
        probability = np.array([0.25, 0.75])
        self.assertEqual(probability @ gradients, 0.25)
        self.assertEqual(probability @ (-np.sign(gradients)), 0.5)
        self.assertEqual(probability @ (gradients - 0.25)**2, 75 / 16)
        for eta in [0.001, 0.1, 0.5]:
            w = 0.25
            direct = probability @ (((w - eta * np.sign(gradients))**2 - w**2) / 2)
            self.assertAlmostEqual(direct, eta / 8 + eta**2 / 2)

    def test_binomial_sum_matches_independent_enumeration(self):
        for batch in range(1, 9):
            direct = 0.0
            for samples in itertools.product([4, -1], repeat=batch):
                probability = math.prod(0.25 if x == 4 else 0.75 for x in samples)
                direct -= np.sign(sum(samples)) * probability
            self.assertAlmostEqual(direct, expected_unit_step(batch))
        self.assertEqual(expected_unit_step(1), 0.5)
        self.assertEqual(expected_unit_step(2), 0.125)
        self.assertEqual(expected_unit_step(4), -47 / 128)
        self.assertLess(expected_unit_step(256), -0.9)

    def test_ema_finite_mean_and_variance(self):
        for alpha in [1, 0.2, 0.1, 0.01]:
            for t in [1, 5, 100]:
                weights = alpha * (1 - alpha)**np.arange(t)
                self.assertAlmostEqual(weights.sum(), 1 - (1 - alpha)**t)
                self.assertAlmostEqual(weights @ weights, alpha / (2 - alpha) * (1 - (1 - alpha)**(2 * t)))
        for alpha, count in [(0.2, 9), (0.1, 19), (0.01, 199)]:
            self.assertAlmostEqual((2 - alpha) / alpha, count)

    def test_trend_lag_and_general_tracking_identity(self):
        for alpha, expected in [(0.1, -0.09), (0.01, -0.99)]:
            mean = 0.0
            for t in range(1, 6001):
                target = 0.01 * t
                mean = (1 - alpha) * mean + alpha * target
            self.assertAlmostEqual(mean - target, expected, places=10)
        rng = np.random.default_rng(1415)
        old_h, new_h, old_m, noise = rng.normal(size=(4, 6))
        alpha = 0.15
        new_m = (1 - alpha) * old_m + alpha * (new_h + noise)
        expected = (1 - alpha) * (old_m - old_h + old_h - new_h) + alpha * noise
        np.testing.assert_allclose(new_m - new_h, expected)

    def test_exact_and_approximate_support_error_bound(self):
        rng = np.random.default_rng(1416)
        for _ in range(80):
            h, m = rng.normal(size=(2, 3, 4))
            dual = lambda value: np.linalg.norm(value, 'nuc')
            exact = partial_polar(m)
            approximate = matrix_iteration(m, 4)
            for direction in [exact, approximate]:
                defect = dual(m) - np.sum(m * direction)
                self.assertGreaterEqual(defect, -1e-12)
                self.assertLessEqual(np.linalg.norm(direction, 2), 1 + 1e-12)
                self.assertGreaterEqual(np.sum(h * direction), dual(h) - 2 * dual(h - m) - defect - 1e-12)
        self.assertAlmostEqual(1 - 2 * 0.2 - 0.1, 0.5)

    def test_variable_step_norm_envelope(self):
        rng = np.random.default_rng(1515)
        for order in [1, 2, np.inf]:
            norm = lambda value: np.linalg.norm(value, ord=order)
            for initial in [0.5, 3.0]:
                rho, decay = 1.0, 0.5
                w = rng.normal(size=5)
                w *= initial / norm(w)
                product = 1.0
                for _ in range(80):
                    eta = rng.uniform(0, 1 / decay)
                    v = rng.normal(size=5)
                    v *= rho / norm(v)
                    w = (1 - eta * decay) * w + eta * v
                    product *= 1 - eta * decay
                    envelope = product * initial + rho / decay * (1 - product)
                    self.assertLessEqual(norm(w), envelope + 1e-12)

    def test_matrix_norm_budget_and_scaled_approximation(self):
        rng = np.random.default_rng(1516)
        for order in [2, 'fro', 'nuc']:
            norm = lambda value: np.linalg.norm(value, ord=order)
            for rho in [1, 1.2]:
                w = np.zeros((3, 5))
                for _ in range(50):
                    v = rng.normal(size=w.shape)
                    v *= rho / norm(v)
                    w = 0.95 * w + 0.1 * v
                    self.assertLessEqual(norm(w), rho / 0.5 + 1e-12)

    def test_conditional_gradient_equivalence(self):
        rng = np.random.default_rng(1517)
        w, constrained = np.zeros((3, 5)), np.zeros((3, 5))
        rho, decay = 1.4, 0.6
        for _ in range(60):
            m = rng.normal(size=w.shape)
            v = -rho * partial_polar(m)
            eta = rng.uniform(0, 1 / decay)
            w = (1 - eta * decay) * w + eta * v
            a = eta * decay
            constrained = (1 - a) * constrained + a * (-rho / decay * partial_polar(m))
            np.testing.assert_allclose(w, constrained, atol=1e-13)

    def test_printed_constant_proposal_and_exercises(self):
        for initial in [0.0, 5.0]:
            w = initial
            for t in range(81):
                self.assertAlmostEqual(w, 2 + (initial - 2) * 0.95**t)
                if initial == 5:
                    self.assertGreater(w, 2)
                w = 0.95 * w + 0.1
        self.assertAlmostEqual(2 * (1 - 0.95**20), 1.2830281552)
        self.assertAlmostEqual(2 + 3 * 0.95**20, 3.0754577672)
        self.assertAlmostEqual(math.log(0.5) / math.log(0.95), 13.5134073340)
        self.assertAlmostEqual(0.81 * 9 + 0.19 * 6, 8.43)

    def test_cumulative_exposure_and_separate_decay(self):
        eta = np.array([0.1, 0.2, 0.3, 0.4])
        decay = 0.5
        product = np.prod(1 - decay * eta)
        self.assertLessEqual(product, np.exp(-decay * eta.sum()))
        rho = 1.2
        for rate, shrinkage in zip(eta, decay * eta):
            self.assertAlmostEqual(rate * rho / shrinkage, rho / decay)

    def test_overshoot_and_divergence_outside_convex_range(self):
        self.assertEqual(1.5 * 2, 3)
        w = 0
        sequence = []
        for _ in range(6):
            sequence.append(w)
            w = -2 * w + 6
        self.assertEqual(sequence, [0, 6, -6, 18, -30, 66])

    def test_coupled_penalty_changes_nonlinear_oracle(self):
        w, g = np.array([1.0, 0]), np.array([0.0, 1])
        eta, decay = 0.1, 0.5
        decoupled = (1 - eta * decay) * w - eta * g / np.linalg.norm(g)
        coupled_gradient = g + decay * w
        coupled = w - eta * coupled_gradient / np.linalg.norm(coupled_gradient)
        np.testing.assert_allclose(decoupled, [0.95, -0.1])
        np.testing.assert_allclose(coupled, [0.95527864045, -0.0894427191])
        self.assertGreater(np.linalg.norm(coupled - decoupled), 0.01)


if __name__ == '__main__':
    import sys
    if '--tables' in sys.argv:
        print('Polar table')
        for row in polar_rows():
            print(row)
        print('Batch table')
        for batch in [1, 2, 4, 16, 64, 256]:
            print(batch, expected_unit_step(batch))
    else:
        unittest.main()
