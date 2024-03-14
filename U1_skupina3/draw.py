from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        
        #Initializing
        super().__init__(*args, **kwargs)
        self.polygons = []
        self.pol = QPolygonF()
        self.polygons.append(self.pol)
        self.q = QPointF(-100,-100)
        self.add_vertex = True
        self.hpolygons = []
        self.hpol = QPolygonF()
        self.hpolygons.append(self.hpol)
        
    def mousePressEvent(self, e:QMouseEvent):   
    #Event when clicked

        #Clear highlight polygon
        self.hpolygons = []
        self.hpol = QPolygonF()
        self.hpolygons.append(self.hpol)
        
        #Get cursor position
        x = e.position().x()
        y = e.position().y()

        #Draw polygon
        if self.add_vertex:
            #Create new point
            p = QPointF(x,y)
        
            #Add point to polygon
            self.pol.append(p)
            self.polygons[0] = self.pol
            
        #Draw point
        else:
            self.q.setX(x)
            self.q.setY(y)

        #Repaint screen
        self.repaint()
        

    def paintEvent(self,  e:QPaintEvent):
    #Draw situation
        
        #Create new object
        qp = QPainter(self)

        #Start drawing
        qp.begin(self)
        
        #Set atributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)

        #Draw polygons
        for i in self.polygons:
            qp.drawPolygon(i)
        
        #Set atributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.green)
        
        #Draw heiglight polygons
        for j in self.hpolygons:
            qp.drawPolygon(j)
        
        #Set atributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        #Draw point
        r = 5
        qp.drawEllipse(int(self.q.x() - r), int(self.q.y() - r), int(2*r), int(2*r))

        #End drawing
        qp.end()
        
    def switchDraw(self):
    #Switch drawing
        self.add_vertex = not(self.add_vertex)
        
    def switchToPoint(self):
    #Drawing point
        self.add_vertex = False
        
    def switchToPols(self):
    #Drawing polygons
        self.add_vertex = True
       
    def getPoint(self):
    #Return point 
        return self.q
    
    def getPolygon(self):
    #Return polygon
        return self.polygons
    
    def clearData(self):
        
        #Clear point
        self.q.setX(-100)
        self.q.setY(-100)
        
        #Clear polygons
        self.pol.clear()
        self.hpol.clear()
        self.polygons = []
        self.hpolygons = []
        self.polygons.append(self.pol)
        self.hpolygons.append(self.hpol)
        
        #Repaint screen
        self.repaint()
    
    def setData(self, pols):
    #Set polygons from file
        self.clearData()
        
        self.polygons = pols
        
        self.repaint()
    
    def highlightPolygon(self, pol):
    #Highlight polygons
        self.hpol = pol
        self.hpolygons.append(self.hpol)
        self.repaint()
        
                
                
    