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

from folium.plugins   import MarkerCluster
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



def overview_map(df):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df.iterrows():

        name = line["restaurant_name"]
        price_for_two = round(line["average_cost_for_two_USD"], 2)
        cuisine = line["cuisines"]
        rating = line["aggregate_rating"]
        color = f'{line["rating_color"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: US$ {} for two"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)





# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Overview',
                   page_icon='🔎',
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
st.title('A journey of flavors at the click of a button')


with st.container():
# Order Metric
    st.markdown('## Overall Metrics')
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    with col1:
        n_restaurants = df.restaurant_id.nunique()
        col1.metric('\# Restaurants', n_restaurants)
    with col2:
        n_countries = df.country_code.nunique()
        col2.metric('\# Countries', n_countries)          
    with col3:
        n_cities = df.city.nunique()
        col3.metric('\# Cities', n_cities)
    with col4:
        aux = df.votes.sum()
        col4.metric('\# total of evaluations', aux)            
    with col5:
        aux = df.cuisines.nunique()
        col5.metric('\# Cuisines', aux)
        

with st.container():
    # List of countries 
    st.markdown('## Overview Map')
    overview_map(df)
    