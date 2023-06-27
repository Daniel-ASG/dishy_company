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


def bar_plot_per_city(df, column, new_column_name, op):
    cols = ['city', 'country_id', column]
    aux = (df[cols].groupby(['city', 'country_id'])
                   .agg(op)
                   .sort_values(by=column, ascending=False)
                   .reset_index()
                   .rename(columns={column:new_column_name,
                                    'country_id':'Country'})
                   )
    n = 20
    fig = px.bar(aux.head(n), x='city', y=new_column_name,
                 text_auto='.2s', 
                 color='Country',
                 color_discrete_sequence=px.colors.qualitative.Plotly,
                 )
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': aux['city'].head(n)},
    )
    return fig



# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Cities',
                   page_icon='🏙️',
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
st.title("Cities")

with st.container():
# Order Metric
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of registered restaurants per city</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_city(df, 'restaurant_id', 'n_restaurant', 'count')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Number of registered cuisines per city</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_city(df, 'cuisines', 'n_cuisines', 'nunique')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Average restaurants ratings per city</h2>",
                unsafe_allow_html=True)
    fig = bar_plot_per_city(df, 'aggregate_rating', 'avg_rating', 'mean')
    st.plotly_chart(fig, use_container_width=True)
  