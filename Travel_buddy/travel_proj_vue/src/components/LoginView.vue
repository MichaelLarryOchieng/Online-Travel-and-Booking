<template>
  <div>
    <h2 class="login-heading">Log In</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username" class="login-label">Username:</label>
        <input type="text" id="username" v-model="username" required class="login-input">
      </div>
      <div class="form-group">
        <label for="password" class="login-label">Password:</label>
        <input type="password" id="password" v-model="password" required class="login-input">
      </div>
      <button type="submit" class="login-button">Log In</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p class="forgot-password-link">
      <router-link to="/forgot-password" class="forgot-password-link-text">Forgot Password?</router-link>
    </p>
    <p class="signup-link">
      Don't have an account?
      <router-link to="/signup" class="signup-link-text">Sign up</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
methods: {
  async login() {
    this.error = null;
    if (!this.username || !this.password) {
      this.error = 'Username and password are required.';
      return;
    }
    try {
      const response = await axios.post('/api/travel_buddy/accounts/login/', {
        username: this.username,
        password: this.password,
      });

      // Store tokens in localStorage
      localStorage.setItem('access_token', response.data.access || response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh || response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user || {}));

      // Redirect to the home page or dashboard
      this.$router.push('/');
    } catch (error) {
      console.error('Login error:', error); // Log the error for debugging
      this.error = error.response
        ? error.response.data.detail || 'Login failed. Please check your credentials.'
        : 'Login failed. Please check your credentials.';
    }
  },
},
};
</script>

<style scoped lang="scss">
/* scoped means these styles apply only to this component  */
.login-heading {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}
.login-form {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
.login-label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}
.login-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.login-button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
}
.error {
  color: red;
  margin-top: 10px;
}
.signup-link {
  margin-top: 15px;
  text-align: center;
}
.signup-link-text {
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
  .forgot-password-link {
  margin-top: 10px;
  text-align: center;
  font-size: 0.9em; /* Slightly smaller */
}
.forgot-password-link-text {
  color: #6c757d; /* Grey color */
  text-decoration: none;
  &:hover {
    text-decoration: underline;
    color: #0056b3; /* Darker blue on hover */
  }
}
}
</style>

