<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">
        <span class="headline">My Trips</span>
      </v-card-title>
      <v-card-text>
        <div v-for="trip in trips" :key="trip.id" class="trip-item">
          <router-link :to="'/trips/' + trip.id">{{ trip.name }}</router-link>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      trips: [],
    };
  },
  created() {
    this.fetchTrips();
  },
  methods: {
    fetchTrips() {
      const participantId = this.$route.params.id;
      apiClient
        .get(`http://localhost:8000/trip/participants/${participantId}/trips/`)
        .then((response) => {
          this.trips = response.data;
        })
        .catch((error) => {
          console.error("Error fetching trips for participant:", error);
        });
    },
  },
};
</script>


<style>
.primary {
  background-color: #1976d2;
  color: white;
}

.trip-item {
  margin-bottom: 16px;
}
</style>
