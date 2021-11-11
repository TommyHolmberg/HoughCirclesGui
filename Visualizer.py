from matplotlib import pyplot as plt
import numpy as np

class Visualizer:
    def plotCircleDistances(self, list):
        plt.plot(range(len(list)), list)
        plt.title("Circle detection")
        plt.xticks(range(0,10))
        plt.xlim(0, 10)
        plt.ylim(10, 20)
        plt.xlabel("Test nr")
        plt.ylabel("Pixels")
        plt.show()

    def exportToCsv(self, filename, list):
        np.savetxt(filename, list, delimiter=",", fmt='% s')

    def exportMeanStdVarToCsv(self, filename, list):
        stats = [np.mean(list), np.std(list), np.var(list)]
        list.insert(0, "Test nr")
        stats.insert(0, "Mean, standard dev, variance")
        self.exportToCsv(filename, [list, stats])
