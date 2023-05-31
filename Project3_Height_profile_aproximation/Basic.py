import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_csv_data(file_name):
    path = './Data/' + file_name + '.csv'
    new_headers = ['Distance', 'Height']
    data = pd.read_csv(path)
    headers = list(data.columns)
    if type(headers[1]) is float:
        data = pd.read_csv(path, header=None, names=new_headers)
    else:
        data = pd.read_csv(path, skiprows=1, names=new_headers)
    dist = data["Distance"].to_numpy()
    h = data["Height"].to_numpy()
    data_arr = []
    for i in range(len(h)):
        data_arr.append((i, float(h[i])))
    # print(data_arr)
    return data_arr, dist, h


def get_x(data):
    return [x[0] for x in data]


def get_height(data):
    return [height[1] for height in data]


def draw_rout(distances, heights, rout_name):
    plt.plot(distances, heights, label=f'Rout: {rout_name}')
    plt.ylim(ymin=0)
    plt.xlabel('Distance [m]')
    plt.ylabel('Height [m]')
    plt.legend()
    plt.title(f'{rout_name}')
    chart = f'./Result/\\{rout_name}.png'
    plt.savefig(chart)
    plt.close()


def draw_chart(interpolation_data, nodes, data, method, file):
    data = data[0:nodes[-1][0] + 1]
    x, height = get_x(data), get_height(data)
    x_interpolation, height_interpolation = get_x(interpolation_data), get_height(interpolation_data)
    x_calc, y_calc = get_x(nodes), get_height(nodes)

    plt.plot(x, height, '.', markersize=1, label='interpolated function')
    plt.plot(x_interpolation, height_interpolation, label='interpolating function')
    plt.plot(x_calc, y_calc, 'o', markersize=3, label='interpolated nodes')
    plt.yscale('log')
    # plt.ylim(ymin=min(height)-1)
    plt.xlabel('N')
    plt.ylabel('Height [m]')
    plt.legend()

    plt.title(f'{method} - {str(len(nodes))} nodes\n{file}')
    chart = f'./Result/\\{method}\\interpolation_{file}_{method}_{str(len(nodes))}.png'
    plt.savefig(chart)
    plt.close()
