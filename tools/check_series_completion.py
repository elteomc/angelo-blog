"""Check the worked examples and synthetic controls in parts 7 through 12."""
import json
from pathlib import Path
import unittest
import numpy as np

from check_layer_duality import fro, op, polar


def inverse_sqrt(matrix):
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * (1 / np.sqrt(values))) @ vectors.T


def rotation_angle(eta, rho):
    return np.arctan2(eta * np.sqrt(np.maximum(0, 1 - np.asarray(rho)**2)), 1 - eta * np.asarray(rho))


def frozen_teacher_results():
    rng = np.random.default_rng(1126)
    a = rng.normal(size=(4, 4))
    a /= fro(a)
    features = np.concatenate([2 * np.eye(4), -2 * np.eye(4)], axis=0)
    rows = []
    for ratio in np.linspace(0.25, 3, 45):
        targets = [a, ratio * a]
        norms = np.array([fro(target) for target in targets])
        gain = float(norms.mean())
        weights = [target / size for target, size in zip(targets, norms)]
        group_gain = float(np.linalg.norm(norms) / np.sqrt(2))
        group_weights = [target / group_gain for target in targets]

        def loss(effective):
            return float(sum(np.mean(np.sum((features @ (value - target).T)**2, axis=1)) for value, target in zip(effective, targets)) / 2)

        rows.append({
            'ratio': float(ratio),
            'formula': float((ratio - 1)**2 / 4),
            'individual': loss([gain * w for w in weights]),
            'group': loss([group_gain * w for w in group_weights]),
            'multipliers': loss([size * w for size, w in zip(norms, weights)]),
            'individual_radii_error': float(max(abs(fro(w) - 1) for w in weights)),
            'group_radius_squared_error': float(abs(sum(fro(w)**2 for w in group_weights) - 2)),
        })
    return rows


def attention(tokens, gain, query, key, value, output):
    q = tokens * gain * query
    k = tokens * gain * key
    v = tokens * gain * value
    scores = np.outer(q, k)
    shifted = scores - scores.max(axis=1, keepdims=True)
    probability = np.exp(shifted)
    probability /= probability.sum(axis=1, keepdims=True)
    return scores, probability @ v * output


class CompletionChecks(unittest.TestCase):
    def test_three_modular_budgets(self):
        c = np.array([2.0, 1.0])
        m = np.array([0.25, 0.75])
        g = np.array([6.0, 1.0])
        maximum = m / c
        quadratic = (m * g / c**2) / np.sqrt(np.sum(m * (g / c)**2))
        summed = np.array([0.5, 0])
        self.assertAlmostEqual(np.max(c * maximum / m), 1)
        self.assertAlmostEqual(np.sum(c * maximum), 1)
        self.assertAlmostEqual(g @ maximum, 1.5)
        self.assertAlmostEqual(np.sum(c * summed), 1)
        self.assertAlmostEqual(g @ summed, 3)
        self.assertAlmostEqual(np.sum(c**2 * quadratic**2 / m), 1)
        self.assertAlmostEqual(g @ quadratic, np.sqrt(3))
        np.testing.assert_allclose(quadratic, [0.216506350946, 0.433012701892])
        self.assertLessEqual(c @ quadratic, 1)
        equal = np.full(2, 0.5) / c
        np.testing.assert_allclose(equal, [0.25, 0.5])
        self.assertAlmostEqual(g @ equal, 2)

    def test_general_modular_support_bounds(self):
        rng = np.random.default_rng(72)
        for _ in range(100):
            c = rng.uniform(0.1, 3, 5)
            m = rng.dirichlet(np.ones(5))
            g = rng.normal(size=5)
            support = float(np.sum(m * abs(g) / c))
            direction = m * np.sign(g) / c
            self.assertAlmostEqual(g @ direction, support)
            candidate = rng.uniform(-1, 1, 5) * m / c
            self.assertLessEqual(g @ candidate, support + 1e-12)
            self.assertLessEqual(c @ abs(candidate), 1 + 1e-12)
            quadratic = m * g / c**2
            quadratic /= np.sqrt(np.sum(m * (g / c)**2))
            self.assertAlmostEqual(np.sum(c**2 * quadratic**2 / m), 1)
            self.assertLessEqual(c @ abs(quadratic), 1 + 1e-12)

    def test_sphere_projection_and_retraction(self):
        w = np.array([1.0, 0])
        z = np.array([0.0, 0.5])
        retracted = (w + z) / np.linalg.norm(w + z)
        np.testing.assert_allclose(retracted, [2 / np.sqrt(5), 1 / np.sqrt(5)])
        theta = np.arccos(w @ retracted)
        self.assertAlmostEqual(theta, np.arctan(0.5))
        self.assertAlmostEqual(np.linalg.norm(retracted - w), 2 * np.sin(theta / 2))
        w = np.array([2.0, 0, 0])
        g = np.array([3.0, 4, 1])
        tangent = g - (w @ g) * w / (w @ w)
        self.assertAlmostEqual(w @ tangent, 0)
        self.assertAlmostEqual(g @ tangent, tangent @ tangent)

    def test_stiefel_projection_retraction_and_first_order(self):
        rng = np.random.default_rng(73)
        w, _ = np.linalg.qr(rng.normal(size=(5, 3)))
        g = rng.normal(size=w.shape)
        symmetric = (w.T @ g + g.T @ w) / 2
        z = g - w @ symmetric
        np.testing.assert_allclose(w.T @ z + z.T @ w, 0, atol=1e-14)
        self.assertAlmostEqual(np.sum((g - z) * z), 0)
        np.testing.assert_allclose((w + z).T @ (w + z), np.eye(3) + z.T @ z)
        retracted = (w + z) @ inverse_sqrt((w + z).T @ (w + z))
        np.testing.assert_allclose(retracted.T @ retracted, np.eye(3), atol=1e-13)
        errors = []
        for h in [1e-3, 5e-4]:
            trial = w + h * z
            back = trial @ inverse_sqrt(trial.T @ trial)
            errors.append(fro(back - trial))
        self.assertAlmostEqual(errors[0] / errors[1], 4, places=4)

    def test_projected_polar_counterexample(self):
        g = np.array([[2.0, 1], [0, 1]])
        p = polar(g)
        np.testing.assert_allclose(p, np.array([[3, 1], [-1, 3]]) / np.sqrt(10))
        j = np.array([[0.0, 1], [-1, 0]])
        projected = (p - p.T) / 2
        np.testing.assert_allclose(projected, j / np.sqrt(10))
        self.assertAlmostEqual(op(projected), 1 / np.sqrt(10))
        self.assertAlmostEqual(np.sum(g * projected), 1 / np.sqrt(10))
        self.assertAlmostEqual(op(j), 1)
        self.assertAlmostEqual(np.sum(g * j), 1)

    def test_oblique_singular_values(self):
        phi = np.pi / 3
        w = np.array([[1.0, np.cos(phi)], [0, np.sin(phi)]])
        np.testing.assert_allclose(np.linalg.norm(w, axis=0), 1)
        np.testing.assert_allclose(np.linalg.svd(w, compute_uv=False), np.sqrt([1.5, 0.5]))
        self.assertAlmostEqual(np.linalg.cond(w), np.sqrt(3))

    def test_wrapper_angle_and_chord(self):
        for eta in [0.2, 0.5, 1.4]:
            for rho in [-1, -0.8, 0, 0.9, 1]:
                e = np.array([1.0, 0])
                u = np.array([rho, np.sqrt(max(0, 1 - rho**2))])
                trial = e - eta * u
                back = trial / np.linalg.norm(trial)
                theta = rotation_angle(eta, rho)
                self.assertAlmostEqual(theta, np.arccos(np.clip(e @ back, -1, 1)))
                self.assertAlmostEqual(np.linalg.norm(back - e), 2 * np.sin(theta / 2))
        self.assertAlmostEqual(np.degrees(rotation_angle(0.5, -0.8)), 12.094757077, places=8)
        self.assertAlmostEqual(np.degrees(rotation_angle(0.5, 0)), 26.565051177, places=8)
        self.assertAlmostEqual(2 * np.sin(rotation_angle(0.5, 0) / 2), 0.4595058411)

    def test_matched_one_step_direction(self):
        rng = np.random.default_rng(74)
        e = rng.normal(size=6)
        e /= np.linalg.norm(e)
        u = rng.normal(size=6)
        u /= np.linalg.norm(u)
        radius, decay, eta = 3, 0.9, 0.2
        alpha = decay * radius * eta
        self.assertAlmostEqual(alpha, 0.54)
        free = decay * radius * e - alpha * u
        wrapped = e - eta * u
        np.testing.assert_allclose(free / np.linalg.norm(free), wrapped / np.linalg.norm(wrapped))

    def test_scalar_factorization_changes_sgd(self):
        products = []
        for w, gain in [(1.0, 1.0), (2.0, 0.5)]:
            a = w * gain
            dw, dg = gain * a, w * a
            products.append((w - 0.1 * dw) * (gain - 0.1 * dg))
        np.testing.assert_allclose(products, [0.81, 0.585])

    def test_gain_differential_and_gauge_kernel(self):
        rng = np.random.default_rng(75)
        w = rng.normal(size=(3, 4))
        gamma = rng.uniform(0.5, 2, 4)
        dw = rng.normal(size=w.shape)
        dg = rng.normal(size=4)
        derivative = dw * gamma + w * dg
        h = 1e-5
        finite = ((w + h * dw) * (gamma + h * dg) - w * gamma) / h
        np.testing.assert_allclose(finite - derivative, h * dw * dg, atol=1e-10)
        np.testing.assert_allclose((0.3 * w) * gamma + w * (-0.3 * gamma), 0, atol=1e-15)
        self.assertLessEqual(op(derivative), np.max(abs(gamma)) * op(dw) + op(w) * np.max(abs(dg)))

    def test_positive_gain_reconstruction(self):
        targets = [np.array([[1.0, 1]]), np.array([[1.0, 2]])]
        c = np.array([[1.0, 1], [1, 4]])
        q = np.linalg.solve(c, [2, 4])
        np.testing.assert_allclose(q, [4 / 3, 2 / 3])
        gamma = 1 / np.sqrt(q)
        np.testing.assert_allclose(gamma, [0.866025403784, 1.224744871392])
        for target, radius_squared in zip(targets, [2, 4]):
            w = target * np.sqrt(q)
            np.testing.assert_allclose(w * gamma, target)
            self.assertAlmostEqual(fro(w)**2, radius_squared)
        np.testing.assert_allclose(np.linalg.solve(c, [2, 2]), [2, 0])
        self.assertFalse(np.all((q >= 0.25) & (q <= 1)))

    def test_two_branch_ratio_characterization(self):
        rng = np.random.default_rng(76)
        for _ in range(80):
            c = rng.uniform(0.1, 2, size=(2, 6))
            q = rng.uniform(0.1, 2, size=6)
            r = c @ q
            ratios = c[1] / c[0]
            weights = c[0] * q / r[0]
            self.assertAlmostEqual(weights @ ratios, r[1] / r[0])
            self.assertGreater(r[1] / r[0], ratios.min())
            self.assertLess(r[1] / r[0], ratios.max())

    def test_scalar_fitting_floor(self):
        for b, expected_gain, expected_loss in [([1, 2], 1.5, 0.25), ([1, 3], 2, 1)]:
            radii = np.ones(2)
            sizes = np.array(b)
            gain = radii @ sizes / (radii @ radii)
            loss = ((sizes @ sizes) - (radii @ sizes)**2 / (radii @ radii)) / 2
            self.assertAlmostEqual(gain, expected_gain)
            self.assertAlmostEqual(loss, expected_loss)
            for alternative in np.linspace(0, 4, 101):
                self.assertGreaterEqual(np.sum((alternative * radii - sizes)**2) / 2, loss - 1e-12)

    def test_finite_isotropic_design_and_45_teacher_controls(self):
        features = np.concatenate([2 * np.eye(4), -2 * np.eye(4)], axis=0)
        np.testing.assert_allclose(features.T @ features / 8, np.eye(4))
        rows = frozen_teacher_results()
        self.assertEqual(len(rows), 45)
        for row in rows:
            self.assertLess(abs(row['individual'] - row['formula']), 1e-12)
            self.assertLess(row['group'], 1e-25)
            self.assertLess(row['multipliers'], 1e-25)
            self.assertLess(row['individual_radii_error'], 1e-12)
            self.assertLess(row['group_radius_squared_error'], 1e-12)

    def test_attention_factorization_products(self):
        rng = np.random.default_rng(77)
        q, k, v, output = [rng.normal(size=(3, 3)) for _ in range(4)]
        s, t = rng.normal(size=(3, 3)) + 3 * np.eye(3), rng.normal(size=(3, 3)) + 3 * np.eye(3)
        np.testing.assert_allclose((s @ q).T @ np.linalg.solve(s.T, k), q.T @ k, atol=1e-12)
        np.testing.assert_allclose((output @ np.linalg.inv(t)) @ (t @ v), output @ v, atol=1e-12)

    def test_scalar_attention_escape(self):
        for tokens in [np.array([-1.0, 0.3, 1.2]), np.array([0.4]), np.linspace(-2, 2, 10)]:
            teacher_scores, teacher_output = attention(tokens, 1, 1, 2, 1, 1)
            new_scores, new_output = attention(tokens, np.sqrt(2), 1, 1, 1, 1 / np.sqrt(2))
            np.testing.assert_allclose(new_scores, teacher_scores, atol=1e-13)
            np.testing.assert_allclose(new_output, teacher_output, atol=1e-13)

    def test_rotary_middle_operator_restricts_the_gauge(self):
        phi = np.pi / 4
        r = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
        s = np.diag([2.0, 1])
        changed = s.T @ r @ np.linalg.inv(s.T)
        self.assertGreater(fro(changed - r), 0.5)
        scalar = 2 * np.eye(2)
        np.testing.assert_allclose(scalar.T @ r @ np.linalg.inv(scalar.T), r)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == '--results':
        rows = frozen_teacher_results()
        result = {
            'design': 'Eight equally weighted points plus and minus twice each coordinate vector in four dimensions',
            'seed': 1126,
            'method': 'Direct branch-output loss evaluation at analytically specified representatives',
            'max_formula_error': max(abs(r['individual'] - r['formula']) for r in rows),
            'max_group_loss': max(r['group'] for r in rows),
            'max_multiplier_loss': max(r['multipliers'] for r in rows),
            'rows': rows,
        }
        Path(sys.argv[2]).write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))
    else:
        unittest.main()
