import streamlit as st

Description = st.Page("Description.py", title = "📃 Description")
Chat_bot = st.Page("Chat_bot.py", title = "🤖 Chat")
Currency = st.Page("Currency.py", title = "💵 Currency Converter")

pg = st.navigation([Description, Chat_bot, Currency])
st.set_page_config(page_title="Labs")

pg.run()