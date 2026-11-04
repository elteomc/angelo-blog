"""Render the worked-example figures for the weight decay and momentum posts."""
from pathlib import Path
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from check_decay_momentum import decay_example, gradient, norm, split, step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/scale-geometry'
PAPER = '#fffdf8'
INK = '#262c29'
MUTED = '#656a62'
LINE = '#d8d8cd'
RUST = '#ad492d'
BLUE = '#526f82'


def style():
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 10,
        'text.color': INK,
        'axes.labelcolor': MUTED,
        'xtick.color': MUTED,
        'ytick.color': MUTED,
        'axes.edgecolor': LINE,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'figure.facecolor': PAPER,
        'axes.facecolor': PAPER,
        'svg.fonttype': 'none',
        'svg.hashsalt': 'scale-geometry-decay-momentum',
    })


def save(fig, name):
    fig.savefig(OUT / name, facecolor=PAPER, metadata={'Date': None})
    plt.close(fig)


def decay_clock():
    records = decay_example()
    times, radii, transformed_radii, predictions, transformed_predictions = zip(*records)
    assert max(abs(a - b) for a, b in zip(predictions, transformed_predictions)) < 1e-12
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.5))
    fig.suptitle('Different radii. Matching predictions.', x=0.06, ha='left', fontsize=18, y=0.96)
    for ax, first, second, label in [
        (axes[0], radii, transformed_radii, 'Weight radius'),
        (axes[1], predictions, transformed_predictions, 'Prediction on the training input'),
    ]:
        ax.plot(times, first, color=RUST, linewidth=2.5, label='Decay, fixed learning rate')
        ax.plot(times, second, color=BLUE, linewidth=1.8, linestyle=(0, (4, 3)), marker='o', markevery=4, markersize=4, markerfacecolor=PAPER, label='No decay, matched schedule')
        ax.set_xlabel('SGD step')
        ax.set_title(label, loc='left', fontsize=11, pad=12)
        ax.grid(axis='y', color=LINE, linewidth=0.6, alpha=0.7)
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 1.14)
        ax.set_xticks([0, 6, 12, 18, 24])
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.88), frameon=False, ncol=2, fontsize=10)
    fig.text(0.06, 0.035, 'Normalized linear predictor, target 1, initial weight (1, 0).  Learning rate 0.1, decay coefficient 1.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.19, top=0.70, wspace=0.25)
    save(fig, 'decay-clock.svg')


def vector_axes(ax):
    ax.set_aspect('equal')
    ax.axhline(0, color=LINE, linewidth=0.8)
    ax.axvline(0, color=LINE, linewidth=0.8)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def arrow(ax, start, end, color, width=2, linestyle='-'):
    ax.annotate('', xy=end, xytext=start, arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': width, 'linestyle': linestyle, 'shrinkA': 0, 'shrinkB': 0})


def momentum_memory():
    w0 = (1.0, 0.0)
    m0 = gradient(w0)
    w1 = step(w0, m0, 0.5)
    g1 = gradient(w1)
    m1 = tuple(0.9 * old + current for old, current in zip(m0, g1))
    w2 = step(w1, m1, 0.5)
    radial, tangent = split(w1, m1)
    after_gradient = step(w1, g1, 0.5)
    after_radial = tuple(value - 0.5 * radial * value / norm(w1) for value in w1)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 5.0))
    fig.suptitle('The gradient is tangent. Its memory is not.', x=0.06, ha='left', fontsize=18, y=0.96)
    for ax in axes:
        vector_axes(ax)
        ax.set_xlim(-0.1, 1.65)
        ax.set_ylim(-0.07, 1.50)
        ax.plot([0, w1[0]], [0, w1[1]], color=INK, linewidth=1.3)
        ax.scatter([w1[0], w2[0]], [w1[1], w2[1]], color=INK, s=16, zorder=4)
        ax.text(w1[0] + 0.03, w1[1] - 0.10, 'current weight', fontsize=9)
        ax.text(w2[0] + 0.04, w2[1] + 0.04, 'next weight', fontsize=9)
    axes[0].set_title('Where the step came from', loc='left', fontsize=11, pad=12)
    arrow(axes[0], w1, after_gradient, BLUE)
    arrow(axes[0], after_gradient, w2, RUST)
    axes[0].text(0.18, 0.65, 'current gradient\ncontribution', color=BLUE, fontsize=10)
    axes[0].text(1.03, 0.88, 'memory\ncontribution', color=RUST, fontsize=10)
    axes[1].set_title('The same step, split at the current weight', loc='left', fontsize=11, pad=12)
    arrow(axes[1], w1, after_radial, BLUE)
    arrow(axes[1], after_radial, w2, RUST)
    arrow(axes[1], w1, w2, INK, width=1, linestyle=':')
    axes[1].text(1.22, 0.49, 'radial', color=BLUE, fontsize=10)
    axes[1].text(1.18, 0.92, 'tangent', color=RUST, fontsize=10)
    fig.text(0.06, 0.055, 'Second step with momentum 0.9, learning rate 0.5, and no decay.  Exact rotation: 25.30 degrees.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.13, top=0.80, wspace=0.25)
    save(fig, 'momentum-memory.svg')


def normalized_rotation():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    fig.suptitle('Equal update lengths do not fix the angle.', x=0.06, ha='left', fontsize=18, y=0.96)
    w = (1.0, 0.0)
    for ax, proposal in zip(axes, [(0.0, -1.0), (-0.8, -0.6)]):
        updated = step(w, proposal, 0.5)
        degrees = math.degrees(math.atan2(updated[1], updated[0]))
        vector_axes(ax)
        ax.set_xlim(-0.10, 1.7)
        ax.set_ylim(-0.15, 0.8)
        arrow(ax, (0, 0), w, BLUE)
        arrow(ax, w, updated, RUST, width=2.5)
        arrow(ax, (0, 0), updated, INK, width=1.2)
        ax.text(0.15, 0.56, f'{degrees:.2f} degrees', fontsize=16)
        ax.text(updated[0] + 0.04, updated[1] + 0.03, f'({updated[0]:g}, {updated[1]:g})', fontsize=10)
        ax.text(0.35, -0.12, 'initial weight (1, 0)', color=BLUE, fontsize=9)
    fig.text(0.06, 0.055, 'Both proposals have norm 1.  Both displacements have length 0.5.  Neither run uses weight decay.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.15, top=0.80, wspace=0.25)
    save(fig, 'normalized-rotation.svg')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    decay_clock()
    momentum_memory()
    normalized_rotation()
    print('Built the decay clock, momentum memory, and normalized rotation figures')
