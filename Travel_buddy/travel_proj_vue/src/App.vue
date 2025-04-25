<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Home</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
       <div class="navbar-end">
         <router-link to="/flights" class="navbar-item">Flights</router-link>
         <router-link to="/cities" class="navbar-item">Cities</router-link>
         <router-link to="/car" class="navbar-item">Car Rentals</router-link>
         <router-link to="/Attractions" class="navbar-item">Attractions</router-link>
         <router-link to="/Terrain" class="navbar-item">Terrain Condition</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <router-link to="/login" class="button is-light">Log in</router-link>
              <router-link to="/signup" class="button is-primary">Sign up</router-link>  <router-link to="/my-bookings" class="button is-success">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>MyBookings</span>
              </router-link>
            </div>
          </div>
       </div>
      </div>
    </nav>

     <section class="hero is-info is-bold">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">Your Next Adventure, One Click Away.</h1>
          <h2 class="subtitle">Don't know youre Travel plans, don't worry we've got you</h2>
        </div>
      </div>
    </section>



    <section class="section">
     <router-view/>  
    </section>

    <footer class="footer">
     <p class="has-text-centered">Copyright (c) 2025</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMobileMenu: false,
      }
    }
}
</script>

<style lang="scss">
@import 'bulma';
</style>

     