"""Draw the exact worked examples for the network geometry follow-ups."""
import math
import numpy as np

from decay_momentum_figures import style, save, PAPER, INK, MUTED, LINE, RUST, BLUE
import matplotlib.pyplot as plt
from check_network_scaling import residual_rows


def clean(ax):
    ax.grid(axis='y', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)


def residual_remainder():
    depth, actual, bound = np.array(residual_rows()).T
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    fig.suptitle('More blocks, a bounded remainder.', x=0.07, y=0.96, ha='left', fontsize=17)
    ax.plot(depth, bound, color=BLUE, linewidth=2, linestyle=(0, (4, 3)), label='Finite-depth upper bound')
    ax.plot(depth, actual, color=RUST, linewidth=2, marker='o', markersize=5, label='Exact scalar remainder')
    ax.set_xscale('log', base=2)
    ax.set_xticks([1, 2, 4, 8, 16, 32, 64, 128], ['1', '2', '4', '8', '16', '32', '64', '128'])
    ax.set_ylim(-0.001, 0.023)
    ax.set_xlabel('Residual depth L', labelpad=10)
    ax.set_ylabel('Output minus its first-order prediction', labelpad=10)
    clean(ax)
    ax.legend(loc='upper left', frameon=False)
    fig.text(0.07, 0.035, 'Scalar averaged residual stack. Initial weight 0.5, weight change 0.2 in every block. No training data.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.2, top=0.84)
    save(fig, 'residual-remainder.svg')


def width_transfer():
    width = np.array([16, 32, 64, 128, 256, 512, 1024])
    master = 0.01
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.1))
    fig.suptitle('A copied number can hide a different step.', x=0.06, y=0.96, ha='left', fontsize=17)
    left, right = axes
    left.plot(width, master * width, color=RUST, marker='o', label='Sign, raw rate 0.01')
    left.plot(width, np.full(len(width), master), color=BLUE, marker='o', label='Gradient / polar / scaled sign')
    left.set_yscale('log')
    left.set_ylabel('One-step output RMS change', labelpad=9)
    left.set_ylim(0.007, 20)
    left.set_title('Account for the proposal norm', loc='left', fontsize=11, pad=13)
    right.plot(width, master / (1 + width * 0.01), color=RUST, marker='o', label='Fixed epsilon: 0.01')
    right.plot(width, np.full(len(width), master / 1.16), color=BLUE, marker='o', label='Scaled epsilon: 0.16 / width')
    right.set_ylabel('RMS change after sign-rate scaling', labelpad=9)
    right.set_ylim(0, 0.0101)
    right.set_title('The denominator still matters', loc='left', fontsize=11, pad=13)
    for ax in axes:
        ax.set_xscale('log', base=2)
        ax.set_xticks([16, 64, 256, 1024], ['16', '64', '256', '1024'])
        ax.set_xlabel('Square layer width', labelpad=10)
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1.03), frameon=False, fontsize=8)
        clean(ax)
    fig.text(0.06, 0.035, 'Exact mean-readout example. Frozen all-ones input, master rate 0.01. Stabilized sign is not a full Adam update.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.19, top=0.74, wspace=0.3)
    save(fig, 'width-transfer.svg')


def normalized_rotation():
    kappa = np.logspace(0, 4, 400)
    alpha = 0.01
    head = np.degrees(np.arctan(abs(math.sin(alpha)) * np.sqrt(kappa**2 - 1)))
    matrix_angle = math.degrees(math.acos((2 + 2 * math.cos(alpha)) / 4))
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    fig.suptitle('A small packed rotation can turn one head.', x=0.07, y=0.96, ha='left', fontsize=17)
    ax.plot(kappa, head, color=RUST, linewidth=2, label='Normalized head angle')
    ax.axhline(matrix_angle, color=BLUE, linewidth=1.5, linestyle=(0, (4, 3)), label='Whole-matrix Frobenius angle')
    for value in [100, 1000]:
        theta = math.degrees(math.atan(abs(math.sin(alpha)) * math.sqrt(value**2 - 1)))
        ax.scatter([value], [theta], color=RUST, zorder=4, s=28)
        ax.annotate(f'{theta:.1f} degrees', (value, theta), xytext=(9, -18), textcoords='offset points', fontsize=10, color=RUST)
    ax.set_xscale('log')
    ax.set_ylim(-3, 96)
    ax.set_xlabel('Projection sensitivity kappa (inverse margin)', labelpad=10)
    ax.set_ylabel('Angle in degrees', labelpad=10)
    ax.set_yticks([0, 30, 60, 90])
    ax.legend(loc='upper left', frameon=False)
    clean(ax)
    fig.text(0.07, 0.035, 'Exact orthogonal 4 by 4 construction. Plane rotation 0.01 radians. Feature-dependent angles, not training outcomes.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.1, right=0.97, bottom=0.2, top=0.84)
    save(fig, 'normalized-head-rotation.svg')


if __name__ == '__main__':
    style()
    residual_remainder()
    width_transfer()
    normalized_rotation()
