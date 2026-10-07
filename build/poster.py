# -*- coding: utf-8 -*-
"""Turns a phone photo of the printed timetable into a flat, clean poster.

    python3 build/poster.py PHOTO [OUT]          # OUT defaults to assets/timetable.webp

Finds the sheet of paper (the biggest bright four-cornered shape), squares it
up to A4 landscape, trims the paper border, makes the paper white again and
writes webp at quality 82 with no metadata. Colour, not black and white: it
is a document, not a photo. A digital poster file is always better; use this
only when a photo of the print is all there is.

Runs in the cloud sandbox (pip install --break-system-packages opencv-python-headless pillow numpy).
Copy the result back and run build/strip_c2pa.py on it on the Mac."""
import sys
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps


def corners(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, t = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    t = cv2.morphologyEx(t, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cs, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    q = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True).reshape(-1, 2).astype(np.float32)
    if len(q) != 4:
        sys.exit('Could not find the four corners of the sheet (found %d). Photograph it flat on a darker surface.' % len(q))
    s, d = q.sum(1), np.diff(q, axis=1).ravel()
    return np.float32([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]])  # tl, tr, br, bl


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'assets/timetable.webp'
    pil = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    img = cv2.cvtColor(np.asarray(pil), cv2.COLOR_RGB2BGR)
    tl, tr, br, bl = q = corners(img)
    width = max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))
    W = int(round(min(1600, width * 1.4))); H = int(round(W / 1.414))       # A4 landscape
    M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [W, 0], [W, H], [0, H]]))
    flat = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_CUBIC).astype(np.float32)
    m = int(round(W * 0.0155))                                                 # the paper border
    flat = flat[m:H - m, m:W - m]
    for ch in range(3):                                                        # the paper reads white again
        flat[..., ch] *= 248 / max(np.percentile(flat[..., ch], 80), 1)
    flat = np.clip(flat, 0, 255).astype(np.uint8)
    im = Image.fromarray(cv2.cvtColor(flat, cv2.COLOR_BGR2RGB)).filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=2))
    im.save(out, 'WEBP', quality=82, method=6)
    print(out, im.size)


if __name__ == '__main__':
    main()
