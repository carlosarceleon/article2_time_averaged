def NACA0018_trailing_edge_profile():
    from numpy import array

    upper_side_surface_x = [
        0       ,
        -0.144  ,
        -0.4022 ,
        -0.7296 ,
        -1.109  ,
        -1.53   ,
        -1.985  ,
        -2.4684 ,
        -2.9754 ,
        -3.5022 ,
        -4.0452 ,
        -4.6018 ,
        -5.1692 ,
        -5.745  ,
        -6.327  ,
        -6.9132 ,
        -7.5016 ,
        -8.0906 ,
        -8.6786 ,
    ]

    upper_side_surface_y = [0.0378 ,
                            0.068  ,
                            0.1214 ,
                            0.188  ,
                            0.2636 ,
                            0.3454 ,
                            0.4316 ,
                            0.5206 ,
                            0.6114 ,
                            0.703  ,
                            0.7944 ,
                            0.8852 ,
                            0.9744 ,
                            1.0616 ,
                            1.1464 ,
                            1.228  ,
                            1.306  ,
                            1.3802 ,
                            1.4496 ,
                           ]

    return array([upper_side_surface_x[::-1], upper_side_surface_y[::-1]])



def rename_df_columns_from_DaVis_to_standard(df):
    DaVis_naming_dict= {
          "x"                            : "x",
          "y"                            : "y",
          "Avg_Vx"                       : "u",
          "Avg_Vy"                       : "v",
          "Avg_Vz"                       : "w",
          "Length_of_Avg_V"                 : "Length of Avg V",
          "RMS_Vx"                       : "u_rms",
          "RMS_Vy"                       : "v_rms",
          "RMS_Vz"                       : "w_rms",
          "Length_of_Standard_deviation_of_V" : "Length of RMS V",
          "Reynold_stress_XY"            : "Reynold_stress_uv",
          "Reynold_stress_XZ"            : "Reynold_stress_uw",
          "Reynold_stress_YZ"            : "Reynold_stress_vw",
          "Reynold_stress_XX"            : "Reynold_stress_uu",
          "Reynold_stress_YY"            : "Reynold_stress_vv",
          "Reynold_stress_ZZ"            : "Reynold_stress_ww",
          }

    df.columns = [
        DaVis_naming_dict[col] for col in df.columns
    ]

    return df

def find_nearest(to_point,from_array):
   """ Finds the nearest available value in a array to a given value

   Inputs:
      to_point: value to find the nearest to in the array
      from_array: array of available values of which the nearest has to be 
      found
   Returns:
      The nearest value found in the array
      The difference between the requested and available closest value 
      in the array
   """
   from numpy import ones,argmin
   deltas = ones(len(from_array))*1000
   for v,i in zip(from_array,range(len(from_array))):
      deltas[i] = abs(to_point - v)

   return from_array[argmin(deltas)]

def regrid_df(df,variables,resolution=[0]):
    import numpy as np
    from scipy.interpolate import griddata
    import pandas as pd

    string_columns = df.select_dtypes(include=['object'])

    if not len(resolution)==2:
        grid_y, grid_x = np.mgrid[
                    int(df['y'].min()):int(df['y'].max()):0.1,
                    int(df['x'].min()):int(df['x'].max()):0.1,
                    ]
    else:
        grid_y, grid_x = np.mgrid[
                    int(df['y'].min())-1:int(df['y'].max()+1):resolution[1]*1j,
                    int(df['x'].min())-1:int(df['x'].max()+1):resolution[0]*1j,
                    ]
    df_interpolated = pd.DataFrame({
            'x' : grid_x.ravel(),
            'y' : grid_y.ravel(),
            })
    
    for v in variables:
        grid_var = griddata(
                (df['x'].values,df['y'].values), 
                df[v].values, 
                (grid_x,grid_y),
                method='cubic'
                )
        df_interpolated[v] = grid_var.ravel()


    # Re-center the array to the TE location at (0,0)
    df_interpolated.y = df_interpolated.y - \
            find_nearest(0,df_interpolated.y.values)
    df_interpolated.x = df_interpolated.x - \
            find_nearest(0,df_interpolated.x.values)

    for col in string_columns.columns:
        df_interpolated[col] = df[col].unique()[0]

    df_interpolated.fillna(0)

    return df_interpolated

def rotate_polygon(polygon,theta):
    """Rotates the given polygon which consists of corners 
    represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees
    
    """
    
    import math
    from numpy import array
    theta = math.radians(-theta)
    rotatedPolygon = []

    for corner in polygon.T :
        rotatedPolygon.append(
            ( 
                corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , 
                corner[0]*math.sin(theta)+corner[1]*math.cos(theta) 
            ) 
        )

    return array(rotatedPolygon).T

def mask_orientation_from_DaVis_to_standard(mask):
    from numpy import array

    mask_x_rot =  mask[1,:]
    mask_y_rot = -mask[0,:]

    return array([mask_x_rot , mask_y_rot])

def return_mask(case_name):
    from Masks import Masks as masks
    from numpy import array

    mask = array(masks[case_name])

    mask = mask - mask[1]
    mask = mask.T
    mask = mask_orientation_from_DaVis_to_standard(mask)

    return mask

def get_angle_between_points(point1, point2):
    from math import atan, pi, degrees

    delta_y = point2[1] - point1[1]
    delta_x = point2[0] - point1[0]
    if delta_x == 0:
        return pi

    return degrees(atan( delta_y / delta_x ))


def show_surface_from_pickle(pickle_file,variable='u'):

    df = load_df_from_pickle(pickle_file)
    show_surface_from_df(df,variable=variable)

def show_surface_from_df(df, variable=[], points = [], mask = []):
    import matplotlib.pyplot as plt
    from numpy import meshgrid,linspace

    if len(df.x.unique())>1000:
        df = regrid_df(df,variables=df.columns)

    X,Y = meshgrid( df.x.unique() , df.y.unique() )
    Z   = df[variable].reshape(X.shape)
    U   = df['u'].reshape(X.shape)
    V   = df['v'].reshape(X.shape)

    fig,axes = plt.subplots(1,1)

    if variable == 'flow_angle':
        df.flow_angle.fillna(90)
        levels = linspace(-15,15)
        cf = axes.contourf(X,Y,Z,levels=levels)

    else:
        cf = axes.contourf(X,Y,Z)

    stride = 20
    axes.quiver(
        X[::stride, ::stride],
        Y[::stride, ::stride],
        U[::stride, ::stride],
        V[::stride, ::stride],
        scale=300
    )

    if len(mask):
        axes.plot(mask[0,:],mask[1,:])

    if len(points):
        axes.scatter(points[0],points[1])

    plt.colorbar(cf)
    axes.set_aspect('equal')

    plt.show()
    plt.close(fig)

def show_streamlined_surface_from_df(df, variable='u', 
                                     points = [], mask = [],
                                     height_correction     = 0,
                                     streamwise_correction = 0,
                                     angle_correction      = 0,
                                     x_max                 = 0,
                                     x_min                 = 0,
                                     y_max                 = 0,
                                     y_min                 = 0,
                                     plot_name             = 'SurfacePlot.png',
                                     airfoil_rotate        = 0,
                                    ):
    import matplotlib.pyplot as plt
    from numpy import meshgrid,linspace,array,append
    from matplotlib import rc
    import seaborn as sns

    rc('text',usetex=True)
    rc('font',weight='normal')

    sns.set_context('paper')
    sns.set(font='serif',font_scale=1.6,style='whitegrid')
    rc('font',family='serif', serif='cm10')


    data_shape = (
        len(df[ (df.x >= x_min) & (df.x <= x_max) ].x.unique()),
        len(df[ (df.y >= y_min) & (df.y <= y_max) ].y.unique())
    )

    df = correct_flow_plane_df(
        df, 
        rotation_angle        = angle_correction,
        height_correction     = height_correction,
        streamwise_correction = streamwise_correction,
    )

    if x_min or x_max:
        df = df[ (df.x >= x_min) & (df.x <= x_max) ]
    if y_min or y_max:
        df = df[ (df.y >= y_min) & (df.y <= y_max) ]

    df = regrid_df(df,variables=list(set(['u','v',variable])),
                   resolution = data_shape)

    X,Y = meshgrid( df.x.unique() , df.y.unique() )
    Z   = df[variable].values.reshape(X.shape)
    U   = df['u'].values.reshape(X.shape)
    V   = df['v'].values.reshape(X.shape)

    fig,axes = plt.subplots(1,1)

    if variable == 'flow_angle':
        df.flow_angle.fillna(90)
        levels = linspace(-15,15)
        cf = axes.contourf(X,Y,Z,levels=levels)

    else:
        cf = axes.contourf(X,Y,Z,
                          cmap = plt.get_cmap('Reds'))

    if len(mask):
        axes.plot(mask[0,:],mask[1,:])

    if len(points):
        axes.scatter(points[0],points[1])

    axes.streamplot(
        X, Y, U, V, 
        density      = 0.5,
        zorder       = 1,
    )

    naca0018_profile = NACA0018_trailing_edge_profile()

    axes.fill_between(
        append(array(naca0018_profile[0]),[df.x.max()]),
        append(array(naca0018_profile[1]),[naca0018_profile[1][-1]]),
        array([df.y.min()]*(len(naca0018_profile[1])+1)),
        facecolor='k',
        zorder = 10
    )

    axes.set_xlabel('$x$ [mm]')
    axes.set_ylabel('$y$ [mm]')

    clb = plt.colorbar(cf)
    clb.set_label('$u$ [m/s]')

    axes.set_aspect('equal')

    if x_min or x_max:
        plt.xlim(x_min, x_max) 
    if y_min or y_max:
        plt.ylim(y_min, y_max)
    
    if not plot_name:
        plt.show()
    else:
        plt.savefig(plot_name,bbox_inches='tight')
    plt.close(fig)

def rotate_df(df,degrees = 0):
    from math import radians
    from numpy import sin, cos, sqrt
    import pandas as pd

    angle = radians(degrees)

    x = df['x'] 
    y = df['y'] 

    df_rotated = pd.DataFrame()

    df_rotated['x'] =  x*cos(angle) + y*sin(angle) 
    df_rotated['y'] = -x*sin(angle) + y*cos(angle) 

    # Velocity components
    df_rotated['u'] =  df['u']*cos(angle) \
            + df['v']*sin(angle)
    df_rotated['v'] = -df['u']*sin(angle) \
            + df['v']*cos(angle)
    df_rotated['w'] = df['w']

    # RMS components
    df_rotated['Reynold_stress_uu'] = \
            df['Reynold_stress_uu']*cos(angle)**2\
            + df['Reynold_stress_vv']*sin(angle)**2\
            + 2.*cos(angle)*sin(angle)*df['Reynold_stress_uv']

    df_rotated['Reynold_stress_vv'] = \
            df['Reynold_stress_uu']*sin(angle)**2\
            + df['Reynold_stress_vv']*cos(angle)**2\
            - 2.*cos(angle)*sin(angle)*df['Reynold_stress_uv']

    df_rotated['Reynold_stress_uv'] = \
            df['Reynold_stress_uv']*cos(2*angle) \
            + (cos(angle)*sin(angle)) \
            * ( df['Reynold_stress_uu']**2\
               * -df['Reynold_stress_vv']**2)

    df_rotated['u_rms'] = sqrt(
        df_rotated['Reynold_stress_uu'].fillna(0).values
    )
    df_rotated['v_rms'] = sqrt(
        df_rotated['Reynold_stress_vv'].fillna(0).values
    )
    df_rotated['u_rms'] = df_rotated['u_rms'].fillna(0)
    df_rotated['v_rms'] = df_rotated['v_rms'].fillna(0)

    ###

    for col in df.select_dtypes(include=['object']).columns:
        df_rotated[col] = df[col].unique()[0]

    return df_rotated

def decript_case_name(case_name):
    from re import findall

    trailing_edge = findall('[SrTE201R]+', case_name)[0]
    if trailing_edge == "STE" : trailing_edge = 'straight'
    if trailing_edge == "Sr20R21" : trailing_edge = 'serrated'

    phi   = findall('phi[0-9]',case_name)[0].replace('phi','')
    alpha = findall('alpha[0-9][0-9]?',case_name)[0].replace('alpha','')
    U     = findall('U[0-9][0-9]',case_name)[0].replace('U','')
    z     = findall('loc[0-9][0-9]',case_name)[0].replace('loc','')
    if   z == '00' : z = '0'
    elif z == '05' : z = '0.25'
    elif z == '10' : z = '0.5'

    return trailing_edge,phi,alpha,U,z

def load_df_from_pickle(pickle_file):
    from pandas import read_pickle
    import os

    df = read_pickle(pickle_file)

    df = rename_df_columns_from_DaVis_to_standard(df)

    df = df.fillna(value=0)
    
    df['case_name'] = os.path.split(pickle_file)[1]\
            .replace('_rotated.p','')

    trailing_edge, phi, alpha, U, z = decript_case_name(pickle_file)

    df['trailing_edge'] = trailing_edge
    df['phi']           = phi
    df['alpha']         = alpha
    df['U']             = U
    df['z']             = z

    return df

def correct_flow_plane_df( df, rotation_angle = 0, 
                          height_correction = 0, 
                          streamwise_correction = 0
                         ):
    # Do all the plane correcions ########################################
    if rotation_angle:
        df = rotate_df( df, rotation_angle )
    ######################################################################

    # Correct height and ignore below minimum trustable y ################
    df.y = df.y+height_correction
    ######################################################################

    # Correct streanwise translation #####################################
    df.x = df.x-streamwise_correction
    ######################################################################

    return df


def get_wall_normal_line(pickle_file, x_loc, 
                         variable                  = ['u'],
                         rotation_angle            = 0,
                         plot                      = False,
                         trust_y_min               = -100,
                         height_correction         = 0,
                         streamwise_correction     = 0
                        ):

    from numpy import diff,array,append,abs

    df = load_df_from_pickle(pickle_file)

    mask = return_mask(df.case_name.unique()[0])
    mask_rotation = get_angle_between_points(
        mask[:,1], mask[:,2]
    )
    mask = rotate_polygon(mask, rotation_angle+mask_rotation)

    data_shape = (
        len(df[df.y>0].x.unique()),len(df[df.y>0].y.unique())
    )

    df = correct_flow_plane_df(
        df, 
        rotation_angle, 
        height_correction, 
        streamwise_correction
    )

    # Put airfoil-wall-normal if x<0 #####################################
    if x_loc < 0:
        df = rotate_df( df, -11.4 )
    ######################################################################

    #df = df[df.y > trust_y_min]

    # Regrid to be able to get a vertical line ###########################
    df = regrid_df(
        df, 
        variables = list(set(['u','v']+variable)),
        resolution = data_shape
    )
    ######################################################################

    if plot:

        if x_loc < 0: airfoil_rotate = -11
        else: airfoil_rotate = 0
        show_streamlined_surface_from_df(
            df, 
            variable              = 'u',
            points                = [],
            mask                  = [],
            height_correction     = 0,
            streamwise_correction = 0,
            angle_correction      = 0,
            x_max                 = 6,
            x_min                 = -2,
            y_max                 = 15,
            y_min                 = -1,
            plot_name             = 0,
            airfoil_rotate        = airfoil_rotate
        )

    df = df[ df.x == find_nearest(x_loc, df.x.unique()) ]

    df = df.sort_values(by='y',ascending=True).reset_index(drop=True)

    df['u_rate_of_change'] = append(
        diff(df.u)/diff(df.y),
        array(diff(df.u)/diff(df.y))[-1]
    )

    # Cleaning filters ########################################
    df = df[ df.u > 0 ]
    df = df[ df.y > trust_y_min ]

    df_bool = (df.y>15) & (abs(df.u_rate_of_change)>0.1)
    df = df[~df_bool]

    df_bool = (df.y>15) & (df.u_rate_of_change<1e-2)
    df = df[~df_bool]

    df = df[~df.u_rate_of_change.isnull()]
    ###########################################################

    return df


def get_Reynolds_number(U, C = 0.2):
    rho = 1.193
    mu  = 1.813e-5

    return rho*U*C/mu


def get_averaged_data(df,n=50):
    import pandas as pd

    def moving_average(a, n) :
        from numpy import cumsum
        ret = cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    variables = df.columns
    new_df = pd.DataFrame(columns=variables)
    for v in variables:
        new_df[v] = moving_average(df[v].values,n=n)

    return new_df

def get_dimensionless_inner_variables(df,correction=0,Cf = 0):
    from math import sqrt,log10

    rho = 1.193
    mu  = 1.813e-5
    nu  = mu / rho
    
    U_inf = df.u.max()

    # Reynolds number
    Re = get_Reynolds_number( U = U_inf )
    if not Cf:
        # Friction coefficient, accordint to the 7th power law
        Cf = 0.074 / Re**0.2
        # Schlichting
        Cf = 0.455 / log10(Re)**2.58
        # XFOIL
        Cf = 0.00113
        # Self
        Cf = 0.00113
    # Wall shear, approximated
    tau_w = Cf * 0.5 * rho * U_inf**2
    # Wall shear velocity, approximated
    u_tau = sqrt( tau_w / rho )
    # Viscous length scale
    l_star = nu / u_tau
    
    df['y_plus'] = ( (df.y + correction) / 1000. ) / l_star
    df['u_plus'] = df.u / u_tau 

    return df

def get_flow_angle(df):
    from numpy import rad2deg, arctan

    df['flow_angle'] = rad2deg(arctan(df.v/df.u))

    return df

def write_to_csv_with_units(df,csv_file_name):
    column_dict = {
        'x'     : 'x [mm]',
        'y'     : 'y [mm]',
        'u'     : 'u [m/s]',
        'v'     : 'v [m/s]',
        "u_rms" : 'u_rms [m/s]',
        "v_rms" : 'v_rms [m/s]',
        "z"     : 'z [z/lambda]',
        "alpha" : 'alpha [deg]',
        "phi"   : 'phi [deg]',
        "U"     : 'U [m/s]',
    }

    new_columns = []
    for col in df.columns:
        if col in column_dict.keys():
            new_columns.append(column_dict[col])
        else:
            new_columns.append(col)

    df.columns = new_columns

    df.to_csv(csv_file_name)

