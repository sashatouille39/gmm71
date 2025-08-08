#!/usr/bin/env python3
"""
Debug game completion and statistics saving
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

def debug_game_completion():
    print("🔍 DEBUGGING GAME COMPLETION AND STATISTICS SAVING")
    print("=" * 80)
    
    # Step 1: Create a simple game
    print("Step 1: Creating a simple game...")
    game_request = {
        "player_count": 20,  # Minimum required
        "game_mode": "standard",
        "selected_events": [1, 2, 3],  # Few events
        "manual_players": []
    }
    
    response = requests.post(f"{API_BASE}/games/create", 
                           json=game_request, 
                           headers={"Content-Type": "application/json"},
                           timeout=15)
    
    if response.status_code != 200:
        print(f"❌ Failed to create game: HTTP {response.status_code}")
        print(response.text)
        return
        
    game_data = response.json()
    game_id = game_data.get('id')
    print(f"✅ Game created: {game_id}")
    
    # Step 2: Check initial statistics
    print("\nStep 2: Checking initial statistics...")
    stats_response = requests.get(f"{API_BASE}/statistics/completed-games", timeout=5)
    if stats_response.status_code == 200:
        initial_stats = stats_response.json()
        print(f"Initial completed games: {len(initial_stats)}")
    else:
        print(f"❌ Failed to get initial stats: HTTP {stats_response.status_code}")
    
    # Step 3: Simulate events until completion
    print("\nStep 3: Simulating events until completion...")
    max_events = 10
    event_count = 0
    
    while event_count < max_events:
        event_count += 1
        print(f"  Simulating event {event_count}...")
        
        response = requests.post(f"{API_BASE}/games/{game_id}/simulate-event", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Event simulation failed: HTTP {response.status_code}")
            print(response.text)
            break
        
        data = response.json()
        game = data.get('game', {})
        result = data.get('result', {})
        
        survivors = result.get('survivors', [])
        completed = game.get('completed', False)
        winner = game.get('winner')
        
        print(f"    Survivors: {len(survivors)}, Completed: {completed}")
        
        if completed:
            print(f"    Winner: {winner.get('name') if winner else 'None'}")
            break
    
    if not completed:
        print(f"❌ Game did not complete after {max_events} events")
        return
    
    # Step 4: Check statistics after completion
    print("\nStep 4: Checking statistics after completion...")
    stats_response = requests.get(f"{API_BASE}/statistics/completed-games", timeout=5)
    if stats_response.status_code == 200:
        final_stats = stats_response.json()
        print(f"Final completed games: {len(final_stats)}")
        
        # Look for our game
        our_game = None
        for game in final_stats:
            if game.get('id') == game_id:
                our_game = game
                break
        
        if our_game:
            print(f"✅ Our game found in statistics!")
            print(f"  Winner: {our_game.get('winner')}")
            print(f"  Date: {our_game.get('date')}")
            print(f"  Players: {our_game.get('total_players')}")
        else:
            print(f"❌ Our game NOT found in statistics")
            print(f"Available game IDs: {[g.get('id') for g in final_stats]}")
    else:
        print(f"❌ Failed to get final stats: HTTP {stats_response.status_code}")
    
    # Step 5: Check winners API
    print("\nStep 5: Checking winners API...")
    winners_response = requests.get(f"{API_BASE}/statistics/winners", timeout=5)
    if winners_response.status_code == 200:
        winners = winners_response.json()
        print(f"Winners found: {len(winners)}")
        
        if winners:
            for winner in winners[:3]:  # Show first 3
                print(f"  Winner: {winner.get('name')} - {winner.get('stars')} stars - ${winner.get('price', 0):,}")
        else:
            print("  No winners found")
    else:
        print(f"❌ Failed to get winners: HTTP {winners_response.status_code}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    debug_game_completion()