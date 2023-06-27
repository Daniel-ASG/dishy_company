# ========================================
# Import libraries
# ========================================

import folium
import inflection
import streamlit  as st

from PIL import Image

# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Home',
                   page_icon='🍛',
                   layout='wide'
                  )

# #########################
#         Sidebar
# #########################

image = Image.open('logo.png')
st.sidebar.image(image, width=300)

st.sidebar.markdown('# Dishy ')
st.sidebar.markdown('## Delights at your fingertips')

st.sidebar.markdown('''___''')
st.sidebar.markdown('##### Powered by Comunidade DS')
st.sidebar.markdown('##### Data Analyst: Daniel Gomes')

st.write("# Dishy Dashboard")
st.markdown(
    '''
    ### This dashboard is designed to track restaurant growth metrics on its platform.
    ### How to use this Dashboard?
    - Overview:
    
        - General behavioral metrics.
        - Geolocation distribution.
    - Countries:
        - Information regarding country-level indicators.
    - Cities:
        - Information regarding city-level indicators.
    - Restaurants:
        - Information regarding restaurans-level indicators.
        
    ### Ask for help
    - Data Science Team on Discord
        - @daniel_asg
    - For more information, please visit the [project page on GitHub](https://github.com/Daniel-ASG/dishy_company/tree/main). Thanks for your visit.
    
    ''')
