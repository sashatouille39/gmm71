import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { 
  ArrowLeft, 
  Settings as SettingsIcon, 
  Volume2, 
  Eye, 
  Gamepad2,
  Save,
  RotateCcw,
  Trash2,
  AlertTriangle,
  Download,
  Upload
} from 'lucide-react';

const Settings = ({ gameState, updateGameState }) => {
  const navigate = useNavigate();
  const [settings, setSettings] = useState({
    audio: {
      masterVolume: 80,
      effectsVolume: 90,
      musicVolume: 70,
      voiceVolume: 85,
      muteAll: false
    },
    graphics: {
      quality: 'high',
      fullscreen: false,
      vsync: true,
      showBlood: true,
      animationSpeed: 'normal'
    },
    gameplay: {
      autoSave: true,
      fastMode: false,
      spectatorDefault: false,
      showStats: true,
      pauseOnFocus: true
    },
    interface: {
      language: 'fr',
      theme: 'dark',
      fontSize: 'medium',
      showTooltips: true,
      compactMode: false
    }
  });

  const [showResetConfirm, setShowResetConfirm] = useState(false);

  const updateSetting = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: { ...prev[category], [key]: value }
    }));
  };

  const saveSettings = () => {
    // Sauvegarder les paramètres dans le localStorage
    localStorage.setItem('gamemaster-settings', JSON.stringify(settings));
    console.log('Paramètres sauvegardés');
  };

  const resetSettings = () => {
    setSettings({
      audio: {
        masterVolume: 80,
        effectsVolume: 90,
        musicVolume: 70,
        voiceVolume: 85,
        muteAll: false
      },
      graphics: {
        quality: 'high',
        fullscreen: false,
        vsync: true,
        showBlood: true,
        animationSpeed: 'normal'
      },
      gameplay: {
        autoSave: true,
        fastMode: false,
        spectatorDefault: false,
        showStats: true,
        pauseOnFocus: true
      },
      interface: {
        language: 'fr',
        theme: 'dark',
        fontSize: 'medium',
        showTooltips: true,
        compactMode: false
      }
    });
    setShowResetConfirm(false);
  };

  const resetGameData = () => {
    updateGameState({
      money: 50000,
      vipSalonLevel: 1,
      unlockedUniforms: [],
      unlockedPatterns: [],
      ownedCelebrities: [],
      gameStats: {
        totalGamesPlayed: 0,
        totalKills: 0,
        totalBetrayals: 0,
        favoriteCelebrity: null
      }
    });
    localStorage.removeItem('gamemaster-state');
  };

  const exportSave = () => {
    const saveData = {
      gameState,
      settings,
      exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(saveData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `gamemaster-save-${new Date().toLocaleDateString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const importSave = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const saveData = JSON.parse(e.target.result);
        if (saveData.gameState) {
          updateGameState(saveData.gameState);
        }
        if (saveData.settings) {
          setSettings(saveData.settings);
        }
        console.log('Sauvegarde importée avec succès');
      } catch (error) {
        console.error('Erreur lors de l\'importation:', error);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              className="text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Retour
            </Button>
            <div>
              <h1 className="text-4xl font-black text-white">Paramètres</h1>
              <p className="text-gray-400">Configuration et préférences du jeu</p>
            </div>
          </div>
        </div>

        <Tabs defaultValue="audio" className="space-y-6">
          <TabsList className="bg-black/50 border border-red-500/30 grid grid-cols-5 w-full">
            <TabsTrigger value="audio" className="data-[state=active]:bg-red-600">
              <Volume2 className="w-4 h-4 mr-2" />
              Audio
            </TabsTrigger>
            <TabsTrigger value="graphics" className="data-[state=active]:bg-red-600">
              <Eye className="w-4 h-4 mr-2" />
              Graphismes
            </TabsTrigger>
            <TabsTrigger value="gameplay" className="data-[state=active]:bg-red-600">
              <Gamepad2 className="w-4 h-4 mr-2" />
              Gameplay
            </TabsTrigger>
            <TabsTrigger value="interface" className="data-[state=active]:bg-red-600">
              <SettingsIcon className="w-4 h-4 mr-2" />
              Interface
            </TabsTrigger>
            <TabsTrigger value="data" className="data-[state=active]:bg-red-600">
              <Save className="w-4 h-4 mr-2" />
              Données
            </TabsTrigger>
          </TabsList>

          {/* Paramètres Audio */}
          <TabsContent value="audio" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Volume2 className="w-5 h-5" />
                  Paramètres Audio
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label className="text-gray-300">Volume principal</Label>
                      <span className="text-white">{settings.audio.masterVolume}%</span>
                    </div>
                    <Input
                      type="range"
                      min="0"
                      max="100"
                      value={settings.audio.masterVolume}
                      onChange={(e) => updateSetting('audio', 'masterVolume', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label className="text-gray-300">Effets sonores</Label>
                      <span className="text-white">{settings.audio.effectsVolume}%</span>
                    </div>
                    <Input
                      type="range"
                      min="0"
                      max="100"
                      value={settings.audio.effectsVolume}
                      onChange={(e) => updateSetting('audio', 'effectsVolume', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label className="text-gray-300">Musique</Label>
                      <span className="text-white">{settings.audio.musicVolume}%</span>
                    </div>
                    <Input
                      type="range"
                      min="0"
                      max="100"
                      value={settings.audio.musicVolume}
                      onChange={(e) => updateSetting('audio', 'musicVolume', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label className="text-gray-300">Voix</Label>
                      <span className="text-white">{settings.audio.voiceVolume}%</span>
                    </div>
                    <Input
                      type="range"
                      min="0"
                      max="100"
                      value={settings.audio.voiceVolume}
                      onChange={(e) => updateSetting('audio', 'voiceVolume', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg">
                  <div>
                    <Label className="text-gray-300">Couper tout le son</Label>
                    <p className="text-sm text-gray-400">Désactive complètement l'audio</p>
                  </div>
                  <Switch
                    checked={settings.audio.muteAll}
                    onCheckedChange={(checked) => updateSetting('audio', 'muteAll', checked)}
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Paramètres Graphismes */}
          <TabsContent value="graphics" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Eye className="w-5 h-5" />
                  Paramètres Graphiques
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label className="text-gray-300">Qualité graphique</Label>
                    <Select 
                      value={settings.graphics.quality} 
                      onValueChange={(value) => updateSetting('graphics', 'quality', value)}
                    >
                      <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">Faible</SelectItem>
                        <SelectItem value="medium">Moyen</SelectItem>
                        <SelectItem value="high">Élevé</SelectItem>
                        <SelectItem value="ultra">Ultra</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-gray-300">Vitesse d'animation</Label>
                    <Select 
                      value={settings.graphics.animationSpeed} 
                      onValueChange={(value) => updateSetting('graphics', 'animationSpeed', value)}
                    >
                      <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="slow">Lente</SelectItem>
                        <SelectItem value="normal">Normale</SelectItem>
                        <SelectItem value="fast">Rapide</SelectItem>
                        <SelectItem value="instant">Instantanée</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-4">
                  {[
                    { key: 'fullscreen', label: 'Mode plein écran', description: 'Affichage en plein écran' },
                    { key: 'vsync', label: 'Synchronisation verticale', description: 'Évite les déchirures d\'écran' },
                    { key: 'showBlood', label: 'Afficher le gore', description: 'Animations sanglantes et violentes' }
                  ].map((option) => (
                    <div key={option.key} className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg">
                      <div>
                        <Label className="text-gray-300">{option.label}</Label>
                        <p className="text-sm text-gray-400">{option.description}</p>
                      </div>
                      <Switch
                        checked={settings.graphics[option.key]}
                        onCheckedChange={(checked) => updateSetting('graphics', option.key, checked)}
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Paramètres Gameplay */}
          <TabsContent value="gameplay" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Gamepad2 className="w-5 h-5" />
                  Paramètres de Gameplay
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  { key: 'autoSave', label: 'Sauvegarde automatique', description: 'Sauvegarde automatique toutes les 5 minutes' },
                  { key: 'fastMode', label: 'Mode rapide', description: 'Animations plus rapides et moins de dialogues' },
                  { key: 'spectatorDefault', label: 'Mode spectateur par défaut', description: 'Démarre automatiquement en mode spectateur' },
                  { key: 'showStats', label: 'Afficher les statistiques', description: 'Montre les stats des joueurs en temps réel' },
                  { key: 'pauseOnFocus', label: 'Pause si focus perdu', description: 'Met le jeu en pause si la fenêtre perd le focus' }
                ].map((option) => (
                  <div key={option.key} className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg">
                    <div>
                      <Label className="text-gray-300">{option.label}</Label>
                      <p className="text-sm text-gray-400">{option.description}</p>
                    </div>
                    <Switch
                      checked={settings.gameplay[option.key]}
                      onCheckedChange={(checked) => updateSetting('gameplay', option.key, checked)}
                    />
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Paramètres Interface */}
          <TabsContent value="interface" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <SettingsIcon className="w-5 h-5" />
                  Paramètres Interface
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label className="text-gray-300">Langue</Label>
                    <Select 
                      value={settings.interface.language} 
                      onValueChange={(value) => updateSetting('interface', 'language', value)}
                    >
                      <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="fr">Français</SelectItem>
                        <SelectItem value="en">English</SelectItem>
                        <SelectItem value="es">Español</SelectItem>
                        <SelectItem value="de">Deutsch</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-gray-300">Thème</Label>
                    <Select 
                      value={settings.interface.theme} 
                      onValueChange={(value) => updateSetting('interface', 'theme', value)}
                    >
                      <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="dark">Sombre</SelectItem>
                        <SelectItem value="light">Clair</SelectItem>
                        <SelectItem value="auto">Automatique</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-gray-300">Taille du texte</Label>
                    <Select 
                      value={settings.interface.fontSize} 
                      onValueChange={(value) => updateSetting('interface', 'fontSize', value)}
                    >
                      <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="small">Petit</SelectItem>
                        <SelectItem value="medium">Moyen</SelectItem>
                        <SelectItem value="large">Grand</SelectItem>
                        <SelectItem value="xlarge">Très grand</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-4">
                  {[
                    { key: 'showTooltips', label: 'Afficher les infobulles', description: 'Aide contextuelle au survol' },
                    { key: 'compactMode', label: 'Mode compact', description: 'Interface plus dense avec moins d\'espacement' }
                  ].map((option) => (
                    <div key={option.key} className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg">
                      <div>
                        <Label className="text-gray-300">{option.label}</Label>
                        <p className="text-sm text-gray-400">{option.description}</p>
                      </div>
                      <Switch
                        checked={settings.interface[option.key]}
                        onCheckedChange={(checked) => updateSetting('interface', option.key, checked)}
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Gestion des données */}
          <TabsContent value="data" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Save className="w-5 h-5" />
                    Sauvegarde et restauration
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-4">
                    <Button
                      onClick={saveSettings}
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      <Save className="w-4 h-4 mr-2" />
                      Sauvegarder paramètres
                    </Button>
                    
                    <Button
                      onClick={() => setShowResetConfirm(true)}
                      variant="outline"
                      className="flex-1 border-yellow-500 text-yellow-400 hover:bg-yellow-500/10"
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Réinitialiser
                    </Button>
                  </div>

                  <div className="flex gap-4">
                    <Button
                      onClick={exportSave}
                      variant="outline"
                      className="flex-1 border-blue-500 text-blue-400 hover:bg-blue-500/10"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Exporter
                    </Button>
                    
                    <div className="flex-1">
                      <Input
                        type="file"
                        accept=".json"
                        onChange={importSave}
                        className="hidden"
                        id="import-save"
                      />
                      <Button
                        onClick={() => document.getElementById('import-save').click()}
                        variant="outline"
                        className="w-full border-blue-500 text-blue-400 hover:bg-blue-500/10"
                      >
                        <Upload className="w-4 h-4 mr-2" />
                        Importer
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Trash2 className="w-5 h-5" />
                    Gestion des données
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-gray-800/30 p-4 rounded-lg">
                    <h4 className="text-white font-medium mb-2">État actuel</h4>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Argent:</span>
                        <span className="text-green-400">${gameState.money.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Parties jouées:</span>
                        <span className="text-white">{gameState.gameStats.totalGamesPlayed}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Salon niveau:</span>
                        <span className="text-yellow-400">{gameState.vipSalonLevel}</span>
                      </div>
                    </div>
                  </div>

                  <Button
                    onClick={resetGameData}
                    variant="outline"
                    className="w-full border-red-500 text-red-400 hover:bg-red-500/10"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Réinitialiser progression
                  </Button>

                  <div className="text-xs text-gray-400">
                    ⚠️ Cette action supprimera définitivement toute votre progression
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Informations système */}
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white">Informations système</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-gray-400">Version</div>
                    <div className="text-white font-medium">Game Master Manager v1.0</div>
                  </div>
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-gray-400">Navigateur</div>
                    <div className="text-white font-medium">{navigator.userAgent.split(' ')[0]}</div>
                  </div>
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-gray-400">Résolution</div>
                    <div className="text-white font-medium">{window.screen.width}×{window.screen.height}</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Modal de confirmation de réinitialisation */}
        {showResetConfirm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="bg-gray-900 border-red-500/30 max-w-md w-full">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-400" />
                  Confirmer la réinitialisation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-gray-300">
                  Êtes-vous sûr de vouloir réinitialiser tous les paramètres ? 
                  Cette action ne peut pas être annulée.
                </p>
                <div className="flex gap-4">
                  <Button
                    onClick={() => setShowResetConfirm(false)}
                    variant="outline"
                    className="flex-1 border-gray-600 text-gray-400"
                  >
                    Annuler
                  </Button>
                  <Button
                    onClick={resetSettings}
                    className="flex-1 bg-red-600 hover:bg-red-700"
                  >
                    Réinitialiser
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;