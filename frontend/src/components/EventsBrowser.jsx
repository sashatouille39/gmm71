import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Search, 
  Filter, 
  Skull, 
  Zap, 
  Brain, 
  Dumbbell,
  Eye,
  ChevronDown,
  ChevronUp,
  PlayCircle,
  AlertTriangle
} from 'lucide-react';
import axios from 'axios';

const EventsBrowser = () => {
  const [events, setEvents] = useState([]);
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');
  const [expandedEvent, setExpandedEvent] = useState(null);
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchEvents();
    fetchStatistics();
  }, []);

  useEffect(() => {
    filterEvents();
  }, [events, searchTerm, filterType, filterDifficulty]);

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/games/events/available`);
      setEvents(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur lors de la récupération des épreuves:', error);
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/games/events/statistics`);
      setStatistics(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques:', error);
    }
  };

  const filterEvents = () => {
    let filtered = events;

    // Filtrer par recherche
    if (searchTerm) {
      filtered = filtered.filter(event =>
        event.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        event.decor.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filtrer par type
    if (filterType !== 'all') {
      filtered = filtered.filter(event => event.type === filterType);
    }

    // Filtrer par difficulté  
    if (filterDifficulty !== 'all') {
      const difficulty = parseInt(filterDifficulty);
      filtered = filtered.filter(event => event.difficulty === difficulty);
    }

    setFilteredEvents(filtered);
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'intelligence': return <Brain className="w-4 h-4" />;
      case 'force': return <Dumbbell className="w-4 h-4" />;
      case 'agilité': return <Zap className="w-4 h-4" />;
      default: return <Eye className="w-4 h-4" />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'intelligence': return 'bg-blue-600';
      case 'force': return 'bg-red-600';  
      case 'agilité': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  const getDifficultyColor = (difficulty) => {
    if (difficulty <= 3) return 'bg-green-600';
    if (difficulty <= 6) return 'bg-yellow-600';
    if (difficulty <= 8) return 'bg-orange-600';
    return 'bg-red-600';
  };

  const toggleEventDetails = (eventId) => {
    setExpandedEvent(expandedEvent === eventId ? null : eventId);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black flex items-center justify-center">
        <div className="text-white text-xl">Chargement des épreuves...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-black text-white mb-4 flex items-center gap-4">
            <Skull className="w-12 h-12 text-red-500" />
            ÉPREUVES MORTELLES
          </h1>
          <p className="text-gray-400 text-lg">
            Explorez les {events.length} épreuves avec décors uniques et animations gore
          </p>
        </div>

        {/* Statistiques */}
        {statistics && (
          <Card className="bg-black/50 border-red-500/30 mb-8">
            <CardHeader>
              <CardTitle className="text-white">Statistiques des épreuves</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-400">{statistics.total_events}</div>
                  <div className="text-gray-400">Total épreuves</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-400">{statistics.by_type?.intelligence || 0}</div>
                  <div className="text-gray-400">Intelligence</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-400">{statistics.by_type?.force || 0}</div>
                  <div className="text-gray-400">Force</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400">{statistics.by_type?.agilité || 0}</div>
                  <div className="text-gray-400">Agilité</div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Filtres */}
        <Card className="bg-black/50 border-red-500/30 mb-8">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Recherche */}
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Rechercher une épreuve..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white pl-10"
                />
              </div>

              {/* Filtre par type */}
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue placeholder="Type d'épreuve" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Tous les types</SelectItem>
                  <SelectItem value="intelligence">Intelligence</SelectItem>
                  <SelectItem value="force">Force</SelectItem>
                  <SelectItem value="agilité">Agilité</SelectItem>
                </SelectContent>
              </Select>

              {/* Filtre par difficulté */}
              <Select value={filterDifficulty} onValueChange={setFilterDifficulty}>
                <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                  <AlertTriangle className="w-4 h-4 mr-2" />
                  <SelectValue placeholder="Difficulté" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Toutes difficultés</SelectItem>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(diff => (
                    <SelectItem key={diff} value={diff.toString()}>
                      Niveau {diff}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* Compteur résultats */}
              <div className="flex items-center justify-center text-gray-400">
                {filteredEvents.length} / {events.length} épreuves
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Liste des épreuves */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredEvents.map((event) => (
            <Card 
              key={event.id} 
              className="bg-black/50 border-red-500/30 hover:border-red-400 transition-all duration-300"
            >
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge className={`${getTypeColor(event.type)} text-white`}>
                      {getTypeIcon(event.type)}
                      <span className="ml-1 capitalize">{event.type}</span>
                    </Badge>
                    <Badge className={`${getDifficultyColor(event.difficulty)} text-white`}>
                      Niveau {event.difficulty}
                    </Badge>
                  </div>
                  <div className="text-gray-400 text-sm">#{event.id}</div>
                </div>
                
                <CardTitle className="text-white text-lg font-bold">
                  {event.name}
                </CardTitle>
                
                <p className="text-gray-400 text-sm">
                  {event.description}
                </p>
              </CardHeader>

              <CardContent>
                {/* Décor */}
                <div className="mb-4">
                  <h4 className="text-white font-medium mb-2 flex items-center gap-2">
                    <Eye className="w-4 h-4" />
                    Décor
                  </h4>
                  <p className="text-gray-300 text-sm bg-gray-800/30 p-2 rounded italic">
                    "{event.decor}"
                  </p>
                </div>

                {/* Statistiques de l'épreuve */}
                <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                  <div>
                    <span className="text-gray-400">Élimination:</span>
                    <div className="text-red-400 font-bold">
                      {Math.round(event.elimination_rate * 100)}%
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-400">Durée:</span>
                    <div className="text-white">
                      {Math.round(event.survival_time_min / 60)}-{Math.round(event.survival_time_max / 60)}min
                    </div>
                  </div>
                </div>

                {/* Bouton pour voir détails */}
                <Button
                  variant="outline"
                  onClick={() => toggleEventDetails(event.id)}
                  className="w-full border-red-500 text-red-400 hover:bg-red-500/10"
                >
                  {expandedEvent === event.id ? (
                    <>
                      <ChevronUp className="w-4 h-4 mr-2" />
                      Masquer animations gore
                    </>
                  ) : (
                    <>
                      <ChevronDown className="w-4 h-4 mr-2" />
                      Voir animations gore ({event.death_animations?.length || 0})
                    </>
                  )}
                </Button>

                {/* Animations de mort */}
                {expandedEvent === event.id && (
                  <div className="mt-4 p-4 bg-red-900/20 rounded border border-red-500/30">
                    <h4 className="text-red-400 font-medium mb-3 flex items-center gap-2">
                      <Skull className="w-4 h-4" />
                      Animations de mort
                    </h4>
                    
                    {event.death_animations && event.death_animations.length > 0 ? (
                      <div className="space-y-2">
                        {event.death_animations.map((animation, index) => (
                          <div 
                            key={index}
                            className="flex items-start gap-2 text-sm text-gray-300 bg-black/30 p-2 rounded"
                          >
                            <PlayCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                            <span>{animation}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-400 text-sm">Aucune animation spécifique</p>
                    )}

                    {/* Mécaniques spéciales */}
                    {event.special_mechanics && event.special_mechanics.length > 0 && (
                      <div className="mt-4">
                        <h5 className="text-yellow-400 font-medium mb-2">Mécaniques spéciales:</h5>
                        <div className="flex flex-wrap gap-1">
                          {event.special_mechanics.map((mechanic, index) => (
                            <Badge key={index} variant="outline" className="text-yellow-400 border-yellow-400 text-xs">
                              {mechanic}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Message si aucun résultat */}
        {filteredEvents.length === 0 && (
          <div className="text-center py-12">
            <Skull className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl text-gray-400 mb-2">Aucune épreuve trouvée</h3>
            <p className="text-gray-500">Essayez de modifier vos filtres de recherche</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventsBrowser;