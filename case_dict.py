def return_case_df():
    import pandas as pd
    case_dicts = [ 

        # x = 0 ###############################################################
        {
            'file':              'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Straight edge',
            'type':              'surface',
            'height_correction': 0.1,
            'rotation':          0.0,
            'x_loc':             0,
            'x_corr':            -2.5,
            'y_trust_min':       1.0,
            'Cf':                0.00113,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.5,
            'rotation':          0.0,
            'x_loc':             0,
            'y_trust_min':       0,
            'x_corr':            0,
            'Cf':                0.00113,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          0.0,
            'x_loc':             0,
            'x_corr':            0,
            'y_trust_min':       0,
            'Cf':                0.00113,
        },
        {
            'file':              \
            'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.5$',
            'type':              'surface',
            'height_correction': -0.2,
            'rotation':          0.0,
            'x_loc':             0,
            'x_corr':            0,
            'y_trust_min':       1.0,
            'Cf':                0.00113,
        },

        # x = -2.0 ############################################################
        {
            'file':              'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Straight edge',
            'type':              'surface',
            'height_correction': 0.1,
            'rotation':          -8.0,
            'x_loc':             -2.0,
            'x_corr':            -2.5,
            'y_trust_min':       1.0,
            'Cf':                0.00113,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.5,
            'rotation':          -8.0,
            'x_loc':             -2.0,
            'x_corr':            0,
            'y_trust_min':       1.0,
            'Cf':                0.00113,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          -8.0,
            'x_loc':             -2.0,
            'x_corr':            0,
            'y_trust_min':       0.5,
            'Cf':                0.00113,
        },
        {
            'file':              \
            'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.5$',
            'type':              'surface',
            'height_correction': 1.0,
            'rotation':          -8.0,
            'x_loc':             -2.0,
            'x_corr':            0,
            'y_trust_min':       1.0,
            'Cf':                0.00113,
        },

        # x = 10.0 ############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.3,
            'rotation':          -2.0,
            'x_loc':             10.0,
            'x_corr':            0,
            'y_trust_min':       0.3,
            'Cf':                0.0020,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          -3.0,
            'x_loc':             10.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0020,
        },


        # x = 8.0 #############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.3,
            'rotation':          -2.0,
            'x_loc':             8.0,
            'x_corr':            0,
            'y_trust_min':       0.3,
            'Cf':                0.0020,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          -3.0,
            'x_loc':             8.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0020,
        },

        # x = 20.0 ############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.1,
            'rotation':          -2.0,
            'x_loc':             20.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0024,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          -3.0,
            'x_loc':             20.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0024,
        },

        # x = 18.0 ############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': 0.1,
            'rotation':          -2.0,
            'x_loc':             18.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0024,
        },
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0.25$',
            'type':              'surface',
            'height_correction': 0.0,
            'rotation':          -3.0,
            'x_loc':             18.0,
            'x_corr':            0,
            'y_trust_min':       0.0,
            'Cf':                0.0024,
        },

        # x = 40.0 ############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': -0.3,
            'rotation':          -2.0,
            'x_loc':             40.0,
            'x_corr':            0,
            'y_trust_min':       0.4,
            'Cf':                0.0030,
        },
        # x = 38.0 ############################################################
        {
            'file':              'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
            'case_name':         'Serrated, $z/\\lambda = 0$',
            'type':              'surface',
            'height_correction': -0.3,
            'rotation':          -2.0,
            'x_loc':             38.0,
            'x_corr':            0,
            'y_trust_min':       0.4,
            'Cf':                0.0030,
        },

    ]

    for c in case_dicts:
        if c == case_dicts[0]:
            df = pd.DataFrame( data = c , index = [0])
        else:
            df = df.append( pd.DataFrame( data = c , index = [0]), 
                           ignore_index=True )
    return df
