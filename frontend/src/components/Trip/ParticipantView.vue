// ParticipantTripsView.vue
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
      const participantId = this.$route.params.id;
      axios.get(`http://localhost:8000/trip/participants/${participantId}/trips/`)
        .then(response => {
          this.trips = response.data;
        })
        .catch(error => {
          console.error('Error fetching trips for participant:', error);
        });
    }
  }
}
</script>
