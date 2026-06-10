"""Rebuild favicon + OG image from real grafička SVG (purple version).

Uses svglib + reportlab for SVG → PIL conversion (no Cairo dependency).
"""

from io import BytesIO
from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

REPO = Path(__file__).resolve().parent.parent.parent.parent
PUBLIC = REPO / "public"

# Source SVG files (real grafička exports)
SRC_PIKTOGRAM = REPO / "public" / "logos" / "lifo-logo-piktogram.svg"
SRC_WHITE_PIKTOGRAM = REPO / "public" / "logos" / "lifo-logo-white-piktogram.svg"
SRC_GRADIENT = REPO / "public" / "logos" / "lifo-logo-gradient.svg"

# New brand colors
PURPLE = (111, 84, 209)      # #6F54D1
TEAL = (54, 162, 168)        # #36A2A8
PAPER = (255, 255, 255)
NAVY = (12, 18, 35)


def render_svg_to_png(svg_path: Path, size: int, recolor_to: tuple = None) -> Image.Image:
    """Render an SVG file to a PIL Image at given square size.

    svglib's renderPM doesn't preserve transparent background. We work around it
    by rendering, then chroma-keying out near-white pixels (the bg) to alpha=0.

    If `recolor_to` (R,G,B) is given, the remaining (path) pixels get recolored.
    """
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise RuntimeError(f"Could not load SVG: {svg_path}")
    sw, sh = drawing.width, drawing.height
    scale = size / max(sw, sh)
    drawing.scale(scale, scale)
    drawing.width = sw * scale
    drawing.height = sh * scale
    buf = BytesIO()
    renderPM.drawToFile(drawing, buf, fmt="PNG")
    buf.seek(0)
    img = Image.open(buf).convert("RGBA")

    # Chroma-key: pixels close to white become transparent; rest stays opaque.
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # Distance from white
            white_dist = max(255 - r, 255 - g, 255 - b)
            if white_dist < 30:  # near-white = background
                pixels[x, y] = (0, 0, 0, 0)
            else:
                # Non-white = path
                if recolor_to is not None:
                    # Preserve alpha intensity (anti-aliased edges) by mapping
                    # darkness to alpha relative to bg distance.
                    alpha = min(255, int(white_dist * 8.5))
                    pixels[x, y] = (recolor_to[0], recolor_to[1], recolor_to[2], alpha)

    # Center on square canvas if not square
    if img.size != (size, size):
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        x = (size - img.width) // 2
        y = (size - img.height) // 2
        canvas.paste(img, (x, y), img)
        img = canvas
    return img


def find_bold_font(size: int):
    paths = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def find_regular_font(size: int):
    paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make_og_image(width: int, height: int, lang: str = "sk") -> Image.Image:
    """Compose OG image: navy bg + LIFO logo + wordmark + date subtitle."""
    bg = Image.new("RGB", (width, height), NAVY)

    # Subtle purple glow from top-left
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gp = glow.load()
    for y in range(height):
        for x in range(width):
            d = ((x / width) + (y / height)) * 0.5
            alpha = int(60 * max(0, 1 - d * 1.5))
            gp[x, y] = (PURPLE[0], PURPLE[1], PURPLE[2], alpha)
    bg.paste(glow, (0, 0), glow)

    # Logo on dark bg — render PURPLE piktogram + recolor to white
    logo_size = height - 200
    logo = render_svg_to_png(SRC_PIKTOGRAM, logo_size, recolor_to=PAPER)
    logo_x = 80
    logo_y = (height - logo_size) // 2
    bg.paste(logo, (logo_x, logo_y), logo)

    # Text on the right
    text_x = logo_x + logo_size + 60

    f_big = find_bold_font(150)
    f_med = find_regular_font(42)
    f_small = find_bold_font(30)

    draw = ImageDraw.Draw(bg)

    if lang == "sk":
        date_venue = "11. 2. 2027   ·   Bratislava"
    else:
        date_venue = "Feb 11, 2027   ·   Bratislava"

    wordmark = "LIFO"
    subtitle = "Local Innovation Forum"

    y0 = height // 2 - 170
    draw.text((text_x, y0), wordmark, fill=PAPER, font=f_big)
    y0 += 170
    draw.text((text_x, y0), subtitle, fill=(200, 200, 210), font=f_med)
    y0 += 70
    draw.text((text_x, y0), date_venue, fill=PURPLE, font=f_small)

    return bg


# Render at large size then downscale for sharpness
print("Rendering favicon sources from grafička SVG...")
fav_base = render_svg_to_png(SRC_PIKTOGRAM, 512)

print("Saving favicon set...")
fav_16 = fav_base.resize((16, 16), Image.LANCZOS)
fav_32 = fav_base.resize((32, 32), Image.LANCZOS)
fav_48 = fav_base.resize((48, 48), Image.LANCZOS)
fav_180 = fav_base.resize((180, 180), Image.LANCZOS)
fav_192 = fav_base.resize((192, 192), Image.LANCZOS)
fav_512 = fav_base  # already 512

fav_48.save(PUBLIC / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
fav_16.save(PUBLIC / "favicon-16.png", "PNG", optimize=True)
fav_32.save(PUBLIC / "favicon-32.png", "PNG", optimize=True)
fav_180.save(PUBLIC / "apple-touch-icon-180.png", "PNG", optimize=True)
fav_192.save(PUBLIC / "android-chrome-192.png", "PNG", optimize=True)
fav_512.save(PUBLIC / "android-chrome-512.png", "PNG", optimize=True)
print("  favicon.ico, favicon-16/32, apple-touch-icon-180, android-chrome-192/512")

print("Generating Open Graph + Twitter card...")
og_sk = make_og_image(1200, 630, "sk")
og_sk.save(PUBLIC / "og-image-1200x630.png", "PNG", optimize=True)
og_en = make_og_image(1200, 630, "en")
og_en.save(PUBLIC / "og-image-1200x630-en.png", "PNG", optimize=True)
tw_sk = make_og_image(1200, 600, "sk")
tw_sk.save(PUBLIC / "twitter-card-1200x600.png", "PNG", optimize=True)
print("  og-image-1200x630.png (SK + EN), twitter-card-1200x600.png")

print("\nDone — favicon and OG image regenerated with new purple branding.")
