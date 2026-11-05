"""Draw exact frozen-kernel, width-scaling, and operator examples."""
import numpy as np

from decay_momentum_figures import style,save as save_base,OUT,INK,MUTED,LINE,RUST,BLUE
import matplotlib.pyplot as plt
from check_width_feature_operators import Z,R0,RATE,EPSILON,frozen_residuals,scaling_step,operator,moment_path


def save(fig,name):
    save_base(fig,name)
    path = OUT/name
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')


def clean(ax):
    ax.grid(axis='y',color=LINE,linewidth=0.6)
    ax.set_axisbelow(True)


def frozen_kernel():
    residuals = frozen_residuals(40)
    t = np.arange(len(residuals))
    eigen,basis = np.linalg.eigh(Z @ Z.T)
    coefficients = np.abs(residuals @ basis)
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('Predictions learn while the feature matrix stays fixed.',x=0.06,y=0.96,ha='left',fontsize=17)
    left,right = axes
    for i,color in enumerate([MUTED,BLUE,RUST]):
        left.semilogy(t,coefficients[:,i],color=color,linewidth=1.8,label=f'Eigenvalue {round(eigen[i])}')
    left.set_ylim(1e-8,3)
    left.set_xlabel('Gradient-descent updates',labelpad=9)
    left.set_ylabel('Absolute residual eigencomponent',labelpad=9)
    left.legend(frameon=False,fontsize=8,loc='lower left')
    right.plot(t,np.mean(residuals*residuals,axis=1)/2,color=INK,linewidth=2,label='Exact squared loss')
    right.axhline(1/18,color=RUST,linewidth=1.2,linestyle=(0,(4,3)),label='Fitting floor 1/18')
    right.set_ylim(0,0.55)
    right.set_xlabel('Gradient-descent updates',labelpad=9)
    right.set_ylabel('Mean half-squared residual',labelpad=9)
    right.legend(frameon=False,fontsize=8,loc='upper right')
    for ax in axes: clean(ax)
    fig.text(0.06,0.035,'Exact three-example linear model. Two feature coordinates, rate 0.5, mean loss normalization.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.81,wspace=0.32)
    save(fig,'frozen-kernel-modes.svg')


def width_scaling():
    widths = 2**np.arange(4,15)
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('Width can preserve outputs while erasing feature motion.',x=0.06,y=0.96,ha='left',fontsize=17)
    for beta,gamma,label,color,dash in [(0.5,0,'Tangent scaling',BLUE,'-'),
                                         (1,0,'Mean output, unchanged rate',MUTED,'--'),
                                         (1,1,'Feature-learning mean scaling',RUST,'-')]:
        rows = [scaling_step(int(n),beta,gamma) for n in widths]
        for ax,key in zip(axes,['feature_change','output_change']):
            ax.loglog(widths,[r[key] for r in rows],color=color,linestyle=dash,linewidth=1.8,label=label)
    axes[0].set_ylabel('One-step activation change',labelpad=9)
    axes[1].set_ylabel('One-step output change',labelpad=9)
    for ax in axes:
        ax.set_xlabel('Number of independently trainable neurons',labelpad=9)
        ax.legend(frameon=False,fontsize=7.5,loc='lower left')
        clean(ax)
    fig.text(0.06,0.035,'Exact centered tanh example. Identical deterministic initialization, target 1, rate constant 0.2.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.81,wspace=0.32)
    save(fig,'width-feature-scales.svg')


def nonlinear_operator():
    ray = np.array([1.,0.5,-0.25])
    t = np.linspace(-3,3,301)
    response = np.array([ray @ operator(s*ray)/(ray @ ray) for s in t])
    linear = t*(ray @ (Z @ Z.T) @ ray)/(len(Z)*EPSILON*(ray @ ray))
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('A fixed representation does not fix the update law.',x=0.06,y=0.96,ha='left',fontsize=17)
    left,right = axes
    left.plot(t,response,color=RUST,linewidth=2,label='Smooth normalized response')
    left.plot(t,linear,color=BLUE,linewidth=1.5,linestyle=(0,(4,3)),label='Matched linear response at zero')
    left.axhline(0,color=MUTED,linewidth=0.6)
    left.axvline(0,color=MUTED,linewidth=0.6)
    left.set_xlabel('Residual scale along a fixed ray',labelpad=9)
    left.set_ylabel('Response projected onto that ray',labelpad=9)
    left.legend(frameon=False,fontsize=8,loc='upper left')
    for initial,color in [(1,RUST),(-1,BLUE)]:
        states = moment_path(initial)
        right.plot([0,1,2],[r['theta'] for r in states],marker='o',color=color,linewidth=1.8,label=f'Initial output {initial:+g}')
    right.axhline(0,color=MUTED,linewidth=0.6)
    right.set_xticks([0,1,2])
    right.set_ylim(-1.65,1.3)
    right.set_xlabel('Updates of the explicit moment rule',labelpad=9)
    right.set_ylabel('Scalar output',labelpad=9)
    right.set_title('Same output at step 1, different next updates',loc='left',fontsize=9,pad=12)
    right.legend(frameon=False,fontsize=8,loc='lower left')
    for ax in axes: clean(ax)
    fig.text(0.06,0.035,'Exact finite models. Left: fixed feature matrix, damping 0.2. Right: fixed scalar feature, persistent moments.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.8,wspace=0.32)
    save(fig,'frozen-feature-operator.svg')


if __name__ == '__main__':
    style()
    frozen_kernel()
    width_scaling()
    nonlinear_operator()
