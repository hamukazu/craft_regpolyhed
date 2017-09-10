#!/usr/bin/env python
from functools import partial
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import numpy as np

from craftmath import rotation_matrix, margin
from craftdraw import polyline


EDGE_LENGTH = 8 * cm
WITH_MERGIN = True
MARGIN_SIZE = 1 * cm
MARGIN_ANG = np.pi * 28 / 180

ROTMAT = rotation_matrix(np.pi * 120 / 180)


def polygon(v1, v2, n=3):
    v = v2 - v1
    vv = v2 + np.dot(ROTMAT, v)
    return np.c_[v2, vv, v1, v2].T[:n + 1]


margin = partial(margin, MARGIN_ANG, MARGIN_SIZE)


def main():
    # Paper size (A4)
    width = 21.0 * cm
    height = 29.7 * cm

    pdf = canvas.Canvas("./octahedron.pdf")
    pdf.saveState()

    pdf.setAuthor("Kimikazu Kato")
    pdf.setTitle("Regular Octahedron")

    pdf.setPageSize((width, height))
    v1 = np.array([width / 2 + EDGE_LENGTH / 2, height / 2])
    v2 = np.array([width / 2 - EDGE_LENGTH / 2, height / 2])

    # Lower half
    vs = polygon(v1, v2)
    polyline(pdf, vs)
    vs2 = polygon(vs[1, :], vs[0, :], 2)
    polyline(pdf, vs2)
    if WITH_MERGIN:
        mvs = margin(vs2[1, :], vs2[0, :])
        polyline(pdf, mvs)
    vs2 = polygon(vs2[2, :], vs2[1, :], 2)
    polyline(pdf, vs2)
    if WITH_MERGIN:
        mvs = margin(vs2[1, :], vs2[0, :])
        polyline(pdf, mvs)
        mvs = margin(vs2[2, :], vs2[1, :])
        polyline(pdf, mvs)
    vs2 = polygon(vs[2, :], vs[1, :], 2)
    polyline(pdf, vs2)
    if WITH_MERGIN:
        mvs = margin(vs2[2, :], vs2[1, :])
        polyline(pdf, mvs)

    # Upper half
    vs = polygon(v2, v1)
    polyline(pdf, vs)
    vs2 = polygon(vs[1, :], vs[0, :], 2)
    polyline(pdf, vs2)
    vs2 = polygon(vs2[2, :], vs2[1, :], 2)
    polyline(pdf, vs2)
    vs2 = polygon(vs[2, :], vs[1, :], 2)
    polyline(pdf, vs2)
    if WITH_MERGIN:
        mvs = margin(vs2[1, :], vs2[0, :])
        polyline(pdf, mvs)

    pdf.saveState()
    pdf.save()

if __name__ == '__main__':
    main()
