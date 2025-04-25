import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import FlightView from '../views/FlightView.vue' // Import the FlightView page
import CitiesView from '../views/CitiesView.vue' // Import the CitiesView page
import RentalCarsView from '../views/RentalCarsView.vue' // Import the RentalCarsView page
import TerrainView from '../views/TerrainView.vue' // Import the TerrainView page
import MyBookingsView from '../views/MyBookingsView.vue' // Import the MyBookingsView page
import LoginView from '../components/LoginView.vue';// Import the LoginView page
import SignupView from '../components/SignupView.vue';// Import the SignupView page
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ResetPasswordConfirmView from '../views/ResetPasswordConfirmView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/flights', // Add the flight route here
    name: 'flights',
    component: FlightView
  },
  {
    path: '/cities',
    name: 'cities',
    component: CitiesView // This will now display the list of cities
  },
  {
    path: '/car',
    name: 'car',
    component: RentalCarsView // This will now display the list of rental cars
  },
  {
    path: '/Terrain', // This matches the <router-link to="/Terrain"> in your App.vue
    name: 'Terrain',
    component: TerrainView, // This is the component that will be rendered
  },
  {
    path: '/my-bookings',
    name: 'MyBookings',
    component: MyBookingsView
  },
  {
    path: '/login',
    name: 'login', // Add the name property
    component: LoginView
  },
  {
    path: '/signup',  // Add this route for SignupView
    component: SignupView
  },
  { path: '/forgot-password', 
    name: 'forgot-password', 
    component: ForgotPasswordView 
  },
  { path: '/password/reset/confirm/:uid/:token', 
    name: 'password-reset-confirm', 
    component: ResetPasswordConfirmView 
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Optional: Add navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('access_token'); // Basic check

  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    // Redirect to login page if trying to access a protected route without being logged in
    next({ name: 'login', query: { redirect: to.fullPath } }); // Optionally pass redirect query
  } else {
    next(); // Proceed as normal
  }
});

export default router
