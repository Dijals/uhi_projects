import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from datetime import datetime

def convertCoords(dictionary):
    
    """ This Converts lat and long values into a UTM 29 North values"""
    
    inProj = pyproj.Proj(init='epsg:4326')
    outProj = pyproj.Proj(init='epsg:32629')
    UTM29N_lon,UTM29N_lat = pyproj.transform(inProj,outProj,dictionary['lon'],dictionary['lat'])
    UTM29N = {
        'UTM29N_lon' : UTM29N_lon,
        'UTM29N_lat' : UTM29N_lat
    }
    
    return UTM29N  #pd.Series({'UTM29N_lon':x2,'UTM29N_lat':y2})

def utm_of_the_polar_data(UTM29N, distance, columns, rows):
    
    """ 
        This takes the UTM29N values of the radar, the distance the radar covers, 
        and the quantity of rows and columns for the whole rotation. 
        
        This returns a dictionary that holds the UTM29N values for the whole rotation, 
        and a Scatter Plot that shows the rotations and its UTM 29 North 
        values. 
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
    
    plt.figure("fig3")
    plt.scatter(xopp_and_yadj['x_opp'], xopp_and_yadj['y_adj'])
    plt.show()
    
    return xopp_and_yadj


def mk_utm29n_values(angular_position_range, distance_position_range, xopp_and_yadj):
    
    """
    This takes a dictionary that contains the whole rotational utm29n values 
    and extracts the utm29n values of the mkiv using the angular,
    and distance position range of the mkiv
    
    This returns a dic with the mkiv or mkiii's UTM29N x and y positions in the 
    radar and shows the scatter plot
    """
    
    x_opp_df = pd.DataFrame(xopp_and_yadj['x_opp'])
    y_adj_df = pd.DataFrame(xopp_and_yadj['y_adj'])
    mk_x_opp_df = x_opp_df.iloc[angular_position_range,distance_position_range]
    mk_y_adj_df = y_adj_df.iloc[angular_position_range,distance_position_range]
    
    mk_xopp_and_yadj_utm29n = {'mk_x_opp_df' : mk_x_opp_df, 'mk_y_adj_df': mk_y_adj_df}
    
    plt.figure("fig3")
    plt.scatter(mk_xopp_and_yadj_utm29n['mk_x_opp_df'], mk_xopp_and_yadj_utm29n['mk_y_adj_df'])
    plt.show()
    
    return mk_xopp_and_yadj_utm29n

