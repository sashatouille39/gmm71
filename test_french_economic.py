#!/usr/bin/env python3
"""
Test script to validate the French economic system according to the review request
"""

import requests
import json

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

def test_french_economic_system():
    """Test the French economic system according to the review request"""
    print("🇫🇷 TESTING FRENCH ECONOMIC SYSTEM")
    print("=" * 60)
    print("According to the French user review request:")
    print("- Initial money: 10,000,000$ (10 million)")
    print("- Player cost: 100$ per player")
    print("- Event cost: 5,000$ per event")
    print("- Game costs: Standard=100,000$, Hardcore=500,000$, Custom=1,000,000$")
    print("- VIP earnings: 100$ per player + 50$ per death")
    print()
    
    results = []
    
    # Test 1: Check initial money
    print("Test 1: Checking initial money...")
    try:
        response = requests.get(f"{API_BASE}/gamestate/", timeout=5)
        if response.status_code == 200:
            game_state = response.json()
            initial_money = game_state.get('money', 0)
            
            if initial_money == 10000000:
                print(f"✅ Initial money correct: {initial_money:,}$ (10 million)")
                results.append(("Initial Money", True, f"{initial_money:,}$"))
            else:
                print(f"❌ Initial money incorrect: {initial_money:,}$ (expected 10,000,000$)")
                results.append(("Initial Money", False, f"Got {initial_money:,}$, expected 10,000,000$"))
        else:
            print(f"❌ Could not get gamestate - HTTP {response.status_code}")
            results.append(("Initial Money", False, f"HTTP {response.status_code}"))
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Initial Money", False, str(e)))
    
    # Test 2: Check game creation costs
    print("\nTest 2: Testing game creation costs...")
    
    # Test Standard game cost with the exact example from review
    game_request = {
        "player_count": 50,
        "game_mode": "standard",
        "selected_events": [1, 2, 3],
        "manual_players": []
    }
    
    try:
        response = requests.post(f"{API_BASE}/games/create", 
                               json=game_request, 
                               headers={"Content-Type": "application/json"},
                               timeout=15)
        
        if response.status_code == 200:
            game_data = response.json()
            total_cost = game_data.get('total_cost', 0)
            
            # Expected: 100,000$ + (50 × 100$) + (3 × 5,000$) = 120,000$
            expected_cost = 100000 + (50 * 100) + (3 * 5000)  # 120,000$
            
            if total_cost == expected_cost:
                print(f"✅ Standard game cost correct: {total_cost:,}$ (100k + 5k + 15k)")
                results.append(("Standard Game Cost", True, f"{total_cost:,}$"))
                game_id = game_data.get('id')
            else:
                print(f"❌ Standard game cost incorrect: {total_cost:,}$ (expected {expected_cost:,}$)")
                results.append(("Standard Game Cost", False, f"Got {total_cost:,}$, expected {expected_cost:,}$"))
                game_id = None
        else:
            print(f"❌ Could not create game - HTTP {response.status_code}")
            results.append(("Standard Game Cost", False, f"HTTP {response.status_code}"))
            game_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Standard Game Cost", False, str(e)))
        game_id = None
    
    # Test 3: Check VIP earnings
    print("\nTest 3: Testing VIP earnings...")
    
    if game_id:
        try:
            # Simulate an event to test VIP earnings
            response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
            
            if response.status_code == 200:
                sim_data = response.json()
                game_after_event = sim_data.get('game', {})
                earnings = game_after_event.get('earnings', 0)
                
                result = sim_data.get('result', {})
                survivors_count = len(result.get('survivors', []))
                eliminated_count = len(result.get('eliminated', []))
                
                # Expected: (50 players × 100$) + (deaths × 50$)
                expected_base_earnings = 50 * 100  # 5,000$ base
                expected_death_bonus = eliminated_count * 50
                expected_total_earnings = expected_base_earnings + expected_death_bonus
                
                if earnings == expected_total_earnings:
                    print(f"✅ VIP earnings correct: {earnings:,}$ ({survivors_count} survivors, {eliminated_count} deaths)")
                    results.append(("VIP Earnings", True, f"{earnings:,}$ with {eliminated_count} deaths"))
                else:
                    print(f"❌ VIP earnings incorrect: {earnings:,}$ (expected {expected_total_earnings:,}$)")
                    print(f"   Details: {survivors_count} survivors, {eliminated_count} deaths")
                    print(f"   Expected: (50×100$) + ({eliminated_count}×50$) = {expected_total_earnings:,}$")
                    results.append(("VIP Earnings", False, f"Got {earnings:,}$, expected {expected_total_earnings:,}$"))
            else:
                print(f"❌ Could not simulate event - HTTP {response.status_code}")
                results.append(("VIP Earnings", False, f"HTTP {response.status_code}"))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(("VIP Earnings", False, str(e)))
    else:
        print("❌ Cannot test VIP earnings - no game created")
        results.append(("VIP Earnings", False, "No game available"))
    
    # Test 4: Check budget sufficiency
    print("\nTest 4: Checking budget sufficiency...")
    
    if initial_money >= expected_cost:
        remaining_budget = initial_money - expected_cost
        print(f"✅ 10M budget sufficient: {remaining_budget:,}$ remaining after standard game")
        results.append(("Budget Sufficiency", True, f"{remaining_budget:,}$ remaining"))
    else:
        print(f"❌ 10M budget insufficient: need {expected_cost:,}$, have {initial_money:,}$")
        results.append(("Budget Sufficiency", False, f"Need {expected_cost:,}$, have {initial_money:,}$"))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FRENCH ECONOMIC SYSTEM TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, details in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {details}")
    
    print(f"\nResults: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("🎉 All French economic system tests passed!")
        return True
    else:
        print("⚠️  Some tests failed - see details above")
        return False

if __name__ == "__main__":
    test_french_economic_system()