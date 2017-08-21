import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from datetime import datetime

def convertCoords(row):
    
    """ This Converts lat and long values into a UTM 29 North values"""
    
    inProj = pyproj.Proj(init='epsg:4326')
    outProj = pyproj.Proj(init='epsg:32629')
    UTM29N_lon,UTM29N_lat = pyproj.transform(inProj,outProj,row['lon'],row['lat'])
    UTM29N = {
        'UTM29N_lon' : UTM29N_lon,
        'UTM29N_lat' : UTM29N_lat
    }
    
    return UTM29N  #pd.Series({'UTM29N_lon':x2,'UTM29N_lat':y2})

def utm_of_the_polar_data(UTM29N, distance, columns, rows):
    
    """ This takes the UTM29N values of the radar, the distance the radar covers, and the quantity of rows and columns for the whole rotation 
        This returns a dictionary that holds the UTM29N values for the whole rotation     
    """

    full_angle = np.pi * 2
    full_distance = distance # meters (3.07km)
    
    total_columns = columns
    total_rows = rows    
    single_cell_angle = full_angle/total_columns
    single_cell_distance = full_distance/total_rows
    
    x_opp = []
    y_adj = []
    for x in range(total_columns):      
        for y in range(total_rows):                     
            x_opp.append( UTM29N['UTM29N_lat']   + ( np.sin(single_cell_angle*x) * single_cell_distance*(y)) ) #
            y_adj.append( UTM29N['UTM29N_lon'] + ( np.cos(single_cell_angle*x) * single_cell_distance*(y)) )   
    
   
    x_opp = np.reshape(x_opp, (columns, rows))
    y_adj = np.reshape(y_adj, (columns, rows))
    
    xopp_and_yadj = { 'x_opp' : x_opp, 'y_adj' : y_adj}
    
    return xopp_and_yadj


def mkiv_utm29n_values(angular_position_range, distance_position_range, xopp_and_yadj):
    
    """This takes a dictionary that contains the whole rotational utm29n values and extracts the utm29n values of the mkiv using the angular,
    and distance position range of the mkiv"""
    
    x_opp_df = pd.DataFrame(xopp_and_yadj['x_opp'])
    y_adj_df = pd.DataFrame(xopp_and_yadj['y_adj'])
    mkiv_x_opp_df = x_opp_df.iloc[angular_position_range,distance_position_range]
    mkiv_y_adj_df = y_adj_df.iloc[angular_position_range,distance_position_range]
    
    mkiv_xopp_and_yadj_utm29n = {'mkiv_x_opp_df' : mkiv_x_opp_df, 'mkiv_y_adj_df': mkiv_y_adj_df}
    return mkiv_xopp_and_yadj_utm29n