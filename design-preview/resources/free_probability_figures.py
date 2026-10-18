"""Reproduce the free probability series figures and numerical tables."""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/free-probability'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.facecolor': '#fffdf8',
                     'axes.facecolor': '#fffdf8', 'savefig.facecolor': '#fffdf8'})
BLUE, ORANGE, GREEN = '#285f91', '#bc542c', '#327764'
rng = np.random.default_rng(1729)

def save(fig, name):
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight')
    fig.savefig(OUT / (name + '.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

def haar(n):
    z = (rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    diagonal = np.diag(r)
    return q * (diagonal / np.abs(diagonal))[None, :]

def signs(n):
    assert n % 2 == 0
    return np.r_[np.ones(n//2), -np.ones(n//2)]

def rotated(n):
    d = signs(n)
    u = haar(n)
    b = (u*d) @ u.conj().T
    a = np.diag(d)
    e = np.linalg.eigvalsh(a+b)
    mixed = np.trace((a@b)@(a@b)).real/n
    return e, float(mixed), float(np.max(np.abs(u.conj().T@u-np.eye(n))))

def wishart(n, m):
    x = (rng.normal(size=(n,m)) + 1j*rng.normal(size=(n,m))) / np.sqrt(2*m)
    return x @ x.conj().T

# The three pairings on four cyclically ordered points.
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
points = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])
for ax, pairs, label in zip(axes, [[(0,1),(2,3)],[(0,3),(1,2)],[(0,2),(1,3)]],
                           ['(1,2)(3,4): noncrossing', '(1,4)(2,3): noncrossing', '(1,3)(2,4): crossing']):
    for i, j in pairs:
        ax.plot(points[[i,j],0], points[[i,j],1], color=ORANGE if '): crossing' in label else BLUE, lw=3)
    ax.scatter(points[:,0], points[:,1], s=40, c=GREEN, zorder=3)
    for k, (x,y) in enumerate(points):
        ax.text(x*1.2, y*1.2, str(k+1), ha='center', va='center')
    ax.set(xlim=(-1.6,1.6), ylim=(-1.6,1.6), aspect='equal', title=label)
    ax.axis('off')
fig.tight_layout()
save(fig, 'pairings')

# Compare the same marginal spectra with different relative eigenbases.
n = 384
d = signs(n)
aligned = 2*d
permuted = d + rng.permutation(d)
spectra, mixed_values, orth_errors = [], [], []
for _ in range(6):
    e, mixed, err = rotated(n)
    spectra.append(e)
    mixed_values.append(mixed)
    orth_errors.append(err)
pooled = np.concatenate(spectra)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
for ax, ev, title in zip(axes[:2], [aligned, permuted], ['Aligned eigenbases', 'Random permutation']):
    values, counts = np.unique(ev, return_counts=True)
    ax.bar(values, counts/n, width=.25, color=BLUE)
    ax.set(xlabel='Eigenvalue', ylabel='Probability mass', title=title, xlim=(-2.3,2.3), ylim=(0,.6))
x = np.linspace(-1.99,1.99,600)
axes[2].hist(pooled, bins=45, range=(-2,2), density=True, alpha=.55, color=BLUE, label='Six matrices, n = 384')
axes[2].plot(x, 1/(np.pi*np.sqrt(4-x*x)), c=ORANGE, lw=2, label='Arcsine density')
axes[2].set(xlabel='Eigenvalue', ylabel='Density', title='Haar-rotated eigenbases', xlim=(-2.3,2.3))
axes[2].legend(fontsize=8)
fig.tight_layout()
save(fig, 'sum-comparison')

# Fixed-moment checks across dimensions. The spread is not a confidence interval.
rows=[]
for size in (64,128,256):
    vals=[]
    for _ in range(10):
        e, mixed, err = rotated(size)
        vals.append([float(np.mean(e**2)),float(np.mean(e**4)),mixed])
        orth_errors.append(err)
    data=np.array(vals)
    rows.append({'n':size,'m2':float(data[:,0].mean()),'m4':float(data[:,1].mean()),
                 'abab_mean':float(data[:,2].mean()),'abab_rms':float(np.sqrt(np.mean(data[:,2]**2)))})
fig, ax=plt.subplots(figsize=(6.5,3.6))
ax.plot([r['n'] for r in rows],[r['abab_rms'] for r in rows], 'o-',c=BLUE)
ax.set(xlabel='Matrix dimension n',ylabel='RMS of normalized trace of ABAB',title='An alternating centered moment becomes small',xticks=[64,128,256])
fig.tight_layout()
save(fig,'mixed-moment')

# Mean-one Marchenko-Pastur laws, including the zero atom for n/m > 1.
fig, axes=plt.subplots(1,3,figsize=(12,3.7))
mp_rows=[]
for ax, gamma in zip(axes, [.5,1,2]):
    size=320
    m=round(size/gamma)
    ev=np.linalg.eigvalsh(wishart(size,m))
    lo,hi=(1-np.sqrt(gamma))**2,(1+np.sqrt(gamma))**2
    positive=ev[ev>1e-9]
    bins=np.linspace(0,hi*1.08,45)
    counts,edges=np.histogram(positive,bins=bins)
    ax.bar(edges[:-1],counts/(size*np.diff(edges)),width=np.diff(edges),align='edge',alpha=.5,color=BLUE)
    xx=np.linspace(max(lo,0)+.002,hi-.002,700)
    density=np.sqrt((hi-xx)*(xx-lo))/(2*np.pi*gamma*xx)
    ax.plot(xx,density,c=ORANGE,lw=2)
    atom=max(0,1-1/gamma)
    ax.set(xlabel='Eigenvalue',ylabel='Continuous density',title=f'Aspect ratio γ = {gamma:g}')
    ax.text(.97,.93,f'Zero mass: {atom:g}',transform=ax.transAxes,ha='right',va='top')
    mp_rows.append({'gamma':gamma,'m1':float(ev.mean()),'m2':float(np.mean(ev**2)),
                    'zero_fraction':float(np.mean(ev<1e-9)),'expected_zero_fraction':atom})
fig.tight_layout()
save(fig,'marchenko-pastur')

# A positive product of independent square covariance matrices.
product_moments=[]
product_spectra=[]
for _ in range(8):
    size=384
    a,b=wishart(size,size),wishart(size,size)
    w,v=np.linalg.eigh(a)
    root=(v*np.sqrt(np.maximum(w,0)))@v.conj().T
    p=root@b@root
    ev=np.linalg.eigvalsh((p+p.conj().T)/2)
    product_spectra.append(ev)
    product_moments.append([float(np.mean(ev**k)) for k in range(1,5)])
prod=np.array(product_moments)
theory=np.array([math.comb(3*k,k)/(2*k+1) for k in range(1,5)])
fig,ax=plt.subplots(figsize=(7,3.8))
ax.hist(np.concatenate(product_spectra),bins=65,range=(0,7.5),density=True,color=BLUE,alpha=.65)
ax.axvline(27/4,c=ORANGE,ls='--',label='Limiting right endpoint 27/4')
ax.set(xlabel='Eigenvalue',ylabel='Density',title='Product of two independent square covariance matrices')
ax.legend(fontsize=9)
fig.tight_layout()
save(fig,'covariance-product')

# Independent exact checks of the coefficients used in the articles.
# P(t) = t (1 + P(t))^3 determines the product moments recursively.
coeff=[0]
for k in range(1,9):
    a=np.array([1]+coeff[1:],dtype=object)
    cube=np.convolve(np.convolve(a,a),a)
    coeff.append(int(cube[k-1]) if k-1<len(cube) else 0)
assert coeff[1:]==[math.comb(3*k,k)//(2*k+1) for k in range(1,9)]
assert max(orth_errors)<1e-12
assert abs(rows[-1]['m2']-2)<.05
assert abs(rows[-1]['m4']-6)<.2
assert rows[-1]['abab_rms']<.03
assert np.all(np.abs(prod.mean(axis=0)/theory-1)<.15)
assert all(abs(r['zero_fraction']-r['expected_zero_fraction'])<1e-8 for r in mp_rows)
report={'seed':1729,'numpy':np.__version__,'matplotlib':matplotlib.__version__,
        'sum_checks':rows,'sum_histogram_n':n,'sum_histogram_draws':6,
        'maximum_unitarity_error':max(orth_errors),'marchenko_pastur':mp_rows,
        'product':{'n':384,'draws':8,'theory':theory.tolist(),'mean':prod.mean(axis=0).tolist(),
                   'sample_sd':prod.std(axis=0,ddof=1).tolist()},'fuss_catalan_first_eight':coeff[1:]}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['| Dimension | Mean second moment | Mean fourth moment | RMS alternating moment |',
       '| --- | ---: | ---: | ---: |']
for r in rows:
    lines.append(f"| {r['n']} | {r['m2']:.5f} | {r['m4']:.5f} | {r['abab_rms']:.5f} |")
(ROOT/'blog/free-prob-4/_sum-table.qmd').write_text('\n'.join(lines)+'\n')
lines=['| Moment | Exact limit | Empirical mean | Sample standard deviation |',
       '| --- | ---: | ---: | ---: |']
for k,(t,m,s) in enumerate(zip(theory,prod.mean(axis=0),prod.std(axis=0,ddof=1)),1):
    lines.append(f'| {k} | {t:g} | {m:.5f} | {s:.5f} |')
(ROOT/'blog/free-prob-6/_product-table.qmd').write_text('\n'.join(lines)+'\n')
print(json.dumps(report,indent=2))
