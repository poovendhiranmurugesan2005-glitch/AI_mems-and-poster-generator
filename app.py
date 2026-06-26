import streamlit as st
import io
import base64
import textwrap
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CreativeAI Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0a0a0f !important;
    color: #e8e4f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e30 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* ── main content ── */
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 100% !important;
}

/* ── hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #13002a 0%, #0a0a1f 40%, #001a13 100%);
    border: 1px solid #2a1a4a;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;  left: -20%;
    width: 60%; height: 200%;
    background: radial-gradient(ellipse, rgba(120,40,255,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40%;  right: -10%;
    width: 50%; height: 180%;
    background: radial-gradient(ellipse, rgba(0,255,150,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: rgba(120,40,255,0.25);
    border: 1px solid rgba(120,40,255,0.5);
    color: #b580ff;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(90deg, #ffffff 0%, #c084fc 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
}
.hero-sub {
    color: #8b8aa0;
    font-size: 1rem;
    max-width: 540px;
    line-height: 1.6;
}

/* ── nav pills ── */
.nav-container {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.nav-pill {
    background: #111120;
    border: 1px solid #2a2a40;
    color: #8b8aa0;
    padding: 0.55rem 1.3rem;
    border-radius: 100px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
}
.nav-pill:hover, .nav-pill.active {
    background: rgba(120,40,255,0.2);
    border-color: #7828ff;
    color: #c084fc;
}

/* ── cards ── */
.card {
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e8e4f0;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-sub {
    color: #5a5870;
    font-size: 0.82rem;
}

/* ── caption output box ── */
.caption-box {
    background: linear-gradient(135deg, #13002a, #0f0f1a);
    border: 1px solid #3a1a6a;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.8rem;
    position: relative;
}
.caption-text {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #e8e4f0;
}
.caption-accent {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #7828ff, #34d399);
    border-radius: 4px 0 0 4px;
}

/* ── stat chips ── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.stat-chip {
    background: #111120;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 0.9rem 1.3rem;
    flex: 1;
    min-width: 110px;
    text-align: center;
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #c084fc, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label { color: #5a5870; font-size: 0.75rem; margin-top: 0.2rem; }

/* ── streamlit widgets override ── */
.stButton > button {
    background: linear-gradient(135deg, #7828ff, #4f1aaa) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #9040ff, #6025cc) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(120,40,255,0.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #047857) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.35) !important;
}
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #111120 !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e4f0 !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7828ff !important;
    box-shadow: 0 0 0 2px rgba(120,40,255,0.2) !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #7828ff, #34d399) !important;
}
label, .stSelectbox label, .stTextInput label, .stTextArea label,
.stSlider label, .stNumberInput label, .stRadio label, .stCheckbox label {
    color: #8b8aa0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
.stRadio > div { gap: 0.4rem !important; }
.stRadio > div > label {
    background: #111120 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.9rem !important;
    color: #8b8aa0 !important;
}
[data-testid="stFileUploader"] {
    background: #111120 !important;
    border: 1px dashed #2a2a40 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #7828ff !important; }
.stColorPicker > div > div { border-radius: 8px !important; }
.stDivider { border-color: #1e1e30 !important; }
[data-testid="stExpander"] {
    background: #111120 !important;
    border: 1px solid #1e1e30 !important;
    border-radius: 12px !important;
}

/* ── section headings ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8e4f0;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e30;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-purple { background: rgba(120,40,255,0.2); color: #c084fc; border: 1px solid rgba(120,40,255,0.3); }
.badge-green  { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-blue   { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }

/* ── preview container ── */
.preview-wrap {
    background: #111120;
    border: 1px solid #2a2a40;
    border-radius: 16px;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}
.preview-label {
    font-size: 0.75rem;
    color: #5a5870;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* ── tip box ── */
.tip-box {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.82rem;
    color: #34d399;
}

/* ── sidebar brand ── */
.sidebar-brand {
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid #1e1e30;
    margin-bottom: 1rem;
}
.brand-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #c084fc, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.brand-tagline { color: #5a5870; font-size: 0.75rem; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Caption AI"
if "generated_caption" not in st.session_state:
    st.session_state.generated_caption = ""
if "poster_img" not in st.session_state:
    st.session_state.poster_img = None
if "meme_img" not in st.session_state:
    st.session_state.meme_img = None
if "bg_img" not in st.session_state:
    st.session_state.bg_img = None

# ─────────────────────────────────────────────
#  AI CAPTION ENGINE  (Gemini via google-generativeai)
# ─────────────────────────────────────────────
def generate_caption(api_key: str, style: str, topic: str, extra: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        style_guides = {
            "Meme": "Generate a hilarious, relatable meme caption with top text and bottom text format. Use internet humor, irony, and wit. Format: TOP: <text>\nBOTTOM: <text>",
            "Motivational": "Write a powerful motivational quote that inspires students. Use strong verbs, vivid imagery, and emotional resonance. Make it shareable and uplifting.",
            "Event Promotion": "Create an exciting, energetic event promotion caption that builds hype and drives attendance. Include a call-to-action. Make it punchy and memorable.",
            "Educational": "Craft an informative yet engaging educational caption that makes learning fun. Use curiosity-sparking language and clear insights.",
            "Social Media": "Write a viral-worthy social media caption with relevant hashtags. Optimize for engagement, use trendy language, and keep it concise. Include 5 relevant hashtags.",
        }

        prompt = f"""You are a creative content specialist for college students in India.
{style_guides[style]}

Topic/Event: {topic}
Additional context: {extra if extra else 'None'}

Generate ONE outstanding caption. Be creative, authentic, and culturally relevant to Indian college students."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except ImportError:
        return _fallback_caption(style, topic)
    except Exception as e:
        return f"[API Error: {str(e)[:120]}]\n\n" + _fallback_caption(style, topic)

def _fallback_caption(style: str, topic: str) -> str:
    fallbacks = {
        "Meme": f"TOP: When the professor says 'this won't come in exam'\nBOTTOM: *{topic} intensifies*",
        "Motivational": f"Your only competition is who you were yesterday. Rise for {topic}. 🚀",
        "Event Promotion": f"🔥 {topic} is HERE! Don't miss the event that'll change everything. Register NOW! ⚡",
        "Educational": f"Did you know? {topic} is revolutionizing the way we think and learn. Dive in! 🎓",
        "Social Media": f"Crushing it at {topic} 💪 Dreams don't work unless you do. #CollegeLife #StudentLife #{topic.replace(' ','')[:15]} #Motivation #India",
    }
    return fallbacks.get(style, f"Creative caption for {topic} — powered by AI ✨")

# ─────────────────────────────────────────────
#  IMAGE HELPERS
# ─────────────────────────────────────────────
GRADIENT_THEMES = {
    "Technology":    [(10, 10, 40), (20, 80, 200), (5, 200, 180)],
    "Education":     [(5, 30, 60), (0, 120, 80), (200, 160, 0)],
    "Sports":        [(60, 5, 5), (200, 50, 0), (255, 180, 0)],
    "Cultural":      [(80, 5, 60), (200, 0, 120), (255, 140, 0)],
    "Hackathon":     [(0, 20, 0), (0, 180, 60), (0, 255, 120)],
    "Festival":      [(80, 20, 0), (220, 80, 0), (255, 200, 0)],
    "Workshop":      [(10, 10, 60), (60, 10, 180), (200, 80, 255)],
    "Symposium":     [(5, 40, 60), (0, 100, 180), (0, 200, 255)],
}

def make_gradient_bg(width: int, height: int, theme: str, add_noise: bool = True) -> Image.Image:
    colors = GRADIENT_THEMES.get(theme, GRADIENT_THEMES["Technology"])
    c1, c2, c3 = [np.array(c) for c in colors]

    img_arr = np.zeros((height, width, 3), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            tx = x / width
            ty = y / height
            diag = (tx + ty) / 2
            top = c1 * (1 - tx) + c2 * tx
            color = top * (1 - ty * 0.7) + c3 * ty * 0.5
            # Add subtle vignette
            vx = abs(tx - 0.5) * 2
            vy = abs(ty - 0.5) * 2
            vignette = 1 - 0.4 * (vx ** 2 + vy ** 2) * 0.5
            img_arr[y, x] = np.clip(color * vignette, 0, 255)

    if add_noise:
        noise = np.random.randint(0, 8, (height, width, 3), dtype=np.uint8)
        img_arr = np.clip(img_arr.astype(np.uint8) + noise, 0, 255)

    img = Image.fromarray(img_arr.astype(np.uint8), "RGB")

    # Overlay glowing orbs
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    orb_color = tuple(min(255, int(c) + 40) for c in colors[1]) + (40,)
    cx, cy = int(width * 0.25), int(height * 0.3)
    r = min(width, height) // 3
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orb_color)
    orb2 = tuple(min(255, int(c) + 30) for c in colors[2]) + (30,)
    cx2, cy2 = int(width * 0.75), int(height * 0.7)
    r2 = r // 2
    draw.ellipse([cx2 - r2, cy2 - r2, cx2 + r2, cy2 + r2], fill=orb2)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img

def _get_font(size: int):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            return ImageFont.load_default()

def _get_font_regular(size: int):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return _get_font(size)

def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_text_shadow(draw, pos, text, font, text_color, shadow_color=(0,0,0,160), shadow_offset=3):
    x, y = pos
    shadow = Image.new("RGBA", (1, 1))  # dummy
    # Draw shadow passes
    for dx, dy in [(-shadow_offset, -shadow_offset), (shadow_offset, shadow_offset),
                   (-shadow_offset, shadow_offset), (shadow_offset, -shadow_offset)]:
        draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=text_color)

def wrap_text(text: str, font, max_width: int, draw: ImageDraw.Draw) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

# ─────────────────────────────────────────────
#  POSTER BUILDER
# ─────────────────────────────────────────────
def create_poster(
    bg_img, title, subtitle, date, venue, description,
    logo_img, font_name, title_size, body_size,
    title_color, body_color, overlay_opacity,
    template_style, caption_text
) -> Image.Image:
    W, H = 900, 1200
    poster = Image.new("RGBA", (W, H), (0, 0, 0, 255))

    # Background
    if bg_img:
        bg = bg_img.resize((W, H), Image.LANCZOS).convert("RGBA")
    else:
        bg = make_gradient_bg(W, H, "Technology").convert("RGBA")
    poster.paste(bg, (0, 0))

    # Overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, int(overlay_opacity * 2.55)))
    poster = Image.alpha_composite(poster, overlay)
    draw = ImageDraw.Draw(poster)

    tc = hex_to_rgb(title_color) + (255,)
    bc = hex_to_rgb(body_color) + (220,)

    title_font   = _get_font(title_size)
    subtitle_font = _get_font(int(title_size * 0.55))
    body_font    = _get_font_regular(body_size)
    small_font   = _get_font_regular(max(18, body_size - 4))

    # ── Template decorations ──
    if template_style == "Modern Neon":
        # Neon accent bars
        draw.rectangle([0, 0, W, 8], fill=(120, 40, 255, 255))
        draw.rectangle([0, H - 8, W, H], fill=(52, 211, 153, 255))
        draw.rectangle([0, 0, 6, H], fill=(120, 40, 255, 200))
        # Corner brackets
        blen = 60
        for x, y, dx, dy in [(30, 30, 1, 1), (W-30, 30, -1, 1), (30, H-30, 1, -1), (W-30, H-30, -1, -1)]:
            draw.line([x, y, x + dx*blen, y], fill=(255,255,255,100), width=2)
            draw.line([x, y, x, y + dy*blen], fill=(255,255,255,100), width=2)

    elif template_style == "Glassmorphism":
        glass = Image.new("RGBA", (W - 80, H - 100), (255, 255, 255, 18))
        poster.paste(glass, (40, 50), glass)
        draw.rounded_rectangle([40, 50, W-40, H-50], radius=24,
                                outline=(255,255,255,60), width=1)

    elif template_style == "Bold Minimal":
        draw.rectangle([0, 0, W, int(H * 0.08)], fill=(255, 255, 255, 20))
        draw.line([60, int(H*0.09), W-60, int(H*0.09)], fill=(255,255,255,80), width=1)

    elif template_style == "Retro Burst":
        # Sunburst lines from center
        import math
        cx, cy = W//2, H//3
        for i in range(24):
            angle = math.radians(i * 15)
            x2 = cx + int(math.cos(angle) * max(W, H))
            y2 = cy + int(math.sin(angle) * max(W, H))
            draw.line([cx, cy, x2, y2], fill=(255,255,200,15), width=2)

    elif template_style == "Circuit Board":
        for _ in range(30):
            x1 = random.randint(0, W)
            y1 = random.randint(0, H)
            length = random.randint(40, 120)
            direction = random.choice(["h", "v"])
            alpha = random.randint(20, 60)
            if direction == "h":
                draw.line([x1, y1, x1+length, y1], fill=(0,255,150,alpha), width=1)
                draw.ellipse([x1+length-3, y1-3, x1+length+3, y1+3], fill=(0,255,150,80))
            else:
                draw.line([x1, y1, x1, y1+length], fill=(0,255,150,alpha), width=1)
                draw.ellipse([x1-3, y1+length-3, x1+3, y1+length+3], fill=(0,255,150,80))

    # ── Logo ──
    y_cursor = 60
    if logo_img:
        logo = logo_img.copy().convert("RGBA")
        logo.thumbnail((120, 120))
        lw, lh = logo.size
        poster.paste(logo, (W - lw - 50, y_cursor), logo)

    # ── Title ──
    y_cursor = 120
    title_lines = wrap_text(title.upper(), title_font, W - 100, draw)
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw_text_shadow(draw, (x, y_cursor), line, title_font, tc, shadow_offset=4)
        y_cursor += bbox[3] - bbox[1] + 10
    y_cursor += 10

    # ── Subtitle ──
    if subtitle:
        sub_lines = wrap_text(subtitle, subtitle_font, W - 120, draw)
        for line in sub_lines:
            bbox = draw.textbbox((0, 0), line, font=subtitle_font)
            lw = bbox[2] - bbox[0]
            x = (W - lw) // 2
            draw.text((x, y_cursor), line, font=subtitle_font, fill=bc)
            y_cursor += bbox[3] - bbox[1] + 8
    y_cursor += 20

    # ── Divider ──
    draw.line([W//4, y_cursor, 3*W//4, y_cursor], fill=(255,255,255,80), width=2)
    y_cursor += 30

    # ── Date & Venue ──
    if date or venue:
        info_font = _get_font(int(body_size * 1.1))
        for icon, text in [("📅", date), ("📍", venue)]:
            if text:
                line = f"{icon}  {text}"
                bbox = draw.textbbox((0, 0), line, font=info_font)
                lw = bbox[2] - bbox[0]
                draw.text(((W - lw)//2, y_cursor), line, font=info_font,
                          fill=(255, 255, 255, 220))
                y_cursor += bbox[3] - bbox[1] + 12
        y_cursor += 15

    # ── Description ──
    if description:
        desc_lines = wrap_text(description, body_font, W - 160, draw)
        for line in desc_lines:
            bbox = draw.textbbox((0, 0), line, font=body_font)
            lw = bbox[2] - bbox[0]
            draw.text(((W - lw)//2, y_cursor), line, font=body_font,
                      fill=(200, 200, 220, 200))
            y_cursor += bbox[3] - bbox[1] + 8
        y_cursor += 20

    # ── AI Caption ──
    if caption_text:
        draw.line([W//4, y_cursor, 3*W//4, y_cursor], fill=(255,255,255,40), width=1)
        y_cursor += 20
        cap_font = _get_font(int(body_size * 0.9))
        cap_lines = wrap_text(f'"{caption_text}"', cap_font, W - 180, draw)
        for line in cap_lines:
            bbox = draw.textbbox((0, 0), line, font=cap_font)
            lw = bbox[2] - bbox[0]
            draw.text(((W - lw)//2, y_cursor), line, font=cap_font,
                      fill=(180, 140, 255, 220))
            y_cursor += bbox[3] - bbox[1] + 8

    # ── Footer band ──
    footer_h = 60
    footer = Image.new("RGBA", (W, footer_h), (0, 0, 0, 160))
    poster.paste(footer, (0, H - footer_h), footer)
    footer_font = _get_font_regular(22)
    draw.text((W//2 - 80, H - 40), "✨ CreativeAI Studio", font=footer_font,
              fill=(150, 120, 255, 180))

    return poster.convert("RGB")

# ─────────────────────────────────────────────
#  MEME BUILDER
# ─────────────────────────────────────────────
MEME_TEMPLATES = {
    "Drake (Approve/Reject)":    {"top_label": "Reject:", "bottom_label": "Approve:"},
    "Distracted Boyfriend":      {"top_label": "Distraction:", "bottom_label": "Ignoring:"},
    "This Is Fine (Dog in fire)":{"top_label": "Reality:", "bottom_label": "Me:"},
    "Two Buttons":               {"top_label": "Button A:", "bottom_label": "Button B:"},
    "Galaxy Brain":              {"top_label": "Normal thought:", "bottom_label": "Big brain move:"},
    "Change My Mind":            {"top_label": "Controversial statement:", "bottom_label": ""},
    "Expanding Brain":           {"top_label": "Basic idea:", "bottom_label": "Massive brain:"},
    "Surprised Pikachu":         {"top_label": "Does something risky:", "bottom_label": "Shocked at result:"},
}

def create_meme(template_name: str, top_text: str, bottom_text: str,
                font_size: int, text_color: str, bg_image=None,
                bg_theme: str = "Hackathon") -> Image.Image:
    W, H = 900, 700
    if bg_image:
        img = bg_image.resize((W, H), Image.LANCZOS).convert("RGB")
    else:
        img = make_gradient_bg(W, H, bg_theme)

    # Blur + darken for readability
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.blend(img, dark, 0.35)

    draw = ImageDraw.Draw(img)
    font = _get_font(font_size)
    tc = hex_to_rgb(text_color) + (255,)

    # Template label bars
    tmpl = MEME_TEMPLATES.get(template_name, {"top_label": "", "bottom_label": ""})
    label_font = _get_font_regular(22)

    if tmpl["top_label"]:
        bar = Image.new("RGBA", (W, 36), (0, 0, 0, 160))
        img.paste(bar.convert("RGB"), (0, 0))
        draw.text((16, 8), tmpl["top_label"], font=label_font, fill=(180,180,180,200))

    # Top text
    top_lines = wrap_text(top_text.upper(), font, W - 60, draw)
    y = 48
    for line in top_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw_text_shadow(draw, (x, y), line, font, tc, shadow_offset=4)
        y += bbox[3] - bbox[1] + 6

    # Bottom text
    if bottom_text:
        if tmpl["bottom_label"]:
            bar2 = Image.new("RGBA", (W, 36), (0, 0, 0, 160))
            img.paste(bar2.convert("RGB"), (0, H - 36))
            draw.text((16, H - 30), tmpl["bottom_label"], font=label_font, fill=(180,180,180,200))

        bot_lines = wrap_text(bottom_text.upper(), font, W - 60, draw)
        total_h = sum(
            draw.textbbox((0,0), l, font=font)[3] - draw.textbbox((0,0), l, font=font)[1] + 6
            for l in bot_lines
        )
        y = H - total_h - 55
        for line in bot_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            x = (W - lw) // 2
            draw_text_shadow(draw, (x, y), line, font, tc, shadow_offset=4)
            y += bbox[3] - bbox[1] + 6

    # Watermark
    wm_font = _get_font_regular(18)
    draw.text((W - 180, H - 24), "CreativeAI Studio", font=wm_font, fill=(120,100,180,120))
    return img

# ─────────────────────────────────────────────
#  HELPER: img to bytes
# ─────────────────────────────────────────────
def img_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def img_to_b64(img: Image.Image) -> str:
    return base64.b64encode(img_to_bytes(img)).decode()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-logo">🎨 CreativeAI</div>
        <div class="brand-tagline">Studio for college creators</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    tabs = ["🤖 Caption AI", "🖼️ Poster Creator", "😂 Meme Generator", "🌌 AI Background", "⚙️ Settings"]
    for tab in tabs:
        label = tab.split(" ", 1)[1]
        is_active = st.session_state.active_tab == label
        if st.button(tab, key=f"nav_{label}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_tab = label

    st.divider()
    st.markdown("**🔑 Gemini API Key**")
    api_key = st.text_input("API Key", type="password",
                            placeholder="AIza...",
                            help="Get free key at aistudio.google.com",
                            key="gemini_key")
    if api_key:
        st.markdown('<div class="badge badge-green">✓ API Key Set</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge badge-purple">Enter key for AI captions</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="color:#5a5870;font-size:0.75rem;line-height:1.6">
    <b style="color:#8b8aa0">Quick Tips</b><br>
    → Upload custom images for richer posters<br>
    → Try all 5 caption styles<br>
    → Mix AI captions with poster creator<br>
    → Export as PNG for best quality
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="text-align:center;color:#3a3850;font-size:0.72rem">
    CreativeAI Studio v2.0<br>Built for Indian College Students
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN AREA
# ─────────────────────────────────────────────
active = st.session_state.active_tab

# ── HERO ──
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-tag">AI-Powered Design Studio</div>
    <div class="hero-title">CreativeAI Studio 🎨</div>
    <div class="hero-sub">Generate professional posters, viral memes, and AI captions for college events, hackathons, cultural programs & more — in seconds.</div>
</div>
""", unsafe_allow_html=True)

# ── STATS ──
st.markdown("""
<div class="stat-row">
    <div class="stat-chip"><div class="stat-num">5</div><div class="stat-label">Caption Styles</div></div>
    <div class="stat-chip"><div class="stat-num">8</div><div class="stat-label">Poster Templates</div></div>
    <div class="stat-chip"><div class="stat-num">8</div><div class="stat-label">Meme Formats</div></div>
    <div class="stat-chip"><div class="stat-num">8</div><div class="stat-label">BG Themes</div></div>
    <div class="stat-chip"><div class="stat-num">∞</div><div class="stat-label">Possibilities</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TAB: CAPTION AI
# ═══════════════════════════════════════════════
if active == "Caption AI":
    st.markdown('<div class="section-heading">🤖 AI Caption Generator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">✍️ Caption Settings</div>', unsafe_allow_html=True)

        caption_style = st.selectbox(
            "Caption Style",
            ["Meme", "Motivational", "Event Promotion", "Educational", "Social Media"],
            help="Choose the tone and purpose"
        )
        topic = st.text_input("Topic / Event Name", placeholder="e.g. Annual Tech Symposium 2025, Culturals, Hackathon…")
        extra = st.text_area("Extra context (optional)", placeholder="Target audience, key highlights, theme color, speakers…", height=90)

        col_gen, col_clear = st.columns(2)
        with col_gen:
            gen_clicked = st.button("⚡ Generate Caption", use_container_width=True)
        with col_clear:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.generated_caption = ""

        st.markdown('</div>', unsafe_allow_html=True)

        # Style guide
        st.markdown("""
        <div class="card">
        <div class="card-title">🎯 Style Guide</div>
        <div style="display:grid;gap:0.5rem;margin-top:0.5rem">
            <div><span class="badge badge-purple">Meme</span> <span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.5rem">Humor, irony, top+bottom format</span></div>
            <div><span class="badge badge-green">Motivational</span> <span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.5rem">Inspiring quotes, strong verbs</span></div>
            <div><span class="badge badge-blue">Event Promo</span> <span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.5rem">Hype-building, call-to-action</span></div>
            <div><span class="badge badge-purple">Educational</span> <span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.5rem">Insightful, curiosity-sparking</span></div>
            <div><span class="badge badge-green">Social Media</span> <span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.5rem">Viral, hashtags, trendy</span></div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if gen_clicked:
            if not topic:
                st.error("Please enter a topic or event name.")
            else:
                with st.spinner("AI is crafting your caption…"):
                    key = st.session_state.get("gemini_key", "")
                    st.session_state.generated_caption = generate_caption(key, caption_style, topic, extra)

        if st.session_state.generated_caption:
            st.markdown(f"""
            <div class="caption-box">
                <div class="caption-accent"></div>
                <div style="margin-bottom:0.5rem">
                    <span class="badge badge-purple">{caption_style}</span>
                    <span style="color:#5a5870;font-size:0.75rem;margin-left:0.5rem">AI Generated</span>
                </div>
                <div class="caption-text">{st.session_state.generated_caption.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            edited_caption = st.text_area("✏️ Edit Caption", value=st.session_state.generated_caption, height=140, key="edit_cap")
            if edited_caption != st.session_state.generated_caption:
                st.session_state.generated_caption = edited_caption

            st.markdown('<div class="tip-box">💡 Tip: Copy this caption to the Poster Creator or Meme Generator!</div>', unsafe_allow_html=True)

            if st.button("📤 Use in Poster Creator", use_container_width=True):
                st.session_state.active_tab = "Poster Creator"
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;background:#0f0f1a;border:1px dashed #2a2a40;border-radius:16px">
                <div style="font-size:3rem">🤖</div>
                <div style="color:#3a3850;margin-top:1rem;font-size:0.9rem">Fill in the form and click<br><b style="color:#7828ff">Generate Caption</b> to get started</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TAB: POSTER CREATOR
# ═══════════════════════════════════════════════
elif active == "Poster Creator":
    st.markdown('<div class="section-heading">🖼️ Poster Creator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.1], gap="large")

    with col1:
        with st.expander("📝 Event Details", expanded=True):
            p_title = st.text_input("Event Title *", placeholder="NATIONAL TECH SYMPOSIUM 2025")
            p_subtitle = st.text_input("Subtitle / Tagline", placeholder="Where Innovation Meets Excellence")
            p_date = st.text_input("Date", placeholder="15th March 2025 | 9:00 AM onwards")
            p_venue = st.text_input("Venue", placeholder="Main Auditorium, Engineering Block A")
            p_desc = st.text_area("Description", placeholder="Join us for an extraordinary day of…", height=80)

        with st.expander("🎨 Design", expanded=True):
            p_template = st.selectbox("Template Style",
                ["Modern Neon", "Glassmorphism", "Bold Minimal", "Retro Burst", "Circuit Board"])
            p_theme = st.selectbox("Background Theme",
                list(GRADIENT_THEMES.keys()))
            p_overlay = st.slider("Dark Overlay %", 0, 90, 40,
                                  help="Increase for better text readability")
            c1, c2 = st.columns(2)
            with c1:
                p_tc = st.color_picker("Title Color", "#ffffff")
            with c2:
                p_bc = st.color_picker("Body Color", "#e0d4ff")
            p_title_size = st.slider("Title Font Size", 40, 90, 62)
            p_body_size  = st.slider("Body Font Size",  18, 42, 26)

        with st.expander("📁 Upload Assets"):
            p_bg_upload = st.file_uploader("Custom Background Image", type=["png","jpg","jpeg","webp"])
            p_logo_upload = st.file_uploader("Logo / Organization Icon", type=["png","jpg","jpeg","webp"])
            p_caption_for_poster = st.text_area(
                "AI Caption (optional)",
                value=st.session_state.generated_caption,
                height=70,
                placeholder="Paste or generate a caption to embed on poster…"
            )

        gen_poster = st.button("🖼️ Generate Poster", use_container_width=True)

    with col2:
        st.markdown('<div class="preview-wrap"><div class="preview-label">Live Preview</div>', unsafe_allow_html=True)

        if gen_poster or st.session_state.poster_img:
            if gen_poster:
                if not p_title:
                    st.error("Event title is required.")
                else:
                    with st.spinner("Rendering poster…"):
                        bg_img = None
                        if p_bg_upload:
                            bg_img = Image.open(p_bg_upload)
                        else:
                            bg_img = make_gradient_bg(900, 1200, p_theme)

                        logo_img = Image.open(p_logo_upload) if p_logo_upload else None

                        st.session_state.poster_img = create_poster(
                            bg_img, p_title, p_subtitle, p_date, p_venue,
                            p_desc, logo_img, "DejaVu",
                            p_title_size, p_body_size,
                            p_tc, p_bc, p_overlay,
                            p_template, p_caption_for_poster
                        )

            if st.session_state.poster_img:
                st.image(st.session_state.poster_img, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    "📥 Download Poster (PNG)",
                    data=img_to_bytes(st.session_state.poster_img),
                    file_name="poster_creativeai.png",
                    mime="image/png",
                    use_container_width=True,
                )
        else:
            st.markdown("""
            <div style="text-align:center;padding:4rem 1rem;color:#3a3850">
                <div style="font-size:4rem">🖼️</div>
                <div style="margin-top:1rem;font-size:0.9rem">Fill in details and click<br><b style="color:#7828ff">Generate Poster</b></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TAB: MEME GENERATOR
# ═══════════════════════════════════════════════
elif active == "Meme Generator":
    st.markdown('<div class="section-heading">😂 Meme Generator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.1], gap="large")

    with col1:
        with st.expander("🎭 Meme Settings", expanded=True):
            m_template = st.selectbox("Meme Template", list(MEME_TEMPLATES.keys()))
            tmpl_info = MEME_TEMPLATES[m_template]

            m_top = st.text_input(
                f"Top Text ({tmpl_info['top_label'] or 'Top'})",
                placeholder="When the prof says no exam tomorrow…"
            )
            m_bottom = st.text_input(
                f"Bottom Text ({tmpl_info['bottom_label'] or 'Bottom'})",
                placeholder="*stays up till 3AM anyway*"
            )

            # AI autofill
            if st.button("🤖 AI Autofill Texts", use_container_width=True):
                topic_hint = st.session_state.get("meme_topic", "college life")
                key = st.session_state.get("gemini_key", "")
                with st.spinner("AI generating meme texts…"):
                    raw = generate_caption(key, "Meme", topic_hint or m_template, "")
                lines = raw.split("\n")
                for line in lines:
                    if "TOP:" in line.upper():
                        st.session_state["m_top_auto"] = line.split(":", 1)[-1].strip()
                    if "BOTTOM:" in line.upper():
                        st.session_state["m_bot_auto"] = line.split(":", 1)[-1].strip()
                st.rerun()

            if "m_top_auto" in st.session_state and not m_top:
                m_top = st.session_state.m_top_auto
            if "m_bot_auto" in st.session_state and not m_bottom:
                m_bottom = st.session_state.m_bot_auto

            m_topic = st.text_input("Topic for AI Autofill", placeholder="e.g. exam season, placement prep…", key="meme_topic")

        with st.expander("🎨 Meme Style"):
            m_font_size = st.slider("Font Size", 30, 80, 48)
            m_text_color = st.color_picker("Text Color", "#FFFFFF")
            m_bg_theme = st.selectbox("Background Theme", list(GRADIENT_THEMES.keys()), index=4)
            m_bg_upload = st.file_uploader("Custom Background (optional)", type=["png","jpg","jpeg"])

        gen_meme = st.button("😂 Generate Meme", use_container_width=True)

    with col2:
        st.markdown('<div class="preview-wrap"><div class="preview-label">Meme Preview</div>', unsafe_allow_html=True)

        if gen_meme or st.session_state.meme_img:
            if gen_meme:
                if not m_top and not m_bottom:
                    st.error("Enter at least top or bottom text.")
                else:
                    with st.spinner("Creating meme…"):
                        bg = Image.open(m_bg_upload) if m_bg_upload else None
                        st.session_state.meme_img = create_meme(
                            m_template, m_top or "", m_bottom or "",
                            m_font_size, m_text_color, bg, m_bg_theme
                        )

            if st.session_state.meme_img:
                st.image(st.session_state.meme_img, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    "📥 Download Meme (PNG)",
                    data=img_to_bytes(st.session_state.meme_img),
                    file_name="meme_creativeai.png",
                    mime="image/png",
                    use_container_width=True
                )
        else:
            st.markdown("""
            <div style="text-align:center;padding:4rem 1rem;color:#3a3850">
                <div style="font-size:4rem">😂</div>
                <div style="margin-top:1rem;font-size:0.9rem">Enter texts and click<br><b style="color:#7828ff">Generate Meme</b></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Template gallery
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📚 Template Gallery</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (name, info) in enumerate(MEME_TEMPLATES.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:1rem">
                <div style="font-size:2rem">{"😂🤣😏🤔🤯🔥🧠😱"[i]}</div>
                <div style="font-size:0.8rem;font-weight:600;color:#c084fc;margin-top:0.5rem">{name}</div>
                <div style="font-size:0.72rem;color:#5a5870;margin-top:0.3rem">{info['top_label']}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TAB: AI BACKGROUND
# ═══════════════════════════════════════════════
elif active == "AI Background":
    st.markdown('<div class="section-heading">🌌 AI Background Generator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎨 Background Settings</div>', unsafe_allow_html=True)

        bg_theme = st.selectbox("Theme", list(GRADIENT_THEMES.keys()))
        bg_w = st.selectbox("Width", [900, 1080, 1200, 1920], index=0)
        bg_h = st.selectbox("Height", [900, 1080, 1200, 1920], index=0)
        add_noise = st.checkbox("Add Texture Grain", value=True)

        # Preview theme palette
        theme_colors = GRADIENT_THEMES[bg_theme]
        palette_html = "".join(
            f'<div style="width:40px;height:40px;border-radius:8px;background:rgb{tuple(c)};border:1px solid #2a2a40"></div>'
            for c in theme_colors
        )
        st.markdown(f'<div style="display:flex;gap:0.5rem;margin:0.8rem 0">{palette_html}</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Theme color palette preview</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        gen_bg = st.button("🌌 Generate Background", use_container_width=True)

        if gen_bg:
            with st.spinner("Rendering background…"):
                st.session_state.bg_img = make_gradient_bg(bg_w, bg_h, bg_theme, add_noise)

        if st.session_state.bg_img:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                "📥 Download Background (PNG)",
                data=img_to_bytes(st.session_state.bg_img),
                file_name=f"bg_{bg_theme.lower()}.png",
                mime="image/png",
                use_container_width=True
            )
            if st.button("📌 Use as Poster Background", use_container_width=True):
                st.session_state.active_tab = "Poster Creator"
                st.rerun()

    with col2:
        st.markdown('<div class="preview-wrap"><div class="preview-label">Background Preview</div>', unsafe_allow_html=True)
        if st.session_state.bg_img:
            st.image(st.session_state.bg_img, use_container_width=True)
        else:
            # Show a quick preview of all themes as thumbnails
            st.markdown("<div style='display:grid;grid-template-columns:1fr 1fr;gap:0.8rem'>", unsafe_allow_html=True)
            theme_names = list(GRADIENT_THEMES.keys())
            tcols = st.columns(2)
            for i, tn in enumerate(theme_names):
                with tcols[i % 2]:
                    preview = make_gradient_bg(200, 130, tn, False)
                    st.image(preview, caption=tn, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TAB: SETTINGS
# ═══════════════════════════════════════════════
elif active == "Settings":
    st.markdown('<div class="section-heading">⚙️ Settings & Info</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🔑 API Configuration</div>
            <div class="card-sub" style="margin-bottom:1rem">Configure Gemini AI for intelligent caption generation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📋 How to Get Gemini API Key</div>
            <div style="color:#8b8aa0;font-size:0.85rem;line-height:2">
            1. Visit <b style="color:#c084fc">aistudio.google.com</b><br>
            2. Sign in with Google account<br>
            3. Click <b style="color:#c084fc">Get API Key</b><br>
            4. Create new project → Copy key<br>
            5. Paste in the sidebar field<br>
            6. <span class="badge badge-green">Free tier available!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🎯 Caption Styles Explained</div>
            <div style="display:grid;gap:0.6rem;margin-top:0.5rem">
                <div><span class="badge badge-purple">Meme</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">TOP text + BOTTOM text format with humor</span></div>
                <div><span class="badge badge-green">Motivational</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Inspiring quotes to energize students</span></div>
                <div><span class="badge badge-blue">Event Promo</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Exciting event announcements with CTA</span></div>
                <div><span class="badge badge-purple">Educational</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Fun and informative learning content</span></div>
                <div><span class="badge badge-green">Social Media</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Viral captions with trending hashtags</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🖼️ Poster Templates</div>
            <div style="display:grid;gap:0.5rem;margin-top:0.5rem">
                <div><span class="badge badge-purple">Modern Neon</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Glowing edges, corner brackets, vibrant</span></div>
                <div><span class="badge badge-blue">Glassmorphism</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Frosted glass effect, minimal borders</span></div>
                <div><span class="badge badge-green">Bold Minimal</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Clean, high contrast, whitespace focused</span></div>
                <div><span class="badge badge-purple">Retro Burst</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Sunburst lines, vintage event poster feel</span></div>
                <div><span class="badge badge-blue">Circuit Board</span><span style="color:#8b8aa0;font-size:0.82rem;margin-left:0.6rem">Tech-themed with circuit trace overlays</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">⚡ Quick Workflow Guide</div>
            <div style="color:#8b8aa0;font-size:0.85rem;line-height:2.2">
            <b style="color:#c084fc">Step 1</b> → Go to Caption AI, enter your event topic<br>
            <b style="color:#c084fc">Step 2</b> → Choose style, click Generate Caption<br>
            <b style="color:#c084fc">Step 3</b> → Click "Use in Poster Creator"<br>
            <b style="color:#c084fc">Step 4</b> → Fill event details, pick template<br>
            <b style="color:#c084fc">Step 5</b> → Generate & Download! 🎉
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📦 Tech Stack</div>
            <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin-top:0.5rem">
                <span class="badge badge-purple">Python 3.11</span>
                <span class="badge badge-blue">Streamlit</span>
                <span class="badge badge-green">Pillow (PIL)</span>
                <span class="badge badge-purple">Google Gemini AI</span>
                <span class="badge badge-blue">NumPy</span>
                <span class="badge badge-green">google-generativeai</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear All Generated Content", use_container_width=True):
            st.session_state.poster_img = None
            st.session_state.meme_img = None
            st.session_state.bg_img = None
            st.session_state.generated_caption = ""
            st.success("All content cleared!")