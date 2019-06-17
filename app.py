''' Present an interactive function explorer.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show app.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Button, Range1d
from bokeh.plotting import figure
# from bokeh.models.widgets import Dropdown

from functools import partial
import json
import urllib2
import time
import numpy as np
global current_field

url = 'https://api.thingspeak.com/channels/{chan}/feeds.json?api_key={key}'


def get_xaxis(data):
    sampling_rate = 1
    t = time.time()
    axis = np.arange(len(data)) * sampling_rate
    xaxis = [t - (max(axis) - x) for x in axis]
    xaxis = [time.gmtime(t - (max(axis) - x)) for x in axis]
    xaxis = ["%.2d:%.2d:%.2d" % (x.tm_hour, x.tm_min, x.tm_sec) for x in xaxis]

    label_dict = {}
    for i, x in enumerate(xaxis):
        if i % 20 == 0:
            label_dict[i] = x
    return np.arange(len(data)), label_dict


data = {'field1': [-1],
        'field2': [-1],
        'field3': [-1],
        'field4': [-1],
        'field5': [-1],
        'field6': [-1],
        'field7': [-1],
        'field8': [-1]}
labels = {'field1': {'label': 'PM10', 'unit': 'ug/m3'},
          'field2': {'label': 'PM2.5', 'unit': 'ug/m3'},
          'field3': {'label': 'Temperatur Aussen', 'unit': 'Grad C'},
          'field4': {'label': 'Luftfeuchtigkeit Aussen', 'unit': '%'},
          'field5': {'label': 'Niederschlag', 'unit': ''},
          'field6': {'label': 'Luftdruck', 'unit': 'hPa'},
          'field7': {'label': 'Temperatur Innen', 'unit': 'Grad C'},
          'field8': {'label': 'Luftfeuchtigkeit Innen', 'unit': '%'}}

channels = {
            1: {'id': '801706', 'key': 'QF3J8GJU26GWBKGV'},
            2: {'id': '734828', 'key': 'YJX4M1WU9B002N5Z'}
            }

for id in channels.keys():
    url_in = url.format(chan=channels[id]['id'], key=channels[id]['key'])

    try:
        response = urllib2.urlopen(url_in)

        # Set up data
        html = response.read()
        data_feed = json.loads(html)
        for entry in data_feed['feeds']:
            for key, values in entry.iteritems():
                if key in data:
                    # print(labels[key]['label'], values)
                    try:
                        data[key].append(float(values))
                    except Exception:
                        continue
    except Exception as e:
        print(e)

current_field = 'field7'
x, xaxis_ticks = get_xaxis(data[current_field])
y = data[current_field]
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=800, plot_width=800,
              title=labels[current_field]['label'],
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_axis_label='Zeit')

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
plot.y_range = Range1d(0, 30)
# if 'Temperatur' in labels[current_field]['label']:
#     plot.y_range.start = 0
#     plot.y_range.end = 50
# elif 'Luftfeuchtigkeit' in labels[current_field]['label']:
#     plot.y_range.start = 0
#     plot.y_range.end = 100
# else:
#     plot.y_range.start = min(y)-10
#     plot.y_range.end = max(y)+10

plot.yaxis.axis_label = labels[current_field]['unit']
plot.xaxis.ticker = xaxis_ticks.keys()
plot.xaxis.major_label_overrides = xaxis_ticks


# Set up callbacks
def update_data(inkey, b):
    # Set up data
    d = []

    if int(inkey[-1]) in (1, 2, 3, 4, 5, 6):
        id = 1
    else:
        id = 2

    url_in = url.format(chan=channels[id]['id'], key=channels[id]['key'])
    response = urllib2.urlopen(url_in)
    # Set up data
    try:
        html = response.read()
        data_feed = json.loads(html)
        for entry in data_feed['feeds']:
            for key, values in entry.iteritems():
                if key == inkey:
                    # print(labels[key]['label'], values)
                    try:
                        d.append(float(values))
                    except Exception:
                        d.append(-1)

        if d is not None:
            x, xaxis_ticks = get_xaxis(d)
            y = d
            plot.title.text = labels[inkey]['label']
            if 'Temperatur' in labels[inkey]['label']:
                plot.y_range.start = 0
                plot.y_range.end = 30
            elif 'Luftfeuchtigkeit' in labels[inkey]['label']:
                plot.y_range.start = 0
                plot.y_range.end = 100
            else:
                plot.y_range.start = min(d)-10
                plot.y_range.end = max(d)+10
            plot.yaxis.axis_label = labels[inkey]['unit']

            source.data = dict(x=x, y=y)
    except Exception as e:
        print(e)


def update_weather(inkey):
    print(labels[inkey]['label'])


# # Set up layouts and add to document
buttons = {}

if data['field1'][-1] >= 10.:
    color = 'danger'
else:
    color = 'success'
buttons[1] = Button(label=r"%s: %s %s" % (labels['field1']['label'],
                                          data['field1'][-1],
                                          labels['field1']['unit']),
                    button_type=color)


if data['field2'][-1] >= 5.:
    color = 'danger'
else:
    color = 'success'
buttons[2] = Button(label=r"%s: %s %s" % (labels['field2']['label'],
                                          data['field2'][-1],
                                          labels['field2']['unit']),
                    button_type=color)

buttons[3] = Button(label="%s: %.1f %s" % (labels['field3']['label'],
                                           data['field3'][-1],
                                           labels['field3']['unit']))
buttons[4] = Button(label="%s: %.1f %s" % (labels['field4']['label'],
                                           data['field4'][-1],
                                           labels['field4']['unit']))

if data['field5'][-1] < 0:
    color = 'danger'
    txt = 'Ja'
else:
    color = 'success'
    txt = 'Nein'

buttons[5] = Button(label="%s: %s" % (labels['field5']['label'], txt),
                    button_type=color)
buttons[6] = Button(label="%s: %.1f %s" % (labels['field6']['label'],
                                           data['field6'][-1],
                                           labels['field6']['unit']))
buttons[7] = Button(label="%s: %.1f %s" % (labels['field7']['label'],
                                           data['field7'][-1],
                                           labels['field7']['unit']))
buttons[8] = Button(label="%s: %.1f %s" % (labels['field8']['label'],
                                           data['field8'][-1],
                                           labels['field8']['unit']))

buttons[1].on_click(partial(update_data, inkey="field1", b=buttons[1]))
buttons[2].on_click(partial(update_data, inkey="field2", b=buttons[2]))
buttons[3].on_click(partial(update_data, inkey="field3", b=buttons[3]))
buttons[4].on_click(partial(update_data, inkey="field4", b=buttons[4]))
buttons[5].on_click(partial(update_data, inkey="field5", b=buttons[5]))
buttons[6].on_click(partial(update_data, inkey="field6", b=buttons[6]))
buttons[7].on_click(partial(update_data, inkey="field7", b=buttons[7]))
buttons[8].on_click(partial(update_data, inkey="field8", b=buttons[8]))

# menu = [("Channel 1", "channel_1"), ("Channel 2", "channel2_2")]
# dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

inputs = column(buttons[1], buttons[2], buttons[3], buttons[4],
                buttons[5],
                buttons[6], buttons[7], buttons[8])

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Wetterstation"

# curdoc().add_periodic_callback(partial(update_weather,
#                                        inkey=current_field), 1000)
