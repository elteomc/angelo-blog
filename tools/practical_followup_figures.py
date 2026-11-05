"""Draw the polar, averaging, and decay examples for the three review drafts."""
import numpy as np
import matplotlib.pyplot as plt

from decay_momentum_figures import style, save, PAPER, INK, MUTED, LINE, RUST, BLUE
from check_practical_followups import scalar_trace, expected_unit_step


def clean(ax):
    ax.tick_params(length=0, pad=6, labelsize=10)
    for side in ['bottom', 'left']:
        ax.spines[side].set_color(LINE)
    ax.grid(axis='y', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)


def polar_iterations():
    traces = scalar_trace([1, 0.1, 0.001, 0])
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    fig.suptitle('A finite iteration treats singular modes differently.', x=0.07, y=0.97, ha='left', fontsize=17)
    for index, color, label, linestyle in [
        (0, BLUE, 'Initial singular value 1', '-'),
        (1, RUST, 'Initial singular value 0.1', '-'),
        (2, INK, 'Initial singular value 0.001', '-'),
        (3, MUTED, 'Exact zero', (0, (3, 3))),
    ]:
        ax.plot(np.arange(len(traces)), traces[:, index], color=color, linewidth=2, label=label, linestyle=linestyle)
    clean(ax)
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.025, 1.06)
    ax.set_xticks([0, 5, 10, 15, 20, 24])
    ax.set_xlabel('Cubic iterations', labelpad=9)
    ax.set_ylabel('Signed amplitude in the original singular basis', labelpad=12)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.51, 0.88), frameon=False, ncol=2, fontsize=9)
    fig.text(0.07, 0.035, 'Diagonal input (1, 0.1, 0.001, 0), divided by its Frobenius norm. Float64 scalar recurrence.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.19, top=0.72)
    save(fig, 'polar-iterations.svg')


def averaging_order():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.0))
    fig.suptitle('Magnitude information survives averaging first.', x=0.06, y=0.97, ha='left', fontsize=17)
    left, right = axes
    left.bar([-1, 4], [0.75, 0.25], color=[BLUE, RUST], width=0.85)
    left.axvline(0.25, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)))
    left.text(0.38, 0.87, 'Mean: +0.25', fontsize=10, color=MUTED)
    for x, y in [(-1, 0.75), (4, 0.25)]:
        left.text(x, y + 0.025, f'{y:g}', ha='center', fontsize=11)
    left.set_xlim(-2.1, 5.1)
    left.set_ylim(0, 1)
    left.set_xticks([-1, 4])
    left.set_xlabel('Sampled gradient', labelpad=9)
    left.set_ylabel('Probability', labelpad=9)
    left.set_title('Rare magnitude, common sign', loc='left', fontsize=11, pad=13)
    batch = np.arange(1, 257)
    expected = [expected_unit_step(int(b)) for b in batch]
    right.plot(batch, expected, color=RUST, linewidth=1.6)
    right.scatter([1, 2, 4, 16, 64, 256], [expected_unit_step(b) for b in [1, 2, 4, 16, 64, 256]], color=RUST, s=26, zorder=4)
    right.axhline(0, color=INK, linewidth=0.8)
    right.axhline(-1, color=BLUE, linewidth=1.2, linestyle=(0, (4, 3)))
    right.set_xscale('log', base=2)
    right.set_xticks([1, 4, 16, 64, 256], ['1', '4', '16', '64', '256'])
    right.set_xlim(0.85, 310)
    right.set_ylim(-1.08, 0.65)
    right.set_xlabel('Independent gradients per average', labelpad=9)
    right.set_ylabel('Expected unit descent proposal', labelpad=9)
    right.set_title('Average, then take the sign', loc='left', fontsize=11, pad=13)
    for ax in axes:
        clean(ax)
    fig.text(0.06, 0.035, 'Exact binomial probabilities at one fixed evaluation point. Ties return zero. The mean-gradient descent direction is negative.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.21, top=0.79, wspace=0.38)
    save(fig, 'averaging-order.svg')


def averaging_tracking():
    alpha = np.geomspace(0.005, 1, 400)
    variance = alpha / (2 - alpha)
    lag_squared = (0.01 * (1 - alpha) / alpha)**2
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    fig.suptitle('Averaging trades noise reduction for tracking lag.', x=0.07, y=0.97, ha='left', fontsize=17)
    ax.loglog(alpha, variance, color=RUST, linewidth=2, label='Noise variance')
    ax.loglog(alpha, np.maximum(lag_squared, 1e-12), color=BLUE, linewidth=2, label='Squared trend lag')
    ax.loglog(alpha, variance + lag_squared, color=INK, linewidth=2.3, label='Mean squared error')
    clean(ax)
    ax.set_xlim(0.005, 1)
    ax.set_ylim(1e-4, 5)
    ax.set_xticks([0.005, 0.01, 0.03, 0.1, 0.3, 1], ['0.005', '0.01', '0.03', '0.1', '0.3', '1'])
    ax.set_xlabel(r'Fresh-gradient weight $\alpha$', labelpad=9)
    ax.set_ylabel('Squared-gradient units', labelpad=10)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.88), frameon=False, ncol=3, fontsize=9)
    fig.text(0.07, 0.035, 'Independent scalar noise variance 1. Mean increases by 0.01 each step. Steady tracking calculations, not training runs.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.2, top=0.76)
    save(fig, 'averaging-tracking.svg')


def decay_norm_budget():
    t = np.arange(81)
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    fig.suptitle('Decay bounds accumulation of a unit proposal.', x=0.07, y=0.97, ha='left', fontsize=17)
    ax.plot(t, 2 * (1 - 0.95**t), color=RUST, linewidth=2.3, label='Decay, start at 0')
    ax.plot(t, 2 + 3 * 0.95**t, color=BLUE, linewidth=2.3, label='Decay, start at 5')
    ax.plot(t, 0.1 * t, color=INK, linewidth=1.8, linestyle=(0, (3, 3)), label='No decay, start at 0')
    ax.axhline(2, color=MUTED, linewidth=1, linestyle=(0, (5, 3)))
    ax.text(80, 2.17, r'$R=2$', color=MUTED, ha='right', fontsize=11)
    clean(ax)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 8.3)
    ax.set_xlabel('Update count', labelpad=9)
    ax.set_ylabel('Weight norm in the positive scalar example', labelpad=10)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.88), frameon=False, ncol=3, fontsize=9)
    fig.text(0.07, 0.035, r'Constant proposal 1, learning rate 0.1, decay coefficient 0.5. The initially infeasible curve stays above $R$.', color=MUTED, fontsize=9)
    fig.subplots_adjust(left=0.1, right=0.97, bottom=0.2, top=0.76)
    save(fig, 'decay-norm-budget.svg')


if __name__ == '__main__':
    style()
    polar_iterations()
    averaging_order()
    averaging_tracking()
    decay_norm_budget()
    print('Built four figures for the three practical follow-up drafts')
