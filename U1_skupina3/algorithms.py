from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:
    
    def __init__(self):
        pass
    
    def getPointPolPosition(self, q:QPointF, pol:QPolygonF):
        #Point and polygon position, ray crossing algorithm
        k = 0
        n = len(pol)
        V = 0
        
        #Process all vertices of polygon
        for i in range(n):
            
            if (i != (n-1)):      
                a = i
                b = i+1
            else:
                a = i
                b = 0
            
            #Reduce coordinates
            x_ir = pol[a].x() - q.x()
            y_ir = pol[a].y() - q.y()
            
            x_i1r = pol[(b)%n].x() - q.x()
            y_i1r = pol[(b)%n].y() - q.y()
            
            #Appropriate segment intersection the ray
            if (((y_i1r > 0) and (y_ir <= 0)) or ((y_ir > 0) and (y_i1r <= 0))):
                
                #Compute intersection coordinate
                xm = (x_i1r*y_ir - x_ir*y_i1r)/(y_i1r-y_ir)
                
                # Appropriate intersection, increment k
                if xm > 0:
                    k = k + 1

            #det
            t = ((pol[b].x()-pol[a].x())*(q.y()-pol[a].y()))-((pol[b].y()-pol[a].y())*(q.x()-pol[a].x()))
            
            #on the edge or vertex?
            if (t==0):
                V = V+1
        
        #on edge
        if(V==1):
            return 2
        
        #on vertex
        if(V>1):
            return 3
            
        #Inside          
        if k%2 == 1:
            return 1
        
        #Outside
        return 0
    
    def windingNumber(self, q:QPointF, pol:QPolygonF):
        #Winding Number algorithm
        w = 0
        n = len(pol)
        V = 0 #q on edges
        
        #Process all vertices of polygon
        for i in range(n):
            
            if (i != (n-1)):      
                a = i
                b = i+1
            else:
                a = i
                b = 0
                             
            #sides of triangle
            dif_x_qi = pol[a].x() - q.x()
            dif_y_qi = pol[a].y() - q.y()
            l_qi = sqrt(dif_x_qi*dif_x_qi + dif_y_qi*dif_y_qi)
            
            dif_x_qi1 = pol[b].x() - q.x()
            dif_y_qi1 = pol[b].y() - q.y()
            l_qi1 = sqrt(dif_x_qi1*dif_x_qi1 + dif_y_qi1*dif_y_qi1)
            
            dif_x_ii1 = pol[a].x() - pol[b].x()
            dif_y_ii1 = pol[a].y() - pol[b].y()
            l_ii1 = sqrt(dif_x_ii1*dif_x_ii1 + dif_y_ii1*dif_y_ii1)
            
            #w_i - Law of cosines 
            if(l_qi == 0 or l_qi1 == 0):
                V==5
            else:
                con = (l_qi*l_qi + l_qi1*l_qi1 - l_ii1*l_ii1)/(2*l_qi*l_qi1)
                con = min(con, 1)
                con = max(con, -1)
                w_i = acos(con)
            
            #det
            t = ((pol[b].x()-pol[a].x())*(q.y()-pol[a].y()))-((pol[b].y()-pol[a].y())*(q.x()-pol[a].x()))
            
            #counting w
            if (t>0): 
                w = w + w_i
            elif (t<0):
                w = w-w_i
                
            #on the edge or vertex?
            if (t==0):
                V = V+1
                   
        const = 2*pi
        E = 0.01 #nevim jakou zadat
        
        #on edge
        if(V==1):
            return 2
        
        #on vertex
        if(V>1):
            return 3
        
        #Inside          
        if (abs(abs(w)-const)<E):
            return 1
        
        #Outside
        return 0
                
                
        