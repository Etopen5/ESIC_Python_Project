import pandas as pd
import re
import os 
import sys 
from datetime import datetime

# Chemin vers le fichier de logs web
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
LOG_FILE = os.path.join(script_directory,"access.log.txt")
REPORT_FILE = "intrusion_report.txt"



# Expressions régulières pour détecter des attaques courantes
PATTERNS = {
    "directory_traversal": r"\.\./",  # Tentatives de traversée de répertoires
    "sql_injection": r"(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|--|;|\')",  # Tentatives d'injection SQL
    "xss_attack": r"(<script>|%3Cscript%3E|onerror=|javascript:)",  # Tentatives d'injection XSS
    "suspicious_user_agents": r"(sqlmap|nmap|curl|nikto|wpscan|fuzzer)",  # Bots malveillants
}

def parse_log_line_to_dict(line):
    #Analyse une ligne de journal et extrait les champs pertinents.
    log_pattern = r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(log_pattern, line)
    if match:
        return {
            "ip": match.group(1),
            "datetime": match.group(4),
            "request": match.group(5),
            "status": match.group(6),
            "size": match.group(7),
            "referrer": match.group(8),
            "user_agent": match.group(9),
        }
    return None

def load_logs_to_dataframe(log_file):
    #Charge les logs dans un DataFrame Pandas.
    logs_data = []
    with open(log_file, "r", encoding="utf-8") as logs:
        for line in logs:
            log_entry = parse_log_line_to_dict(line)
            if log_entry:
                logs_data.append(log_entry)

    # Créer un DataFrame à partir des données collectées
    return pd.DataFrame(logs_data)

def detect_intrusions(df):
    #Ajoute des colonnes indiquant les types d'intrusion détectés.
    df["directory_traversal"] = df["request"].str.contains(PATTERNS["directory_traversal"], regex=True, case=False, na=False)
    df["sql_injection"] = df["request"].str.contains(PATTERNS["sql_injection"], regex=True, case=False, na=False)
    df["xss_attack"] = df["request"].str.contains(PATTERNS["xss_attack"], regex=True, case=False, na=False)
    df["suspicious_user_agents"] = df["user_agent"].str.contains(PATTERNS["suspicious_user_agents"], regex=True, case=False, na=False)

    # Filtrer les lignes avec au moins une attaque détectée
    df["is_intrusion"] = df[["directory_traversal", "sql_injection", "xss_attack", "suspicious_user_agents"]].any(axis=1)
    return df[df["is_intrusion"]]

def save_report(df_intrusions, report_file):
    #Enregistre les intrusions détectées dans un fichier texte.
    with open(report_file, "w", encoding="utf-8") as report:
        report.write("Rapport de détection des tentatives d'intrusion\n")
        report.write("=" * 50 + "\n\n")
        for _, row in df_intrusions.iterrows():
            report.write(f"[{row['datetime']}] {row['ip']} - Intrusion détectée\n")
            report.write(f"Requête : {row['request']}\n")
            report.write(f"User-Agent : {row['user_agent']}\n")
            if row["directory_traversal"]:
                report.write("- Type : Traversée de répertoires\n")
            if row["sql_injection"]:
                report.write("- Type : Injection SQL\n")
            if row["xss_attack"]:
                report.write("- Type : Injection XSS\n")
            if row["suspicious_user_agents"]:
                report.write("- Type : User-Agent suspect\n")
            report.write("-" * 50 + "\n")

    print(f"Analyse terminée. Rapport enregistré dans {report_file}")

if __name__ == "__main__":
    # Charger les logs dans un DataFrame
    df_logs = load_logs_to_dataframe(LOG_FILE)
    if df_logs.empty:
        print("Aucun log valide trouvé.")
    else:
        # Détecter les intrusions
        df_intrusions = detect_intrusions(df_logs)

        # Sauvegarder le rapport
        save_report(df_intrusions, REPORT_FILE)
