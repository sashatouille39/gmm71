import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { 
  ArrowLeft, 
  Trophy, 
  Skull, 
  Users, 
  Target,
  TrendingUp,
  Award,
  Clock,
  Zap,
  Crown,
  Star
} from 'lucide-react';

const Statistics = ({ gameState }) => {
  const navigate = useNavigate();
  const [selectedPeriod, setSelectedPeriod] = useState('all');
  const [celebrityStats, setCelebrityStats] = useState(null);
  const [detailedStats, setDetailedStats] = useState(null);
  const [roleStats, setRoleStats] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Charger toutes les statistiques depuis le backend
  useEffect(() => {
    const fetchAllStats = async () => {
      setIsLoading(true);
      try {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
        
        // Charger statistiques détaillées
        const detailedResponse = await fetch(`${backendUrl}/api/statistics/detailed`);
        if (detailedResponse.ok) {
          const detailed = await detailedResponse.json();
          setDetailedStats(detailed);
        }
        
        // Charger statistiques des rôles
        const roleResponse = await fetch(`${backendUrl}/api/statistics/roles`);
        if (roleResponse.ok) {
          const roles = await roleResponse.json();
          setRoleStats(roles);
        }
        
        // Charger statistiques des célébrités
        const celebrityResponse = await fetch(`${backendUrl}/api/celebrities/stats/summary`);
        if (celebrityResponse.ok) {
          const celebrity = await celebrityResponse.json();
          setCelebrityStats(celebrity);
        }
        
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
      }
      setIsLoading(false);
    };

    fetchAllStats();
  }, []);

  // Utiliser les données détaillées du backend ou fallback sur gameState
  const realGames = detailedStats?.completed_games || [];
  const realStats = {
    games: realGames,
    topEvents: detailedStats?.event_statistics || {},
    achievements: [
      { 
        name: 'Premier sang', 
        description: 'Organisez votre premier jeu', 
        completed: gameState.gameStats.totalGamesPlayed > 0,
        progress: gameState.gameStats.totalGamesPlayed 
      },
      { 
        name: 'Massacre', 
        description: '1000 éliminations totales', 
        completed: gameState.gameStats.totalKills >= 1000,
        progress: gameState.gameStats.totalKills 
      },
      { 
        name: 'Empereur', 
        description: 'Organisez 50 jeux', 
        completed: gameState.gameStats.totalGamesPlayed >= 50,
        progress: gameState.gameStats.totalGamesPlayed 
      },
      { 
        name: 'Millionaire', 
        description: 'Gagnez $1,000,000', 
        completed: gameState.totalEarnings >= 1000000,
        progress: gameState.totalEarnings || 0 
      },
      { 
        name: 'Le Zéro', 
        description: 'Voyez apparaître Le Zéro dans un jeu', 
        completed: gameState.gameStats.zeroAppearances > 0,
        progress: gameState.gameStats.zeroAppearances || 0 
      }
    ]
  };

  const totalEarnings = realGames.reduce((sum, game) => sum + (game.earnings || 0), 0);
  const totalPlayers = realGames.reduce((sum, game) => sum + (game.totalPlayers || 0), 0);
  const totalSurvivors = realGames.reduce((sum, game) => sum + (game.survivors || 0), 0);
  const survivalRate = totalPlayers > 0 ? (totalSurvivors / totalPlayers * 100).toFixed(1) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-7xl mx-auto">
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
              <h1 className="text-4xl font-black text-white">Statistiques</h1>
              <p className="text-gray-400">Analyse de vos performances en tant que Game Master</p>
            </div>
          </div>
        </div>

        {/* Statistiques globales */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-black/50 border-blue-500/30">
            <CardContent className="p-6 text-center">
              <Trophy className="w-8 h-8 text-blue-400 mx-auto mb-3" />
              <div className="text-3xl font-black text-white mb-1">{gameState.gameStats.totalGamesPlayed}</div>
              <div className="text-sm text-gray-400">Jeux organisés</div>
            </CardContent>
          </Card>

          <Card className="bg-black/50 border-red-500/30">
            <CardContent className="p-6 text-center">
              <Skull className="w-8 h-8 text-red-400 mx-auto mb-3" />
              <div className="text-3xl font-black text-white mb-1">{gameState.gameStats.totalKills.toLocaleString()}</div>
              <div className="text-sm text-gray-400">Éliminations totales</div>
            </CardContent>
          </Card>

          <Card className="bg-black/50 border-green-500/30">
            <CardContent className="p-6 text-center">
              <TrendingUp className="w-8 h-8 text-green-400 mx-auto mb-3" />
              <div className="text-3xl font-black text-white mb-1">${totalEarnings.toLocaleString()}</div>
              <div className="text-sm text-gray-400">Gains totaux</div>
            </CardContent>
          </Card>

          <Card className="bg-black/50 border-yellow-500/30">
            <CardContent className="p-6 text-center">
              <Users className="w-8 h-8 text-yellow-400 mx-auto mb-3" />
              <div className="text-3xl font-black text-white mb-1">{survivalRate}%</div>
              <div className="text-sm text-gray-400">Taux de survie moyen</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="games" className="space-y-6">
          <TabsList className="bg-black/50 border border-red-500/30">
            <TabsTrigger value="games" className="data-[state=active]:bg-red-600">
              <Trophy className="w-4 h-4 mr-2" />
              Historique des jeux
            </TabsTrigger>
            <TabsTrigger value="celebrities" className="data-[state=active]:bg-red-600">
              <Crown className="w-4 h-4 mr-2" />
              Célébrités
            </TabsTrigger>
            <TabsTrigger value="events" className="data-[state=active]:bg-red-600">
              <Target className="w-4 h-4 mr-2" />
              Épreuves
            </TabsTrigger>
            <TabsTrigger value="achievements" className="data-[state=active]:bg-red-600">
              <Award className="w-4 h-4 mr-2" />
              Succès
            </TabsTrigger>
            <TabsTrigger value="analytics" className="data-[state=active]:bg-red-600">
              <TrendingUp className="w-4 h-4 mr-2" />
              Analyses
            </TabsTrigger>
          </TabsList>

          {/* Historique des jeux */}
          <TabsContent value="games" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Trophy className="w-5 h-5" />
                  Derniers jeux organisés
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {realStats.games.length === 0 ? (
                    <div className="text-center py-12 text-gray-400">
                      <Trophy className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p>Aucune partie jouée</p>
                      <p className="text-sm">Lancez votre première partie pour voir les statistiques</p>
                    </div>
                  ) : (
                    realStats.games.map((game) => (
                      <div key={game.id} className="bg-gray-800/30 p-4 rounded-lg hover:bg-gray-700/30 transition-colors">
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <h3 className="text-white font-medium">Jeu #{game.id}</h3>
                            <p className="text-gray-400 text-sm">{game.date}</p>
                          </div>
                          <Badge variant="outline" className="text-green-400 border-green-400">
                            +${(game.earnings || 0).toLocaleString()}
                          </Badge>
                        </div>

                        <div className="grid grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-gray-400">Joueurs:</span>
                            <div className="text-white font-medium">{game.totalPlayers || 0}</div>
                          </div>
                          <div>
                            <span className="text-gray-400">Survivants:</span>
                            <div className="text-white font-medium">{game.survivors || 0}</div>
                          </div>
                          <div>
                            <span className="text-gray-400">Durée:</span>
                            <div className="text-white font-medium">{game.duration || 'N/A'}</div>
                          </div>
                          <div>
                            <span className="text-gray-400">Vainqueur:</span>
                            <div className="text-white font-medium text-xs">{game.winner || 'Aucun'}</div>
                          </div>
                        </div>

                        <div className="mt-3 bg-gray-700/50 rounded-full h-2">
                          <div 
                            className="bg-red-500 h-2 rounded-full"
                            style={{ 
                              width: `${game.totalPlayers > 0 ? ((game.totalPlayers - game.survivors) / game.totalPlayers) * 100 : 0}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          Taux d'élimination: {game.totalPlayers > 0 ? (((game.totalPlayers - game.survivors) / game.totalPlayers) * 100).toFixed(1) : 0}%
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Statistiques des célébrités */}
          <TabsContent value="celebrities" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-black/50 border-yellow-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Crown className="w-5 h-5 text-yellow-400" />
                    Statistiques générales
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {celebrityStats ? (
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-gray-800/30 p-3 rounded-lg text-center">
                          <div className="text-2xl font-bold text-yellow-400">{celebrityStats.total_celebrities}</div>
                          <div className="text-xs text-gray-400">Célébrités totales</div>
                        </div>
                        <div className="bg-gray-800/30 p-3 rounded-lg text-center">
                          <div className="text-2xl font-bold text-green-400">{celebrityStats.owned_celebrities}</div>
                          <div className="text-xs text-gray-400">Possédées</div>
                        </div>
                      </div>
                      <div className="bg-gray-800/30 p-3 rounded-lg text-center">
                        <div className="text-2xl font-bold text-orange-400">{celebrityStats.total_wins}</div>
                        <div className="text-xs text-gray-400">Victoires totales</div>
                      </div>
                      <div className="bg-gray-800/30 p-3 rounded-lg text-center">
                        <div className="text-lg font-bold text-blue-400">{celebrityStats.average_wins.toFixed(2)}</div>
                        <div className="text-xs text-gray-400">Victoires moyennes</div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <Crown className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p>Chargement des données...</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-yellow-500/30">
                <CardHeader>
                  <CardTitle className="text-white">Répartition par catégorie</CardTitle>
                </CardHeader>
                <CardContent>
                  {celebrityStats && celebrityStats.by_category ? (
                    <div className="space-y-3">
                      {Object.entries(celebrityStats.by_category).map(([category, count]) => (
                        <div key={category} className="flex justify-between items-center p-2 bg-gray-800/20 rounded">
                          <span className="text-gray-300 capitalize">{category}</span>
                          <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                            {count}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <p>Aucune donnée de catégorie</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-yellow-500/30 lg:col-span-2">
                <CardHeader>
                  <CardTitle className="text-white">Répartition par niveau d'étoiles</CardTitle>
                </CardHeader>
                <CardContent>
                  {celebrityStats && celebrityStats.by_stars ? (
                    <div className="grid grid-cols-4 gap-4">
                      {Object.entries(celebrityStats.by_stars).map(([stars, count]) => (
                        <div key={stars} className="bg-gray-800/30 p-4 rounded-lg text-center">
                          <div className="flex justify-center mb-2">
                            {[...Array(parseInt(stars))].map((_, i) => (
                              <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                            ))}
                          </div>
                          <div className="text-xl font-bold text-white">{count}</div>
                          <div className="text-xs text-gray-400">{stars} étoiles</div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <p>Aucune donnée d'étoiles</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Statistiques des épreuves */}
          <TabsContent value="events" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Skull className="w-5 h-5" />
                    Épreuves les plus mortelles
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {realStats.topEvents.length === 0 ? (
                      <div className="text-center py-8 text-gray-400">
                        <Target className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p>Aucune donnée d'épreuve</p>
                      </div>
                    ) : (
                      realStats.topEvents.map((event, index) => (
                        <div key={event.name} className="flex items-center justify-between p-3 bg-gray-800/30 rounded-lg">
                          <div className="flex items-center gap-3">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                              index === 0 ? 'bg-red-600' : index === 1 ? 'bg-red-500' : 'bg-red-400'
                            }`}>
                              {index + 1}
                            </div>
                            <div>
                              <div className="text-white font-medium">{event.name}</div>
                              <div className="text-gray-400 text-sm">
                                Taux de survie: {((event.survival_rate || 0) * 100).toFixed(1)}%
                              </div>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-red-400 font-bold">{event.deaths || 0}</div>
                            <div className="text-gray-400 text-xs">morts</div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white">Performances par type</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {['Intelligence', 'Force', 'Agilité'].map((type) => (
                      <div key={type} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-300">{type}</span>
                          <span className="text-white">{Math.floor(Math.random() * 30 + 60)}%</span>
                        </div>
                        <div className="bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-red-500 h-2 rounded-full transition-all duration-1000"
                            style={{ width: `${Math.floor(Math.random() * 30 + 60)}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Succès */}
          <TabsContent value="achievements" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Award className="w-5 h-5" />
                  Succès et accomplissements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {realStats.achievements.map((achievement) => (
                    <div 
                      key={achievement.name}
                      className={`p-4 rounded-lg border transition-all ${
                        achievement.completed 
                          ? 'bg-green-900/20 border-green-500/30' 
                          : 'bg-gray-800/30 border-gray-600/30'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h3 className={`font-medium ${
                          achievement.completed ? 'text-green-400' : 'text-white'
                        }`}>
                          {achievement.name}
                        </h3>
                        {achievement.completed && (
                          <Trophy className="w-5 h-5 text-yellow-400" />
                        )}
                      </div>
                      <p className="text-gray-400 text-sm mb-3">{achievement.description}</p>
                      
                      {!achievement.completed && achievement.progress !== undefined && (
                        <div className="space-y-1">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Progression</span>
                            <span className="text-white">{achievement.progress}</span>
                          </div>
                          <div className="bg-gray-700 rounded-full h-1.5">
                            <div 
                              className="bg-red-500 h-1.5 rounded-full"
                              style={{ 
                                width: `${Math.min(100, (achievement.progress / (achievement.name === 'Empereur' ? 50 : achievement.name === 'Millionaire' ? 1000000 : 1000)) * 100)}%` 
                              }}
                            ></div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analyses */}
          <TabsContent value="analytics" className="space-y-6">
            {isLoading ? (
              <div className="text-center py-12 text-gray-400">
                <div className="w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p>Chargement des analyses...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-black/50 border-red-500/30">
                  <CardHeader>
                    <CardTitle className="text-white">Tendances temporelles</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-64 bg-gray-800/30 rounded-lg p-4">
                      {realGames.length > 0 ? (
                        <div className="space-y-3">
                          <div className="text-sm text-gray-400 mb-4">Évolution des gains par partie</div>
                          {realGames.slice(-10).map((game, index) => (
                            <div key={game.id} className="flex justify-between items-center">
                              <span className="text-xs text-gray-400">Partie #{game.id.slice(-4)}</span>
                              <div className="flex items-center gap-2">
                                <div 
                                  className="bg-red-500 h-2 rounded"
                                  style={{ 
                                    width: `${Math.max(10, (game.earnings / 50000) * 100)}px` 
                                  }}
                                ></div>
                                <span className="text-xs text-green-400">${game.earnings.toLocaleString()}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-center text-gray-400 h-full flex items-center justify-center flex-col">
                          <TrendingUp className="w-12 h-12 mx-auto mb-2 opacity-50" />
                          <p>Aucune donnée disponible</p>
                          <p className="text-xs">Jouez des parties pour voir les tendances</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-black/50 border-red-500/30">
                  <CardHeader>
                    <CardTitle className="text-white">Analyses des rôles</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {roleStats.length > 0 ? (
                      <div className="space-y-4">
                        {roleStats.map((roleData) => {
                          const roleDisplayNames = {
                            'normal': 'Normal',
                            'sportif': 'Sportif',
                            'intelligent': 'L\'Intelligent',
                            'brute': 'La Brute',
                            'peureux': 'Peureux',
                            'zero': 'Le Zéro'
                          };
                          
                          const roleColors = {
                            'normal': 'text-white',
                            'sportif': 'text-green-400',
                            'intelligent': 'text-blue-400',
                            'brute': 'text-red-400',
                            'peureux': 'text-gray-400',
                            'zero': 'text-purple-400'
                          };
                          
                          const displayName = roleDisplayNames[roleData.role] || roleData.role;
                          const color = roleColors[roleData.role] || 'text-white';
                          
                          return (
                            <div key={roleData.role} className="flex justify-between items-center p-2 bg-gray-800/20 rounded">
                              <div>
                                <span className={`font-medium ${color}`}>{displayName}</span>
                                <div className="text-xs text-gray-400">{roleData.appearances} apparitions</div>
                              </div>
                              <div className="text-right">
                                <div className={color}>{roleData.survival_rate}%</div>
                                <div className="text-xs text-gray-400">survie</div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <div className="text-center py-8 text-gray-400">
                        <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p>Aucune donnée de rôle disponible</p>
                        <p className="text-xs">Terminez des parties pour voir les statistiques</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Statistics;