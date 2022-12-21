import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My new tutorial')

streamlit.header('Breakfast Menu')
streamlit.text('🎂Omega 3 & Blueberry Oatmeal')
streamlit.text('🥙Kale, Spinach & Rocket Smoothie')
streamlit.text('🍽Hard-Boiled Free-Range Egg')
streamlit.text('Build Your own Fruit Smoothie')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create function for repetative code block
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized

#New Section to make Fruityvice API Response

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
    else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
  streamlit.error()

streamlit.header("Fruit load list contains:")
#snowflake-realted Functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
           my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
           return my_cur.fetchall()
 
# aDD A BUTTON TO LOAD THE FRUIT
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# Allow end user to add fruit to list
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
           my_cur.execute("insert into FRUIT_LOAD_LIST values ('" +papaya+ "')")
      return "Thanks for Adding" + new_fruit
      
add_my_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a fruit to the List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      streamlit.text(back_from_function)




