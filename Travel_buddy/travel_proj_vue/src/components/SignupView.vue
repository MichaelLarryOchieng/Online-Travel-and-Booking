    <template>
      <div>
        <h2 class="signup-heading">Sign Up</h2>
        <form @submit.prevent="signup" class="signup-form">
          <!-- Username -->
          <div class="form-group">
            <label for="username" class="signup-label">Username:</label>
            <input type="text" id="username" v-model="username" required class="signup-input" />
          </div>
          <!-- First Name -->
          <div class="form-group">
            <label for="first_name" class="signup-label">First Name:</label>
            <input type="text" id="first_name" v-model="first_name" class="signup-input" />
          </div>
          <!-- Last Name -->
          <div class="form-group">
            <label for="last_name" class="signup-label">Last Name:</label>
            <input type="text" id="last_name" v-model="last_name" class="signup-input" />
          </div>
          <!-- Email -->
          <div class="form-group">
            <label for="email" class="signup-label">Email:</label>
            <input type="email" id="email" v-model="email" required class="signup-input" />
          </div>
          <!-- Phone Number -->
          <div class="form-group">
            <label for="phone_number" class="signup-label">Phone Number:</label>
            <input type="text" id="phone_number" v-model="phone_number" class="signup-input" />
          </div>
          <!-- Password -->
          <div class="form-group">
            <label for="password" class="signup-label">Password:</label>
            <input type="password" id="password" v-model="password" required class="signup-input" />
          </div>
          <button type="submit" class="signup-button">Sign Up</button>
          <p v-if="error" class="error">{{ error }}</p>
          <p v-if="success" class="success">{{ success }}</p>
        </form>
        <!-- Login Link -->
        <p class="login-link">
          Already have an account?
          <router-link to="/login" class="login-link-text">Log in</router-link>
        </p>
      </div>
    </template>

    <script>
    import axios from 'axios';

    export default {
      data() {
        return {
          username: '',
          email: '',
          password: '',
          first_name: '', // Added
          last_name: '',  // Added
          phone_number: '',
          error: null,
          success: null,
        };
      },
      methods: {
        async signup() {
          this.error = null;
          this.success = null;
          try {
            // --- Use Djoser's default user creation URL ---
            // If you customized it, use your custom URL
            const response = await axios.post('/api/travel_buddy/users/', { // CHECK THIS URL
              username: this.username,
              email: this.email,
              password: this.password,
              first_name: this.first_name, 
              last_name: this.last_name,
              phone_number: this.phone_number,
            });
            this.success = 'Signup successful! You can now log in.';
            this.username = ''; /* ... clear other fields ... */
            this.phone_number = '';
            setTimeout(() => { this.$router.push('/login'); }, 1500);

          } catch (error) { /* ... error handling ... */ }
        },
      },
    };
    </script>

<style scoped lang="scss">
.signup-heading {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}
.signup-form {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
.signup-label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}
.signup-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.signup-button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: #218838;
  }
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
.login-link {
  margin-top: 15px;
  text-align: center;
}
.login-link-text {
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
}
</style>
