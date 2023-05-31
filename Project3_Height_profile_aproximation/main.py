import pandas as pd
import matplotlib.pyplot as plt
from Basic import *
from Lagrange import Lagrange
from Spline import Spline

if __name__ == '__main__':
    files_names = ["WielkiKanionKolorado", "MountEverest", "Obiadek", "SpacerniakGdansk", "Hel_yeah"]
    for file in files_names:
        data, distances, heights = read_csv_data(file)
        draw_rout(distances, heights, file)
        # steps = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        steps = [5, 10, 15, 50, 100, 200]
        # steps = [100, 200]
        for step in steps:
            lagrange = Lagrange(data)
            result, nodes = lagrange.lagrange_interpolation(step)
            draw_chart(result, nodes, data, 'Lagrange', file)

        for step in steps:
            spline = Spline(data)
            result, nodes = spline.spline_interpolation(step)
            draw_chart(result, nodes, data, 'Spline', file)
