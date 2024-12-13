import time
import random
import matplotlib.pyplot as plt

# Simulated service with a password
class SimulatedService:
    def __init__(self, password):
        self.password = password

    def authenticate(self, attempt):
        time.sleep(0.1)  # Simulate network delay
        return attempt == self.password

# Perform brute force attack
def brute_force_attack(service, password_list):
    attempts = []
    success = 0
    failures = 0

    for password in password_list:
        is_success = service.authenticate(password)
        attempts.append((password, is_success))

        if is_success:
            success += 1
            print(f"Tentative réussie : {password}")
            break
        else:
            failures += 1
            print(f"Échec avec : {password}")

    return attempts, success, failures

# Generate a report and visualize results
def visualize_results(attempts):
    successful_attempts = len([attempt for attempt in attempts if attempt[1]])
    failed_attempts = len(attempts) - successful_attempts

    # Display statistics
    print(f"Total des tentatives : {len(attempts)}")
    print(f"Tentatives réussies : {successful_attempts}")
    print(f"Tentatives échouées : {failed_attempts}")

    # Plot results
    labels = ['Réussites', 'Échecs']
    counts = [successful_attempts, failed_attempts]
    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=['green', 'red'])
    plt.xlabel('Résultat')
    plt.ylabel('Nombre de tentatives')
    plt.title('Résultats des tentatives de brute force')
    plt.show()

if __name__ == "__main__":
    # Simulated service password
    actual_password = "secure123"
    service = SimulatedService(actual_password)

    # Common password list
    common_passwords = [
        "123456", "password", "123456789", "12345678", "12345", "1234567",
        "qwerty", "azerty", "123Qwerty", "123Azerty", "abc123", "password1", "secure123", "letmein"
    ]
    print("Lancement de l'attaque de brute force...")
    attempts, success, failures = brute_force_attack(service, common_passwords)

    print("\nVisualisation des résultats...")
    visualize_results(attempts)
