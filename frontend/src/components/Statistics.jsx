import React, { useState } from 'react';
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
  Zap
} from 'lucide-react';

const Statistics = ({ gameState }) => {
  const navigate = useNavigate();
  const [selectedPeriod, setSelectedPeriod] = useState('all');

  // Utiliser les vraies données de jeu au lieu des données mockées
  const realGames = gameState.completedGames || [];
  const realStats = {
    games: realGames,
    topEvents: gameState.eventStats || [],
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
                  {mockStats.games.map((game) => (
                    <div key={game.id} className="bg-gray-800/30 p-4 rounded-lg hover:bg-gray-700/30 transition-colors">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="text-white font-medium">Jeu #{game.id}</h3>
                          <p className="text-gray-400 text-sm">{game.date}</p>
                        </div>
                        <Badge variant="outline" className="text-green-400 border-green-400">
                          +${game.earnings.toLocaleString()}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-400">Joueurs:</span>
                          <div className="text-white font-medium">{game.players}</div>
                        </div>
                        <div>
                          <span className="text-gray-400">Survivants:</span>
                          <div className="text-white font-medium">{game.survivors}</div>
                        </div>
                        <div>
                          <span className="text-gray-400">Durée:</span>
                          <div className="text-white font-medium">{game.duration}</div>
                        </div>
                        <div>
                          <span className="text-gray-400">Vainqueur:</span>
                          <div className="text-white font-medium text-xs">{game.winner}</div>
                        </div>
                      </div>

                      <div className="mt-3 bg-gray-700/50 rounded-full h-2">
                        <div 
                          className="bg-red-500 h-2 rounded-full"
                          style={{ width: `${((game.players - game.survivors) / game.players) * 100}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        Taux d'élimination: {(((game.players - game.survivors) / game.players) * 100).toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
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
                    {mockStats.topEvents.map((event, index) => (
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
                              Taux de survie: {(event.survival_rate * 100).toFixed(1)}%
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-red-400 font-bold">{event.deaths}</div>
                          <div className="text-gray-400 text-xs">morts</div>
                        </div>
                      </div>
                    ))}
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
                  {mockStats.achievements.map((achievement) => (
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
                                width: `${Math.min(100, (achievement.progress / (achievement.name === 'Empereur' ? 50 : 1000000)) * 100)}%` 
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
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white">Tendances temporelles</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 bg-gray-800/30 rounded-lg flex items-center justify-center">
                    <div className="text-center text-gray-400">
                      <TrendingUp className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p>Graphique des performances</p>
                      <p className="text-xs">(Données en temps réel)</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-red-500/30">
                <CardHeader>
                  <CardTitle className="text-white">Analyses des rôles</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries({
                      'Le Zéro': { appearances: 2, survival: 100, color: 'text-purple-400' },
                      'L\'Intelligent': { appearances: 47, survival: 72, color: 'text-blue-400' },
                      'Sportif': { appearances: 89, survival: 45, color: 'text-green-400' },
                      'La Brute': { appearances: 92, survival: 38, color: 'text-red-400' },
                      'Peureux': { appearances: 78, survival: 12, color: 'text-gray-400' },
                      'Normal': { appearances: 534, survival: 28, color: 'text-white' }
                    }).map(([role, stats]) => (
                      <div key={role} className="flex justify-between items-center p-2 bg-gray-800/20 rounded">
                        <div>
                          <span className={`font-medium ${stats.color}`}>{role}</span>
                          <div className="text-xs text-gray-400">{stats.appearances} apparitions</div>
                        </div>
                        <div className="text-right">
                          <div className={stats.color}>{stats.survival}%</div>
                          <div className="text-xs text-gray-400">survie</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Statistics;