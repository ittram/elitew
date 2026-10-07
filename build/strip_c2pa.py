# -*- coding: utf-8 -*-
"""Removes everything but the picture from webp files: the C2PA chunk the
sandbox transfer adds, and any EXIF or XMP (phone photos carry location).

    python3 build/strip_c2pa.py assets/class-hyrox.webp assets/class-hyrox-600.webp

Run it on the Mac, after the files are copied back and before committing."""
import struct, sys

KEEP = (b'VP8 ', b'VP8L', b'VP8X', b'ALPH', b'ANIM', b'ANMF')

for path in sys.argv[1:]:
    d = open(path, 'rb').read()
    if d[:4] != b'RIFF' or d[8:12] != b'WEBP':
        print(path, 'is not a webp, left alone'); continue
    i, kept, seen = 12, [], []
    while i + 8 <= len(d):
        cid = d[i:i + 4]; n = struct.unpack('<I', d[i + 4:i + 8])[0]
        chunk = d[i:i + 8 + n + (n & 1)]; seen.append(cid.decode('latin1').strip())
        if cid == b'VP8X':      # clear the EXIF and XMP flags along with the chunks
            chunk = chunk[:8] + bytes([chunk[8] & ~0x0C]) + chunk[9:]
        if cid in KEEP: kept.append(chunk)
        i += 8 + n + (n & 1)
    body = b'WEBP' + b''.join(kept)
    out = b'RIFF' + struct.pack('<I', len(body)) + body
    open(path, 'wb').write(out)
    print(path, ' '.join(seen), len(d), '->', len(out), 'bytes')
