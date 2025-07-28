from typing import List
import random
from models.game_models import VipCharacter

class VipService:
    
    # Base de données complète de 50 VIPs avec masques d'animaux/insectes
    _ALL_VIPS = [
        # Mammifères terrestres
        VipCharacter(
            name="Le Loup Alpha", mask="loup", personality="dominateur",
            dialogues=["La meute ne survit que par la force du plus fort.", "Seuls les alphas méritent de régner.", "La faiblesse sera éliminée.", "Le sang appelle le sang.", "Hurlez avec moi ou mourez seuls."]
        ),
        VipCharacter(
            name="Le Renard Rusé", mask="renard", personality="manipulateur",
            dialogues=["L'intelligence prime sur la force brute.", "Tous les pièges sont beaux à voir.", "La ruse est l'arme des sages.", "Qui sème le chaos récolte le pouvoir.", "Les naïfs font les meilleurs spectacles."]
        ),
        VipCharacter(
            name="L'Ours Brutal", mask="ours", personality="violent",
            dialogues=["GRAAAAH ! Plus de sang !", "Écrasez-les tous comme des fourmis !", "La violence est la seule vérité !", "Que les faibles périssent !", "DESTRUCTION TOTALE !"]
        ),
        VipCharacter(
            name="Le Chat Mystérieux", mask="chat", personality="énigmatique",
            dialogues=["Nine lives, but only one game...", "Curiosity killed more than cats.", "In shadows, truth reveals itself.", "Purr... the hunt begins.", "Every mouse thinks it can escape."]
        ),
        VipCharacter(
            name="L'Éléphant Sage", mask="elephant", personality="philosophe",
            dialogues=["La mémoire conserve toutes les tragédies.", "Rien n'est oublié, tout est préservé.", "La sagesse naît de l'observation des cycles.", "Les anciens ont tout vu avant nous.", "La patience est l'arme des éternels."]
        ),
        VipCharacter(
            name="Le Lion Impérial", mask="lion", personality="royal",
            dialogues=["Nous sommes le roi de cette jungle moderne.", "Seuls les nobles comprennent l'art du spectacle.", "La majesté exige des sacrifices.", "Que les sujets divertissent leur monarque.", "Couronnons le plus digne de survivre."]
        ),
        VipCharacter(
            name="Le Tigre Solitaire", mask="tigre", personality="chasseur",
            dialogues=["La chasse est un art, pas un massacre.", "Chaque proie mérite un prédateur digne.", "Rayures de sang sur toile de chair.", "Le silence précède toujours l'attaque.", "Un seul bond, une seule mort."]
        ),
        VipCharacter(
            name="Le Singe Chaotique", mask="singe", personality="fou",
            dialogues=["Ahahah ! Chaos ! Chaos ! Chaos !", "Dansez, marionnettes ! Dansez !", "Bananes et cervelles, même combat !", "Singe voit, singe fait... TUER !", "Grimpons vers l'apocalypse !"]
        ),
        
        # Oiseaux
        VipCharacter(
            name="L'Aigle Impérial", mask="aigle", personality="observateur",
            dialogues=["Du haut de mon perchoir, je vois tout.", "Les faibles ne méritent pas de voler.", "La mort fond du ciel comme un rapace.", "Mes serres ne ratent jamais leur proie.", "L'altitude donne la perspective sur la mortalité."]
        ),
        VipCharacter(
            name="Le Corbeau Prophète", mask="corbeau", personality="oracle",
            dialogues=["Croah ! La mort approche !", "Les présages ne mentent jamais.", "Corbeau noir, destin noir.", "Je me nourris des cadavres à venir.", "L'apocalypse a des ailes noires."]
        ),
        VipCharacter(
            name="La Chouette Nocturne", mask="chouette", personality="mystique",
            dialogues=["La nuit révèle la véritable nature.", "Hoot... qui survivra à l'aube ?", "Mes yeux percent l'obscurité des âmes.", "La sagesse nocturne guide ma vision.", "Dans le silence, j'entends leurs peurs."]
        ),
        VipCharacter(
            name="Le Vautour Charognard", mask="vautour", personality="nécrophage",
            dialogues=["Mmmh, l'odeur de la mort imminente.", "Les charognes sont mes mets préférés.", "Planons au-dessus du carnage.", "Plus ils meurent, mieux je me nourris.", "La décomposition est un art délicat."]
        ),
        VipCharacter(
            name="Le Paon Vaniteux", mask="paon", personality="narcissique",
            dialogues=["Regardez comme je suis magnifique !", "Mes plumes brillent plus que leur sang.", "Seule la beauté mérite de survivre.", "Quelle élégance dans cette violence !", "Mon reflet vaut mille vies humaines."]
        ),
        VipCharacter(
            name="Le Flamant Rose", mask="flamant", personality="excentrique",
            dialogues=["Rose comme le sang, gracieux comme la mort.", "Dansons sur une patte vers l'éternité.", "L'équilibre entre vie et mort est un art.", "Mes couleurs s'harmonisent avec le carnage.", "Filtreons les faibles de ce monde."]
        ),
        
        # Reptiles
        VipCharacter(
            name="Le Serpent Venimeux", mask="serpent", personality="traître",
            dialogues=["Sssss... le poison coule dans mes veines.", "La trahison est mon langage natal.", "Morssss fatales pour tous.", "Je rampe vers la victoire sur leurs cadavres.", "Le venin de la vérité les tuera tous."]
        ),
        VipCharacter(
            name="Le Crocodile Antique", mask="crocodile", personality="primitif",
            dialogues=["Unchanged for millions of years.", "Ancient hunger, modern prey.", "Death roll imminent.", "Prehistoric power in modern times.", "Evolution perfected with me."]
        ),
        VipCharacter(
            name="L'Iguane Zen", mask="iguane", personality="méditatif",
            dialogues=["La patience est la clé de l'observation.", "Immobile, je contemple leur agonie.", "Le temps n'existe pas pour les reptiles.", "Chaque mort est une leçon de impermanence.", "Basking in the warmth of their despair."]
        ),
        VipCharacter(
            name="La Tortue Éternelle", mask="tortue", personality="sage",
            dialogues=["J'ai vu mille générations périr.", "La lenteur révèle tous les secrets.", "Ma carapace a survécu à tous les cataclysmes.", "Time flows like blood in my presence.", "Patience... death comes to all."]
        ),
        
        # Insectes
        VipCharacter(
            name="La Mante Religieuse", mask="mante", personality="predateur",
            dialogues=["Prions avant le massacre.", "Mes griffes sont bénies par la mort.", "Dévoration sacrée en cours.", "L'oraison funèbre commence.", "God's hunter in action."]
        ),
        VipCharacter(
            name="Le Scorpion Mortel", mask="scorpion", personality="vengeur",
            dialogues=["Ma queue porte la justice finale.", "Vengeance is best served with venom.", "Sting first, ask questions never.", "Desert justice for all.", "My poison ends all arguments."]
        ),
        VipCharacter(
            name="L'Araignée Tisseuse", mask="araignee", personality="manipulateur",
            dialogues=["Ma toile capture tous les destins.", "Tissons la mort avec élégance.", "Chaque fil mène à la perdition.", "Patience... they always get trapped.", "Web of death spans generations."]
        ),
        VipCharacter(
            name="Le Scarabée Doré", mask="scarabee", personality="mystique",
            dialogues=["Doré comme les sarcophages pharaoniques.", "La mort est un passage vers l'éternité.", "Roulons vers l'au-delà ensemble.", "Ancient wisdom in modern suffering.", "Golden death for chosen ones."]
        ),
        VipCharacter(
            name="La Libellule Hypnotique", mask="libellule", personality="envoûteur",
            dialogues=["Mes ailes dansent avec la mort.", "Hypnose fatale en préparation.", "Iridescent wings, dark intentions.", "Water skimming towards doom.", "Transparency reveals hidden truths."]
        ),
        VipCharacter(
            name="Le Papillon des Ténèbres", mask="papillon", personality="mélancolique",
            dialogues=["Metamorphosis into eternal darkness.", "Beauty fades, death remains.", "From cocoon to tomb.", "Wings of sorrow carry souls away.", "Final transformation begins now."]
        ),
        
        # Créatures aquatiques
        VipCharacter(
            name="Le Requin Blanc", mask="requin", personality="prédateur",
            dialogues=["Sang dans l'eau, festin assuré.", "Mâchoires d'acier, appétit éternel.", "Ocean's apex predator watching.", "Chum the waters with their fear.", "Perfect killing machine activated."]
        ),
        VipCharacter(
            name="La Pieuvre Tentaculaire", mask="pieuvre", personality="manipulateur",
            dialogues=["Huit tentacules, mille possibilités de mort.", "Encre noire comme leur destin.", "Intelligence alien observing.", "Suction cups taste their despair.", "Ancient wisdom in modern depths."]
        ),
        VipCharacter(
            name="Le Homard Blindé", mask="homard", personality="brutal",
            dialogues=["Pinces d'acier pour écraser les os.", "Carapace impénétrable, volonté inébranlable.", "Crustacé royal du carnage.", "Boil them alive metaphorically.", "Exoskeleton protects dark soul."]
        ),
        VipCharacter(
            name="L'Hippocampe Mystique", mask="hippocampe", personality="sage",
            dialogues=["Courants marins portent leurs âmes.", "Graceful death dance underwater.", "Paternal instincts for destruction.", "Vertical swimming towards doom.", "Oceanic wisdom flows through me."]
        ),
        
        # Créatures mythiques/exotiques
        VipCharacter(
            name="Le Dragon d'Obsidienne", mask="dragon", personality="impérial",
            dialogues=["Mes écailles brillent du sang des anciens.", "Fire breath purifies the weak.", "Hoard of souls in my treasury.", "Millennia of wisdom in destruction.", "Ancient power in modern form."]
        ),
        VipCharacter(
            name="Le Phénix Noir", mask="phenix", personality="cyclique",
            dialogues=["De leurs cendres renaîtra ma gloire.", "Death and rebirth, eternal cycle.", "Ashes to ashes, all return to me.", "Fire cleanses, death redeems.", "Resurrection through annihilation."]
        ),
        VipCharacter(
            name="La Chauve-Souris Nocturne", mask="chauve-souris", personality="vampirique",
            dialogues=["Sonar détecte leur terreur.", "Night hunter in blood lust.", "Echolocation finds all prey.", "Darkness is my domain.", "Wings of night bring death."]
        ),
        VipCharacter(
            name="Le Pangolin Blindé", mask="pangolin", personality="défensif",
            dialogues=["Ma carapace a survécu aux extinctions.", "Rolled up, watching world burn.", "Scales of justice weigh souls.", "Ancient armor, eternal vigilance.", "Protected observer of chaos."]
        ),
        VipCharacter(
            name="Le Caméléon Invisible", mask="cameleon", personality="observateur",
            dialogues=["Je change selon l'humeur du massacre.", "Eyes see all directions simultaneously.", "Camouflage hides true intentions.", "Adaptation is survival key.", "Color-coded death approaches."]
        ),
        
        # Créatures polaires/exotiques
        VipCharacter(
            name="Le Pingouin Aristocrate", mask="pingouin", personality="snob",
            dialogues=["Smoking et élégance polaire.", "Tuxedo for every funeral.", "Formal attire for informal death.", "Waddle towards destiny with class.", "Black and white moral clarity."]
        ),
        VipCharacter(
            name="L'Ours Polaire", mask="ours-polaire", personality="survivant",
            dialogues=["Ice age survivor watching extinction.", "White death on frozen landscape.", "Polar power in global warming.", "Apex predator of frozen souls.", "Climate change refugee's revenge."]
        ),
        VipCharacter(
            name="Le Narval Mystique", mask="narval", personality="licorne",
            dialogues=["Corne magique perce les mystères.", "Arctic unicorn of the depths.", "Spiral tusk drills truth.", "Ice whale wisdom flows deep.", "Horned guardian of polar seas."]
        ),
        
        # Créatures de la jungle
        VipCharacter(
            name="Le Toucan Coloré", mask="toucan", personality="tropical",
            dialogues=["Bec géant pour croquer leurs têtes.", "Tropical colors hide dark intent.", "Rainbow beak, black heart.", "Jungle wisdom speaks through me.", "Colorful death in paradise setting."]
        ),
        VipCharacter(
            name="Le Jaguar Tacheté", mask="jaguar", personality="chasseur",
            dialogues=["Taches comme les éclaboussures de sang.", "Jungle cat with urban hunting.", "Spotted death stalks concrete prey.", "Amazonian power in modern maze.", "Rosettes mark my territory."]
        ),
        VipCharacter(
            name="Le Capibarque Zen", mask="capibara", personality="pacifique",
            dialogues=["Peaceful observer of violent ends.", "Largest rodent, smallest violence.", "Calm waters hide deep currents.", "Zen master of patient watching.", "Serenity in surrounding chaos."]
        ),
        
        # Créatures marines supplémentaires
        VipCharacter(
            name="La Raie Manta", mask="raie-manta", personality="gracieux",
            dialogues=["Gliding through oceans of blood.", "Graceful death from above.", "Ocean's angel with dark wings.", "Floating salvation or damnation.", "Gentle giant with cruel intentions."]
        ),
        VipCharacter(
            name="Le Poisson-Lune", mask="poisson-lune", personality="bizarre",
            dialogues=["Strangest fish in strangest game.", "Moonlight reflects on blood pools.", "Alien creature from deep space.", "Evolutionary joke watching comedy.", "Bizarre form, bizarre thoughts."]
        ),
        VipCharacter(
            name="L'Anguille Électrique", mask="anguille", personality="énergique",
            dialogues=["High voltage, high mortality.", "Electric personality shocks all.", "Current events flow through me.", "Shocking developments guaranteed.", "Amperage equals carnage."]
        ),
        
        # Créatures préhistoriques
        VipCharacter(
            name="Le Trilobite Fossile", mask="trilobite", personality="ancien",
            dialogues=["500 million years of observation.", "Fossil wisdom in modern setting.", "Cambrian explosion survivor.", "Ancient eyes see all patterns.", "Prehistoric patience pays off."]
        ),
        VipCharacter(
            name="L'Ammonite Spiralée", mask="ammonite", personality="cyclique",
            dialogues=["Spiral shell holds spiral thoughts.", "Geometric perfection in chaos.", "Mathematical death approaching.", "Fibonacci sequence of suffering.", "Nautical nightmare navigation."]
        ),
        
        # Créatures légendaires
        VipCharacter(
            name="Le Kraken Tentaculé", mask="kraken", personality="léviathan",
            dialogues=["From deepest trenches I arise.", "Tentacles reach across continents.", "Sea monster of modern times.", "Ancient terror in glass arena.", "Leviathan watches land dwellers die."]
        ),
        VipCharacter(
            name="La Licorne Sombre", mask="licorne", personality="corrompu",
            dialogues=["Purity corrupted by blood lust.", "Horn pierces through innocence.", "Fallen grace in darkest hour.", "Magic turned to malevolence.", "Unicorn of the apocalypse."]
        ),
        VipCharacter(
            name="Le Griffon Majestueux", mask="griffon", personality="royal",
            dialogues=["Eagle and lion combined power.", "Royal guardian of death games.", "Majestic predator from above.", "Wings and claws united in purpose.", "Noble death for ignoble deeds."]
        ),
        VipCharacter(
            name="Le Sphinx Énigmatique", mask="sphinx", personality="devinettes",
            dialogues=["Riddle me this: who dies next?", "Ancient puzzles, modern solutions.", "Guardian of deadly secrets.", "Enigma wrapped in mystery.", "Wrong answer equals death."]
        )
    ]
    
    @classmethod
    def get_default_vips(cls) -> List[VipCharacter]:
        """Retourne les VIP par défaut avec leurs dialogues"""
        return cls._ALL_VIPS[:3]  # Pour compatibilité, retourne les 3 premiers
    
    @classmethod 
    def get_random_vips(cls, count: int, exclude_ids: List[str] = None) -> List[VipCharacter]:
        """Sélectionne aléatoirement des VIPs pour un salon donné"""
        if exclude_ids is None:
            exclude_ids = []
            
        available_vips = [vip for vip in cls._ALL_VIPS if vip.id not in exclude_ids]
        
        # S'assurer qu'on ne dépasse pas le nombre de VIPs disponibles
        actual_count = min(count, len(available_vips))
        
        selected = random.sample(available_vips, actual_count)
        
        # Assigner des frais de visionnage aléatoires basés sur la personnalité
        for vip in selected:
            base_fee = random.randint(500000, 2000000)  # Entre 500k et 2M
            if vip.personality in ['royal', 'impérial', 'aristocrate']:
                vip.viewing_fee = int(base_fee * 2)  # VIPs royaux paient plus
            elif vip.personality in ['mystique', 'sage', 'oracle']:
                vip.viewing_fee = int(base_fee * 1.5)  # VIPs sages paient modérément plus
            else:
                vip.viewing_fee = base_fee
                
        return selected
    
    @classmethod
    def get_all_vips(cls) -> List[VipCharacter]:
        """Retourne tous les VIPs disponibles"""
        return cls._ALL_VIPS.copy()
        
    @classmethod
    def get_vip_by_mask(cls, mask: str) -> VipCharacter:
        """Trouve un VIP par son masque"""
        for vip in cls._ALL_VIPS:
            if vip.mask == mask:
                return vip
        return None