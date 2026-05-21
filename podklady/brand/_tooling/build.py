"""Build LIFO brand raster assets from path coordinates.

Generates PNG/WebP exports, favicon ICO + multi-size icons, and Open Graph image.
Pure Pillow rendering — no Cairo / external SVG renderer required.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# ---------- Configuration ----------
BRAND_DIR = Path(__file__).resolve().parent.parent  # podklady/brand/
RASTER_PNG = BRAND_DIR / "03_raster" / "png"
RASTER_WEBP = BRAND_DIR / "03_raster" / "webp"
WEB_ASSETS = BRAND_DIR / "04_web_assets"

# LIFO symbol path coordinates in 512x512 viewBox
CANVAS = 512
UPPER_L = [(50, 50), (120, 50), (120, 260), (270, 260), (270, 330), (50, 330)]
LOWER_L = [(462, 462), (392, 462), (392, 252), (242, 252), (242, 182), (462, 182)]

# Brand colors (working defaults)
MAGENTA = (214, 48, 122)   # #D6307A
TEAL = (54, 162, 168)      # #36A2A8
INK = (10, 10, 10)         # #0A0A0A
PAPER = (255, 255, 255)    # #FFFFFF
NAVY = (12, 18, 35)        # dark background (OG image)

# ---------- Helpers ----------

def scale_poly(points, size):
    s = size / CANVAS
    return [(x * s, y * s) for x, y in points]


def make_diagonal_gradient(width, height, c_start, c_end):
    """Generate a diagonal gradient from top-left (c_start) to bottom-right (c_end)."""
    # Render at modest size, scale up for performance — gradient is smooth so scaling is fine
    gen_w = min(width, 1024)
    gen_h = min(height, 1024)
    mask = Image.new("L", (gen_w, gen_h))
    mp = mask.load()
    norm = gen_w + gen_h - 2
    for y in range(gen_h):
        for x in range(gen_w):
            mp[x, y] = int(255 * (x + y) / max(norm, 1))
    layer1 = Image.new("RGB", (gen_w, gen_h), c_start)
    layer2 = Image.new("RGB", (gen_w, gen_h), c_end)
    grad = Image.composite(layer2, layer1, mask)
    if (gen_w, gen_h) != (width, height):
        grad = grad.resize((width, height), Image.LANCZOS)
    return grad.convert("RGBA")


def render_logo(size, mode="gradient", supersample=4):
    """Render LIFO logo at given size. mode: gradient/black/white/outline-black/outline-white."""
    ss = supersample if size <= 512 else 2
    big = size * ss
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))

    if mode == "gradient":
        mask = Image.new("L", (big, big), 0)
        md = ImageDraw.Draw(mask)
        md.polygon(scale_poly(UPPER_L, big), fill=255)
        md.polygon(scale_poly(LOWER_L, big), fill=255)
        grad = make_diagonal_gradient(big, big, MAGENTA, TEAL)
        img.paste(grad, (0, 0), mask)
    elif mode in ("black", "white"):
        fill = INK if mode == "black" else PAPER
        d = ImageDraw.Draw(img)
        d.polygon(scale_poly(UPPER_L, big), fill=fill + (255,))
        d.polygon(scale_poly(LOWER_L, big), fill=fill + (255,))
    elif mode in ("outline-black", "outline-white"):
        stroke = INK if mode == "outline-black" else PAPER
        d = ImageDraw.Draw(img)
        sw = max(2, big // 128)
        d.polygon(scale_poly(UPPER_L, big), outline=stroke + (255,), width=sw)
        d.polygon(scale_poly(LOWER_L, big), outline=stroke + (255,), width=sw)

    if ss > 1:
        img = img.resize((size, size), Image.LANCZOS)
    return img


def find_bold_font(size):
    paths = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
        r"C:\Windows\Fonts\Inter-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def find_regular_font(size):
    paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make_og_image(width, height, lang="sk"):
    """Compose Open Graph image: navy bg + LIFO logo + wordmark + date/venue subtitle."""
    bg = Image.new("RGB", (width, height), NAVY)
    # Subtle radial-ish glow from top-left (magenta tinted)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gp = glow.load()
    for y in range(height):
        for x in range(width):
            d = ((x / width) + (y / height)) * 0.5
            alpha = int(60 * max(0, 1 - d * 1.5))
            gp[x, y] = (MAGENTA[0], MAGENTA[1], MAGENTA[2], alpha)
    bg.paste(glow, (0, 0), glow)

    # Logo on the left
    logo_size = height - 180
    logo = render_logo(logo_size, "gradient", supersample=2)
    logo_x = 70
    logo_y = (height - logo_size) // 2
    bg.paste(logo, (logo_x, logo_y), logo)

    # Text on the right
    text_x = logo_x + logo_size + 60

    f_big = find_bold_font(150)
    f_med = find_regular_font(42)
    f_small = find_bold_font(30)

    draw = ImageDraw.Draw(bg)

    if lang == "sk":
        date_venue = "11. 2. 2027   ·   Hotel Clarion Bratislava"
    else:
        date_venue = "Feb 11, 2027   ·   Hotel Clarion Bratislava"

    wordmark = "LIFO"
    subtitle = "Local Innovation Forum"

    y0 = height // 2 - 170
    draw.text((text_x, y0), wordmark, fill=PAPER, font=f_big)
    y0 += 170
    draw.text((text_x, y0), subtitle, fill=(190, 190, 200), font=f_med)
    y0 += 70
    draw.text((text_x, y0), date_venue, fill=MAGENTA, font=f_small)

    return bg


# ---------- Build ----------

print("Generating PNG + WebP exports...")
sizes = [256, 512, 1024, 2048]
modes = ["gradient", "black", "white"]
for mode in modes:
    for size in sizes:
        img = render_logo(size, mode=mode)
        png_out = RASTER_PNG / f"lifo-logo-{mode}-{size}.png"
        webp_out = RASTER_WEBP / f"lifo-logo-{mode}-{size}.webp"
        img.save(png_out, "PNG", optimize=True)
        img.save(webp_out, "WEBP", quality=92, lossless=True)
        print(f"  {png_out.name}, {webp_out.name}")

print("\nGenerating favicon set...")
# Favicon ICO with multiple sizes embedded
fav_base = render_logo(48, "gradient", supersample=8)
fav_base.save(WEB_ASSETS / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print("  favicon.ico (16/32/48)")

render_logo(16, "gradient", supersample=8).save(WEB_ASSETS / "favicon-16.png")
render_logo(32, "gradient", supersample=8).save(WEB_ASSETS / "favicon-32.png")
render_logo(180, "gradient", supersample=4).save(WEB_ASSETS / "apple-touch-icon-180.png")
render_logo(192, "gradient", supersample=4).save(WEB_ASSETS / "android-chrome-192.png")
render_logo(512, "gradient", supersample=2).save(WEB_ASSETS / "android-chrome-512.png")
print("  favicon-16.png, favicon-32.png, apple-touch-icon-180.png, android-chrome-192.png, android-chrome-512.png")

print("\nGenerating Open Graph + Twitter card...")
make_og_image(1200, 630, "sk").save(WEB_ASSETS / "og-image-1200x630.png", "PNG", optimize=True)
make_og_image(1200, 630, "en").save(WEB_ASSETS / "og-image-1200x630-en.png", "PNG", optimize=True)
make_og_image(1200, 600, "sk").save(WEB_ASSETS / "twitter-card-1200x600.png", "PNG", optimize=True)
print("  og-image-1200x630.png, og-image-1200x630-en.png, twitter-card-1200x600.png")

print("\nAll done.")
