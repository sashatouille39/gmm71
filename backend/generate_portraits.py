"""
Script pour générer un ensemble initial de portraits par calques
Cela permet de pré-générer des portraits pour accélérer la génération de joueurs
"""
import asyncio
import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.portrait_generator_service import portrait_service


async def generate_initial_portraits():
    """Génère un ensemble initial de portraits pour les nationalités les plus courantes"""
    
    # Nationalités à générer (les plus courantes dans le jeu)
    nationalities_to_generate = [
        'Français',
        'Américain',
        'Britannique',
        'Japonais',
        'Chinois',
        'Brésilien',
        'Indien',
        'Nigérian',
        'Espagnol',
        'Allemand',
    ]
    
    genders = ['male', 'female']
    variations_per_combo = 2  # 2 variations par combinaison nationalité/genre
    
    print(f"🎨 Génération de portraits pour {len(nationalities_to_generate)} nationalités")
    print(f"📊 Total à générer: {len(nationalities_to_generate)} × {len(genders)} × {variations_per_combo} = {len(nationalities_to_generate) * len(genders) * variations_per_combo} portraits")
    print("⏱️  Temps estimé: ~2-3 minutes (chaque portrait prend ~20-30 secondes)\n")
    
    total_generated = 0
    total_failed = 0
    
    for nationality in nationalities_to_generate:
        for gender in genders:
            print(f"\n🌍 {nationality} - {gender}")
            print("=" * 60)
            
            for i in range(variations_per_combo):
                try:
                    print(f"  Variation {i+1}/{variations_per_combo}...")
                    
                    portrait_layers = await portrait_service.generate_portrait_layers_set(
                        nationality=nationality,
                        gender=gender,
                        age=25,
                        set_id=i + 1
                    )
                    
                    print(f"  ✅ Portrait généré : {len(portrait_layers)} calques")
                    total_generated += 1
                    
                except Exception as e:
                    print(f"  ❌ Erreur: {str(e)}")
                    total_failed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Génération terminée !")
    print(f"📊 Portraits générés avec succès: {total_generated}")
    print(f"❌ Échecs: {total_failed}")
    print(f"📁 Les portraits sont stockés dans: /app/backend/static/portraits/")
    print("=" * 60)


if __name__ == "__main__":
    print("🎨 Générateur de portraits par calques")
    print("=" * 60)
    print("Ce script va générer des portraits semi-réalistes par IA")
    print("Les portraits seront stockés sous forme de calques PNG")
    print("=" * 60)
    print("")
    
    # Lancer la génération
    asyncio.run(generate_initial_portraits())
