from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *
from numpy.linalg import * #scipy.linalg
from QPoint3DF import *
from Edge import *
from Triangle import *

class Algorithms:
    
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        arg = dot/(nu*nv)
        
        #correct interval
        arg = max(-1, min(1,arg))
        
        return acos(arg)
 
    def getNearestPoint(self, q:QPoint3DF, points:list[QPoint3DF]):
        #return point nearest to q
        
        min_dis = inf
        min_i = -1
        
        #process all points of the cloud
        for i in range(len(points)):
            #compute distance
            if (q != points[i]):
                #q different from points[i]
                dis = sqrt((q.x()-points[i].x())**2+(q.y()-points[i].y())**2)
                
                #is distance new minimum?
                if (dis<min_dis):
                    min_dis = dis
                    min_i = i
                    
        return min_dis, min_i
    
    def getPointLinePosition(self, p:QPoint3DF, p1:QPoint3DF, p2:QPoint3DF):
        #analyze point and line position
        epsilon = 1.0e-6
        
        #compute vectors
        ux = p2.x()-p1.x()
        uy = p2.y()-p1.y()
        vx = p.x()-p1.x()
        vy = p.y()-p1.y()
        
        #compute test
        t = ux*vy - uy*vx
        
        if (t>0): #point on the left half-plane
            return 1
        elif (t<0): #point on the right half-plan
            return 0
        else: #point on line
            return -1
    
    def getDelauneyPoint(self, start:QPoint3DF, end:QPoint3DF, points:list[QPoint3DF]):
        #return delauney point
        omega_max = 0
        i_max = -1
        
        #process all points of the cloud
        for i in range(len(points)):
            #compute distance
            if (start != points[i] and end != points[i]):
                
                #point in left half-plane
                if self.getPointLinePosition(points[i], start, end) == 1:
                    
                    #compute angle
                    omega = self.get2VectorsAngle(points[i], start, points[i], end)
                
                    #is angle new maximum?
                    if (omega > omega_max):
                        omega_max = omega
                        i_max = i
                    
        return omega_max, i_max
        
    def createDT(self, points:list[QPoint3DF]):
        #return list of edges
        dt = []
        #active edges list
        ael = []
        
        #find start point
        p1 = min(points, key = lambda k: k.x())
        
        #find nearest point
        min_dis, min_i = self.getNearestPoint(p1, points)
        p2 = points[min_i]
        #p2 = self.getNearestPoint(p1, points)
        
        #create edges
        e = Edge(p1,p2)
        e_op = Edge(p2,p1)
        
        #add to AEL
        ael.append(e)
        ael.append(e_op)
        
        #repeat until AEL is empty
        while ael:
            #take the first edge
            e1 = ael.pop()
        
            #switch orientation
            e1_op = e1.changeOrientation()
            
            #fing optimal delaunay point
            omega_max, i_max = self.getDelauneyPoint(e1_op.getStart(), e1_op.getEnd(), points)
            
            #is there any delaunay point
            if i_max >= 0:
                
                #create remaining edges
                e2 = Edge(e1_op.getEnd(), points[i_max])
                e3 = Edge(points[i_max], e1_op.getStart())
                
                #add triangle to DT
                dt.append(e1_op)
                dt.append(e2)
                dt.append(e3)
                
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)
        
        return dt 
    
    def updateAEL(self, e:Edge, ael:list[Edge]):  
        #update list of valid delaunay edges
        
        #switch orientation
        e_op = e.changeOrientation()
        
        #is edge in ael
        if e_op in ael:
            ael.remove(e_op)
        else:
            ael.append(e)    
            
    def getContourPoint(self, p1:QPoint3DF, p2:QPoint3DF, z:float):
        #compute intersection point
        xb = (p2.x()-p1.x())/(p2.getZ()-p1.getZ())*(z-p1.getZ())+p1.x()
        yb = (p2.y()-p1.y())/(p2.getZ()-p1.getZ())*(z-p1.getZ())+p1.y()
        b = QPoint3DF(xb, yb, z)
        return b
    
    def createContourLine(self, dt:list[Edge], zmin:float, zmax:float, dz:float):
        #create contour lines with max z, min z and interval z
        contours = []
        contours_main = []
        
        #process all triangles
        for i in range(0, len(dt),3):
            #get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            
            #get Z of points
            z1 = p1.getZ()  
            z2 = p2.getZ()  
            z3 = p3.getZ()  
            
            #test horizontal plane and triangle intersections
            for z in arange(zmin, zmax, dz):
                dz1 = z-z1
                dz2 = z-z2
                dz3 = z-z3
                
                #triangle is coplanar
                if (dz1==0 and dz2==0 and dz3==0):
                    continue
                
                #edge 12 in plane
                elif(dz1==0 and dz2==0):
                    contours.append(dt[i])
                    
                #edge 23 in plane
                elif(dz2==0 and dz3==0):
                    contours.append(dt[i+1])
                    
                #edge 31 in plane
                elif(dz3==0 and dz1==0):
                    contours.append(dt[i+2])
                
                #edges 12 and 23 intersected by plane
                elif(dz1*dz2<=0 and dz2*dz3<0 or dz1*dz2<0 and dz2*dz3<=0):
                    #compute intersections
                    a = self.getContourPoint(p1,p2,z)
                    b = self.getContourPoint(p2,p3,z)
                    
                    #create edge and append to the list
                    e = Edge(a,b)
                    contours.append(e)
                    
                #edges 23 and 31 intersected by plane
                elif(dz2*dz3<=0 and dz3*dz1<0 or dz2*dz3<0 and dz3*dz1<=0):
                    #compute intersections
                    a = self.getContourPoint(p2,p3,z)
                    b = self.getContourPoint(p3,p1,z)
                    
                    #create edge and append to the list
                    e = Edge(a,b)
                    contours.append(e)
                    
                #edges 31 and 12 intersected by plane
                elif(dz3*dz1<=0 and dz1*dz2<0 or dz3*dz1<0 and dz1*dz2<=0):
                    #compute intersections
                    a = self.getContourPoint(p3,p1,z)
                    b = self.getContourPoint(p1,p2,z)
                    
                    #create edge and append to the list
                    e = Edge(a,b)
                    contours.append(e)                  
                      
        return contours
    
    def computeSlope (self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF):
        # compute triangle slope
        
        #vectors
        ux = p1.x()-p2.x()
        uy = p1.y()-p2.y()
        uz = p1.getZ()-p2.getZ()
        
        vx = p3.x()-p2.x()
        vy = p3.y()-p2.y()
        vz = p3.getZ()-p2.getZ()
        
        #normal vector
        nx = uy*vz-uz*vy
        ny = uz*vx-ux*vz
        nz = ux*vy-uy*vx
        
        #norm of vector
        norm = sqrt(nx*nx + ny*ny + nz*nz)
        
        #slope
        cosfi = abs(nz)/norm
        return acos(cosfi)
    
    def computeAspect(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF):
        # compute triangle aspect
        
        #vectors
        ux = p1.x()-p2.x()
        uy = p1.y()-p2.y()
        uz = p1.getZ()-p2.getZ()
        
        vx = p3.x()-p2.x()
        vy = p3.y()-p2.y()
        vz = p3.getZ()-p2.getZ()
        
        #normal vector
        nx = uy*vz-uz*vy
        ny = uz*vx-ux*vz
        
        #aspect
        aspect_help = atan2(nx,ny)
        if (aspect_help<0):
            aspect_help = aspect_help+2*pi
        return aspect_help
    
    def analyzeDTMSlope(self, dt:list[Edge]):
        #analyze DTM slope
        dtm_slope: list [Triangle] = []
        
        #process all triangles
        for i in range(0, len(dt),3):
            #get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            
            #compute slope
            slope = self.computeSlope(p1, p2, p3)
            
            #create triangle
            triangle = Triangle(p1, p2, p3, slope, 0)
            
            #add triangles to list
            dtm_slope.append(triangle)
            
        return dtm_slope
        
    def analyzeDTMAspect(self, dt:list [Edge]):
        #analyze dtm aspect 
        dtm_aspect: list [Triangle] = []    
        
        #Process all triangles
        for i in range(0, len(dt), 3):
            #Get vertices of triangle
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()
            
            #Get aspect
            aspect = self.computeAspect(p1, p2, p3)
            
            #Create triangle
            triangle = Triangle(p1, p2, p3, 0, aspect)
            
            #Add triangle to the list
            dtm_aspect.append(triangle)
            
        return dtm_aspect
        