import pandas as pd

def unify_date_format(csv_path, output_path):
    # Charger le fichier CSV avec un séparateur probable
    df = pd.read_csv(csv_path, delimiter=',')  # Remplacez ',' par ';' ou '\t' si nécessaire
    print("Colonnes détectées :", df.columns)
    return

# Chemins des fichiers
csv_path = r'C:\Users\33652\Desktop\SI5\WebSemantique\projet\JO2024\paris-2024-results-medals-oly-eng.csv'
output_path = r'C:\Users\33652\Desktop\SI5\WebSemantique\projet\JO2024\paris-2024-results-corrected.csv'

# Exécuter le script
unify_date_format(csv_path, output_path)