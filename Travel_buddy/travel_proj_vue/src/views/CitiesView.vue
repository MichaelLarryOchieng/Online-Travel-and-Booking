<template>
  <div class="city-list">
    <h1>Popular Destinations</h1>
    <div v-if="loading">Loading cities...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else class="city-grid">
      <li v-for="city in cities" :key="city.id" class="city-card">
        <h3>{{ city.name }}, {{ city.country }}</h3>
        <img :src="city.get_thumbnail" :alt="city.name" v-if="city.get_thumbnail" class="city-image">
        <p>{{ city.description ? city.description.substring(0, 100) + '...' : '' }}</p>
        <button @click="showCityDetails(city)" class="view-details-button">View Details</button>
        <div class="map-container" :id="`map-${city.id}`" ref="mapContainers"></div>
      </li>
    </ul>

    <div v-if="selectedCity" class="modal is-active">
      <div class="modal-background" @click="closeCityDetails"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ selectedCity.name }}, {{ selectedCity.country }}</p>
          <button class="delete" aria-label="close" @click="closeCityDetails"></button>
        </header>
        <section class="modal-card-body">
          <p><strong>Description:</strong></p>
          <p>{{ selectedCity.description }}</p>
          <br>
          <p><strong>Latitude:</strong> {{ selectedCity.latitude }}</p>
          <p><strong>Longitude:</strong> {{ selectedCity.longitude }}</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="bookFlight(selectedCity)">Book Flight</button>
          <button class="button" @click="closeCityDetails">Close</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
  data() {
    return {
      cities: null,
      loading: true,
      error: null,
      selectedCity: null, // To control the modal and store the selected city
    };
  },
  mounted() {
    this.fetchCitiesAndInitMaps();
  },
  methods: {
    async fetchCitiesAndInitMaps() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/travel_buddy/cities/');
        this.cities = response.data;
        this.$nextTick(() => {
          this.initAllMaps();
        });
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load cities';
      } finally {
        this.loading = false;
      }
    },
    initAllMaps() {
      this.cities.forEach(city => {
        this.initMapForCity(city);
      });
    },
    initMapForCity(city) {
      const lat = parseFloat(city.latitude);
      const lng = parseFloat(city.longitude);

      if (!Number.isFinite(lat) || !Number.isFinite(lng) || Math.abs(lat) > 90 || Math.abs(lng) > 180) {
        console.error(`Invalid coordinates for ${city.name}: ${lat},${lng}`);
        return;
      }

      this.$nextTick(() => {
        const mapContainer = this.$refs.mapContainers.find(
          el => el.id === `map-${city.id}`
        );

        if (mapContainer && !mapContainer._leaflet_map) {
          try {
            const map = L.map(mapContainer, {
              attributionControl: false,
              preferCanvas: true
            }).setView([lat, lng], 10);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              maxZoom: 19,
              detectRetina: true
            }).addTo(map);

            L.marker([lat, lng])
              .addTo(map)
              .bindPopup(`<b>${city.name}</b><br>${city.country}`);

            mapContainer._leaflet_map = map;
          } catch (error) {
            console.error('Map init error:', error);
          }
        }
      });
    },
    beforeUnmount() {
      this.$refs.mapContainers?.forEach(container => {
        if (container._leaflet_map) {
          container._leaflet_map.remove();
          delete container._leaflet_map;
        }
      });
    },
    showCityDetails(city) {
      this.selectedCity = city;
    },
    closeCityDetails() {
      this.selectedCity = null;
    },
    bookFlight(city) {
      // Navigate to the flight search page, passing the city name as a query parameter
      this.$router.push({ name: 'flights', query: { destination: city.name } });
      this.closeCityDetails(); // Optionally close the modal after clicking "Book Flight"
    },
  },
};
</script>

<style scoped>
.city-list {
  padding: 20px;
}

.city-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  list-style: none;
  padding: 0;
}

.city-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.city-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 10px;
}

.view-details-button {
  display: inline-block;
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  margin-top: 10px;
  cursor: pointer; /* Indicate it's clickable */
}

.loading, .error {
  text-align: center;
  padding: 20px;
  font-size: 1.2rem;
}

.map-container {
  height: 200px;
  background: #f8f9fa;

  /* Fix Leaflet image paths */
  .leaflet-container img {
    max-width: none !important;
    max-height: none !important;
  }

  /* Hide attribution */
  .leaflet-control-attribution {
    display: none;
  }
}

.map-placeholder {
  background-color: #f0f0f0;
  color: #777;
  text-align: center;
  padding: 15px;
  border-radius: 6px;
  margin-top: 10px;
  height: 200px; /* Match map container height */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer; /* Indicate it's clickable to close */
}

.modal-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin: 20px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-card-head {
  padding: 1rem;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-card-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.modal-card-body {
  padding: 1rem;
  flex-grow: 1; /* Allow body to grow and scroll */
}

.modal-card-foot {
  padding: 1rem;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: flex-end;
}

.modal-card-foot .button {
  margin-left: 0.5rem;
}
</style>