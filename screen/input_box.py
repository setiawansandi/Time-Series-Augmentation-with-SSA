from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

from screen.plotly_viewer import PlotlyViewer
from pltSSsur import pltSSsur
from utils.plot import Plot
  
class InputBox(QMainWindow):
  
    def __init__(self, total_entry = 3, *, fe, separator, num_comp, data_dir_path=None):
        super().__init__()
        self._total_entry = total_entry
        self.fe = fe
        self.separator = separator
        self.num_comp = num_comp
        self.data_dir_path = data_dir_path
        self.w = None # plot window

        # keep main window on top when another window is open
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Enter File Name")
        # self.resize(453,117) # resize() will auto center the window
        winSize = [453, 117]
        centerPoint = QDesktopWidget().availableGeometry().center()
        xPos = centerPoint.x() - winSize[0]//2 - 710
        yPos = centerPoint.y() - winSize[1]//2

        self.setGeometry(QtCore.QRect(xPos, yPos, winSize[0], winSize[1]))
        self.setFixedSize(winSize[0], winSize[1])
        self.UiComponents() # initializing ui      
        self.show() # showing all the widgets
  

    def UiComponents(self):
        # https://stackoverflow.com/questions/54749161/what-is-the-rule-for-choosing-central-widget-in-qmainwindow-and-why-is-it-imp
        # tldr: not important unless you want to have extra components
        #       such as toolbar, menubar, docker, etc
        self.centralwidget = QtWidgets.QWidget(self)
        # objectName acts similar to id
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # initialisation
        segoe = QtGui.QFont()
        segoe.setFamily("Segoe UI")
        segoe.setPointSize(9)

        segoe_sb = QtGui.QFont()
        segoe_sb.setFamily("Segoe UI Semibold")
        segoe_sb.setPointSize(9)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 351, 21))
        self.label.setFont(segoe)
        self.label.setObjectName("label")
        self.label.setText("Press [Tab] to change entry, and [Enter] to submit")

        self.inputContainerWidget = QtWidgets.QWidget(self.centralwidget)
        self.inputContainerWidget.setGeometry(QtCore.QRect(20, 50, 416, 51))
        self.inputContainerWidget.setObjectName("inputContainer")
        # convert widget to layout
        self.inputContainerLayout = QtWidgets.QHBoxLayout(self.inputContainerWidget)
        self.inputContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.inputContainerLayout.setObjectName("inputContainerLayout")

        self.entry_list = []
        # create input box
        for i in range(self._total_entry):
            self.entry_list.append(self.create_entry(self.inputContainerWidget))
            self.inputContainerLayout.addWidget(self.entry_list[i])


    def create_entry(self, parentWidget):
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        line_style = '''
        QLineEdit
        {background : lightblue;}
        '''

        lineEdit = QtWidgets.QLineEdit(parentWidget)
        lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        lineEdit.setFont(font)
        lineEdit.setStyleSheet(line_style)
        lineEdit.setObjectName("lineEdit")

        return lineEdit

    
    def show_plot(self, file_data, surr_data, *, fn=''):
        
        fig = Plot.ssa(file_data, surr_data, num_comp=self.num_comp, title=fn)
        self.w = PlotlyViewer(fig=fig)
        self.w.show()

        # so cursor remains active when switching window
        self.show() 
        self.raise_() 
        self.activateWindow()

    
    def constuct_fn(self):
        fn = ''
        for i in range(len(self.entry_list)):
            text = self.entry_list[i].text()
            fn += text
            if text != '':
                fn +=  self.separator
        if fn [-1] == self.separator:
            fn = fn[:-1]
        fn = fn + '.' + self.fe

        return fn

    
    # @override
    def keyPressEvent(self, event):
        import logging
        logger=logging.getLogger()
        
        if event.key() == Qt.Key_Return:
            try:
                _fn = self.constuct_fn() # construct file name
                
                file_data, surr_data = pltSSsur(_fn, num_comp=self.num_comp, plot_ok=True, data_dir_path=self.data_dir_path)

                self.show_plot(file_data, surr_data, fn=_fn)
            except Exception as e:
                logger.exception(str(e))
    

    def closeEvent(self, event):
        try: self.w.close()
        except: pass



if __name__ == '__main__':  
    App = QApplication(sys.argv) # create pyqt5 app
    window = InputBox(total_entry=3, fe='csv', separator='_', num_comp=3) # create the instance of our Window
    sys.exit(App.exec()) # start the app