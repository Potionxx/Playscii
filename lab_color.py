# L*a*b color space conversion
# from EDSCII

import math


def _srgb_channel_to_linear(c):
    c /= 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4

def rgb_to_xyz(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    if r > 0.04045:
        r = ((r + 0.055) / 1.055)**2.4
    else:
        r /= 12.92
    if g > 0.04045:
        g = ((g + 0.055) / 1.055)**2.4
    else:
        g /= 12.92
    if b > 0.04045:
        b = ((b + 0.055) / 1.055)**2.4
    else:
        b /= 12.92
    r *= 100
    g *= 100
    b *= 100
    # observer: 2deg, illuminant: D65
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    return x, y, z

def xyz_to_lab(x, y, z):
    # observer: 2deg, illuminant: D65
    x /= 95.047
    y /= 100.0
    z /= 108.883
    if x > 0.008856:
        x = x**(1.0/3)
    else:
        x = (7.787 * x) + (16.0 / 116)
    if y > 0.008856:
        y = y**(1.0/3)
    else:
        y = (7.787 * y) + (16.0 / 116)
    if z > 0.008856:
        z = z**(1.0/3)
    else:
        z = (7.787 * z) + (16.0 / 116)
    l = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)
    return l, a, b

def rgb_to_lab(r, g, b):
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)

def lab_color_diff(l1, a1, b1, l2, a2, b2):
    "quick n' dirty CIE 1976 color delta"
    dl = (l1 - l2)**2
    da = (a1 - a2)**2
    db = (b1 - b2)**2
    return math.sqrt(dl + da + db)


def rgb_to_oklab(r, g, b):
    # Oklab conversion from linear sRGB (D65).
    r = _srgb_channel_to_linear(r)
    g = _srgb_channel_to_linear(g)
    b = _srgb_channel_to_linear(b)

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = l ** (1.0 / 3.0)
    m_ = m ** (1.0 / 3.0)
    s_ = s ** (1.0 / 3.0)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b


def oklab_color_diff(l1, a1, b1, l2, a2, b2):
    dl = (l1 - l2) ** 2
    da = (a1 - a2) ** 2
    db = (b1 - b2) ** 2
    return math.sqrt(dl + da + db)
