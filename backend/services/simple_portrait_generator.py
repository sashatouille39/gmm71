"""
Générateur de calques de portraits simples et rapides avec Pillow
Alternative rapide à la génération par IA pour des tests immédiats
"""
import os
from PIL import Image, ImageDraw
import random
from typing import Dict, Tuple


class SimplePortraitGenerator:
    """Génère des calques de portraits simples avec des formes géométriques"""
    
    def __init__(self, base_path: str = "/app/backend/static/portraits"):
        self.base_path = base_path
        self.size = (256, 256)  # Taille des calques
        
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convertit une couleur hex en RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def lighten_color(self, rgb: Tuple[int, int, int], factor: float = 0.8) -> Tuple[int, int, int]:
        """Éclaircit une couleur RGB"""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
    
    def darken_color(self, rgb: Tuple[int, int, int], factor: float = 0.3) -> Tuple[int, int, int]:
        """Assombrit une couleur RGB"""
        return tuple(max(0, int(c * factor)) for c in rgb)
    
    def generate_base_layer(self, skin_color: str, filename: str) -> str:
        """Génère un calque de base (tête ovale)"""
        img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Convertir la couleur de peau
        skin_rgb = self.hex_to_rgb(skin_color)
        
        # Dessiner une tête ovale
        head_bbox = [50, 30, 206, 220]  # x1, y1, x2, y2
        draw.ellipse(head_bbox, fill=skin_rgb + (255,))
        
        # Ajouter le cou
        neck_bbox = [100, 200, 156, 256]
        draw.rectangle(neck_bbox, fill=skin_rgb + (255,))
        
        # Sauvegarder
        filepath = os.path.join(self.base_path, "base", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG')
        
        return f"/static/portraits/base/{filename}"
    
    def generate_eyes_layer(self, eye_color: str, eye_shape: str, filename: str) -> str:
        """Génère un calque d'yeux"""
        img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Couleur des yeux
        eye_rgb = self.hex_to_rgb(eye_color) if eye_color.startswith('#') else (139, 69, 19)  # Marron par défaut
        
        # Position des yeux
        left_eye_center = (90, 100)
        right_eye_center = (166, 100)
        eye_radius = 12
        
        # Dessiner les yeux blancs
        draw.ellipse([left_eye_center[0]-eye_radius-2, left_eye_center[1]-eye_radius-2,
                     left_eye_center[0]+eye_radius+2, left_eye_center[1]+eye_radius+2],
                    fill=(255, 255, 255, 255))
        draw.ellipse([right_eye_center[0]-eye_radius-2, right_eye_center[1]-eye_radius-2,
                     right_eye_center[0]+eye_radius+2, right_eye_center[1]+eye_radius+2],
                    fill=(255, 255, 255, 255))
        
        # Dessiner les iris
        iris_radius = 8
        draw.ellipse([left_eye_center[0]-iris_radius, left_eye_center[1]-iris_radius,
                     left_eye_center[0]+iris_radius, left_eye_center[1]+iris_radius],
                    fill=eye_rgb + (255,))
        draw.ellipse([right_eye_center[0]-iris_radius, right_eye_center[1]-iris_radius,
                     right_eye_center[0]+iris_radius, right_eye_center[1]+iris_radius],
                    fill=eye_rgb + (255,))
        
        # Dessiner les pupilles
        pupil_radius = 4
        draw.ellipse([left_eye_center[0]-pupil_radius, left_eye_center[1]-pupil_radius,
                     left_eye_center[0]+pupil_radius, left_eye_center[1]+pupil_radius],
                    fill=(0, 0, 0, 255))
        draw.ellipse([right_eye_center[0]-pupil_radius, right_eye_center[1]-pupil_radius,
                     right_eye_center[0]+pupil_radius, right_eye_center[1]+pupil_radius],
                    fill=(0, 0, 0, 255))
        
        # Sauvegarder
        filepath = os.path.join(self.base_path, "eyes", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG')
        
        return f"/static/portraits/eyes/{filename}"
    
    def generate_hair_layer(self, hair_color: str, gender: str, filename: str) -> str:
        """Génère un calque de cheveux"""
        img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Convertir la couleur des cheveux
        hair_rgb = self.hex_to_rgb(hair_color)
        
        if gender == 'M':
            # Cheveux courts pour homme
            # Partie supérieure de la tête
            hair_bbox = [50, 20, 206, 100]
            draw.ellipse(hair_bbox, fill=hair_rgb + (255,))
        else:
            # Cheveux longs pour femme
            # Partie supérieure
            hair_bbox = [50, 20, 206, 100]
            draw.ellipse(hair_bbox, fill=hair_rgb + (255,))
            # Cheveux qui descendent sur les côtés
            draw.polygon([(50, 80), (40, 200), (80, 200), (70, 80)], fill=hair_rgb + (255,))
            draw.polygon([(206, 80), (216, 200), (176, 200), (186, 80)], fill=hair_rgb + (255,))
        
        # Sauvegarder
        filepath = os.path.join(self.base_path, "hair", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG')
        
        return f"/static/portraits/hair/{filename}"
    
    def generate_mouth_layer(self, skin_color: str, filename: str) -> str:
        """Génère un calque de bouche"""
        img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Couleur des lèvres (un peu plus foncée que la peau)
        skin_rgb = self.hex_to_rgb(skin_color)
        lip_rgb = self.darken_color(skin_rgb, 0.7)
        
        # Dessiner la bouche (ellipse horizontale)
        mouth_bbox = [110, 150, 146, 165]
        draw.ellipse(mouth_bbox, fill=lip_rgb + (255,))
        
        # Sauvegarder
        filepath = os.path.join(self.base_path, "mouth", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG')
        
        return f"/static/portraits/mouth/{filename}"
    
    def generate_nose_layer(self, skin_color: str, filename: str) -> str:
        """Génère un calque de nez"""
        img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Couleur du nez (un peu plus foncée que la peau pour l'ombre)
        skin_rgb = self.hex_to_rgb(skin_color)
        nose_rgb = self.darken_color(skin_rgb, 0.9)
        
        # Dessiner le nez (petit triangle ou ovale)
        nose_center = (128, 120)
        nose_points = [
            (nose_center[0], nose_center[1] - 15),  # Haut
            (nose_center[0] - 10, nose_center[1] + 10),  # Bas gauche
            (nose_center[0] + 10, nose_center[1] + 10)   # Bas droit
        ]
        draw.polygon(nose_points, fill=nose_rgb + (200,))  # Légèrement transparent
        
        # Narines
        draw.ellipse([nose_center[0]-12, nose_center[1]+8, nose_center[0]-8, nose_center[1]+12],
                    fill=nose_rgb + (255,))
        draw.ellipse([nose_center[0]+8, nose_center[1]+8, nose_center[0]+12, nose_center[1]+12],
                    fill=nose_rgb + (255,))
        
        # Sauvegarder
        filepath = os.path.join(self.base_path, "nose", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG')
        
        return f"/static/portraits/nose/{filename}"
    
    def generate_complete_portrait(
        self,
        nationality: str,
        region: str,
        gender: str,
        skin_color: str,
        hair_color: str,
        eye_color: str,
        eye_shape: str,
        set_id: int = 1
    ) -> Dict[str, str]:
        """Génère un portrait complet avec tous les calques"""
        
        gender_code = 'M' if gender == 'M' or gender == 'male' else 'F'
        base_filename = f"{region}_{gender_code}_simple_{set_id}"
        
        layers = {
            'base': self.generate_base_layer(skin_color, f"{base_filename}_base.png"),
            'eyes': self.generate_eyes_layer(eye_color, eye_shape, f"{base_filename}_eyes.png"),
            'hair': self.generate_hair_layer(hair_color, gender_code, f"{base_filename}_hair.png"),
            'mouth': self.generate_mouth_layer(skin_color, f"{base_filename}_mouth.png"),
            'nose': self.generate_nose_layer(skin_color, f"{base_filename}_nose.png"),
        }
        
        return layers


# Instance globale
simple_portrait_gen = SimplePortraitGenerator()
