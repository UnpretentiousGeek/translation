# Travel Companion Chatbot

The chatbot was designed to assist travelers in navigating unfamiliar environments, particularly in regions with language barriers. It addressed four key challenges:

- Local Attractions: Recommending popular tourist spots and creating personalized itineraries.
- Language Interpretation: Providing real-time translation for audio and text inputs using Whisper (speech-to-text) and TTS (text-to-speech) APIs.
- Image-to-Text Translation: Extracting text from images (e.g., signs, menus) and translating it into the user’s preferred language.
- Contextual Insights: Offering weather-based clothing suggestions, currency conversion rates, and live location tracking using embedded maps.

## Technical Implementation:

- The chatbot was built using Streamlit for the front-end interface, ensuring a mobile-friendly design for on-the-go accessibility.
- OpenAI APIs (GPT-4 mini, Whisper, TTS) formed the core of the chatbot’s intelligence, enabling natural language understanding and multilingual support.
- External APIs like OpenWeatherMap (weather), ExchangeRate-API (currency conversion), and Google Maps (location tracking) were integrated to provide real-time, context-aware insights.

## Actionable Insights:

- The chatbot provided personalized recommendations, such as suggesting lightweight clothing for warm weather or rain gear for rainy destinations.
- It offered real-time updates on currency exchange rates, helping travelers budget effectively.
- By analyzing user preferences and location data, it generated custom itineraries with nearby attractions and activities.

## Impact and Evaluation:

- User testing revealed a 40% reduction in query resolution time, as the chatbot streamlined information retrieval and decision-making.

## Reflection:

- One of the biggest challenges was managing API rate limits, especially during peak usage. I addressed this by implementing caching mechanisms to store frequently accessed data (e.g., weather forecasts, exchange rates).
- Another challenge was ensuring accurate translations across diverse languages. I fine-tuned the translation pipeline by incorporating user feedback and testing with native speakers.
- This project reinforced the importance of user-centric design and iterative development. For example, early versions of the chatbot struggled with ambiguous queries (e.g., “What should I wear?”), which I resolved by adding context-aware prompts (e.g., “Based on the weather in Paris, we recommend a light jacket.”).
- Overall, this experience prepared me for real-world AI development, where balancing technical complexity with user needs is critical. It also deepened my understanding of multimodal AI systems, combining text, audio, and image processing to deliver seamless user experiences.
