import os
import shutil
import numpy as np
import pandas as pd
import imageio
import glob

from bokeh.layouts import column, row, gridplot, layout
from bokeh.plotting import figure, curdoc, output_file

from bokeh.models import (ColumnDataSource, RangeTool, BoxSelectTool, FileInput,
    Button, Div, Paragraph, TableColumn, DataTable, Span, Panel, Tabs, Label, LabelSet, CheckboxGroup)

output_file("../python-visualization-tool/templates/index.html")
df = pd.read_csv('../python-visualization-tool/data/data.csv')

source_graph = ColumnDataSource(
    data = dict(
        x = np.arange(0, len(df)), 
        y = df['score'], 
        frame = df['frame'], 
        ground_truth = df['ground_truth'], 
        image = df['image']
    )
)

source_table = ColumnDataSource(
    data = dict(
        frame = [], 
        y = [], 
        behaviour = [], 
        image = []
    )
)

def populate_table():
    pass


def get_mean():
    data_points = source_graph.data['y']
    sum_score = sum(data_points)
    mean = sum_score / len(data_points)
    return mean

TOOLTIPS = """ """
with open('../python-visualization-tool/templates/hover.html', 'r') as f:
    TOOLTIPS = f.read()
    
plot = figure(
    plot_width = 1400, 
    plot_height = 500, 
    tools = "xpan, ypan, save, reset",
    x_range = (0, 100), 
    tooltips = TOOLTIPS,
    )

plot.y_range.flipped = True


color_pallet = ['#9c9ede', '#6b6ecf', '#5254a3', '#393b79']

plot.line(
    x = "x", 
    y = "y", 
    source = source_graph, 
    line_width = 5,
    line_color = color_pallet[2],
    line_cap = 'round'
    )

plot.circle(
    x = "x", 
    y = "y", 
    source = source_graph,
    size = 6,
    line_color = color_pallet[1],
    color = color_pallet[1]
)
labels = LabelSet(
    text = "ground_truth", 
    source = source_graph, 
    render_mode = "canvas", 
    text_font_size = {'value': '10px'},
    text_align = 'center',
    text_alpha = 0.5,
    y_offset = 10
    )

plot_preview = figure(
    plot_height = 100, 
    plot_width = 1400, 
    y_range = plot.y_range, 
    x_axis_type = 'linear', 
    y_axis_type = None,
    outline_line_color = 'white'
    )

mean = Span(
    location = get_mean(), 
    dimension = 'width', 
    line_color = color_pallet[0], 
    line_dash = 'dashed', 
    line_width = 2,
    )

# plot grid style
plot.ygrid.minor_grid_line_color = 'navy'
plot.ygrid.minor_grid_line_alpha = 0.1

# box_select tool style
box_select = BoxSelectTool(dimensions="width")
box_select.overlay.line_dash =  "solid"
box_select.overlay.line_width = 1
box_select.overlay.fill_color = "green"
box_select.overlay.fill_alpha = 0.1
plot.add_tools(box_select)

# range_tool style
range_tool = RangeTool(x_range=plot.x_range)
range_tool.overlay.fill_color = "white"
range_tool.overlay.fill_alpha = 0.1
range_tool.overlay.line_dash = 'solid'
range_tool.overlay.line_width = 1

# plot_preview style
plot_preview.line('x', 'y', source=source_graph, color="grey", line_alpha=0.4)
plot_preview.add_tools(range_tool)
plot_preview.toolbar.active_multi = range_tool
plot_preview.ygrid.grid_line_color = 'whitesmoke'
plot_preview.ygrid.line_color = 'whitesmoke'

def file_handler(event):
    # to access retrieve the name and content of mp4 and npy file(s) use .filename and .value
    pass
def check_directory():
    source = source_table.data['image']
    target_ext = glob.glob("../python-visualization-tool/static/gif/selected/*.jpg")
    file_count = len(target_ext)
    try:
        if file_count >= 1:
            for file in target_ext:
                os.remove(file)
    except:
        print("unable to delete frames")
    else:
        duplicate_frames()
        print("frames copied")
def duplicate_frames():
    file_path = source_table.data['image']
    dest = "../python-visualization-tool/static/gif/selected/"
    try:
        for src in file_path:
            shutil.copy2(src, dest)
    except:
        print(f"unable to copy {src} to {dest}")
        
def create_gif():
    check_directory()
    save_path = "../python-visualization-tool/static/gif/test.gif"
    selected_frames = glob.glob("../python-visualization-tool/static/gif/selected/*.jpg")
    image_data = []
    try:
        for i in range(len(selected_frames)):
            data = imageio.imread(selected_frames[i])
            image_data.append(data)
        imageio.mimwrite(save_path, image_data, format=".gif", fps="10")
    except RuntimeError:
        print("must select multiple frames to generate a gif")
    else:
        print("gif has been successfully generated")
def select_tool_handler(event):
    source_table.data = {
        'frame' : [],
        'y' : [],
        'ground_truth': [],
        'image': []
        }
    
    event_data = event.geometry
    start = round(event_data['x0'])
    end   = round(event_data['x1'])
    source = source_graph.data
    
    # grabs the selected data from source_graph
    _frame = source['frame'][start:end]
    _y = source['y'][start:end]
    _ground_truth = source['ground_truth'][start:end]
    _image = source['image'][start:end]
    
    
    # where selected data is stored
    new_data = {
        'frame' : _frame,
        'y' : _y,
        'ground_truth': _ground_truth,
        'image': _image
        }
    source_table.stream(new_data)

## tab 1 ##
file_input1 = FileInput(accept = ".csv", multiple = False)
file_input2 = FileInput(accept = "video/*", multiple = False)
button1 = Button(label = "upload files")
tag1 = Paragraph(text = "select .csv file")
tag2 = Paragraph(text = "select .mp4 file")
file_input = column(tag1, file_input1, tag2, file_input2, button1)


## tab 2 ##
columns = [
    TableColumn(field="frame", title="frame id"),
    TableColumn(field="y", title="score"),
    TableColumn(field="ground_truth", title="behaviour"),
]
table_grid = DataTable(source = source_table, columns = columns, width = 1700, height = 200)
button2 = Button(label = "create")
table = column(table_grid)


## tab3 ##
LABELS = ["line graph", "scatter graph"]
checkbox_group1 = CheckboxGroup(labels = LABELS, active = [0])
checkbox1 = column(checkbox_group1)

## initialize tabs ##
tab1 = Panel(child = file_input, title = "upload files")
tab2 = Panel(child = checkbox1, title = "plot settings")
tab_panel_left = Tabs(tabs = [tab1, tab2])

## graph ##
plot.add_layout(mean)
graph = column(plot, plot_preview)

## callbacks ##
plot.on_event('selectiongeometry', select_tool_handler)
button2.on_event("button_click", create_gif)

## layout ##
curdoc().add_root(
    layout([[table],[tab_panel_left, graph]])
)
