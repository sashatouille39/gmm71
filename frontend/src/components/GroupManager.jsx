import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { Users, Settings, Trash2, Edit2, Shield, ShieldOff } from 'lucide-react';

const GroupManager = ({ gameId = null, players, onGroupsCreated, onGroupsUpdated }) => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingGroup, setEditingGroup] = useState(null);
  const [editName, setEditName] = useState('');
  const [showManualCreation, setShowManualCreation] = useState(false);
  
  // État pour la création de groupes automatique
  const [createForm, setCreateForm] = useState({
    num_groups: 2,
    min_members: 2,
    max_members: 8,
    allow_betrayals: false
  });

  // État pour la création manuelle
  const [manualGroups, setManualGroups] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const [selectedPlayers, setSelectedPlayers] = useState({});
  const [draggedPlayer, setDraggedPlayer] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchGroups();
  }, [gameId]);

  const fetchGroups = async () => {
    try {
      setLoading(true);
      
      let url;
      if (gameId) {
        // Récupérer les groupes d'une partie spécifique
        url = `${backendUrl}/api/games/${gameId}/groups`;
      } else {
        // Récupérer les groupes pré-configurés
        url = `${backendUrl}/api/games/groups/preconfigured`;
      }
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setGroups(data.groups || []);
      } else {
        setError('Erreur lors du chargement des groupes');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const createGroups = async () => {
    try {
      setLoading(true);
      setError('');
      
      let url, payload;
      
      if (gameId) {
        // Création pour une partie spécifique (mode auto)
        url = `${backendUrl}/api/games/${gameId}/groups`;
        payload = createForm;
      } else {
        // Création de groupes pré-configurés (mode manuel)
        url = `${backendUrl}/api/games/groups/preconfigured`;
        payload = { groups: manualGroups };
      }
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        setGroups(data.groups || data.applied_groups || []);
        setShowCreateForm(false);
        setShowManualCreation(false);
        setManualGroups([]);
        onGroupsCreated && onGroupsCreated(data.groups || data.applied_groups);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la création des groupes');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const createManualGroup = () => {
    if (!newGroupName.trim()) {
      setError('Veuillez saisir un nom de groupe');
      return;
    }

    const selectedPlayerIds = Object.keys(selectedPlayers).filter(id => selectedPlayers[id]);
    
    if (selectedPlayerIds.length < 2) {
      setError('Un groupe doit contenir au moins 2 joueurs');
      return;
    }

    const newGroup = {
      name: newGroupName.trim(),
      member_ids: selectedPlayerIds,
      allow_betrayals: false
    };

    setManualGroups(prev => [...prev, newGroup]);
    setNewGroupName('');
    setSelectedPlayers({});
    setError('');
  };

  const removeManualGroup = (index) => {
    setManualGroups(prev => prev.filter((_, i) => i !== index));
  };

  const togglePlayerSelection = (playerId) => {
    setSelectedPlayers(prev => ({
      ...prev,
      [playerId]: !prev[playerId]
    }));
  };

  const saveManualGroups = async () => {
    if (manualGroups.length === 0) {
      setError('Créez au moins un groupe avant de sauvegarder');
      return;
    }
    await createGroups();
  };

  const updateGroup = async (groupId, updates) => {
    try {
      setLoading(true);
      
      let url;
      if (gameId) {
        url = `${backendUrl}/api/games/${gameId}/groups/${groupId}`;
      } else {
        url = `${backendUrl}/api/games/groups/preconfigured/${groupId}`;
      }
      
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        await fetchGroups();
        setEditingGroup(null);
        setEditName('');
        onGroupsUpdated && onGroupsUpdated();
      } else {
        setError('Erreur lors de la mise à jour du groupe');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const toggleBetrayalsForAll = async (allowBetrayals) => {
    try {
      setLoading(true);
      
      if (gameId) {
        const response = await fetch(`${backendUrl}/api/games/${gameId}/groups/toggle-betrayals`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ allow_betrayals: allowBetrayals }),
        });

        if (response.ok) {
          await fetchGroups();
          onGroupsUpdated && onGroupsUpdated();
        } else {
          setError('Erreur lors de la mise à jour des trahisons');
        }
      } else {
        // Pour les groupes pré-configurés, mettre à jour chacun individuellement
        const updatePromises = groups.map(group => 
          updateGroup(group.id, { allow_betrayals: allowBetrayals })
        );
        
        await Promise.all(updatePromises);
        await fetchGroups();
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const clearAllGroups = async () => {
    try {
      setLoading(true);
      
      let url;
      if (gameId) {
        url = `${backendUrl}/api/games/${gameId}/groups`;
      } else {
        url = `${backendUrl}/api/games/groups/preconfigured`;
      }
      
      const response = await fetch(url, {
        method: 'DELETE',
      });

      if (response.ok) {
        setGroups([]);
        onGroupsUpdated && onGroupsUpdated();
      } else {
        setError('Erreur lors de la suppression des groupes');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const alivePlayers = players.filter(p => p.alive);
  const maxPossibleGroups = Math.floor(alivePlayers.length / 2);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Gestion des Groupes
          </CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <div className="flex gap-4 mb-4">
            <div className="text-sm text-gray-600">
              Joueurs vivants: {alivePlayers.length}
            </div>
            <div className="text-sm text-gray-600">
              Groupes créés: {groups.length}
            </div>
          </div>

          {groups.length === 0 ? (
            <div className="text-center py-8">
              <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">Aucun groupe créé</p>
              <div className="flex gap-3 justify-center">
                {gameId ? (
                  // Mode partie: création automatique
                  <Button 
                    onClick={() => setShowCreateForm(true)}
                    disabled={loading || alivePlayers.length < 4}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    Créer automatiquement
                  </Button>
                ) : (
                  // Mode pré-configuration: création manuelle
                  <Button 
                    onClick={() => setShowManualCreation(true)}
                    disabled={loading || players.length < 2}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    Créer des groupes
                  </Button>
                )}
              </div>
              {(!gameId && players.length < 2) && (
                <p className="text-sm text-red-600 mt-2">
                  Minimum 2 joueurs requis pour créer des groupes
                </p>
              )}
              {(gameId && alivePlayers.length < 4) && (
                <p className="text-sm text-red-600 mt-2">
                  Minimum 4 joueurs vivants requis pour créer des groupes
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {/* Actions globales */}
              <div className="flex gap-2 justify-between items-center">
                <div className="flex gap-2">
                  <Button
                    onClick={() => toggleBetrayalsForAll(true)}
                    disabled={loading}
                    variant="outline"
                    size="sm"
                    className="text-red-600 hover:text-red-700"
                  >
                    <Shield className="h-4 w-4 mr-1" />
                    Activer trahisons (tous)
                  </Button>
                  <Button
                    onClick={() => toggleBetrayalsForAll(false)}
                    disabled={loading}
                    variant="outline"
                    size="sm"
                    className="text-green-600 hover:text-green-700"
                  >
                    <ShieldOff className="h-4 w-4 mr-1" />
                    Désactiver trahisons (tous)
                  </Button>
                </div>
                <Button
                  onClick={clearAllGroups}
                  disabled={loading}
                  variant="outline"
                  size="sm"
                  className="text-red-600 hover:text-red-700"
                >
                  <Trash2 className="h-4 w-4 mr-1" />
                  Supprimer tous
                </Button>
              </div>

              {/* Liste des groupes */}
              <div className="grid gap-4">
                {groups.map((group, index) => (
                  <Card key={group.id} className="border-l-4 border-l-blue-500">
                    <CardContent className="p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div className="flex items-center gap-2">
                          {editingGroup === group.id ? (
                            <div className="flex gap-2 items-center">
                              <Input
                                value={editName}
                                onChange={(e) => setEditName(e.target.value)}
                                className="w-32"
                              />
                              <Button
                                onClick={() => updateGroup(group.id, { name: editName })}
                                disabled={loading}
                                size="sm"
                              >
                                OK
                              </Button>
                              <Button
                                onClick={() => {
                                  setEditingGroup(null);
                                  setEditName('');
                                }}
                                variant="outline"
                                size="sm"
                              >
                                Annuler
                              </Button>
                            </div>
                          ) : (
                            <>
                              <h3 className="font-semibold">{group.name}</h3>
                              <Button
                                onClick={() => {
                                  setEditingGroup(group.id);
                                  setEditName(group.name);
                                }}
                                variant="ghost"
                                size="sm"
                              >
                                <Edit2 className="h-4 w-4" />
                              </Button>
                            </>
                          )}
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge variant={group.allow_betrayals ? "destructive" : "default"}>
                            {group.allow_betrayals ? "Trahisons ON" : "Trahisons OFF"}
                          </Badge>
                          <Switch
                            checked={group.allow_betrayals}
                            onCheckedChange={(checked) => 
                              updateGroup(group.id, { allow_betrayals: checked })
                            }
                            disabled={loading}
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="text-sm text-gray-600">
                          Membres ({group.members.length}):
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {group.members.map((member) => (
                            <Badge 
                              key={member.id} 
                              variant="outline"
                              className={member.alive ? "bg-green-50" : "bg-red-50"}
                            >
                              #{member.number} {member.name}
                              {!member.alive && " (mort)"}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Formulaire de création */}
          {showCreateForm && (
            <Card className="mt-4 border-2 border-blue-200">
              <CardHeader>
                <CardTitle className="text-lg">Créer des groupes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="num_groups">Nombre de groupes</Label>
                    <Input
                      id="num_groups"
                      type="number"
                      min="2"
                      max={maxPossibleGroups}
                      value={createForm.num_groups}
                      onChange={(e) => setCreateForm({
                        ...createForm,
                        num_groups: parseInt(e.target.value) || 2
                      })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="min_members">Membres minimum</Label>
                    <Input
                      id="min_members"
                      type="number"
                      min="2"
                      max="8"
                      value={createForm.min_members}
                      onChange={(e) => setCreateForm({
                        ...createForm,
                        min_members: parseInt(e.target.value) || 2
                      })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="max_members">Membres maximum</Label>
                    <Input
                      id="max_members"
                      type="number"
                      min="2"
                      max="8"
                      value={createForm.max_members}
                      onChange={(e) => setCreateForm({
                        ...createForm,
                        max_members: parseInt(e.target.value) || 8
                      })}
                    />
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={createForm.allow_betrayals}
                      onCheckedChange={(checked) => setCreateForm({
                        ...createForm,
                        allow_betrayals: checked
                      })}
                    />
                    <Label>Autoriser les trahisons</Label>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button
                    onClick={createGroups}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {loading ? 'Création...' : 'Créer les groupes'}
                  </Button>
                  <Button
                    onClick={() => setShowCreateForm(false)}
                    variant="outline"
                  >
                    Annuler
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default GroupManager;