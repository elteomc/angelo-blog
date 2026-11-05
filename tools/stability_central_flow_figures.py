"""Draw the explicit quadratic, two-cycle, and averaged-flow examples."""
import math
import numpy as np

from decay_momentum_figures import style,save as save_base,OUT,INK,MUTED,LINE,RUST,BLUE
import matplotlib.pyplot as plt
from check_stability_central_flows import trajectory,cycle,loss,hessian,central_y,GAMMA,TARGET,INITIAL


def save(fig,name):
    save_base(fig,name)
    path = OUT/name
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')


def clean(ax):
    ax.grid(axis='y',color=LINE,linewidth=0.6)
    ax.set_axisbelow(True)


def quadratic_stability():
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('A frozen quadratic exposes the discrete boundary.',x=0.06,y=0.96,ha='left',fontsize=17)
    x = np.linspace(0,3,301)
    left,right = axes
    left.axvspan(2,3,color=RUST,alpha=0.07)
    left.axhline(1,color=MUTED,linewidth=0.8)
    left.axvline(2,color=MUTED,linewidth=0.8,linestyle=(0,(3,3)))
    left.plot(x,np.abs(1-x),color=RUST,linewidth=2,label='Absolute GD multiplier')
    left.plot(x,np.exp(-x),color=BLUE,linewidth=1.7,label='Exact flow over one step')
    left.set_xlim(0,3)
    left.set_ylim(0,2.15)
    left.set_xlabel('Step size times positive curvature',labelpad=9)
    left.set_ylabel('One-step amplification',labelpad=9)
    left.legend(frameon=False,fontsize=8,loc='upper left')
    t = np.arange(61)
    stable = 0.1*(2*0.8**t)**2
    unstable = 1.1*(1e-4*1.2**t)**2
    right.semilogy(t,stable+unstable,color=INK,linewidth=2,label='Total loss')
    right.semilogy(t,stable,color=BLUE,linewidth=1.2,label='Stable-mode contribution')
    right.semilogy(t,unstable,color=RUST,linewidth=1.2,linestyle=(0,(4,3)),label='Unstable-mode contribution')
    right.set_ylim(1e-10,100)
    right.set_xlabel('Gradient-descent updates',labelpad=9)
    right.set_ylabel('Quadratic loss',labelpad=9)
    right.legend(frameon=False,fontsize=8,loc='upper left')
    for ax in axes: clean(ax)
    fig.text(0.06,0.035,'Exact formulas. Right panel: rate 1, curvatures 0.2 and 2.2, initial coordinates 2 and 0.0001.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.81,wspace=0.32)
    save(fig,'quadratic-stability-boundary.svg')


def feedback_cycle():
    values = trajectory()
    t = np.arange(len(values))
    amp,center_y = cycle()
    sharpness = [np.linalg.eigvalsh(hessian(w))[-1] for w in values]
    fig = plt.figure(figsize=(10.4,7.0))
    grid = fig.add_gridspec(2,2)
    upper = fig.add_subplot(grid[0,:])
    left,right = fig.add_subplot(grid[1,0]),fig.add_subplot(grid[1,1])
    fig.suptitle('The oscillation changes the curvature it encounters.',x=0.06,y=0.97,ha='left',fontsize=17)
    upper.plot(t[:161],values[:161,0],color=RUST,linewidth=0.85,label='Exact alternating coordinate')
    for sign in [-1,1]: upper.axhline(sign*amp,color=MUTED,linewidth=0.8,linestyle=(0,(4,3)))
    upper.set_ylabel('Oscillating coordinate x',labelpad=9)
    upper.set_xlabel('Updates, onset detail',labelpad=6)
    upper.legend(frameon=False,fontsize=8,loc='upper left')
    left.plot(t,1+values[:,1],color=BLUE,linewidth=1.6,label='Coordinate curvature')
    left.plot(t,sharpness,color=RUST,linewidth=1.4,label='Full largest Hessian eigenvalue')
    left.axhline(2,color=MUTED,linewidth=0.8,linestyle=(0,(4,3)))
    left.set_ylim(1.32,2.19)
    left.set_xlabel('Gradient-descent updates',labelpad=8)
    left.set_ylabel('Curvature',labelpad=9)
    left.legend(frameon=False,fontsize=8,loc='lower right')
    right.plot(t,[loss(w) for w in values],color=INK,linewidth=1.6,label='Actual iterate loss')
    right.axhline(loss([amp,center_y]),color=RUST,linewidth=1,linestyle=(0,(4,3)),label='Exact cycle loss')
    right.set_xlabel('Gradient-descent updates',labelpad=8)
    right.set_ylabel('Loss',labelpad=9)
    right.legend(frameon=False,fontsize=8,loc='lower right')
    for ax in [upper,left,right]: clean(ax)
    fig.text(0.06,0.03,'Explicit two-variable polynomial. Rate 1, 400 updates, no data or stochastic gradients.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.13,top=0.89,wspace=0.31,hspace=0.53)
    save(fig,'self-stabilizing-cycle.svg')


def averaged_flow():
    values = trajectory()
    t = np.arange(len(values))
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('Keep the fluctuation effect after removing its phase.',x=0.06,y=0.96,ha='left',fontsize=17)
    left,right = axes
    pair_y = (values[:-1,1]+values[1:,1])/2
    left.plot(t[:-1]+0.5,pair_y,color=INK,linewidth=1.8,label='Adjacent-pair average of GD')
    left.plot(t,central_y(t),color=RUST,linewidth=1.7,label='Constrained center model')
    left.plot(t,TARGET-(TARGET-INITIAL[1])*np.exp(-GAMMA*t),color=BLUE,linewidth=1.4,linestyle=(0,(4,3)),label='Ordinary gradient flow')
    left.set_xlim(0,160)
    left.set_ylim(0.35,1.17)
    left.set_xlabel('Optimizer-step time, rate 1',labelpad=9)
    left.set_ylabel('Curvature coordinate y',labelpad=9)
    left.legend(frameon=False,fontsize=8,loc='lower right')
    amp,y = cycle()
    center_loss = loss([0,y])
    fluctuation = amp*amp
    right.bar([0,1],[center_loss,center_loss],color=BLUE,width=0.55,label='Loss at cycle center')
    right.bar([1],[fluctuation],bottom=[center_loss],color=RUST,width=0.55,label='Displacement contribution')
    right.set_xticks([0,1],['Center','Actual cycle'])
    right.set_ylim(0,0.058)
    right.set_ylabel('Equilibrium loss',labelpad=9)
    right.legend(frameon=False,fontsize=8,loc='upper left')
    for ax in axes: clean(ax)
    fig.text(0.06,0.035,'Same explicit recurrence as Part 29. The constrained model misses the onset delay. No fitted cycle amplitude.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.81,wspace=0.31)
    save(fig,'central-flow-average.svg')


if __name__ == '__main__':
    style()
    quadratic_stability()
    feedback_cycle()
    averaged_flow()
