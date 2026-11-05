"""Render the exact geometry examples and archived paired-seed comparisons."""
import math
import numpy as np

from decay_momentum_figures import style, save, INK, MUTED, LINE, RUST, BLUE
import matplotlib.pyplot as plt
from check_geometry_evidence import lift_example, softmax, softmax_jacobian, experiment_record


def clean(ax):
    ax.grid(axis='y', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)


def tangent_completion():
    matrices = lift_example()
    norms = [np.linalg.norm(m, 2) for m in matrices]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    fig.suptitle('The free block changes the norm, not the action.', x=0.07, y=0.96, ha='left', fontsize=17)
    bars = ax.bar(range(3), norms, color=[INK, RUST, BLUE], width=0.52, zorder=3)
    ax.axhline(1, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)))
    for bar, value in zip(bars, norms):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.025, f'{value:.3f}', ha='center', color=INK, fontsize=12)
    ax.set_xticks(range(3), ['Tangent direction', 'Zero-block lift', 'Completed lift'])
    ax.set_ylim(0, 1.35)
    ax.set_ylabel('Spectral norm after dividing by square root two', labelpad=11)
    clean(ax)
    fig.text(0.07, 0.035, 'Exact 4 by 4 construction. Both skew lifts produce the same tangent direction. Dashed line: unit budget.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.18, top=0.83)
    save(fig, 'tangent-completion.svg')


def attention_gap():
    scale = np.linspace(1, 4, 200)
    gap = [np.linalg.norm(softmax_jacobian(softmax(np.array([c*c, 0, 0, 0])))) for c in scale]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    fig.suptitle('A growing gap matters. A common offset cancels.', x=0.07, y=0.96, ha='left', fontsize=17)
    ax.plot(scale, np.full_like(scale, math.sqrt(3) / 4), color=BLUE, linewidth=2, linestyle=(0, (4, 3)), label='Equal logits: common-offset control')
    ax.plot(scale, gap, color=RUST, linewidth=2, label='Unique winner: gap equals c squared')
    ax.set_yscale('log')
    ax.set_ylim(1e-7, 2)
    ax.set_xlabel('Query and key scale c', labelpad=10)
    ax.set_ylabel('Softmax Jacobian Frobenius norm', labelpad=10)
    ax.legend(loc='lower left', frameon=False)
    clean(ax)
    fig.text(0.07, 0.035, 'Four-token examples. Fixed features, unnormalized Q/K projections. No training.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.2, top=0.83)
    save(fig, 'attention-gap-control.svg')


def matched_seeds():
    record = experiment_record()
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    fig.suptitle('The clock changes the comparison.', x=0.07, y=0.96, ha='left', fontsize=17)
    labels = ['One head, width 32', 'Four heads, width 32', 'Expanded one head, width 48']
    for rows, shift, color, label in [
        (record['angular_identical'], 0.14, BLUE, 'Angular clock, identical initial arrays'),
        ([r for r in record['matched'] if r['endpoint'] == 'fixed_steps'], -0.14, RUST, 'Prescribed predictive-KL clock'),
    ]:
        for index, setting in enumerate(['h1', 'h4', 'wide']):
            selected = [r for r in rows if r['setting'] == setting]
            if not selected:
                continue
            row = selected[0]
            values = [r['delta'] for r in row['seeds']]
            y = 2 - index + shift
            ax.scatter(values, np.full(3, y), color=color, s=38, zorder=4, label=label if index == 0 else None)
            ax.plot([row['mean'], row['mean']], [y - 0.08, y + 0.08], color=color, linewidth=2.5, zorder=5)
    ax.axvline(0, color=INK, linewidth=1)
    ax.set_yticks([2, 1, 0], labels)
    ax.set_ylim(-0.5, 2.5)
    ax.set_xlim(-1, 1)
    ax.set_xlabel('Test loss difference: hard constraint minus norm-only (nats per masked byte)', labelpad=10)
    ax.grid(axis='x', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.47, 1.15), ncol=1, frameon=False, fontsize=9)
    fig.text(0.07, 0.035, 'Archived 4000-update runs. Each dot is a paired seed, short bars show means. Different clocks are separate interventions.', fontsize=9, color=MUTED)
    fig.subplots_adjust(left=0.29, right=0.98, bottom=0.19, top=0.72)
    save(fig, 'matched-step-seeds.svg')


if __name__ == '__main__':
    style()
    tangent_completion()
    attention_gap()
    matched_seeds()
