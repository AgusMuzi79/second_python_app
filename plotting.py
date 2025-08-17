from motion_detector import df 
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd

df['Start'] = pd.to_datetime(df['Start']) # Convert 'Start' column to datetime
df['End'] = pd.to_datetime(df['End']) # Convert 'End' column to datetime

cds = ColumnDataSource(df) # Create a ColumnDataSource from the DataFrame

p = figure(
    x_axis_label = 'datetime', 
    height = 200, width = 800, 
    sizing_mode="stretch_width", 
    title ='Motion Detection Status') # Create a figure for plotting

p.yaxis.minor_tick_line_color = None # Remove minor ticks from y-axis

hover = HoverTool(tooltips=[("Start", "@Start{%F %T}"), ("End", "@End{%F %T}")],
                  formatters={'@Start': 'datetime', '@End': 'datetime'}) # Create a hover tool to display start and end times
p.add_tools(hover) # Add the hover tool to the figure

p.quad(
    top=1,
    bottom=0,
    left="Start",
    right="End",
    color="green",
    source=cds
) # Create a quad glyph to represent motion events

output_file("motion_detection_plot.html") # Specify the output file for the plot
show(p) # Display the plot in the browser