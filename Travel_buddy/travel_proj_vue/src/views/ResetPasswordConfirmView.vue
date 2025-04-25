<template>
  <div class="reset-confirm-container">
    <h2 class="page-heading">Set New Password</h2>
    <form @submit.prevent="confirmReset" class="reset-confirm-form">
      <div class="form-group">
        <label for="new_password" class="form-label">New Password:</label>
        <input type="password" id="new_password" v-model="new_password" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="re_new_password" class="form-label">Confirm New Password:</label>
        <input type="password" id="re_new_password" v-model="re_new_password" required class="form-input" />
      </div>
      <button type="submit" class="submit-button" :disabled="loading">
        {{ loading ? 'Resetting...' : 'Reset Password' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </form>
     <p v-if="success" class="login-link">
      <router-link to="/login" class="login-link-text">Log In Now</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ResetPasswordConfirmView',
  data() {
    return {
      new_password: '',
      re_new_password: '',
      loading: false,
      error: null,
      success: null,
      uid: null, // To store uid from route params
      token: null, // To store token from route params
    };
  },
  created() {
    // Get uid and token from the route parameters when the component is created
    this.uid = this.$route.params.uid;
    this.token = this.$route.params.token;
    if (!this.uid || !this.token) {
        this.error = "Invalid password reset link. Please request a new one.";
        // Optionally redirect or disable form
    }
  },
  methods: {
    async confirmReset() {
      if (this.new_password !== this.re_new_password) {
        this.error = 'Passwords do not match.';
        return;
      }
      if (!this.uid || !this.token) {
          this.error = "Invalid password reset link. Cannot proceed.";
          return;
      }

      this.loading = true;
      this.error = null;
      this.success = null;

      try {
        // Use Djoser's password reset confirmation endpoint
        await axios.post('/api/travel_buddy/users/reset_password_confirm/', {
          uid: this.uid,
          token: this.token,
          new_password: this.new_password,
          re_new_password: this.re_new_password,
        });
        this.success = 'Password has been reset successfully! You can now log in with your new password.';
        // Clear form fields
        this.new_password = '';
        this.re_new_password = '';
        // Optionally redirect after a delay
        // setTimeout(() => { this.$router.push('/login'); }, 3000);
      } catch (err) {
        console.error('Password reset confirmation error:', err.response || err);
         if (err.response && err.response.data) {
          // Try to extract specific errors from Djoser (e.g., invalid token, password too common)
          this.error = Object.values(err.response.data).flat().join(' ') || 'Failed to reset password. The link might be invalid or expired.';
        } else {
          this.error = 'Failed to reset password. Please try again later.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
/* Styles similar to ForgotPasswordView */
.reset-confirm-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
}

.page-heading {
  font-size: 24px;
  margin-bottom: 1.5rem; /* More space */
  color: #333;
}

.reset-confirm-form {
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
  background-color: #28a745; /* Green */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;

  &:hover:not(:disabled) {
    background-color: #218838;
  }

  &:disabled {
    background-color: #94d3a2;
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

.login-link {
  margin-top: 1.5rem;
}

.login-link-text {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
  &:hover {
    text-decoration: underline;
  }
}
</style>
