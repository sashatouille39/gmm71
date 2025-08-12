#!/usr/bin/env python3
"""
VIP Earnings Bonus Test - Review Request Française
Tests the VIP earnings problem with bonus according to the French review request
"""

import requests
import json
import sys
import os
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

def test_vip_earnings_bonus_problem():
    """Test CRITICAL: Problème des gains VIP avec bonus - Review Request Française"""
    try:
        print("\n🎯 TESTING VIP EARNINGS BONUS PROBLEM - REVIEW REQUEST FRANÇAISE")
        print("=" * 80)
        print("OBJECTIF: Tester le problème des gains VIP avec bonus pour comprendre l'écart")
        print("entre l'affichage et les gains réels selon la demande française spécifique")
        print()
        
        # Créer une partie simple pour tester les gains VIP
        print("🔍 ÉTAPE 1: CRÉATION PARTIE SIMPLE POUR TEST VIP")
        print("-" * 60)
        
        # Créer la partie avec salon VIP niveau 3 (5 VIPs)
        game_request = {
            "player_count": 20,
            "game_mode": "standard",
            "selected_events": [1, 2, 3, 4],  # 4 événements pour simulation complète
            "manual_players": [],
            "vip_salon_level": 3  # Niveau 3 = 5 VIPs selon la logique
        }
        
        response = requests.post(f"{API_BASE}/games/create", 
                               json=game_request, 
                               headers={"Content-Type": "application/json"},
                               timeout=20)
        
        if response.status_code != 200:
            print(f"❌ Impossible de créer la partie - HTTP {response.status_code}: {response.text[:300]}")
            return False
            
        game_data = response.json()
        game_id = game_data.get('id')
        
        if not game_id:
            print("❌ Aucun ID de partie retourné")
            return False
        
        print(f"   ✅ Partie créée avec succès: {game_id}")
        print(f"   📊 Joueurs dans la partie: {len(game_data.get('players', []))}")
        
        # Vérifier les VIPs assignés avant simulation
        vip_response = requests.get(f"{API_BASE}/vips/salon/3", timeout=5)
        base_vip_total = 0
        if vip_response.status_code == 200:
            vips_data = vip_response.json()
            base_vip_total = sum(vip.get('viewing_fee', 0) for vip in vips_data.get('vips', []))
            print(f"   💰 VIPs salon niveau 3: {len(vips_data.get('vips', []))} VIPs")
            print(f"   💰 Total viewing_fee de base: {base_vip_total:,}$")
        else:
            print(f"   ⚠️ Impossible de récupérer les VIPs salon niveau 3")
            base_vip_total = 0
        
        # Étape 2: Simuler la partie jusqu'à la fin avec un gagnant
        print("\n🔍 ÉTAPE 2: SIMULATION PARTIE JUSQU'À LA FIN")
        print("-" * 60)
        
        simulation_count = 0
        max_simulations = 10  # Limite de sécurité
        
        while simulation_count < max_simulations:
            simulation_count += 1
            
            # Vérifier l'état de la partie
            game_response = requests.get(f"{API_BASE}/games/{game_id}", timeout=10)
            if game_response.status_code != 200:
                break
                
            current_game = game_response.json()
            if current_game.get('completed', False):
                print(f"   ✅ Partie terminée après {simulation_count-1} simulations")
                winner = current_game.get('winner')
                if winner:
                    print(f"   🏆 Gagnant: {winner.get('name', 'Inconnu')} (#{winner.get('number', '???')})")
                break
            
            # Simuler un événement
            sim_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=15)
            if sim_response.status_code != 200:
                print(f"   ❌ Erreur simulation événement {simulation_count}: HTTP {sim_response.status_code}")
                break
                
            sim_data = sim_response.json()
            result = sim_data.get('result', {})
            survivors = len(result.get('survivors', []))
            eliminated = len(result.get('eliminated', []))
            
            print(f"   📊 Événement {simulation_count}: {survivors} survivants, {eliminated} éliminés")
            
            # Vérifier si la partie est terminée
            updated_game = sim_data.get('game', {})
            if updated_game.get('completed', False):
                print(f"   ✅ Partie terminée après {simulation_count} simulations")
                winner = updated_game.get('winner')
                if winner:
                    print(f"   🏆 Gagnant: {winner.get('name', 'Inconnu')} (#{winner.get('number', '???')})")
                break
        
        if simulation_count >= max_simulations:
            print(f"   ⚠️ Limite de simulations atteinte ({max_simulations})")
        
        # Étape 3: Vérifier les gains VIP dans les 3 endroits
        print("\n🔍 ÉTAPE 3: VÉRIFICATION GAINS VIP DANS 3 ENDROITS")
        print("-" * 60)
        
        # 3.1: API /api/games/{game_id}/final-ranking - champ vip_earnings
        print("   📊 3.1: API final-ranking - champ vip_earnings")
        final_ranking_response = requests.get(f"{API_BASE}/games/{game_id}/final-ranking", timeout=10)
        
        final_ranking_vip_earnings = 0
        if final_ranking_response.status_code == 200:
            final_ranking_data = final_ranking_response.json()
            final_ranking_vip_earnings = final_ranking_data.get('vip_earnings', 0)
            print(f"      ✅ final-ranking vip_earnings: {final_ranking_vip_earnings:,}$")
        else:
            print(f"      ❌ Erreur final-ranking: HTTP {final_ranking_response.status_code}")
        
        # 3.2: API /api/games/{game_id}/vip-earnings-status - champ earnings_available
        print("   📊 3.2: API vip-earnings-status - champ earnings_available")
        vip_status_response = requests.get(f"{API_BASE}/games/{game_id}/vip-earnings-status", timeout=10)
        
        vip_status_earnings = 0
        if vip_status_response.status_code == 200:
            vip_status_data = vip_status_response.json()
            vip_status_earnings = vip_status_data.get('earnings_available', 0)
            can_collect = vip_status_data.get('can_collect', False)
            print(f"      ✅ vip-earnings-status earnings_available: {vip_status_earnings:,}$")
            print(f"      📋 can_collect: {can_collect}")
        else:
            print(f"      ❌ Erreur vip-earnings-status: HTTP {vip_status_response.status_code}")
        
        # 3.3: Gamestate avant/après pour voir l'argent réellement ajouté
        print("   📊 3.3: Gamestate avant/après collection")
        
        # Récupérer le gamestate avant collection
        gamestate_before_response = requests.get(f"{API_BASE}/gamestate/", timeout=5)
        money_before = 0
        if gamestate_before_response.status_code == 200:
            gamestate_before = gamestate_before_response.json()
            money_before = gamestate_before.get('money', 0)
            print(f"      💰 Argent avant collection: {money_before:,}$")
        else:
            print(f"      ❌ Erreur gamestate avant: HTTP {gamestate_before_response.status_code}")
        
        # Collecter les gains VIP
        collect_response = requests.post(f"{API_BASE}/games/{game_id}/collect-vip-earnings", timeout=10)
        collected_amount = 0
        if collect_response.status_code == 200:
            collect_data = collect_response.json()
            collected_amount = collect_data.get('earnings_collected', 0)
            print(f"      ✅ Collection réussie: {collected_amount:,}$ collectés")
        else:
            print(f"      ❌ Erreur collection: HTTP {collect_response.status_code}: {collect_response.text[:200]}")
        
        # Récupérer le gamestate après collection
        gamestate_after_response = requests.get(f"{API_BASE}/gamestate/", timeout=5)
        money_after = 0
        actual_money_added = 0
        if gamestate_after_response.status_code == 200:
            gamestate_after = gamestate_after_response.json()
            money_after = gamestate_after.get('money', 0)
            actual_money_added = money_after - money_before
            print(f"      💰 Argent après collection: {money_after:,}$")
            print(f"      💰 Argent réellement ajouté: {actual_money_added:,}$")
        else:
            print(f"      ❌ Erreur gamestate après: HTTP {gamestate_after_response.status_code}")
        
        # Étape 4: Calculer et comparer
        print("\n🔍 ÉTAPE 4: CALCUL ET COMPARAISON")
        print("-" * 60)
        
        # Comparer les 3 sources
        print(f"   📊 COMPARAISON DES 3 SOURCES:")
        print(f"      - final-ranking vip_earnings: {final_ranking_vip_earnings:,}$")
        print(f"      - vip-earnings-status earnings_available: {vip_status_earnings:,}$")
        print(f"      - Argent réellement ajouté au gamestate: {actual_money_added:,}$")
        
        # Analyser les écarts
        sources_match = (final_ranking_vip_earnings == vip_status_earnings == actual_money_added)
        
        # Évaluer le résultat
        if sources_match:
            if final_ranking_vip_earnings > 0:
                print(f"✅ GAINS VIP COHÉRENTS: Les 3 sources concordent ({final_ranking_vip_earnings:,}$)")
                success = True
            else:
                print(f"❌ AUCUN GAIN VIP: Les 3 sources concordent mais aucun gain détecté")
                success = False
        else:
            print(f"❌ INCOHÉRENCE GAINS VIP: Les sources ne concordent pas - "
                  f"final-ranking: {final_ranking_vip_earnings:,}$, "
                  f"vip-earnings-status: {vip_status_earnings:,}$, "
                  f"gamestate ajouté: {actual_money_added:,}$")
            success = False
        
        # Détails pour debugging
        print(f"\n   🔍 DÉTAILS POUR DEBUGGING:")
        print(f"      - Base VIP total: {base_vip_total:,}$")
        print(f"      - Sources concordent: {sources_match}")
        print(f"      - Gains détectés: {final_ranking_vip_earnings > 0}")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print(f"\n🎯 TEST DU PROBLÈME DES GAINS VIP AVEC BONUS - REVIEW REQUEST FRANÇAISE")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base: {API_BASE}")
    print("=" * 80)
    
    # Test server connectivity first
    try:
        response = requests.get(f"{API_BASE}/", timeout=10)
        if response.status_code == 200:
            print("✅ Server accessible")
        else:
            print("❌ Server not accessible, aborting tests")
            exit(1)
    except:
        print("❌ Server not accessible, aborting tests")
        exit(1)
    
    # Run the VIP earnings bonus test
    success = test_vip_earnings_bonus_problem()
    
    if success:
        print("\n✅ TEST RÉUSSI: Les gains VIP fonctionnent correctement")
    else:
        print("\n❌ TEST ÉCHOUÉ: Problème détecté avec les gains VIP")
    
    print("\n" + "=" * 80)