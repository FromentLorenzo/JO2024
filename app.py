import streamlit as st

# Simulated data for athletes (you can replace this with actual API data or database queries)
athletes_data = {
    "Basketball": ["LeBron James", "Kevin Durant", "Stephen Curry", "Giannis Antetokounmpo"],
    "Football": ["Lionel Messi", "Cristiano Ronaldo", "Neymar", "Kylian Mbappé"],
    "Tennis": ["Roger Federer", "Serena Williams", "Novak Djokovic", "Rafael Nadal"],
    "Swimming": ["Michael Phelps", "Katie Ledecky", "Caeleb Dressel", "Simone Manuel"],
    "Athletics": ["Usain Bolt", "Mo Farah", "Shelly-Ann Fraser-Pryce", "Eliud Kipchoge"],
    "Cycling": ["Chris Froome", "Eddy Merckx", "Lance Armstrong", "Mark Cavendish"]
}

# Set page config to make it wide
st.set_page_config(layout="wide")

# Title of the Streamlit app
st.markdown("<h1 style='text-align: center;'>Sports and Athletes</h1>", unsafe_allow_html=True)

# Function to display athletes based on selected sport
def display_athletes(sport):
    # Display the list of athletes for the selected sport
    athletes = athletes_data.get(sport, [])
    if athletes:
        for athlete in athletes:
            st.write(f"- {athlete}")
    else:
        st.write("No athletes found for this sport.")

# Display sports in a 3x3 grid
sports_list = list(athletes_data.keys())
columns = st.columns(3)  # Create 3 columns for the grid layout

# Loop through sports and place them in the columns
for i, sport in enumerate(sports_list):
    column = columns[i % 3]  # This ensures the sports are distributed in the 3 columns
    with column:
        with st.expander(sport, expanded=False):
            display_athletes(sport)
