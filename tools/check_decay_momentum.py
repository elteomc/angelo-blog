"""Verify the finite-step examples and trajectory identities in parts 3 and 4."""
import math
import unittest


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def norm(vector):
    return math.sqrt(dot(vector, vector))


def prediction(w, x=(0.0, 1.0)):
    return dot(w, x) / norm(w)


def loss(w, x=(0.0, 1.0), target=1.0):
    return 0.5 * (prediction(w, x) - target)**2


def gradient(w, x=(0.0, 1.0), target=1.0):
    radius = norm(w)
    score = prediction(w, x)
    return tuple((score - target) * (feature / radius - score * weight / radius**2) for weight, feature in zip(w, x))


def step(w, update, eta, shrink=1.0):
    return tuple(shrink * weight - eta * direction for weight, direction in zip(w, update))


def direction(w):
    return tuple(value / norm(w) for value in w)


def angle(w, updated):
    cross = abs(w[0] * updated[1] - w[1] * updated[0])
    return math.atan2(cross, dot(w, updated))


def split(w, proposal):
    e = direction(w)
    radial = dot(e, proposal)
    tangent = tuple(value - radial * basis for value, basis in zip(proposal, e))
    return radial, tangent


def batch(t):
    return (math.cos(0.23 * t), math.sin(0.23 * t)), 0.3 * math.sin(0.41 * t)


def hyperparameters(t):
    eta = 0.03 + 0.01 * math.sin(t)**2
    decay = 0.4 + 0.2 * math.cos(t)**2
    return eta, decay, 1 - eta * decay


def decay_example(count=24):
    w = (1.0, 0.0)
    z = w
    cumulative = 1.0
    records = []
    for t in range(count + 1):
        records.append((t, norm(w), norm(z), prediction(w), prediction(z)))
        if t < count:
            next_cumulative = 0.9 * cumulative
            w = step(w, gradient(w), 0.1, 0.9)
            z = step(z, gradient(z), 0.1 / (cumulative * next_cumulative))
            cumulative = next_cumulative
    return records


class DecayMomentumChecks(unittest.TestCase):
    def vectors_close(self, left, right, tolerance=1e-10):
        for actual, expected in zip(left, right):
            self.assertAlmostEqual(actual, expected, delta=tolerance)

    def test_gradient_against_numerical_differentiation(self):
        w = (0.7, -1.2)
        x, target = batch(7)
        numerical = []
        for index in range(2):
            plus, minus = list(w), list(w)
            plus[index] += 1e-6
            minus[index] -= 1e-6
            numerical.append((loss(plus, x, target) - loss(minus, x, target)) / 2e-6)
        self.vectors_close(gradient(w, x, target), numerical, 1e-8)

    def test_variable_schedule_equivalence_with_the_same_batches(self):
        w = (1.2, -0.4)
        z = w
        cumulative = 1.0
        for t in range(60):
            eta, decay, shrink = hyperparameters(t)
            x, target = batch(t)
            next_cumulative = shrink * cumulative
            w = step(w, gradient(w, x, target), eta, shrink)
            z = step(z, gradient(z, x, target), eta / (cumulative * next_cumulative))
            self.vectors_close(w, tuple(next_cumulative * value for value in z))
            self.vectors_close(direction(w), direction(z))
            cumulative = next_cumulative

    def test_radius_recurrence_and_frozen_statistic_example(self):
        w = (0.7, -1.2)
        eta, shrink = 0.1, 0.9
        e = direction(w)
        h = gradient(e)
        updated = step(w, gradient(w), eta, shrink)
        expected = shrink**2 * norm(w)**2 + eta**2 * norm(h)**2 / norm(w)**2
        self.assertAlmostEqual(norm(updated)**2, expected)
        self.assertAlmostEqual(math.tan(angle(w, updated)), eta * norm(h) / (shrink * norm(w)**2))
        fixed = (0.01 / 0.19)**0.25
        self.assertAlmostEqual(fixed**2, 0.9**2 * fixed**2 + 0.1**2 / fixed**2)
        fixed_angle = math.atan2(0.1 / fixed, 0.9 * fixed)
        self.assertAlmostEqual(math.cos(fixed_angle), 0.9)
        self.assertEqual(round(fixed, 4), 0.4790)
        self.assertEqual(round(math.degrees(fixed_angle), 2), 25.84)

    def test_printed_decay_example_and_schedule(self):
        records = decay_example()
        self.assertLess(max(abs(row[3] - row[4]) for row in records), 1e-12)
        self.assertEqual([round(0.1 / 0.9**(2 * t + 1), 6) for t in range(3)], [0.111111, 0.137174, 0.169351])
        self.assertEqual(round(math.degrees(math.atan(1 / 9)), 2), 6.34)
        self.assertAlmostEqual(1 / 0.9**2, 1.2345679012345678)

    def test_second_momentum_step_and_actual_rotation(self):
        w0 = (1.0, 0.0)
        m0 = gradient(w0)
        w1 = step(w0, m0, 0.5)
        g1 = gradient(w1)
        m1 = tuple(0.9 * old + current for old, current in zip(m0, g1))
        w2 = step(w1, m1, 0.5)
        radial, tangent = split(w1, m1)
        self.assertAlmostEqual(dot(w1, g1), 0)
        self.assertAlmostEqual(radial, -0.9 * 0.5 * norm(m0)**2 / norm(w1))
        self.vectors_close(w2, (0.9011145618000168, 1.1477708763999663))
        geometric = math.atan2(0.5 * norm(tangent), norm(w1) - 0.5 * radial)
        self.assertAlmostEqual(angle(w1, w2), geometric)
        self.assertEqual(round(math.degrees(geometric), 2), 25.30)
        naive = math.atan(0.5 * norm(m1) / norm(w1))
        self.assertEqual(round(math.degrees(naive), 2), 30.37)

    def test_normalized_updates_and_angle_quadrants(self):
        w = (1.0, 0.0)
        for proposal, expected in [((0.0, -1.0), 26.57), ((-0.8, -0.6), 12.09)]:
            self.assertAlmostEqual(norm(proposal), 1)
            updated = step(w, proposal, 0.5)
            radial, tangent = split(w, proposal)
            geometric = math.atan2(0.5 * norm(tangent), 1 - 0.5 * radial)
            self.assertAlmostEqual(angle(w, updated), geometric)
            self.assertEqual(round(math.degrees(geometric), 2), expected)
        self.assertEqual(step(w, (1, 0), 1), (0, 0))
        self.assertAlmostEqual(angle(w, step(w, (1, 0), 2)), math.pi)
        self.assertAlmostEqual(angle(w, step(w, (1, -1), 1)), math.pi / 2)
        self.assertEqual(round(math.degrees(angle(w, (0.8, 0.2))), 2), 14.04)

    def test_constant_rescaling_transports_nonzero_momentum(self):
        w = (0.6, 0.8)
        memory = (0.3, -0.2)
        factor = 2.5
        scaled_w = tuple(factor * value for value in w)
        scaled_memory = tuple(value / factor for value in memory)
        for t in range(20):
            eta, decay, shrink = hyperparameters(t)
            x, target = batch(t)
            memory = tuple(0.9 * old + current for old, current in zip(memory, gradient(w, x, target)))
            scaled_memory = tuple(0.9 * old + current for old, current in zip(scaled_memory, gradient(scaled_w, x, target)))
            w = step(w, memory, eta, shrink)
            scaled_eta, scaled_decay = factor**2 * eta, decay / factor**2
            scaled_w = step(scaled_w, scaled_memory, scaled_eta, 1 - scaled_eta * scaled_decay)
            self.vectors_close(scaled_w, tuple(factor * value for value in w))
            self.vectors_close(scaled_memory, tuple(value / factor for value in memory))

    def test_momentum_clock_changes_memory_and_not_only_rate(self):
        w = (1.2, -0.4)
        z = w
        wrong_z = w
        memory = q = wrong_q = (0.0, 0.0)
        cumulative = previous_shrink = 1.0
        for t in range(40):
            eta, decay, shrink = hyperparameters(t)
            x, target = batch(t)
            next_cumulative = shrink * cumulative
            memory = tuple(0.9 * old + current for old, current in zip(memory, gradient(w, x, target)))
            q = tuple(0.9 * previous_shrink * old + current for old, current in zip(q, gradient(z, x, target)))
            wrong_q = tuple(0.9 * old + current for old, current in zip(wrong_q, gradient(wrong_z, x, target)))
            w = step(w, memory, eta, shrink)
            transformed_eta = eta / (cumulative * next_cumulative)
            z = step(z, q, transformed_eta)
            wrong_z = step(wrong_z, wrong_q, transformed_eta)
            self.vectors_close(w, tuple(next_cumulative * value for value in z))
            cumulative = next_cumulative
            previous_shrink = shrink
        self.assertGreater(norm(tuple(a - b for a, b in zip(direction(w), direction(wrong_z)))), 1e-4)

    def test_coupled_and_decoupled_decay_match_only_the_first_step(self):
        coupled = decoupled = (1.0, 0.0)
        coupled_memory = memory = (0.0, 0.0)
        for t in range(2):
            g = gradient(decoupled)
            cg = gradient(coupled)
            memory = tuple(0.9 * old + current for old, current in zip(memory, g))
            coupled_memory = tuple(0.9 * old + current + weight for old, current, weight in zip(coupled_memory, cg, coupled))
            decoupled = step(decoupled, memory, 0.1, 0.9)
            coupled = step(coupled, coupled_memory, 0.1)
            if t == 0:
                self.vectors_close(coupled, decoupled)
        self.assertGreater(angle(coupled, decoupled), 1e-5)


if __name__ == '__main__':
    unittest.main()
