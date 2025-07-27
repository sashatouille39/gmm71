import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Play, 
  BarChart3, 
  Palette, 
  Crown, 
  Settings, 
  LogOut,
  Users,
  Skull,
  DollarSign
} from 'lucide-react';

const MainMenu = ({ gameState, hasActiveGame }) => {
  const navigate = useNavigate();
  const [hoveredCard, setHoveredCard] = useState(null);

  const menuItems = [
    {
      id: 'play',
      title: 'Jouer',
      description: 'Créer une nouvelle partie ou reprendre',
      icon: Play,
      path: '/game-setup',
      color: 'from-red-600 to-red-800',
      badge: hasActiveGame ? 'Partie en cours' : null
    },
    {
      id: 'stats',
      title: 'Statistiques',
      description: 'Voir les performances et records',
      icon: BarChart3,
      path: '/statistics',
      color: 'from-blue-600 to-blue-800'
    },
    {
      id: 'uniforms',
      title: 'Uniformes',
      description: 'Personnaliser couleurs et motifs',
      icon: Palette,
      path: '/uniform-customization',
      color: 'from-purple-600 to-purple-800'
    },
    {
      id: 'vip',
      title: 'Salon VIP',
      description: 'Gérer les VIP et célébrités',
      icon: Crown,
      path: '/vip-salon',
      color: 'from-yellow-600 to-yellow-800',
      badge: `Niveau ${gameState.vipSalonLevel}`
    },
    {
      id: 'settings',
      title: 'Paramètres',
      description: 'Configuration et options',
      icon: Settings,
      path: '/settings',
      color: 'from-gray-600 to-gray-800'
    }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 relative overflow-hidden">
      {/* Arrière-plan animé */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-32 h-32 border border-red-500 rotate-45 animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-24 h-24 border border-red-500 rotate-12 animate-bounce"></div>
        <div className="absolute top-1/2 left-1/4 w-16 h-16 bg-red-500 opacity-20 rotate-45 animate-spin"></div>
      </div>

      {/* Logo et titre */}
      <div className="text-center mb-12 z-10">
        <div className="mb-6 relative">
          <div className="absolute inset-0 blur-xl bg-red-500 opacity-20 rounded-full"></div>
          <Skull className="w-24 h-24 text-red-500 mx-auto relative z-10 animate-pulse" />
        </div>
        
        <h1 className="text-6xl font-black text-white mb-4 tracking-tight">
          GAME MASTER
          <span className="block text-red-500 text-4xl font-light tracking-widest">MANAGER</span>
        </h1>
        
        <p className="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">
          Gérez votre propre version personnalisée de Squid Game. 
          Créez des joueurs, organisez des épreuves mortelles et regardez le spectacle se dérouler.
        </p>
      </div>

      {/* Statistiques rapides */}
      <div className="flex gap-6 mb-12 z-10">
        <Card className="bg-black/50 border-red-500/30 backdrop-blur-sm">
          <CardContent className="p-4 text-center">
            <DollarSign className="w-6 h-6 text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">${gameState.money.toLocaleString()}</div>
            <div className="text-sm text-gray-400">Budget</div>
          </CardContent>
        </Card>
        
        <Card className="bg-black/50 border-red-500/30 backdrop-blur-sm">
          <CardContent className="p-4 text-center">
            <Users className="w-6 h-6 text-blue-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">{gameState.gameStats.totalGamesPlayed}</div>
            <div className="text-sm text-gray-400">Parties jouées</div>
          </CardContent>
        </Card>
        
        <Card className="bg-black/50 border-red-500/30 backdrop-blur-sm">
          <CardContent className="p-4 text-center">
            <Skull className="w-6 h-6 text-red-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">{gameState.gameStats.totalKills}</div>
            <div className="text-sm text-gray-400">Éliminations</div>
          </CardContent>
        </Card>
      </div>

      {/* Menu principal */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl w-full z-10">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isHovered = hoveredCard === item.id;
          
          return (
            <Card 
              key={item.id}
              className={`
                relative overflow-hidden cursor-pointer transition-all duration-500
                ${isHovered ? 'scale-105 shadow-2xl shadow-red-500/20' : 'scale-100'}
                bg-gradient-to-br ${item.color} border-0
                hover:shadow-2xl hover:shadow-red-500/30
              `}
              onMouseEnter={() => setHoveredCard(item.id)}
              onMouseLeave={() => setHoveredCard(null)}
              onClick={() => navigate(item.path)}
            >
              {/* Effet de brillance */}
              <div className={`
                absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent
                transition-transform duration-700 ${isHovered ? 'translate-x-full' : '-translate-x-full'}
              `} />
              
              <CardContent className="p-8 text-white relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <Icon className={`w-12 h-12 transition-transform duration-300 ${isHovered ? 'scale-110 rotate-6' : ''}`} />
                  {item.badge && (
                    <Badge variant="secondary" className="bg-white/20 text-white border-0">
                      {item.badge}
                    </Badge>
                  )}
                </div>
                
                <h3 className="text-2xl font-bold mb-3 tracking-wide">{item.title}</h3>
                <p className="text-white/80 leading-relaxed">{item.description}</p>
                
                {/* Animation de particules */}
                {isHovered && (
                  <div className="absolute inset-0 pointer-events-none">
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className="absolute w-1 h-1 bg-white rounded-full animate-ping"
                        style={{
                          left: `${20 + i * 15}%`,
                          top: `${30 + i * 10}%`,
                          animationDelay: `${i * 0.2}s`
                        }}
                      />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Bouton quitter */}
      <Button
        variant="ghost"
        className="mt-12 text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-all duration-300"
        onClick={() => window.close()}
      >
        <LogOut className="w-5 h-5 mr-2" />
        Quitter le jeu
      </Button>

      {/* Footer */}
      <div className="absolute bottom-4 text-center text-gray-600 text-sm">
        <p>Game Master Manager v1.0 - Développé pour les vrais Game Masters</p>
      </div>
    </div>
  );
};

export default MainMenu;