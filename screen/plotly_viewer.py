import os
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets
import plotly.offline

class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig, exec=True):

        super().__init__()

        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "plot.html"))
        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))
        self.setWindowTitle("SSA output")
        self.resize(930, 750)

    def closeEvent(self, event):
        os.remove(self.file_path)
