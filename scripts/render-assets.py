"""Regenerate the profile's original, theme-aware SVG artwork (Python 3, no dependencies)."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
PALETTES = {
    "light": dict(bg="#f5f8fc", fg="#132238", muted="#50627a", line="#d9e3ef", accent="#087f8c", tint="#e3f4f3", blue="#2864d7"),
    "dark": dict(bg="#101b2b", fg="#edf4ff", muted="#a0b1c8", line="#293b53", accent="#5ee0ce", tint="#153637", blue="#83b2ff"),
}

def text(x, y, value, size=18, color="fg", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{C[color]}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'

def line(x1, y1, x2, y2, color="line", width=1, extra=""):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{C[color]}" stroke-width="{width}" {extra}/>'

def rect(x, y, w, h, fill="bg", radius=12, stroke="line"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{C[fill]}" stroke="{C[stroke]}"/>'

def svg(w, h, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<g font-family="Segoe UI, Arial, sans-serif">
{rect(1, 1, w-2, h-2, radius=20)}
{body}
</g></svg>\n'''

def label(x, y, value):
    return text(x, y, value, 12, "muted", 600, 'letter-spacing="1.6"')

def hero(mobile):
    w, h = (480, 352) if mobile else (960, 356)
    x = 28 if mobile else 40
    body = label(x, 41, "AI ENGINEER  /  DUBAI, UAE")
    if mobile:
        body += text(x, 104, "Abdullah", 48, weight=650)
        body += text(x, 157, "Taufiq.", 48, weight=650)
        body += text(x, 204, "Agents. Retrieval.", 22, "muted")
        body += text(x, 235, "Real-world software.", 22, "muted")
        status_y = 272
    else:
        body += text(x, 121, "Abdullah Taufiq.", 54, weight=650)
        body += text(x, 168, "Agents. Retrieval.", 26, "muted")
        body += text(x, 204, "Real-world software.", 26, "muted")
        status_y = 246
        # A small, original agent-system diagram echoes the work described in the profile.
        body += rect(604, 40, 316, 246, radius=16)
        body += label(626, 68, "FROM CONTEXT TO ACTION")
        body += line(624, 86, 900, 86)
        for cx, cy in [(664, 119), (860, 119), (664, 244), (860, 244)]:
            body += line(762, 183, cx, cy, width=1.5)
        for nx, ny, title in [(619, 101, "MEMORY"), (815, 101, "TOOLS"), (619, 227, "RETRIEVE"), (815, 227, "OBSERVE")]:
            body += rect(nx, ny, 90, 34, radius=7)
            body += text(nx+45, ny+22, title, 11, "muted", 600, 'text-anchor="middle" letter-spacing="0.6"')
        body += rect(711, 158, 102, 49, "tint", radius=10, stroke="accent")
        body += text(762, 188, "AGENTS", 14, "accent", 650, 'text-anchor="middle" letter-spacing="1"')
    body += rect(x, status_y, 276, 38, "tint", radius=19, stroke="tint")
    body += f'<circle cx="{x+18}" cy="{status_y+19}" r="4" fill="{C["accent"]}"/>'
    body += text(x+32, status_y+24, "Currently AI Engineer @ Lorrysa", 14, "accent", 600)
    if not mobile:
        body += line(40, 310, 920, 310)
        body += label(40, 335, "MULTI-AGENT SYSTEMS   ·   KNOWLEDGE GRAPHS   ·   PRODUCTION APIs")
    return svg(w, h, "Abdullah Taufiq — AI Engineer in Dubai. Currently at Lorrysa.", body)

PROJECTS = [
    ("agent", "01 / AUTOMATION", "Multi-Purpose Agent", ["One agent for document summaries, Q&A,", "and LinkedIn drafts from URLs and PDFs."], ["Document summaries, Q&A, and LinkedIn", "drafts from URLs and PDFs."], "n8n  /  Python  /  Docker  /  LLMs"),
    ("docling", "02 / DOCUMENT INTELLIGENCE", "Docling API", ["Turn PDFs, office files, and images into", "structured content with table extraction."], ["PDFs, office files, and images into", "structured content and extracted tables."], "Python  /  FastAPI  /  Docker"),
    ("memory", "03 / AGENT MEMORY", "Agent Memory Workflows", ["Extract content, generate useful tags,", "and store searchable memories in A-Mem."], ["Extract content, tag it with AI, and", "store searchable memories in A-Mem."], "A-Mem  /  n8n  /  Python  /  LLMs"),
]

def project(data, mobile):
    slug, category, title, desktop_lines, mobile_lines, tech = data
    w, h = (480, 244) if mobile else (960, 196)
    x = 28 if mobile else 36
    body = label(x, 33, category)
    body += text(x, 75, title, 28 if mobile else 31, weight=650)
    for i, s in enumerate(mobile_lines if mobile else desktop_lines):
        body += text(x, 111+i*26, s, 18, "muted")
    body += line(x, h-52, w-x, h-52)
    body += text(x, h-22, tech, 14, "accent", 500)
    if not mobile:
        body += text(912, 40, "↗", 25, "accent", extra='text-anchor="end"')
        if slug == "agent":
            for nx, ny in [(760, 58), (865, 65), (844, 131)]:
                body += line(802, 94, nx, ny, "blue", 2)
                body += f'<circle cx="{nx}" cy="{ny}" r="10" fill="{C["bg"]}" stroke="{C["blue"]}" stroke-width="2"/>'
            body += f'<circle cx="802" cy="94" r="18" fill="{C["tint"]}" stroke="{C["accent"]}" stroke-width="2"/>'
        elif slug == "docling":
            body += rect(775, 46, 74, 89, radius=7)
            for yy in [64, 77, 90]:
                body += line(788, yy, 834, yy, "blue", 2)
            body += rect(788, 104, 46, 18, "tint", radius=2, stroke="accent")
        else:
            for dx, dy in [(0, 0), (14, -12), (28, -24)]:
                body += rect(767+dx, 77+dy, 66, 49, radius=7)
                body += line(780+dx, 94+dy, 819+dx, 94+dy, "blue", 2)
                body += line(780+dx, 106+dy, 805+dx, 106+dy, "accent", 2)
    return svg(w, h, title + ". " + " ".join(desktop_lines), body)

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for theme, C in PALETTES.items():
        for mobile in [False, True]:
            suffix = f'{"mobile-" if mobile else ""}{theme}'
            (OUT / f"hero-{suffix}.svg").write_text(hero(mobile), encoding="utf-8")
            for data in PROJECTS:
                (OUT / f"project-{data[0]}-{suffix}.svg").write_text(project(data, mobile), encoding="utf-8")
    print("Generated 16 SVGs: light/dark, desktop/mobile.")
