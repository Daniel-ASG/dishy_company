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
import requests

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



currency_mapping = {
    "Botswana Pula(P)":       "BWP",
    "Brazilian Real(R$)":     "BRL",
    "Dollar($)":              "USD",
    "Emirati Diram(AED)":     "AED",
    "Indian Rupees(Rs.)":     "INR",
    "Indonesian Rupiah(IDR)": "IDR",
    "NewZealand($)":          "NZD",
    "Pounds(£)":              "GBP",
    "Qatari Rial(QR)":        "QAR",
    "Rand(R)":                "ZAR",
    "Sri Lankan Rupee(LKR)":  "LKR",
    "Turkish Lira(TL)":       "TRY"
}
def convert_to_usd(df, currency_column, currency_mapping):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    if response.status_code == 200:
        rates = response.json()['rates']
        df_rates = pd.DataFrame(rates.items(), columns=['Currency', 'Rate'])
        df_rates.set_index('Currency', inplace=True)
        df['average_cost_for_two_USD'] = df.apply(lambda x: x['average_cost_for_two'] / df_rates.loc[currency_mapping[x[currency_column]], 'Rate'], axis=1)
    else:
        print('Error', response.status_code)
    
    

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
    df['restaurant_id'] = df['restaurant_id'].astype(str)
    convert_to_usd(df, 'currency', currency_mapping)
    df.cuisines = df.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    df = df.drop_duplicates()
    df = df.drop(df[df.average_cost_for_two > 400000].index)
    df = df.reset_index(drop=True)
    return df



def bar_plot(df, col_x, new_col_x_name, col_y, new_col_y_name, op):
    cols = [col_x, col_y]
    aux = (df[cols].groupby(col_x)
                   .agg(op)
                   .sort_values(by=col_y, ascending=False)
                   .reset_index()
                   .rename(columns={col_x:new_col_x_name,
                                    col_y:new_col_y_name})
                   )
    fig = px.bar(aux.head(15), x=col_x, y=new_col_y_name,
                 text_auto='.2s', color=new_col_x_name,
                 color_continuous_scale='teal',
                 # labels={'country_id':'Country'}
                 )
    fig.update_layout(xaxis={'categoryorder': 'array',
                             'categoryarray': aux[col_x].head(15)},
                     )
    return fig


def avg_per_country(df, column):
    sum_reviews = (df.loc[:,['country_id', column]]
                     .groupby('country_id')
                     .sum()
                     .sort_values(by=column, ascending=False)
                     .reset_index()
                     )

    n_restaurants = (df.loc[:,['country_id', 'restaurant_id']]
                       .groupby('country_id')
                       .nunique()
                       .sort_values(by='restaurant_id', ascending=False)
                       .rename(columns={'restaurant_id':'n_restaurant'})
                       .reset_index()
                       )

    aux = pd.merge(sum_reviews, n_restaurants, on='country_id')

    # reviews_per_rest = n_votes / n_restaurants
    aux['result'] = aux[column] / aux.n_restaurant
    aux = aux.sort_values(by='result')

    fig = px.bar(aux, y='country_id', x='result',
                 text_auto='.3s', color='result',
                 color_continuous_scale='teal',
                 labels={'result':column}
                 )
    return fig



def scatter_plot(df):
    fig = px.scatter(df, y='aggregate_rating', x='average_cost_for_two_USD',
                     color='cuisines',
                     hover_data=["city", "country_id"],
                     hover_name='restaurant_name',
                     size_max=30)
    return fig



def table_top_15(df):
    aux = (df.sort_values(by=['aggregate_rating', 'votes'],
                         ascending=[False, False])
             .loc[:,['restaurant_id', 'restaurant_name', 'country_id', 'city', 'cuisines', 'average_cost_for_two_USD', 'price_type', 'aggregate_rating', 'votes']]
          )
    return aux.head(15)



def treemap_plot(df):
    fig = px.treemap(df, path=[px.Constant('all'), 'country_id', 'cuisines'],
                    color_continuous_scale='Blues', title='Restaurant Distribution')
    fig.update_layout(margin = dict(t=20, l=10, r=10, b=10),
                      height=600)
    return fig
# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Countries',
                   page_icon='🍴',
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
empty_slot = st.empty()
selection = st.sidebar.radio('', ('Select all countries', 'Select countries'))
if selection == 'Select all countries':
    default = df.country_id.unique().tolist()
else:
    default = None
country_options = st.sidebar.multiselect('Select the country:',
                                         df.country_id.unique().tolist(),
                                         default=default
                                        )
# st.write(country_options)

if country_options == []:
    empty_slot.markdown('# <span style="color:red">⬅️ Select at least one country</span>', unsafe_allow_html=True)
else:
    empty_slot.empty()

st.sidebar.markdown('''___''')
price_options = st.sidebar.multiselect('Select the price type:',
                                       df.price_type.unique().tolist(),
                                       default=df.price_type.unique().tolist()
                                      )

st.sidebar.markdown('''___''')
rating_options = st.sidebar.slider('Select a range of ratings:',
                                        min_value=df.aggregate_rating.min(),
                                        max_value=df.aggregate_rating.max(),
                                        value=(df.aggregate_rating.min(),df.aggregate_rating.max())
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
st.title('Restaurants')

with st.container():
# Order Metric
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        is_delivering = df.is_delivering_now.sum()
        col1.metric('Is delivering', is_delivering)
    with col2:
        n_table_booking = df.has_table_booking.sum()
        col2.metric('Has table booking', n_table_booking)          
    with col3:
        n_online_delivery = df.has_online_delivery.sum()
        col3.metric('Has online delivery', n_online_delivery)
    with col4:
        n_online_delivery = (df.loc[df.average_cost_for_two_USD == df.average_cost_for_two_USD.max()]
                               .sort_values(by='restaurant_id')
                               .head(1).restaurant_name.values[0])
        col4.metric('Highest dish for two Restaurant', n_online_delivery)
        
with st.container():
# Order Metric
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Average cost for two per Ratings</h2>",
                unsafe_allow_html=True)
    fig = scatter_plot(df)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Top 15 Restaurants (by ratings & votes)</h2>",
                unsafe_allow_html=True)
    aux = table_top_15(df)
    st.dataframe(aux)
    
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Average cost for two (US$) by cuisines</h2>",
                unsafe_allow_html=True)
    fig = bar_plot(df, 'cuisines', 'cuisines', 'average_cost_for_two_USD', 'US$', 'mean')
    # fig = bar_plot_per_country(df, 'cuisines', '#_cuisines', 'mean')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown("<h3 style='text-align: center; color: #129fa5;'>Cuisines diversity</h2>",
                unsafe_allow_html=True)
    fig = treemap_plot(df)
    st.plotly_chart(fig, use_container_width=True)
       
