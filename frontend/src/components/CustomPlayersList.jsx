import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { 
  Edit2, 
  Trash2, 
  Copy, 
  Search, 
  Users, 
  Plus,
  Eye,
  Filter
} from 'lucide-react';
import { useCustomPlayers } from '../hooks/useCustomPlayers';
import { PLAYER_ROLES } from '../mock/mockData';

const CustomPlayersList = ({ onSelectPlayer, onCreateNew, selectedPlayers = [] }) => {
  const { customPlayers, removePlayer, duplicatePlayer } = useCustomPlayers();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  const [showDetails, setShowDetails] = useState({});

  // Filtrer les joueurs
  const filteredPlayers = customPlayers.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         player.nationality.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = filterRole === 'all' || player.role === filterRole;
    const result = matchesSearch && matchesRole;
    
    console.log('🔍 DEBUG Filter player:', {
      player: player.name,
      searchTerm,
      filterRole,
      matchesSearch,
      matchesRole,
      result
    });
    
    return result;
  });

  console.log('🔍 DEBUG filteredPlayers:', filteredPlayers);

  const handleDelete = (playerId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce joueur ?')) {
      removePlayer(playerId);
    }
  };

  const handleDuplicate = (playerId) => {
    const duplicated = duplicatePlayer(playerId);
    if (duplicated) {
      console.log('Joueur dupliqué:', duplicated);
    }
  };

  const toggleDetails = (playerId) => {
    setShowDetails(prev => ({
      ...prev,
      [playerId]: !prev[playerId]
    }));
  };

  const isSelected = (playerId) => {
    return selectedPlayers.some(p => p.id === playerId);
  };

  return (
    <Card className="bg-black/50 border-red-500/30">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Users className="w-5 h-5" />
          Joueurs personnalisés ({customPlayers.length})
        </CardTitle>
        
        {/* Filtres et recherche */}
        <div className="flex gap-4 items-center">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Rechercher par nom ou nationalité..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-800 border-gray-600 text-white pl-10"
            />
          </div>
          
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-400" />
            <select
              value={filterRole}
              onChange={(e) => setFilterRole(e.target.value)}
              className="bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white text-sm"
            >
              <option value="all">Tous les rôles</option>
              {Object.entries(PLAYER_ROLES).map(([role, data]) => (
                <option key={role} value={role}>{data.name}</option>
              ))}
            </select>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Bouton créer nouveau */}
        <Button
          onClick={onCreateNew}
          className="w-full bg-red-600 hover:bg-red-700"
        >
          <Plus className="w-4 h-4 mr-2" />
          Créer un nouveau joueur
        </Button>

        {/* Liste des joueurs */}
        <div className="bg-yellow-500/10 border border-yellow-500 p-4 rounded mb-4">
          <p className="text-yellow-400 font-bold">DEBUG: customPlayers.length = {customPlayers.length}</p>
          <p className="text-yellow-400">DEBUG: filteredPlayers.length = {filteredPlayers.length}</p>
          <p className="text-yellow-400">DEBUG: searchTerm = "{searchTerm}"</p>
          <p className="text-yellow-400">DEBUG: filterRole = "{filterRole}"</p>
        </div>
        
        {filteredPlayers.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            {customPlayers.length === 0 ? (
              <>
                <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Aucun joueur personnalisé créé</p>
                <p className="text-sm">Cliquez sur "Créer un nouveau joueur" pour commencer</p>
              </>
            ) : (
              <p>Aucun joueur ne correspond aux filtres</p>
            )}
          </div>
        ) : (
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredPlayers.map((player) => (
              <div key={player.id} className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {/* Avatar miniature */}
                      <div 
                        className="w-10 h-10 rounded-full border-2 border-red-500 relative overflow-hidden"
                        style={{ backgroundColor: player.portrait.skinColor }}
                      >
                        <div className="w-full h-6 absolute top-0" 
                             style={{ backgroundColor: player.portrait.hairColor, opacity: 0.8 }}></div>
                        <div className="absolute inset-0 flex items-center justify-center text-xs font-bold text-black">
                          {player.name.charAt(0).toUpperCase()}
                        </div>
                      </div>
                      
                      <div className="flex-1">
                        <h4 className="text-white font-medium">{player.name}</h4>
                        <div className="flex gap-2 mt-1">
                          <Badge variant="outline" className="text-xs text-gray-300">
                            {player.nationality}
                          </Badge>
                          <Badge variant="outline" className="text-xs text-red-400 border-red-400">
                            {PLAYER_ROLES[player.role].name}
                          </Badge>
                          {isSelected(player.id) && (
                            <Badge className="text-xs bg-green-600">
                              Sélectionné
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Statistiques rapides */}
                    <div className="flex gap-4 text-xs text-gray-400">
                      <span>Int: {player.stats.intelligence}</span>
                      <span>For: {player.stats.force}</span>
                      <span>Agi: {player.stats.agilité}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleDetails(player.id)}
                      className="text-gray-400 hover:text-white"
                    >
                      <Eye className="w-4 h-4" />
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onSelectPlayer(player)}
                      className="text-blue-400 hover:text-blue-300"
                      disabled={isSelected(player.id)}
                    >
                      {isSelected(player.id) ? 'Sélectionné' : 'Sélectionner'}
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDuplicate(player.id)}
                      className="text-green-400 hover:text-green-300"
                    >
                      <Copy className="w-4 h-4" />
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(player.id)}
                      className="text-red-400 hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                {/* Détails étendus */}
                {showDetails[player.id] && (
                  <div className="mt-4 pt-4 border-t border-gray-600">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <h5 className="text-white font-medium mb-2">Portrait</h5>
                        <div className="space-y-1 text-gray-400">
                          <div>Visage: {player.portrait.faceShape}</div>
                          <div>Yeux: {player.portrait.eyeShape}</div>
                          <div>Coiffure: {player.portrait.hairstyle}</div>
                        </div>
                      </div>
                      
                      <div>
                        <h5 className="text-white font-medium mb-2">Informations</h5>
                        <div className="space-y-1 text-gray-400">
                          <div>Genre: {player.gender === 'M' ? 'Homme' : 'Femme'}</div>
                          <div>Âge: {player.age || 'Non spécifié'} ans</div>
                          <div>Rôle: {PLAYER_ROLES[player.role].name}</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-3 text-xs text-gray-500">
                      Créé le: {new Date(player.createdAt).toLocaleDateString('fr-FR')}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default CustomPlayersList;