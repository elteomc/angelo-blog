"""Check tangent oracles, attention examples, and archived experiment aggregates."""
from pathlib import Path
import json
import math
import unittest

import numpy as np


def skew(matrix):
    return (matrix - matrix.T) / 2


def partial_polar(matrix):
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    if not s.size or s[0] == 0:
        return np.zeros_like(matrix)
    active = s > np.finfo(float).eps * max(matrix.shape) * s[0]
    return u[:, active] @ vh[active]


def tangent_oracle(frame, cost):
    lifted = skew(cost @ frame.T)
    return -partial_polar(lifted) @ frame


def compressed_oracle(frame, cost):
    n, p = frame.shape
    if 2 * p > n:
        raise ValueError('The stated thin compression requires 2p at most n.')
    q, r = np.linalg.qr(np.column_stack([-frame, cost]), mode='reduced')
    j = np.block([[np.zeros((p, p)), np.eye(p)], [-np.eye(p), np.zeros((p, p))]])
    k = r @ j @ r.T / 2
    return -q @ partial_polar(k) @ (q.T @ frame)


def lift_example():
    j = np.array([[0.0, 1], [-1, 0]])
    direction = np.vstack([j, np.eye(2)]) / math.sqrt(2)
    zero = np.block([[j, -np.eye(2)], [np.eye(2), np.zeros((2, 2))]]) / math.sqrt(2)
    completed = np.block([[j, -np.eye(2)], [np.eye(2), -j]]) / math.sqrt(2)
    return direction, zero, completed


def softmax(logits):
    weights = np.exp(logits - np.max(logits))
    return weights / weights.sum()


def softmax_jacobian(probabilities):
    return np.diag(probabilities) - np.outer(probabilities, probabilities)


def logsumexp(logits):
    maximum = float(np.max(logits))
    return maximum + math.log(float(np.exp(logits - maximum).sum()))


def cross_entropy(labels, logits):
    return logsumexp(logits) - labels @ logits


def predictive_kl(old, new):
    return logsumexp(new) - logsumexp(old) - softmax(old) @ (new - old)


def experiment_record():
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / 'specs/009-tangent-constraints-evidence/experiment-record.json').read_text())


class TangentOracleChecks(unittest.TestCase):
    def test_certificate_and_tangency(self):
        rng = np.random.default_rng(19)
        for n, p in [(3, 2), (5, 2), (8, 3), (12, 2)]:
            frame = np.linalg.qr(rng.normal(size=(n, p)))[0]
            cost = rng.normal(size=(n, p))
            result = tangent_oracle(frame, cost)
            lifted = skew(cost @ frame.T)
            nuclear = np.linalg.svd(lifted, compute_uv=False).sum()
            np.testing.assert_allclose(frame.T @ result + result.T @ frame, 0, atol=2e-14)
            self.assertLessEqual(np.linalg.norm(result, 2), 1 + 1e-13)
            self.assertAlmostEqual(float(np.sum(cost * result)), -nuclear, places=12)
            for _ in range(10):
                candidate = rng.normal(size=(n, p))
                candidate -= frame @ ((frame.T @ candidate + candidate.T @ frame) / 2)
                candidate /= max(1, np.linalg.norm(candidate, 2))
                self.assertGreaterEqual(float(np.sum(cost * candidate)), -nuclear - 1e-12)

    def test_compression_against_dense_action(self):
        rng = np.random.default_rng(190)
        for n, p in [(8, 2), (12, 3), (20, 4)]:
            frame = np.linalg.qr(rng.normal(size=(n, p)))[0]
            cost = rng.normal(size=(n, p))
            np.testing.assert_allclose(compressed_oracle(frame, cost), tangent_oracle(frame, cost), atol=2e-13)

    def test_rank_deficient_compression(self):
        frame = np.eye(8)[:, :2]
        cost = np.zeros_like(frame)
        cost[2, 0] = 2
        np.testing.assert_allclose(compressed_oracle(frame, cost), tangent_oracle(frame, cost), atol=1e-14)
        with self.assertRaises(ValueError):
            compressed_oracle(np.eye(3)[:, :2], np.zeros((3, 2)))

    def test_normal_cost_and_one_column_case(self):
        frame = np.eye(5)[:, :2]
        normal = frame @ np.array([[2.0, 1], [1, -3]])
        np.testing.assert_allclose(tangent_oracle(frame, normal), 0)
        x = np.array([1, 0, 0.0])[:, None]
        cost = np.array([2, 3, 4.0])[:, None]
        np.testing.assert_allclose(tangent_oracle(x, cost), [[0], [-0.6], [-0.8]], atol=1e-14)

    def test_free_completion_block(self):
        b, zero, completed = lift_example()
        frame = np.eye(4)[:, :2]
        np.testing.assert_allclose(zero @ frame, b)
        np.testing.assert_allclose(completed @ frame, b)
        self.assertAlmostEqual(np.linalg.norm(b, 2), 1)
        self.assertAlmostEqual(np.linalg.norm(completed, 2), 1)
        self.assertAlmostEqual(np.linalg.norm(zero, 2), (1 + math.sqrt(5)) / (2 * math.sqrt(2)))
        self.assertGreater(np.linalg.norm(zero, 2), 1)

    def test_nonunique_zero_cost_kernel_action(self):
        frame = np.eye(4)[:, [0, 2]]
        cost = np.zeros_like(frame)
        cost[1, 0] = 2
        n = skew(cost @ frame.T)
        canonical = -partial_polar(n)
        other = canonical.copy()
        other[2, 3], other[3, 2] = 1, -1
        self.assertGreater(np.linalg.norm((other - canonical) @ frame), 0.9)
        for generator in [canonical, other]:
            result = generator @ frame
            np.testing.assert_allclose(frame.T @ result + result.T @ frame, 0)
            self.assertLessEqual(np.linalg.norm(result, 2), 1 + 1e-14)
            self.assertAlmostEqual(np.sum(cost * result), -2)

    def test_skewing_a_full_polar_completion(self):
        n = np.zeros((5, 5))
        n[0, 1], n[1, 0] = 2, -2
        u, _, vh = np.linalg.svd(n)
        factor = skew(u @ vh)
        self.assertLessEqual(np.linalg.norm(factor, 2), 1 + 1e-14)
        self.assertAlmostEqual(np.sum(n * factor), 4)
        np.testing.assert_allclose(factor + factor.T, 0)

    def test_retraction_and_first_derivative(self):
        rng = np.random.default_rng(191)
        frame = np.linalg.qr(rng.normal(size=(7, 3)))[0]
        direction = tangent_oracle(frame, rng.normal(size=(7, 3)))
        def retract(t):
            vals, vectors = np.linalg.eigh(np.eye(3) + t**2 * direction.T @ direction)
            return (frame + t * direction) @ ((vectors / np.sqrt(vals)) @ vectors.T)
        np.testing.assert_allclose(retract(0.2).T @ retract(0.2), np.eye(3), atol=1e-14)
        np.testing.assert_allclose((retract(1e-5) - retract(-1e-5)) / 2e-5, direction, atol=1e-9)
        expected = -0.5 * frame @ direction.T @ direction
        observed = (retract(0.001) - frame - 0.001 * direction) / 0.001**2
        np.testing.assert_allclose(observed, expected, atol=5e-4)


class AttentionGeometryChecks(unittest.TestCase):
    def test_gram_spectra_and_free_scales(self):
        q = np.linalg.qr(np.random.default_rng(20).normal(size=(6, 3)))[0]
        scales = np.array([2, 0.5, 3.0])
        w = q * scales
        np.testing.assert_allclose(w.T @ w, np.diag(scales**2), atol=1e-14)
        np.testing.assert_allclose(np.linalg.svd(w, compute_uv=False), sorted(scales, reverse=True))
        self.assertAlmostEqual(np.linalg.norm(w, 2), 3)

    def test_packed_contraction_does_not_make_heads_isometric(self):
        packed = np.vstack([np.eye(2), np.eye(2), np.eye(2)]) / math.sqrt(3)
        np.testing.assert_allclose(packed.T @ packed, np.eye(2))
        for part in np.split(packed, 3):
            self.assertLess(np.linalg.norm(part, 2), 1)
            self.assertGreater(np.linalg.norm(part.T @ part - np.eye(2)), 0.5)

    def test_dgram_restoration_zero_step_failure(self):
        w = np.diag([1.0, 2])
        u, s, vh = np.linalg.svd(w, full_matrices=False)
        result = (u @ vh) * s
        np.testing.assert_allclose(result, np.diag([2, 1]))
        np.testing.assert_allclose(result.T @ result, np.diag([4, 1]))
        self.assertGreater(np.linalg.norm(result - w), 1)
        self.assertAlmostEqual(np.linalg.norm(result, 2), np.linalg.norm(w, 2))

    def test_exact_restoration_norm_budget(self):
        rng = np.random.default_rng(200)
        w = np.diag([1.0, 2])
        original = np.linalg.norm(w, 2)
        exposure = 0.0
        for _ in range(30):
            d = rng.normal(size=w.shape)
            d /= np.linalg.norm(d, 2)
            exposure += 0.02
            u, s, vh = np.linalg.svd(w - 0.02 * d)
            w = (u @ vh) * s
            self.assertLessEqual(np.linalg.norm(w, 2), original + exposure + 1e-13)
        self.assertEqual(50000 * 0.02, 1000)

    def test_logits_scale_and_reciprocal_invariance(self):
        rng = np.random.default_rng(201)
        h, q, k = rng.normal(size=(4, 3)), rng.normal(size=(3, 2)), rng.normal(size=(3, 2))
        logits = lambda q, k: h @ q @ k.T @ h.T / math.sqrt(2)
        original = logits(q, k)
        np.testing.assert_allclose(logits(3 * q, 3 * k), 9 * original)
        np.testing.assert_allclose(logits(3 * q, k / 3), original)
        self.assertLessEqual(np.linalg.norm(original, 2), np.linalg.norm(h, 2)**2 * np.linalg.norm(q, 2) * np.linalg.norm(k, 2) / math.sqrt(2))

    def test_common_offsets_and_gap_control(self):
        uniform_norm = math.sqrt(3) / 4
        previous = math.inf
        for c in np.linspace(1, 4, 40):
            p = softmax(np.array([c**2, 0, 0, 0]))
            jac = softmax_jacobian(p)
            self.assertLessEqual(1 - p[0], 3 * math.exp(-c**2) + 1e-14)
            self.assertLessEqual(np.linalg.norm(jac), 6 * math.exp(-c**2) + 1e-14)
            self.assertLess(np.linalg.norm(jac), previous)
            previous = np.linalg.norm(jac)
            self.assertAlmostEqual(np.linalg.norm(softmax_jacobian(softmax(np.full(4, c**2)))), uniform_norm)
        np.testing.assert_allclose(softmax([0.1, 0.2, 0.3]), softmax(np.array([0.1, 0.2, 0.3]) + 1000), atol=1e-13)

    def test_softmax_jacobian_and_null_direction(self):
        z = np.array([-1, 0.2, 0.7])
        p = softmax(z)
        jac = softmax_jacobian(p)
        for index in range(3):
            e = np.eye(3)[index] * 1e-6
            observed = (softmax(z + e) - softmax(z - e)) / 2e-6
            np.testing.assert_allclose(observed, jac[:, index], atol=1e-10)
        np.testing.assert_allclose(jac @ np.ones(3), 0, atol=1e-14)
        self.assertAlmostEqual(float(softmax_jacobian(np.ones(1))[0, 0]), 0)

    def test_bounded_logits_lower_bound(self):
        rng = np.random.default_rng(202)
        for support in [2, 4, 10]:
            for maximum in [0.1, 1, 3]:
                a = math.exp(-2 * maximum) / support
                for _ in range(20):
                    p = softmax(rng.uniform(-maximum, maximum, support))
                    self.assertGreaterEqual(p.min(), a)
                    self.assertLessEqual(p.max(), 1 - a)
                    self.assertGreaterEqual(np.linalg.norm(softmax_jacobian(p)), math.sqrt(support) * a * (1 - a))

    def test_gelu_derivative_and_positive_tail(self):
        phi = lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi)
        cdf = lambda t: (1 + math.erf(t / math.sqrt(2))) / 2
        gelu = lambda t: t * cdf(t)
        for t in [-3, -1, 0, 1, 3]:
            self.assertAlmostEqual((gelu(t + 1e-5) - gelu(t - 1e-5)) / 2e-5, cdf(t) + t * phi(t), places=9)
        self.assertAlmostEqual(cdf(10) + 10 * phi(10), 1)


class ExperimentEvidenceChecks(unittest.TestCase):
    def test_exact_cross_entropy_identity(self):
        rng = np.random.default_rng(21)
        for _ in range(40):
            z, dz = rng.normal(size=7), rng.normal(size=7)
            q = softmax(rng.normal(size=7))
            actual = cross_entropy(q, z + dz) - cross_entropy(q, z)
            rhs = predictive_kl(z, z + dz) - (q - softmax(z)) @ dz
            self.assertAlmostEqual(actual, rhs, places=13)

    def test_predictive_fisher_quadratic_limit(self):
        z, direction = np.array([0.2, -0.7, 0.4]), np.array([-0.3, 0.1, 0.8])
        expected = direction @ softmax_jacobian(softmax(z)) @ direction / 2
        errors = [abs(predictive_kl(z, z + t * direction) / t**2 - expected) for t in [0.04, 0.02, 0.01]]
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

    def test_global_scale_cancels_in_quadratic_matching(self):
        d = np.array([1.0, -0.5, 0.2])
        f = softmax_jacobian(softmax(np.array([0.1, -0.3, 0.7])))
        match = lambda x: math.sqrt(0.002 / (x @ f @ x)) * x
        for a in [0.1, 3, 100]:
            np.testing.assert_allclose(match(a * d), match(d), atol=1e-14)
        self.assertGreater(np.linalg.norm(match(d * np.array([1, 3, 1])) - match(d)), 0.01)

    def test_nested_local_oracle_and_optimizer_distinction(self):
        r = np.array([1, 2.0])
        hard_best = abs(r[0])
        sphere_best = np.linalg.norm(r)
        self.assertLess(hard_best, sphere_best)
        hard_choice, poor_sphere_choice = np.array([1.0, 0]), np.array([-1.0, 0])
        self.assertGreater(r @ hard_choice, r @ poor_sphere_choice)

    def test_archived_paired_aggregates(self):
        record = experiment_record()
        for row in record['matched'] + record['angular_identical']:
            deltas = [seed['hard_test_ce'] - seed['sphere_test_ce'] for seed in row['seeds']]
            np.testing.assert_allclose(deltas, [seed['delta'] for seed in row['seeds']], atol=1e-14)
            self.assertAlmostEqual(float(np.mean(deltas)), row['mean'], places=13)
        fixed = {row['setting']: row for row in record['matched'] if row['endpoint'] == 'fixed_steps'}
        self.assertAlmostEqual(fixed['h1']['mean'], -0.5181255534003464)
        self.assertEqual(f"{fixed['h4']['mean']:.6f}", '0.040624')
        self.assertEqual(sum(x['delta'] > 0 for x in fixed['wide']['seeds']), 3)
        self.assertGreater(max(x['delta'] for x in fixed['wide']['seeds']), 0.8)

    def test_archived_initialization_comparison(self):
        record = experiment_record()
        for row in record['angular_archived']:
            self.assertAlmostEqual(float(np.mean([s['hard_test_ce'] - s['sphere_test_ce'] for s in row['seeds']])), row['mean'], places=13)
        means = {row['setting']: row['mean'] for row in record['angular_archived']}
        self.assertAlmostEqual(means['h1'], 0.035325, places=6)
        self.assertAlmostEqual(means['h4'], -0.092984, places=6)

    def test_forecast_counts_and_checkpoint_clustering(self):
        for row, independent, local, checkpoint in zip(experiment_record()['shuffled'], [20, 12, 18], [24, 23, 22], [2, 1, 3]):
            self.assertEqual(row['count'], 24)
            self.assertEqual(round(row['independent_accuracy'] * row['count']), independent)
            self.assertEqual(round(row['local_accuracy'] * row['count']), local)
            self.assertEqual(round(row['checkpoint_accuracy'] * len(row['actual_by_seed'])), checkpoint)
            self.assertEqual(len(row['actual_by_seed']), 3)
            correct = sum(np.sign(row['actual_by_seed'][seed]) == np.sign(row['forecast_by_seed'][seed]) for seed in row['actual_by_seed'])
            self.assertEqual(correct, checkpoint)

    def test_routing_aggregate_and_controller_limit(self):
        record = experiment_record()
        route = record['routing']
        for condition, mean in route['means'].items():
            self.assertAlmostEqual(float(np.mean([r['ce'] for r in route['records'] if r['condition'] == condition])), mean, places=13)
        self.assertGreater(route['means']['uniform_block0'] - route['means']['learned'], 1.4)
        self.assertLess(record['max_calibration_error'], 0.005)
        self.assertGreater(record['expanded_validation_kl_ratio'], 2)


if __name__ == '__main__':
    unittest.main()
