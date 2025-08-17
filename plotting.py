from motion_detector import df 
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import HoverTool, ColumnDataSource

df['Start'] = df['Start'].astype(str) # Convert Start column to string for plotting
df['End'] = df['End'].astype(str) # Convert End column to string for plotting

cds = ColumnDataSource(df) # Create a ColumnDataSource from the DataFrame

p = figure(x_axis_label = 'datetime', height = 100, width = 500, sizing_mode="stretch_both", title ='Motion Detection Status') # Create a figure for plotting
p.yaxis.minor_tick_line_color = None # Remove minor ticks from y-axis

hover = HoverTool(tooltips=[("Start", "@Start"), ("End", "@End")]) # Create a hover tool to show start and end times

q = p.quad(
    top=[1]*len(df),
    bottom=[0]*len(df),
    left=df['Start'],
    right=df['End'],
    color="green"
) # Create a quad glyph to represent motion events

output_file("motion_detection_plot.html") # Specify the output file for the plot
show(p) # Display the plot in the browser