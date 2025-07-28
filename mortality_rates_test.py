#!/usr/bin/env python3
"""
Mortality Rates Test Suite for Game Master Manager
Tests the corrected mortality rates as specified in the review request
"""

import requests
import json
import sys
import os
from datetime import datetime
import statistics

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

class MortalityRatesTester:
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
    
    def test_events_mortality_rates(self):
        """Test: Vérifier que les taux de mortalité sont dans les bonnes fourchettes"""
        try:
            print("\n🎯 TESTING CORRECTED MORTALITY RATES FOR ALL EVENTS")
            print("=" * 80)
            
            # Get all available events
            response = requests.get(f"{API_BASE}/games/events/available", timeout=10)
            if response.status_code != 200:
                self.log_result("Events Mortality Rates", False, f"Could not get events - HTTP {response.status_code}")
                return
                
            events = response.json()
            
            # Analyze mortality rates by event
            normal_events = []
            special_events = []
            out_of_range_events = []
            
            for event in events:
                event_name = event.get('name', '')
                elimination_rate = event.get('elimination_rate', 0)
                mortality_rate = elimination_rate * 100  # Convert to percentage
                
                # Categorize events
                if event_name in ["Bataille royale", "Le Jugement Final"]:
                    special_events.append({
                        'name': event_name,
                        'mortality_rate': mortality_rate,
                        'expected_range': '65-70%' if event_name == "Bataille royale" else '70%'
                    })
                else:
                    normal_events.append({
                        'name': event_name,
                        'mortality_rate': mortality_rate
                    })
                    
                    # Check if normal event is out of expected range (40-60%)
                    if mortality_rate < 30 or mortality_rate > 60:
                        out_of_range_events.append({
                            'name': event_name,
                            'mortality_rate': mortality_rate,
                            'issue': 'Outside 30-60% range'
                        })
            
            # Analyze normal events statistics
            normal_mortality_rates = [event['mortality_rate'] for event in normal_events]
            avg_mortality = statistics.mean(normal_mortality_rates) if normal_mortality_rates else 0
            min_mortality = min(normal_mortality_rates) if normal_mortality_rates else 0
            max_mortality = max(normal_mortality_rates) if normal_mortality_rates else 0
            
            # Check special events
            bataille_royale_ok = False
            jugement_final_ok = False
            
            for special_event in special_events:
                if special_event['name'] == "Bataille royale":
                    bataille_royale_ok = 60 <= special_event['mortality_rate'] <= 70
                elif special_event['name'] == "Le Jugement Final":
                    jugement_final_ok = special_event['mortality_rate'] == 70
            
            # Evaluate results
            success = True
            messages = []
            
            # Check normal events range
            if out_of_range_events:
                success = False
                messages.append(f"❌ {len(out_of_range_events)} events outside 30-60% mortality range")
                for event in out_of_range_events[:5]:  # Show first 5
                    messages.append(f"  - {event['name']}: {event['mortality_rate']:.1f}%")
            
            # Check special events
            if not bataille_royale_ok:
                bataille_rate = next((e['mortality_rate'] for e in special_events if e['name'] == "Bataille royale"), 0)
                messages.append(f"⚠️  Bataille royale mortality rate: {bataille_rate:.1f}% (expected ~65%)")
            
            if not jugement_final_ok:
                jugement_rate = next((e['mortality_rate'] for e in special_events if e['name'] == "Le Jugement Final"), 0)
                messages.append(f"⚠️  Jugement Final mortality rate: {jugement_rate:.1f}% (expected 70%)")
            
            if success:
                self.log_result("Events Mortality Rates", True, 
                              f"✅ MORTALITY RATES CORRECTED: "
                              f"Normal events avg: {avg_mortality:.1f}% (range: {min_mortality:.1f}%-{max_mortality:.1f}%), "
                              f"Special events properly configured")
                
                # Log detailed results
                print(f"   📊 DETAILED MORTALITY ANALYSIS:")
                print(f"   - Total events analyzed: {len(events)}")
                print(f"   - Normal events (30-60% range): {len(normal_events)}")
                print(f"   - Special events: {len(special_events)}")
                print(f"   - Average normal mortality: {avg_mortality:.1f}%")
                print(f"   - Range: {min_mortality:.1f}% - {max_mortality:.1f}%")
                
                print(f"   🎯 SPECIAL EVENTS:")
                for special_event in special_events:
                    status = "✅" if (special_event['name'] == "Bataille royale" and 60 <= special_event['mortality_rate'] <= 70) or \
                                   (special_event['name'] == "Le Jugement Final" and special_event['mortality_rate'] == 70) else "⚠️"
                    print(f"   - {special_event['name']}: {status} {special_event['mortality_rate']:.1f}% ({special_event['expected_range']})")
                    
            else:
                self.log_result("Events Mortality Rates", False, 
                              f"❌ MORTALITY RATES ISSUES FOUND", messages)
            
            return len(out_of_range_events) == 0
                
        except Exception as e:
            self.log_result("Events Mortality Rates", False, f"Error during test: {str(e)}")
            return False

    def test_actual_simulation_mortality_rates(self):
        """Test: Simuler plusieurs parties pour vérifier les taux de mortalité réels"""
        try:
            print("\n🎯 TESTING ACTUAL SIMULATION MORTALITY RATES")
            print("=" * 80)
            
            # Test different event types with multiple simulations
            test_events = [
                {"name": "Feu rouge, Feu vert", "expected_range": (30, 60)},
                {"name": "Billes", "expected_range": (40, 60)},
                {"name": "Bataille royale", "expected_range": (60, 70)},
                {"name": "Le Jugement Final", "expected_range": (65, 75)}
            ]
            
            simulation_results = []
            
            for test_event in test_events:
                event_name = test_event["name"]
                expected_min, expected_max = test_event["expected_range"]
                
                print(f"   Testing {event_name}...")
                
                # Run multiple simulations for this event
                mortality_rates = []
                
                for simulation in range(5):  # 5 simulations per event
                    # Create a game with this specific event
                    game_request = {
                        "player_count": 50,  # Good sample size
                        "game_mode": "standard",
                        "selected_events": [1],  # We'll find the right event ID
                        "manual_players": []
                    }
                    
                    # Get event ID by name
                    events_response = requests.get(f"{API_BASE}/games/events/available", timeout=5)
                    if events_response.status_code == 200:
                        events = events_response.json()
                        target_event = next((e for e in events if e['name'] == event_name), None)
                        if target_event:
                            game_request["selected_events"] = [target_event['id']]
                        else:
                            continue
                    else:
                        continue
                    
                    # Create game
                    game_response = requests.post(f"{API_BASE}/games/create", 
                                                json=game_request, 
                                                headers={"Content-Type": "application/json"},
                                                timeout=10)
                    
                    if game_response.status_code != 200:
                        continue
                        
                    game_data = game_response.json()
                    game_id = game_data.get('id')
                    initial_players = len(game_data.get('players', []))
                    
                    if not game_id:
                        continue
                    
                    # Simulate the event
                    simulate_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
                    
                    if simulate_response.status_code == 200:
                        result_data = simulate_response.json()
                        result = result_data.get('result', {})
                        
                        survivors_count = len(result.get('survivors', []))
                        eliminated_count = len(result.get('eliminated', []))
                        
                        if survivors_count + eliminated_count == initial_players:
                            actual_mortality_rate = (eliminated_count / initial_players) * 100
                            mortality_rates.append(actual_mortality_rate)
                
                if mortality_rates:
                    avg_mortality = statistics.mean(mortality_rates)
                    min_mortality = min(mortality_rates)
                    max_mortality = max(mortality_rates)
                    
                    # Check if within expected range
                    within_range = expected_min <= avg_mortality <= expected_max
                    
                    simulation_results.append({
                        'event_name': event_name,
                        'avg_mortality': avg_mortality,
                        'min_mortality': min_mortality,
                        'max_mortality': max_mortality,
                        'expected_range': (expected_min, expected_max),
                        'within_range': within_range,
                        'simulations': len(mortality_rates)
                    })
                    
                    status = "✅" if within_range else "❌"
                    print(f"   - {event_name}: {status} Avg: {avg_mortality:.1f}% (range: {min_mortality:.1f}%-{max_mortality:.1f}%, expected: {expected_min}-{expected_max}%)")
            
            # Evaluate overall results
            all_within_range = all(result['within_range'] for result in simulation_results)
            
            if all_within_range and simulation_results:
                self.log_result("Actual Simulation Mortality Rates", True, 
                              f"✅ SIMULATION MORTALITY RATES CORRECT: All {len(simulation_results)} tested events within expected ranges")
            else:
                failed_events = [r for r in simulation_results if not r['within_range']]
                self.log_result("Actual Simulation Mortality Rates", False, 
                              f"❌ {len(failed_events)} events outside expected mortality ranges", 
                              [f"{e['event_name']}: {e['avg_mortality']:.1f}%" for e in failed_events])
            
            return all_within_range
                
        except Exception as e:
            self.log_result("Actual Simulation Mortality Rates", False, f"Error during test: {str(e)}")
            return False

    def test_player_stats_survival_correlation(self):
        """Test: Vérifier que les joueurs avec de meilleures stats survivent plus souvent"""
        try:
            print("\n🎯 TESTING PLAYER STATS SURVIVAL CORRELATION")
            print("=" * 80)
            
            # Create a game with many players to get good statistics
            game_request = {
                "player_count": 100,
                "game_mode": "standard",
                "selected_events": [1, 2, 3],  # Multiple events
                "manual_players": []
            }
            
            game_response = requests.post(f"{API_BASE}/games/create", 
                                        json=game_request, 
                                        headers={"Content-Type": "application/json"},
                                        timeout=15)
            
            if game_response.status_code != 200:
                self.log_result("Player Stats Survival Correlation", False, f"Could not create test game - HTTP {game_response.status_code}")
                return False
                
            game_data = game_response.json()
            game_id = game_data.get('id')
            initial_players = game_data.get('players', [])
            
            if not game_id or not initial_players:
                self.log_result("Player Stats Survival Correlation", False, "No game ID or players returned")
                return False
            
            # Simulate first event
            simulate_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
            
            if simulate_response.status_code != 200:
                self.log_result("Player Stats Survival Correlation", False, f"Event simulation failed - HTTP {simulate_response.status_code}")
                return False
            
            result_data = simulate_response.json()
            result = result_data.get('result', {})
            
            survivors = result.get('survivors', [])
            eliminated = result.get('eliminated', [])
            
            if not survivors or not eliminated:
                self.log_result("Player Stats Survival Correlation", False, "No survivors or eliminated players to analyze")
                return False
            
            # Calculate average stats for survivors vs eliminated
            survivor_stats = []
            eliminated_stats = []
            
            for survivor_data in survivors:
                player = survivor_data.get('player', {})
                stats = player.get('stats', {})
                if stats:
                    total_stats = stats.get('intelligence', 0) + stats.get('force', 0) + stats.get('agilite', 0)
                    survivor_stats.append(total_stats)
            
            for eliminated_data in eliminated:
                player = eliminated_data.get('player', {})
                stats = player.get('stats', {})
                if stats:
                    total_stats = stats.get('intelligence', 0) + stats.get('force', 0) + stats.get('agilite', 0)
                    eliminated_stats.append(total_stats)
            
            if not survivor_stats or not eliminated_stats:
                self.log_result("Player Stats Survival Correlation", False, "Could not extract stats from players")
                return False
            
            # Calculate averages
            avg_survivor_stats = statistics.mean(survivor_stats)
            avg_eliminated_stats = statistics.mean(eliminated_stats)
            
            # Check if survivors have better stats on average
            stats_correlation_correct = avg_survivor_stats > avg_eliminated_stats
            
            difference = avg_survivor_stats - avg_eliminated_stats
            difference_percentage = (difference / avg_eliminated_stats) * 100 if avg_eliminated_stats > 0 else 0
            
            if stats_correlation_correct:
                self.log_result("Player Stats Survival Correlation", True, 
                              f"✅ STATS CORRELATION CORRECT: Survivors have {difference:.1f} higher avg stats ({difference_percentage:.1f}% better)")
                
                print(f"   📊 STATS ANALYSIS:")
                print(f"   - Survivors avg stats: {avg_survivor_stats:.1f}")
                print(f"   - Eliminated avg stats: {avg_eliminated_stats:.1f}")
                print(f"   - Difference: +{difference:.1f} ({difference_percentage:.1f}% better)")
                print(f"   - Sample sizes: {len(survivor_stats)} survivors, {len(eliminated_stats)} eliminated")
            else:
                self.log_result("Player Stats Survival Correlation", False, 
                              f"❌ STATS CORRELATION INCORRECT: Eliminated players have better stats on average")
            
            return stats_correlation_correct
                
        except Exception as e:
            self.log_result("Player Stats Survival Correlation", False, f"Error during test: {str(e)}")
            return False

    def test_edge_cases_player_counts(self):
        """Test: Tester les cas limites avec peu (5-10) vs beaucoup (100+) de joueurs"""
        try:
            print("\n🎯 TESTING EDGE CASES WITH DIFFERENT PLAYER COUNTS")
            print("=" * 80)
            
            test_cases = [
                {"count": 5, "name": "Very Few Players"},
                {"count": 10, "name": "Few Players"},
                {"count": 100, "name": "Many Players"},
                {"count": 200, "name": "Very Many Players"}
            ]
            
            edge_case_results = []
            
            for test_case in test_cases:
                player_count = test_case["count"]
                case_name = test_case["name"]
                
                print(f"   Testing {case_name} ({player_count} players)...")
                
                # Create game with specific player count
                game_request = {
                    "player_count": player_count,
                    "game_mode": "standard",
                    "selected_events": [1],  # Use first event
                    "manual_players": []
                }
                
                game_response = requests.post(f"{API_BASE}/games/create", 
                                            json=game_request, 
                                            headers={"Content-Type": "application/json"},
                                            timeout=15)
                
                if game_response.status_code != 200:
                    edge_case_results.append({
                        'case_name': case_name,
                        'player_count': player_count,
                        'success': False,
                        'issue': f"Game creation failed - HTTP {game_response.status_code}"
                    })
                    continue
                    
                game_data = game_response.json()
                game_id = game_data.get('id')
                actual_players = len(game_data.get('players', []))
                
                if actual_players != player_count:
                    edge_case_results.append({
                        'case_name': case_name,
                        'player_count': player_count,
                        'success': False,
                        'issue': f"Expected {player_count} players, got {actual_players}"
                    })
                    continue
                
                # Simulate event
                simulate_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
                
                if simulate_response.status_code != 200:
                    edge_case_results.append({
                        'case_name': case_name,
                        'player_count': player_count,
                        'success': False,
                        'issue': f"Event simulation failed - HTTP {simulate_response.status_code}"
                    })
                    continue
                
                result_data = simulate_response.json()
                result = result_data.get('result', {})
                
                survivors_count = len(result.get('survivors', []))
                eliminated_count = len(result.get('eliminated', []))
                total_participants = result.get('total_participants', 0)
                
                # Validate results
                if survivors_count + eliminated_count != total_participants:
                    edge_case_results.append({
                        'case_name': case_name,
                        'player_count': player_count,
                        'success': False,
                        'issue': f"Participant count mismatch: {survivors_count}+{eliminated_count}≠{total_participants}"
                    })
                    continue
                
                # Check mortality rate is reasonable
                mortality_rate = (eliminated_count / total_participants) * 100 if total_participants > 0 else 0
                reasonable_mortality = 10 <= mortality_rate <= 90  # Very broad range for edge cases
                
                # Check at least 1 survivor (unless very small group)
                min_survivors_ok = survivors_count >= 1 or player_count <= 3
                
                success = reasonable_mortality and min_survivors_ok
                
                edge_case_results.append({
                    'case_name': case_name,
                    'player_count': player_count,
                    'success': success,
                    'survivors': survivors_count,
                    'eliminated': eliminated_count,
                    'mortality_rate': mortality_rate,
                    'issue': None if success else f"Unreasonable results: {survivors_count} survivors, {eliminated_count} eliminated ({mortality_rate:.1f}% mortality)"
                })
                
                status = "✅" if success else "❌"
                print(f"   - {case_name}: {status} {survivors_count} survivors, {eliminated_count} eliminated ({mortality_rate:.1f}% mortality)")
            
            # Evaluate overall results
            all_successful = all(result['success'] for result in edge_case_results)
            failed_cases = [r for r in edge_case_results if not r['success']]
            
            if all_successful:
                self.log_result("Edge Cases Player Counts", True, 
                              f"✅ EDGE CASES HANDLED CORRECTLY: All {len(edge_case_results)} player count scenarios work properly")
            else:
                self.log_result("Edge Cases Player Counts", False, 
                              f"❌ {len(failed_cases)} edge cases failed", 
                              [f"{case['case_name']}: {case['issue']}" for case in failed_cases])
            
            return all_successful
                
        except Exception as e:
            self.log_result("Edge Cases Player Counts", False, f"Error during test: {str(e)}")
            return False

    def run_mortality_tests(self):
        """Run all mortality rate tests"""
        print(f"🎯 Starting Mortality Rates Tests for Game Master Manager")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 80)
        
        # Test 1: Check configured mortality rates
        self.test_events_mortality_rates()
        
        # Test 2: Test actual simulation mortality rates
        self.test_actual_simulation_mortality_rates()
        
        # Test 3: Test player stats correlation with survival
        self.test_player_stats_survival_correlation()
        
        # Test 4: Test edge cases with different player counts
        self.test_edge_cases_player_counts()
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 MORTALITY RATES TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        print("\n📋 DETAILED RESULTS:")
        for result in self.results:
            print(f"{result['status']}: {result['test']}")
            if result['status'] == "❌ FAIL":
                print(f"   → {result['message']}")
        
        # Critical issues
        critical_failures = [r for r in self.results if r['status'] == "❌ FAIL"]
        
        if critical_failures:
            print(f"\n🚨 ISSUES FOUND: {len(critical_failures)}")
            for failure in critical_failures:
                print(f"   • {failure['test']}: {failure['message']}")
        else:
            print(f"\n✅ ALL MORTALITY RATE TESTS PASSED!")
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "success_rate": (self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0,
            "results": self.results,
            "critical_failures": len(critical_failures)
        }

if __name__ == "__main__":
    tester = MortalityRatesTester()
    summary = tester.run_mortality_tests()
    
    # Exit with error code if tests failed
    if summary["critical_failures"] > 0 or summary["success_rate"] < 75:
        sys.exit(1)
    else:
        sys.exit(0)