<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <div class="text-body-2 font-weight-light mb-n1">Travel Planner</div>

      <div class="py-14" />
      <p class="message">Don't know where to start?</p>
      <router-link to="/addtrip" class="primary">Add your trip!</router-link>
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts"></script>

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
  font-size: 1.2rem;
  margin-bottom: 10px;
}
</style>
