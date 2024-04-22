from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *
from numpy.linalg import * #scipy.linalg

class Algorithms:
    
    def __init__(self):
        pass
    
    def getPointPolPosition(self, q:QPointF, pol:QPolygonF):
        #Point and polygon position, ray crossing algorithm
        k = 0
        n = len(pol)
        
        #Process all vertices of the polygon
        for i in range(n):
            #Reduce coordinates
            x_ir = pol[i].x() - q.x()
            y_ir = pol[i].y() - q.y()
            
            x_i1r = pol[(i+1)%n].x() - q.x()
            y_i1r = pol[(i+1)%n].y() - q.y()
            
            #Appropriate segment intersection the ray
            if (((y_i1r > 0) and (y_ir <= 0)) or ((y_ir > 0) and (y_i1r <= 0))):
                
                #Compute intersection coordinate
                xm = (x_i1r*y_ir - x_ir*y_i1r)/(y_i1r-y_ir)
                
                # Appropriate intersection, increment k
                if xm > 0:
                    k = k + 1
        
        #Inside          
        if k%2 == 1:
            return 1
        
        #Outside
        return 0
    
    
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
    
    
    def createCH(self, pol:QPolygonF):
        #Create Convex Hull using Jarvis Scan
        ch = QPolygonF()
        
        #Find pivot q (minimize y)
        q = min(pol, key = lambda k: k.y())

        #Find left-most point (minimize x)
        s = min(pol, key = lambda k: k.x())
        
        #Initial segment
        pj = q
        pj1 = QPointF(s.x(), q.y())
        
        #Add to CH
        ch.append(pj)
        
        # Find all points of CH
        while True:
            #Maximum and its index
            omega_max = 0
            index_max = -1
            
            #Browse all points
            for i in range(len(pol)):
                
                if pj != pol[i]:
                    
                    #Compute omega
                    omega = self.get2VectorsAngle(pj, pj1, pj, pol[i])
            
                    #Actualize maximum
                    if(omega>omega_max):
                        omega_max = omega
                        index_max = i
                    
            #Add point to the convex hull
            ch.append(pol[index_max])
            
            #Reasign points
            pj1 = pj
            pj = pol[index_max]
            
            # Stopping condition
            if pj == q:
                break
            
        return ch
    
    
    def createMMB(self, pol:list[QPolygonF]):
        # Create min max box and compute its area
        
        #Points with extreme coordinates        
        p_xmin = min(pol, key = lambda k: k.x())
        p_xmax = max(pol, key = lambda k: k.x())
        p_ymin = min(pol, key = lambda k: k.y())
        p_ymax = max(pol, key = lambda k: k.y())
        
        #Create vertices
        v1 = QPointF(p_xmin.x(), p_ymin.y())
        v2 = QPointF(p_xmax.x(), p_ymin.y())
        v3 = QPointF(p_xmax.x(), p_ymax.y())
        v4 = QPointF(p_xmin.x(), p_ymax.y())
        
        #Create new polygon
        mmb = QPolygonF([v1, v2, v3, v4])
        
        #Area of MMB
        area = (v2.x() - v1.x()) * (v3.y() - v2.y())
        
        return mmb, area
    
    def LH(self, pol:QPolygonF):
        #Compute polygon area using LH formula
        area = 0
        n = len(pol)
        
        #Compute area
        for i in range(n):
            area = area + pol[i].x() * (pol[(i + 1)%n].y() - pol[(i - 1 + n)%n].y())
            
        return abs(area)/2


    def rotatePolygon(self, pol:QPolygonF, sig:float):
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            # Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot


    def createMBR(self, pol: list[QPolygonF]):
        # Create minimum area enclosing rectangle
        mmb_r_list = []
        effi_list = []
        
        for j in pol:

            #Create convex hull
            ch = self.createCH(j)

            #Get minmax box, area and sigma
            mmb_min, area_min = self.createMMB(ch)
            sigma_min = 0

            # Process all segments of ch
            for i in range(len(ch)-1):
                # Compute sigma
                dx = ch[i+1].x() - ch[i].x()
                dy = ch[i+1].y() - ch[i].y()
                sigma = atan2(dy,dx)

                #Rotate convex hull by sigma
                ch_rot = self.rotatePolygon(ch, -sigma)

                #Find min-max box over rotated ch
                mmb, area = self.createMMB(ch_rot)

                #Actualize minimum area
                if area < area_min:
                    area_min = area
                    mmb_min = mmb
                    sigma_min = sigma

            #Rotate minmax box
            er = self.rotatePolygon(mmb_min, sigma_min)

            #Resize rectangle
            mmb_r = self.resizeRectangle(er, j)
            effi = self.efficiency(mmb_r, j)
            
            mmb_r_list.append(mmb_r)
            effi_list.append(effi)

        return mmb_r_list, effi_list


    def resizeRectangle(self, er: QPolygonF, pol:QPolygonF):
        #Building area
        Ab = abs(self.LH(pol))

        #Enclosing rectangle area
        A = abs(self.LH(er))

        # Fraction of Ab and A
        k = Ab/A

        #Center of mass
        x_t = (er[0].x() + er[1].x() + er[2].x() + er[3].x())/4
        y_t = (er[0].y() + er[1].y() + er[2].y() + er[3].y())/4

        #Vectors
        u1_x = er[0].x() - x_t
        u2_x = er[1].x() - x_t
        u3_x = er[2].x() - x_t
        u4_x = er[3].x() - x_t
        u1_y = er[0].y() - y_t
        u2_y = er[1].y() - y_t
        u3_y = er[2].y() - y_t
        u4_y = er[3].y() - y_t

        #Coordinates of new vertices
        v1_x = x_t + sqrt(k) * u1_x
        v1_y = y_t + sqrt(k) * u1_y

        v2_x = x_t + sqrt(k) * u2_x
        v2_y = y_t + sqrt(k) * u2_y

        v3_x = x_t + sqrt(k) * u3_x
        v3_y = y_t + sqrt(k) * u3_y

        v4_x = x_t + sqrt(k) * u4_x
        v4_y = y_t + sqrt(k) * u4_y

        #Create new vertices
        v1 = QPointF(v1_x, v1_y)
        v2 = QPointF(v2_x, v2_y)
        v3 = QPointF(v3_x, v3_y)
        v4 = QPointF(v4_x, v4_y)

        #Create rectangle
        er_r = QPolygonF([v1, v2, v3, v4])

        return er_r
    
    def createER_PCA(self, pol: QPolygonF):
        #create enclosing rectangle using PCA
        
        mmb_r_list = []
        effi_list = []
        
        for j in pol:
            
            x = []
            y = []
                    
            #add x,y coordinates to the list
            for p in j:
                x.append(p.x())
                y.append(p.y())
            
            #convert to matrix
            A = array([x,y])
            
            #covariance matrix
            C = cov(A)
                
            #singular value decomposition
            [U,S,V] = svd(C)
            
            #compute sigma
            sigma = atan2(V[0][1], V[0][0])
            
            #Rotate polygon
            pol_rot = self.rotatePolygon(j, -sigma)
            
            #Find min-max box over rotated polygon
            mmb, area = self.createMMB(pol_rot)
            
            #Rotate minmax box
            mmb_rot = self.rotatePolygon(mmb, sigma)

            #Resize rectangle
            mmb_r = self.resizeRectangle(mmb_rot, j)
            effi = self.efficiency(mmb_r, j)
            
            mmb_r_list.append(mmb_r)
            effi_list.append(effi)

        return mmb_r_list, effi_list

    def createER_LongestEdge(self, pol: QPolygonF):
        #create enclosing rectangle using Longest Edge
        
        mmb_r_list = []
        effi_list = []
        
        for j in pol:
            #find longest edge
            max_dist = 0
            
            for i in range(len(j)-1):
                # Compute distance and sigma
                dx = j[i+1].x() - j[i].x()
                dy = j[i+1].y() - j[i].y()
                d = sqrt(dx*dx+dy*dy)
                if (d>max_dist):
                    max_dist = d
                    sigma = atan2(dy,dx)
        
            #Rotate polygon
            pol_rot = self.rotatePolygon(j, -sigma)
            
            #Find min-max box over rotated polygon
            mmb, area = self.createMMB(pol_rot)
            
            #Rotate minmax box
            mmb_rot = self.rotatePolygon(mmb, sigma)

            #Resize rectangle
            mmb_r = self.resizeRectangle(mmb_rot, j)
            effi = self.efficiency(mmb_r, j)
            
            mmb_r_list.append(mmb_r)
            effi_list.append(effi)

        return mmb_r_list, effi_list
    
    def createER_WallAverage(self, pol: QPolygonF):
        #create enclosing rectangle using Wall Average
        
        mmb_r_list = []
        effi_list = []
        
        for j in pol:
            
            #compute sigma
            n = len(j)
            sumaA = 0
            sumaB = 0
            for i in range(n):
                #condition replacing modulo
                if (i != (n-1) and i != 0):      
                    a = i
                    b = i+1
                    c = i-1
                elif (i==0): #connection between the first and the last point of the polygon
                    a = i
                    b = i+1
                    c = n-1
                else: #connection between the last and the first point of the polygon
                    a = i
                    b = 0
                    c = i-1
                    
                # Compute distance and sigmas        
                dx1 = j[c].x() - j[a].x()
                dy1 = j[c].y() - j[a].y()
                sigma1 = atan2(dy1,dx1)
                
                dx2 = j[b].x() - j[a].x()
                dy2 = j[b].y() - j[a].y()
                sigma2 = atan2(dy2,dx2)
                d = sqrt(dx2*dx2+dy2*dy2)
                
                #compute w
                w = sigma1-sigma2
                
                #compute residua
                k = 2*w/pi
                r = (k-floor(k))*(pi/2)
                if (w%(pi/2)<(pi/4)):
                    r = r
                else:
                    r = pi/2 - r
                                        
                sumaA = sumaA+r*d
                sumaB = sumaB+d
            
            #sigma12
            dx = j[1].x() - j[0].x()
            dy = j[1].y() - j[0].y()
            sigma12 = atan2(dy,dx)    
                
            #final sigma
            sigma = sigma12 + sumaA/sumaB
        
            #Rotate polygon
            pol_rot = self.rotatePolygon(j, -sigma)
            
            #Find min-max box over rotated polygon
            mmb, area = self.createMMB(pol_rot)
            
            #Rotate minmax box
            mmb_rot = self.rotatePolygon(mmb, sigma)

            #Resize rectangle
            mmb_r = self.resizeRectangle(mmb_rot, j)
            effi = self.efficiency(mmb_r, j)
            
            mmb_r_list.append(mmb_r)
            effi_list.append(effi)

        return mmb_r_list, effi_list
    
    def createER_WeightedBisector(self, pol: QPolygonF):
        #create enclosing rectangle using weighted bisector
        
        mmb_r_list = []
        effi_list = []
        
        for k in pol:
            
            #find 2 longest diagonalls
            max_diag_1 = 0
            max_diag_2 = 0
            i_h1 = j_h1 = i_h2 = j_h2 = -1
            x1i = x1j = y1i = y1j = x2i = x2j = y2i = y2j = 0
            
            for i in range(len(k)):
                for j in range(len(k)):
                    if (i==i_h1 and j==j_h1):
                        continue
                    
                    # Compute diagonals
                    dx = k[j].x() - k[i].x()
                    dy = k[j].y() - k[i].y()
                    d = sqrt(dx*dx+dy*dy)
                    if (d>max_diag_1):
                        max_diag_1 = d
                        x1i = k[i].x()
                        y1i = k[i].y()
                        x1j = k[j].x()
                        y1j = k[j].y()
                        i_h1 = j
                        j_h1 = i

            i_h2 = j_h2 = -1
            for i in range(len(k)):
                for j in range(len(k)):
                    if (i==i_h2 and j==j_h2 or i==i_h1 or i==j_h1 or j==i_h1 or j==j_h1):
                        continue
                    
                    # Compute diagonals
                    dx = k[j].x() - k[i].x()
                    dy = k[j].y() - k[i].y()
                    d = sqrt(dx*dx+dy*dy)
                    if (d>max_diag_2):
                        max_diag_2 = d
                        x2i = k[i].x()
                        y2i = k[i].y()
                        x2j = k[j].x()
                        y2j = k[j].y()
                        i_h2 = j
                        j_h2 = i
            
            
            
            x = ((x1i*y1j-y1i*x1j)*(x2i-x2j)-(x1i-x1j)*(x2i*y2j-y2i*x2j)) / ((x1i-x1j)*(y2i-y2j)-(y1i-y1j)*(x2i-x2j)) 
            y = ((x1i*y1j-y1i*x1j)*(y2i-y2j)-(y1i-y1j)*(x2i*y2j-y2i*x2j)) / ((x1i-x1j)*(y2i-y2j)-(y1i-y1j)*(x2i-x2j))

            
            #compute sigmas          
            dx1 = x1i-x
            dy1 = y1i-y  
            dx2 = x2i-x
            dy2 = y2i-y      
            sigma1 = atan2(dy1,dx1)
            if (sigma1<0):
                sigma1 = sigma1+pi
            sigma2 = atan2(dy2,dx2)
            if (sigma2<0):
                sigma2 = sigma2+pi
            #sigma
            sigma = (sigma1*max_diag_1+sigma2*max_diag_2)/(max_diag_1+max_diag_2)
        
            #Rotate polygon
            pol_rot = self.rotatePolygon(k, -sigma)
            
            #Find min-max box over rotated polygon
            mmb, area = self.createMMB(pol_rot)
            
            #Rotate minmax box
            mmb_rot = self.rotatePolygon(mmb, sigma)

            #Resize rectangle
            mmb_r = self.resizeRectangle(mmb_rot, k)
            effi = self.efficiency(mmb_r, k)
            
            mmb_r_list.append(mmb_r)
            effi_list.append(effi)

        return mmb_r_list, effi_list 
    
    def efficiency (self, mbr: QPolygonF, pol: QPolygonF):
        #computing efficiency of aproximation
        
        #compute main sigma of mbr
        d1 = sqrt((mbr[0].x()-mbr[1].x())**2 + (mbr[0].y()-mbr[1].y())**2)
        d2 = sqrt((mbr[1].x()-mbr[2].x())**2 + (mbr[1].y()-mbr[2].y())**2)
        if (d1>d2):
            sigma_mbr = atan2((mbr[0].y()-mbr[1].y()),(mbr[0].x()-mbr[1].x()))
        else:
            sigma_mbr = atan2((mbr[1].y()-mbr[2].y()),(mbr[1].x()-mbr[2].x()))
            
        #compute r of mbr
        k_mbr = 2*sigma_mbr/pi
        r_mbr = (k_mbr-floor(k_mbr))*(pi/2)
           
        #compute suma of residuas         
        suma = 0
        n = len(pol)
        for i in range(n):
            #condition replacing modulo
            if (i != (n-1) and i != 0):      
                a = i
                b = i+1
                c = i-1
            elif (i==0): #connection between the first and the last point of the polygon
                a = i
                b = i+1
                c = n-1
            else: #connection between the last and the first point of the polygon
                a = i
                b = 0
                c = i-1
                
            #sigma
            sigma = atan2((pol[b].y()-pol[a].y()),(pol[b].x()-pol[a].x()))
            
            #r
            k = 2*sigma/pi
            r = (k-floor(k))*(pi/2)
            
            #suma of residuas
            suma = suma + (r-r_mbr)**2
        
        dsigma = (pi/(2*len(pol))*sqrt(suma))*(180/pi) #in degrees
        return dsigma