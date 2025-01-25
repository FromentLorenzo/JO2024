from SPARQLWrapper import SPARQLWrapper, JSON

def get_athlete_data(athlete_name):
    # Remplace les espaces par des underscores (format DBpedia)
    athlete_name = athlete_name.replace(" ", "_")
    
    # Endpoint SPARQL de DBpedia
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
     
    # Requête SPARQL
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?property ?value WHERE {{
    dbr:{athlete_name} ?property ?value .
    FILTER (?property IN (dbo:birthDate, dbo:birthPlace, dbo:nationality, dbo:sport, dbo:height, dbo:weight))
    }}
"""

    
    # Configuration de la requête
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # Envoi de la requête
    results = sparql.query().convert()
    
    # Transformation des résultats
    data = []
    for result in results["results"]["bindings"]:
        property_name = result["property"]["value"]
        value = result["value"]["value"]
        data.append({"property": property_name, "value": value})
    
    return data

# Exemple d'utilisation
athlete_name = "Inbar LANIR"
data = get_athlete_data(athlete_name)

# Affiche les résultats
for item in data:
    print(f"{item['property']} : {item['value']}")
