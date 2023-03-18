import pandas as pd
import matplotlib.pyplot as plt
import numpy


def readCsvFile():
    samples = []
    data = pd.read_csv("dis.csv")
    samples = data.Zamkniecie
    return samples


def calcEMA(samples, n, current):
    alpha = 2 / (n + 1)
    ema = 0
    denominator = 0
    for i in range(n + 1):
        if current - i >= 0:
            ema += ((1 - alpha) ** i) * samples[current - i]
            denominator += (1 - alpha) ** i
        else:
            break
    return ema / denominator


def formulaMACD():
    samples = readCsvFile()
    macd = []
    signal = []
    for current in range(1000):
        ema12 = calcEMA(samples, 12, current)
        ema26 = calcEMA(samples, 26, current)
        macd.append((ema12 - ema26))
        ema9 = calcEMA(macd, 9, current)
        signal.append(ema9)
    drawMainPlot(samples)
    drawMacdSignalPlot(macd, signal)
    drawAllInOnePlots(samples, macd, signal)
    

def drawMainPlot(samples):
    samples.plot(linewidth='0.8')
    plt.xlabel("Samples 29.03.2019 - 17.03.2023")
    plt.ylabel("close of the day on stocks")
    plt.show()


def drawMacdSignalPlot(macd, signal):
    plt.plot(macd, linewidth='0.8')
    plt.plot(signal, linewidth='0.8')
    plt.xlabel("Samples 29.03.2019 - 17.03.2023")
    plt.ylabel("close of the day on stocks")
    plt.show()


def drawAllInOnePlots(samples, macd, signal):
    x = samples


formulaMACD()
