from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Plot:
    ''' Class to generate plotly graph
    '''

    def ssa(self, file_data, surr_data, *, num_comp, title, is_jupyter=False):
        ''' Plot generated surrogate data
    
        if the method is run on jupyter notebook (set is_jupyter to 'True'),\
        this method will not return any value. Otherwise, it will return Figure() object.
        '''


        # colour of the graphs
        ori_colour = '#636efa'
        ori2_colour = '#b3cde3'
        surr_colour = '#00cc96'

        fig = make_subplots(
            rows=num_comp, cols=2,
            subplot_titles=("Original", "Surrogate"),
            vertical_spacing=0.10,
            )

        x_coor = [x for x in range(file_data.shape[1])]

        show_legend = True
        ori_str = "Original"
        surr_str ="Surrogate"
        for i in range (num_comp):
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
                title_text=title + " SSA plot", 
                height=100 + 250 * num_comp, 
                width=900,
                )
            fig.show()

        else:
            fig.update_layout(
                title_text=title + " SSA plot", 
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    # pad = 4
                ),
                showlegend=False)

            return fig # send fig variable to be displayed on windowed mode
        

            

    def reconstructed(self, file_data, R, *, num_comp, title, is_jupyter=False, signal_no=5):
        ''' Plot reconstructed signals
    
        if the method is run on jupyter notebook (set is_jupyter to 'True'),\
        this method will not return any value. Otherwise, it will return Figure() object.

        R = Reconstructed signal (2D matrix)
        signal_amount = no. of reconstructed signal to be plotted
        '''
        

        # colour of the graphs
        ori_colour = '#636efa'
        plot_colour = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', \
                        '#0099c6', '#dd4477', '#66aa00', '#b82e2e', '#316395']

        fig = make_subplots(
            rows=num_comp, cols=2,
            subplot_titles=("Original", "Reconstructed"),
            vertical_spacing=0.10)

        x_coor = [x for x in range(file_data.shape[1])]

        show_legend = False
        ori_str = "Original"
        r_str ="Reconstructed"


        for i in range(num_comp):
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
        for i in range(num_comp):
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
                
                # add line annotation
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
                    title_text=title + " SSA plot", 
                    height=100 + 250 * num_comp, 
                    width=900,
                    )
                fig.show()

        else:
            fig.update_layout(
                title_text=title + " SSA plot", 
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    # pad = 4
                ),
                showlegend=False)

            return fig # send fig variable to be displayed on windowed mode