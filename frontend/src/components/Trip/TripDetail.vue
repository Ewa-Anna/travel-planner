<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title id="trip-title" class="primary">
        <span class="headline">Trip {{ trip.name }}</span>
        <router-link
          v-if="isOrganizer"
          :to="'/edittrip/' + trip.id"
          class="edit-trip"
          >Edit trip</router-link
        >
      </v-card-title>
      <v-card-text>
        <div v-if="trip" class="trip-details">
          <h2>{{ trip.name }}</h2>
          <div><b>From:</b> {{ trip.start_date }}</div>
          <div><b>To:</b> {{ trip.end_date }}</div>
          <div><b>Duration:</b> {{ trip.trip_length }}</div>
          <div v-if="trip.organizer">
            <b>Organizer:</b> {{ trip.organizer.first_name }}
            {{ trip.organizer.last_name }}
          </div>
          <div>
            <h3>Participants:</h3>
            <ul>
              <li
                v-for="participant in trip.participants"
                :key="participant.participant"
              >
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
              <li
                v-for="accommodation in trip.accommodations"
                :key="accommodation.id"
              >
                {{ accommodation.name }} - {{ accommodation.location }} -
                {{ accommodation.details }}
              </li>
            </ul>
          </div>
          <div>
            <h3>Transportations:</h3>
            <ul>
              <li
                v-for="transportation in trip.transportations"
                :key="transportation.id"
              >
                {{ transportation.name }} -
                {{ transportation.departure_location }} to
                {{ transportation.arrival_location }}
              </li>
            </ul>
          </div>
        </div>
        <!-- <Map :coordinates="trip.pois.map(poi => [poi.location_latitude, poi.location_longitude])"></Map> -->
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";
import Map from "../Map";

export default {
  components: {
    Map,
  },
  props: {
    trip: Object,
  },
  data() {
    return {
      pois: [],
      trip: {},
      currentUserId: null,
    };
  },
  computed: {
    isOrganizer() {
      return (
        this.trip.organizer && this.trip.organizer.id === this.currentUserId
      );
    },
  },
  created() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    } else {
      this.fetchTrip()
        .then(() => {
          if (this.isOrganizer) {
            return true;
          } else {
            console.log("You are not authorized to edit this trip.");
          }
        })
        .catch((error) => {
          console.error("Error fetching trip:", error);
        });
      apiClient
        .get("/authx/profile/")
        .then((response) => {
          const userId = response.data.user.id;
          this.currentUserId = userId;
        })
        .catch((error) => {
          console.error("Error getting current user:", error);
        });
    }
  },
  methods: {
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchTrip() {
      const tripId = this.$route.params.id;
      return apiClient
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

.trip-details h2 {
  margin-top: 20px;
  margin-bottom: 20px;
}

.trip-details div {
  margin-bottom: 10px;
}

.trip-details h3 {
  margin-top: 20px;
  margin-bottom: 10px;
}

.trip-details ul {
  list-style-type: none;
  padding: 0;
}

.trip-details li {
  margin-bottom: 5px;
}

#trip-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-trip {
  display: inline-block;
  background-color: #007bff;
  border-radius: 6px;
  padding: 8px 16px;
  border: none;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  padding: 8px;
}

.edit-trip:hover {
  text-decoration: none;
  background-color: #0056b3;
}
</style>
