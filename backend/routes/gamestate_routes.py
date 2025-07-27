from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from models.game_models import GameState, GameStats, GameStateUpdate, PurchaseRequest
from services.game_service import GameService

router = APIRouter(prefix="/api/gamestate", tags=["gamestate"])

# Stockage temporaire en mémoire
game_states_db = {}

@router.get("/", response_model=GameState)
async def get_game_state(user_id: str = "default_user"):
    """Récupère l'état du jeu pour un utilisateur"""
    if user_id not in game_states_db:
        # Créer un nouvel état par défaut
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    
    return game_states_db[user_id]

@router.put("/", response_model=GameState)
async def update_game_state(update: GameStateUpdate, user_id: str = "default_user"):
    """Met à jour l'état du jeu"""
    if user_id not in game_states_db:
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    # Mettre à jour les champs fournis
    update_dict = update.dict(exclude_unset=True)
    
    for field, value in update_dict.items():
        if field == "money" and value is not None:
            game_state.money = value
        elif field == "vip_salon_level" and value is not None:
            game_state.vip_salon_level = value
        elif field == "unlocked_uniforms" and value is not None:
            game_state.unlocked_uniforms = value
        elif field == "unlocked_patterns" and value is not None:
            game_state.unlocked_patterns = value
        elif field == "owned_celebrities" and value is not None:
            game_state.owned_celebrities = value
        elif field == "game_stats" and value is not None:
            game_state.game_stats = value
    
    game_state.updated_at = datetime.utcnow()
    game_states_db[user_id] = game_state
    
    return game_state

@router.post("/purchase", response_model=GameState)
async def purchase_item(request: PurchaseRequest, user_id: str = "default_user"):
    """Achète un objet (uniforme, motif, célébrité)"""
    if user_id not in game_states_db:
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    if game_state.money < request.price:
        raise HTTPException(status_code=400, detail="Fonds insuffisants")
    
    # Déduire l'argent
    game_state.money -= request.price
    
    # Ajouter l'objet acheté selon le type
    if request.item_type == "uniform":
        if request.item_id not in game_state.unlocked_uniforms:
            game_state.unlocked_uniforms.append(request.item_id)
    elif request.item_type == "pattern":
        if request.item_id not in game_state.unlocked_patterns:
            game_state.unlocked_patterns.append(request.item_id)
    elif request.item_type == "celebrity":
        if request.item_id not in game_state.owned_celebrities:
            game_state.owned_celebrities.append(request.item_id)
    
    game_state.updated_at = datetime.utcnow()
    game_states_db[user_id] = game_state
    
    return game_state

@router.post("/reset", response_model=GameState)
async def reset_game_state(user_id: str = "default_user"):
    """Remet à zéro l'état du jeu"""
    game_state = GameState(user_id=user_id)
    game_states_db[user_id] = game_state
    return game_state

@router.post("/add-earnings")
async def add_earnings(earnings: int, user_id: str = "default_user"):
    """Ajoute des gains à l'état du jeu"""
    if user_id not in game_states_db:
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    game_state.money += earnings
    game_state.game_stats.total_earnings += earnings
    game_state.updated_at = datetime.utcnow()
    
    game_states_db[user_id] = game_state
    return {"message": f"Ajouté {earnings}$ aux gains", "new_total": game_state.money}

@router.post("/complete-game")
async def complete_game(kills: int, betrayals: int, user_id: str = "default_user"):
    """Met à jour les statistiques après une partie terminée"""
    if user_id not in game_states_db:
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    game_state.game_stats.total_games_played += 1
    game_state.game_stats.total_kills += kills
    game_state.game_stats.total_betrayals += betrayals
    game_state.updated_at = datetime.utcnow()
    
    game_states_db[user_id] = game_state
    return {"message": "Statistiques mises à jour", "stats": game_state.game_stats}

@router.post("/upgrade-salon")
async def upgrade_salon(level: int, cost: int, user_id: str = "default_user"):
    """Améliore le salon VIP"""
    if user_id not in game_states_db:
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    if game_state.money < cost:
        raise HTTPException(status_code=400, detail="Fonds insuffisants pour l'amélioration")
    
    if level <= game_state.vip_salon_level:
        raise HTTPException(status_code=400, detail="Niveau d'amélioration invalide")
    
    game_state.money -= cost
    game_state.vip_salon_level = level
    game_state.updated_at = datetime.utcnow()
    
    game_states_db[user_id] = game_state
    return {"message": f"Salon amélioré au niveau {level}", "new_level": level}