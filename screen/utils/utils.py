
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
    it will not return any value, Otherwise, it will return Figure() object 
    to be displayed on windowed mode
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
        vertical_spacing=0.10)

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
        

    if is_jupyter:
        # Update title and height
        fig.update_layout(
            title_text=file_name + " SSA plot", 
            height=700, 
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


