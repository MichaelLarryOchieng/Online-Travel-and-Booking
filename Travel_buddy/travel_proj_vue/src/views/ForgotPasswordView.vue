<template>
  <div class="forgot-password-container">
    <h2 class="page-heading">Forgot Password</h2>
    <p class="instructions">Enter your email address and we'll send you a link to reset your password.</p>
    <form @submit.prevent="requestReset" class="forgot-password-form">
      <div class="form-group">
        <label for="email" class="form-label">Email:</label>
        <input type="email" id="email" v-model="email" required class="form-input" />
      </div>
      <button type="submit" class="submit-button" :disabled="loading">
        {{ loading ? 'Sending...' : 'Send Reset Link' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </form>
     <p class="back-link">
      Remembered your password?
      <router-link to="/login" class="back-link-text">Log In</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ForgotPasswordView',
  data() {
    return {
      email: '',
      loading: false,
      error: null,
      success: null,
    };
  },
  methods: {
    async requestReset() {
      this.loading = true;
      this.error = null;
      this.success = null;
      try {
        // Use Djoser's password reset endpoint
        await axios.post('/api/travel_buddy/users/reset_password/', {
          email: this.email,
        });
        this.success = 'Password reset link sent! Please check your email (and spam folder).';
        this.email = ''; // Clear email field on success
      } catch (err) {
        console.error('Password reset request error:', err.response || err);
        if (err.response && err.response.data) {
          // Try to extract specific errors from Djoser
          this.error = Object.values(err.response.data).flat().join(' ') || 'Failed to send reset link. Please check the email address and try again.';
        } else {
          this.error = 'Failed to send reset link. Please try again later.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
.forgot-password-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
}

.page-heading {
  font-size: 24px;
  margin-bottom: 1rem;
  color: #333;
}

.instructions {
  margin-bottom: 1.5rem;
  color: #555;
  font-size: 0.95em;
}

.forgot-password-form {
  /* Styles similar to login/signup */
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Include padding in width */
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;

  &:hover:not(:disabled) {
    background-color: #0056b3;
  }

  &:disabled {
    background-color: #a0cfff;
    cursor: not-allowed;
  }
}

.error {
  color: red;
  margin-top: 1rem;
}

.success {
  color: green;
  margin-top: 1rem;
}

.back-link {
  margin-top: 1.5rem;
}

.back-link-text {
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
}
</style>
