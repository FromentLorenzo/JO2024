# Rapport Projet JO2024
## Auteurs: Podda Valentin, Froment Lorenzo

## Introduction
Contexte: Rapport du projet final traitant des données à propos de Jeux Olympiques 2024.

Objectif: Concevoir et mettre en œuvre une application innovante basée sur les compétences en web de données, ingénierie des connaissances et web semantique.


### Modélisation ontologique en OWL et SKOS:

Concernant la modélisation SKOS, nous avons choisi de représenter les sports des Jeux Olympiques en les organisant hiérarchiquement en catégories générales, comme les sports individuels, les sports d’équipe ou les sports aquatiques. À partir de ces catégories principales, nous avons défini des concepts plus spécifiques représentant des disciplines comme la natation, l’escrime ou le football. Chaque concept est enrichi par des informations comme une étiquette préférée (**skos:prefLabel**) et une définition (**skos:definition**).

Par exemple, le concept **sse:Individual_Sports** regroupe des disciplines comme le tir à l’arc, la musculation ou l’équitation, tandis que **sse:Team_Sports** inclut des sports tels que le basketball, le rugby à 7 ou le volleyball. Ces relations hiérarchiques sont exprimées avec des propriétés telles que **skos:broader** et **skos:narrower**.

Pour le OWL, nous avons conçu une ontologie qui représente les entités clés, leurs propriétés et les relations entre elles. Cette ontologie se concentre sur les concepts centraux des Jeux, comme les athlètes, les épreuves, les résultats et les lieux.

La classe **Athlete** joue un rôle central dans notre ontologie, car elle représente les participants individuels aux épreuves. Chaque athlète est nécessairement associé à un pays qu’il représente, ce qui est exprimé par la propriété **representsCountry**. Pour garantir la cohérence des données, une restriction OWL limite cette relation à un seul pays par athlète. De plus, un athlète doit obligatoirement participer à au moins une épreuve, une contrainte que nous avons exprimée à l’aide d’une restriction OWL sur la propriété **epreuve**.

Les épreuves sont modélisées par la classe **Epreuve**, qui représente une compétition spécifique au sein d’un sport. Par exemple, le 100 mètres appartient à la catégorie de l’athlétisme, et cette relation est exprimée par la propriété **epreuve**, reliant une épreuve à un sport. Chaque épreuve est également associée à un lieu spécifique, modélisé par la classe **Venue** et relié via la propriété **venue**. Ces relations permettent de structurer clairement où et dans quel contexte se déroulent les compétitions.
etc ...

### Construction des graphes de connaissances

Pour les données textuelles non structurées, nous avons récupéré un fichier PDF sur le site des Jeux Olympiques de Paris 2024 contenant la liste des lieux et des épreuves associées. Après extraction du texte, nous avons utilisé le modèle REBEL pour générer des triplets RDF à partir des relations présentes dans le document, comme (Aquatics Centre, located in, Saint-Denis). Ces triplets ont ensuite été intégrés dans notre graphe.

## Enrichissement du graphe de connaissances

Les données structurées étaient des données provenant d'un fichier csv regroupant toutes les médailles remportées durant ces Jeux avec le nom de l'athlète/équipe, le pays et l'épreuve. Nous avons effectué une transformation csv2rdf et utilisé l'API du journal The Guardian afin de proposer des articles à propos de l'athlète, mais aussi nous avons essayé d'utilisé l'API SPARQL de DBpedia pour récupérer la date de naissance, la taille et le poids des athlètes.

## Interface

Pour représenter nos données, nous avons utilisé la bibliothèque Python Streamlit, qui nous permet de créer une interface simple et intuitive. Cette interface affiche dans un premier temps une liste de tous les sports sous forme de menu déroulant. En sélectionnant un sport, l’utilisateur peut explorer les épreuves associées, puis découvrir les athlètes médaillés pour chaque épreuve.