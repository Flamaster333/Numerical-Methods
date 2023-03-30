from macd import Macd

if __name__ == '__main__':
    macd = Macd("dis.csv", 1000, 450, 500)
    macd.formulaMACD()
    macd.intersectionSignalMacd()
    macd.simulation()
    macd.drawPlots()