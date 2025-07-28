import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  ArrowLeft, 
  Palette, 
  ShoppingCart, 
  Lock, 
  Check,
  Star,
  Zap
} from 'lucide-react';
import { UNIFORM_STYLES, UNIFORM_COLORS, UNIFORM_PATTERNS } from '../mock/mockData';

const UniformCustomization = ({ gameState, updateGameState }) => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('colors');

  // Prix et conditions de déblocage
  const uniformPricing = {
    colors: {
      basic: { price: 50000, unlocked: true },
      premium: { price: 200000, unlocked: gameState.money >= 10000 },
      legendary: { price: 500000, unlocked: gameState.gameStats.totalKills >= 500 }
    },
    patterns: {
      basic: { price: 80000, unlocked: true },
      special: { price: 300000, unlocked: gameState.gameStats.totalGamesPlayed >= 10 },
      exclusive: { price: 1000000, unlocked: gameState.gameStats.totalKills >= 200 }
    },
    styles: {
      basic: { price: 120000, unlocked: true },
      designer: { price: 400000, unlocked: gameState.vipSalonLevel >= 3 }
    }
  };

  const uniformItems = {
    colors: {
      basic: [
        { name: 'Rouge Classique', color: '#DC2626', owned: true },
        { name: 'Vert Militaire', color: '#059669', owned: gameState.unlockedUniforms?.includes('green-military') },
        { name: 'Bleu Marine', color: '#1E40AF', owned: gameState.unlockedUniforms?.includes('blue-navy') },
        { name: 'Noir Profond', color: '#111827', owned: gameState.unlockedUniforms?.includes('black-deep') }
      ],
      premium: [
        { name: 'Or Impérial', color: '#F59E0B', owned: gameState.unlockedUniforms?.includes('gold-imperial') },
        { name: 'Violet Royal', color: '#7C3AED', owned: gameState.unlockedUniforms?.includes('purple-royal') },
        { name: 'Rose Néon', color: '#EC4899', owned: gameState.unlockedUniforms?.includes('pink-neon') },
        { name: 'Cyan Électrique', color: '#06B6D4', owned: gameState.unlockedUniforms?.includes('cyan-electric') }
      ],
      legendary: [
        { name: 'Sang de Dragon', color: '#7F1D1D', owned: gameState.unlockedUniforms?.includes('blood-dragon') },
        { name: 'Ombre Mortelle', color: '#000000', owned: gameState.unlockedUniforms?.includes('shadow-death') },
        { name: 'Feu Éternel', color: '#DC2626', owned: gameState.unlockedUniforms?.includes('eternal-fire'), special: true }
      ]
    },
    patterns: {
      basic: [
        { name: 'Uni', pattern: 'solid', owned: true },
        { name: 'Rayures Horizontales', pattern: 'stripes-h', owned: gameState.unlockedPatterns?.includes('stripes-h') },
        { name: 'Rayures Verticales', pattern: 'stripes-v', owned: gameState.unlockedPatterns?.includes('stripes-v') },
        { name: 'Carreaux', pattern: 'checkered', owned: gameState.unlockedPatterns?.includes('checkered') }
      ],
      special: [
        { name: 'Écailles de Serpent', pattern: 'snake-scales', owned: gameState.unlockedPatterns?.includes('snake-scales') },
        { name: 'Camouflage', pattern: 'camo', owned: gameState.unlockedPatterns?.includes('camo') },
        { name: 'Circuit Électronique', pattern: 'circuit', owned: gameState.unlockedPatterns?.includes('circuit') }
      ],
      exclusive: [
        { name: 'Motif du Maître', pattern: 'master-pattern', owned: gameState.unlockedPatterns?.includes('master-pattern'), 
          requirement: '200 éliminations', locked: gameState.gameStats.totalKills < 200 },
        { name: 'Essence du Zéro', pattern: 'zero-essence', owned: gameState.unlockedPatterns?.includes('zero-essence'),
          requirement: 'Voir Le Zéro apparaître', locked: !gameState.gameStats.hasSeenZero }
      ]
    }
  };

  const purchaseItem = (category, tier, item) => {
    const price = uniformPricing[category][tier].price;
    
    if (gameState.money >= price && !item.owned) {
      updateGameState({
        money: gameState.money - price,
        unlockedUniforms: category === 'colors' 
          ? [...(gameState.unlockedUniforms || []), item.name.toLowerCase().replace(' ', '-')]
          : gameState.unlockedUniforms,
        unlockedPatterns: category === 'patterns'
          ? [...(gameState.unlockedPatterns || []), item.pattern]
          : gameState.unlockedPatterns
      });
    }
  };

  const canPurchase = (category, tier, item) => {
    return uniformPricing[category][tier].unlocked && 
           gameState.money >= uniformPricing[category][tier].price && 
           !item.owned && 
           !item.locked;
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
              <h1 className="text-4xl font-black text-white">Uniformes</h1>
              <p className="text-gray-400">Personnalisez les tenues de vos joueurs</p>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-2xl font-bold text-green-400">${gameState.money.toLocaleString()}</div>
            <div className="text-sm text-gray-400">Budget disponible</div>
          </div>
        </div>

        <Tabs value={selectedCategory} onValueChange={setSelectedCategory} className="space-y-6">
          <TabsList className="bg-black/50 border border-red-500/30">
            <TabsTrigger value="colors" className="data-[state=active]:bg-red-600">
              <Palette className="w-4 h-4 mr-2" />
              Couleurs
            </TabsTrigger>
            <TabsTrigger value="patterns" className="data-[state=active]:bg-red-600">
              <div className="w-4 h-4 mr-2 bg-white rounded-sm"></div>
              Motifs
            </TabsTrigger>
            <TabsTrigger value="styles" className="data-[state=active]:bg-red-600">
              <Star className="w-4 h-4 mr-2" />
              Styles
            </TabsTrigger>
          </TabsList>

          {/* Couleurs */}
          <TabsContent value="colors" className="space-y-6">
            {Object.entries(uniformItems.colors).map(([tier, items]) => (
              <Card key={tier} className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span className="capitalize">{tier} Colors</span>
                    <div className="flex items-center gap-2">
                      <Badge 
                        variant="outline" 
                        className={`${
                          uniformPricing.colors[tier].unlocked 
                            ? 'text-green-400 border-green-400' 
                            : 'text-red-400 border-red-400'
                        }`}
                      >
                        ${uniformPricing.colors[tier].price}
                      </Badge>
                      {!uniformPricing.colors[tier].unlocked && (
                        <Lock className="w-4 h-4 text-red-400" />
                      )}
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {items.map((item) => (
                      <div
                        key={item.name}
                        className={`relative p-4 rounded-lg border transition-all ${
                          item.owned 
                            ? 'bg-green-900/20 border-green-500/30' 
                            : 'bg-gray-800/50 border-gray-600/30 hover:bg-gray-700/50'
                        }`}
                      >
                        <div className="text-center">
                          <div 
                            className="w-16 h-16 rounded-full mx-auto mb-3 border-2 border-gray-600"
                            style={{ backgroundColor: item.color }}
                          ></div>
                          <h3 className="text-white font-medium text-sm mb-2">{item.name}</h3>
                          
                          {item.owned ? (
                            <div className="flex items-center justify-center gap-1 text-green-400">
                              <Check className="w-4 h-4" />
                              <span className="text-xs">Possédé</span>
                            </div>
                          ) : (
                            <Button
                              onClick={() => purchaseItem('colors', tier, item)}
                              disabled={!canPurchase('colors', tier, item)}
                              className={`w-full text-xs ${
                                canPurchase('colors', tier, item)
                                  ? 'bg-red-600 hover:bg-red-700'
                                  : 'bg-gray-600 cursor-not-allowed'
                              }`}
                            >
                              <ShoppingCart className="w-3 h-3 mr-1" />
                              Acheter
                            </Button>
                          )}
                        </div>

                        {item.special && (
                          <div className="absolute -top-2 -right-2">
                            <Zap className="w-6 h-6 text-yellow-400 animate-pulse" />
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {!uniformPricing.colors[tier].unlocked && (
                    <div className="mt-4 p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
                      <div className="flex items-center gap-2 text-red-400 text-sm">
                        <Lock className="w-4 h-4" />
                        {tier === 'premium' && 'Débloquer en atteignant $10,000'}
                        {tier === 'legendary' && 'Débloquer avec 500 éliminations totales'}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Motifs */}
          <TabsContent value="patterns" className="space-y-6">
            {Object.entries(uniformItems.patterns).map(([tier, items]) => (
              <Card key={tier} className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span className="capitalize">{tier} Patterns</span>
                    <Badge 
                      variant="outline" 
                      className={`${
                        uniformPricing.patterns[tier].unlocked 
                          ? 'text-green-400 border-green-400' 
                          : 'text-red-400 border-red-400'
                      }`}
                    >
                      ${uniformPricing.patterns[tier].price}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {items.map((item) => (
                      <div
                        key={item.name}
                        className={`relative p-4 rounded-lg border transition-all ${
                          item.owned 
                            ? 'bg-green-900/20 border-green-500/30' 
                            : item.locked
                            ? 'bg-red-900/20 border-red-500/30 opacity-60'
                            : 'bg-gray-800/50 border-gray-600/30 hover:bg-gray-700/50'
                        }`}
                      >
                        <div className="text-center">
                          <div className="w-full h-16 bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                            <span className="text-gray-400 text-xs">{item.pattern}</span>
                          </div>
                          <h3 className="text-white font-medium text-sm mb-2">{item.name}</h3>
                          
                          {item.requirement && (
                            <div className="text-xs text-gray-400 mb-2">{item.requirement}</div>
                          )}
                          
                          {item.owned ? (
                            <div className="flex items-center justify-center gap-1 text-green-400">
                              <Check className="w-4 h-4" />
                              <span className="text-xs">Possédé</span>
                            </div>
                          ) : item.locked ? (
                            <div className="flex items-center justify-center gap-1 text-red-400">
                              <Lock className="w-4 h-4" />
                              <span className="text-xs">Verrouillé</span>
                            </div>
                          ) : (
                            <Button
                              onClick={() => purchaseItem('patterns', tier, item)}
                              disabled={!canPurchase('patterns', tier, item)}
                              className={`w-full text-xs ${
                                canPurchase('patterns', tier, item)
                                  ? 'bg-red-600 hover:bg-red-700'
                                  : 'bg-gray-600 cursor-not-allowed'
                              }`}
                            >
                              <ShoppingCart className="w-3 h-3 mr-1" />
                              Acheter
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  {!uniformPricing.patterns[tier].unlocked && (
                    <div className="mt-4 p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
                      <div className="flex items-center gap-2 text-red-400 text-sm">
                        <Lock className="w-4 h-4" />
                        {tier === 'special' && 'Débloquer en jouant 10 parties'}
                        {tier === 'exclusive' && 'Débloquer avec 200 éliminations'}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Styles */}
          <TabsContent value="styles" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white">Styles d'uniforme</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {UNIFORM_STYLES.map((style, index) => (
                    <div key={style} className="bg-gray-800/30 p-6 rounded-lg text-center">
                      <div className="w-20 h-24 bg-gray-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
                        <span className="text-white text-xs">{style}</span>
                      </div>
                      <h3 className="text-white font-medium mb-2">{style}</h3>
                      <div className="text-sm text-gray-400 mb-4">
                        {index === 0 && 'Style classique et intemporel'}
                        {index === 1 && 'Design contemporain et épuré'}
                        {index === 2 && 'Inspiration rétro chic'}
                        {index === 3 && 'Performance et confort'}
                        {index === 4 && 'Raffinement et prestige'}
                      </div>
                      <Badge variant="outline" className="text-green-400 border-green-400">
                        Gratuit
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Aperçu et combinaisons */}
        <Card className="bg-black/50 border-red-500/30 mt-8">
          <CardHeader>
            <CardTitle className="text-white">Aperçu des combinaisons</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {['Combinaison Classique', 'Look Moderne', 'Style Élite'].map((combo, index) => (
                <div key={combo} className="text-center">
                  <div className="w-24 h-32 bg-gray-700 rounded-lg mx-auto mb-3 flex items-center justify-center">
                    <span className="text-white text-sm">{combo}</span>
                  </div>
                  <h3 className="text-white font-medium">{combo}</h3>
                  <div className="text-sm text-gray-400">
                    {index === 0 && 'Rouge + Uni + Classic'}
                    {index === 1 && 'Noir + Circuit + Moderne'}
                    {index === 2 && 'Or + Écailles + Élégant'}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default UniformCustomization;