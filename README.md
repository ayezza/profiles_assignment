# profiles_assignment

New methods to assign profiles to activities

# MCAP Profiles

Un package Python pour l'affectation des profils aux activités basé sur les compétences.

## Installation


## Utilisation

bash
Utilisation avec les paramètres par défaut
mcap


## Utilisation avec des fichiers personnalisés

mcap --mca chemin/vers/mca.csv --mcp chemin/vers/mcp.csv --scale free


## Aide
mcap --help


## Format des fichiers d'entrée

Les fichiers CSV doivent avoir le format suivant :

### MCA (Matrix Compétences-Activités) - example

csv
Activity,Comp1,Comp2,Comp3,...

Act1,0.8,0.6,0.4,...

Act2,0.5,0.9,0.3,...


### MCP (Matrix Compétences-Profils)

csv
Profile,Comp1,Comp2,Comp3,...

Prof1,0.9,0.5,0.3,...

Prof2,0.4,0.8,0.6,...


## Licence

Ce projet est sous licence MIT.

