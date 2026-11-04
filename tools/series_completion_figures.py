"""Draw the six worked geometry and research-control figures for parts 7 to 12."""
import numpy as np
import matplotlib.pyplot as plt

from decay_momentum_figures import style, save, PAPER, INK, MUTED, LINE, RUST, BLUE
from check_series_completion import rotation_angle, frozen_teacher_results


def clean_axes(ax):
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    for side in ['bottom', 'left']:
        ax.spines[side].set_color(LINE)
    ax.tick_params(length=0, labelsize=10, pad=6)


def modular_budgets():
    theta = np.linspace(0, 2 * np.pi, 513)
    boundaries = [
        (np.array([-1, 1, 1, -1, -1]) / 8, np.array([-1, -1, 1, 1, -1]) * 0.75),
        (0.25 * np.cos(theta), np.sqrt(0.75) * np.sin(theta)),
        ([0.5, 0, -0.5, 0, 0.5], [0, 1, 0, -1, 0]),
    ]
    points = [(0.125, 0.75), (np.sqrt(3) / 8, np.sqrt(3) / 4), (0.5, 0)]
    values = [1.5, np.sqrt(3), 3]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 4.9))
    fig.suptitle('One feature bound, three allocations.', x=0.05, y=0.97, ha='left', fontsize=17)
    for ax, boundary, point, value, title in zip(axes, boundaries, points, values, ['Weighted maximum', 'Weighted quadratic', 'Weighted sum']):
        clean_axes(ax)
        ax.axhline(0, color=LINE, linewidth=0.8)
        ax.axvline(0, color=LINE, linewidth=0.8)
        ax.fill(*boundary, color=BLUE, alpha=0.1)
        ax.plot(*boundary, color=BLUE, linewidth=2)
        x = np.linspace(-0.6, 0.6, 300)
        ax.plot(x, value - 6 * x, color=RUST, linewidth=1.3, linestyle=(0, (4, 3)))
        ax.scatter(*point, color=RUST, s=38, zorder=4)
        ax.set_xlim(-0.6, 0.6)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xticks([-0.5, 0, 0.5])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel(r'$d_1$')
        ax.set_ylabel(r'$d_2$')
        ax.set_title(title, fontsize=11, pad=15)
        ax.text(0.5, -0.28, f'Support value: {value:.3f}', ha='center', transform=ax.transAxes, color=RUST, fontsize=10)
    fig.text(0.05, 0.045, r'$c=(2,1)$, $m=(1/4,3/4)$, $G=(6,1)$. Orange dots maximize the same linear functional.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.27, top=0.78, wspace=0.4)
    save(fig, 'modular-budgets.svg')


def sphere_retraction():
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    fig.suptitle('A tangent displacement still needs a return map.', x=0.06, y=0.97, ha='left', fontsize=17)
    clean_axes(ax)
    ax.set_aspect('equal')
    theta = np.linspace(0, 2 * np.pi, 513)
    ax.plot(np.cos(theta), np.sin(theta), color=BLUE, linewidth=1.8)
    w = np.array([1.0, 0])
    trial = np.array([1.0, 0.5])
    back = trial / np.linalg.norm(trial)
    ax.plot([0, trial[0]], [0, trial[1]], color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.plot([0, 1], [0, 0], color=LINE, linewidth=1)
    ax.annotate('', xy=trial, xytext=w, arrowprops={'arrowstyle': '-|>', 'color': RUST, 'lw': 2})
    ax.plot([1, back[0]], [0, back[1]], color=BLUE, linewidth=2, linestyle=(0, (3, 2)))
    arc = np.linspace(0, np.arctan(0.5), 50)
    ax.plot(0.35 * np.cos(arc), 0.35 * np.sin(arc), color=RUST, linewidth=1.5)
    ax.text(0.4, 0.07, r'$\theta$', color=RUST, fontsize=12)
    ax.scatter([w[0], trial[0], back[0]], [w[1], trial[1], back[1]], color=[INK, RUST, BLUE], s=38, zorder=5)
    ax.annotate(r'$w=(1,0)$', w, xytext=(15, -14), textcoords='offset points', fontsize=10)
    ax.annotate('Trial: (1, 0.5)', trial, xytext=(15, 14), textcoords='offset points', fontsize=10, color=RUST)
    ax.annotate(r'Retracted: $(2,1)/\sqrt{5}$', back, xytext=(-145, 25), textcoords='offset points', fontsize=10, color=BLUE)
    ax.text(1.07, 0.22, r'$Z$', color=RUST, fontsize=12)
    ax.set_xlim(-1.2, 1.7)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    fig.text(0.06, 0.045, 'Tangent length: 0.5. Rotation: 26.57 degrees. Final chord: 0.4595.', color=MUTED, fontsize=10)
    fig.subplots_adjust(left=0.08, right=0.96, bottom=0.15, top=0.85)
    save(fig, 'sphere-retraction.svg')


def fixed_norm_angle():
    fig, ax = plt.subplots(figsize=(8.7, 5.1))
    fig.suptitle('Two fixed lengths still leave the angle free.', x=0.07, y=0.97, ha='left', fontsize=17)
    rho = np.linspace(-1, 1, 801)
    ax.plot(rho, np.degrees(rotation_angle(0.5, rho)), color=RUST, linewidth=2.4)
    for value, label, offset in [(-0.8, 'Correlation -0.8: 12.09 degrees', (16, -25)), (0, 'Tangent: 26.57 degrees', (-70, -42))]:
        angle = np.degrees(rotation_angle(0.5, value))
        ax.scatter([value], [angle], color=RUST, s=35, zorder=3)
        ax.annotate(label, (value, angle), xytext=offset, textcoords='offset points', fontsize=10, color=INK)
    clean_axes(ax)
    ax.set_xlim(-1.04, 1.04)
    ax.set_ylim(0, 35)
    ax.set_xlabel(r'Weight-proposal correlation $\rho$', labelpad=11)
    ax.set_ylabel('Actual rotation (degrees)', labelpad=12)
    ax.grid(axis='y', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.text(0.07, 0.035, r'Normalized proposal length $\eta=0.5$. Final weight radius is fixed throughout.', color=MUTED, fontsize=10)
    fig.subplots_adjust(left=0.11, right=0.96, bottom=0.21, top=0.84)
    save(fig, 'fixed-norm-angle.svg')


def learnable_scales():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('The same effective map can take different steps.', x=0.06, y=0.97, ha='left', fontsize=17)
    c = np.geomspace(0.25, 4, 200)
    axes[0].plot(c, c, color=RUST, linewidth=2, label=r'$w=c$')
    axes[0].plot(c, 1 / c, color=BLUE, linewidth=2, label=r'$g=1/c$')
    axes[0].axhline(1, color=MUTED, linestyle=(0, (4, 3)), linewidth=1.5, label=r'$wg=1$')
    axes[0].set_xscale('log', base=2)
    axes[0].set_xticks([0.25, 0.5, 1, 2, 4], ['0.25', '0.5', '1', '2', '4'])
    axes[0].set_xlabel('Rescaling factor')
    axes[0].set_ylabel('Parameter value')
    axes[0].set_ylim(0, 4.3)
    axes[0].set_title('Before the step', loc='left', fontsize=11, pad=12)
    axes[0].legend(frameon=False, fontsize=10, loc='upper center')
    bars = axes[1].bar([0, 1], [0.81, 0.585], width=0.5, color=[RUST, BLUE])
    axes[1].axhline(1, color=MUTED, linestyle=(0, (4, 3)), linewidth=1.2)
    axes[1].set_xticks([0, 1], ['Start: (1, 1)', 'Start: (2, 0.5)'])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_ylabel('Effective product after SGD')
    axes[1].set_title(r'One step on $L=(wg)^2/2$, $\eta=0.1$', loc='left', fontsize=11, pad=12)
    for bar, label in zip(bars, ['0.810', '0.585']):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.035, label, ha='center', fontsize=11)
    for ax in axes:
        clean_axes(ax)
    fig.text(0.06, 0.035, 'The product is unchanged by reciprocal rescaling. Coordinate-wise gradient descent depends on the factors.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.08, right=0.96, bottom=0.2, top=0.8, wspace=0.4)
    save(fig, 'learnable-scales.svg')


def shared_gain_cone():
    fig, ax = plt.subplots(figsize=(8.7, 5.5))
    fig.suptitle('One gain must satisfy both squared radii.', x=0.06, y=0.97, ha='left', fontsize=17)
    x = np.linspace(0, 3.1, 300)
    ax.fill_between(x, x, 4 * x, color=BLUE, alpha=0.12)
    ax.plot(x, x, color=BLUE, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.plot(x, 4 * x, color=BLUE, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(2.8, 3.1, r'Ray $(1,1)$', color=BLUE, fontsize=10, rotation=9)
    ax.text(2.48, 9.4, r'Ray $(1,4)$', color=BLUE, fontsize=10, rotation=36)
    for point, label, color, offset, filled in [
        ((2, 4), '(2, 4): feasible', RUST, (15, 8), True),
        ((2, 2), '(2, 2): excluded boundary', BLUE, (-135, -25), False),
        ((2, 10), '(2, 10): outside', MUTED, (-125, 12), True),
    ]:
        ax.scatter(*point, s=50, facecolors=color if filled else PAPER, edgecolors=color, linewidth=1.5, zorder=4)
        ax.annotate(label, point, xytext=offset, textcoords='offset points', color=color, fontsize=10)
    clean_axes(ax)
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 12)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_xlabel(r'First squared radius $r_1$', labelpad=10)
    ax.set_ylabel(r'Second squared radius $r_2$', labelpad=10)
    fig.text(0.06, 0.035, r'Positive combinations of $(1,1)$ and $(1,4)$. Both coefficients must be strictly positive.', color=MUTED, fontsize=10)
    fig.subplots_adjust(left=0.1, right=0.96, bottom=0.19, top=0.84)
    save(fig, 'shared-gain-cone.svg')


def research_controls():
    rows = frozen_teacher_results()
    ratio = np.array([row['ratio'] for row in rows])
    fig, ax = plt.subplots(figsize=(9.4, 5.3))
    fig.suptitle('A fitting floor, and two controls that remove it.', x=0.06, y=0.97, ha='left', fontsize=17)
    dense = np.linspace(0.25, 3, 300)
    ax.plot(dense, (dense - 1)**2 / 4, color=RUST, linewidth=2, label='Individual radii: exact floor')
    ax.scatter(ratio, [row['individual'] for row in rows], color=RUST, s=13, zorder=4, label='Direct frozen-feature evaluation')
    ax.plot(ratio, [row['group'] for row in rows], color=BLUE, linewidth=2.7, label='Joint group radius')
    ax.scatter(ratio[::3], [row['multipliers'] for row in rows][::3], facecolors=PAPER, edgecolors=INK, marker='s', s=27, zorder=5, label='Independent branch multipliers')
    clean_axes(ax)
    ax.set_xlim(0.2, 3.05)
    ax.set_ylim(-0.06, 1.08)
    ax.set_xlabel(r'Target norm ratio $b$', labelpad=10)
    ax.set_ylabel('Minimum branch-fitting loss', labelpad=10)
    ax.legend(frameon=False, fontsize=9, loc='upper left')
    fig.text(0.06, 0.035, '45 target ratios. Eight isotropic inputs in four dimensions. Direct evaluation, with no optimizer training.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.1, right=0.96, bottom=0.2, top=0.84)
    save(fig, 'research-controls.svg')


if __name__ == '__main__':
    style()
    modular_budgets()
    sphere_retraction()
    fixed_norm_angle()
    learnable_scales()
    shared_gain_cone()
    research_controls()
    print('Built six figures for the final six chapters')
