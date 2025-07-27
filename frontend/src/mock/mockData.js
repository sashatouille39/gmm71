// Mock data pour Game Master Manager

// Rôles des joueurs avec probabilités
export const PLAYER_ROLES = {
  normal: { probability: 0.60, name: "Normal", baseStats: "équilibrés", bonus: [] },
  sportif: { probability: 0.11, name: "Sportif", baseStats: "agilité", bonus: ["+2 force"] },
  peureux: { probability: 0.10, name: "Peureux", baseStats: "faibles", bonus: ["-4 répartis"] },
  brute: { probability: 0.11, name: "La Brute", baseStats: "force", bonus: ["+2 agilité", "intimidation"] },
  intelligent: { probability: 0.07, name: "L'Intelligent", baseStats: "intelligence", bonus: ["+2 aléatoire", "manipulation"] },
  zero: { probability: 0.01, name: "Le Zéro", baseStats: "aléatoires 4-10", bonus: ["très manipulateur"] }
};

// Nationalités cohérentes
export const NATIONALITIES = [
  "Coréenne", "Japonaise", "Chinoise", "Américaine", "Française", "Allemande", 
  "Britannique", "Italienne", "Espagnole", "Russe", "Brésilienne", "Indienne",
  "Australienne", "Canadienne", "Mexicaine", "Turque", "Égyptienne", "Nigériane"
];

// Formes de visages
export const FACE_SHAPES = [
  "Ovale", "Rond", "Carré", "Rectangulaire", "Triangulaire", "Cœur", 
  "Losange", "Oblong", "Poire", "Hexagonal", "Pentagonal", "Allongé",
  "Large", "Étroit", "Angular", "Doux"
];

// Couleurs de peau
export const SKIN_COLORS = [
  "#FDF2E9", "#FAE7D0", "#F8D7C0", "#F6C8A0", "#F4B980", "#E8A456",
  "#D49156", "#C07D46", "#AC6A36", "#985726", "#844516", "#703306",
  "#5C2100", "#481000", "#340000", "#FFEEE6", "#FFE4D6", "#FFDAC6",
  "#FFD0B6", "#FFC6A6", "#FFBC96", "#FFB286", "#FFA876", "#FF9E66",
  "#FF9456", "#E88A46", "#D18036", "#BA7626", "#A36C16"
];

// Coiffures
export const HAIRSTYLES = [
  "Cheveux courts", "Cheveux longs", "Bob", "Pixie", "Afro", "Dreadlocks",
  "Tresses", "Queue de cheval", "Chignon", "Mohawk", "Undercut", "Fade",
  "Pompadour", "Quiff", "Buzz cut", "Crew cut", "Slicked back", "Wavy",
  "Curly", "Straight", "Layered", "Shag", "Mullet", "Top knot", "Man bun",
  "Cornrows", "Bangs", "Side swept", "Spiky", "Messy", "Sleek", "Volume",
  "Textured", "Choppy", "Blunt", "Asymmetrical", "Retro", "Modern",
  "Classic", "Edgy", "Romantic", "Bohemian", "Punk", "Gothic", "Vintage",
  "Contemporary", "Trendy", "Timeless", "Elegant", "Casual", "Formal",
  "Sporty", "Artistic", "Creative", "Bold", "Subtle", "Natural", "Styled",
  "Wild", "Tame", "Flowing", "Structured", "Loose", "Tight", "Soft",
  "Hard", "Smooth", "Rough", "Fine", "Thick", "Thin", "Full", "Sparse",
  "Dense", "Light", "Heavy", "Bouncy", "Flat", "Voluminous", "Sleek"
];

// Couleurs de cheveux
export const HAIR_COLORS = [
  "#2C1B18", "#3C2414", "#4A2C20", "#5D4037", "#6D4C41", "#8D6E63",
  "#A1887F", "#BCAAA4", "#D7CCC8", "#EFEBE9", "#FFF3E0", "#FFE0B2",
  "#FFCC02", "#FFA000", "#FF8F00", "#FF6F00", "#E65100", "#D84315",
  "#BF360C", "#A0522D", "#8B4513", "#654321", "#800080", "#9932CC",
  "#BA55D3", "#DA70D6", "#EE82EE", "#FF1493", "#FF69B4", "#FFB6C1"
];

// Épreuves du jeu
export const GAME_EVENTS = [
  // Épreuves classiques Squid Game
  { id: 1, name: "Feu rouge, Feu vert", type: "agilité", difficulty: 3, description: "Avancez quand c'est vert, arrêtez-vous au rouge" },
  { id: 2, name: "Pont de verre", type: "intelligence", difficulty: 8, description: "Choisissez le bon verre pour traverser" },
  { id: 3, name: "Billes", type: "intelligence", difficulty: 6, description: "Jeu de stratégie avec des billes" },
  { id: 4, name: "Tir à la corde", type: "force", difficulty: 7, description: "Tirez plus fort que l'équipe adverse" },
  { id: 5, name: "Gaufres au sucre", type: "agilité", difficulty: 5, description: "Découpez la forme sans la casser" },
  
  // Épreuves originales
  { id: 6, name: "Labyrinthe mortel", type: "intelligence", difficulty: 6, description: "Trouvez la sortie avant le temps" },
  { id: 7, name: "Combat de gladiateurs", type: "force", difficulty: 9, description: "Battez-vous pour survivre" },
  { id: 8, name: "Énigme du sphinx", type: "intelligence", difficulty: 8, description: "Résolvez l'énigme ou mourez" },
  { id: 9, name: "Course d'obstacles", type: "agilité", difficulty: 7, description: "Premier arrivé, premier servi" },
  { id: 10, name: "Jeu de la confiance", type: "intelligence", difficulty: 5, description: "Faites confiance ou trahissez" }
];

// VIP avec personnalités
export const VIP_CHARACTERS = [
  {
    id: 1,
    name: "Le Cochon Sale",
    mask: "cochon-sale",
    personality: "absurde",
    dialogues: [
      "Ah ! Comme dirait mon grand-père... euh... il est mort !",
      "Cette épreuve me rappelle quand j'ai mangé un sandwich... au thon !",
      "MAGNIFIQUE ! Comme la fois où j'ai perdu mes clés dans un aquarium !",
      "Ho ho ho ! Exactement comme dans Titanic... ou était-ce Bambi ?",
      "Mes chers amis, ceci me rappelle ma première pizza... elle était carrée !"
    ],
    bets: 0,
    favoritePlayer: null
  },
  {
    id: 2,
    name: "Le Porc Propre", 
    mask: "cochon-propre",
    personality: "raffiné",
    dialogues: [
      "Quelle élégance dans cette brutalité, très cher !",
      "L'art de mourir avec classe, tout à fait remarquable.",
      "Ces jeux me rappellent les soirées à l'opéra... en plus sanglant.",
      "Magnifique chorégraphie de la mort, mes compliments !",
      "Un spectacle digne des plus grands maîtres !"
    ],
    bets: 0,
    favoritePlayer: null
  },
  {
    id: 3,
    name: "Le Triangle",
    mask: "triangle",
    personality: "calculateur",
    dialogues: [
      "Les probabilités de survie sont... intéressantes.",
      "Analyse statistique : 73.4% de chances d'élimination.",
      "Variables imprévues détectées dans le comportement.",
      "Calculs recalculés. Nouveau pronostic en cours.",
      "Données insuffisantes. Observation requise."
    ],
    bets: 0,
    favoritePlayer: null
  }
];

// Célébrités fictives
export const MOCK_CELEBRITIES = [
  // Célébrités 5 étoiles (Anciens vainqueurs)
  {
    id: 1,
    name: "Viktor Kozlov",
    category: "Ancien vainqueur",
    stars: 5,
    price: 50000,
    nationality: "Russe",
    wins: 3,
    stats: { intelligence: 9, force: 8, agilité: 10 },
    biography: "Triple vainqueur légendaire, maître de tous les jeux."
  },
  {
    id: 2,
    name: "Luna Hartwell",
    category: "Ancienne vainqueur",
    stars: 5,
    price: 45000,
    nationality: "Britannique",
    wins: 2,
    stats: { intelligence: 10, force: 6, agilité: 9 },
    biography: "Stratège exceptionnelle, gagnante de deux éditions consécutives."
  },
  
  // Célébrités 4 étoiles
  {
    id: 3,
    name: "Marco Rossini",
    category: "Sportif",
    stars: 4,
    price: 25000,
    nationality: "Italienne",
    stats: { intelligence: 6, force: 9, agilité: 10 },
    biography: "Champion olympique de décathlon."
  },
  {
    id: 4,
    name: "Dr. Sarah Chen",
    category: "Scientifique",
    stars: 4,
    price: 22000,
    nationality: "Chinoise",
    stats: { intelligence: 10, force: 4, agilité: 6 },
    biography: "Prix Nobel de physique, génie reconnu mondialement."
  },
  
  // Célébrités 3 étoiles
  {
    id: 5,
    name: "Jake Morrison",
    category: "Acteur",
    stars: 3,
    price: 15000,
    nationality: "Américaine",
    stats: { intelligence: 7, force: 6, agilité: 7 },
    biography: "Star de cinéma action, cascadeur expérimenté."
  },
  {
    id: 6,
    name: "Isabella Santos",
    category: "Chanteuse",
    stars: 3,
    price: 12000,
    nationality: "Brésilienne",
    stats: { intelligence: 8, force: 5, agilité: 8 },
    biography: "Diva internationale, voix d'or du Brésil."
  },
  
  // Célébrités 2 étoiles
  {
    id: 7,
    name: "Tommy Fletcher",
    category: "Influenceur",
    stars: 2,
    price: 8000,
    nationality: "Australienne",
    stats: { intelligence: 6, force: 5, agilité: 6 },
    biography: "Influenceur populaire, 50M de followers."
  },
  {
    id: 8,
    name: "Marie Dubois",
    category: "Chef",
    stars: 2,
    price: 6000,
    nationality: "Française",
    stats: { intelligence: 7, force: 4, agilité: 5 },
    biography: "Chef étoilée, reine de la gastronomie française."
  }
];

// Uniformes et personnalisation
export const UNIFORM_STYLES = ["Classic", "Moderne", "Vintage", "Sport", "Élégant"];
export const UNIFORM_PATTERNS = ["Uni", "Rayures", "Carreaux", "Points", "Floral", "Géométrique"];
export const UNIFORM_COLORS = ["Rouge", "Bleu", "Vert", "Jaune", "Rose", "Violet", "Orange", "Noir", "Blanc"];

// Générateur de joueurs aléatoires
export const generateRandomPlayer = (id) => {
  // Sélection du rôle selon les probabilités
  const rand = Math.random();
  let cumulativeProbability = 0;
  let selectedRole = 'normal';
  
  for (const [role, data] of Object.entries(PLAYER_ROLES)) {
    cumulativeProbability += data.probability;
    if (rand <= cumulativeProbability) {
      selectedRole = role;
      break;
    }
  }
  
  const roleData = PLAYER_ROLES[selectedRole];
  const nationality = NATIONALITIES[Math.floor(Math.random() * NATIONALITIES.length)];
  const gender = Math.random() > 0.5 ? 'M' : 'F';
  
  // Génération des stats selon le rôle
  let stats = { intelligence: 0, force: 0, agilité: 0 };
  let totalPoints = 12;
  
  // Distribution selon le rôle
  switch (selectedRole) {
    case 'sportif':
      stats.agilité = Math.min(10, 4 + Math.floor(Math.random() * 4));
      stats.force = Math.min(10, stats.agilité - 2 + Math.floor(Math.random() * 3));
      stats.intelligence = Math.max(0, totalPoints - stats.agilité - stats.force);
      break;
    case 'brute':
      stats.force = Math.min(10, 4 + Math.floor(Math.random() * 4));
      stats.agilité = Math.min(10, stats.force - 2 + Math.floor(Math.random() * 3));
      stats.intelligence = Math.max(0, totalPoints - stats.force - stats.agilité);
      break;
    case 'intelligent':
      stats.intelligence = Math.min(10, 4 + Math.floor(Math.random() * 4));
      const bonus = Math.floor(Math.random() * 3);
      if (bonus === 0) stats.force += 2;
      else if (bonus === 1) stats.agilité += 2;
      else stats.intelligence += 2;
      totalPoints = 14; // +2 bonus
      break;
    case 'peureux':
      totalPoints = 8; // -4 malus
      break;
    case 'zero':
      stats.intelligence = 4 + Math.floor(Math.random() * 7);
      stats.force = 4 + Math.floor(Math.random() * 7);
      stats.agilité = 4 + Math.floor(Math.random() * 7);
      break;
    default: // normal
      break;
  }
  
  // Distribution équilibrée pour les normaux et ajustements
  if (selectedRole === 'normal' || selectedRole === 'peureux') {
    const remaining = totalPoints;
    stats.intelligence = Math.floor(Math.random() * (remaining / 3)) + 1;
    stats.force = Math.floor(Math.random() * ((remaining - stats.intelligence) / 2)) + 1;
    stats.agilité = Math.max(0, remaining - stats.intelligence - stats.force);
  }
  
  return {
    id,
    number: String(id).padStart(3, '0'),
    name: generateRandomName(nationality, gender),
    nationality,
    gender,
    role: selectedRole,
    stats,
    portrait: generatePortraitData(nationality),
    uniform: {
      style: UNIFORM_STYLES[Math.floor(Math.random() * UNIFORM_STYLES.length)],
      color: UNIFORM_COLORS[Math.floor(Math.random() * UNIFORM_COLORS.length)],
      pattern: UNIFORM_PATTERNS[Math.floor(Math.random() * UNIFORM_PATTERNS.length)]
    },
    alive: true,
    kills: 0,
    betrayals: 0,
    survivedEvents: 0,
    totalScore: 0
  };
};

const generateRandomName = (nationality, gender) => {
  const names = {
    'Coréenne': {
      M: ['Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Joon-ho'],
      F: ['Seo-yeon', 'Min-seo', 'Ji-woo', 'Ha-eun', 'Soo-jin']
    },
    'Japonaise': {
      M: ['Hiroshi', 'Takeshi', 'Akira', 'Yuki', 'Daiki'],
      F: ['Sakura', 'Yuki', 'Ai', 'Rei', 'Mana']
    },
    'Française': {
      M: ['Pierre', 'Jean', 'Michel', 'Alain', 'Philippe'],
      F: ['Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine']
    },
    // Ajouter plus de noms par nationalité...
  };
  
  const nationalityNames = names[nationality] || names['Française'];
  const genderNames = nationalityNames[gender];
  return genderNames[Math.floor(Math.random() * genderNames.length)];
};

const generatePortraitData = (nationality) => {
  // Génération cohérente selon la nationalité
  const skinColorIndex = getSkinColorByNationality(nationality);
  
  return {
    faceShape: FACE_SHAPES[Math.floor(Math.random() * FACE_SHAPES.length)],
    skinColor: SKIN_COLORS[skinColorIndex],
    hairstyle: HAIRSTYLES[Math.floor(Math.random() * HAIRSTYLES.length)],
    hairColor: HAIR_COLORS[Math.floor(Math.random() * HAIR_COLORS.length)],
    eyeColor: generateEyeColor(),
    eyeShape: generateEyeShape()
  };
};

const getSkinColorByNationality = (nationality) => {
  const ranges = {
    'Coréenne': [0, 8],
    'Japonaise': [0, 8],
    'Chinoise': [2, 10],
    'Européenne': [0, 5],
    'Africaine': [15, 24],
    'Indienne': [8, 18],
    // etc...
  };
  
  const range = ranges[nationality] || [0, 15];
  return range[0] + Math.floor(Math.random() * (range[1] - range[0]));
};

const generateEyeColor = () => {
  const colors = ['#8B4513', '#654321', '#2F4F2F', '#483D8B', '#556B2F', '#000000'];
  return colors[Math.floor(Math.random() * colors.length)];
};

const generateEyeShape = () => {
  const shapes = ['Amande', 'Rond', 'Allongé', 'Tombant', 'Relevé', 'Petit', 'Grand'];
  return shapes[Math.floor(Math.random() * shapes.length)];
};

// État initial du jeu
export const INITIAL_GAME_STATE = {
  money: 50000,
  vipSalonLevel: 1,
  unlockedUniforms: [],
  unlockedPatterns: [],
  gameStats: {
    totalGamesPlayed: 0,
    totalKills: 0,
    totalBetrayals: 0,
    favoriteCelebrity: null
  }
};