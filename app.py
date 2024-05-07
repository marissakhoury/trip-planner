from chat_completions import TravelPlannerAgent
import streamlit as st
import json

def display_itinerary(itinerary_json):
    st.title(f"Your Trip to {itinerary_json['destination']}")

    for day in itinerary_json['itinerary']:
        with st.expander(f"Day {day['day']} Activities"):
            for activity in day['activities']:
                st.markdown(f"### {activity['name']}")
                st.markdown(f"**Type**: {activity['type']}")
                st.markdown(f"**Description**: {activity['description']}")
                st.markdown(
                    f"**Location**: [View on Map](https://www.google.com/maps/search/?api=1&query={activity['coordinates']['lat']},{activity['coordinates']['lon']})",
                    unsafe_allow_html=True
                )

def main():
    st.sidebar.title("API Configuration")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key")
    model_choice = st.sidebar.selectbox("Model", ["gpt-3.5-turbo-1106", "gpt-3.5-turbo"])
    st.title('Trip Planner')
    destination = st.text_input('Destination', '')
    number_of_days = st.number_input('Duration of stay', min_value=1)

    if st.button('Show Itinerary'):
        if destination and openai_api_key:
            travel_planner = TravelPlannerAgent(model=model_choice, api_key=openai_api_key)
            response = travel_planner.get_recommendations(number_of_days, destination)
            if response:
                try:
                    response_json = json.loads(response)
                    display_itinerary(response_json)
                except json.JSONDecodeError:
                    st.error('Invalid response format. Please ensure the destination is valid.')
            else:
                st.error('API call failed. Please check your API key and network connection.')
        else:
            st.error('Please enter a destination and ensure your API key is set.')


if __name__ == "__main__":
    main()
