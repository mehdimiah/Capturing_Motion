from video_grey import df #imports df from the file

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool,ColumnDataSource

#formatting and adding string column, as cds outputs entire format, .dt formats the string into y m d h m s
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


#columndatasource provide data to bokeh plot
csd = ColumnDataSource(df)

TOOLTIPS = [("Start","@Start_string"),("End","@End_string")]
#pointing to the string new data created as hover label is incorrect due to formatting of date time whne pointing to only date time


p = figure(x_axis_type = 'datetime',
height = 300,
width = 900,
tooltips = TOOLTIPS)

p.title.text = "Date Time Motion Graph"
p.title.align = "center"
p.title.text_font_size = "25px"
p.xaxis.axis_label = "Date and Time"
p.xgrid.visible = False
p.ygrid.visible = False
p.yaxis.minor_tick_line_color = None 
p.yaxis.ticker.desired_num_ticks = 1





q = p.quad(left="Start",right ="End",bottom=0,top=1,color = "blue",source = csd)
#because of cds, dont need to index the df anymore only column name and source via cds


#q = p.quad(left=df["Start"],right =df["End"],bottom=0,top=1,color = "blue")
#alternative version of quad adding data

output_file("graph.html")
show(p)
