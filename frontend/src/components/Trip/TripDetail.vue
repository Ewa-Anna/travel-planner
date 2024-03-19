<template>
  <div>
    <div>{{ trip.name }}</div> 
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      trip: {}
    };
  },
  created() {
    this.fetchTrip();
  },
  methods: {
    fetchTrip() {
      const tripId = this.$route.params.id;
      axios.get(`http://localhost:8000/trip/trips/${tripId}/`)
        .then(response => {
          this.trip = response.data;
        })
        .catch(error => {
          console.error('Error fetching trip:', error);
        });
    }
  }
}
</script>
