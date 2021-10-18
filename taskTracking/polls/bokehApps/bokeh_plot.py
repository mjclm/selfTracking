from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.layouts import row


def bar_plot(source, x, top):

    p = figure(title="Simple line example",
               x_axis_label='x',
               y_axis_label='y')

    p.vbar(x=x, top=top, width=.9,
           line_color='white',
           color="#e84d60",
           legend_label="tasks", source=source)

    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return p
