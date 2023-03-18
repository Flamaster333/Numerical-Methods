import pandas as pd
import matplotlib.pyplot as plt
import numpy


def readCsvFile():
    samples = []
    data = pd.read_csv("dis.csv")
    samples = data.Zamkniecie
    return samples


def calcEMA(samples, n):
    alpha = 2 / (n + 1)
    ema = samples[0]
    denominator = 1
    for i in range(1, n + 1):
        ema += ((1 - alpha) ** i) * samples[i]
        denominator += (1 - alpha) ** i
    return ema / denominator


def formulaMACD(samples):
    ema12 = calcEMA(samples, 12)
    ema26 = calcEMA(samples, 26)

    return ema12 - ema26


samples = readCsvFile()
samples.plot(linewidth='0.8')
plt.xlabel("Samples 29.03.2019 - 17.03.2023")
plt.ylabel("close of the day on stocks")
plt.show()
