#!/usr/bin/env python
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import numpy as np

from craftmath import rotation_matrix
from craftdraw import polyline

EDGE_LENGTH = 5 * cm
WITH_MERGIN = True
MARGIN_SIZE = 1 * cm
MARGIN_ANG = np.pi * 28 / 180


ROTMAT = rotation_matrix(np.pi * 120 / 180)


def hat(v1, v2):
    v = v2 - v1
    vv = v2 + np.dot(ROTMAT, v)
    return np.c_[v2, vv, v1].T


def margin(v1, v2):
    vv = v2 - v1
    vv = vv / np.sqrt((vv**2).sum())
    edgelen = MARGIN_SIZE / np.sin(MARGIN_ANG)
    v3 = v1 + edgelen * np.dot(rotation_matrix(MARGIN_ANG), vv)
    v4 = v2 - edgelen * np.dot(rotation_matrix(-MARGIN_ANG), vv)
    return np.c_[v2, v4, v3, v1].T


def main():
    # Paper size (A4)
    width = 21.0 * cm
    height = 29.7 * cm

    pdf = canvas.Canvas("./icosahedron.pdf")
    pdf.saveState()

    pdf.setAuthor("Kimikazu Kato")
    pdf.setTitle("Regular Octahedron")

    # length of edge
    pdf.setPageSize((width, height))
    v = np.array([width / 2, EDGE_LENGTH / 2])
    v1 = np.array([v[0] - EDGE_LENGTH * np.sqrt(3) / 4,
                   v[1] + EDGE_LENGTH / 4])
    v2 = np.array([v[0] + EDGE_LENGTH * np.sqrt(3) / 4,
                   v[1] - EDGE_LENGTH / 4])

    if WITH_MERGIN:
        mvs = margin(v2, v1)
        polyline(pdf, mvs)

    vs1 = v1.copy()
    vs2 = v2.copy()
    vv = np.array([0, EDGE_LENGTH])
    for i in range(1, 6):
        vs1 = np.c_[vs1, v1 + vv * i]
    vs1 = vs1.T
    polyline(pdf, vs1)
    for i in range(1, 6):
        vs2 = np.c_[vs2, v2 + vv * i]
    vs2 = vs2.T
    polyline(pdf, vs2)
    vs = np.c_[v2.copy(), v1.copy()]
    for i in range(1, 6):
        vs = np.c_[vs, vs2[i, :], vs1[i, :]]
    vs = vs.T
    polyline(pdf, vs)

    for i in range(5):
        vs = hat(vs1[i, :], vs1[i + 1, :])
        polyline(pdf, vs)
        if WITH_MERGIN:
            if i != 0:
                mvs = margin(vs[2, :], vs[1, :])
                polyline(pdf, mvs)
            if i == 4:
                mvs = margin(vs[1, :], vs[0, :])
                polyline(pdf, mvs)

    for i in range(5):
        vs = hat(vs2[i + 1, :], vs2[i, :])
        polyline(pdf, vs)
        if WITH_MERGIN:
            if i != 0:
                mvs = margin(vs[1, :], vs[0, :])
                polyline(pdf, mvs)
            if i == 4:
                mvs = margin(vs[2, :], vs[1, :])
                polyline(pdf, mvs)

    pdf.saveState()
    pdf.save()

if __name__ == '__main__':
    main()
