import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.pyplot as plt
import datetime

# Configurer le logging
logging.basicConfig(
    filename='file_changes.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.events = []

    def on_modified(self, event):
        if event.is_directory:
            return
        message = f"Fichier modifié: {event.src_path}"
        logging.info(message)
        print(message)
        self.events.append((datetime.datetime.now(), event.src_path))

    def get_events(self):
        return self.events

def monitor_directory(path_to_watch):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return event_handler.get_events()

def plot_events(events):
    if not events:
        print("Aucun événement détecté.")
        return

    times = [event[0] for event in events]
    files = [os.path.basename(event[1]) for event in events]

    plt.figure(figsize=(10, 6))
    plt.plot(times, range(len(times)), marker='o', label='Modifications')
    plt.yticks(range(len(files)), files)
    plt.xlabel('Temps')
    plt.ylabel('Fichiers')
    plt.title('Événements de modification de fichiers')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    path = input("Entrez le chemin du répertoire à surveiller : ")
    if not os.path.exists(path):
        print("Le chemin spécifié n'existe pas.")
    else:
        print(f"Surveillance du répertoire : {path}")
        events = monitor_directory(path)
        plot_events(events)

# Atention si vous ouvrez le fichiez qui stock les log, vous allez créé une boucle infini
# qui n'arette pas d'enregistrer des changements
