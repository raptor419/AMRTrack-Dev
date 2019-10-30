from dashboard.forms import *
# Models
from dashboard.models import *
from .biotable import *
from .googlelogin import *
from .viewmethods import *

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
from bokeh.layouts import layout, row
from bokeh.models import ColorBar, Legend, LegendItem
from bokeh.models.glyphs import Text
from bokeh.plotting import figure
from bokeh.transform import linear_cmap


from bokeh.palettes import *
from bokeh.transform import cumsum
from numpy import pi
import pandas as pd
from bokeh.resources import CDN

def heatmap(data_matrix, sample_matrix, ls_color_palette=Reds9, r_low=-5, r_high=105, s_z="Sensivity"):
    """
    input:
        df_matrx: a dataframe in same xy orientation as the final heatmap.
          the index should cary the y axis label.
          the column should cary the x axis label.
          the matrix as such should only cary the z axis values.

        ls_color_palette: a list color strings to specify the color spectrum.
            this variable is compatible with the ordinary bokeh palettes:
            https://bokeh.pydata.org/en/latest/docs/reference/palettes.html

        r_low: quantitative minimum value. the dataset can contain lower values,
            but for color labeling they will be mapped to this minimum value.
            e.g.: -8.

        r_high: quantitative maximum value. the dataset can contain lower values,
            but for color labeling they will be mapped to this maximum value.
            e.g.: 8.

        s_z: string. label that specifies what the values in the matrix actually
            are. e.g.: 'gene expression [log2]'

    output:
        p: bokeh plot object.

    description:
        this function will return a bokeh based interactive heatmap plot.
        the color are representing the z value.
    """
    df_matrix = data_matrix
    sm_matrix = sample_matrix

    if (df_matrix.index.name == None):
        df_matrix.index.name = "organisms"
    if (df_matrix.columns.name == None):
        df_matrix.columns.name = "antimicrobials"
    s_y = df_matrix.index.name
    s_x = df_matrix.columns.name


    # melt dataframe
    df_tidy = df_matrix.reset_index().melt(
        id_vars=[df_matrix.index.name],
        value_name=s_z
    )

    sm_tidy = sm_matrix.reset_index().melt(
        id_vars=[df_matrix.index.name],
        value_name='samples'
    )

    result = pd.concat([df_tidy, sm_tidy], axis=1, join='inner')

    # color declaration
    d_zcolormapper = linear_cmap(
        field_name=s_z,
        palette=ls_color_palette,
        low=r_low,
        high=r_high
    )
    # tooltip declaration
    lt_tooltip = [
        (s_y, f"@{s_y}"),
        (s_x, f"@{s_x}"),
        (s_z, f"@{s_z}"),
        ('samples', f"@{'samples'}"),
    ]
    # generate figure
    o_colorbar = ColorBar(color_mapper=d_zcolormapper['transform'])
    p = figure(
        y_range=df_matrix.index.values,
        x_range=df_matrix.columns.values,
        tools = "hover,pan,reset,wheel_zoom",  # have to be set hardcoded
        #active_drag = "wheel_zoom",  # have to be set hardcoded
        tooltips=lt_tooltip,
        title=s_z,
        plot_width=1200,
        plot_height=600,
    )
    p.rect(
        source=result,
        x=s_x,
        y=s_y,
        color=d_zcolormapper,
        width=1,
        height=1,
    )
    p.add_layout(o_colorbar, place='left')
    p.yaxis.major_label_orientation = "horizontal"
    p.xaxis.major_label_orientation = "vertical"
    # out
    return(p)
