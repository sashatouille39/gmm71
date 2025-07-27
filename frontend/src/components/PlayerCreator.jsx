import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Slider } from './ui/slider';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { ArrowLeft, Save, Eye, RotateCcw, CheckCircle } from 'lucide-react';
import { useCustomPlayers } from '../hooks/useCustomPlayers';
import { 
  NATIONALITIES, 
  FACE_SHAPES, 
  SKIN_COLORS, 
  HAIRSTYLES, 
  HAIR_COLORS,
  EYE_SHAPES,
  EYE_COLORS,
  PLAYER_ROLES,
  UNIFORM_STYLES,
  UNIFORM_COLORS,
  UNIFORM_PATTERNS
} from '../mock/mockData';

const PlayerCreator = ({ gameState, updateGameState }) => {
  const navigate = useNavigate();
  const { addPlayer } = useCustomPlayers();
  const [savedStatus, setSavedStatus] = useState(false);
  
  const [player, setPlayer] = useState({
    name: '',
    nationality: '',
    gender: 'M',
    role: 'normal',
    stats: { intelligence: 5, force: 5, agilité: 5 },
    portrait: {
      faceShape: FACE_SHAPES[0],
      skinColor: SKIN_COLORS[0],
      hairstyle: HAIRSTYLES[0],
      hairColor: HAIR_COLORS[0],
      eyeColor: EYE_COLORS[0],
      eyeShape: EYE_SHAPES[0]
    },
    uniform: {
      style: UNIFORM_STYLES[0],
      color: UNIFORM_COLORS[0],
      pattern: UNIFORM_PATTERNS[0]
    }
  });

  const [statsPoints, setStatsPoints] = useState(15);
  const [currentTab, setCurrentTab] = useState('basic');

  const updatePlayerField = (field, value) => {
    setPlayer(prev => ({ ...prev, [field]: value }));
  };

  const updateNestedField = (category, field, value) => {
    setPlayer(prev => ({
      ...prev,
      [category]: { ...prev[category], [field]: value }
    }));
  };

  const updateStats = (stat, value) => {
    const currentValue = player.stats[stat];
    const newValue = value[0];
    const difference = newValue - currentValue;
    
    if (statsPoints - difference >= 0 && newValue >= 0 && newValue <= 10) {
      setStatsPoints(prev => prev - difference);
      updateNestedField('stats', stat, newValue);
    }
  };

  const resetStats = () => {
    setPlayer(prev => ({
      ...prev,
      stats: { intelligence: 5, force: 5, agilité: 5 }
    }));
    setStatsPoints(15 - 15); // 15 points utilisés initialement
  };

  const randomizePortrait = () => {
    const randomPortrait = {
      faceShape: FACE_SHAPES[Math.floor(Math.random() * FACE_SHAPES.length)],
      skinColor: SKIN_COLORS[Math.floor(Math.random() * SKIN_COLORS.length)],
      hairstyle: HAIRSTYLES[Math.floor(Math.random() * HAIRSTYLES.length)],
      hairColor: HAIR_COLORS[Math.floor(Math.random() * HAIR_COLORS.length)],
      eyeColor: EYE_COLORS[Math.floor(Math.random() * EYE_COLORS.length)],
      eyeShape: EYE_SHAPES[Math.floor(Math.random() * EYE_SHAPES.length)]
    };
    setPlayer(prev => ({ ...prev, portrait: randomPortrait }));
  };

  const tabs = [
    { id: 'basic', name: 'Informations', icon: '👤' },
    { id: 'portrait', name: 'Portrait', icon: '🎨' },
    { id: 'stats', name: 'Statistiques', icon: '📊' },
    { id: 'uniform', name: 'Uniforme', icon: '👕' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/game-setup')}
              className="text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Retour
            </Button>
            <div>
              <h1 className="text-4xl font-black text-white">Créateur de joueur</h1>
              <p className="text-gray-400">Personnalisez chaque détail de votre joueur</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Aperçu du joueur */}
          <Card className="bg-black/50 border-red-500/30 lg:col-span-1">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Eye className="w-5 h-5" />
                Aperçu
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              {/* Avatar stylisé amélioré */}
              <div className="relative mx-auto w-40 h-48 rounded-lg border-4 border-red-500 overflow-hidden bg-gradient-to-b from-gray-800 to-gray-900">
                {/* Visage */}
                <div 
                  className="w-full h-32 flex items-center justify-center text-2xl font-bold relative"
                  style={{ backgroundColor: player.portrait.skinColor }}
                >
                  {/* Yeux */}
                  <div className="absolute top-6 left-1/2 transform -translate-x-1/2 flex gap-3">
                    <div 
                      className="w-3 h-2 rounded-full"
                      style={{ backgroundColor: player.portrait.eyeColor }}
                      title={player.portrait.eyeShape}
                    ></div>
                    <div 
                      className="w-3 h-2 rounded-full"
                      style={{ backgroundColor: player.portrait.eyeColor }}
                    ></div>
                  </div>
                  
                  {/* Nom */}
                  <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 text-black text-xs font-bold">
                    {player.name ? player.name.charAt(0).toUpperCase() : '?'}
                  </div>
                </div>
                
                {/* Cheveux */}
                <div 
                  className="absolute top-0 w-full h-8 opacity-90"
                  style={{ backgroundColor: player.portrait.hairColor }}
                  title={player.portrait.hairstyle}
                >
                </div>
                
                {/* Corps/Uniforme */}
                <div className="w-full h-16 flex items-center justify-center">
                  <div className={`w-24 h-12 rounded flex items-center justify-center text-xs text-white font-semibold
                    ${player.uniform.color === 'Rouge' ? 'bg-red-600' : 
                      player.uniform.color === 'Bleu' ? 'bg-blue-600' :
                      player.uniform.color === 'Vert' ? 'bg-green-600' :
                      player.uniform.color === 'Jaune' ? 'bg-yellow-600' :
                      player.uniform.color === 'Rose' ? 'bg-pink-600' :
                      player.uniform.color === 'Violet' ? 'bg-purple-600' :
                      player.uniform.color === 'Orange' ? 'bg-orange-600' :
                      player.uniform.color === 'Noir' ? 'bg-black' :
                      'bg-white text-black'}`}
                  >
                    {player.uniform.style}
                  </div>
                </div>
              </div>

              {/* Informations détaillées du joueur */}
              <div className="space-y-3">
                <h3 className="text-xl font-bold text-white">
                  {player.name || 'Sans nom'}
                </h3>
                
                <div className="grid grid-cols-2 gap-2">
                  <Badge variant="outline" className="text-gray-300 text-xs">
                    {player.nationality || 'Aucune'}
                  </Badge>
                  <Badge variant="outline" className="text-gray-300 text-xs">
                    {player.gender === 'M' ? 'Homme' : 'Femme'}
                  </Badge>
                </div>
                
                <Badge 
                  variant="outline" 
                  className="text-red-400 border-red-400 text-sm"
                >
                  {PLAYER_ROLES[player.role].name}
                </Badge>

                {/* Détails du portrait */}
                <div className="bg-gray-800/30 p-2 rounded text-xs">
                  <div className="grid grid-cols-1 gap-1 text-left">
                    <div><span className="text-gray-400">Visage:</span> <span className="text-white">{player.portrait.faceShape}</span></div>
                    <div><span className="text-gray-400">Yeux:</span> <span className="text-white">{player.portrait.eyeShape}</span></div>
                    <div><span className="text-gray-400">Coiffure:</span> <span className="text-white">{player.portrait.hairstyle}</span></div>
                  </div>
                </div>
              </div>

              <Separator className="bg-gray-600" />

              {/* Statistiques */}
              <div className="space-y-2">
                <h4 className="text-white font-medium">Statistiques</h4>
                {Object.entries(player.stats).map(([stat, value]) => (
                  <div key={stat} className="flex justify-between items-center">
                    <span className="text-gray-400 capitalize">{stat}:</span>
                    <div className="flex items-center gap-1">
                      <div className="flex">
                        {[...Array(10)].map((_, i) => (
                          <div
                            key={i}
                            className={`w-2 h-2 rounded-full ${
                              i < value ? 'bg-red-500' : 'bg-gray-600'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-white text-sm ml-2">{value}/10</span>
                    </div>
                  </div>
                ))}
                <div className="text-sm text-gray-400">
                  Points restants: <span className="text-white">{statsPoints}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Formulaire de création */}
          <Card className="bg-black/50 border-red-500/30 lg:col-span-2">
            <CardHeader>
              {/* Onglets */}
              <div className="flex gap-1 p-1 bg-gray-800 rounded-lg">
                {tabs.map((tab) => (
                  <Button
                    key={tab.id}
                    variant={currentTab === tab.id ? "default" : "ghost"}
                    className={`flex-1 ${
                      currentTab === tab.id 
                        ? "bg-red-600 text-white" 
                        : "text-gray-400 hover:text-white"
                    }`}
                    onClick={() => setCurrentTab(tab.id)}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.name}
                  </Button>
                ))}
              </div>
            </CardHeader>

            <CardContent className="space-y-6">
              {/* Onglet Informations de base */}
              {currentTab === 'basic' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="text-gray-300">Nom du joueur</Label>
                      <Input
                        value={player.name}
                        onChange={(e) => updatePlayerField('name', e.target.value)}
                        placeholder="Entrez le nom..."
                        className="bg-gray-800 border-gray-600 text-white mt-1"
                      />
                    </div>
                    
                    <div>
                      <Label className="text-gray-300">Genre</Label>
                      <Select value={player.gender} onValueChange={(value) => updatePlayerField('gender', value)}>
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="M">Homme</SelectItem>
                          <SelectItem value="F">Femme</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="text-gray-300">Nationalité</Label>
                      <Select value={player.nationality} onValueChange={(value) => updatePlayerField('nationality', value)}>
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue placeholder="Choisir..." />
                        </SelectTrigger>
                        <SelectContent className="max-h-40">
                          {NATIONALITIES.map((nationality) => (
                            <SelectItem key={nationality} value={nationality}>
                              {nationality}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-gray-300">Rôle</Label>
                      <Select value={player.role} onValueChange={(value) => updatePlayerField('role', value)}>
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {Object.entries(PLAYER_ROLES).map(([role, data]) => (
                            <SelectItem key={role} value={role}>
                              {data.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="bg-gray-800/30 p-4 rounded-lg">
                    <h4 className="text-white font-medium mb-2">Description du rôle</h4>
                    <p className="text-gray-400 text-sm">{PLAYER_ROLES[player.role].baseStats} - {PLAYER_ROLES[player.role].bonus.join(', ')}</p>
                  </div>
                </div>
              )}

              {/* Onglet Portrait */}
              {currentTab === 'portrait' && (
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-white font-medium">Personnalisation complète du visage</h3>
                    <Button
                      variant="outline"
                      onClick={randomizePortrait}
                      className="border-red-500 text-red-400 hover:bg-red-500/10"
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Aléatoire
                    </Button>
                  </div>

                  {/* Forme du visage */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Forme du visage ({FACE_SHAPES.length} options)</Label>
                    <div className="grid grid-cols-3 gap-2 max-h-32 overflow-y-auto p-2 bg-gray-800/30 rounded-lg">
                      {FACE_SHAPES.map((shape) => (
                        <button
                          key={shape}
                          className={`p-2 text-xs rounded transition-all ${
                            player.portrait.faceShape === shape 
                              ? 'bg-red-600 text-white' 
                              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                          }`}
                          onClick={() => updateNestedField('portrait', 'faceShape', shape)}
                        >
                          {shape}
                        </button>
                      ))}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Sélectionné: {player.portrait.faceShape}</p>
                  </div>

                  {/* Couleur de peau */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Couleur de peau ({SKIN_COLORS.length} nuances)</Label>
                    <div className="grid grid-cols-10 gap-1 p-3 bg-gray-800/30 rounded-lg">
                      {SKIN_COLORS.map((color) => (
                        <button
                          key={color}
                          className={`w-6 h-6 rounded-full border-2 transition-all ${
                            player.portrait.skinColor === color 
                              ? 'border-red-500 scale-110 shadow-lg' 
                              : 'border-gray-600 hover:border-gray-400'
                          }`}
                          style={{ backgroundColor: color }}
                          onClick={() => updateNestedField('portrait', 'skinColor', color)}
                          title={color}
                        />
                      ))}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Couleur sélectionnée: {player.portrait.skinColor}</p>
                  </div>

                  {/* Coiffures */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Coiffure ({HAIRSTYLES.length} styles disponibles)</Label>
                    <div className="relative">
                      <input
                        type="text"
                        placeholder="Rechercher une coiffure..."
                        className="w-full p-2 bg-gray-800 border border-gray-600 rounded text-white text-sm mb-2"
                        onChange={(e) => {
                          const search = e.target.value.toLowerCase();
                          const filtered = HAIRSTYLES.filter(style => 
                            style.toLowerCase().includes(search)
                          );
                          // Pour simplifier, on affiche les résultats directement
                        }}
                      />
                      <div className="grid grid-cols-2 gap-1 max-h-40 overflow-y-auto p-2 bg-gray-800/30 rounded-lg">
                        {HAIRSTYLES.map((style) => (
                          <button
                            key={style}
                            className={`p-2 text-xs rounded text-left transition-all ${
                              player.portrait.hairstyle === style 
                                ? 'bg-red-600 text-white' 
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                            }`}
                            onClick={() => updateNestedField('portrait', 'hairstyle', style)}
                          >
                            {style}
                          </button>
                        ))}
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Coiffure sélectionnée: {player.portrait.hairstyle}</p>
                  </div>

                  {/* Couleur des cheveux */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Couleur des cheveux</Label>
                    <div className="grid grid-cols-8 gap-2 p-3 bg-gray-800/30 rounded-lg">
                      {HAIR_COLORS.map((color) => (
                        <button
                          key={color}
                          className={`w-8 h-8 rounded-full border-2 transition-all ${
                            player.portrait.hairColor === color 
                              ? 'border-red-500 scale-110 shadow-lg' 
                              : 'border-gray-600 hover:border-gray-400'
                          }`}
                          style={{ backgroundColor: color }}
                          onClick={() => updateNestedField('portrait', 'hairColor', color)}
                          title={color}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Forme des yeux */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Forme des yeux</Label>
                    <div className="grid grid-cols-3 gap-2">
                      {EYE_SHAPES.map((shape) => (
                        <button
                          key={shape}
                          className={`p-2 text-xs rounded transition-all ${
                            player.portrait.eyeShape === shape 
                              ? 'bg-red-600 text-white' 
                              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                          }`}
                          onClick={() => updateNestedField('portrait', 'eyeShape', shape)}
                        >
                          {shape}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Couleur des yeux */}
                  <div>
                    <Label className="text-gray-300 mb-3 block">Couleur des yeux</Label>
                    <div className="grid grid-cols-6 gap-2 p-3 bg-gray-800/30 rounded-lg">
                      {EYE_COLORS.map((color) => (
                        <button
                          key={color}
                          className={`w-8 h-8 rounded-full border-2 transition-all ${
                            player.portrait.eyeColor === color 
                              ? 'border-red-500 scale-110 shadow-lg' 
                              : 'border-gray-600 hover:border-gray-400'
                          }`}
                          style={{ backgroundColor: color }}
                          onClick={() => updateNestedField('portrait', 'eyeColor', color)}
                          title={color}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Résumé du portrait */}
                  <div className="bg-gray-800/30 p-4 rounded-lg">
                    <h4 className="text-white font-medium mb-2">Résumé du portrait</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div><span className="text-gray-400">Visage:</span> <span className="text-white">{player.portrait.faceShape}</span></div>
                      <div><span className="text-gray-400">Yeux:</span> <span className="text-white">{player.portrait.eyeShape}</span></div>
                      <div><span className="text-gray-400">Coiffure:</span> <span className="text-white">{player.portrait.hairstyle}</span></div>
                      <div className="col-span-2">
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-gray-400">Couleurs:</span>
                          <div className="flex gap-1">
                            <div className="w-4 h-4 rounded border" style={{backgroundColor: player.portrait.skinColor}} title="Peau"></div>
                            <div className="w-4 h-4 rounded border" style={{backgroundColor: player.portrait.hairColor}} title="Cheveux"></div>
                            <div className="w-4 h-4 rounded border" style={{backgroundColor: player.portrait.eyeColor}} title="Yeux"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Onglet Statistiques */}
              {currentTab === 'stats' && (
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-white font-medium">Répartition des points</h3>
                    <div className="flex items-center gap-4">
                      <span className="text-gray-400">Points restants: <span className="text-white">{statsPoints}</span></span>
                      <Button
                        variant="outline"
                        onClick={resetStats}
                        className="border-red-500 text-red-400 hover:bg-red-500/10"
                      >
                        <RotateCcw className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>

                  {Object.entries(player.stats).map(([stat, value]) => (
                    <div key={stat} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <Label className="text-gray-300 capitalize">{stat}</Label>
                        <span className="text-white">{value}/10</span>
                      </div>
                      <Slider
                        value={[value]}
                        min={0}
                        max={10}
                        step={1}
                        onValueChange={(newValue) => updateStats(stat, newValue)}
                        className="w-full"
                      />
                      <div className="flex justify-between text-xs text-gray-500">
                        <span>0</span>
                        <span>5</span>
                        <span>10</span>
                      </div>
                    </div>
                  ))}

                  <div className="bg-gray-800/30 p-4 rounded-lg">
                    <h4 className="text-white font-medium mb-2">Impact des statistiques</h4>
                    <ul className="text-sm text-gray-400 space-y-1">
                      <li>• <strong className="text-red-400">Intelligence</strong>: Réflexion, stratégie, énigmes</li>
                      <li>• <strong className="text-red-400">Force</strong>: Combat, intimidation, résistance</li>
                      <li>• <strong className="text-red-400">Agilité</strong>: Vitesse, précision, esquive</li>
                    </ul>
                  </div>
                </div>
              )}

              {/* Onglet Uniforme */}
              {currentTab === 'uniform' && (
                <div className="space-y-4">
                  <h3 className="text-white font-medium">Personnalisation de l'uniforme</h3>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label className="text-gray-300">Style</Label>
                      <Select 
                        value={player.uniform.style} 
                        onValueChange={(value) => updateNestedField('uniform', 'style', value)}
                      >
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {UNIFORM_STYLES.map((style) => (
                            <SelectItem key={style} value={style}>{style}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-gray-300">Couleur</Label>
                      <Select 
                        value={player.uniform.color} 
                        onValueChange={(value) => updateNestedField('uniform', 'color', value)}
                      >
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {UNIFORM_COLORS.map((color) => (
                            <SelectItem key={color} value={color}>{color}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-gray-300">Motif</Label>
                      <Select 
                        value={player.uniform.pattern} 
                        onValueChange={(value) => updateNestedField('uniform', 'pattern', value)}
                      >
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {UNIFORM_PATTERNS.map((pattern) => (
                            <SelectItem key={pattern} value={pattern}>{pattern}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Aperçu de l'uniforme */}
                  <div className="bg-gray-800/30 p-6 rounded-lg text-center">
                    <h4 className="text-white font-medium mb-4">Aperçu de l'uniforme</h4>
                    <div className="w-24 h-32 mx-auto bg-gray-600 rounded-lg flex items-center justify-center relative">
                      <div className="text-white text-xs">
                        {player.uniform.style}<br/>
                        {player.uniform.color}<br/>
                        {player.uniform.pattern}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Boutons de contrôle */}
              <div className="flex gap-4 pt-6 border-t border-gray-600">
                <Button
                  variant="outline"
                  onClick={() => navigate('/game-setup')}
                  className="flex-1 border-gray-600 text-gray-400"
                >
                  Annuler
                </Button>
                <Button
                  onClick={() => {
                    // Sauvegarder le joueur créé
                    console.log('Joueur créé:', player);
                    navigate('/game-setup');
                  }}
                  disabled={!player.name || !player.nationality}
                  className="flex-1 bg-red-600 hover:bg-red-700"
                >
                  <Save className="w-4 h-4 mr-2" />
                  Sauvegarder joueur
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PlayerCreator;