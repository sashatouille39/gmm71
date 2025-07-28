#!/usr/bin/env python3
import re
import random

# Lire le fichier events_service.py
with open('/app/backend/services/events_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Exceptions : épreuves qui peuvent garder des taux plus élevés (mais max 70%)
exceptions = [
    "Pont de verre",  # Déjà à 60%, peut rester
    "Bataille royale",  # Déjà modifié à 65%
    "Le Jugement Final"  # Épreuve finale, peut rester élevé à 70%
]

# Fonction pour générer un taux d'élimination varié dans la fourchette 40-60%
def generate_varied_rate():
    # Distribution variée entre 0.4 et 0.6
    rates = [0.42, 0.45, 0.48, 0.50, 0.52, 0.55, 0.58, 0.60]
    return random.choice(rates)

# Traiter chaque ligne
lines = content.split('\n')
current_event_name = ""

for i, line in enumerate(lines):
    # Détecter le nom de l'épreuve actuelle
    if 'name="' in line:
        match = re.search(r'name="([^"]+)"', line)
        if match:
            current_event_name = match.group(1)
    
    # Traiter les taux d'élimination
    if 'elimination_rate=' in line:
        current_rate_match = re.search(r'elimination_rate=([0-9.]+)', line)
        if current_rate_match:
            current_rate = float(current_rate_match.group(1))
            
            # Si le taux est > 60% et n'est pas une exception
            if current_rate > 0.6:
                is_exception = False
                
                # Vérifier si c'est une exception
                for exception in exceptions:
                    if exception in current_event_name:
                        is_exception = True
                        break
                
                if is_exception:
                    if current_event_name == "Le Jugement Final":
                        # Épreuve finale : max 70%
                        new_rate = 0.70
                        lines[i] = re.sub(r'elimination_rate=[0-9.]+', f'elimination_rate={new_rate}  # Exception: Épreuve finale', line)
                    # Pont de verre et Bataille royale restent inchangés (déjà traités)
                else:
                    # Pas une exception : ajuster dans la fourchette 40-60%
                    new_rate = generate_varied_rate()
                    lines[i] = re.sub(r'elimination_rate=[0-9.]+', f'elimination_rate={new_rate}', line)
                    print(f"Corrigé '{current_event_name}': {current_rate} → {new_rate}")

# Réécrire le fichier
content = '\n'.join(lines)
with open('/app/backend/services/events_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Correction des taux d'élimination terminée !")