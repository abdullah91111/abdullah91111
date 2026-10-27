"""Render the existing portfolio banner and simple logo badges. Python 3, no dependencies."""
from pathlib import Path
from html import escape
import base64
import json
import random

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
TECH = json.loads((ROOT / 'scripts/tech-stack.json').read_text())

def banner(dark):
    photo = base64.b64encode((ASSETS / 'portfolio-banner.webp').read_bytes()).decode()
    edge = '#000000' if dark else '#ffffff'
    rng = random.Random(44)
    leaves, keyframes = [], []
    for i in range(32):
        y = rng.randint(-30, 350)
        end_y = y + rng.randint(-20, 80)
        size = rng.uniform(.45, 1.1)
        duration = rng.uniform(12, 28)
        delay = -rng.uniform(0, duration)
        angle = rng.randint(-150, 150)
        keyframes.append(f'@keyframes leaf{i}{{from{{transform:translate(-24px,{y}px) rotate({angle}deg)}}to{{transform:translate(1310px,{end_y}px) rotate({angle+75}deg)}}}}')
        leaves.append(f'<g class="leaf" style="animation:leaf{i} {duration:.2f}s linear {delay:.2f}s infinite"><g transform="scale({size:.2f})"><path d="M0 -7 Q-7 0 0 7 Q7 0 0 -7" fill="#bfdbfe" stroke="#60a5fa" stroke-width=".4"/><path d="M0 -7 V7" stroke="#60a5fa" stroke-width=".4"/></g></g>')
    image_filter = ' filter="url(#night)"' if dark else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="427" viewBox="0 0 1280 427" role="img" aria-labelledby="title">
<title id="title">The mountain and lake banner from Abdullah Taufiq's portfolio</title>
<defs>
  <filter id="night" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values=".65"/><feComponentTransfer><feFuncR type="linear" slope=".38"/><feFuncG type="linear" slope=".38"/><feFuncB type="linear" slope=".38"/></feComponentTransfer></filter>
  <linearGradient id="sides"><stop offset="0" stop-color="{edge}" stop-opacity=".9"/><stop offset=".06" stop-color="{edge}" stop-opacity="0"/><stop offset=".94" stop-color="{edge}" stop-opacity="0"/><stop offset="1" stop-color="{edge}" stop-opacity=".9"/></linearGradient>
  <linearGradient id="bottom" x2="0" y2="1"><stop offset="0" stop-color="{edge}" stop-opacity="0"/><stop offset="1" stop-color="{edge}" stop-opacity=".9"/></linearGradient>
</defs>
<style>.leaf{{opacity:.6}}{''.join(keyframes)}@media(prefers-reduced-motion:reduce){{.leaf{{display:none}}}}</style>
<image href="data:image/webp;base64,{photo}" width="1280" height="427"{image_filter}/>
{''.join(leaves)}
<path d="M0 0H1280V427H0Z" fill="url(#sides)"/>
<path d="M0 347H1280V427H0Z" fill="url(#bottom)"/>
</svg>\n'''

def badge(item, dark):
    bg, fg, border = ('#111111','#e4e4e7','#27272a') if dark else ('#fafafa','#27272a','#e4e4e7')
    name = escape(item['name'])
    icon = f'<path d="{item["path"]}" transform="translate(12 11) scale(.75)" fill="{fg}"/>' if item['path'] else ''
    label = f'<text x="{40 if icon else 68}" y="24" text-anchor="{"start" if icon else "middle"}" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="{fg}">{name}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="136" height="40" viewBox="0 0 136 40" role="img" aria-label="{name}"><rect x=".5" y=".5" width="135" height="39" rx="8" fill="{bg}" stroke="{border}"/>{icon}{label}</svg>\n'

if __name__ == '__main__':
    (ASSETS/'tech').mkdir(exist_ok=True)
    for dark in [False,True]:
        theme='dark' if dark else 'light'
        (ASSETS/f'portfolio-banner-{theme}.svg').write_text(banner(dark),encoding='utf-8')
        for group in TECH:
            for item in group['items']:
                (ASSETS/'tech'/f'{item["slug"]}-{theme}.svg').write_text(badge(item,dark),encoding='utf-8')
    print('Rendered portfolio banner and 31 tech badges, in light and dark themes.')
