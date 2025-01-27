# JO2024

requirements: 
%pip install rdflib
%pip install streamlit

Pour lancer l'application:
``` 
streamlit run app.py
```


### Construction des données
Pour lifter le fichier csv en RDF, nous avons utilisé le script csv2rdf.py:
```
./csv2rdf -t data.csv -u metadata.json -o data.ttl -m minimal
```
### Explication des dossiers et programmes
Le dossier "**SPARQL_requetes**" contient des requetes fédérées simples permettant d'utiliser l'API sparql de DBpedia ainsi que celle du journal The Guardian afin d'enrichir les données.

Le dossier "**sparql-micro-service**" contient un projet GitHub fourni par l'enseignant M. Franck Michel, permettant d'exploiter l'architecture des micro-services SPARQL. Ce projet a pour objectif de faciliter l'interrogation des API Web en utilisant des requêtes SPARQL.

le dossier "**triplets**" contient un json regroupant tous les triplets créés à partir du fichier PDF des JO2024. (qu'on peut retrouver page par page dans les fichier texte associés)

"**app.py**" est le fichier principal de l'application Streamlit. Il permet de lancer l'interface utilisateur et d'effectuer les requêtes SPARQL pour récupérer les données.

"**extract_Triplets_From_Text.ipynb**" est un notebook permettant d'utiliser le model REBEL pour extraire les triplets des fichiers textes extrait du PDF des JO2024.

"**generate.ipynb**" est un notebook permettant de créer tous les triplets RDF à partir d'un fichier CSV contenant des chaînes de caractères. Il convertit ces données en format RDF, les lie entre elles, et y ajoute les informations extraites du texte.

"**merge.py**" est un script permettant de réunir toutes les données des fichiers triplets.txt en un seul fichier merged.json, en convertissant les données au format JSON si nécessaire.

Ensuite nous avons tous les fichiers de données:
og24_data.ttl, og24_pre_data.ttl, og24_shacl.ttl,se_schema.ttl, se_skos.ttl

