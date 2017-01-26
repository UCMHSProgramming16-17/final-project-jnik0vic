import csv
f = open('njpop.csv')
csv_f = csv.reader(f)
for row in csv_f:
    print(row)
f.close()

from bokeh.io import save, output_file
from bokeh.models import(
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)

output_file("map.html")

from bokeh.palettes import Spectral6 as palette
from bokeh.plotting import figure
from bokeh.sampledata.us_counties import data as counties

with open('njpop.csv', mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)
    popdata = {rows[0]:rows[1] for rows in reader}

palette.reverse()

# state_xs = state["NJ"]["lons"]
# state_ys = state["NJ"]["lats"]

# # print(county.items())

# # print('county:', county

# source = ColumnDataSource(
#     data = dict(
#         x = state_xs,
#         y = state_ys
#     )
# )

# p = figure(
#     title = "Population Per County in NJ",
#     x_axis_location = None, y_axis_location = None
# )

# p.patch('x', 'y', source=source, fill_color='white', line_color='black')

# save(p)


counties = {
    code: county for code, county in counties.items() if county["state"] == "nj"
}

print('counties keys:', counties.keys())

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
popdict = [popdata[county_id] for county_id in counties]
# color_mapper = LogColorMapper(palette=palette)

county_population = [popdict[row] for row in counties]

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    # name=county_names,
    # population=county_population,
))



TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(
    title="Texas Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None
)
p.grid.grid_line_color = None

# p.patches('x', 'y', source=source,
#           fill_color={'field': 'rate', 'transform': color_mapper},
#           fill_alpha=0.7, line_color="white", line_width=0.5)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("NJ County Population)", "@population"),
    ("(Long, Lat)", "($x, $y)"),
]