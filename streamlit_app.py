import streamlit as st

Chat_bot = st.Page("Chat_bot.py", title = "Lab 1")
Currency = st.Page("Currency.py", title = "Lab 2")

pg = st.navigation([Chat_bot, Currency])
st.set_page_config(page_title="Labs")

pg.run()