<template>
  <div class="container is-fluid">
    <section class="hero is-primary mb-4">
      <div class="hero-body">
        <h2 class="title">Terrain Condition</h2>
      </div>
    </section>

    <div v-if="loading" class="notification is-info">
      <i class="fas fa-spinner fa-spin mr-2"></i> {{ loadingMessage }}
    </div>
    <div v-if="error" class="notification is-danger">
      <i class="fas fa-exclamation-triangle mr-2"></i> {{ error }}
    </div>
    <div v-if="terrainCondition" class="box">
      <h3 class="subtitle is-4"><i :class="getWeatherIcon(terrainCondition.current_condition)" class="mr-2"></i> {{ terrainCondition.current_condition }}</h3>
      <p><i class="fas fa-thermometer-half mr-2"></i> Temperature: {{ terrainCondition.temperature }} °C</p>
      <p><i class="fas fa-wind mr-2"></i> Wind Speed: {{ terrainCondition.windspeed }} km/h</p>
      <p><i class="fas fa-mountain mr-2"></i> Elevation: {{ terrainCondition.elevation }} m</p>
      <p><strong><i class="fas fa-map-signs mr-2"></i> Terrain Assessment:</strong> {{ terrainCondition.terrain_assessment }}</p>
      <p><i class="fas fa-map-marker-alt mr-2"></i> Latitude: {{ terrainCondition.latitude }}</p>
      <p><i class="fas fa-map-marker-alt mr-2"></i> Longitude: {{ terrainCondition.longitude }}</p>
      <p><i class="fas fa-clock mr-2"></i> Timezone: {{ terrainCondition.timezone }} (Current Time: {{ currentTime }})</p>
    </div>
    <div v-else-if="!loading && !error && !searchResults.length" class="notification">
      <i class="fas fa-info-circle mr-2"></i> Enter a location to search for terrain condition data.
    </div>
    <div v-if="searchResults.length" class="box">
      <h3 class="subtitle is-5">Search Results:</h3>
      <ul>
        <li v-for="result in searchResults" :key="result.id" @click="selectLocation(result)" class="mb-2">
          <a href="#" class="has-text-weight-semibold">{{ result.name }}, {{ result.admin1 }}, {{ result.country }}</a>
          <span class="is-size-7">(Lat: {{ result.latitude }}, Lon: {{ result.longitude }})</span>
        </li>
      </ul>
    </div>
    <div class="field">
      <label class="label" for="location"><i class="fas fa-search mr-2"></i> Search Location:</label>
      <div class="control">
        <input class="input" type="text" id="location" v-model="searchQuery">
      </div>
    </div>
    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link" @click="searchLocation"><i class="fas fa-binoculars mr-2"></i> Search</button>
      </div>
    </div>
    <div class="field is-grouped">
      <div class="control">
        <label class="label" for="latitude"><i class="fas fa-globe mr-2"></i> Latitude:</label>
        <input class="input is-small" type="text" id="latitude" v-model="latitude" :readonly="selectedLocation">
      </div>
      <div class="control">
        <label class="label" for="longitude"><i class="fas fa-globe mr-2"></i> Longitude:</label>
        <input class="input is-small" type="text" id="longitude" v-model="longitude" :readonly="selectedLocation">
      </div>
    </div>
    <div class="control">
      <button class="button is-primary" @click="fetchTerrainCondition" :disabled="!latitude || !longitude">
        <i class="fas fa-cloud-sun mr-2"></i> Fetch Terrain Condition
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';

export default {
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      latitude: null,
      longitude: null,
      terrainCondition: null,
      loading: false,
      loadingMessage: '',
      error: null,
      selectedLocation: false,
      currentTime: '',
    };
  },
  watch: {
    terrainCondition: {
      handler(newCondition) {
        if (newCondition && newCondition.timezone) {
          this.updateCurrentTime(newCondition.timezone);
        } else {
          this.currentTime = '';
        }
      },
      immediate: true,
    },
  },
  methods: {
    async searchLocation() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        return;
      }
      this.loading = true;
      this.loadingMessage = 'Searching locations...';
      this.error = null;
      this.searchResults = [];
      this.selectedLocation = false;
      this.latitude = null;
      this.longitude = null;
      try {
        const geocodingApiUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${this.searchQuery}&count=5`;
        const response = await axios.get(geocodingApiUrl);
        if (response.data.results) {
          this.searchResults = response.data.results;
        } else {
          this.searchResults = [];
          this.error = 'No locations found matching your query.';
        }
      } catch (error) {
        console.error('Error searching locations:', error);
        this.error = 'Error searching for locations.';
      } finally {
        this.loading = false;
        this.loadingMessage = '';
      }
    },
    selectLocation(location) {
      this.latitude = location.latitude;
      this.longitude = location.longitude;
      this.searchResults = [];
      this.selectedLocation = true;
    },
    updateCurrentTime(timezone) {
      try {
        const now = new Date();
        const zonedTime = toZonedTime(now, timezone);
        this.currentTime = format(zonedTime, 'yyyy-MM-dd HH:mm:ss zzzz');
      } catch (error) {
        console.error('Error formatting timezone:', error);
        this.currentTime = 'Error displaying time';
      }
    },
    getWeatherIcon(condition) {
      const lowerCaseCondition = condition.toLowerCase();
      if (lowerCaseCondition.includes('clear')) return 'fas fa-sun';
      if (lowerCaseCondition.includes('cloudy') || lowerCaseCondition.includes('overcast')) return 'fas fa-cloud';
      if (lowerCaseCondition.includes('rain') || lowerCaseCondition.includes('drizzle') || lowerCaseCondition.includes('showers')) return 'fas fa-cloud-rain';
      if (lowerCaseCondition.includes('snow') || lowerCaseCondition.includes('grains')) return 'fas fa-snowflake';
      if (lowerCaseCondition.includes('thunderstorm')) return 'fas fa-bolt';
      if (lowerCaseCondition.includes('fog')) return 'fas fa-smog';
      return 'fas fa-question'; // Default icon
    },
    async fetchTerrainCondition() {
      this.currentTime = '';
      if (!this.latitude || !this.longitude) {
        this.error = 'Please select a location or enter latitude and longitude.';
        return;
      }
      this.loading = true;
      this.loadingMessage = 'Fetching terrain condition...';
      this.error = null;
      this.terrainCondition = null;
      try {
        const response = await axios.get(`/api/travel_buddy/terrain-condition/?latitude=${this.latitude}&longitude=${this.longitude}`);
        this.terrainCondition = response.data;
        console.log("Terrain Condition:", this.terrainCondition);
      } catch (error) {
        console.error("Error fetching terrain condition:", error);
        this.error = 'Failed to fetch terrain condition data.';
        if (error.response && error.response.data) {
          console.error("Backend Error:", error.response.data);
          this.error += ` Backend error: ${JSON.stringify(error.response.data)}`;
        }
      } finally {
        this.loading = false;
        this.loadingMessage = '';
      }
    },
  },
};
</script>