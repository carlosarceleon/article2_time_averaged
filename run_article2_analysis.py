import case_dict_overall_correction as case_dict

cases_df = case_dict.return_case_df()
#markers = ['o', 'v',  's', 'p', '^', '<', '>', '8',
#                  '*', 'h', 'H', 'D', 'd']
markers = ['x','2','+','o','s']


#####################################################
#####################################################
# Analyze the boundary layer at the very trailing
# edge
#####################################################
#####################################################

def get_streamlined_surface(z_loc = 0):
    import article2_time_averaged_routines as tar

            
    pickle_files = [
        'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p',
        'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p',
        'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p',
        'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p',
    ]
    plot_names = [
        'SurfacePlot_u_Straight_edge.png',
        'SurfacePlot_u_Serrated_z00.png',
        'SurfacePlot_u_Serrated_z05.png',
        'SurfacePlot_u_Serrated_z10.png',
    ]

    for pf,pn in zip(
        pickle_files,plot_names
    ):
        df = tar.load_df_from_pickle(pf)

        height_correction = cases_df[ cases_df.file == pf ]\
                .height_correction.values[0]

        angle_correction = cases_df[ cases_df.file == pf ]\
                .rotation.values[0]
        
        streamwise_correction = cases_df[ cases_df.file == pf ]\
                .x_corr.values[0]


        tar.show_streamlined_surface_from_df(
            df                    = df,
            variable              = 'u',
            points                = [],
            mask                  = [],
            height_correction     = height_correction,
            angle_correction      = angle_correction,
            x_max                 = 40,
            x_min                 = -2,
            y_max                 = 6,
            y_min                 = -1,
            streamwise_correction = streamwise_correction,
            plot_name             = pn
        )

def write_wall_normal_lines_to_csv():
    import pandas as pd
    import article2_time_averaged_routines as tar

    case_STE = cases_df[ 
        (cases_df.file == 'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p') &\
        (cases_df.x_loc == 0) ]

    case_z00_x40 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p')&\
        (cases_df.x_loc == 40) ]
    
    case_z00_x20 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p')&\
        (cases_df.x_loc == 20) ]
    
    case_z00_x00 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p')&\
        (cases_df.x_loc == 0) ]
    
    case_z05 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p')&\
        (cases_df.x_loc == 20) ]

    case_z10 = cases_df[ 
        (cases_df.file == \
         'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p')&\
        (cases_df.x_loc == 0) ]

    cases = case_STE
    cases = cases.append(case_z00_x00)
    cases = cases.append(case_z00_x20)
    cases = cases.append(case_z00_x40)
    cases = cases.append(case_z05)
    cases = cases.append(case_z10)

    df_cases = pd.DataFrame()

    for case in cases.iterrows():

        df = tar.get_wall_normal_line(
            pickle_file               = case[1].file,
            x_loc                     = case[1].x_loc,
            variable                  = ['u','v',"u_rms","v_rms",],
            plot                      = False,
            rotation_angle            = case[1].rotation,
            trust_y_min               = case[1].y_trust_min,
            height_correction         = case[1].height_correction,
            streamwise_correction     = case[1].x_corr,
        )
        tar.write_to_csv_with_units(
            df, 
            '{0}_x{1:.2f}_z{2}'.format(
                df.trailing_edge.unique()[0],
                df.x.unique()[0],
                df.z.unique()[0],
            )
        )

        df_cases = df_cases.append(df, ignore_index = True)

    tar.write_to_csv_with_units(
        df_cases, 
        'Serrations_BoundaryLayerData_StereoPIV_v2.csv'
    )

def get_trailing_edge_for_all_cases_at_TE_m1():

    case_STE = cases_df[ 
        (cases_df.file == 'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p') &\
        (cases_df.x_loc == -1) ]
    case_z00 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p')&\
        (cases_df.x_loc == 39) ]
    case_z05 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p')&\
        (cases_df.x_loc == 19) ]
    case_z10 = cases_df[ 
        (cases_df.file == \
         'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p')&\
        (cases_df.x_loc == -1) ]

    cases = case_STE
    cases = cases.append(case_z00)
    cases = cases.append(case_z05)
    cases = cases.append(case_z10)

    plot_cases( cases , plot_name = "At_trailing_edge")

def get_trailing_edge_for_all_cases_at_x_m1():

    case_STE = cases_df[ 
        (cases_df.file == 'data/STE_phi0_alpha0_U20_loc00.dat_rotated.p') &\
        (cases_df.x_loc == -1) ]
    case_z00 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc00.dat_rotated.p')&\
        (cases_df.x_loc == -1) ]
    case_z05 = cases_df[ 
        (cases_df.file == 'data/Sr20R21_phi0_alpha0_U20_loc05.dat_rotated.p')&\
        (cases_df.x_loc == -1) ]
    case_z10 = cases_df[ 
        (cases_df.file == \
         'data/Sr20R21_phi0_alpha0_U20_loc10_Reprocessed.dat_rotated.p')&\
        (cases_df.x_loc == -1) ]

    cases = case_STE
    cases = cases.append(case_z00)
    cases = cases.append(case_z05)
    cases = cases.append(case_z10)

    plot_cases( cases , plot_name = "At_x_m1")

def plot_cases(cases,plot_name = ''):
    import article2_time_averaged_routines as tar
    import matplotlib.pyplot as plt
    from matplotlib import rc
    import seaborn as sns
    from numpy import linspace,log,diff
    import pandas as pd

    markeredgewidth = 1
    markerfacecolor = 'none'

    """ Cite
    Nagano1998
    Lee2008
    """

    rc('text',usetex=True)
    rc('font',weight='normal')

    sns.set_context('paper')
    sns.set(font='serif',font_scale=1.6,style='whitegrid')
    rc('font',family='serif', serif='cm10')

    fig_nondim   , axes_nondim   = plt.subplots(1,1,sharex=True,sharey=True)
    fig_u        , axes_u        = plt.subplots(1,1,sharex=True,sharey=True)
    fig_v        , axes_v        = plt.subplots(1,1,sharex=True,sharey=True)
    fig_diff     , axes_diff     = plt.subplots(1,1,sharex=True,sharey=True)
    fig_diff_rms , axes_diff_rms = plt.subplots(1,1,sharex=True,sharey=True)
    fig_u_rms    , axes_u_rms    = plt.subplots(1,1,sharex=True,sharey=True)
    fig_v_rms    , axes_v_rms    = plt.subplots(1,1,sharex=True,sharey=True)

    df_all_cases = pd.DataFrame()

    palette = sns.color_palette("colorblind", len(cases))

    for case,marker,color in zip(cases.iterrows(),markers,palette):
        print "Processing {0}".format(case[1].file)

        df = tar.get_wall_normal_line(
            pickle_file               = case[1].file,
            x_loc                     = case[1].x_loc,
            variable                  = ['u','v',"u_rms","v_rms",],
            plot                      = False,
            rotation_angle            = case[1].rotation,
            trust_y_min               = case[1].y_trust_min,
            height_correction         = case[1].height_correction,
            streamwise_correction     = case[1].x_corr,
        )


        df = tar.get_dimensionless_inner_variables(
            df,
            correction = 0,
            Cf = case[1].Cf,
            #correction = -3.6
        )
        axes_nondim.plot(
            df.y_plus,
            df.u_plus,
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )
        axes_u.plot(
            #df.u/20.,
            df.u/df.u.max(),
            df.y,
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )

        axes_u_rms.plot(
            df.u_rms/df.u.max(),
            df.y,
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )

        axes_v_rms.plot(
            df.v_rms/df.u.max(),
            df.y,
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )

        axes_diff.plot(
            df.y.values[0:-1],
            diff(df.u)/diff(df.y),
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )
        
        axes_diff_rms.plot(
            df.y.values[0:-1],
            diff(df.u_rms)/diff(df.y),
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )

        axes_v.plot(
            df.v/20.,
            df.y+case[1].rotation,
            label = case[1].case_name,
            marker = marker,
            markeredgewidth=markeredgewidth,
            markerfacecolor = markerfacecolor,
            markeredgecolor = color,
            color = color,
        )

        df_all_cases = df_all_cases.append(
            df,
            ignore_index=True
        )

    axes_nondim.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )

    # Plot u_plus = y_plus law
    line = axes_nondim.plot(
        linspace(1e0,1.2e1),
        linspace(1e0,1.2e1),
        '--'
    )
    # Plot u_plus = 1/0.4 * ln y_plus law
    axes_nondim.plot(
        linspace(8e0,1e3),
        log(linspace(8e0,1e3))/0.4+5,
        '--',
        color = line[0].get_color()
    )

    axes_nondim.set_xlabel("$y^+$")
    axes_nondim.set_ylabel("$u^+$")
    axes_nondim.set_xscale('log')
    axes_nondim.set_xlim(1e0, 1e3)
    axes_nondim.xaxis.grid(True, which='minor')

    axes_u.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )
    axes_v.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )
    axes_v_rms.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )
    axes_u_rms.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )
    axes_diff.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )
    axes_diff_rms.legend(
        bbox_to_anchor = (0., 1.02, 1.0, .102),
        loc            = 3,
        ncol           = 2,
        mode           = "expand",
        borderaxespad  = 0.
    )

    axes_u.set_xlabel("$u/U_\\infty$")
    axes_u.set_ylabel("$y$ [mm]")
    axes_u.set_xlim(0, 1)
    axes_v.set_xlabel("$v/U_\\infty$")
    axes_v.set_ylabel("$y$ [mm]")
    axes_u_rms.set_xlabel("$u'_\\textrm{rms}/U_\\infty$")
    axes_u_rms.set_ylabel("$y$ [mm]")
    axes_v_rms.set_xlabel("$v'_\\textrm{rms}/U_\\infty$")
    axes_v_rms.set_ylabel("$y$ [mm]")
    axes_diff.set_xlabel("$y$ [mm]")
    axes_diff.set_ylabel("$\\partial u/ \\partial y$")
    axes_diff.set_yscale("log")
    axes_diff_rms.set_xlabel("$y$ [mm]")
    axes_diff_rms.set_ylabel("$\\partial u'_\\textrm{rms}/ \\partial y$")

    axes_u.set_ylim(bottom = 0)
    axes_v.set_ylim(bottom = 0)
    axes_u_rms.set_ylim(bottom = 0)
    axes_v_rms.set_ylim(bottom = 0)
    axes_diff.set_xlim(left = 0)
    axes_diff_rms.set_xlim(left = 0)

    fig_u.savefig(
        'images/{0}_BoundaryLayerAnalysis_u.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_v.savefig(
        'images/{0}_BoundaryLayerAnalysis_v.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_u_rms.savefig(
        'images/{0}_BoundaryLayerAnalysis_urms.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_v_rms.savefig(
        'images/{0}_BoundaryLayerAnalysis_vrms.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_diff.savefig(
        'images/{0}_BoundaryLayerAnalysis_dudy.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_diff_rms.savefig(
        'images/{0}_BoundaryLayerAnalysis_durmsdy.png'.format(plot_name),
        bbox_inches='tight'
    )
    fig_nondim.savefig(
        'images/{0}_NonDimenaionalBoundaryLayerAnalysis_u.png'.format(plot_name),
        bbox_inches='tight'
    )
    tar.write_to_csv_with_units(
        df_all_cases,
        "{0}_BoundaryLayerData_StereoPIV.csv".format(plot_name),
    )

#get_streamlined_surface(z_loc = 0)
#get_trailing_edge_for_all_cases_at_TE_m1()
write_wall_normal_lines_to_csv()
#get_trailing_edge_for_all_cases_at_x_m1()
