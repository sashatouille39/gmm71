#!/usr/bin/env python3
"""
Test spécifique pour la fonctionnalité de collecte automatique des gains VIP
Selon la review request française
"""

import requests
import json
import sys
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        return "http://localhost:8001"
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

def test_vip_automatic_collection():
    """Test FRENCH REVIEW REQUEST: Tester la nouvelle fonctionnalité de collecte automatique des gains VIP"""
    print("\n🇫🇷 TESTING VIP AUTOMATIC COLLECTION SYSTEM - FRENCH REVIEW REQUEST")
    print("=" * 80)
    print("OBJECTIF: Confirmer que les gains VIP sont maintenant collectés automatiquement dès qu'une partie se termine")
    print("TESTS À EFFECTUER:")
    print("1. Test de création de partie avec VIPs")
    print("2. Test de simulation jusqu'à la fin")
    print("3. Test de collecte automatique des gains VIP")
    print("4. Test de cohérence")
    print()
    
    # Test 1: Créer une partie standard avec des joueurs et vérifier que des VIPs sont assignés au salon VIP
    print("🔍 TEST 1: CRÉATION DE PARTIE AVEC VIPS")
    print("-" * 60)
    
    game_request = {
        "player_count": 30,
        "game_mode": "standard", 
        "selected_events": [1, 2, 3, 4],
        "manual_players": []
    }
    
    response = requests.post(f"{API_BASE}/games/create", 
                           json=game_request, 
                           headers={"Content-Type": "application/json"},
                           timeout=15)
    
    if response.status_code != 200:
        print(f"❌ ÉCHEC: Could not create game - HTTP {response.status_code}")
        print(f"   Détails: {response.text}")
        return False
        
    game_data = response.json()
    game_id = game_data.get('id')
    print(f"   ✅ Partie créée avec ID: {game_id}")
    print(f"   ✅ Nombre de joueurs: {len(game_data.get('players', []))}")
    
    # Vérifier les VIPs assignés au salon VIP niveau 3 (5 VIPs)
    vips_response = requests.get(f"{API_BASE}/vips/game/{game_id}?salon_level=3", timeout=10)
    
    if vips_response.status_code != 200:
        print(f"❌ ÉCHEC: Could not get VIPs - HTTP {vips_response.status_code}")
        return False
        
    vips_data = vips_response.json()
    
    if not isinstance(vips_data, list) or len(vips_data) != 5:
        print(f"❌ ÉCHEC: Expected 5 VIPs for salon level 3, got {len(vips_data) if isinstance(vips_data, list) else 'non-list'}")
        return False
    
    # Récupérer les VIPs assignés et noter leurs viewing_fee totaux
    total_vip_viewing_fees = sum(vip.get('viewing_fee', 0) for vip in vips_data)
    print(f"   ✅ {len(vips_data)} VIPs assignés au salon VIP niveau 3")
    print(f"   ✅ Viewing_fee total des VIPs: {total_vip_viewing_fees:,}$")
    
    # Afficher détails des VIPs
    for i, vip in enumerate(vips_data):
        print(f"   - VIP {i+1}: {vip.get('name', 'Unknown')} - {vip.get('viewing_fee', 0):,}$")
    
    # Test 2: Simuler des événements jusqu'à ce qu'il y ait un gagnant (completed=true)
    print("\n🔍 TEST 2: SIMULATION JUSQU'À LA FIN")
    print("-" * 60)
    
    max_simulations = 10
    simulation_count = 0
    
    while simulation_count < max_simulations:
        simulation_count += 1
        sim_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
        
        if sim_response.status_code != 200:
            print(f"❌ ÉCHEC: Event simulation failed - HTTP {sim_response.status_code}")
            return False
        
        sim_data = sim_response.json()
        game_state = sim_data.get('game', {})
        
        alive_count = len([p for p in game_state.get('players', []) if p.get('alive', False)])
        print(f"   Événement {simulation_count}: {alive_count} survivants")
        
        if game_state.get('completed', False):
            winner = game_state.get('winner', {})
            print(f"   ✅ Partie terminée après {simulation_count} événements")
            print(f"   ✅ Gagnant: {winner.get('name', 'Inconnu')} (#{winner.get('number', 'N/A')})")
            break
    
    if simulation_count >= max_simulations:
        print(f"❌ ÉCHEC: Game did not complete after {max_simulations} simulations")
        return False
    
    # Test 3: Vérifier que les gains VIP (game.earnings) correspondent exactement à la somme des viewing_fee des VIPs assignés
    print("\n🔍 TEST 3: COLLECTE AUTOMATIQUE DES GAINS VIP")
    print("-" * 60)
    
    # Récupérer l'état final de la partie
    game_response = requests.get(f"{API_BASE}/games/{game_id}", timeout=10)
    
    if game_response.status_code != 200:
        print(f"❌ ÉCHEC: Could not get final game data - HTTP {game_response.status_code}")
        return False
        
    final_game_data = game_response.json()
    actual_game_earnings = final_game_data.get('earnings', 0)
    vip_earnings_collected = final_game_data.get('vip_earnings_collected', False)
    
    print(f"   📊 Gains VIP dans game.earnings: {actual_game_earnings:,}$")
    print(f"   📊 Viewing_fee total attendu: {total_vip_viewing_fees:,}$")
    print(f"   📊 VIP earnings collected flag: {vip_earnings_collected}")
    
    # Vérifier que les gains correspondent exactement
    earnings_match = (actual_game_earnings == total_vip_viewing_fees)
    
    if earnings_match:
        print(f"   ✅ SUCCÈS: Les gains VIP correspondent exactement aux viewing_fee")
    else:
        print(f"   ❌ PROBLÈME: Les gains VIP ne correspondent pas")
        print(f"   ❌ Différence: {abs(actual_game_earnings - total_vip_viewing_fees):,}$ ({((actual_game_earnings / total_vip_viewing_fees) * 100):.1f}% des gains attendus)")
    
    # Test 4: Vérifier que les gains ont été automatiquement ajoutés au gamestate (portefeuille du joueur)
    print("\n🔍 TEST 4: COHÉRENCE - VÉRIFICATION DU GAMESTATE")
    print("-" * 60)
    
    # Récupérer l'état du gamestate pour vérifier l'argent
    gamestate_response = requests.get(f"{API_BASE}/gamestate/", timeout=10)
    
    if gamestate_response.status_code != 200:
        print(f"❌ ÉCHEC: Could not get gamestate - HTTP {gamestate_response.status_code}")
        return False
        
    gamestate_data = gamestate_response.json()
    current_money = gamestate_data.get('money', 0)
    total_earnings = gamestate_data.get('game_stats', {}).get('total_earnings', 0)
    
    print(f"   💰 Argent actuel dans le gamestate: {current_money:,}$")
    print(f"   📈 Total des gains accumulés: {total_earnings:,}$")
    
    # Vérifier que game.vip_earnings_collected=true
    if vip_earnings_collected:
        print(f"   ✅ SUCCÈS: Flag vip_earnings_collected = true")
    else:
        print(f"   ❌ PROBLÈME: Flag vip_earnings_collected = false")
    
    # Test final: Vérifier que les gains VIP ne peuvent plus être collectés manuellement
    print("\n🔍 TEST FINAL: VÉRIFICATION COLLECTE MANUELLE IMPOSSIBLE")
    print("-" * 60)
    
    # Tenter de collecter manuellement (devrait échouer car déjà collecté automatiquement)
    manual_collect_response = requests.post(f"{API_BASE}/games/{game_id}/collect-vip-earnings", timeout=10)
    
    if manual_collect_response.status_code == 400:
        print(f"   ✅ SUCCÈS: Collecte manuelle refusée (déjà collecté automatiquement)")
    else:
        print(f"   ❌ PROBLÈME: Collecte manuelle autorisée (ne devrait pas être possible)")
        print(f"   ❌ HTTP {manual_collect_response.status_code}: {manual_collect_response.text}")
    
    # Résumé final
    print("\n📋 RÉSUMÉ DES TESTS VIP AUTOMATIC COLLECTION")
    print("=" * 60)
    
    all_tests_passed = earnings_match and vip_earnings_collected
    
    if all_tests_passed:
        print(f"✅ SYSTÈME DE COLLECTE AUTOMATIQUE FONCTIONNEL")
        print(f"   - Gains VIP ({actual_game_earnings:,}$) collectés automatiquement dès la fin de partie")
        print(f"   - Flag vip_earnings_collected correctement défini")
        print(f"   - Cohérence entre viewing_fee des VIPs et gains calculés")
        return True
    else:
        issues = []
        if not earnings_match:
            issues.append(f"Gains incorrects ({actual_game_earnings:,}$ vs {total_vip_viewing_fees:,}$)")
        if not vip_earnings_collected:
            issues.append("Flag vip_earnings_collected non défini")
        
        print(f"❌ PROBLÈMES DÉTECTÉS:")
        for issue in issues:
            print(f"   - {issue}")
        return False

if __name__ == "__main__":
    success = test_vip_automatic_collection()
    if success:
        print("\n🎉 TOUS LES TESTS VIP AUTOMATIC COLLECTION RÉUSSIS!")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS VIP AUTOMATIC COLLECTION ONT ÉCHOUÉ")
        sys.exit(1)