"""Draw the constant-trace ODE, finite valley, and rotated moment examples."""
import math
import numpy as np

from decay_momentum_figures import style, save, MUTED, LINE, RUST, BLUE
import matplotlib.pyplot as plt
from check_noise_sharpness_symmetry import gamma_solution, valley_run, rotation_defects


def clean(ax):
    ax.grid(axis='y', color=LINE, linewidth=0.6)
    ax.set_axisbelow(True)


def intrinsic_clock():
    fig, axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('One clock for this constant-trace radius model.', x=0.06, y=0.96, ha='left', fontsize=17)
    time = np.linspace(0, 1500, 300)
    for delta, color, pattern in [(0.001,RUST,'-'),(0.002,BLUE,(0,(4,3)))]:
        normalized = gamma_solution(time,delta) / (1/(2*delta))
        axes[0].plot(time,normalized,color=color,linestyle=pattern,linewidth=2,label=f'Intrinsic product {delta:g}')
        axes[1].plot(delta*time,normalized,color=color,linestyle=pattern,linewidth=2)
    for ax in axes:
        clean(ax)
        ax.set_ylim(0.9,4.2)
        ax.set_ylabel('Gamma divided by its equilibrium',labelpad=9)
    axes[0].set_xlabel('Iteration time',labelpad=9)
    axes[1].set_xlabel('Rescaled time: intrinsic product times t',labelpad=9)
    axes[0].legend(loc='upper right',frameon=False,fontsize=8)
    axes[1].set_xlim(0,1.5)
    fig.text(0.06,0.035,'Exact ODE solutions. Noise trace one, initial Gamma four times equilibrium. No network training.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.82,wspace=0.3)
    save(fig,'intrinsic-noise-clock.svg')


def spherical_valley():
    decayed, plain = valley_run(), valley_run(0)
    fig, axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('Small transverse oscillations can move along a valley.',x=0.06,y=0.96,ha='left',fontsize=17)
    axes[0].plot(decayed[:,0],decayed[:,3],color=RUST,linewidth=2,label='Decay 0.01')
    axes[0].plot(plain[:,0],plain[:,3],color=BLUE,linewidth=1.8,linestyle=(0,(4,3)),label='No decay')
    axes[0].set_xlabel('Updates',labelpad=9)
    axes[0].set_ylabel('Equatorial curvature at current longitude',labelpad=9)
    axes[0].set_ylim(1.1,2.9)
    axes[0].legend(loc='lower left',frameon=False,fontsize=9)
    axes[1].plot(decayed[:41,0],decayed[:41,2],color=RUST,linewidth=1,marker='o',markersize=3)
    axes[1].axhline(0,color=MUTED,linewidth=0.7)
    axes[1].set_xlabel('First 40 updates with decay',labelpad=9)
    axes[1].set_ylabel('Signed normal coordinate z',labelpad=9)
    for ax in axes:
        clean(ax)
    fig.text(0.06,0.035,'Explicit scale-invariant loss in three dimensions. Same initial weights, raw rate 0.1. Float64 finite calculation.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.82,wspace=0.3)
    save(fig,'spherical-valley-drift.svg')


def moment_rotation():
    degrees = np.linspace(0,90,181)
    diagonal, full = rotation_defects(np.radians(degrees))
    fig, ax = plt.subplots(figsize=(9.2,4.8))
    fig.suptitle('The diagonal moment remembers the coordinate axes.',x=0.07,y=0.96,ha='left',fontsize=17)
    ax.plot(degrees,diagonal,color=RUST,linewidth=2,label='Coordinatewise second moment')
    ax.plot(degrees,full,color=BLUE,linewidth=1.5,linestyle=(0,(4,3)),label='Full-matrix second moment')
    ax.scatter([45],[diagonal[90]],color=RUST,s=30,zorder=4)
    ax.annotate(f'{diagonal[90]:.3f} at 45 degrees',(45,diagonal[90]),xytext=(12,14),textcoords='offset points',fontsize=10,color=RUST)
    ax.set_xlabel('Basis rotation in degrees',labelpad=10)
    ax.set_ylabel('Relative update discrepancy after rotating back',labelpad=10)
    ax.set_xlim(0,90)
    ax.set_ylim(-0.025,max(diagonal)*1.2)
    ax.legend(loc='upper left',frameon=False,fontsize=9)
    clean(ax)
    fig.text(0.07,0.035,'Exact two-dimensional state example. First moment (0.5, 1), second moment diag(1, 9), zero damping.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.12,right=0.97,bottom=0.2,top=0.82)
    save(fig,'moment-rotation-defect.svg')


if __name__ == '__main__':
    style()
    intrinsic_clock()
    spherical_valley()
    moment_rotation()
