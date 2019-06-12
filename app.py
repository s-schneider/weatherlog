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
from bokeh.plotting import figure, show
from bokeh.models.annotations import Title

from functools import partial

import json
import urllib2
import numpy as np


url = 'https://api.thingspeak.com/channels/794255/'
url += 'feeds.json?api_key=0AWEFXGCB5L3T4LC'
response = urllib2.urlopen(url)

# Set up data
html = response.read()
data_feed = json.loads(html)
data = {'field1': [],
        'field2': [],
        'field3': [],
        'field4': [],
        'field5': [],
        'field6': [],
        'field7': [],
        'field8': []}
labels = {'field1': 'PM10',
          'field2': 'PM2.5',
          'field3': 'Temperatur Aussen',
          'field4': 'Luftfeuchtigkeit Aussen',
          'field5': 'Niederschlag',
          'field6': 'Luftdruck',
          'field7': 'Temperatur Innen',
          'field8': 'Luftfeuchtigkeit Innen'}

for entry in data_feed['feeds']:
    for key, values in entry.iteritems():
        if key in data:
            try:
                data[key].append(float(values))
            except Exception:
                data[key] = np.nan

# N = 200
for f in data.keys():
    try:
        x = range(len(data[f]))
        y = data[f]
        init_field = f
    except Exception:
        continue
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=800, plot_width=800, title=labels[init_field],
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up callbacks
i = 0


def update_data(inkey):
    url = 'https://api.thingspeak.com/channels/794255/'
    url += 'feeds.json?api_key=0AWEFXGCB5L3T4LC'
    response = urllib2.urlopen(url)

    # Set up data
    html = response.read()
    data_feed = json.loads(html)
    d = []
    for entry in data_feed['feeds']:
        for key, values in entry.iteritems():
            if key == inkey:
                try:
                    d.append(float(values))
                except Exception:
                    d = None

    if d is not None:
        x = range(len(d))
        y = d
        plot.title.text = labels[inkey]
        source.data = dict(x=x, y=y)


# # Set up layouts and add to document
button1 = Button(label="%s: %s" % (labels['field1'], data['field1'][-1]))
button2 = Button(label="%s: %s" % (labels['field2'], data['field2'][-1]))
button3 = Button(label="%s" % labels['field3'])
button4 = Button(label="%s" % labels['field4'])
button5 = Button(label="%s" % labels['field5'])
button6 = Button(label="%s" % labels['field6'])
button7 = Button(label="%s: %.2f" % (labels['field7'], data['field7']))
button8 = Button(label="%s: %.2f" % (labels['field8'], data['field8']))

button1.on_click(partial(update_data, inkey="field1"))
button2.on_click(partial(update_data, inkey="field2"))
button3.on_click(partial(update_data, inkey="field3"))
button4.on_click(partial(update_data, inkey="field4"))
button5.on_click(partial(update_data, inkey="field5"))
button6.on_click(partial(update_data, inkey="field6"))
button7.on_click(partial(update_data, inkey="field7"))
button8.on_click(partial(update_data, inkey="field8"))

inputs = column(button1, button2, button3, button4, button5, button6,
                button7, button8)  # , offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Wetterstation"
