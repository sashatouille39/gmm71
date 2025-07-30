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
  DollarSign,
  RefreshCw
} from 'lucide-react';

const MainMenu = ({ gameState, hasActiveGame, onRefreshGameState }) => {
  const navigate = useNavigate();
  const [hoveredCard, setHoveredCard] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefreshGameState = async () => {
    if (!onRefreshGameState || isRefreshing) return;
    
    setIsRefreshing(true);
    try {
      await onRefreshGameState();
      
      // Afficher notification de synchronisation
      const notification = document.createElement('div');
      notification.innerHTML = `
        <div class="fixed top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 flex items-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          <span>Solde synchronisé</span>
        </div>
      `;
      document.body.appendChild(notification.firstElementChild);
      
      setTimeout(() => {
        const notif = document.querySelector('.fixed.top-4.right-4');
        if (notif) notif.remove();
      }, 3000);
      
    } catch (error) {
      console.error('Erreur lors de la synchronisation:', error);
    }
    setIsRefreshing(false);
  };

  const menuItems = [
    {
      id: 'play',
      title: 'Jouer',
      description: 'Créer une nouvelle partie',
      icon: Play,
      path: '/game-setup',
      color: 'from-red-600 to-red-800',
      badge: null // Supprimer le badge "Partie en cours" problématique
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
            <div className="flex items-center justify-between mb-2">
              <DollarSign className="w-6 h-6 text-green-400" />
              <Button
                variant="ghost"
                size="sm"
                onClick={handleRefreshGameState}
                disabled={isRefreshing}
                className="h-6 w-6 p-0 text-green-400 hover:text-green-300"
                title="Synchroniser le solde"
              >
                <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              </Button>
            </div>
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