import numpy as np


def rotation_matrix(a):
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a), np.cos(a)]])


def margin(angle, size, v1, v2):
    vv = v2 - v1
    vv = vv / np.sqrt((vv**2).sum())
    edgelen = size / np.sin(angle)
    v3 = v1 + edgelen * np.dot(rotation_matrix(angle), vv)
    v4 = v2 - edgelen * np.dot(rotation_matrix(-angle), vv)
    return np.c_[v2, v4, v3, v1].T


def regular_polygon(n, v1, v2):
    ang = 2 * np.pi / n
    mat = rotation_matrix(ang)
    vs = np.c_[v1, v2]
    vv = v2 - v1
    vprev = v2
    for i in range(n - 2):
        v = np.dot(mat, vv) + vprev
        vs = np.c_[vs, v]
        vv = v - vprev
        vprev = v
    return vs.T
