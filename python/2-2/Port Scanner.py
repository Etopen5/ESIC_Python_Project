import socket
import matplotlib.pyplot as plt

# Fonction pour scanner un port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            if s.connect_ex((ip, port)) == 0:
                return True
    except socket.error:
        return False
    return False

# Fonction principale pour scanner une liste de ports
def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        if scan_port(ip, port):
            open_ports.append(port)
    return open_ports

# Fonction pour afficher les résultats sous forme de graphique
def plot_results(ports, open_ports):
    status = ['Ouvert' if port in open_ports else 'Fermé' for port in ports]
    colors = ['green' if s == 'Ouvert' else 'red' for s in status]

    plt.figure(figsize=(10, 6))
    plt.bar(ports, [1] * len(ports), color=colors, edgecolor='black')
    plt.xticks(ports, rotation=90)
    plt.yticks([])
    plt.xlabel('Ports')
    plt.title('Statut des ports sur la cible')
    
    for i, port in enumerate(ports):
        plt.text(port, 0.5, status[i], ha='center', va='center', color='white', fontsize=8)

    plt.show()

if __name__ == "__main__":
    target_ip = input("Entrez l'adresse IP de la cible : ")
    ports_to_scan = list(range(20, 1025))  # Exemple : ports 20 à 1024

    print(f"Scan des ports sur {target_ip}...")
    open_ports = scan_ports(target_ip, ports_to_scan)

    print(f"Ports ouverts : {open_ports}")
    plot_results(ports_to_scan, open_ports)
