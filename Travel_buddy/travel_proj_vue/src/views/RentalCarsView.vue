<template>
  <div class="rental-cars-container">
    <h1 class="page-title">Available Rental Cars</h1>

    <!-- Filter Section -->
    <div class="filters-section">
       <div class="filter-group">
        <label for="company-filter">Company:</label>
        <select id="company-filter" v-model="filters.company" @change="applyFilters">
          <option value="">All Companies</option>
          <option v-for="company in uniqueCompanies" :key="company" :value="company"> {{ company }} </option>
        </select>
      </div>
      <div class="filter-group">
        <label for="model-filter">Model:</label>
        <select id="model-filter" v-model="filters.model" @change="applyFilters">
          <option value="">All Models</option>
          <option v-for="model in uniqueModels" :key="model" :value="model"> {{ model }} </option>
        </select>
      </div>
      <div class="filter-group">
        <label for="city-filter">City:</label>
        <select id="city-filter" v-model="filters.city" @change="applyFilters">
          <option value="">All Cities</option>
          <option v-for="city in uniqueCities" :key="city" :value="city"> {{ city }} </option>
        </select>
      </div>
      <div class="filter-group">
        <label for="price-filter">Max Price/Day:</label>
        <input type="number" id="price-filter" v-model.number="filters.price" placeholder="Max price" min="0" @input="applyFilters">
      </div>
      <button class="reset-btn" @click="resetFilters">Reset Filters</button>
    </div>

    <!-- Status Messages -->
    <div v-if="loading" class="status-message">Loading rental cars...</div>
    <div v-else-if="error" class="status-message error">{{ error }}</div>
    <div v-else-if="filteredCars.length === 0" class="status-message">
      No cars found matching your criteria.
    </div>

    <!-- Cars Grid -->
    <div v-else class="cars-grid">
      <div v-for="car in filteredCars" :key="car.id" class="car-card">
        <div class="image-container">
          <img :src="car.thumbnail || car.image_url" :alt="car.name" class="car-image" @error="handleImageError"> <!-- Use API field names -->
        </div>
        <div class="car-details">
          <h2 class="car-name">{{ car.name }}</h2>
          <div class="detail-row"> <span class="detail-label">Company:</span> <span class="detail-value">{{ car.company }}</span> </div>
          <div class="detail-row"> <span class="detail-label">Location:</span> <span class="detail-value">{{ car.city_name }}</span> </div>
          <div class="detail-row"> <span class="detail-label">Model:</span> <span class="detail-value">{{ car.model }}</span> </div>
          <div class="detail-row price-row"> <span class="detail-label">Price/Day:</span> <span class="price-value">Ksh {{ car.price_per_day }}</span> </div>
          <div class="actions"> <button class="details-btn" @click="showDetails(car)">View Details</button> </div>
          <div class="availability-badge" :class="{ 'available': car.availability, 'unavailable': !car.availability }">
            {{ car.availability ? 'Available' : 'Likely Booked' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="selectedCar" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">&times;</button>
        <h2>{{ selectedCar.name }} Details</h2>
        <div class="modal-details">
          <div class="detail-column">
            <p><strong>Company:</strong> {{ selectedCar.company }}</p>
            <p><strong>Model:</strong> {{ selectedCar.model }}</p>
            <p><strong>Year:</strong> {{ selectedCar.year }}</p>
            <p><strong>Color:</strong> {{ selectedCar.color }}</p>
            <p><strong>Seats:</strong> {{ selectedCar.seats }}</p>
            <p><strong>Luggage:</strong> {{ selectedCar.luggage_capacity }} bags</p>
          </div>
          <div class="detail-column">
            <p><strong>Fuel:</strong> {{ selectedCar.fuel_type }}</p>
            <p><strong>Transmission:</strong> {{ selectedCar.transmission }}</p>
            <p><strong>Price/Day:</strong> Ksh {{ selectedCar.price_per_day }}</p>
            <p><strong>Location:</strong> {{ selectedCar.city_name }}</p>
            <div class="features">
              <h3>Features:</h3>
              <ul>
                <li v-if="selectedCar.air_conditioning">Air Conditioning</li>
                <li v-if="selectedCar.gps">GPS</li>
                <li v-if="selectedCar.bluetooth">Bluetooth</li>
                <li v-if="selectedCar.child_seat">Child Seat</li>
                <li v-if="selectedCar.sunroof">Sunroof</li>
                <!-- Add other boolean features similarly -->
              </ul>
            </div>
          </div>
        </div>

        <!-- Booking Section within Modal -->
        <div class="booking-section">
          <h3>Book This Car</h3>
          <div class="date-inputs">
            <div class="form-group">
              <label for="start-date">Pickup Date & Time:</label>
              <input type="datetime-local" id="start-date" v-model="bookingStartDate" :min="minDateTimeLocal()">
            </div>
            <div class="form-group">
              <label for="end-date">Return Date & Time:</label>
              <input type="datetime-local" id="end-date" v-model="bookingEndDate" :min="bookingStartDate || minDateTimeLocal()">
            </div>
          </div>
          <button
            class="book-btn"
            :disabled="!selectedCar.availability || bookingLoading || !bookingStartDate || !bookingEndDate"
            @click="bookCar(selectedCar)"
          >
            {{ bookingLoading ? 'Booking...' : (selectedCar.availability ? 'Confirm Booking' : 'Not Available') }}
          </button>

          <!-- *** MODIFIED ERROR DISPLAY AREA *** -->
          <div v-if="bookingError" class="error-container">
              <p class="error booking-error">{{ bookingError }}</p>
              <!-- Show login button only for session expired error -->
              <button
                  v-if="bookingError.includes('session may have expired')"
                  @click="$router.push('/login')"
                  class="login-link-button"
              >
                  Log In
              </button>
          </div>
          <!-- *** END MODIFIED AREA *** -->

          <p v-if="bookingSuccess" class="success booking-success">{{ bookingSuccess }}</p>
        </div>
        <!-- End Booking Section -->

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RentalCarsView',
  data() {
    return {
      cars: [],
      loading: true,
      error: null,
      selectedCar: null,
      filters: {
        company: '',
        city: '',
        model: '',
        price: null
      },
      // Booking specific data
      bookingStartDate: '',
      bookingEndDate: '',
      bookingLoading: false,
      bookingError: null,
      bookingSuccess: null,
    };
  },
  computed: {
    // Filtering computed properties
    filteredCars() {
      return this.cars.filter(car => {
        const matchesCompany = this.filters.company ? car.company === this.filters.company : true;
        const matchesCity = this.filters.city ? car.city_name?.toLowerCase().includes(this.filters.city.toLowerCase()) : true;
        const matchesModel = this.filters.model ? car.model === this.filters.model : true;
        const matchesPrice = this.filters.price != null && this.filters.price >= 0 ? parseFloat(car.price_per_day) <= this.filters.price : true;
        return matchesCompany && matchesCity && matchesModel && matchesPrice;
      });
    },
    uniqueCompanies() {
      return [...new Set(this.cars.map(car => car.company).filter(Boolean))].sort();
    },
    uniqueModels() {
      return [...new Set(this.cars.map(car => car.model).filter(Boolean))].sort();
    },
    uniqueCities() {
      return [...new Set(this.cars.map(car => car.city_name).filter(Boolean))].sort();
    }
  },
  methods: {
    async fetchCars() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/travel_buddy/cars/');
        this.cars = response.data;
      } catch (err) {
        console.error('Error fetching cars:', err.response?.data || err.message);
        this.error = 'Failed to load rental cars. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    showDetails(car) {
      // Reset booking state when opening modal
      this.bookingStartDate = '';
      this.bookingEndDate = '';
      this.bookingError = null;
      this.bookingSuccess = null;
      this.selectedCar = car;
    },
    closeModal() {
        this.selectedCar = null;
        this.bookingStartDate = '';
        this.bookingEndDate = '';
        this.bookingError = null;
        this.bookingSuccess = null;
    },
    async bookCar(car) {
      this.bookingLoading = true;
      this.bookingError = null;
      this.bookingSuccess = null;

      // 1. Get Auth Token
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.bookingError = 'You must be logged in to book a car.';
        this.bookingLoading = false;
        return;
      }

      // 2. Validate Dates
      if (!this.bookingStartDate || !this.bookingEndDate) {
        this.bookingError = 'Please select both pickup and return dates.';
        this.bookingLoading = false;
        return;
      }
      if (new Date(this.bookingEndDate) <= new Date(this.bookingStartDate)) {
          this.bookingError = 'Return date must be after pickup date.';
          this.bookingLoading = false;
          return;
      }
       if (new Date(this.bookingStartDate) < new Date(this.minDateTimeLocal())) {
          this.bookingError = 'Pickup date cannot be in the past.';
          this.bookingLoading = false;
          return;
      }

      // 3. Construct Payload
      const payload = {
        car: car.id,
        start_date: this.bookingStartDate,
        end_date: this.bookingEndDate,
      };
      console.log("Booking Payload:", payload);

      try {
        // 4. POST to Correct Endpoint
        const response = await axios.post(
          'http://127.0.0.1:8000/api/travel_buddy/car-bookings/',
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // 5. Handle Success
        if (response.status === 201) {
          this.bookingSuccess = `Booking successful for ${car.name}! Check 'My Bookings'.`;
          setTimeout(() => { this.closeModal(); }, 2000);
        } else {
          this.bookingError = `Booking attempt finished with status ${response.status}. Please check 'My Bookings' or try again.`;
        }
      } catch (err) {
        // 6. Handle Errors
        console.error('Error booking car:', err.response?.data || err.message);
         if (err.response?.status === 401) {
            // Set specific error message for the v-if condition
            this.bookingError = 'Your session may have expired. Please log in again.';
         } else if (err.response?.data) {
            let messages = [];
            for (const key in err.response.data) {
                messages.push(`${key}: ${Array.isArray(err.response.data[key]) ? err.response.data[key].join(', ') : err.response.data[key]}`);
            }
            this.bookingError = messages.join('; ') || 'Booking failed. Please check your selections.';
        } else {
            this.bookingError = 'An error occurred while booking the car. Please try again later.';
        }
      } finally {
        this.bookingLoading = false;
      }
    },
    resetFilters() {
      this.filters = { company: '', city: '', model: '', price: null };
    },
    applyFilters() { /* Filtering handled by computed */ },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/300x200?text=No+Image'; // Placeholder image
    },
    // Helper to set minimum date/time for date inputs to now
    minDateTimeLocal() {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        return now.toISOString().slice(0, 16);
    }
  },
  mounted() {
    this.fetchCars();
  }
};
</script>

<style scoped lang="scss">
/* Styles for Booking Section in Modal */
.booking-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}
.booking-section h3 {
  margin-bottom: 1rem;
  text-align: center;
  color: #333;
}
.date-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.date-inputs .form-group label {
  font-size: 0.9em;
  display: block; /* Ensure label is above input */
  margin-bottom: 0.3rem;
}
.date-inputs .form-group input {
  font-size: 0.95em;
  width: 100%; /* Ensure input takes full width */
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* --- Styles for Booking Button --- */
.book-btn {
  width: 100%;
  padding: 10px 15px;
  background-color: #28a745; /* Green color for confirmation */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
  margin-top: 1rem; /* Add some space above the button */
}

.book-btn:hover:not(:disabled) {
  background-color: #218838; /* Darker green on hover */
}

.book-btn:disabled {
  background-color: #94d3a2; /* Lighter, less saturated green when disabled */
  cursor: not-allowed;
}

/* --- Styles for Error Container and Login Button --- */
.error-container {
  margin-top: 1rem;
  text-align: center;
}

.booking-error {
    /* Keep existing styles */
    margin-bottom: 0.5rem; /* Add space below error text if button appears */
    display: inline-block; /* Allow button to sit somewhat alongside */
    margin-right: 0.5rem; /* Space between text and button */
    color: #dc3545; /* Ensure error text is red */
    background-color: transparent; /* Remove background for inline modal error */
    border: none;
}

.login-link-button {
  padding: 0.4rem 0.8rem;
  font-size: 0.9em;
  background-color: #007bff; /* Blue like other links/actions */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  vertical-align: baseline; /* Align with the error text */
}

.login-link-button:hover {
  background-color: #0056b3;
}
/* --- End Added Styles --- */

.booking-success {
    margin-top: 1rem;
    text-align: center;
    color: green;
}


/* Existing Styles */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6); display: flex;
  justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: white; padding: 2rem; border-radius: 8px;
  max-width: 700px; width: 90%; position: relative;
  max-height: 90vh; overflow-y: auto;
}
.modal-details {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem; margin: 1.5rem 0;
}
.detail-column p { margin-bottom: 0.75rem; }
.detail-column strong { color: #34495e; }
.close-btn {
  position: absolute; top: 0.5rem; right: 0.75rem; background: none;
  border: none; font-size: 2rem; cursor: pointer; padding: 0.5rem; color: #aaa;
}
.close-btn:hover { color: #333; }

.features { margin-top: 1rem; }
.features h3 { font-size: 1em; color: #34495e; margin-bottom: 0.5rem; }
.features ul { list-style: none; padding-left: 0; margin-top: 0.5rem; }
.features li { padding: 0.25rem 0; color: #555; font-size: 0.95em; }
.features li::before { content: "✓ "; color: #27ae60; margin-right: 5px; }


.rental-cars-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.page-title { text-align: center; color: #2c3e50; margin-bottom: 2rem; font-size: 2rem; }
.filters-section {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem; margin-bottom: 2rem; padding: 1.5rem; background: #f8f9fa;
  border-radius: 8px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08); align-items: end;
}
.filter-group { display: flex; flex-direction: column; }
.filter-group label { margin-bottom: 0.5rem; font-weight: 500; color: #495057; font-size: 0.9em; }
.filter-group input, .filter-group select {
  padding: 0.6rem; border: 1px solid #ced4da; border-radius: 4px; font-size: 0.95rem; box-sizing: border-box; width: 100%;
}
.reset-btn {
  padding: 0.6rem; background: #6c757d; color: white; border: none;
  border-radius: 4px; cursor: pointer; transition: background 0.3s ease; font-size: 0.95rem; height: fit-content;
}
.reset-btn:hover { background: #5a6268; }

.cars-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
.car-card {
  background: white; border-radius: 8px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: transform 0.2s ease, box-shadow 0.2s ease; display: flex; flex-direction: column;
}
.car-card:hover { transform: translateY(-4px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); }
.image-container { height: 180px; overflow: hidden; background-color: #eee; }
.car-image { width: 100%; height: 100%; object-fit: cover; }
.car-details { padding: 1rem 1.25rem; position: relative; display: flex; flex-direction: column; flex-grow: 1; }
.car-name { font-size: 1.15rem; color: #343a40; margin-bottom: 0.8rem; font-weight: 600; }
.detail-row { display: flex; justify-content: space-between; margin-bottom: 0.4rem; font-size: 0.85rem; }
.detail-label { color: #6c757d; }
.detail-value { color: #343a40; font-weight: 500; }
.price-row { margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f1f3f5; }
.price-value { color: #28a745; font-weight: bold; font-size: 1rem; }
.availability-badge {
  position: absolute; top: 1rem; right: 1rem; padding: 0.2rem 0.6rem;
  border-radius: 10px; font-size: 0.75rem; font-weight: 500;
}
.available { background: #e6f9f0; color: #28a745; }
.unavailable { background: #fdeded; color: #dc3545; }
.actions { margin-top: auto; padding-top: 1rem; }
.details-btn {
  width: 100%; padding: 0.6rem; background: #007bff; color: white;
  border: none; border-radius: 4px; cursor: pointer; transition: background 0.2s ease; font-size: 0.9rem;
}
.details-btn:hover { background: #0056b3; }

.status-message { text-align: center; padding: 2rem; font-size: 1.1rem; color: #6c757d; }
.error { color: #dc3545; } /* General error color */

</style>

