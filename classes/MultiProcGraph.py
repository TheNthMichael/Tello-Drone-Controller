# Library packages needed
import numpy as np
import datetime
import sys
import queue
import multiprocessing

# Plot related packages
import matplotlib.pyplot as plt


def startGraph(q, title):
    grph = DroneGraph(q, title)


class DroneGraph:
    def __init__(self, q, title):
        super().__init__()
        self.previousEstimatedPoses = {
            "x": [0],
            "y": [0],
            "z": [0],
            "u": [0],
            "v": [0],
            "w": [0],
            "t": [0],
        }
        self.q = q
        self.title = title
        self.figure = plt.figure()
        self.figure.suptitle(title)
        self.ax = self.figure.gca(projection="3d")
        self.figure.show()
        self.RXDataLoop()

    def RXDataLoop(self):
        while True:
            try:
                previousEstimatedPoses = self.q.get(True, 1.0)  # Wait a couple of seconds
            except queue.Empty:
                print("Data Not Received...\nClosing Grapher...")
                #sys.exit()
            self.previousEstimatedPoses["x"].append(previousEstimatedPoses["x"][-1])
            self.previousEstimatedPoses["y"].append(previousEstimatedPoses["y"][-1])
            self.previousEstimatedPoses["z"].append(previousEstimatedPoses["z"][-1])
            self.previousEstimatedPoses["u"].append(previousEstimatedPoses["u"][-1])
            self.previousEstimatedPoses["v"].append(previousEstimatedPoses["v"][-1])
            self.previousEstimatedPoses["w"].append(previousEstimatedPoses["w"][-1])
            self.ax.quiver(
                self.previousEstimatedPoses["x"],
                self.previousEstimatedPoses["y"],
                self.previousEstimatedPoses["z"],
                self.previousEstimatedPoses["u"],
                self.previousEstimatedPoses["v"],
                self.previousEstimatedPoses["w"],
                length=10,
                normalize=True,
                color="b",
            )
            self.figure.canvas.draw()
            plt.pause(1/1000)