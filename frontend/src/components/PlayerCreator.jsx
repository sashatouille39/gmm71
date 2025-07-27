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
import { ArrowLeft, Save, Eye, RotateCcw } from 'lucide-react';
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
      eyeColor: '#8B4513',
      eyeShape: 'Amande'
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
      eyeColor: ['#8B4513', '#654321', '#2F4F2F', '#483D8B'][Math.floor(Math.random() * 4)],
      eyeShape: ['Amande', 'Rond', 'Allongé', 'Tombant'][Math.floor(Math.random() * 4)]
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
              {/* Avatar stylisé */}
              <div className="relative mx-auto w-32 h-32 rounded-full border-4 border-red-500 overflow-hidden">
                <div 
                  className="w-full h-full flex items-center justify-center text-4xl font-bold"
                  style={{ backgroundColor: player.portrait.skinColor }}
                >
                  {player.name ? player.name.charAt(0).toUpperCase() : '?'}
                </div>
                <div className="absolute bottom-0 w-full h-8 opacity-80"
                  style={{ backgroundColor: player.portrait.hairColor }}>
                </div>
              </div>

              {/* Informations du joueur */}
              <div className="space-y-2">
                <h3 className="text-xl font-bold text-white">
                  {player.name || 'Sans nom'}
                </h3>
                <div className="flex justify-center gap-2">
                  <Badge variant="outline" className="text-gray-300">
                    {player.nationality || 'Aucune'}
                  </Badge>
                  <Badge variant="outline" className="text-gray-300">
                    {player.gender === 'M' ? 'Homme' : 'Femme'}
                  </Badge>
                </div>
                <Badge 
                  variant="outline" 
                  className="text-red-400 border-red-400"
                >
                  {PLAYER_ROLES[player.role].name}
                </Badge>
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
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h3 className="text-white font-medium">Personnalisation du visage</h3>
                    <Button
                      variant="outline"
                      onClick={randomizePortrait}
                      className="border-red-500 text-red-400 hover:bg-red-500/10"
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Aléatoire
                    </Button>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="text-gray-300">Forme du visage</Label>
                      <Select 
                        value={player.portrait.faceShape} 
                        onValueChange={(value) => updateNestedField('portrait', 'faceShape', value)}
                      >
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="max-h-40">
                          {FACE_SHAPES.map((shape) => (
                            <SelectItem key={shape} value={shape}>{shape}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-gray-300">Coiffure</Label>
                      <Select 
                        value={player.portrait.hairstyle} 
                        onValueChange={(value) => updateNestedField('portrait', 'hairstyle', value)}
                      >
                        <SelectTrigger className="bg-gray-800 border-gray-600 text-white mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="max-h-40">
                          {HAIRSTYLES.slice(0, 30).map((style) => (
                            <SelectItem key={style} value={style}>{style}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label className="text-gray-300 mb-3 block">Couleur de peau</Label>
                    <div className="grid grid-cols-8 gap-2">
                      {SKIN_COLORS.slice(0, 16).map((color) => (
                        <button
                          key={color}
                          className={`w-8 h-8 rounded-full border-2 ${
                            player.portrait.skinColor === color 
                              ? 'border-red-500 scale-110' 
                              : 'border-gray-600'
                          } transition-all`}
                          style={{ backgroundColor: color }}
                          onClick={() => updateNestedField('portrait', 'skinColor', color)}
                        />
                      ))}
                    </div>
                  </div>

                  <div>
                    <Label className="text-gray-300 mb-3 block">Couleur des cheveux</Label>
                    <div className="grid grid-cols-8 gap-2">
                      {HAIR_COLORS.slice(0, 16).map((color) => (
                        <button
                          key={color}
                          className={`w-8 h-8 rounded-full border-2 ${
                            player.portrait.hairColor === color 
                              ? 'border-red-500 scale-110' 
                              : 'border-gray-600'
                          } transition-all`}
                          style={{ backgroundColor: color }}
                          onClick={() => updateNestedField('portrait', 'hairColor', color)}
                        />
                      ))}
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