from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw
from pio import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1748, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        
        self.actionMinimum_bounding_rectangle = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMinimum_bounding_rectangle.setIcon(icon2)
        self.actionMinimum_bounding_rectangle.setObjectName("actionMinimum_bounding_rectangle")
        
        self.actionPCA = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons/pca.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPCA.setIcon(icon3)
        self.actionPCA.setObjectName("actionPCA")
        
        self.actionLongest_edge = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/icons/longestedge.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongest_edge.setIcon(icon4)
        self.actionLongest_edge.setObjectName("actionLongest_edge")
        
        self.actionWall_average = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWall_average.setIcon(icon5)
        self.actionWall_average.setObjectName("actionWall_average")
        
        self.actionWeighted_Bisector = QtGui.QAction(parent=MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/icons/weightedbisector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeighted_Bisector.setIcon(icon6)
        self.actionWeighted_Bisector.setObjectName("actionWeighted_Bisector")
        
        self.actionClear_results = QtGui.QAction(parent=MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/icons/clear_ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_results.setIcon(icon7)
        self.actionClear_results.setObjectName("actionClear_results")
        self.actionClear_all = QtGui.QAction(parent=MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/icons/clear_er.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon8)
        self.actionClear_all.setObjectName("actionClear_all")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSimplify.addAction(self.actionMinimum_bounding_rectangle)
        self.menuSimplify.addAction(self.actionPCA)
        self.menuSimplify.addAction(self.actionLongest_edge)
        self.menuSimplify.addAction(self.actionWall_average)
        self.menuSimplify.addAction(self.actionWeighted_Bisector)
        self.menuView.addAction(self.actionClear_results)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionClear_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMinimum_bounding_rectangle)
        self.toolBar.addAction(self.actionPCA)
        self.toolBar.addAction(self.actionLongest_edge)
        self.toolBar.addAction(self.actionWall_average)
        self.toolBar.addAction(self.actionWeighted_Bisector)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_results)
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        
        self.actionOpen.triggered.connect(self.openClick) 
        self.actionMinimum_bounding_rectangle.triggered.connect(self.mbrClick) 
        self.actionPCA.triggered.connect(self.pcaClick) 
        self.actionLongest_edge.triggered.connect(self.leClick) 
        self.actionWall_average.triggered.connect(self.waClick) 
        self.actionWeighted_Bisector.triggered.connect(self.wbClick)
        self.actionClear_results.triggered.connect(self.clearClick)
        self.actionClear_all.triggered.connect(self.clearAllClick) 
        self.actionExit.triggered.connect(MainWindow.close) 
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def openClick(self):
        #Opening data
        
        #Create object
        io = IO()

        #Widgete size
        size = self.Canvas.size()
        w = size.width()
        h = size.height() 
        #Polygons from shapefile
        polygons = io.loadData(w,h)
        
        #If polygons load 
        if polygons != None:
            #Show polygons
            self.Canvas.setData(polygons)
            
            #Set switch
            #self.actionPoint_Polygon.setChecked(True)
            #self.actionPoint_Polygon.setEnabled(False)
            #self.Canvas.switchToPoint()
    
    def mbrClick(self):
        #get building 
        building = self.Canvas.getBuilding()
        
        #simplification
        a = Algorithms()
        res, eff = a.createMBR(building)        
        
        #set results
        self.Canvas.setER(res)
        
        #repaint
        self.Canvas.repaint()
        
        #count evaluation criteria
        n = len(res)
        if n > 0:
            criteria = 0
            for i in eff:
                criteria += i
            
            criteria = round(criteria/n, 4)
            #message box with evaluation critera
            dlg = QtWidgets.QMessageBox()
            dlg.setStyleSheet("QLabel{min-width: 400px;}")
            dlg.setWindowTitle("Evaluation criterion for Minimum Area Enclosing Rectangle")
            dlg.setText("Average angular deviation: " + str(criteria) + '°')
            dlg.exec()
    
    def pcaClick(self):
        #get building 
        building = self.Canvas.getBuilding()
        
        #simplification
        a = Algorithms()
        res, eff = a.createER_PCA(building)        
        
        #set results
        self.Canvas.setER(res)
        
        #repaint
        self.Canvas.repaint()
        
        #count evaluation criteria
        n = len(res)
        if n > 0:
            criteria = 0
            for i in eff:
                criteria += i
            
            criteria = round(criteria/n, 4)
            #message box with evaluation critera
            dlg = QtWidgets.QMessageBox()
            dlg.setStyleSheet("QLabel{min-width: 400px;}")
            dlg.setWindowTitle("Evaluation criterion for PCA")
            dlg.setText("Average angular deviation: " + str(criteria) + '°')
            dlg.exec()
    
    def leClick(self):
        #get building 
        building = self.Canvas.getBuilding()
        
        #simplification
        a = Algorithms()
        res, eff = a.createER_LongestEdge(building)        
        
        #set results
        self.Canvas.setER(res)
        
        #repaint
        self.Canvas.repaint()
        
        #count evaluation criteria
        n = len(res)
        if n > 0:
            criteria = 0
            for i in eff:
                criteria += i
            
            criteria = round(criteria/n, 4)
            #message box with evaluation critera
            dlg = QtWidgets.QMessageBox()
            dlg.setStyleSheet("QLabel{min-width: 400px;}")
            dlg.setWindowTitle("Evaluation criterion for Longest Edge")
            dlg.setText("Average angular deviation: " + str(criteria) + '°')
            dlg.exec()
        
    def waClick(self):
        #get building 
        building = self.Canvas.getBuilding()
        
        #simplification
        a = Algorithms()
        res, eff = a.createER_WallAverage(building)        
        
        #set results
        self.Canvas.setER(res)
        
        #repaint
        self.Canvas.repaint()
        
        #count evaluation criteria
        n = len(res)
        if n > 0:
            criteria = 0
            for i in eff:
                criteria += i
            
            criteria = round(criteria/n, 4)
            #message box with evaluation critera
            dlg = QtWidgets.QMessageBox()
            dlg.setStyleSheet("QLabel{min-width: 400px;}")
            dlg.setWindowTitle("Evaluation criterion for Wall Average")
            dlg.setText("Average angular deviation: " + str(criteria) + '°')
            dlg.exec()
    
    def wbClick(self):
        #get building 
        building = self.Canvas.getBuilding()
        
        #simplification
        a = Algorithms()
        res, eff = a.createER_WeightedBisector(building)        
        
        #set results
        self.Canvas.setER(res)
        
        #repaint
        self.Canvas.repaint()
        
        #count evaluation criteria
        n = len(res)
        if n > 0:
            criteria = 0
            for i in eff:
                criteria += i
            
            criteria = round(criteria/n, 4)
            #message box with evaluation critera
            dlg = QtWidgets.QMessageBox()
            dlg.setStyleSheet("QLabel{min-width: 400px;}")
            dlg.setWindowTitle("Evaluation criterion for Weighted Bisector")
            dlg.setText("Average angular deviation: " + str(criteria) + '°')
            dlg.exec()
        
    def clearClick(self):
        self.Canvas.clearER()
        self.Canvas.repaint()
    
    def clearAllClick(self):
        self.Canvas.clearData()
        self.Canvas.repaint()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simplify buildings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSimplify.setTitle(_translate("MainWindow", "Simplify"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open file"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Close application"))
        self.actionMinimum_bounding_rectangle.setText(_translate("MainWindow", "Minimum Area Enclosing Rectangle"))
        self.actionMinimum_bounding_rectangle.setToolTip(_translate("MainWindow", "Simplify using minimum area enclosing rectanglee"))
        self.actionPCA.setText(_translate("MainWindow", "PCA"))
        self.actionPCA.setToolTip(_translate("MainWindow", "Simplify building using PCA"))
        self.actionLongest_edge.setText(_translate("MainWindow", "Longest Edge"))
        self.actionLongest_edge.setToolTip(_translate("MainWindow", "Simplify using longest edge"))
        self.actionWall_average.setText(_translate("MainWindow", "Wall Average"))
        self.actionWall_average.setToolTip(_translate("MainWindow", "Simplify building using wall average"))
        self.actionWeighted_Bisector.setText(_translate("MainWindow", "Weighted Bisector"))
        self.actionWeighted_Bisector.setToolTip(_translate("MainWindow", "Simplify using weighted bisector"))
        self.actionClear_results.setText(_translate("MainWindow", "Clear results"))
        self.actionClear_all.setText(_translate("MainWindow", "Clear all"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
