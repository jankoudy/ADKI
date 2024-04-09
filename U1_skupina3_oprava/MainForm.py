from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from pio import *
from draw import Draw



class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(937, 1020)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.verticalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 937, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        self.menuInput = QtWidgets.QMenu(parent=self.menubar)
        self.menuInput.setObjectName("menuInput")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionRay_Crossing_Alg = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icons/ray.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRay_Crossing_Alg.setIcon(icon2)
        self.actionRay_Crossing_Alg.setObjectName("actionRay_Crossing_Alg")
        self.actionWinding_Number_Alg = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons/winding.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWinding_Number_Alg.setIcon(icon3)
        self.actionWinding_Number_Alg.setObjectName("actionWinding_Number_Alg")
        #self.actionPoint_Polygon = QtGui.QAction(parent=MainForm)
        #self.actionPoint_Polygon.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/icons/pointpol.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        #self.actionPoint_Polygon.setIcon(icon4)
        #self.actionPoint_Polygon.setObjectName("actionPoint_Polygon")
        self.actionClear_All = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/icons/clear_all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_All.setIcon(icon5)
        self.actionClear_All.setObjectName("actionClear_All")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAnalyze.addAction(self.actionRay_Crossing_Alg)
        self.menuAnalyze.addAction(self.actionWinding_Number_Alg)
        #self.menuInput.addAction(self.actionPoint_Polygon)
        self.menuInput.addSeparator()
        self.menuInput.addAction(self.actionClear_All)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionWinding_Number_Alg)
        self.toolBar.addAction(self.actionRay_Crossing_Alg)
        self.toolBar.addSeparator()
        #self.toolBar.addAction(self.actionPoint_Polygon)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_All)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainForm)
        self.actionOpen.triggered.connect(self.openClick) # type: ignore
        self.actionWinding_Number_Alg.triggered.connect(self.windingNumberClick) # type: ignore
        self.actionRay_Crossing_Alg.triggered.connect(self.rayCrossingClick) # type: ignore
        #self.actionPoint_Polygon.triggered['bool'].connect(self.pointPolygonClick) # type: ignore
        self.actionClear_All.triggered.connect(self.clearAllClick) # type: ignore
        self.actionExit.triggered.connect(MainForm.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        MainForm.showMaximized()
        
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
    
    def windingNumberClick(self):
    #Winding number algorithm
        
        # Get point and polygon
        q = self.Canvas.getPoint()
        polygons = self.Canvas.getPolygon()
        
        # Create new object
        a = Algorithms()
        
        # Show results
        mb = QtWidgets.QMessageBox() 
        mb.setWindowTitle("Point and polygon position")
        positions = 0
        
        # Run analysis
        for pol in polygons:
            
            #Find MMB points
            pxmin = min(pol, key = lambda k: k.x()) 
            pxmax = max(pol, key = lambda k: k.x())
            pymin = min(pol, key = lambda k: k.y())
            pymax = max(pol, key = lambda k: k.y())

            #Condition if outside MMB
            if q.x() < pxmin.x() or q.x() > pxmax.x() or q.y() < pymin.y() or q.y() > pymax.y():
                position = 0
            else:
                position = a.windingNumber(q,pol)
            
            #Diferent actions for positions
            if position==1:
                self.Canvas.highlightPolygon(pol)
                positions += 1
            elif position==0:
                pass
            elif position==2:
                self.Canvas.highlightPolygon(pol)
                positions += 1
            elif position==3:
                self.Canvas.highlightPolygon(pol)
                positions += 1
        
        #Messegebox if outside polygons
        if positions == 0:
            mb.setText("Point is OUTSIDE all polygons.")
            mb.exec()

    
    def rayCrossingClick(self):
    #Ray crossing algorithm
    
        # Get point and polygon
        q = self.Canvas.getPoint()
        polygons = self.Canvas.getPolygon()
        
        # Create new object
        a = Algorithms()
        
        # Show results
        mb = QtWidgets.QMessageBox() 
        mb.setWindowTitle("Point and polygon position")
        positions = 0
        
        # Run analysis
        for pol in polygons:
            
            #Find MMB points
            pxmin = min(pol, key = lambda k: k.x()) 
            pxmax = max(pol, key = lambda k: k.x())
            pymin = min(pol, key = lambda k: k.y())
            pymax = max(pol, key = lambda k: k.y())

            #Condition if outside MMB
            if q.x() < pxmin.x() or q.x() > pxmax.x() or q.y() < pymin.y() or q.y() > pymax.y():
                position = 0
            else:
                position = a.windingNumber(q,pol)

            #Diferent actions for positions
            if position==1:
                self.Canvas.highlightPolygon(pol)
                positions += 1
            elif position==0:
                pass
            elif position==2:
                self.Canvas.highlightPolygon(pol)
                positions += 1
            elif position==3:
                self.Canvas.highlightPolygon(pol)
                positions += 1
        
        #Messegebox if outside polygons    
        if positions == 0:
            mb.setText("Point is OUTSIDE all polygons.")
            mb.exec()
    
    '''
    def pointPolygonClick(self):
    #Switch drawing
    
        self.Canvas.switchDraw()
    
    '''
    
    def clearAllClick(self):
    #Clear all
    
        self.Canvas.clearData()
        #self.actionPoint_Polygon.setEnabled(True)
        #self.actionPoint_Polygon.setChecked(False)
        #self.Canvas.switchToPols()

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Analyze point and polygon position"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.menuInput.setTitle(_translate("MainForm", "Input"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionOpen.setToolTip(_translate("MainForm", "Open file"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionExit.setToolTip(_translate("MainForm", "Exit application"))
        self.actionRay_Crossing_Alg.setText(_translate("MainForm", "Ray Crossing Alg."))
        self.actionRay_Crossing_Alg.setToolTip(_translate("MainForm", "Ray Crossing Algorithm"))
        self.actionWinding_Number_Alg.setText(_translate("MainForm", "Winding Number Alg."))
        self.actionWinding_Number_Alg.setToolTip(_translate("MainForm", "Winding Number Algorithm"))
        #self.actionPoint_Polygon.setText(_translate("MainForm", "Point/Polygon"))
        #self.actionPoint_Polygon.setToolTip(_translate("MainForm", "Input Point or Polygon"))
        self.actionClear_All.setText(_translate("MainForm", "Clear data"))
        self.actionClear_All.setToolTip(_translate("MainForm", "Clear all data "))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
