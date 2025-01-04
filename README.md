# MCAP Profiles 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Un package Python innovant pour l'affectation optimale des profils aux activités basé sur les compétences. Cette solution utilise des algorithmes avancés pour maximiser la correspondance entre les compétences requises pour les activités et les compétences disponibles dans les profils.

## ✨ Fonctionnalités

- Analyse matricielle des compétences
- Affectation automatique des profils
- Support de différentes échelles d'évaluation
- Génération de rapports détaillés
- Interface en ligne de commande intuitive

## 🚀 Installation

```bash
pip install mcap-profiles
```

## 📖 Utilisation

### Utilisation basique

```bash
mcap
```

### Utilisation avancée

```bash
mcap --mca chemin/vers/mca.csv --mcp chemin/vers/mcp.csv --scale free
```

### Options disponibles

```bash
mcap --help
```

## 📋 Format des fichiers d'entrée

### MCA (Matrice Compétences-Activités)

Format CSV requis :

```csv
Activity,Comp1,Comp2,Comp3
Act1,0.8,0.6,0.4
Act2,0.5,0.9,0.3
```

### MCP (Matrice Compétences-Profils)

Format CSV requis :

```csv
Profile,Comp1,Comp2,Comp3
Prof1,0.9,0.5,0.3
Prof2,0.4,0.8,0.6
```

## 📁 Structure du projet

```
mcap-profiles/
├── LICENSE
├── MANIFEST.in
├── README.md
├── setup.py
├── .gitignore
├── main.py
├── config/
│   └── mylogger.ini
├── data/
│   ├── input/
│   │   ├── mca_01.csv
│   │   └── mcp_01.csv
│   └── output/
└── src/
    ├── __init__.py
    ├── core/
    ├── models/
    └── utils/
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📫 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.


