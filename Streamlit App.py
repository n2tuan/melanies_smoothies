# Import python packages
import streamlit as st
import os
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie.
  """
)

name_on_order = st.text_input('Name on Smoothies:')
st.write('Name on your Smoothie will be: ', name_on_order)

#session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()

df_fruits = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
#st.dataframe(data=df_fruits)
ingredients = st.multiselect(
                'Choose up to 5 ingredients?',
                df_fruits,
                max_selections=5
)
if ingredients:
    #st.write('You selected: ', ingredients)
    #st.text(ingredients)
    #ingredients_list = ' '.join(ingredients)
    ingredients_list = ''
    for fruit in ingredients:
        ingredients_list += fruit + ' '

        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.text(ingredients_list)

    stmt = """insert into smoothies.public.orders(name_on_order, ingredients)
    values('"""+ name_on_order +"""','"""+ ingredients_list+"""')
    """
    #st.text(stmt)

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

