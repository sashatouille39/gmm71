// Service pour gérer les célébrités
export class CelebritiesService {
  constructor() {
    this.backendUrl = process.env.REACT_APP_BACKEND_URL;
  }

  // Récupère toutes les célébrités disponibles (vivantes par défaut)
  async getAllCelebrities(limit = 1000, includeDead = false) {
    try {
      const response = await fetch(`${this.backendUrl}/api/celebrities/?limit=${limit}&include_dead=${includeDead}`);
      if (!response.ok) {
        throw new Error('Erreur lors du chargement des célébrités');
      }
      const celebrities = await response.json();
      return celebrities;
    } catch (error) {
      console.error('Erreur lors du chargement des célébrités:', error);
      throw error;
    }
  }

  // Récupère une célébrité par son ID
  async getCelebrityById(id) {
    try {
      const response = await fetch(`${this.backendUrl}/api/celebrities/${id}`);
      if (!response.ok) {
        throw new Error('Célébrité non trouvée');
      }
      const celebrity = await response.json();
      return celebrity;
    } catch (error) {
      console.error('Erreur lors du chargement de la célébrité:', error);
      throw error;
    }
  }

  // Récupère les célébrités possédées en fonction des IDs du gamestate (vivantes par défaut)
  async getOwnedCelebrities(ownedIds, includeDead = false) {
    try {
      if (!ownedIds || ownedIds.length === 0) {
        return [];
      }

      // Récupérer toutes les célébrités et filtrer celles possédées
      const allCelebrities = await this.getAllCelebrities(1000, includeDead);
      const ownedCelebrities = allCelebrities.filter(celebrity => 
        ownedIds.includes(celebrity.id)
      );
      
      return ownedCelebrities;
    } catch (error) {
      console.error('Erreur lors du chargement des célébrités possédées:', error);
      throw error;
    }
  }

  // Récupère les célébrités par nombre d'étoiles
  async getCelebritiesByStars(stars) {
    try {
      const response = await fetch(`${this.backendUrl}/api/celebrities/?stars=${stars}`);
      if (!response.ok) {
        throw new Error('Erreur lors du chargement des célébrités');
      }
      const celebrities = await response.json();
      return celebrities;
    } catch (error) {
      console.error('Erreur lors du chargement des célébrités par étoiles:', error);
      throw error;
    }
  }

  // Récupère les célébrités par catégorie
  async getCelebritiesByCategory(category) {
    try {
      const response = await fetch(`${this.backendUrl}/api/celebrities/?category=${encodeURIComponent(category)}`);
      if (!response.ok) {
        throw new Error('Erreur lors du chargement des célébrités');
      }
      const celebrities = await response.json();
      return celebrities;
    } catch (error) {
      console.error('Erreur lors du chargement des célébrités par catégorie:', error);
      throw error;
    }
  }

  // Récupère les anciens gagnants
  async getPastWinners() {
    try {
      const response = await fetch(`${this.backendUrl}/api/statistics/winners`);
      if (!response.ok) {
        throw new Error('Erreur lors du chargement des anciens gagnants');
      }
      const winners = await response.json();
      return winners;
    } catch (error) {
      console.error('Erreur lors du chargement des anciens gagnants:', error);
      throw error;
    }
  }
}

// Instance singleton
export const celebritiesService = new CelebritiesService();