"""Verify the worked examples using numerical differentiation and direct maps."""
import math


def close(actual, expected, tolerance=1e-7):
    assert math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (actual, expected)


def loss(w):
    radius = math.hypot(*w)
    return 0.5 * (w[1] / radius - 1)**2


def gradient(w):
    epsilon = 1e-6
    result = []
    for index in range(2):
        plus = list(w)
        minus = list(w)
        plus[index] += epsilon
        minus[index] -= epsilon
        result.append((loss(plus) - loss(minus)) / (2 * epsilon))
    return result


def rms(h, epsilon=0):
    denominator = math.sqrt(sum(value**2 for value in h) / len(h) + epsilon)
    return [value / denominator for value in h]


def layer_norm(h):
    mean = sum(h) / len(h)
    centered = [value - mean for value in h]
    return rms(centered)


def same_vector(left, right):
    for a, b in zip(left, right):
        close(a, b)


def check():
    eta = 0.5
    for radius, slope, prediction in [(1, 0.5, 1 / math.sqrt(5)), (2, 0.125, 1 / math.sqrt(65))]:
        w = [radius, 0]
        grad = gradient(w)
        updated = [value - eta * derivative for value, derivative in zip(w, grad)]
        close(loss(w), 0.5)
        close(updated[1] / updated[0], slope)
        angle = math.degrees(math.atan2(updated[1], updated[0]))
        close(round(angle, 2), 26.57 if radius == 1 else 7.13)
        close(updated[1] / math.hypot(*updated), prediction)
        close(math.hypot(*updated)**2, radius**2 + eta**2 / radius**2)
        corrected = [value - (eta * radius**2) * derivative for value, derivative in zip(w, grad)]
        close(corrected[1] / corrected[0], 0.5)
    w = [0.6, -0.8]
    grad = gradient(w)
    scaled = gradient([3 * value for value in w])
    close(sum(a * b for a, b in zip(w, grad)), 0)
    same_vector(scaled, [value / 3 for value in grad])
    h = [1, 2]
    same_vector(rms(h), rms([2 * value for value in h]))
    assert abs(rms(h, 1)[0] - rms([2 * value for value in h], 1)[0]) > 0.01
    same_vector(rms([2 * value for value in h], 1), rms(h, 0.25))
    same_vector(layer_norm(h), [-1, 1])
    same_vector(layer_norm([3, 2]), [1, -1])
    same_vector(layer_norm([3 * value + 7 for value in h]), layer_norm(h))
    assert rms([1, 1]) != rms([1, 2])
    for gain in [0.25, 1, 4]:
        weights = [1 / gain, 2 / gain]
        same_vector([gain * value for value in weights], [1, 2])
        close(abs(weights[1]) / abs(weights[0]), 2)
    print('Verified SGD steps, inverse-square scaling, angles, radius growth, epsilon, normalization symmetries, and shared-gain ratios')


if __name__ == '__main__':
    check()
