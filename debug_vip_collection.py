#!/usr/bin/env python3
"""
Debug script to understand why VIP automatic collection is not working
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

def debug_vip_collection():
    print("🔍 DEBUG: VIP Collection Issue Analysis")
    print("=" * 60)
    
    # Step 1: Upgrade VIP salon to level 1
    print("Step 1: Upgrading VIP salon to level 1...")
    update_data = {"vip_salon_level": 1}
    update_response = requests.put(f"{API_BASE}/gamestate/", 
                                 json=update_data,
                                 headers={"Content-Type": "application/json"},
                                 timeout=5)
    
    if update_response.status_code == 200:
        print("✅ VIP salon upgraded to level 1")
    else:
        print(f"❌ Failed to upgrade VIP salon - HTTP {update_response.status_code}")
        return
    
    # Step 2: Create a game
    print("\nStep 2: Creating a game...")
    game_request = {
        "player_count": 20,
        "game_mode": "standard",
        "selected_events": [1, 2, 3],
        "manual_players": []
    }
    
    response = requests.post(f"{API_BASE}/games/create", 
                           json=game_request, 
                           headers={"Content-Type": "application/json"},
                           timeout=15)
    
    if response.status_code != 200:
        print(f"❌ Failed to create game - HTTP {response.status_code}")
        return
        
    game_data = response.json()
    game_id = game_data.get('id')
    print(f"✅ Game created with ID: {game_id}")
    
    # Step 3: Check initial game state
    print(f"\nStep 3: Checking initial game state...")
    print(f"   - earnings: {game_data.get('earnings', 'NOT_FOUND')}")
    print(f"   - vip_earnings_collected: {game_data.get('vip_earnings_collected', 'NOT_FOUND')}")
    print(f"   - completed: {game_data.get('completed', 'NOT_FOUND')}")
    
    # Step 4: Check VIPs assigned
    print(f"\nStep 4: Checking VIPs assigned...")
    vips_response = requests.get(f"{API_BASE}/vips/game/{game_id}?salon_level=1", timeout=10)
    if vips_response.status_code == 200:
        vips_data = vips_response.json()
        if isinstance(vips_data, list):
            total_viewing_fee = sum(vip.get('viewing_fee', 0) for vip in vips_data)
            print(f"   ✅ {len(vips_data)} VIPs assigned with total viewing_fee: {total_viewing_fee:,}$")
        else:
            print(f"   ❌ Invalid VIPs data: {vips_data}")
    else:
        print(f"   ❌ Failed to get VIPs - HTTP {vips_response.status_code}")
    
    # Step 5: Simulate until completion
    print(f"\nStep 5: Simulating until completion...")
    for event_num in range(5):
        sim_response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
        if sim_response.status_code == 200:
            sim_data = sim_response.json()
            game_state = sim_data.get('game', {})
            
            print(f"   Event {event_num + 1}:")
            print(f"      - completed: {game_state.get('completed', 'NOT_FOUND')}")
            print(f"      - earnings: {game_state.get('earnings', 'NOT_FOUND')}")
            print(f"      - vip_earnings_collected: {game_state.get('vip_earnings_collected', 'NOT_FOUND')}")
            
            if game_state.get('completed', False):
                print(f"   ✅ Game completed after {event_num + 1} events")
                break
        else:
            print(f"   ❌ Event simulation failed - HTTP {sim_response.status_code}")
            break
    
    # Step 6: Check final state
    print(f"\nStep 6: Checking final game state...")
    final_response = requests.get(f"{API_BASE}/games/{game_id}", timeout=5)
    if final_response.status_code == 200:
        final_game = final_response.json()
        print(f"   Final game state:")
        print(f"      - earnings: {final_game.get('earnings', 'NOT_FOUND')}")
        print(f"      - vip_earnings_collected: {final_game.get('vip_earnings_collected', 'NOT_FOUND')}")
        print(f"      - completed: {final_game.get('completed', 'NOT_FOUND')}")
    else:
        print(f"   ❌ Failed to get final game state - HTTP {final_response.status_code}")
    
    # Step 7: Check VIP earnings status
    print(f"\nStep 7: Checking VIP earnings status...")
    status_response = requests.get(f"{API_BASE}/games/{game_id}/vip-earnings-status", timeout=5)
    if status_response.status_code == 200:
        status_data = status_response.json()
        print(f"   VIP earnings status:")
        print(f"      - earnings_available: {status_data.get('earnings_available', 'NOT_FOUND')}")
        print(f"      - can_collect: {status_data.get('can_collect', 'NOT_FOUND')}")
        print(f"      - completed: {status_data.get('completed', 'NOT_FOUND')}")
    else:
        print(f"   ❌ Failed to get VIP earnings status - HTTP {status_response.status_code}")

if __name__ == "__main__":
    debug_vip_collection()