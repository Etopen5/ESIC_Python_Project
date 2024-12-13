import os
import shutil
from datetime import datetime

# Chemin du dossier Téléchargements
download_folder = os.path.expanduser("~\Downloads")
date = datetime.now().strftime("%Y-%m-%d")
log = date + "_log.txt"
log_directory = os.path.join(download_folder, "log")
log_file = os.path.join(log_directory, log)

def create_folder(folder_path):
    """Créer un dossier s'il n'existe pas."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def log_action(action, file_name, target_folder):
    """Enregistre une action dans le fichier log."""
    with open(log_file, "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {action}: {file_name} -> {target_folder}\n")

def sort_files_by_extension(download_folder):
    """Trie les fichiers par extension dans des sous-dossiers."""
    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
    
        # Ignorer les dossiers et le fichier log
        if os.path.isdir(file_path) or file_name.split("_")[-1] == "log.txt":
            continue

        # Obtenir l'extension du fichier
        file_extension = os.path.splitext(file_name)[1].lower().strip('.')
        target_folder = os.path.join(download_folder, file_extension if file_extension else "autres")

        try:
            # Créer le dossier cible
            create_folder(target_folder)

            # Déplacer le fichier
            shutil.move(file_path, target_folder)

            # Journaliser l'action
            log_action("Déplacé", file_name, target_folder)
        except Exception as e:
            # Journaliser une éventuelle erreur
            log_action("Erreur", file_name, str(e))

if __name__ == "__main__":
    create_folder(log_directory)
    
    # Créer le fichier log au début s'il n'existe pas déjà
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("Journal des actions de tri du "+date+"\n")
            log.write("==================================================\n\n")
    
    # Trier les fichiers
    sort_files_by_extension(download_folder)

    print(f"Tri terminé. Les actions sont consignées dans {log_file}")
