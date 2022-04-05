import pandas as pd
import datetime as dt
from bokeh.io import cardoc
from bokeh.plotting import figure
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectrals
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import DateRangeSlider, Selevt
from bokeh.models.widgets import Tabs, Panel

data = pd.read_csv('myapp/data/it2002.csv')

## change the type formatting here
data['country'] = data['country_str'].astype(str)
data

##Resetting index and groupby here
consumer = data
properties = data
active = data
grouped = data

## indexing
ints_consumer = data[].groupby([]).sum().reset_index()
ints_properties = 
ints_active = 


source_consumer = ColumnDataSource(data=[
    'Total consumers'   :
    'since'             :
    'Total_Revenue'     :
    'country'           :
])

source_properties = ColumnDataSource(data=[
    'Country'   :
    'Amenities'             :
    ''     :
    ''
])

source_active = ColumnDataSource (data=[
    'Country'   :
    'Amenities'             :
    ''     :
    ''
])

source_top_country = ColumnDataSource(grouped)
country = source_top_country.data['country'].tolist()

tooltips_consumer = [
    ('Cinema Code', '@cinema_code'),
    ('Date', '@data{%F}'),
    ('Total Sales', '@total_sales'),
    ('Total Revenue', '@total revenue'),
]

tooltips_properties = [
    ('Cinema Code', '@cinema_code'),
    ('Date', '@data{%F}'),
    ('Total Sales', '@total_sales'),
    ('Total Revenue', '@total revenue'),
]

tooltips_consumer_vbar = [
    ('Cinema Code', '@cinema_code'),
    ('Date', '@data{%F}'),
    ('Total Sales', '@total_sales'),
    ('Total Revenue', '@total revenue'),
]

fig_consumer = figure(x_axis_type = 'datetime',
    plot_height = 500, plot_width=1000,
    title = 'Total Sales across time',
    x_axis_label='Date', y_axis_label='Total Sales')

fig_properties = figure(x_axis_type = 'datetime',
    plot_height = 500, plot_width=1000,
    title = 'Total Sales across time',
    x_axis_label='Date', y_axis_label='Total Sales')

fig_consumer_vbar = figure(plot_height = 500, plot_width =500,
    title = 'Total Sales across time',
    x_axis_label='Date', y_axis_label='Total Sales'
    toolbar_location= None)

fig= figure(x_axis_type= 'datetime',
    plot_height = 500, plot_width =500,
    title = 'Total Sales across time',
    x_axis_label='Date', y_axis_label='Total Sales'
    toolbar_location= None)

fig_consumer.add_tools(Hovertool(tooltips = tooltips_consumer, formatters ={'@date': 'datetime'}))

fig_properties.add_tools(Hovertool(tooltips = tooltips_properties, formatters ={'@date': 'datetime'}))
fig_consumer_vbar.add_tools(Hovertool(tooltips = tooltips_consumer_vbar)

fig_consumer.line('date', 'total_sales',
    color = 'yellow'
    source = source_consumer)

fig_properties.line('date', 'total_sales',
    color = 'blue'
    source = source_properties)

fig_consumers_vbar.vbar(x='contry_str', top =' total_sales', source= source_top_country, width=0.50)

idx
