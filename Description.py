import streamlit as st

st.title("✈️ Travel Companion Chatbot: Your Pocket-Sized Travel BFF 🌍💬")

st.markdown("""
Ever found yourself in a foreign country thinking, *"Wait… what does that sign say?"* or *"How much is this in dollars?"* Yeah, same. That’s why I built the **Travel Companion Chatbot** — a smart, all-in-one assistant to make globetrotting smoother, smarter, and a whole lot more fun. 🧳💡
""")

with st.expander("🔍 What It Does (AKA Why It’s Your New Favorite Travel Buddy)", expanded=True):
    st.markdown("""
- 🗺 **Explore Like a Local**: Personalized itineraries + hot tourist spot recs = less Googling, more vibing.  
- 🗣 **Lost in Translation? Never Again**: Real-time voice & text translation powered by OpenAI Whisper + TTS. Speak your language, get instant answers.  
- 📸 **Snap & Translate**: Take a pic of a menu or street sign — boom, instant translation. Magic? Nah, just tech.  
- 🧠 **Smart Suggestions**: Weather-based outfit ideas, currency conversions, and live maps to keep you prepped and in the know.  
""")

with st.expander("🛠 How It Works (Tech Stack but Make It Cool)", expanded=True):
    st.markdown("""
- **Streamlit** for the sleek, mobile-friendly interface. Swipeable and snackable.  
- **OpenAI APIs** (GPT-4 mini, Whisper, TTS) for multilingual convos and smooth natural language understanding.  
- **Third-party APIs** like:
    - 🌦 **OpenWeatherMap** (so you never get caught in the rain without an umbrella)  
    - 💱 **ExchangeRate-API** (to make sure you’re not overpaying for that croissant)  
    - 📍 **Google Maps API** (to always know where you are, and what’s around)  
""")

with st.expander("📊 What It Did (AKA 'Receipts or it didn’t happen')", expanded=True):
    st.markdown("""
- ⏱️ **Reduced info search time by 40%** during user tests.  
- 🤖 Delivered *context-aware*, personalized answers instead of generic replies.  
- 👕 Suggested the perfect ‘fit for the weather. Paris in spring? Light jacket. Tokyo in summer? Linen all the way.  
""")

with st.expander("💡 Real-World Wins (Actionable Insights)", expanded=True):
    st.markdown("""
- Real-time, geo-based suggestions → smarter decisions *on the fly*.  
- Custom itineraries based on user vibes and preferences.  
- Helped users travel more confidently, even in places where they didn’t know the language or the local customs. (Big win 🏆)  
""")

with st.expander("🔄 Behind the Scenes: Lessons + Glow-Ups ✨", expanded=True):
    st.markdown("""
- **API rate limits** were a pain (💀) — solved it with smart caching to keep things smooth even during rush hours.  
- **Translation accuracy** took trial & error — refined it by looping in native speakers and collecting user feedback (they really told me what's up 👀).  
- Early on, users asked vague stuff like *“What should I wear?”* — so I added weather + location context. Now it’s *“In Paris? 60°F? Bring that light jacket, bestie.”*  
""")

with st.expander("🧠 Takeaways", expanded=True):
    st.markdown("""
Building this chatbot was a deep dive into **real-world AI** meets **user-first design**. It taught me how to balance *cutting-edge tech* with actual human needs — and how to make AI feel more like a friendly guide than a cold machine.

Also: multimodal AI is the future 🚀. Mixing **text + voice + images** to make something truly helpful? Count me in.
""")

st.markdown("---")
st.success("Still thinking about packing lists or lost translations? This bot’s got your back. 🧳📱🌎")
