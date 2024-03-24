<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">
        <span class="headline">Trip {{ trip.name }}</span>
      </v-card-title>
      <v-card-text>
  <div v-if="trip">
    <h2>{{ trip.name }}</h2>
    <div><b>From:</b> {{ trip.start_date }}</div>
    <div><b>To:</b> {{ trip.end_date }}</div>
    <div><b>Duration:</b> {{ trip.trip_length }}</div>
    <div v-if="trip.organizer"><b>Organizer:</b> {{ trip.organizer.first_name }} {{ trip.organizer.last_name }}</div>
    <div>
      <h3>Participants:</h3>
      <ul>
        <li v-for="participant in trip.participants" :key="participant.participant">
          {{ participant.first_name }} {{ participant.last_name }}
        </li>
      </ul>
    </div>
    <div>
      <h3>Points of Interest:</h3>
      <ul>
        <li v-for="poi in trip.pois" :key="poi.name">
          {{ poi.name }} - {{ poi.city.name }}
        </li>
      </ul>
    </div>
    <div>
      <h3>Accommodations:</h3>
      <ul>
        <li v-for="accommodation in trip.accommodations" :key="accommodation.id">
          {{ accommodation.name }} - {{ accommodation.location }} - {{ accommodation.details }}
        </li>
      </ul>
    </div>
    <div>
      <h3>Transportations:</h3>
      <ul>
        <li v-for="transportation in trip.transportations" :key="transportation.id">
          {{ transportation.name }} - {{ transportation.departure_location }} to {{ transportation.arrival_location }}
        </li>
      </ul>
    </div>
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
      trip: {},
    };
  },
  created() {
    this.fetchTrip();
  },
  methods: {
    fetchTrip() {
      const tripId = this.$route.params.id;
      apiClient
        .get(`http://localhost:8000/trip/trips/${tripId}/`)
        .then((response) => {
          this.trip = response.data;
        })
        .catch((error) => {
          console.error("Error fetching trip:", error);
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

</style>