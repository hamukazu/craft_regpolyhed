#!/usr/bin/env python
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import numpy as np

from craftdraw import polyline


EDGE_LENGTH = 8 * cm
WITH_MERGIN = True
MARGIN_SIZE = 1 * cm
MARGIN_ANG = np.pi * 28 / 180


def get_rotmat(a):
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a), np.cos(a)]])

ROTMAT = get_rotmat(np.pi * 120 / 180)


def polygon(v1, v2, n=3):
    v = v2 - v1
    vv = v2 + np.dot(ROTMAT, v)
    return np.c_[v2, vv, v1, v2].T[:n + 1]


def margin(v1, v2):
    vv = v2 - v1
    vv = vv / np.sqrt((vv**2).sum())
    edgelen = MARGIN_SIZE / np.sin(MARGIN_ANG)
    v3 = v1 + edgelen * np.dot(get_rotmat(MARGIN_ANG), vv)
    v4 = v2 - edgelen * np.dot(get_rotmat(-MARGIN_ANG), vv)
    return np.c_[v2, v4, v3, v1].T


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
