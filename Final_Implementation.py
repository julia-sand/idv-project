import os 
import math
#import geocoder
import folium
from folium import plugins
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import datetime
from google.colab import files
from bokeh.models import NumeralTickFormatter, ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral8, brewer
from bokeh.embed import file_html
from bokeh.layouts import column, row
from bokeh.resources import CDN
import warnings
warnings.filterwarnings("ignore")

now = datetime.datetime.now()
curr_year = now.year

#url="https://raw.githubusercontent.com/julia-sand/private/main/Helsinki_alueittain_2019%20-%20Taulukko.tsv?token=ARUCQSMHWGZ6UXDQ4VJU2JTASSZWS"
#data = pd.read_csv(url,header =0,index_col = 0,sep = "\t",skip_blank_lines=True)

#url_2 = "https://raw.githubusercontent.com/julia-sand/private/main/pop%20data1.txt?token=ARUCQSN4MPMD6UMAXIYDG6LASSZWW"
#pop_data = pd.read_csv(url_2,header =0,index_col = 0,sep = "\t",skip_blank_lines=True)

df_1 = pd.DataFrame(data)
df_2 = pd.DataFrame(pop_data)

df = df_1.copy()
df_pop = df_2.copy()

cols = df.iloc[1].values

df.drop(labels = df.index[0:3,],axis=0,inplace=True,errors = "ignore")

df.columns = cols

num = len(df.index)

coordinates = [[60.1674881, 24.9427473],
                [60.1684084083186, 24.9263515733],
                [60.1703, 24.9568],
                [60.1587146, 24.949404],
                [60.168415993, 24.9333962664],
                [60.1853441, 24.9167329],
                [60.1592669, 24.8754247],
                [60.2160031799,24.8840624936],
                [60.189796, 24.891724],
                [60.1990937, 24.8743585],
                [60.2166658, 24.916663],
                [60.222711, 24.8643556],
                [60.251749399999994, 24.873211367854573],
                [60.1972784996,24.9506305048],
                [60.183832598, 24.942829562],
                [60.189728, 24.9441203],
                [60.1961671, 24.9567103],
                [60.1999992, 24.926162962],
                [60.2166658, 24.9833294],
                [60.23945774,24.95182984],
                [60.2217, 24.9409],
                [60.2435384, 24.9269126],
                [60.2572811, 24.9680161],
                [60.2294429, 24.9635828],
                [60.2453263, 24.9597377],
                [60.2568231667,25.135185],
                [60.226708, 25.015215],
                [60.245247, 24.9896936],
                [60.2507611, 25.0085738],
                [60.283019, 25.0064817],
                [60.2760327, 25.036777],
                [60.2591712, 25.0784439],
                [60.1840207,25.0302165],
                [60.1833326, 25.0166666],
                [60.1955246, 25.0290632],
                [60.1732049, 25.0449197],
                [60.2208372,25.113158875],
                [60.2166658, 25.0999996],
                [60.2250101, 25.0757494],
                [60.2333324, 25.1333328],
                [60.2083483, 25.1435537],
                [60.251720, 25.175564],
                [60.251720, 25.175564]]

df["coordinates"] = coordinates

for i in range(len(df.columns)-1):
    #swap commas with dots 
    try:
        df.iloc[:,i] = df.iloc[:,i].str.translate(str.maketrans(',.', '.,'))
        df.iloc[:,i] = df.iloc[:,i].astype(float)
    except:
        pass

#add dist level
dist_level = np.zeros(len(df.index))
for i in range(len(df.index)):
    if "suur" in df.index[i]:
        dist_level[i] = 1
    elif "Helsinki" in df.index[i]:
        dist_level[i] = 2

df["dist_level"] = dist_level

#############GEOCODER############
#coords = []
#for i in range(num): 
#    location = df_all.District.iloc[i]
#    loc = geocoder.osm(location)     
#    row = [loc.lat,loc.lng]
#    coords.append(row)
#df["coords"] = coords

#add district id column 
dist_id = np.zeros(num)

for i in range(1,num):
    dist_id[i] = df.index[i][0]

df["dist_id"] = dist_id

#rename columns
df.rename(columns={"Suomenkieliset": "Finnish", "Ruotsinkieliset": "Swedish", "Vieraskieliset":"Others"}, inplace=True)

#format index
df.set_index(df.index.str.split(" +",expand = True),inplace=True)

df.reset_index(inplace=True)  

df.set_index("level_0",inplace=True)

#drop extra columns
df.drop(["level_1","level_2","level_3"], axis=1,inplace=True, errors="ignore")

#fix district names
df["District"] = ["Helsinki",
                  "Eteläinen",
                  "Vironniemi",
                  "Ullanlinna",
                  "Kampinmalmi",
                  "Taka-Töölö",
                  "Lauttasaari",
                  "Läntinen",
                  "Reijola",
                  "Munkkiniemi",
                  "Haaga",
                  "Pitäjänmäki",
                  "Kaarela",
                  "Keskinen",
                  "Kallio",
                  "Alppiharju",
                  "Vallila",
                  "Pasila",
                  "Vanhankaupunki",
                  "Pohjoinen",
                  "Maunula",
                  "Länsi-Pakila",
                  "Tuomarinkylä",
                  "Oulunkylä",
                  "Itä-Pakila",
                  "Koillinen",
                  "Latokartano",
                  "Pukinmäki",
                  "Malmi",
                  "Suutarila",
                  "Puistola",
                  "Jakomäki",
                  "Kaakkoinen",
                  "Kulosaari",
                  "Herttoniemi",
                  "Laajasalo",
                  "Itäinen",
                  "Vartiokylä",
                  "Myllypuro",
                  "Mellunkylä",
                  "Vuosaari",
                  "Östersundomin",
                  "Östersundom"]

#format column names for population
dates = np.arange(1985,2034,1,dtype=int)

df_pop.columns = dates

#remove zeros from numbers and format as floats
for i in range(len(df_pop.columns)-1):
    try: 
        df_pop.iloc[:,i] = df_pop.iloc[:,i].str.replace(r'\xa0','')
        df_pop.iloc[:,i] = df_pop.iloc[:,i].astype(float)
    except:
        pass

#format index for population df for join
df_pop.set_index(df_pop.index.str.split(" +",expand = True),inplace=True)
df_pop.reset_index(inplace=True)  
df_pop.set_index("level_0",inplace=True)

#drop extra columns
df_pop.drop(["level_1","level_2","level_3"], axis=1,inplace=True, errors="ignore")

#merge the data frames
df_all = df.merge(df_pop,how="outer",left_index=True,right_index=True)

#columns as strings
df_all.columns = df_all.columns.astype("str")

#fill nans
df_all = df_all.fillna(0)
df_pop = df_pop.fillna(0)

#only small districts
df_perispiiri = df_all[df_all.dist_level == 0.0]
num_1 = len(df_perispiiri.index)

df_perispiiri_pop = df_perispiiri.loc[:,"1985":]
num_years = len(df_perispiiri_pop.columns)

#normalise features
norm_weights = normalize(df_perispiiri_pop,"l2",axis = 0) *10

#separate coordinates
lon = np.zeros(num_1)
lat = np.zeros(num_1)
for i in range(num_1):
    lon[i] = df_perispiiri.coordinates.iloc[i][0]
    lat[i] = df_perispiiri.coordinates.iloc[i][1]

#heat_data = [np.c_[lat,lon,norm_weights[:,j]].tolist() for j in range(num_years)]

df_suuri = df_all[df_all.dist_level == 1.0]
df_suuri_pop = df_suuri.loc[:,"1985":]

#popups
def plot_popup(i):

    #sets region id
    curr_dist_id = df_all.dist_id[i]
    curr_index = df_all.index[i]

    #takes indexes of dists with that region id
    idx_region = df_all.query("dist_id == @curr_dist_id & dist_level == 0.0").index.values


    #take the population data only and transpose for stacking
    df_plotting_t = df_pop.loc[idx_region].transpose()

    #turn indexes into their names
    dist_names = df_all.District[idx_region].tolist()
    df_plotting_t.columns = dist_names

    source = ColumnDataSource(df_plotting_t)

    N = len(idx_region)

    p = figure(
              plot_width=450, 
              plot_height=250, 
              toolbar_location = None, 
              #tools="hover",
              #tooltips = "@dist_names: @$name"
              )

    p.title.text = 'Population projections'
    p.grid.minor_grid_line_color = '#eeeeee'

    zeros = np.zeros(num_years)

    curr_sum = 0
    curr_sum_base = 0 

    for j,color in zip(range(len(df_plotting_t.columns)), Spectral8):
        if j == 0:
            p.varea(df_plotting_t.index, 
                y1 = df_plotting_t.iloc[:,j], 
                y2 = zeros,
                #line_width=2, 
                color = color, 
                muted_alpha=0.4, 
                legend_label=df_plotting_t.columns[j],
                muted = False if idx_region[j]==curr_index else True)
        else:
            p.varea(df_plotting_t.index, 
                y1 = df_plotting_t.iloc[:,j] + curr_sum,
                y2 = df_plotting_t.iloc[:,j-1] + curr_sum_base, 
                #line_width=2, 
                color = color, 
                muted_alpha=0.4, 
                legend_label=df_plotting_t.columns[j],
                muted = False if idx_region[j] == curr_index else True)
        curr_sum += df_plotting_t.iloc[:,j]
        if j !=0:
            curr_sum_base += df_plotting_t.iloc[:,j-1]

    p.legend.location = "top_left"
    p.legend.click_policy="mute"
    p.legend.items.reverse()

    #formatting
    p.yaxis.axis_label = 'Population'
    p.yaxis.formatter=NumeralTickFormatter(format='0,0')
    p.xaxis.axis_label = 'Year'
    p.xaxis.axis_label = 'Year'
    p.y_range.start = 0
    p.x_range.start = 1985
    p.x_range.end = 2033
    p.x_range.range_padding = 0.1
    p.ygrid.band_fill_alpha = 0.1
    p.ygrid.band_fill_color = "navy"
    p.yaxis.minor_tick_line_color = None

    #add second plot for district breakdown
    #bar chart of language breakdown
    cols = ["Finnish","Swedish","Others"]
    df_plotting_2 = df_all[cols].iloc[i,:].values.tolist()

    #area average values
    df_plotting_all_reg = df_all[cols].loc[idx_region]
    region_means = df_plotting_all_reg.mean(axis=0).values.tolist()

    p2 = figure(title="Population by Language",
                x_range = cols,
                plot_width=250, 
                plot_height=250,
                toolbar_location = None
                ) 

    offsets_1 = - np.ones(3) * 0.2
    x_vals_1 = list(zip(cols, offsets_1))

    g1 = p2.vbar(top = df_plotting_2, 
            x=x_vals_1, 
            color=brewer['Spectral'][3],
            width = 0.5
            )


    offsets_2 = np.ones(3) * 0.2
    x_vals_2 = list(zip(cols, offsets_2))

    g2 = p2.vbar(top = region_means, 
            x = x_vals_2, 
            color="lightblue",
            fill_alpha = 1.0,
            width = 0.5
            )

    hover_1 = HoverTool(renderers=[g1],
                      tooltips=[
                              ("Speakers","@top{0,0}"),
                                  ],
                      mode="mouse")

    hover_2 = HoverTool(renderers=[g2],
                      tooltips=[
                              ("Region Average","@top{0,0}"),
                                  ],
                      mode="mouse")

    p2.add_tools(hover_1)
    p2.add_tools(hover_2)

    p2.y_range.start = 0
    p2.x_range.range_padding = 0.1
    p2.xgrid.grid_line_color = None
    p2.yaxis.minor_tick_line_color = None
    p2.yaxis.formatter=NumeralTickFormatter(format='0,0')

    p_all = row(p,p2)

    html = file_html(p_all, CDN, "my plot")
    
    return html
def plot_popup_suuri(i):

    curr_index = df_all.index[i]

    p = figure(
              plot_width=450, 
              plot_height=250, 
              toolbar_location = None 
              #tools="hover",
              #tooltips = "$dist_names: @$name"
              )

    p.title.text = 'Population Projections by Region'
    p.grid.minor_grid_line_color = '#eeeeee'

    for j,color in zip(range(len(df_suuri.index)), Spectral8):
        p.line(dates, 
               df_suuri_pop.iloc[j,:], 
               line_width=2, 
               color = color, 
               muted_alpha=0.4, 
               legend_label=df_suuri.District[j],
               muted = False if df_suuri_pop.index[j]==curr_index else True)

    p.legend.location = "top_left"
    p.legend.click_policy="mute"
    p.legend.glyph_width = 20
    p.legend.spacing = 0
    p.legend.padding = 0
    
    #formatting
    p.yaxis.axis_label = 'Population'
    p.yaxis.formatter=NumeralTickFormatter(format='0,0')
    p.xaxis.axis_label = 'Year'
    p.ygrid.band_fill_alpha = 0.1
    p.ygrid.band_fill_color = "navy"
    p.y_range.start = 0
    p.x_range.start = 1985
    p.x_range.end = 2033
    p.x_range.range_padding = 0.1
    p.yaxis.minor_tick_line_color = None

    html = file_html(p, CDN, "my plot")
    
    return html
map_1 = folium.Map(location=[60.20, 25.01],
                 tiles =None, 
                 zoom_start=10,
                 min_zoom = 8,
                 max_zoom = 10,
                 max_bounds= True)

tile = folium.TileLayer('openstreetmap', name='my tilelayer', control=False)
tile.add_to(map_1)

#function to edit marker cluster appearance
icon_create_function_dists = '''
     function(cluster) {
     var childCount = cluster.getChildCount();
     return L.divIcon({html: '<div><span>' + childCount + '</div></span>' ,
                       className: 'marker-cluster marker-cluster-small',
                       iconSize: new L.Point(30, 30)});
     }
 '''
icon_create_function_regions = '''
     function(cluster) {
     var childCount = cluster.getChildCount();
     return L.divIcon({html: '<div><span>' + childCount + '</div></span>' ,
                       className: 'marker-cluster marker-cluster-large',
                       iconSize: new L.Point(35, 35)});
     }
 '''

#feature groups for controls
fg_regions = folium.FeatureGroup(name="View by Region",
                                 control=True,
                                 overlay=True)
fg_regions.add_to(map_1)

fg_dists = folium.FeatureGroup(name="View by District",
                               control=True,
                               overlay=True,
                               show=False)
fg_dists.add_to(map_1)

#cluster markers
clusters_dists = plugins.MarkerCluster(overlay=True, 
                    icon_create_function = icon_create_function_dists,
                    control=True,
                    show=False
                    )
clusters_dists.add_to(fg_dists)

clusters_regions = plugins.MarkerCluster(overlay=True, 
                    icon_create_function = icon_create_function_regions,
                    control=True,
                    show=True
                    )
clusters_regions.add_to(fg_regions)

color = ['blue',
          'lightred',
          'beige',
          'darkgreen',
          'lightgreen',
          'purple',
          'pink',
          'cadetblue'
          ]


#markers for each dist
for i in range(1,num):
    suuri_id = int(df_all.dist_id[i])

    if df_all.dist_level.iloc[i] == 0: 
        region_name = str(df_all.query("dist_id == @suuri_id & dist_level ==1.0").District.values[0])
        
        try: 
            html = plot_popup(i)
        except: 
            html = "something went wrong"
      
        iframe = folium.IFrame(html=html, width=800, height=280)
        popup = folium.Popup(iframe, max_width=2650)
        markers = folium.Marker(
            location=df_all.coordinates.iloc[i], # coordinates for the marker
            icon=folium.Icon(color = color[suuri_id-1]),
                            popup = popup,
                            #add place name as tool tip on hover
                            #add region name
                            tooltip = "<b>District:</b> {} \n <b>Region:</b> {}".format(df_all.District.iloc[i],region_name)
                            )

        markers.add_to(clusters_dists)
    elif df_all.dist_level.iloc[i] == 1:
        try: 
            html = plot_popup_suuri (i)
        except: 
            html = "something went wrong"
        iframe = folium.IFrame(html=html, width=500, height=280)
        popup = folium.Popup(iframe, max_width=2650)

        markers = folium.Marker(
            location=df_all.coordinates.iloc[i], # coordinates for the marker
            icon=folium.Icon(color= "orange",
                            icon = "info-sign",
                            icon_color = "white"),
            popup = popup,
            #add place name as tool tip on hover
            tooltip = df_all.District.iloc[i],
            )
        markers.add_to(clusters_regions)

#add full screen
plugins.Fullscreen(position="topright",
                    title="Full Screen",
                    title_cancel="Exit Full Screen",
                    force_separate_button=True,
                ).add_to(map_1)

#add layer controls
folium.LayerControl(position="topright",
                    autoZIndex = True, 
                    collapsed = False).add_to(map_1)
