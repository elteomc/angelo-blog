"""Build the two explanatory SVG figures without external dependencies."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/scale-geometry'


def frame(title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="440" viewBox="0 0 960 440" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc>
<rect width="960" height="440" fill="#fffdf8"/>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>
<g font-family="Arial, Helvetica, sans-serif" fill="#262c29">{body}</g></svg>
'''


def radius_figure():
    body = '<text x="36" y="40" font-size="21">Same predictor. Same learning rate. Different rotation.</text>'
    body += '<line x1="480" y1="72" x2="480" y2="385" stroke="#d8d8cd"/>'
    for left, radius in [(0, 1), (480, 2)]:
        x = left + 100
        y = 300
        scale = 108
        end_x = x + scale * radius
        end_y = y - scale * 0.5 / radius
        body += f'<text x="{left + 36}" y="92" font-size="18">Radius {radius}</text>'
        body += f'<text x="{left + 36}" y="118" font-size="14" fill="#656a62">initial weight ({radius}, 0)</text>'
        body += f'<line x1="{x - 35}" y1="{y}" x2="{left + 430}" y2="{y}" stroke="#d8d8cd"/>'
        body += f'<line x1="{x}" y1="{y + 24}" x2="{x}" y2="150" stroke="#d8d8cd"/>'
        body += f'<line x1="{x}" y1="{y}" x2="{end_x}" y2="{y}" stroke="#526f82" stroke-width="3" marker-end="url(#arrow)"/>'
        body += f'<line x1="{end_x}" y1="{y}" x2="{end_x}" y2="{end_y}" stroke="#ad492d" stroke-width="3" marker-end="url(#arrow)"/>'
        body += f'<line x1="{x}" y1="{y}" x2="{end_x}" y2="{end_y}" stroke="#262c29" stroke-width="2" marker-end="url(#arrow)"/>'
        body += f'<circle cx="{x}" cy="{y}" r="4" fill="#262c29"/>'
        body += f'<text x="{end_x + 16}" y="{end_y - 8}" font-size="15" fill="#ad492d">step {0.5 / radius:g}</text>'
        angle = math.degrees(math.atan(0.5 / radius**2))
        body += f'<text x="{left + 36}" y="354" font-size="24">{angle:.2f}°</text>'
        body += f'<text x="{left + 36}" y="380" font-size="14" fill="#656a62">tan(angle) = {0.5 / radius**2:g}</text>'
    body += '<text x="36" y="420" font-size="13" fill="#656a62">Blue: initial weight     Rust: SGD displacement     Ink: updated weight     Learning rate = 0.5</text>'
    return frame('Radius changes an SGD step', 'Two exact raw SGD updates on a scale-invariant squared loss, drawn with the same coordinate scale.', body)


def placement_figure():
    body = '<text x="36" y="40" font-size="21">Where does the scale meet normalization?</text>'
    for y, label, first, second, result in [
        (130, 'Normalize after the matrix', 'cW', 'n(·)', 'n(cWx) = n(Wx)'),
        (290, 'Normalize before the matrix', 'n(·)', 'cW', 'cWn(x) = c · Wn(x)'),
    ]:
        body += f'<text x="36" y="{y - 38}" font-size="17">{label}</text>'
        body += f'<text x="42" y="{y + 7}" font-size="21">x</text>'
        for x, text in [(135, first), (340, second)]:
            body += f'<rect x="{x}" y="{y - 25}" width="120" height="56" rx="6" fill="#eeede4" stroke="#d8d8cd"/>'
            body += f'<text x="{x + 60}" y="{y + 10}" font-size="23" text-anchor="middle">{text}</text>'
        for start, end in [(68, 120), (267, 325), (472, 535)]:
            body += f'<line x1="{start}" y1="{y + 3}" x2="{end}" y2="{y + 3}" stroke="#526f82" stroke-width="2" marker-end="url(#arrow)"/>'
        body += f'<text x="560" y="{y + 10}" font-size="23" fill="#ad492d">{result}</text>'
    body += '<text x="36" y="405" font-size="14" fill="#656a62">Idealized RMS normalization n, positive c, nonzero normalized inputs, and zero epsilon.</text>'
    return frame('Normalization placement determines the symmetry', 'A common matrix scale cancels when RMS normalization follows it. The scale remains when normalization precedes the matrix.', body)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'radius-and-step.svg').write_text(radius_figure())
    (OUT / 'normalization-placement.svg').write_text(placement_figure())
    print('Built two scale and geometry figures')
