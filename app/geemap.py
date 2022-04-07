#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from sqlalchemy import create_engine

#have to change the databasekey

host = "ec2-52-202-152-4.compute-1.amazonaws.com"
database = "d56cm9suguuoml"
user = 'iyhitckklvimhx'
password = 'c5facc44d1f2e2fda57f36ee026e57d66eff62c3d5406b33606391ecd3e8b0b7'

connection_string = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

sql = 'SELECT * FROM ne_50m_land'
import geopandas as gpd
gdf = gpd.read_postgis(sql, con=engine)


# In[4]:


import geemap
m = geemap.Map(center=[1.351, 103.8198], zoom=6, ee_initialize=False) #center at singapore
m


# In[5]:


#area
style = {
    "stroke": True,
    "color": "#000000",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#0000ff",
    "fillOpacity": 0.4,
}
gdf_crs = gdf.to_crs(epsg="4326")
geojson = gdf_crs.__geo_interface__
m.add_geojson(geojson, style=style, layer_name="land")


# In[6]:


#points
sql2 = 'SELECT * FROM geometry_test2'
gdf_prop = gpd.read_postgis(sql2, con=engine)
gdf_prop = gdf_prop.set_index("name")
gdf_prop_crs = gdf_prop.to_crs(epsg="4326")
prop_geojson = gdf_prop_crs.__geo_interface__
m.add_geojson(prop_geojson, layer_name="properties")


# out_dir = os.path.expanduser('~/Downloads')
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)
# out_json = os.path.join(out_dir, 'ne_50m_land.geojson')
# gdf.to_file(out_json, driver="GeoJSON")
# out_shp = os.path.join(out_dir, 'ne_50m_land.shp')
# gdf.to_file(out_shp)
