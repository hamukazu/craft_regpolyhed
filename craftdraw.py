def polyline(pdf, vs):
    for i in range(len(vs) - 1):
        pdf.line(vs[i, 0], vs[i, 1], vs[i + 1, 0], vs[i + 1, 1])
