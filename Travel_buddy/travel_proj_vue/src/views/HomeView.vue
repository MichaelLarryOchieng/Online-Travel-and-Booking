<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">
          Travel Buddy
        </p>
        <p class="subtitle">
          Your best online Agency
        </p>
      </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered mb-4">Attractions</h2>
      </div>

      <div class="column is-6 is-5-desktop" v-for="attraction in AttractionList" :key="attraction.id">
        <div class="box has-shadow attraction-box">
          <figure class="image mb-4 attraction-image">
            <img :src="attraction.get_thumbnail" alt="Attraction Thumbnail">
          </figure>

          <h3 class="is-size-4">{{ attraction.name }}</h3>
          <p class="is-size-6">Ksh {{ attraction.price }}</p>

          <button class="button is-link is-small mt-2">View details</button>
        </div>
      </div>

      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered mb-4 mt-6">Cities</h2>
      </div>

      <div class="column is-6 is-5-desktop" v-for="city in CityList" :key="city.id">
        <div class="box has-shadow city-box">
          <figure class="image mb-4 city-image">
            <img :src="city.get_thumbnail" alt="City Thumbnail">
          </figure>

          <h3 class="is-size-4">{{ city.name }}</h3>
          <p class="is-size-6">{{ city.description.substring(0, 100) }}...</p>

          <button class="button is-link is-small mt-2">Explore City</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      AttractionList: [],
      CityList: [],
    };
  },
  mounted() {
    this.getAttractionList();
    this.getCityList();
  },
  methods: {
    getAttractionList() {
      axios
        .get('/api/travel_buddy/attractions/')
        .then((response) => {
          this.AttractionList = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getCityList() {
      axios
        .get('/api/travel_buddy/cities/')
        .then((response) => {
          this.CityList = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.attraction-box, .city-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}

.attraction-box:hover, .city-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.attraction-image, .city-image {
  display: flex;
  justify-content: center;
  overflow: hidden; /* Prevent image overflow */
}

.attraction-image img, .city-image img {
  max-width: 100%;
  height: 200px; /* Fixed height for consistent display */
  object-fit: cover;
  border-radius: 8px 8px 0 0; /* Rounded corners on top */
}

.attraction-box h3, .city-box h3 {
  margin-top: 1rem;
}

.attraction-box p, .city-box p {
  margin-bottom: 1rem;
}
</style>
