from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from shapely import geometry
from fiona import *
from statistics import *
from algorithms import *
from QPoint3DF import *

class IO:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create qt dialog
        self.dia = QFileDialog()
        self.dia.setNameFilter("Shapefile (*.shp)")
        
        
    def loadData(self, w, h):
        
        #Load data
        if self.dia.exec():
            fileNames = self.dia.selectedFiles()
            geometries = []
            #Set data from shapefile to shapely
            with open(fileNames[0]) as shapefile:
                for record in shapefile:
                    geom = geometry.shape(record['geometry'])
                    geometries.append(geom)
                    

            #Polygons from shapely to QPolygonF
            qpointx = []
            qpointy = []
            qpointz = []
            for point in geometries:
                qpointx.append(point.x)
                qpointy.append(point.y)
                qpointz.append(point.z)

            
            #Conversion
            all_points_x = []
            all_points_y = []
            min_x_pols = float('inf')
            min_y_pols = float('inf')
            max_x_pols = float('-inf')
            max_y_pols = float('-inf') 
            
            for i in range(len(qpointx)):
                # actualize minimum and maximum values
                x = qpointx[i]
                y = qpointy[i]
                all_points_x.append(x)
                all_points_y.append(y)
                min_x_pols = min(min_x_pols, x)
                min_y_pols = min(min_y_pols, y)
                max_x_pols = max(max_x_pols, x)
                max_y_pols = max(max_y_pols, y)

            #Size of polygons
            W = max_x_pols - min_x_pols
            H = max_y_pols - min_y_pols
            
            #Scale factor
            scalew = w/W
            scaleh = h/H
            s = min(scalew, scaleh) - 0.2
            
            #Translation
            center_X = mean(all_points_x)
            center_Y = mean(all_points_y)
            
            center_X = center_X*s
            center_Y = center_Y*s        
            
            center_x = w/2
            center_y = h/2
            
            trans_x = center_X - center_x
            trans_y = center_Y - center_y
            
            #Transformation of points and creating polygons
            points_finale = []
            for i in range(len(qpointx)):                
                x = qpointx[i]*s - trans_x
                y = qpointy[i]*s - trans_y   
                
                point = QPoint3DF(x, y, qpointz[i])
                points_finale.append(point) 

            #Return list of polygon
            return points_finale
            