#!/usr/bin/env python3
"""
VIP Automatic Collection Test - French Review Request
Tests the VIP automatic earnings collection system according to the French user's problem description
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

class VIPAutomaticCollectionTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_vip_automatic_collection_system(self):
        """Test FRENCH REVIEW REQUEST: Tester la correction du système de gains VIP automatique selon le problème décrit par l'utilisateur français"""
        try:
            print("\n🇫🇷 TESTING VIP AUTOMATIC COLLECTION SYSTEM - FRENCH REVIEW REQUEST")
            print("=" * 80)
            print("PROBLÈME À VALIDER:")
            print("1. Les gains VIP doivent se collecter automatiquement dès qu'une partie se termine")
            print("2. Le montant doit correspondre exactement aux frais de visionnage des VIPs du salon")
            print("3. L'argent doit s'afficher dans le menu où le gagnant apparaît")
            print("4. Tester avec différents niveaux de salon (1, 3, 6)")
            print()
            
            # Test 1: Salon niveau 3 (5 VIPs) - Test principal
            print("🔍 TEST 1: SALON NIVEAU 3 (5 VIPs) - TEST COLLECTE AUTOMATIQUE")
            print("-" * 70)
            
            game_request = {
                "player_count": 25,
                "game_mode": "standard", 
                "selected_events": [1, 2, 3, 4],
                "manual_players": [],
                "vip_salon_level": 3  # Salon niveau 3 = 5 VIPs
            }
            
            response = requests.post(f"{API_BASE}/games/create", 
                                   json=game_request, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=15)
            
            if response.status_code != 200:
                self.log_result("VIP Automatic Collection - Salon Level 3 Creation", False, f"Could not create game - HTTP {response.status_code}")
                return
                
            game_data = response.json()
            game_id = game_data.get('id')
            print(f"   ✅ Partie créée avec ID: {game_id}")
            
            # Vérifier les VIPs assignés pour salon niveau 3
            vips_response = requests.get(f"{API_BASE}/vips/game/{game_id}?salon_level=3", timeout=10)
            
            if vips_response.status_code != 200:
                self.log_result("VIP Automatic Collection - VIP Assignment Level 3", False, f"Could not get VIPs - HTTP {vips_response.status_code}")
                return
                
            vips_data = vips_response.json()
            
            if not isinstance(vips_data, list) or len(vips_data) != 5:
                self.log_result("VIP Automatic Collection - VIP Assignment Level 3", False, f"Expected 5 VIPs for salon level 3, got {len(vips_data) if isinstance(vips_data, list) else 'non-list'}")
                return
            
            expected_vip_earnings = sum(vip.get('viewing_fee', 0) for vip in vips_data)
            print(f"   ✅ {len(vips_data)} VIPs assignés avec viewing_fee total: {expected_vip_earnings:,}$")
            
            # Print VIP details
            vip_details = []
            for vip in vips_data:
                vip_name = vip.get('name', 'Unknown')
                vip_fee = vip.get('viewing_fee', 0)
                vip_details.append(f"{vip_name}: {vip_fee:,}$")
            print(f"   📋 Détail VIPs: {vip_details}")
            
            # Simuler la partie jusqu'à la fin
            print("\n   🎮 Simulation de la partie jusqu'à la fin...")
            max_simulations = 10
            simulation_count = 0
            
            while simulation_count < max_simulations:
                simulation_count += 1
                sim_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
                
                if sim_response.status_code != 200:
                    self.log_result("VIP Automatic Collection - Game Simulation Level 3", False, f"Event simulation failed - HTTP {sim_response.status_code}")
                    return
                
                sim_data = sim_response.json()
                game_state = sim_data.get('game', {})
                
                if game_state.get('completed', False):
                    print(f"   ✅ Partie terminée après {simulation_count} événements")
                    winner = game_state.get('winner', {})
                    winner_name = winner.get('name', 'Inconnu') if winner else 'Inconnu'
                    winner_number = winner.get('number', 'N/A') if winner else 'N/A'
                    print(f"   🏆 Gagnant: {winner_name} (#{winner_number})")
                    break
            
            if simulation_count >= max_simulations:
                self.log_result("VIP Automatic Collection - Game Simulation Level 3", False, f"Game did not complete after {max_simulations} simulations")
                return
            
            # Vérifier la collecte automatique des gains VIP
            print("\n   💰 Vérification de la collecte automatique des gains VIP...")
            
            # Récupérer l'état final de la partie
            final_game_response = requests.get(f"{API_BASE}/games/{game_id}", timeout=10)
            
            if final_game_response.status_code != 200:
                self.log_result("VIP Automatic Collection - Final Game State", False, f"Could not get final game data - HTTP {final_game_response.status_code}")
                return
                
            final_game_data = final_game_response.json()
            actual_game_earnings = final_game_data.get('earnings', 0)
            vip_earnings_collected = final_game_data.get('vip_earnings_collected', False)
            
            print(f"   📊 Gains VIP dans game.earnings: {actual_game_earnings:,}$")
            print(f"   📊 Gains VIP attendus: {expected_vip_earnings:,}$")
            print(f"   🔄 Flag vip_earnings_collected: {vip_earnings_collected}")
            
            # Vérifier que les gains correspondent exactement
            earnings_match = (actual_game_earnings == expected_vip_earnings)
            
            # Vérifier l'état du gamestate (argent du joueur)
            gamestate_response = requests.get(f"{API_BASE}/gamestate/", timeout=10)
            
            if gamestate_response.status_code != 200:
                self.log_result("VIP Automatic Collection - Gamestate Check", False, f"Could not get gamestate - HTTP {gamestate_response.status_code}")
                return
                
            gamestate_data = gamestate_response.json()
            current_money = gamestate_data.get('money', 0)
            
            print(f"   💳 Argent actuel du joueur: {current_money:,}$")
            
            # Tester la route vip-earnings-status
            status_response = requests.get(f"{API_BASE}/games/{game_id}/vip-earnings-status", timeout=10)
            
            if status_response.status_code != 200:
                self.log_result("VIP Automatic Collection - Status Route", False, f"Could not get VIP earnings status - HTTP {status_response.status_code}")
                return
                
            status_data = status_response.json()
            earnings_available = status_data.get('earnings_available', 0)
            can_collect = status_data.get('can_collect', False)
            
            print(f"   📋 VIP earnings status - earnings_available: {earnings_available:,}$")
            print(f"   📋 VIP earnings status - can_collect: {can_collect}")
            
            # Évaluer les résultats
            success = True
            issues = []
            
            if not earnings_match:
                success = False
                percentage = (actual_game_earnings / expected_vip_earnings * 100) if expected_vip_earnings > 0 else 0
                issues.append(f"❌ Gains VIP incorrects: {actual_game_earnings:,}$ au lieu de {expected_vip_earnings:,}$ attendus (seulement {percentage:.1f}% des gains VIP calculés)")
            
            if not vip_earnings_collected:
                success = False
                issues.append(f"❌ Flag vip_earnings_collected = false (devrait être true)")
            
            # Tester si la collecte manuelle est encore possible (ne devrait pas l'être si collecte automatique a fonctionné)
            manual_collect_response = requests.post(f"{API_BASE}/games/{game_id}/collect-vip-earnings", timeout=10)
            
            if manual_collect_response.status_code == 200:
                success = False
                issues.append(f"❌ Collecte manuelle encore possible (HTTP 200) alors qu'elle devrait être bloquée si la collecte automatique avait fonctionné")
            
            if success:
                self.log_result("VIP Automatic Collection - Salon Level 3", True, 
                              f"✅ COLLECTE AUTOMATIQUE FONCTIONNE - Gains VIP: {actual_game_earnings:,}$, Flag collecté: {vip_earnings_collected}")
            else:
                self.log_result("VIP Automatic Collection - Salon Level 3", False, 
                              f"❌ PROBLÈME CRITIQUE CONFIRMÉ - TESTS EXHAUSTIFS SELON REVIEW REQUEST FRANÇAISE", issues)
            
            # Test 2: Salon niveau 1 (1 VIP) pour comparaison
            print("\n🔍 TEST 2: SALON NIVEAU 1 (1 VIP) - TEST COMPARATIF")
            print("-" * 70)
            
            self.test_salon_level(1, 1)
            
            # Test 3: Salon niveau 6 (12 VIPs) pour test complet
            print("\n🔍 TEST 3: SALON NIVEAU 6 (12 VIPs) - TEST NIVEAU SUPÉRIEUR")
            print("-" * 70)
            
            self.test_salon_level(6, 12)
            
        except Exception as e:
            self.log_result("VIP Automatic Collection System", False, f"Error during test: {str(e)}")
    
    def test_salon_level(self, salon_level, expected_vips):
        """Test a specific salon level"""
        try:
            game_request = {
                "player_count": 25,
                "game_mode": "standard", 
                "selected_events": [1, 2, 3],
                "manual_players": [],
                "vip_salon_level": salon_level
            }
            
            response = requests.post(f"{API_BASE}/games/create", 
                                   json=game_request, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=15)
            
            if response.status_code == 200:
                game_data = response.json()
                game_id = game_data.get('id')
                
                # Récupérer les VIPs pour ce salon level
                vips_response = requests.get(f"{API_BASE}/vips/game/{game_id}?salon_level={salon_level}", timeout=10)
                
                if vips_response.status_code == 200:
                    vips_data = vips_response.json()
                    expected_earnings = sum(vip.get('viewing_fee', 0) for vip in vips_data)
                    
                    print(f"   ✅ Salon niveau {salon_level}: {len(vips_data)} VIP(s) avec viewing_fee total: {expected_earnings:,}$")
                    
                    # Simuler rapidement jusqu'à la fin
                    for i in range(5):
                        sim_resp = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
                        if sim_resp.status_code == 200:
                            sim_data = sim_resp.json()
                            if sim_data.get('game', {}).get('completed', False):
                                break
                    
                    # Vérifier les gains
                    final_resp = requests.get(f"{API_BASE}/games/{game_id}", timeout=10)
                    if final_resp.status_code == 200:
                        final_data = final_resp.json()
                        actual_earnings = final_data.get('earnings', 0)
                        vip_collected = final_data.get('vip_earnings_collected', False)
                        
                        if actual_earnings == expected_earnings and vip_collected:
                            print(f"   ✅ Salon niveau {salon_level}: Calcul correct ({actual_earnings:,}$ attendu = {actual_earnings:,}$ obtenu), collecté automatiquement: {vip_collected}")
                        else:
                            percentage = (actual_earnings / expected_earnings * 100) if expected_earnings > 0 else 0
                            print(f"   ❌ Salon niveau {salon_level}: Calcul incorrect ({expected_earnings:,}$ attendu ≠ {actual_earnings:,}$ obtenu). Seuls ~{percentage:.0f}% des gains sont calculés, collecté: {vip_collected}")
                else:
                    print(f"   ❌ Salon niveau {salon_level}: Erreur lors de la récupération des VIPs - HTTP {vips_response.status_code}")
            else:
                print(f"   ❌ Salon niveau {salon_level}: Erreur lors de la création de partie - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Salon niveau {salon_level}: Erreur - {str(e)}")
    
    def run_tests(self):
        """Run all VIP automatic collection tests"""
        print("🇫🇷 DÉMARRAGE DES TESTS VIP AUTOMATIC COLLECTION - 2025-08-02")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print("=" * 80)
        
        # Test server connectivity first
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                print("✅ Backend server accessible")
            else:
                print(f"❌ Backend server error: HTTP {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Cannot connect to backend: {str(e)}")
            return
        
        # Run the main test
        self.test_vip_automatic_collection_system()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS VIP AUTOMATIC COLLECTION")
        print("=" * 80)
        print(f"Total des tests: {self.total_tests}")
        print(f"Tests réussis: {self.passed_tests}")
        print(f"Tests échoués: {self.total_tests - self.passed_tests}")
        print(f"Taux de réussite: {(self.passed_tests / self.total_tests * 100):.1f}%" if self.total_tests > 0 else "0%")
        
        if self.total_tests - self.passed_tests > 0:
            print(f"\n❌ TESTS ÉCHOUÉS:")
            for result in self.results:
                if "❌ FAIL" in result["status"]:
                    print(f"   - {result['test']}: {result['message']}")
        
        print("\n🏁 TESTS TERMINÉS")
        print("=" * 80)

if __name__ == "__main__":
    tester = VIPAutomaticCollectionTester()
    tester.run_tests()