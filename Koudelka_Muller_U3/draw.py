from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Edge import *
from QPoint3DF import *
from random import *
from Triangle import *
from math import *

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = []
        self.dt = []
        self.contours = []
        self.dtm_slope = []
        self.dtm_aspect = []
        self.dz = 10
        self.zmin = 0
        self.zmax = 1602
        self.viewDT = True
        self.viewContourLines = True
        self.viewSlope = True
        self.viewAspect = True

    def paintEvent(self,  e:QPaintEvent):
        #Draw situation
        
        #Create new object
        qp = QPainter(self)

        #Start drawing
        qp.begin(self)
        
        #Set graphic attributes
        qp.setPen(Qt.GlobalColor.gray)
        
        if self.viewSlope:
            #Draw slope
            for t in self.dtm_slope:
            
                #get slope
                slope = t.getSlope()
            
                #compute color
                k = 255/(pi/2)
                c = int(255 - slope*k)
                color = QColor(c,c,c)
                qp.setBrush(color)
            
                #draw polygon
                qp.drawPolygon(t.getVertices())
            
        if self.viewAspect:
            
            #Draw aspcet
            for t in self.dtm_aspect:
            
                #get aspect
                aspect = t.getAspect()
            
                #compute color
                k = 255/(pi/2)
                if (aspect>=0 and aspect<pi/2):
                    r = int(255-aspect*k)
                    g = 0
                    b = int(aspect*k)
                elif (aspect>=pi/2 and aspect<pi):
                    r = 0
                    g = int((aspect-pi/2)*k)
                    b = 255
                elif (aspect>=pi and aspect<3*pi/2):
                    r = int((aspect-pi)*k)
                    g = 255
                    b = int(255-(aspect-pi)*k)
                elif (aspect>=3*pi/2 and aspect<2*pi):
                    r = 255
                    g = int(255-(aspect-3*pi/2)*k)
                    b = 0
                
                color = QColor(r,g,b)
                qp.setBrush(color)
            
                #draw polygon
                qp.drawPolygon(t.getVertices())
            
        #DRAW DT
        if self.viewDT:     
            #Set graphic attributes
            qp.setPen(Qt.GlobalColor.green)
            qp.setBrush(Qt.GlobalColor.transparent)
            
            #Draw triangulation
            for e in self.dt:
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        
        if self.viewContourLines:
            for c in range(len(self.contours)):
                #Set graphic attributes
                
                pen = QPen()
                pen.setColor(Qt.GlobalColor.darkGray)
                pen.setWidth(1)
                
                start_x = int(self.contours[c].getStart().x())
                start_y = int(self.contours[c].getStart().y())
                end_x = int(self.contours[c].getEnd().x())
                end_y = int(self.contours[c].getEnd().y())
         
                #Draw contour lines
                z = self.contours[c].getStart().getZ()
                if ((z-self.zmin)%(self.dz*5)==0):
                    pen.setWidth(3)
                    
                qp.setPen(pen)
                    
                qp.drawLine(start_x, start_y, end_x, end_y)
   
        #Set graphic attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.black)


        #Draw points
        r = 4
        for p in self.points:
            qp.drawEllipse(int(p.x()-r), int(p.y()-r), 2*r, 2*r)
            
        #End drawing
        qp.end()
        
    def getPoints(self):
        #Return points
        return self.points
    
    def clearResults(self):
        #clear triangles
        self.dt.clear()
        
        #clear contours
        self.contours.clear()
        
        #clear slope
        self.dtm_slope.clear()
        
        #clear aspect
        self.dtm_aspect.clear()
                
        #Repaint screen
        self.repaint()
      
    def clearAll(self):
        #Clear points
        self.points.clear()
        
        #clear triangles
        self.dt.clear()
        
        #clear contours
        self.contours.clear()
        
        #clear slope
        self.dtm_slope.clear()
        
        #clear aspect
        self.dtm_aspect.clear()
                
        #Repaint screen
        self.repaint()
        
    
    def setDT(self, dt:list[Edge]):
        #Set DT
        self.dt = dt
        
    def getDT(self):
        #Get DT
        return self.dt
        
    def setContours(self, contours:list[Edge], zmin, zmax, dz):
        #Set contours
        self.contours = contours
        self.zmin = zmin
        self.zmax = zmax
        self.dz = dz
        
        
    def setDTMSlope(self, dtm_slope: list[Triangle]):
        self.dtm_slope = dtm_slope
        
    def setDTMAspect(self, dtm_aspect: list[Triangle]):
        self.dtm_aspect = dtm_aspect    
        
    def setViewDT(self, viewDT):
        self.viewDT = viewDT

    def setViewContourLines(self, viewContourLines):
        self.viewContourLines = viewContourLines
        
    def setViewSlope(self, viewSlope):
        self.viewSlope = viewSlope

    def setViewAspect(self, viewAspect):
        self.viewAspect = viewAspect
        
    def setData(self, points):
    #Set points from file
        self.clearAll()
        
        self.points = points
        
        self.repaint()