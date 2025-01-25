import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, SKOS

# Define namespaces
SE = Namespace("http://example.org/olympics2024/schema#")
EX = Namespace("http://example.org/vocab/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Initialize the graph
g = Graph()
g.bind("se", SE)
g.bind("ex", EX)
g.bind("skos", SKOS)

# Load the SKOS file into the graph
skos_graph = Graph()
skos_file_path = "se_skos.ttl"  # Path to your SKOS file
skos_graph.parse(skos_file_path, format="turtle")

def find_skos_concept(label):
    """Find the SKOS concept URI in the loaded SKOS graph based on its label."""
    for s, p, o in skos_graph.triples((None, SKOS.prefLabel, None)):
        if str(o).lower() == label.lower():  # Match label case-insensitively
            return s
    return None

def process_json_to_ttl(json_file):
    """Process JSON RDF triples from a file and add them to the graph."""
    with open(json_file, "r") as file:
        json_data = json.load(file)
        for triple in json_data:
            head = URIRef(f"http://example.org/{triple['head'].replace(' ', '_')}")
            predicate = URIRef(f"http://example.org/{triple['type'].replace(' ', '_')}")
            
            skos_concept = find_skos_concept(triple['tail'])
            if skos_concept:
                tail = skos_concept  # Reference SKOS concept
            else:
                tail = Literal(triple['tail'], datatype=XSD.string)
            
            g.add((head, predicate, tail))

def process_ttl_to_graph(ttl_file):
    """Process RDF Turtle data from a file and add them to the graph."""
    g.parse(ttl_file, format="turtle")

# Input file paths
json_file_path = "triplets/merged.json"
ttl_file_path = "csv/data.ttl"

# Process data
process_json_to_ttl(json_file_path)
process_ttl_to_graph(ttl_file_path)

# Serialize graph to Turtle format
ttl_data = g.serialize(format="turtle")

# Save to a file or print
with open("output.ttl", "w") as file:
    file.write(ttl_data)

print("Turtle data generated and saved to output.ttl")
