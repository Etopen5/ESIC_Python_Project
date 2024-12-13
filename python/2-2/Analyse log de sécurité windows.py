import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour analyser les logs de sécurité Windows (nouveau format)
def analyze_security_logs(log_file):
    try:
        # Charger les logs depuis un fichier CSV
        logs = pd.read_csv(log_file)
        
        # Vérifier les colonnes nécessaires
        required_columns = ["Mots clés", "Date et heure", "ID de l’événement", "Catégorie de la tâche"]
        for col in required_columns:
            if col not in logs.columns:
                raise ValueError(f"La colonne requise '{col}' est manquante dans le fichier CSV.")
        
        # Filtrer les événements suspects : Tentatives de connexion échouées (ID de l'événement: 4625)
        failed_logons = logs[logs["ID de l’événement"] == 4625]
        
        # Compter les événements par type
        event_counts = logs["ID de l’événement"].value_counts()

        # Générer un rapport des activités suspectes
        report = {
            "total_events": len(logs),
            "failed_logons": len(failed_logons),
            "suspicious_categories": failed_logons["Catégorie de la tâche"].value_counts().to_dict()
        }

        # Sauvegarder le rapport en JSON
        with open("security_report.json", "w") as report_file:
            pd.DataFrame([report]).to_json(report_file, orient="records", indent=4)

        return logs, failed_logons, event_counts, report

    except Exception as e:
        print(f"Erreur lors de l'analyse des logs : {e}")
        return None, None, None, None

# Fonction pour visualiser les événements
def visualize_event_frequencies(event_counts):
    plt.figure(figsize=(10, 6))
    event_counts.plot(kind="bar", color="steelblue")
    plt.title("Fréquence des types d'événements")
    plt.xlabel("ID de l'événement")
    plt.ylabel("Nombre d'occurrences")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

# Fonction principale
if __name__ == "__main__":
    # Demander le chemin du fichier log
    log_file = input("Entrez le chemin du fichier de logs de sécurité Windows (format CSV) : ")

    print("Analyse des logs en cours...")
    logs, failed_logons, event_counts, report = analyze_security_logs(log_file)

    if logs is not None:
        print("\n--- Résultats de l'analyse ---")
        print(f"Total d'événements : {report['total_events']}")
        print(f"Tentatives de connexion échouées : {report['failed_logons']}")
        print("Catégories suspectes :")
        for category, count in report['suspicious_categories'].items():
            print(f"- {category}: {count} fois")

        print("\nVisualisation des fréquences des événements...")
        visualize_event_frequencies(event_counts)

        print("\nRapport des activités suspectes sauvegardé sous 'security_report.json'.")
