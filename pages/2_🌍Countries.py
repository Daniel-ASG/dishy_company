# ========================================
# Import libraries
# ========================================
# import hvplot.pandas
import folium
import inflection
import pandas         as pd
import geopandas      as gpd
import plotly.express as px
import streamlit      as st
import numpy          as np

from streamlit_folium import folium_static
from geopy.geocoders  import Nominatim
from PIL              import Image


# ==========================================================
#                       Functions
# ==========================================================

def rename_columns(dataframe):
    df = dataframe.copy()
    title      = lambda x: inflection.titleize(x)
    snakecase  = lambda x: inflection.underscore(x)
    spaces     = lambda x: x.replace(" ", "")
    cols_old   = list(df.columns)
    cols_old   = list(map(title, cols_old))
    cols_old   = list(map(spaces, cols_old))
    cols_new   = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


COUNTRIES_ISO = {
    1:  {"country_id": "India",                     "iso_alpha": "IND"},
    14: {"country_id": "Australia",                 "iso_alpha": "AUS"},
    30: {"country_id": "Brazil",                    "iso_alpha": "BRA"},
    37: {"country_id": "Canada",                    "iso_alpha": "CAN"},
    94: {"country_id": "Indonesia",                 "iso_alpha": "IDN"},
    148: {"country_id": "New Zealand",              "iso_alpha": "NZL"},
    162: {"country_id": "Philippines",              "iso_alpha": "PHL"},
    166: {"country_id": "Qatar",                    "iso_alpha": "QAT"},
    184: {"country_id": "Singapore",                "iso_alpha": "SGP"},
    189: {"country_id": "South Africa",             "iso_alpha": "ZAF"},
    191: {"country_id": "Sri Lanka",                "iso_alpha": "LKA"},
    208: {"country_id": "Turkey",                   "iso_alpha": "TUR"},
    214: {"country_id": "United Arab Emirates",     "iso_alpha": "ARE"},
    215: {"country_id": "United Kingdom",           "iso_alpha": "GBR"},
    216: {"country_id": "United States of America", "iso_alpha": "USA"},
}
def get_country_info(country_id):
    country_info = COUNTRIES_ISO.get(country_id)
    return country_info["country_id"], country_info["iso_alpha"]


def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "pear",
    "FFBA00": "darkyellow",
    "CBCBC8": "silver",
    "FF7800": "orange",
    }
def color_name(color_code):
    return COLORS[color_code]


def count_unique_values(df):
    unique_counts = df.nunique().reset_index()
    unique_counts.columns = ['Column', 'Unique Count']
    return unique_counts


def drop_single_value_columns(df):
    unique_counts = count_unique_values(df)
    single_value_columns = unique_counts[unique_counts['Unique Count'] == 1]['Column']
    return df.drop(single_value_columns, axis=1)


def check_nulls(df):
    nulls_per_column = df.isnull().sum()
    total_values_per_column = df.shape[0]
    percent_null_per_column = (nulls_per_column / total_values_per_column) * 100
    return pd.DataFrame({'Column': nulls_per_column.index,
                         'Percent_nulls': percent_null_per_column.values})


# Function for styling country outlines
def style_function(feature):
    return {
        'color': 'red',
        'weight': 1,
        'fillOpacity': 0.2
    }
 
    
def clean_code(df):
    df = drop_single_value_columns(df)
    df = rename_columns(df)
    df["country_id"], df["ISO_Alpha"] = zip(*df["country_code"].apply(get_country_info))
    df['price_type'] = df.price_range.apply(create_price_type)
    df['rating_color'] = df.rating_color.apply(color_name)
    df.cuisines = df.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    df = df.drop_duplicates()
    df = df.drop(df[df.average_cost_for_two > 400000].index)
    df = df.reset_index(drop=True)
    return df


def overview_map(df):
    country_list = df.country_id.unique().tolist()

    # Create a Folium Map object
    map = folium.Map(location=[df.latitude.mean(),
                               df.longitude.mean()],
                     zoom_start=1.5
                     )

    # Create a Geocoder object from Geopy
    geolocator = Nominatim(user_agent="my_app")

    # Loop to get the coordinates of each country and add markers to the map
    for country in country_list:
        location = geolocator.geocode(country)
        latitude = location.latitude
        longitude = location.longitude

        # Add a marker for each country
        folium.Marker(location=[latitude, longitude], popup=country).add_to(map)

    # Load the country contours file
    world_shapes = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Filter the contours of the countries in the list
    filtered_shapes = world_shapes[world_shapes['name'].isin(country_list)]

    # Add the country outlines to the map
    folium.GeoJson(filtered_shapes, style_function=style_function).add_to(map)

    # Show map
    folium_static(map, width=1024, height=600)

    return None


def bar_plot_per_country(df, column, new_column_name, op):
    cols = ['country_id', column]
    aux = (df[cols].groupby('country_id')
                   .agg(op)
                   .sort_values(by=column, ascending=False)
                   .rename(columns={column:new_column_name})
                   .reset_index()
                   )
    fig = px.bar(aux, x='country_id', y=new_column_name,
                 text_auto='.2s', color=new_column_name,
                 color_continuous_scale='teal',
                 labels={'country_id':'Country'}
                 )
    return fig



def horizontal_bar_plot(df, column, result):
    sum_column = (df.loc[:,['country_id', column]]
                     .groupby('country_id')
                     .sum()
                     .reset_index()
                     )
    n_restaurants = (df.loc[:,['country_id', 'restaurant_id']]
                       .groupby('country_id')
                       .nunique()
                       .rename(columns={'restaurant_id':'n_restaurant'})
                       .reset_index()
                       )
    aux = pd.merge(sum_column, n_restaurants, on='country_id')
    aux[result] = aux[column] / aux['n_restaurant']
    aux = aux.sort_values(by=result)
    fig = px.bar(aux, y='country_id', x=result,
                 text_auto='.2s', color=result,
                 color_continuous_scale='teal')
    return fig



def sunburst_plot(df):
    aux = (df.loc[:, ['country_id', 'price_type', 'restaurant_id']]
              .groupby(['country_id', 'price_type'])
              .count()
              .rename(columns={'restaurant_id':'n_restaurant'})
          )
    aux = aux.reset_index()
    fig = px.sunburst(aux, 
                      path=['country_id', 'price_type'],
                      values='n_restaurant'
                     )
    fig.update_layout(height=700)
    return fig



# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Countries',
                   page_icon='🌍',
                   layout='wide'
                  )

# -----------------
# Import Dataset
# -----------------
zomato = pd.read_csv('dataset/zomato.csv')

# -----------------
# Cleaning Dataset
# -----------------
df = clean_code(zomato)



# #########################
#         Sidebar
# #########################

image = Image.open('logo.png')
st.sidebar.image(image, width=300)

st.sidebar.markdown('# Dishy ')
st.sidebar.markdown('### Delights at your fingertips')

st.sidebar.markdown('''___''')
country_options = st.sidebar.multiselect('Select the country:',
                                         df.country_id.unique().tolist(),
                                         default=df.country_id.unique().tolist()
                                        )

st.sidebar.markdown('''___''')
price_options = st.sidebar.multiselect('Select the price type:',
                                       df.price_type.unique().tolist(),
                                       default=df.price_type.unique().tolist()
                                      )

st.sidebar.markdown('''___''')
rating_options = st.sidebar.slider('Select a range of ratings:',
                                   float(df.aggregate_rating.min()), float(df.aggregate_rating.max()), 
                                   (float(df.aggregate_rating.min()), float(df.aggregate_rating.max()))
                                   )

st.sidebar.markdown('''___''')
st.sidebar.markdown('##### Powered by Comunidade DS')
st.sidebar.markdown('##### Data Analyst: Daniel Gomes')


# country filter
rows = df.country_id.isin(country_options)
df = df.loc[rows,:]

# price filter
rows = df.price_type.isin(price_options)
df = df.loc[rows,:]

# rating filter
rows = (df['aggregate_rating'] >= rating_options[0]) & (df['aggregate_rating'] <= rating_options[1])
df = df.loc[rows,:]




# #########################
# Layout in Streamlit
# #########################
st.title("Countries")

with st.container():
# Order Metric
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of registered cities per country</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_country(df, 'city', '#_cities', 'nunique')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of registered restaurants per country</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_country(df, 'restaurant_id', '#_restaurant', 'nunique')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of cuisines per country</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_country(df, 'cuisines', '#_cuisines', 'nunique')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of evaluations per country</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_country(df, 'votes', '#_votes', 'sum')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown("<h3 style='text-align: center; color: #129fa5;'>Avg Number of reviews per country</h2>",
                unsafe_allow_html=True)
        fig = horizontal_bar_plot(df, 'votes', 'reviews_per_rest')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("<h3 style='text-align: center; color: #129fa5;'>Avg score per country</h2>",
                unsafe_allow_html=True)
        fig = horizontal_bar_plot(df, 'aggregate_rating', 'avg_score')
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Countries & Price types</h2>",
                unsafe_allow_html=True)
    fig = sunburst_plot(df)
    st.plotly_chart(fig, use_container_width=True)
