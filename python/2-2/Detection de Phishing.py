import re
import os
import json
from collections import Counter

# Fonction pour vérifier si une adresse e-mail est suspecte
def is_suspicious_email(sender):
    domains_to_watch = [".ru", ".cn", ".info", ".xyz"]  # Domaines couramment utilisés pour le phishing
    if any(sender.endswith(domain) for domain in domains_to_watch):
        return True
    return False

# Fonction pour vérifier les liens suspects dans le contenu
def contains_suspicious_links(content):
    links = re.findall(r'http[s]?://\S+', content)
    for link in links:
        if "bit.ly" in link or not re.match(r'http[s]?://[\w.-]+', link):
            return True
    return False

# Analyse des e-mails pour détecter les signes de phishing
def analyze_emails(email_samples):
    phishing_emails = []
    stats = Counter()

    for email in email_samples:
        sender = email.get("sender", "")
        content = email.get("content", "")

        is_phishing = False

        if is_suspicious_email(sender):
            is_phishing = True
            stats['suspicious_sender'] += 1

        if contains_suspicious_links(content):
            is_phishing = True
            stats['suspicious_links'] += 1

        if is_phishing:
            phishing_emails.append(email)
            stats['phishing_detected'] += 1

        stats['total_emails'] += 1

    return phishing_emails, stats

# Génération d'un rapport des e-mails suspects
def generate_report(phishing_emails, stats):
    report = {
        "total_emails_analyzed": stats['total_emails'],
        "total_phishing_detected": stats['phishing_detected'],
        "percentage_phishing": round((stats['phishing_detected'] / stats['total_emails']) * 100, 2) if stats['total_emails'] > 0 else 0,
        "phishing_emails": phishing_emails
    }

    with open("phishing_report.json", "w") as report_file:
        json.dump(report, report_file, indent=4)

    return report

# Affichage des statistiques
def display_statistics(stats):
    print("Statistiques des e-mails analysés :")
    print(f"- Total d'e-mails analysés : {stats['total_emails']}")
    print(f"- E-mails détectés comme phishing : {stats['phishing_detected']}")
    print(f"- Pourcentage d'e-mails phishing : {round((stats['phishing_detected'] / stats['total_emails']) * 100, 2)}%" if stats['total_emails'] > 0 else "0%")

if __name__ == "__main__":
    # Exemple d'échantillons d'e-mails (ces données peuvent être chargées depuis un fichier si besoin)
    email_samples = [
        {"sender": "john.doe@trusted.com", "content": "Bonjour, voici un lien pour vous connecter : http://secure-login.com"},
        {"sender": "fraud@phishing.ru", "content": "Cliquez ici pour récupérer votre compte : http://bit.ly/fake"},
        {"sender": "support@service.xyz", "content": "Votre compte est compromis. Connectez-vous ici : http://service.xyz"},
        {"sender": "contact@legitbusiness.com", "content": "Votre facture est disponible."}
    ]

    # Analyse des échantillons
    phishing_emails, stats = analyze_emails(email_samples)

    # Génération du rapport
    report = generate_report(phishing_emails, stats)

    # Affichage des statistiques
    display_statistics(stats)

    print("Rapport généré : phishing_report.json")
