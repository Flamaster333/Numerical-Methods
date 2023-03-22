import pandas as pd
import matplotlib.pyplot as plt


class Macd:
    samples = []
    macd = []
    signal = []
    dates = []
    intersection_values = []
    budget_plot = []

    def __init__(self, file_name, number_of_samples):
        self.number_of_samples = number_of_samples
        self.file_name = file_name

    def readCsvFileClosure(self):
        data = pd.read_csv(self.file_name)
        self.samples = data.Zamkniecie

    def readCsvFileDates(self):
        data = pd.read_csv(self.file_name)
        dates = data.Data
        return dates

    @staticmethod
    def calcEMA(data, n, current):
        alpha = 2 / (n + 1)
        ema = 0
        denominator = 0
        for i in range(n + 1):
            if current - i >= 0:
                ema += ((1 - alpha) ** i) * data[current - i]
                denominator += (1 - alpha) ** i
            else:
                break
        return ema / denominator

    def formulaMACD(self):
        self.readCsvFileClosure()
        for current in range(self.number_of_samples):
            ema12 = self.calcEMA(self.samples, 12, current)
            ema26 = self.calcEMA(self.samples, 26, current)
            self.macd.append((ema12 - ema26))
            ema9 = self.calcEMA(self.macd, 9, current)
            self.signal.append(ema9)

    @staticmethod
    def showPlot():
        plt.title("Walt Disney Co")
        plt.xlabel("Samples 29.03.2019 - 17.03.2023")
        plt.ylabel("Close of the day on stocks")
        plt.show()

    # all plot creating
    def drawPlots(self):
        # main data plot
        plt.figure().set_figwidth(15)
        plt.plot(self.samples, color='g', linewidth='0.8')
        self.showPlot()
        # macd and signal plot
        plt.figure().set_figwidth(15)
        plt.plot(self.macd, color='b', linewidth='0.8')
        plt.plot(self.signal, color='r', linewidth='0.8')
        self.showPlot()
        # all in one plot
        plt.figure().set_figwidth(15)
        plt.plot(self.samples, color='g', linewidth='0.8')
        plt.plot(self.macd, color='b', linewidth='0.8')
        plt.plot(self.signal, color='r', linewidth='0.8')
        self.showPlot()
        # all in one plot
        plt.figure().set_figwidth(15)
        plt.plot(self.samples, color='g', linewidth='0.8')
        plt.plot(self.macd, color='b', linewidth='0.8')
        plt.plot(self.signal, color='r', linewidth='0.8')
        plt.plot(self.budget_plot, color='#FF9626', linewidth='0.8')
        self.showPlot()

    def intersectionSignalMacd(self):
        if self.macd[34] > self.signal[34]:
            macd_was_higher = 1
        else:
            macd_was_higher = 0
        for i in range(35, self.number_of_samples):
            if macd_was_higher == 1 and self.macd[i] <= self.signal[i]:
                self.intersection_values.append((i, macd_was_higher))
                macd_was_higher = 0
            elif macd_was_higher == 0 and self.macd[i] >= self.signal[i]:
                self.intersection_values.append((i, macd_was_higher))
                macd_was_higher = 1

    def simulation(self):
        budget = 1000
        # the budget line to the first intersection
        for i in range(0, self.intersection_values[0][0]):
            self.budget_plot.append(budget)
        print("Budget at the beginning: ", budget, "$")
        number_of_shares = 0
        for intersection in self.intersection_values:
            if intersection[1] == 0:
                number_of_shares = budget // self.samples[intersection[0]-1]
                budget -= (number_of_shares * self.samples[intersection[0]-1])
            else:
                budget += (number_of_shares * self.samples[intersection[0]-1])
                number_of_shares = 0
            if intersection[0] != self.intersection_values[(len(self.intersection_values) - 1)][0]:
                for i in range(intersection[0],
                               self.intersection_values[self.intersection_values.index(intersection) + 1][0]):
                    self.budget_plot.append(budget)
        # if some shares are left
        if number_of_shares > 0:
            budget += (number_of_shares * self.samples[len(self.samples) - 1])
        print("Budget at the end: ", round(budget, 2), "$")
