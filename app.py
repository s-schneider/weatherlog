''' Present an interactive function explorer.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show app.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
# from bokeh.models.widgets import Slider, TextInput
from bokeh.models import Button
from bokeh.plotting import figure
import json
import urllib2
import numpy as np


url = 'https://api.thingspeak.com/channels/794255/'
url += 'feeds.json?api_key=0AWEFXGCB5L3T4LC'
response = urllib2.urlopen(url)

# Set up data
html = response.read()
data_feed = json.loads(html)

# with open('data.json', 'r') as fh:
#     content = fh.readlines()
#
# data_feed = json.loads(content[0])

data = {'field1': [],
        'field2': [],
        'field3': [],
        'field4': [],
        'field5': [],
        'field6': [],
        'field7': [],
        'field8': []}

for entry in data_feed['feeds']:
    for key, values in entry.iteritems():
        if key in data:
            try:
                data[key].append(float(values))
            except Exception:
                data[key] = np.nan

# N = 200
x = range(len(data['field7']))
y = data['field7']
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=800, plot_width=800, title="Wetterstation",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up callbacks
i = 0


def update_data():
    url = 'https://api.thingspeak.com/channels/794255/'
    url += 'feeds.json?api_key=0AWEFXGCB5L3T4LC'
    response = urllib2.urlopen(url)

    # Set up data
    html = response.read()
    data_feed = json.loads(html)
    d = []
    for entry in data_feed['feeds']:
        for key, values in entry.iteritems():
            if key == 'field7':
                try:
                    d.append(float(values))
                except Exception:
                    d = np.nan

    x = range(len(d))
    y = d
    source.data = dict(x=x, y=y)


# # Set up layouts and add to document
button1 = Button(label="PM10: %s" % data['field1'])
button2 = Button(label="PM2.5: %s" % data['field2'])
button3 = Button(label="Temperatur Aussen")
button4 = Button(label="Luftfeuchtigkeit Aussen")
button5 = Button(label="Niederschlag")
button6 = Button(label="Luftdruck")
button7 = Button(label="Temperatur Innen: %.2f" % data['field7'][-1])
button8 = Button(label="Luftfeuchtigkeit Innen: %.2f" % data['field8'][-1])

button7.on_click(update_data)
button8.on_click(update_data)

inputs = column(button1, button2, button3, button4, button5, button6,
                button7, button8)  # , offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
