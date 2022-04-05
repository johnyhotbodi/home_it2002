from multiprocessing.sharedctypes import Value
import pandas as pd
import datetime as dt
from bokeh.io import cardoc
from bokeh.plotting import figure, show
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectrals
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import DateRangeSlider, Selevt
from bokeh.models.widgets import Tabs, Panel

data = pd.read_csv('myapp/data/it2002.csv')

## change the type formatting here
data['country'] = data['country_str'].astype(str)
data['date'] = pd.to_datetime(data['date']).dt.date

##Resetting index and groupby here
consumer = data[['country code', 'index']].groupby(['country code']).sum().reset_index()
properties = data[['country', 'index']].groupby(['country']).sum().reset_index()
active = data[[]].groupby([]).sum().reset_index()
grouped = data[['contry', 'index']].groupby(['country code']).sum().sort_values(by= '', ascending= False)

## list indexing
ints_consumer = consumer[].value.counts().sort_index().index.tolist()
ints_properties = properties[].value.counts().sort_index().index.tolist()
ints_active = active[].value.counts().sort_index().index.tolist()


source_consumer = ColumnDataSource(data=[
    'Total consumers'   : consumer[consumer[]] == 304]['consumer_code'],
    'since'             :,
    'Total_Revenue'     :,
    'country'           :,
])

source_properties = ColumnDataSource(data=[
    'Country'    : properties[consumer[]] == 1576]['properties_code']
    'Amenities'  :
    ''              :
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

#Hover tooltips
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


#Plotting the graph
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

### Skipped the gridpoint part

def update_consumers(attr, old, new):

    [start,end] = slider.Value
    date_from = dt.datetime.fromtimestamp(start).date()
    date_until = dt.datetime.fromtimestamp(end).date()
    consumer_cd = int(consumer_select.value)

    #new data
    cinema_date = cinemas[(cinemas['date'] >= date_since

    new_data = {
        'the four columns'
    }
    source.data = new_data

    fig_consumer.title.text = 'Total Sales Cinema' + consumer_select.value

init_value = (data['date_since'].min(), data['date_since'].max())
slider = DataRangeSlider(start = init_value[0], end = init_value[1], value = init_value)
slider.on_change('value', update_consumers)

consumer_select = Select(
    options = [ str(x) for x in ints]
    value = '304'
    title =  'Consumer by Country'
)
consumer_select.on_change('value', update_consumer)

def update_properties(attr, old, new):

    [start,end] = slider.Value
    date_from = dt.datetime.fromtimestamp(start).date()
    date_until = dt.datetime.fromtimestamp(end).date()
    properties_cd = int(properties_select.value)

    #new data
    properties_date = properties[(properties['date'] >= date_from  & (properties['date'] <= date_until)]

    new_data = {
        'the four columns'
    }
    source.data = new_data

    fig_consumer.title.text = 'Total Sales Cinema' + consumer_select.value

init_value = (data['date_since'].min(), data['date_since'].max())
slider = DataRangeSlider(start = init_value[0], end = init_value[1], value = init_value)
slider.on_change('value', update_properties)

properties_select = Select(
    options = [str(x) for x in ints_properties]
    value = '1576'
    title =  'properties count'
)
properties_select.on_change('value', update_properties)

# Create layout
layout_0 = 
layout = row(widgetbox(consumer_select, slider), fig_consumer)
layout_properties = row(widgetbox(properties_select, slider), fig_properties)

zeroth_panel = Panel (child= layout_0, title= 'Home')
first_panel = Panel (child= layout, title= 'Top Sales by country')
second_panel = Panel (child= layout_properties, title= 'Properties by country')

tabs = Tabs(tabs=[first_panel, second_panel])

curdoc().add_root(tabs)
