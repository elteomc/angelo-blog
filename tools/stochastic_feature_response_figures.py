"""Draw Gaussian response and selected archived feature and network results."""
import math
import numpy as np

from decay_momentum_figures import style,save as save_base,OUT,INK,MUTED,LINE,RUST,BLUE
import matplotlib.pyplot as plt
from check_stochastic_feature_response import record,paired_metrics,mean_and_se


def save(fig,name):
    save_base(fig,name)
    path = OUT/name
    path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines())+"\n")


def clean(ax):
    ax.grid(axis='y',color=LINE,linewidth=0.6)
    ax.set_axisbelow(True)


def gaussian_response():
    x = np.linspace(-2.5,2.5,300)
    fig,axes = plt.subplots(1,2,figsize=(10.4,4.9))
    fig.suptitle('Match the response, then inspect the residual.',x=0.06,y=0.96,ha='left',fontsize=17)
    left,right = axes
    left.plot(x,[math.erf(v/math.sqrt(2)) for v in x],color=RUST,linewidth=2,label='Mean sign proposal')
    left.plot(x,math.sqrt(2/math.pi)*x,color=BLUE,linewidth=1.6,linestyle=(0,(4,3)),label='Affine response at zero')
    left.set_xlabel('Signal divided by noise standard deviation',labelpad=9)
    left.set_ylabel('Mean proposal',labelpad=9)
    left.legend(loc='upper left',frameon=False,fontsize=8)
    shared = 2/math.pi
    right.bar([0,1],[shared,shared],color=BLUE,width=0.55,label='Matched affine component')
    right.bar([1],[1-shared],bottom=[shared],color=RUST,width=0.55,label='Uncorrelated residual')
    right.set_xticks([0,1],['Affine control','Sign update'])
    right.set_ylabel('Proposal variance at zero signal',labelpad=9)
    right.set_ylim(0,1.35)
    right.legend(loc='upper left',frameon=False,fontsize=8)
    for ax in axes: clean(ax)
    fig.text(0.06,0.035,'Exact scalar Gaussian sign example. Unit input variance. Residual variance is one minus two over pi.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.09,right=0.98,bottom=0.2,top=0.81,wspace=0.3)
    save(fig,'gaussian-response-residual.svg')


def feature_prediction():
    data = record()['feature']
    modes = ['frob','polar','ns5']
    fig,ax = plt.subplots(figsize=(9.5,4.9))
    fig.suptitle('The slow equation predicts this constructed feature drift.',x=0.07,y=0.96,ha='left',fontsize=17)
    for rate,shift,color in [(0.02,-0.12,RUST),(0.01,0.12,BLUE)]:
        rows = [next(r for r in data['measured'] if r['mode']==mode and r['rate']==rate) for mode in modes]
        ax.errorbar(np.arange(3)+shift,[r['mean_theta_change'] for r in rows],
                    yerr=[r['se_theta_change'] for r in rows],fmt='o',color=color,capsize=4,label=f'Measured, rate {rate:g}',markersize=6)
    predicted = [next(r['predicted_theta_change'] for r in data['predictions'] if r['mode']==mode) for mode in modes]
    ax.scatter(np.arange(3),predicted,marker='D',facecolor='none',edgecolor=INK,s=55,zorder=5,label='Averaged equation')
    ax.axhline(0,color=MUTED,linewidth=0.8)
    ax.set_xticks(np.arange(3),['Output-normalized\ngradient','Exact polar','Five quintic stages'])
    ax.set_ylim(-0.08,0.43)
    ax.set_ylabel('Change in the feature parameter',labelpad=10)
    ax.legend(loc='upper left',frameon=False,fontsize=9)
    clean(ax)
    fig.text(0.07,0.035,'Archived coupled model. Slow horizon 16, decay 0.1. Error bars: one standard error across trajectory copies.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.11,right=0.97,bottom=0.21,top=0.82)
    save(fig,'feature-drift-prediction.svg')


def network_controls():
    fig,axes = plt.subplots(1,2,figsize=(10.4,5.0),sharey=True)
    fig.suptitle('Angle matching leaves a gap that response largely explains.',x=0.06,y=0.96,ha='left',fontsize=17)
    for ax,phase,title in zip(axes,['fresh','exact'],['Fixed noisy labels, calibration every 8 steps','Deterministic labels, calibration every step']):
        for x,arm,color in [(0,'angular_sgd',RUST),(1,'response',BLUE)]:
            values = paired_metrics(phase,arm)
            mean,se = mean_and_se(values)
            ax.scatter(x+np.array([-0.07,-0.025,0.025,0.07]),values,color=color,s=24,zorder=3)
            ax.errorbar([x+0.18],[mean],yerr=[se],fmt='_',color=INK,capsize=4,markersize=10,zorder=5)
        ax.axhline(0,color=MUTED,linewidth=0.9)
        ax.set_xticks([0,1],['Angle and radius','Affine response'])
        ax.set_xlim(-0.35,1.5)
        ax.set_ylim(-0.003,0.028)
        ax.set_title(title,loc='left',fontsize=10,pad=12)
        clean(ax)
    axes[0].set_ylabel('Polar minus comparator, independent-input MSE',labelpad=10)
    fig.text(0.06,0.035,'Archived 1024-step continuations. Four paired seeds per panel. Mean bars show one standard error.',fontsize=9,color=MUTED)
    fig.subplots_adjust(left=0.1,right=0.98,bottom=0.18,top=0.78,wspace=0.18)
    save(fig,'network-response-controls.svg')


if __name__ == '__main__':
    style()
    gaussian_response()
    feature_prediction()
    network_controls()
