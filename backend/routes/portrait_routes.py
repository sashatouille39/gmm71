"""
Routes API pour la génération de portraits par calques
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from services.portrait_generator_service import portrait_service

router = APIRouter(prefix="/api/portraits", tags=["portraits"])


class PortraitGenerationRequest(BaseModel):
    """Requête pour générer un portrait"""
    nationality: str
    gender: str  # 'M' or 'F' ou 'male' or 'female'
    age: Optional[int] = 25
    variations: Optional[int] = 1  # Nombre de variations à générer


@router.post("/generate")
async def generate_portrait_layers(request: PortraitGenerationRequest):
    """
    Génère des calques de portrait cohérents avec la nationalité
    """
    try:
        # Normaliser le genre
        gender = 'male' if request.gender.upper() == 'M' or request.gender.lower() == 'male' else 'female'
        
        # Générer les variations demandées
        generated_portraits = []
        
        for i in range(request.variations):
            portrait_layers = await portrait_service.generate_portrait_layers_set(
                nationality=request.nationality,
                gender=gender,
                age=request.age,
                set_id=i + 1
            )
            generated_portraits.append(portrait_layers)
        
        return {
            "success": True,
            "nationality": request.nationality,
            "gender": gender,
            "age": request.age,
            "portraits": generated_portraits,
            "message": f"{len(generated_portraits)} portrait(s) généré(s) avec succès"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du portrait: {str(e)}"
        )


@router.get("/available/{nationality}/{gender}")
async def get_available_portraits(nationality: str, gender: str):
    """
    Retourne la liste des portraits disponibles pour une nationalité et un genre
    """
    try:
        # Normaliser le genre
        gender_param = 'male' if gender.upper() == 'M' or gender.lower() == 'male' else 'female'
        
        region = portrait_service.get_region_for_nationality(nationality)
        available = portrait_service.get_available_portraits_for_region(region, gender_param)
        
        return {
            "success": True,
            "nationality": nationality,
            "region": region,
            "gender": gender_param,
            "count": len(available),
            "portraits": available
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des portraits: {str(e)}"
        )


@router.get("/regions")
async def get_available_regions():
    """
    Retourne la liste des régions disponibles avec leurs caractéristiques
    """
    return {
        "success": True,
        "regions": portrait_service.SKIN_COLOR_PALETTES,
        "nationality_mapping": portrait_service.NATIONALITY_TO_REGION
    }


@router.post("/batch-generate")
async def batch_generate_portraits(
    nationalities: List[str],
    genders: Optional[List[str]] = None,
    variations_per_combination: int = 2
):
    """
    Génère des portraits en lot pour plusieurs nationalités
    Utile pour pré-générer un ensemble de portraits
    """
    try:
        if not genders:
            genders = ['male', 'female']
        
        total_generated = 0
        generation_summary = []
        
        for nationality in nationalities:
            for gender in genders:
                gender_param = 'male' if gender.upper() == 'M' or gender.lower() == 'male' else 'female'
                
                for i in range(variations_per_combination):
                    try:
                        portrait_layers = await portrait_service.generate_portrait_layers_set(
                            nationality=nationality,
                            gender=gender_param,
                            age=25,  # Âge par défaut
                            set_id=i + 1
                        )
                        
                        total_generated += 1
                        generation_summary.append({
                            "nationality": nationality,
                            "gender": gender_param,
                            "variation": i + 1,
                            "status": "success"
                        })
                    
                    except Exception as e:
                        generation_summary.append({
                            "nationality": nationality,
                            "gender": gender_param,
                            "variation": i + 1,
                            "status": "error",
                            "error": str(e)
                        })
        
        return {
            "success": True,
            "total_generated": total_generated,
            "total_requested": len(nationalities) * len(genders) * variations_per_combination,
            "summary": generation_summary
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération en lot: {str(e)}"
        )
