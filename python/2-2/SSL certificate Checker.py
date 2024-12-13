import ssl
import socket
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Fonction pour récupérer les informations SSL d'un site web
def get_ssl_info(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    return cert

# Fonction pour vérifier la validité des certificats
def check_ssl_certificates(sites):
    results = []
    for site in sites:
        try:
            cert = get_ssl_info(site)
            # Extraire la date d'expiration
            expiry_date_str = cert["notAfter"]
            expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")
            remaining_days = (expiry_date - datetime.now()).days

            results.append({
                "Site": site,
                "Expiry Date": expiry_date,
                "Days Remaining": remaining_days,
                "Status": "Valid" if remaining_days > 0 else "Expired"
            })
        except Exception as e:
            results.append({
                "Site": site,
                "Expiry Date": None,
                "Days Remaining": None,
                "Status": f"Error: {e}"
            })
    return results

# Fonction pour visualiser les résultats sous forme de graphique
def visualize_certificates(results):
    df = pd.DataFrame(results)
    status_counts = df["Status"].value_counts()

    plt.figure(figsize=(8, 6))
    status_counts.plot(kind="bar", color=["green" if "Valid" in s else "red" for s in status_counts.index])
    plt.title("Statut des certificats SSL")
    plt.xlabel("Statut")
    plt.ylabel("Nombre de sites")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

    return df

# Fonction principale
if __name__ == "__main__":
    sites_to_check = [
        "example.com",
        "expired.badssl.com",
        "google.com",
        "self-signed.badssl.com"
    ]

    print("\nVérification des certificats SSL en cours...")
    results = check_ssl_certificates(sites_to_check)

    print("\n--- Résultats de la vérification ---")
    for result in results:
        print(result)

    print("\nVisualisation des résultats...")
    df = visualize_certificates(results)

    # Sauvegarder les résultats dans un fichier CSV
    df.to_csv("ssl_certificates_report.csv", index=False)
    print("Rapport sauvegardé sous 'ssl_certificates_report.csv'.")
