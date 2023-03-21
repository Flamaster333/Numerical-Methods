import pandas as pd
import matplotlib.pyplot as plt


def readCsvFileClosure():
    data = pd.read_csv("dis.csv")
    samples = data.Zamkniecie
    return samples


def readCsvFileDates():
    data = pd.read_csv("dis.csv")
    dates = data.Data
    return dates


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
    samples = readCsvFileClosure()
    macd = []
    signal = []
    for current in range(1000):
        ema12 = calcEMA(samples, 12, current)
        ema26 = calcEMA(samples, 26, current)
        macd.append((ema12 - ema26))
        ema9 = calcEMA(macd, 9, current)
        signal.append(ema9)
    budget_plot = []
    budget_plot = intersectionSignalMacd(samples, macd, signal)
    drawPlots(samples, macd, signal, budget_plot)



def showPlot():
    plt.title("Walt Disney Co")
    plt.xlabel("Samples 29.03.2019 - 17.03.2023")
    plt.ylabel("Close of the day on stocks")
    plt.show()


# all plot creating
def drawPlots(samples, macd, signal, budget):
    # main data plot
    plt.figure().set_figwidth(15)
    plt.plot(samples, color='g', linewidth='0.8')
    showPlot()
    # macd and signal plot
    plt.figure().set_figwidth(15)
    plt.plot(macd, color='b', linewidth='0.8')
    plt.plot(signal, color='r', linewidth='0.8')
    showPlot()
    # all in one plot
    plt.figure().set_figwidth(15)
    plt.plot(samples, color='g', linewidth='0.8')
    plt.plot(macd, color='b', linewidth='0.8')
    plt.plot(signal, color='r', linewidth='0.8')
    showPlot()
    # all in one plot
    plt.figure().set_figwidth(15)
    plt.plot(samples, color='g', linewidth='0.8')
    plt.plot(macd, color='b', linewidth='0.8')
    plt.plot(signal, color='r', linewidth='0.8')
    plt.plot(budget, color='y', linewidth='0.8')
    showPlot()


def intersectionSignalMacd(samples, macd, signal):
    if macd[34] > signal[34]:
        macd_was_higher = 1
    else:
        macd_was_higher = 0
    intersection_values = []

    for i in range(35, 1000):
        if macd_was_higher == 1 and macd[i] <= signal[i]:
            intersection_values.append((i, macd_was_higher))
            macd_was_higher = 0
        elif macd_was_higher == 0 and macd[i] >= signal[i]:
            intersection_values.append((i, macd_was_higher))
            macd_was_higher = 1
    return simulation(samples, intersection_values)


def simulation(samples, intersection_values):
    budget = 500
    budget_plot = []
    for i in range(0, intersection_values[0][0]):
        budget_plot.append(budget)
    print("Budget at the beginning: ", budget, "$")
    number_of_shares = 0
    if intersection_values[(len(intersection_values)-1)][1] == 0:
        intersection_values.pop(len(intersection_values)-1)
    for intersection in intersection_values:
        if intersection[1] == 0:
            number_of_shares = budget // samples[intersection[0]]
            budget -= (number_of_shares * samples[intersection[0]])
        else:
            budget += (number_of_shares * samples[intersection[0]])
            number_of_shares = 0
        if intersection[0] != intersection_values[(len(intersection_values)-1)][0]:
            for i in range(intersection[0], intersection_values[intersection_values.index(intersection)+1][0]):
                budget_plot.append(budget)
    print("Budget at the end: ", budget, "$")
    return budget_plot


# start
formulaMACD()
