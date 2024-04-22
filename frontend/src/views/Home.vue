<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <div class="text-body-2 font-weight-light mb-n1">Travel Planner</div>
      <p class="message">Don't know where to start?</p>
      <router-link to="/addtrip" class="primary">Add your trip!</router-link>
      <p class="message">Here are some statistics:</p>
      <div class="statistics">
        <div class="statistics-item">
          <PopularCountries />
        </div>
        <div class="statistics-item">
          <PopularAccommodations />
        </div>
        <div class="statistics-item">
          <PopularPOIs />
        </div>
      </div>
      <TotalUsers />
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import PopularCountries from "@/components/Analytics/PopularCountries.vue";
import PopularAccommodations from "@/components/Analytics/PopularAccommodations.vue";
import PopularPOIs from "@/components/Analytics/PopularPOIs.vue";
import TotalUsers from "@/components/Analytics/TotalUsers.vue";
</script>

<style>
.primary {
  background-color: #1976d2;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 4px;
}

.primary:hover {
  background-color: #1565c0;
}

.message {
  margin-top: 50px;
  margin-bottom: 20px;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.statistics {
  margin: 20px;
  display: flex;
  justify-content: center;
}

.statistics-item {
  margin-right: 10px;
}
</style>
