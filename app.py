import streamlit as st
from rdflib import Graph, Namespace

# Namespaces
SE = Namespace("http://example.org/olympics2024/schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Initialize RDF Graphs
rdf_data_graph = Graph()
rdfs_ontology_graph = Graph()
skos_graph = Graph()

# Load RDF Data
rdf_data_graph.parse("og24_data.ttl", format="turtle")
rdfs_ontology_graph.parse("se_schema.ttl", format="turtle")
skos_graph.parse("se_skos.ttl", format="turtle")

# Combine all graphs
combined_graph = rdf_data_graph + rdfs_ontology_graph + skos_graph

# Query to retrieve all sports from SKOS concepts
sports_query = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX sse: <http://example.org/olympics2024/skos#>

SELECT DISTINCT ?sport ?sportLabel
WHERE {
    ?sport a skos:Concept ;
           skos:prefLabel ?sportLabel .
    FILTER NOT EXISTS { ?sport skos:narrower ?child . }
}
"""

# Execute the query to get all sports
sports_results = combined_graph.query(sports_query)

# Dictionary to store athletes data for each sport
athletes_data = {}

# For each sport, query its athletes and their countries
for sport_row in sports_results:
    sport_uri = sport_row['sport']  # URI of the sport
    sport_label = str(sport_row['sportLabel'])  # Label of the sport

    # Query to get athletes and their details for the current sport
    athletes_query = """
    PREFIX se: <http://example.org/olympics2024/schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?athleteName ?countryLabel ?eventLabel ?medalLabel
    WHERE {
        # Link events to the specific sport
        ?event se:epreuve ?sport .
        
        # Link results to events and athletes
        ?result se:epreuve ?event ;
                se:athleteOfResult ?athlete ;
                se:value ?medal .

        # Get athlete details
        ?athlete rdfs:label ?athleteName ;
                 se:representsCountry ?country .

        # Get country details
        ?country rdfs:label ?countryLabel .

        # Get event and medal details
        ?event rdfs:label ?eventLabel .
        ?medal rdfs:label ?medalLabel .
    }
    ORDER BY ?athleteName
    """

    # Execute the query for the current sport
    athletes_results = combined_graph.query(athletes_query, initBindings={'sport': sport_uri})

    # Collect athletes for this sport
    athletes_list = []
    for row in athletes_results:
        athletes_list.append(row)

    # Store the athletes list under the sport's label
    athletes_data[sport_label] = athletes_list

# Streamlit App Layout
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Sports and Athletes</h1>", unsafe_allow_html=True)

# Placeholder function triggered when an athlete's name is clicked
def on_athlete_click(row):
    # QUERY THE GUARDIAN
    st.write(f"Country: {str(row['countryLabel'])}") 
    st.write(f"Event: {str(row['eventLabel'])}") 
    st.write(f"Medal: {str(row['medalLabel'])}") 

# Function to display athletes based on the selected sport
def display_athletes(sport):
    athletes = athletes_data.get(sport, [])
    if athletes:
        for index, athlete in enumerate(athletes):  # Use index to ensure unique keys
            if st.button(str(athlete['athleteName']), key=f"{sport}_{index}"):
                on_athlete_click(athlete)
    else:
        st.write("No athletes found for this sport.")

# Display sports in a 3x3 grid
sports_list = list(athletes_data.keys())
columns = st.columns(3)

for i, sport in enumerate(sports_list):
    column = columns[i % 3]
    with column:
        with st.expander(sport, expanded=False):
            display_athletes(sport)
