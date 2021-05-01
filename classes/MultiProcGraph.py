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
        self.q = q
        self.title = title
        self.figure = plt.figure()
        self.figure.suptitle(title)
        self.ax = self.figure.gca(projection="3d")
        self.figure.show()
        self.RXDataLoop()

    def RXDataLoop(self):
        previousEstimatedPoses = None
        while True:
            try:
                previousEstimatedPoses = self.q.get(True, 2.0)  # Wait a couple of seconds
            except queue.Empty:
                print("Data Not Received...\nClosing Grapher...")
                sys.exit()

            self.ax.quiver(
                previousEstimatedPoses["x"][-1],
                previousEstimatedPoses["y"][-1],
                previousEstimatedPoses["z"][-1],
                previousEstimatedPoses["u"][-1],
                previousEstimatedPoses["v"][-1],
                previousEstimatedPoses["w"][-1],
                color="b",
            )
            self.figure.canvas.draw()