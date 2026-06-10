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
SRC_GRADIENT_PIKTOGRAM = REPO / "public" / "logos" / "lifo-logo-gradient-piktogram.svg"

# New brand colors
PURPLE = (111, 84, 209)      # #6F54D1
TEAL = (54, 162, 168)        # #36A2A8
PAPER = (255, 255, 255)
NAVY = (12, 18, 35)

# Gradient stops (matching grafička's SVG gradient)
GRAD_PINK = (235, 0, 139)    # #eb008b at ~14%
GRAD_TEAL = (39, 139, 179)   # #278bb3 at 70%
GRAD_CYAN = (89, 197, 199)   # #59c5c7 at 100%


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


def make_brand_gradient(size: int) -> Image.Image:
    """Create the LIFO brand gradient matching the SVG definition exactly.

    SVG defines gradient from (419.05, 720.59) → (660.95, 301.62) in viewBox 1080.
    Stops: 0.14 = pink, 0.70 = teal, 1.00 = cyan.
    """
    img = Image.new("RGB", (size, size))
    pixels = img.load()

    # Gradient line in viewBox coordinates → normalized to [0,1]
    sx, sy = 419.05 / 1080.0, 720.59 / 1080.0
    ex, ey = 660.95 / 1080.0, 301.62 / 1080.0
    dx, dy = ex - sx, ey - sy
    length_sq = dx * dx + dy * dy

    def interp(c1, c2, u):
        return (
            int(c1[0] * (1 - u) + c2[0] * u),
            int(c1[1] * (1 - u) + c2[1] * u),
            int(c1[2] * (1 - u) + c2[2] * u),
        )

    for y in range(size):
        for x in range(size):
            nx, ny = x / size, y / size
            vx, vy = nx - sx, ny - sy
            t = (vx * dx + vy * dy) / length_sq
            t = max(0.0, min(1.0, t))
            # Apply stops: 0.14 = pink, 0.70 = teal, 1.00 = cyan
            if t <= 0.14:
                rgb = GRAD_PINK
            elif t < 0.70:
                u = (t - 0.14) / (0.70 - 0.14)
                rgb = interp(GRAD_PINK, GRAD_TEAL, u)
            else:
                u = (t - 0.70) / (1.0 - 0.70)
                rgb = interp(GRAD_TEAL, GRAD_CYAN, u)
            pixels[x, y] = rgb
    return img


def render_gradient_logo(size: int) -> Image.Image:
    """Render gradient piktogram: mono shape from SVG + brand gradient fill."""
    # 1) Render mono purple piktogram → use as mask
    mono = render_svg_to_png(SRC_PIKTOGRAM, size)
    mask = mono.split()[3]  # alpha channel = logo mask
    # 2) Create gradient
    grad = make_brand_gradient(size).convert("RGBA")
    # 3) Apply mask to gradient
    grad.putalpha(mask)
    return grad


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

    # Logo on dark bg — gradient piktogram via mask + brand gradient
    logo_size = height - 200
    logo = render_gradient_logo(logo_size)
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
print("Rendering favicon with brand gradient...")
fav_base = render_gradient_logo(512)

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
