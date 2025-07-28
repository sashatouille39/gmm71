import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useCustomPlayers } from '../hooks/useCustomPlayers';

const DebugCustomPlayers = () => {
  const { customPlayers, addPlayer } = useCustomPlayers();

  const testAddPlayer = () => {
    const testPlayer = {
      name: 'Test Player',
      nationality: 'Française',
      gender: 'M',
      age: 25,
      role: 'normal',
      stats: { intelligence: 5, force: 5, agilité: 4 },
      portrait: {
        faceShape: 'Ovale',
        skinColor: '#FDBCB4',
        hairstyle: 'Cheveux courts',
        hairColor: '#8B4513',
        eyeColor: '#8B4513',
        eyeShape: 'Amande'
      }
    };
    
    console.log('🔍 DEBUG: Adding test player manually');
    addPlayer(testPlayer);
  };

  const checkLocalStorage = () => {
    const data = localStorage.getItem('gamemaster-custom-players');
    console.log('🔍 DEBUG localStorage check:', data);
    if (data) {
      console.log('🔍 DEBUG Parsed:', JSON.parse(data));
    }
  };

  const clearLocalStorage = () => {
    localStorage.removeItem('gamemaster-custom-players');
    console.log('🔍 DEBUG: Cleared localStorage');
    window.location.reload();
  };

  return (
    <Card className="bg-black/50 border-yellow-500/30">
      <CardHeader>
        <CardTitle className="text-yellow-400">Debug Custom Players</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-white">Joueurs dans le hook: {customPlayers.length}</p>
          <pre className="text-xs text-gray-300 bg-gray-800 p-2 rounded mt-2 overflow-auto">
            {JSON.stringify(customPlayers, null, 2)}
          </pre>
        </div>
        
        <div className="flex gap-2">
          <Button onClick={testAddPlayer} className="bg-green-600 hover:bg-green-700">
            Ajouter joueur test
          </Button>
          <Button onClick={checkLocalStorage} className="bg-blue-600 hover:bg-blue-700">
            Vérifier localStorage  
          </Button>
          <Button onClick={clearLocalStorage} className="bg-red-600 hover:bg-red-700">
            Vider localStorage
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default DebugCustomPlayers;