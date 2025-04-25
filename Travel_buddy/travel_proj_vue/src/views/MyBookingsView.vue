<template>
  <div class="my-bookings-container">
    <!-- Updated title -->
    <h1 class="page-title">My Bookings</h1>

    <!-- Loading State -->
    <div v-if="loading" class="status-message">Loading your bookings...</div>

    <!-- Error State -->
    <div v-else-if="error" class="status-message error">
      {{ error }}
      <button v-if="error.includes('log in')" @click="$router.push('/login')" class="retry-button">
        Log In
      </button>
      <button v-else @click="fetchAllBookings" class="retry-button"> <!-- Changed method name -->
        Retry
      </button>
    </div>

    <!-- Empty Bookings State -->
    <div v-else-if="allBookings.length === 0" class="status-message"> <!-- Changed variable name -->
      You have no bookings yet.
    </div>

    <!-- Bookings Grid -->
    <div v-else class="bookings-grid">
      <!-- Loop through COMBINED and SORTED bookings -->
      <div v-for="(booking, index) in sortedBookings" :key="`${booking.type}-${booking.id}`" class="booking-card"> <!-- Use type in key -->
        <!-- Dynamic Title -->
        <h2 class="booking-title">
          {{ booking.type === 'flight' ? 'Flight' : 'Car' }} Booking #{{ booking.id }}
        </h2>

        <!-- Common Status Display -->
        <p><strong>Status:</strong>
           <span :class="booking.is_cancelled ? 'status-cancelled' : 'status-confirmed'">
             {{ booking.is_cancelled ? 'Cancelled' : 'Confirmed' }}
           </span>
        </p>

        <!-- Flight Booking Details -->
        <div v-if="booking.type === 'flight'" class="booking-details">
          <p><strong>Booked By:</strong> {{ booking.passenger_name || '(Name not provided)' }}</p>
          <p><strong>Email:</strong> {{ booking.passenger_email || 'N/A' }}</p>
          <p><strong>Contact Phone:</strong> {{ booking.passenger_phone_number || 'N/A' }}</p>
          <hr class="details-divider"> <!-- Optional separator -->
          <p><strong>Flight:</strong> {{ booking.flight_info || 'N/A' }}</p>
          <p><strong>Booking Date:</strong> {{ formatDate(booking.booking_date) }}</p>
          <p><strong>Total Price:</strong> Ksh {{ formatPrice(booking.total_price) }}</p>
          <p><strong>Seats Booked:</strong> {{ booking.seats_booked || (booking.seats_detail ? booking.seats_detail.length : 0) }}</p>
          <div v-if="booking.seats_detail && booking.seats_detail.length > 0" class="seat-details">
            <strong>Seats:</strong>
            <ul> <li v-for="seat in booking.seats_detail" :key="seat.id"> {{ seat.seat_number }} ({{ seat.seat_class_name }}) </li> </ul>
          </div>
          <p v-else-if="!booking.is_cancelled">No seat details available.</p>
          <!-- Flight Cancel Button -->
          <button v-if="!booking.is_cancelled" @click="cancelFlightBooking(booking.id, index)" class="cancel-button" :disabled="cancellingId === booking.id">
            {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel Flight' }}
          </button>
          <p v-if="cancelError && cancellingId === booking.id" class="error cancel-error"> {{ cancelError }} </p>
        </div>

        <!-- Car Booking Details -->
        <div v-if="booking.type === 'car'" class="booking-details">
           <p><strong>Booked By:</strong> {{ booking.passenger_name || '(Name not provided)' }}</p>
           <p><strong>Email:</strong> {{ booking.passenger_email || 'N/A' }}</p>
           <p><strong>Contact Phone:</strong> {{ booking.passenger_phone_number || 'N/A' }}</p>
           <hr class="details-divider"> <!-- Optional separator -->
           <p><strong>Car:</strong> {{ booking.car_details?.name || 'N/A' }} ({{ booking.car_details?.company }})</p>
           <p><strong>City:</strong> {{ booking.car_details?.city_name || 'N/A' }}</p>
           <p><strong>Pickup:</strong> {{ formatDate(booking.start_date) }}</p>
           <p><strong>Return:</strong> {{ formatDate(booking.end_date) }}</p>
           <p><strong>Total Price:</strong> Ksh {{ formatPrice(booking.total_price) }}</p>
           <p><strong>Booked On:</strong> {{ formatDate(booking.booking_date) }}</p>
           <!-- Car Cancel Button -->
           <button v-if="!booking.is_cancelled" @click="cancelCarBooking(booking.id, index)" class="cancel-button cancel-button-car" :disabled="cancellingId === booking.id">
             {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel Car' }}
           </button>
           <p v-if="cancelError && cancellingId === booking.id" class="error cancel-error"> {{ cancelError }} </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MyBookingsView',
  data() {
    return {
      allBookings: [], // Combined list from both APIs
      loading: true,
      error: null,
      cancellingId: null, // Store just the ID of the booking being cancelled
      cancelError: null,
    };
  },
  computed: {
      // Sort combined bookings by booking date, newest first
      sortedBookings() {
          // Create a shallow copy before sorting to avoid mutating original array if needed elsewhere
          return [...this.allBookings].sort((a, b) => new Date(b.booking_date) - new Date(a.booking_date));
      }
  },
  methods: {
    // Renamed fetch method to fetch all types
    async fetchAllBookings() {
      this.loading = true;
      this.error = null;
      this.cancelError = null;
      this.cancellingId = null;
      const token = localStorage.getItem('access_token');

      if (!token) {
        this.error = 'You must be logged in to view your bookings.';
        this.loading = false;
        return;
      }

      const config = { headers: { Authorization: `Bearer ${token}` } };
      const flightBookingsUrl = 'http://127.0.0.1:8000/api/travel_buddy/bookings/';
      const carBookingsUrl = 'http://127.0.0.1:8000/api/travel_buddy/car-bookings/';

      try {
        // Fetch both types of bookings concurrently using Promise.all
        const [flightResponse, carResponse] = await Promise.all([
          axios.get(flightBookingsUrl, config)
               .catch(err => {
                   console.error("Error fetching flight bookings:", err.response?.data || err.message);
                   // Return an empty array on error so Promise.all doesn't reject immediately
                   return { data: [] };
               }),
          axios.get(carBookingsUrl, config)
               .catch(err => {
                   console.error("Error fetching car bookings:", err.response?.data || err.message);
                   // Return an empty array on error
                   return { data: [] };
               })
        ]);

        console.log('Flight Bookings fetched:', flightResponse.data);
        console.log('Car Bookings fetched:', carResponse.data);

        // Add type identifier and combine results
        const flightBookings = flightResponse.data.map(b => ({ ...b, type: 'flight' }));
        const carBookings = carResponse.data.map(b => ({ ...b, type: 'car' }));

        this.allBookings = [...flightBookings, ...carBookings];

        // Optional: Check if both requests failed or returned empty, maybe set a general error
        if (this.allBookings.length === 0 && !this.error) {
             // You could check the actual error objects if needed
             // console.log("No bookings found or errors occurred during fetch.");
             // No need to set error here, the "no bookings yet" message will show.
        }

      } catch (err) { // Catch errors not handled by individual catches (e.g., network error before requests)
        console.error('Generic error fetching all bookings:', err);
        // Handle potential 401 if token expires mid-request (less likely with Promise.all)
        if (err.response && err.response.status === 401) {
            this.error = 'Your session may have expired. Please log in again.';
        } else if (err.request) { // Network error
            this.error = 'Could not connect to the server. Please check your network and try again.';
        } else { // Other unexpected errors
            this.error = 'An unexpected error occurred while fetching bookings.';
        }
      } finally {
        this.loading = false;
      }
    },

    // Renamed cancel method specifically for flights
    async cancelFlightBooking(bookingId, index) {
        // Pass the index from the *sorted* list
        await this.performCancel(
            `http://127.0.0.1:8000/api/travel_buddy/bookings/${bookingId}/cancel/`,
            bookingId,
            index,
            'flight' // Pass type to find in original array
        );
    },

    // Added cancel method specifically for cars
    async cancelCarBooking(bookingId, index) {
        // Pass the index from the *sorted* list
        await this.performCancel(
            `http://127.0.0.1:8000/api/travel_buddy/car-bookings/${bookingId}/cancel/`,
            bookingId,
            index,
            'car' // Pass type to find in original array
        );
    },

    // Generic cancel helper method
    async performCancel(url, bookingId, sortedIndex, bookingType) {
       // Find the correct object in the source array `allBookings`
       // Using findIndex based on id and type is safer than relying on sortedIndex directly
       const originalIndex = this.allBookings.findIndex(b => b.id === bookingId && b.type === bookingType);

       if (originalIndex === -1) {
           console.error("Could not find booking in original list for cancellation update.");
           this.cancelError = "Could not update booking status locally.";
           // Reset cancellingId if it was set for this button
           if (this.cancellingId === bookingId) this.cancellingId = null;
           return;
       }

       if (!confirm(`Are you sure you want to cancel this ${bookingType} booking? This action cannot be undone.`)) {
         return;
       }
       this.cancellingId = bookingId; // Use ID to disable the correct button
       this.cancelError = null; // Reset error specific to this attempt

       try {
         const token = localStorage.getItem('access_token');
         if (!token) {
            this.error = 'You must be logged in to cancel bookings.';
            this.cancellingId = null;
            return;
         }

         // Make the API call
         await axios.post(url, {}, { headers: { Authorization: `Bearer ${token}` } });

         // --- Success: Update local state in the source array ---
         const updatedBooking = { ...this.allBookings[originalIndex], is_cancelled: true };
         // Replace the object in the source array to trigger reactivity
         this.allBookings[originalIndex] = updatedBooking;
         // The computed property 'sortedBookings' will automatically reflect the change.

       } catch (err) {
         console.error(`Error cancelling ${bookingType} booking ${bookingId} at ${url}:`, err.response?.data || err.message);
         // Keep existing detailed error handling
          if (err.response && err.response.data && err.response.data.message) {
              this.cancelError = err.response.data.message;
          } else if (err.response && err.response.status === 401) {
             this.error = 'Session expired. Please log in again to cancel bookings.'; // Show general error
          } else if (err.response && err.response.status === 404) {
              this.cancelError = 'Could not find this booking to cancel.';
          } else if (err.response && err.response.status === 403) {
              this.cancelError = 'You do not have permission to cancel this booking.';
          } else {
             this.cancelError = 'Failed to cancel the booking. Please try again.';
          }
       } finally {
         // Only reset cancellingId if it matches the one we were processing
         if (this.cancellingId === bookingId) {
             this.cancellingId = null;
         }
       }
     },

    // --- Helper methods for formatting ---
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      try {
        // Consistent date formatting
        const options = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true };
        return new Date(dateString).toLocaleString(undefined, options);
      } catch (e) {
        console.error("Error formatting date:", dateString, e);
        return dateString; // Fallback to original string
      }
    },
    formatPrice(price) {
        if (price == null || isNaN(price)) return 'N/A';
        return parseFloat(price).toFixed(2);
    },
  },
  mounted() {
    this.fetchAllBookings(); // Call the updated fetch method
  },
};
</script>

<style scoped>
/* Add specific styles if needed */
.details-divider {
    border: none;
    border-top: 1px dashed #eee;
    margin: 1rem 0;
}
.cancel-button-car {
    background-color: #ffc107; /* Example: Yellow for cars */
    color: #212529;
}
.cancel-button-car:hover:not(:disabled) {
    background-color: #e0a800;
}
.cancel-button-car:disabled {
    background-color: #fff3cd;
}

/* --- Existing Styles --- */
.my-bookings-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: sans-serif;
}

.page-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: bold;
}

.status-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #7f8c8d;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-top: 1rem;
}

.error {
  color: #e74c3c;
  background-color: #fdeded;
  border: 1px solid #f5c6cb;
  /* Ensure inline errors don't have background/border */
}
.booking-card .error.cancel-error {
    background-color: transparent;
    border: none;
    padding: 0;
    margin-top: 0.5rem;
}


.retry-button {
  margin-left: 1rem;
  margin-top: 0.5rem;
  padding: 0.6rem 1.2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.retry-button:hover {
  background-color: #0056b3;
}

.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.booking-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
}

.booking-title {
  font-size: 1.3rem;
  color: #343a40;
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
  word-wrap: break-word; /* Prevent long titles overflowing */
}

.booking-details {
    flex-grow: 1;
}

.booking-details p {
  margin: 0.6rem 0;
  color: #495057;
  line-height: 1.5;
  word-wrap: break-word; /* Prevent long details overflowing */
}

.booking-details strong {
    color: #212529;
}

.status-confirmed {
  color: #28a745;
  font-weight: bold;
}

.status-cancelled {
  color: #dc3545;
  font-weight: bold;
}

.seat-details {
  margin-top: 1rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #eee;
}

.seat-details strong {
    display: block;
    margin-bottom: 0.5rem;
}

.seat-details ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.seat-details li {
  background-color: #e9f5ff;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  margin-bottom: 0.3rem;
  display: inline-block;
  margin-right: 0.4rem;
  font-size: 0.9rem;
}

.cancel-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #dc3545; /* Default red for flight */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  align-self: flex-start;
}

.cancel-button:hover:not(:disabled) {
  background-color: #c82333; /* Darker red */
}

.cancel-button:disabled {
  background-color: #f8d7da;
  cursor: not-allowed;
}

.cancel-error {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #e74c3c;
    text-align: left;
}
</style>


