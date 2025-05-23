<template>
  <div class="container">
    <h1 class="title">Flight Search</h1>

    <div class="columns is-multiline">
      <div class="column is-3">
        <div class="field">
          <label class="label">Departure City:</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="filters.departure_city">
                <option value="">All</option>
                <option v-for="city in cities" :key="city.id" :value="city.id">
                  {{ city.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-3">
        <div class="field">
          <label class="label">Arrival City:</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="filters.arrival_city">
                <option value="">All</option>
                <option v-for="city in cities" :key="city.id" :value="city.id">
                  {{ city.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-3">
        <div class="field">
          <label class="label">Departure Date:</label>
          <div class="control">
            <input class="input" type="date" v-model="filters.departure_time" />
          </div>
        </div>
      </div>

      <div class="column is-3">
        <div class="field">
          <label class="label">Seat Class:</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="filters.seatClass">
                <option value="">All</option>
                <option v-for="seatClass in seatClasses" :key="seatClass.id" :value="seatClass.name">
                  {{ seatClass.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="columns is-multiline">
      <div class="column is-6">
        <div class="field">
          <label class="label">Sort By:</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="sort.by">
                <option value="base_price">Price</option>
                <option value="departure_time">Departure Date</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="field">
          <label class="label">Order:</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="sort.order">
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="has-text-centered">
      <p class="is-size-5">Loading flights...</p>
    </div>

    <div v-else-if="error" class="notification is-danger">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="filteredAndSortedFlights.length > 0">
        <div class="columns is-multiline">
          <div
            v-for="flight in filteredAndSortedFlights"
            :key="flight.id"
            class="column is-4"
          >
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <i class="fas fa-plane fa-2x"></i>
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-5">
                      {{ flight.departure_city?.name }} → {{ flight.arrival_city?.name }}
                    </p>
                    <p class="subtitle is-6">
                      Departure: {{ formatDate(flight.departure_time) }}
                    </p>
                    <p class="subtitle is-6">
                      Arrival: {{ formatDate(flight.arrival_time) }}
                    </p>
                  </div>
                </div>
                <div class="content">
                  <p>Airline: {{ flight.airline }}</p>
                  <p>Price: Ksh{{ flight.base_price }}</p>
                  <button
                    @click="showDetails(flight)"
                    class="button is-primary"
                  >
                    Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="has-text-centered">
        <p class="is-size-5">No flights found matching your criteria</p>
      </div>
    </div>

    <div v-if="selectedFlight" class="modal is-active">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Flight Details</p>
          <button
            class="delete"
            aria-label="close"
            @click="selectedFlight = null"
          ></button>
        </header>
        <section class="modal-card-body">
          <p>Flight Number: {{ selectedFlight?.flight_number }}</p>
          <p>Airline: {{ selectedFlight?.airline }}</p>
          <p>
            Departure Airport: {{ selectedFlight?.departure_airport?.name }}
            ({{ selectedFlight?.departure_airport?.city?.name }})
          </p>
          <p>
            Arrival Airport: {{ selectedFlight?.arrival_airport?.name }}
            ({{ selectedFlight?.arrival_airport?.city?.name }})
          </p>
          <p>Departure Time: {{ formatDate(selectedFlight?.departure_time) }}</p>
          <p>Arrival Time: {{ formatDate(selectedFlight?.arrival_time) }}</p>

          <div v-if="selectedFlight?.seats?.length > 0">
            <p class="has-text-weight-semibold">Available Seats:</p>
            <ul class="menu-list">
              <li
                v-for="seat in selectedFlight.seats"
                :key="seat?.id"
                :class="{
                  'is-unavailable': !seat?.is_available,
                  'is-selected': seat?.id === selectedSeatId
                }"
                @click="seat?.is_available && selectSeat(seat)"
              >
                Seat {{ seat?.seat_number }} ({{ seat?.seat_class?.name }}) -
                Ksh{{ calculateSeatPrice(selectedFlight.base_price, seat?.seat_class?.price_multiplier) }}
              </li>
            </ul>
          </div>
          <div v-else class="has-text-centered">
            <p class="has-text-grey">No available seats</p>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="bookFlightNow()">
            Book Now
          </button>
          <button class="button" @click="selectedFlight = null">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      flights: [],
      cities: [],
      seatClasses: [],
      loading: true,
      error: null,
      filters: {
        departure_city: '',
        arrival_city: '',
        departure_time: '',
        seatClass: '',
      },
      sort: {
        by: 'base_price',
        order: 'asc',
      },
      selectedFlight: null,
      selectedSeatId: null,
    };
  },
  async mounted() {
    await Promise.all([
      this.fetchFlights(),
      this.fetchCities(),
      this.fetchSeatClasses()
    ]);
  },
  computed: {
    filteredAndSortedFlights() {
      const flights = this.flights || [];

      let filteredFlights = flights.filter((flight) => {
        const matchesDeparture = this.filters.departure_city ?
          flight.departure_city?.id === parseInt(this.filters.departure_city) :
          true;

        const matchesArrival = this.filters.arrival_city ?
          flight.arrival_city?.id === parseInt(this.filters.arrival_city) :
          true;

        const matchesDate = this.filters.departure_time ?
          flight.departure_time?.startsWith(this.filters.departure_time) :
          true;

        const matchesSeatClass = this.filters.seatClass ?
          flight.seats?.some(seat =>
            seat.seat_class?.name === this.filters.seatClass &&
            seat.is_available
          ) :
          true;

        return matchesDeparture && matchesArrival && matchesDate && matchesSeatClass;
      });

      return filteredFlights.sort((a, b) => {
        const order = this.sort.order === 'asc' ? 1 : -1;
        if (this.sort.by === 'base_price') {
          return (a.base_price - b.base_price) * order;
        }
        if (this.sort.by === 'departure_time') {
          return (
            new Date(a.departure_time) - new Date(b.departure_time)
          ) * order;
        }
        return 0;
      });
    },
  },
  methods: {
    async fetchFlights() {
      try {
        this.loading = true;
        const response = await axios.get('/api/travel_buddy/flights/');
        this.flights = response.data.results || response.data || [];
        this.error = null;
      } catch (err) {
        console.error('Error fetching flights:', err);
        this.error = 'Failed to load flights. Please try again later.';
        this.flights = [];
      } finally {
        this.loading = false;
      }
    },
    async fetchCities() {
      try {
        const response = await axios.get('/api/travel_buddy/cities/');
        this.cities = response.data || [];
      } catch (err) {
        console.error('Error fetching cities:', err);
        this.cities = [];
      }
    },
    async fetchSeatClasses() {
      try {
        const response = await axios.get('/api/travel_buddy/seatclasses/');
        this.seatClasses = response.data.results || response.data || [];
      } catch (err) {
        console.error('Error fetching seat classes:', err);
        this.seatClasses = [];
      }
    },
    showDetails(flight) {
      this.selectedFlight = flight;
      this.selectedSeatId = null;
      console.log('showDetails - selectedFlight:', this.selectedFlight);
    },
    formatDate(dateTimeString) {
      if (!dateTimeString) return 'N/A';
      const date = new Date(dateTimeString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    selectSeat(seat) {
      if (seat.is_available) {
        this.selectedSeatId = seat.id;
        console.log('selectSeat - Selected Seat ID:', this.selectedSeatId);
      } else {
        alert('This seat is not available.');
      }
    },
    calculateSeatPrice(basePrice, multiplier) {
      const base = parseFloat(basePrice) || 0;
      const mult = parseFloat(multiplier) || 1.0;
      return (base * mult).toFixed(2);
    },
    async bookFlightNow() {
      if (!this.selectedSeatId || !this.selectedFlight) {
        alert('Please select a seat before booking.');
        return;
      }
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('You need to log in to book a flight.');
          this.$router.push({ name: 'login' });
          return;
        }

        // Prepare the list of seat IDs
        const seatIdsToSend = [this.selectedSeatId];
        console.log('bookFlightNow - seatIdsToSend:', seatIdsToSend);

        // --- FIX: Use 'seats_input' as the key ---
        const payload = {
          flight: this.selectedFlight.id,
          seats_input: seatIdsToSend, // Use the correct field name expected by the serializer
        };
        console.log('bookFlightNow - Booking Payload:', payload); // Log the corrected payload

        const response = await axios.post(
          '/api/travel_buddy/bookings/', // Endpoint for creating bookings
          payload, // Send the corrected payload object
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        console.log('bookFlightNow - Response:', response);
        if (response.status === 201) {
          alert('Booking successful!');
          // Update UI state to reflect the booked seat
          const bookedSeat = this.selectedFlight.seats?.find(
            seat => seat.id === this.selectedSeatId
          );
          if (bookedSeat) bookedSeat.is_available = false; // Mark seat as unavailable locally
          this.selectedSeatId = null; // Clear selection
          this.selectedFlight = null; // Close modal
          // Optionally re-fetch flights to get updated seat availability from server
          // this.fetchFlights();
        } else {
          // Handle unexpected success status (though unlikely for POST/create)
          alert(`Booking might have succeeded with status ${response.status}, but check 'My Bookings'.`);
        }
      } catch (err) {
        // Log the detailed error from the backend if available
        console.error('Booking error:', err.response?.data || err.message || err);
        if (err.response?.status === 401) {
          alert('Your session has expired. Please log in again.');
          this.$router.push({ name: 'login' });
        } else if (err.response?.data) {
            // Try to display a more specific error from the backend response
            let errorMessage = 'Failed to book flight. ';
            if (typeof err.response.data === 'object') {
                // Format DRF errors (e.g., { field: ["message"] })
                const errors = Object.entries(err.response.data).map(([field, messages]) =>
                    `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
                );
                errorMessage += errors.join('; ');
            } else {
                errorMessage += err.response.data; // Append if it's just a string
            }
             alert(errorMessage);
        }
         else {
          alert('Failed to book flight. An unknown error occurred.');
        }
      }
    },

  },
};
</script>

<style scoped>
.container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  margin-bottom: 2rem;
  text-align: center;
}

.card {
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.media-content .title {
  margin-bottom: 0.75rem;
  font-size: 1.25rem;
}

.media-content .subtitle {
  font-size: 0.9rem;
  color: #666;
}

.is-unavailable {
  color: #999;
  text-decoration: line-through;
  cursor: not-allowed;
}

.is-selected {
  background-color: #e8f4ff;
  border-left: 3px solid #3273dc;
}

.modal-card {
  width: 80%;
  max-width: 600px;
}

.menu-list li {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  margin: 0.25rem 0;
}

.menu-list li:hover {
  background-color: #f5f5f5;
}
</style>
