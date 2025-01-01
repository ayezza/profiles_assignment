import os

# Créer la structure des dossiers
directories = [
    'data/input',
    'data/output/figures',
    'config',
    'src/core',
    'src/models',
    'src/utils'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Créé/vérifié: {directory}")

# Vérifier si les fichiers CSV existent
csv_files = {
    'data/input/mca.csv': '''Activity,Comp1,Comp2,Comp3,Comp4,Comp5
Act1,0.8,0.6,0.4,0.7,0.5
Act2,0.5,0.9,0.3,0.6,0.8
Act3,0.7,0.4,0.8,0.5,0.6''',
    
    'data/input/mcp.csv': '''Profile,Comp1,Comp2,Comp3,Comp4,Comp5
Prof1,0.9,0.5,0.3,0.8,0.6
Prof2,0.4,0.8,0.6,0.5,0.7
Prof3,0.6,0.4,0.9,0.7,0.5'''
}

for file_path, content in csv_files.items():
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Créé: {file_path}")
    else:
        print(f"Existe déjà: {file_path}")

print("\nStructure des dossiers et fichiers CSV créée/vérifiée.") 