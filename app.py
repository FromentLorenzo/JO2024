import streamlit as st
from rdflib import Graph, Namespace

SE = Namespace("http://example.org/olympics2024/schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

rdf_data_graph = Graph()
rdfs_ontology_graph = Graph()
skos_graph = Graph()

rdf_data_graph.parse("og24_data.ttl", format="turtle") 
rdfs_ontology_graph.parse("se_schema.ttl", format="turtle") 
skos_graph.parse("se_skos.ttl", format="turtle") 

combined_graph = rdf_data_graph + rdfs_ontology_graph + skos_graph

sports_query = f"""
SELECT DISTINCT ?sport ?sportLabel
WHERE {{
    ?sport a <{SE.Sport}> ;
           <{RDFS.label}> ?sportLabel .
}}
"""

# Execute the query to get all sports
sports_results = combined_graph.query(sports_query)

athletes_data = {}

# For each sport, query its athletes and their countries
for sport_row in sports_results:
    sport_label = str(sport_row['sportLabel'])  # Label of the sport
    # Query to get athletes and their countries for the current sport
    athletes_query = f"""
    SELECT ?athleteName ?countryName
    WHERE {{
        ?sport <{SE.epreuve}> ?epreuve .
        ?epreuve <{SE.results}> ?result .
        ?result <{SE.athleteOfResult}> ?athlete .
        ?athlete <{RDFS.label}> ?athleteName ;
                 <{SE.representsCountry}> ?country .
        ?country <{RDFS.label}> ?countryName .
    }}
    """
    
    # Execute the query
    athletes_results = combined_graph.query(athletes_query, initBindings={'sport': sport_row['sport']})
    
    # Collect athletes for this sport
    athletes_list = []
    for row in athletes_results:
        athlete_name = str(row['athleteName'])
        country_name = str(row['countryName'])
        athletes_list.append(f"{athlete_name} ({country_name})")
    
    # Store the athletes list under the sport's label
    athletes_data[sport_label] = athletes_list

# Print the resulting dictionary
print("athletes_data = {")
for sport, athletes in athletes_data.items():
    print(f'    "{sport}": {athletes},')
print("}")

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Sports and Athletes</h1>", unsafe_allow_html=True)

# Placeholder function triggered when an athlete's name is clicked
def on_athlete_click(name):
    st.write(f"Function triggered for: {name}")  # Placeholder functionality

# Function to display athletes based on selected sport
def display_athletes(sport):
    # Display the list of athletes for the selected sport
    athletes = athletes_data.get(sport, [])
    if athletes:
        for athlete in athletes:
            if st.button(athlete, key=f"{sport}_{athlete}"):  # Make athlete names clickable
                on_athlete_click(athlete)  # Call the placeholder function
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
