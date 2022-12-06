
# TKinter - find the path of a screen's assets
def center_window_on_screen(window, width, height):
    screen_width = window.winfo_screenwidth()  # Width of the screen
    screen_height = window.winfo_screenheight()  # Height of the screen

    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    #window.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))

    position = f"{width}x{height}+{x_cord}+{y_cord}"

    return position



# TKinter
def relative_to_assets(asset_dir, asset_name):
    import os

    utils_path = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.abspath(
        os.path.join(utils_path, os.pardir, "assets", asset_dir, asset_name))



def plotly_gen(file_data, surr_data, *, numComp, file_name, is_jupyter=False):
    ''' Plot generated surrogate data
    
    if the method is run on jupyter notebook (set is_jupyter to 'True'), 
    it will not return any value, Otherwise, it will return Figure() object.
    '''
    # visualization
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # colour of the graphs
    ori_colour = '#636efa'
    ori2_colour = '#b3cde3'
    surr_colour = '#00cc96'

    fig = make_subplots(
        rows=numComp, cols=2,
        subplot_titles=("Original", "Surrogate"),
        vertical_spacing=0.10,
        )

    x_coor = [x for x in range(file_data.shape[1])]

    show_legend = True
    ori_str = "Original"
    surr_str ="Surrogate"
    for i in range (numComp):
        if i != 0: 
            show_legend = False
            ori_str = "Original " + str(i+1)
            surr_str = "Surrogate " + str(i+1)

        # original
        fig.add_trace(
            go.Scatter(
                x=x_coor, y=file_data[i,:], name=ori_str, 
                line=dict(color=ori_colour), showlegend=show_legend),
            row=i+1, col=1)
        
        # original + surrogate
        fig.add_trace(
            go.Scatter(
                x=x_coor, y=file_data[i,:], name=ori_str,
                line=dict(color=ori2_colour), showlegend=False),
            row=i+1, col=2)

        fig.add_trace(
            go.Scatter(
                x=x_coor, y=surr_data[i,:], name=surr_str,
                line=dict(color=surr_colour), showlegend=show_legend,
                mode="lines+markers",
                marker=dict(
                    symbol="circle",
                    size=4)),
            row=i+1, col=2)
        
        # fig.update_xaxes(title_text="Time", row=i+1, col=1)
        # fig.update_xaxes(title_text="Time", row=i+1, col=2)
        # fig.update_yaxes(title_text=f"Amp axis {i+1}", row=i+1, col=1)
        # fig.update_yaxes(title_text=f"Amp axis {i+1}", row=i+1, col=2)
        

    if is_jupyter:
        # Update title and height
        fig.update_layout(
            title_text=file_name + " SSA plot", 
            height=100 + 250 * numComp, 
            width=900,
            )
        fig.show()

    else:
        fig.update_layout(
            title_text=file_name + " SSA plot", 
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
                # pad = 4
            ),
            showlegend=False)

        return fig # send fig variable to be displayed on windowed mode



def plotly_reconstructed(file_data, R, *, numComp, file_name, is_jupyter=False, signal_no=5):
    ''' Plot reconstructed signals
    
    if the method is run on jupyter notebook (set is_jupyter to 'True'), 
    it will not return any value, Otherwise, it will return Figure() object.
    '''
    
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # colour of the graphs
    ori_colour = '#636efa'
    plot_colour = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', \
                    '#0099c6', '#dd4477', '#66aa00', '#b82e2e', '#316395']

    fig = make_subplots(
        rows=numComp, cols=2,
        subplot_titles=("Original", "Reconstructed"),
        vertical_spacing=0.10)

    x_coor = [x for x in range(file_data.shape[1])]

    show_legend = False
    ori_str = "Original"
    r_str ="Reconstructed"


    for i in range(numComp):
        if i != 0: 
            show_legend = False
            ori_str = "Original " + str(i+1)

        # original
        fig.add_trace(
            go.Scatter(
                x=x_coor, y=file_data[i,:], name=ori_str, 
                line=dict(color=ori_colour), showlegend=show_legend),
            row=i+1, col=1)


    show_legend = False
    for i in range(numComp):
        colour_iter = 0
        for j in range(signal_no):
            # set name of each plot line
            if i != 0: 
                show_legend = False
                r_str = "Reconstructed " + str(i+1)
            
            # set colour
            colour = plot_colour[colour_iter]
            colour_iter += 1
            if colour_iter == len(plot_colour): colour_iter = 0
            
            # original
            fig.add_trace(
                go.Scatter(
                    x=x_coor, y=R[i,:,j],
                    name=r_str,
                    line=dict(color=colour),
                    showlegend=show_legend,
                ),
                row=i+1, col=2)
            
            # fig.add_annotation(
            #     x=x_coor[-1], y=R[i,-1,j],
            #     text=str(j),
            #     showarrow=False,
            #     yshift=10,
            #     xshift=10,
            #     row=i+1,col=2)


    if is_jupyter:
            # Update title and height
            fig.update_layout(
                title_text=file_name + " SSA plot", 
                height=100 + 250 * numComp, 
                width=900,
                )
            fig.show()

    else:
        fig.update_layout(
            title_text=file_name + " SSA plot", 
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
                # pad = 4
            ),
            showlegend=False)

        return fig # send fig variable to be displayed on windowed mode

