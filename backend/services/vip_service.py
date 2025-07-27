from typing import List
from models.game_models import VipCharacter

class VipService:
    
    @classmethod
    def get_default_vips(cls) -> List[VipCharacter]:
        """Retourne les VIP par défaut avec leurs dialogues"""
        return [
            VipCharacter(
                name="Le Cochon Sale",
                mask="cochon-sale",
                personality="absurde",
                dialogues=[
                    "Ah ! Comme dirait mon grand-père... euh... il est mort !",
                    "Cette épreuve me rappelle quand j'ai mangé un sandwich... au thon !",
                    "MAGNIFIQUE ! Comme la fois où j'ai perdu mes clés dans un aquarium !",
                    "Ho ho ho ! Exactement comme dans Titanic... ou était-ce Bambi ?",
                    "Mes chers amis, ceci me rappelle ma première pizza... elle était carrée !",
                    "Splendide ! Ça me fait penser à mon dentiste... il avait des dents !",
                    "Formidable ! Comme cette fois où j'ai acheté des chaussettes... pour mes mains !",
                    "Extraordinaire ! Pareil que quand j'ai regardé la télé... avec mes oreilles !",
                    "Stupéfiant ! Ça ressemble à ma grand-mère... qui était un homme !",
                    "Fantastique ! Comme mon chat... qui est en fait un poisson rouge !"
                ]
            ),
            VipCharacter(
                name="Le Porc Propre",
                mask="cochon-propre",
                personality="raffiné",
                dialogues=[
                    "Quelle élégance dans cette brutalité, très cher !",
                    "L'art de mourir avec classe, tout à fait remarquable.",
                    "Ces jeux me rappellent les soirées à l'opéra... en plus sanglant.",
                    "Magnifique chorégraphie de la mort, mes compliments !",
                    "Un spectacle digne des plus grands maîtres !",
                    "Cette violence a une poésie qui me touche profondément.",
                    "Quel raffinement dans l'exécution ! Bravo, bravo !",
                    "Cette élégance mortelle mérite tous mes éloges.",
                    "Quelle sophistication dans cette barbarie !",
                    "L'esthétique de ces éliminations est tout simplement divine."
                ]
            ),
            VipCharacter(
                name="Le Triangle",
                mask="triangle",
                personality="calculateur",
                dialogues=[
                    "Les probabilités de survie sont... intéressantes.",
                    "Analyse statistique : 73.4% de chances d'élimination.",
                    "Variables imprévues détectées dans le comportement.",
                    "Calculs recalculés. Nouveau pronostic en cours.",
                    "Données insuffisantes. Observation requise.",
                    "Algorithme de prédiction mis à jour : 84.2% de mortalité.",
                    "Paramètres optimisés. Résultats conformes aux projections.",
                    "Analyse comportementale en cours... Pattern détecté.",
                    "Coefficient de risque réévalué à la hausse.",
                    "Simulation terminée. Résultats archivés."
                ]
            ),
            VipCharacter(
                name="La Sphère",
                mask="sphere",
                personality="mystérieux",
                dialogues=[
                    "L'univers tourne, et nous avec lui...",
                    "Chaque fin est un nouveau commencement.",
                    "Le destin n'est qu'une illusion du temps.",
                    "Dans le chaos, je vois l'ordre parfait.",
                    "La mort n'est qu'une transition vers l'inconnu.",
                    "Tout est écrit dans les étoiles...",
                    "Le cycle éternel recommence encore.",
                    "L'équilibre cosmique sera restauré.",
                    "Chaque âme trouve son chemin dans l'infini.",
                    "La vérité ultime se révèle dans le silence."
                ]
            ),
            VipCharacter(
                name="Le Carré",
                mask="carre",
                personality="militaire",
                dialogues=[
                    "Discipline ! Ordre ! Élimination efficace !",
                    "Protocole respecté. Mission accomplie.",
                    "Tactique exemplaire. Résultat optimal.",
                    "Formation défaillante. Élimination logique.",
                    "Stratégie déployée selon le manuel.",
                    "Commandement satisfait de l'exécution.",
                    "Opération menée avec précision militaire.",
                    "Objectif atteint. Pertes acceptables.",
                    "Manœuvre parfaitement coordonnée.",
                    "Section éliminée selon les règles d'engagement."
                ]
            )
        ]