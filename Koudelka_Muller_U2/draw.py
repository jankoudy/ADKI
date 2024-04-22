from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = []
        self.ch = QPolygonF()
        self.er = []


    def paintEvent(self,  e:QPaintEvent):
        #Draw situation
        
        #Create new object
        qp = QPainter(self)

        #Start drawing
        qp.begin(self)

        #Set graphic attributes - building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)

        #Draw building
        for i in self.building:
            qp.drawPolygon(i)
        
        #Set graphic attributes - er
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)

        #Draw building
        for i in self.er:
            qp.drawPolygon(i)
        
        #End drawing
        qp.end()
        
    
    def getBuilding(self):
        # Return building
        return self.building
    
    def setER(self, er:list[QPolygonF]):
        self.er = er
    
    def clearER(self):
        #Clear polygon
        self.er = []
        
        #Repaint screen
        self.repaint()
        
    def clearData(self):        
        #Clear polygons
        self.building = []
        self.er = []
        
        #Repaint screen
        self.repaint()
        
    def setData(self, pols):
    #Set polygons from file
        self.clearData()
        
        self.building = pols
        
        self.repaint()
        