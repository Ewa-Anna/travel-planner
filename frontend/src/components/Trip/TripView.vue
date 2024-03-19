<template>
  <div>
    <div v-for="trip in trips" :key="trip.id">
      {{ trip.name }} 
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      trips: []
    };
  },
  created() {
    this.fetchTrips();
  },
  methods: {
    fetchTrips() {
      axios.get('http://localhost:8000/trip/trips/')
        .then(response => {
          this.trips = response.data;
        })
        .catch(error => {
          console.error('Error fetching trips:', error);
        });
    }
  }
}
</script>
