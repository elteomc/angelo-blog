"""Draw the activation geometry and matrix support diagrams for parts 5 and 6."""
from pathlib import Path
import numpy as np

from decay_momentum_figures import style, save, vector_axes, PAPER, INK, MUTED, LINE, RUST, BLUE
from check_layer_duality import op, polar, fro
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/scale-geometry'


def layer_perturbations():
    theta = np.linspace(0, 2 * np.pi, 513)
    inputs = np.vstack([np.cos(theta), np.sin(theta)])
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.8))
    fig.suptitle('Equal parameter size. Different activation changes.', x=0.06, ha='left', fontsize=17, y=0.96)
    for ax, matrix, label, color in [
        (axes[0], np.diag([1.0, 0.0]), 'A: one active direction', RUST),
        (axes[1], np.eye(2) / np.sqrt(2), 'B: two active directions', BLUE),
    ]:
        vector_axes(ax)
        ax.set_xlim(-1.24, 1.24)
        ax.set_ylim(-1.24, 1.24)
        ax.plot(inputs[0], inputs[1], color=LINE, linestyle=(0, (4, 3)), linewidth=1.2)
        image = matrix @ inputs
        ax.plot(image[0], image[1], color=color, linewidth=2.7)
        endpoint = matrix @ np.array([1.0, 0.0])
        ax.scatter([endpoint[0]], [endpoint[1]], color=color, s=25, zorder=3)
        ax.set_title(label, loc='left', fontsize=11, pad=12)
        ax.text(0.5, -0.02, f'Largest output length: {op(matrix):.3f}', ha='center', transform=ax.transAxes, fontsize=11, color=color)
    fig.text(0.06, 0.065, 'Both Frobenius norms are 1. Both mean squared output lengths are 0.5 for isotropic unit inputs.', color=MUTED, fontsize=9)
    fig.text(0.06, 0.025, 'Dashed circle: Euclidean radius 1. Colored traces: output changes as the unit input direction varies.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.07, right=0.96, bottom=0.21, top=0.78, wspace=0.24)
    save(fig, 'layer-perturbations.svg')


def dual_norm_balls():
    g = np.diag([3.0, 1.0])
    circle = np.linspace(0, 2 * np.pi, 513)
    boundaries = [
        (np.cos(circle), np.sin(circle)),
        ([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1]),
        ([1, 0, -1, 0, 1], [0, 1, 0, -1, 0]),
    ]
    directions = [np.diag(g / fro(g)), np.diag(polar(g)), np.array([1.0, 0.0])]
    values = [np.sqrt(10), 4, 3]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 4.5))
    fig.suptitle('The same slope, three different unit balls.', x=0.05, ha='left', fontsize=17, y=0.97)
    for ax, boundary, direction, value, title in zip(axes, boundaries, directions, values, ['Frobenius budget', 'Spectral budget', 'Nuclear budget']):
        ax.set_aspect('equal')
        ax.axhline(0, color=LINE, linewidth=0.8)
        ax.axvline(0, color=LINE, linewidth=0.8)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.fill(boundary[0], boundary[1], color=BLUE, alpha=0.08)
        ax.plot(boundary[0], boundary[1], color=BLUE, linewidth=1.8)
        domain = np.linspace(-1.3, 1.3, 200)
        ax.plot(domain, value - 3 * domain, color=RUST, linewidth=1.2, linestyle=(0, (4, 3)))
        ax.annotate('', xy=(0.57, 0.19), xytext=(0, 0), arrowprops={'arrowstyle': '-|>', 'lw': 1.1, 'color': MUTED})
        ax.scatter([direction[0]], [direction[1]], s=35, color=RUST, zorder=4)
        offset = (-22, 13) if title != 'Spectral budget' else (-28, 10)
        ax.annotate(r'$D_*$', xy=direction, xytext=offset, textcoords='offset points', color=RUST, fontsize=11)
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.tick_params(labelsize=9, length=0)
        ax.set_xlabel(r'$d_1$', labelpad=2)
        ax.set_ylabel(r'$d_2$', labelpad=1)
        ax.set_title(title, fontsize=11, pad=10)
        ax.text(0.5, -0.28, f'Support value: {value:.3f}', ha='center', transform=ax.transAxes, fontsize=10, color=RUST)
    fig.text(0.05, 0.045, r'Diagonal support directions for $G=\mathrm{diag}(3,1)$. The descent update is $-\epsilon D_*$.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.25, top=0.79, wspace=0.38)
    save(fig, 'dual-norm-balls.svg')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    layer_perturbations()
    dual_norm_balls()
    print('Built the layer perturbation and dual norm support diagrams')
