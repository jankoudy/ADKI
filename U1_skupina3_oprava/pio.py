from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from shapely.geometry import shape
from fiona import *
from statistics import *
from algorithms import *

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
                    geom = shape(record['geometry'])
                    geometries.append(geom)

            #Polygons from shapely to QPolygonF
            polygons = []
            for pol in geometries:
                qpolygon = QPolygonF()
                for point in pol.exterior.coords:
                    qpolygon.append(QPointF(point[0], point[1]*(-1)))
                polygons.append(qpolygon)

            
            #Conversion
            all_points_x = []
            all_points_y = []
            min_x_pols = float('inf')
            min_y_pols = float('inf')
            max_x_pols = float('-inf')
            max_y_pols = float('-inf') 
            
            for pol in polygons:
                # actualize minimum and maximum values
                for point in pol:
                    x = point.x()
                    y = point.y()
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
            s = min(scalew, scaleh)
            
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
            polygons_finale = []
            for pol in polygons:
                polygon = QPolygonF()
                points = []
                for point in pol:
                    x = point.x()*s - trans_x
                    y = point.y()*s - trans_y   
                    
                    if x not in points:
                        points.append(x) 
      
                        point2 = QPointF(x,y)

                        polygon.append(point2)

                polygons_finale.append(polygon)


            #Return list of polygon
            return polygons_finale