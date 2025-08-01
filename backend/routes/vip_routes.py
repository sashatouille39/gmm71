from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.vip_service import VipService
from models.game_models import VipCharacter, VipBet
import uuid
from datetime import datetime

router = APIRouter(prefix="/api")  # Ajouter le préfixe /api

# Stockage temporaire des VIPs actifs par jeu (remplacer par base de données plus tard)
active_vips_by_game: Dict[str, List[VipCharacter]] = {}
vip_bets: Dict[str, List[VipBet]] = {}

@router.get("/vips/salon/{salon_level}", response_model=List[VipCharacter])
async def get_salon_vips(salon_level: int):
    """Récupère les VIPs pour un niveau de salon donné"""
    try:
        capacity_map = {1: 1, 2: 3, 3: 5, 4: 8, 5: 10, 6: 12, 7: 15, 8: 17, 9: 20}
        capacity = capacity_map.get(salon_level, 3)
        
        vips = VipService.get_random_vips(capacity)
        
        return vips
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des VIPs: {str(e)}")

@router.get("/vips/game/{game_id}", response_model=List[VipCharacter])  
async def get_game_vips(game_id: str, salon_level: int = 1):
    """Récupère ou génère les VIPs pour une partie spécifique"""
    try:
        # Si des VIPs sont déjà assignés à cette partie, les retourner
        if game_id in active_vips_by_game:
            return active_vips_by_game[game_id]
        
        # Sinon, générer de nouveaux VIPs pour cette partie
        capacity_map = {1: 1, 2: 3, 3: 5, 4: 8, 5: 10, 6: 12, 7: 15, 8: 17, 9: 20}
        capacity = capacity_map.get(salon_level, 3)
        
        vips = VipService.get_random_vips(capacity)
        active_vips_by_game[game_id] = vips
        
        return vips
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des VIPs: {str(e)}")

@router.post("/vips/game/{game_id}/refresh")
async def refresh_game_vips(game_id: str, salon_level: int = 1):
    """Génère de nouveaux VIPs pour une partie (nouveau jeu)"""
    try:
        capacity_map = {1: 1, 2: 3, 3: 5, 4: 8, 5: 10, 6: 12, 7: 15, 8: 17, 9: 20}
        capacity = capacity_map.get(salon_level, 3)
        
        # Générer de nouveaux VIPs
        vips = VipService.get_random_vips(capacity)
        active_vips_by_game[game_id] = vips
        
        return {"message": "VIPs rafraîchis avec succès", "vips": vips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du rafraîchissement des VIPs: {str(e)}")

@router.get("/vips/all", response_model=List[VipCharacter])
async def get_all_vips():
    """Récupère tous les VIPs disponibles dans la base de données"""
    try:
        return VipService.get_all_vips()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de tous les VIPs: {str(e)}")

@router.post("/vips/bet")
async def create_vip_bet(vip_id: str, game_id: str, player_id: str, amount: int, event_id: int = None):
    """Crée un pari VIP"""
    try:
        bet = VipBet(
            vip_id=vip_id,
            game_id=game_id, 
            player_id=player_id,
            amount=amount,
            event_id=event_id
        )
        
        if game_id not in vip_bets:
            vip_bets[game_id] = []
        
        vip_bets[game_id].append(bet)
        
        return {"message": "Pari VIP créé avec succès", "bet_id": bet.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du pari: {str(e)}")

@router.get("/vips/bets/{game_id}")
async def get_game_bets(game_id: str):
    """Récupère tous les paris pour une partie"""
    try:
        return vip_bets.get(game_id, [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des paris: {str(e)}")

@router.get("/vips/earnings/{game_id}")
async def calculate_vip_earnings(game_id: str):
    """Calcule les gains des VIPs pour une partie"""
    try:
        game_vips = active_vips_by_game.get(game_id, [])
        total_earnings = sum(vip.viewing_fee for vip in game_vips)
        
        return {
            "game_id": game_id,
            "total_vip_earnings": total_earnings,
            "vip_count": len(game_vips),
            "average_fee": total_earnings // len(game_vips) if game_vips else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des gains: {str(e)}")