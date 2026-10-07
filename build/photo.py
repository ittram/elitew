# -*- coding: utf-8 -*-
"""The house look for training photos, in one command.

    python3 build/photo.py SOURCE NAME [--kind card|hero] [--top N] [--focus X Y]

    python3 build/photo.py ~/Downloads/hyrox.jpg class-hyrox
    → assets/class-hyrox.webp (900 wide) and assets/class-hyrox-600.webp

What it does, in order (this is the look of the TRX card in 2.4.8):
  1. Black and white from the luminance, levels stretched (0.3% / 0.5% clip),
     mids a touch darker (gamma 1.08), contrast +8%, a light unsharp mask.
  2. Cuts out the people and the equipment they hold (rembg: u2net_human_seg
     for bodies, isnet-general-use for straps, bars and the like; the two
     masks combined) and blurs everything else with a round lens kernel:
     strongest on the far wall at the top of the frame, lighter on the floor
     near the bottom. The subject goes back on top with a soft edge.
  3. Crops. card: 3:4 portrait, the class card on desktop and in the phone
     carousel. hero: 4:3 landscape. The crop leaves 14% of the frame above
     the top of the person; --top N sets the crop's top edge in source pixels
     instead.
  4. A light vignette centred a little right of and above the middle
     (--focus 0.58 0.42), so the eye lands on the person, not the wall.
  5. Writes webp at quality 80 with no metadata: card 900 and 600 wide, hero
     1600 and 800 wide (never wider than the source).

Runs in the cloud sandbox, which has the network for the first model
download (about 350 MB, once):
    pip install --break-system-packages "rembg[cpu]" opencv-python-headless pillow numpy
Files copied back to the Mac pick up a C2PA chunk: run build/strip_c2pa.py on
them there before committing.
"""
import argparse, math, os, sys
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageChops


def grade(rgb):
    g = ImageOps.autocontrast(rgb.convert('L'), cutoff=(0.3, 0.5))
    g = g.point(lambda v: int(255 * ((v / 255) ** 1.08)))
    g = ImageEnhance.Contrast(g).enhance(1.08)
    return g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))


def subject_masks(rgb):
    from rembg import remove, new_session
    body = remove(rgb, session=new_session('u2net_human_seg'), only_mask=True)
    kit = remove(rgb, session=new_session('isnet-general-use'), only_mask=True)
    f = lambda m: np.asarray(m).astype(np.float32) / 255
    return f(body), np.maximum(f(body), f(kit))


def lens_blur(gray, mask):
    import cv2
    g = np.asarray(gray).astype(np.float32) / 255
    soft = cv2.GaussianBlur(mask, (0, 0), 1.5)
    bg = 1 - cv2.dilate((soft > 0.5).astype(np.float32), np.ones((9, 9), np.uint8))
    H, W = g.shape
    s = W / 900.0                       # the radii below were set on a 900 wide photo

    def disc(r):
        r = max(1, int(round(r * s)))
        k = np.zeros((2 * r + 1, 2 * r + 1), np.float32)
        cv2.circle(k, (r, r), r, 1, -1)
        return k / k.sum()

    # blur only from background pixels, so the person never bleeds into a halo
    layers = []
    for r in (5, 9, 13):
        k = disc(r)
        layers.append(cv2.filter2D(g * bg, -1, k) / np.maximum(cv2.filter2D(bg, -1, k), 1e-4))
    y = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    top = np.clip((0.55 - y) / 0.25, 0, 1)          # far wall: most blur
    bottom = np.clip((y - 0.75) / 0.15, 0, 1)        # floor in front: least
    mid = np.clip(1 - top - bottom, 0, 1)
    blur = layers[2] * top + layers[1] * mid + layers[0] * bottom
    out = blur * (1 - soft) + g * soft
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))


def crop(img, person, kind, top):
    W, H = img.size
    ratio = 3 / 4 if kind == 'card' else 4 / 3       # width / height
    cw, ch = (W, int(round(W / ratio))) if W / H < ratio else (int(round(H * ratio)), H)
    if top is None:
        rows = np.where(person.max(1) > 0.5)[0]
        top = (rows.min() if len(rows) else 0) - 0.14 * ch
    top = int(min(max(0, top), H - ch))
    cols = np.where(person.max(0) > 0.5)[0]
    cx = (cols.min() + cols.max()) / 2 if len(cols) else W / 2
    left = int(min(max(0, cx - cw / 2), W - cw)) if cw < W else 0
    return img.crop((left, top, left + cw, top + ch))


def vignette(img, fx, fy):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot((xx - w * fx) / (w * 0.75), (yy - h * fy) / (h * 0.7))
    v = np.maximum(0.72, 1 - 0.32 * np.maximum(0, d - 0.35))
    v = Image.fromarray((v * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40 * w / 900))
    return ImageChops.multiply(img, v)


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('source'); p.add_argument('name', help='e.g. class-hyrox, named after what it shows')
    p.add_argument('--kind', choices=['card', 'hero'], default='card')
    p.add_argument('--top', type=int, help='crop top edge in source pixels (default: 14%% headroom above the person)')
    p.add_argument('--focus', type=float, nargs=2, default=(0.58, 0.42), metavar=('X', 'Y'))
    p.add_argument('--out', default='assets')
    a = p.parse_args()

    rgb = Image.open(a.source)
    rgb = ImageOps.exif_transpose(rgb).convert('RGB')    # phone photos are often stored sideways
    person, subject = subject_masks(rgb)
    img = lens_blur(grade(rgb), subject)
    img = vignette(crop(img, person, a.kind, a.top), *a.focus)

    sizes = (900, 600) if a.kind == 'card' else (1600, 800)
    os.makedirs(a.out, exist_ok=True)
    for i, w in enumerate(sizes):
        w = min(w, img.width)
        out = img if w == img.width else img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
        path = os.path.join(a.out, a.name + ('' if i == 0 else '-%d' % sizes[1]) + '.webp')
        out.save(path, 'WEBP', quality=80, method=6)       # Pillow writes no EXIF unless asked
        print(path, out.size, os.path.getsize(path), 'bytes')


if __name__ == '__main__':
    main()
