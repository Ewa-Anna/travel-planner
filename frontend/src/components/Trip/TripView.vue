<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">
        <span class="headline">Trips</span>
      </v-card-title>
      <v-card-text>
        <div class="button-container">
          <v-btn @click="sortTrips('name')" class="order-button"
            >Order by Name</v-btn
          >
          <v-btn @click="sortTrips('start_date')" class="order-button"
            >Order by Start Date</v-btn
          >
          <v-btn @click="sortTrips('end_date')" class="order-button"
            >Order by End Date</v-btn
          >
        </div>
        <v-select
          v-model="filterBy"
          :items="filterOptions"
          label="Filter by"
          dense
          outlined
        ></v-select>

        <div class="trip-row">
          <div v-for="trip in filteredTrips" :key="trip.id" class="trip-item">
            <router-link :to="'/trips/' + trip.id" class="trip-link">
              <div class="trip-name">{{ trip.name }}</div>
              <div class="trip-info">
                <div class="trip-date">Start date: {{ trip.start_date }}</div>
                <div class="trip-date">End date: {{ trip.end_date }}</div>
              </div>
            </router-link>
          </div>
        </div>
      </v-card-text>
    </v-card>
    <!-- <v-pagination v-model="page" :length="totalPages" @click="fetchTrips"></v-pagination> -->
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      trips: [],
      filterBy: null,
      filterOptions: ["All", "Current", "Upcoming", "Past"],
      // page: 1,
      // totalPages: 1,
      // itemsPerPage: 9,
      // nextUrl: null,
      // prevUrl: null,
    };
  },
  created() {
    this.fetchTrips();
  },
  methods: {
    fetchTrips(orderBy) {
      apiClient
        .get("http://localhost:8000/trip/trips/", {
          params: {
            order_by: orderBy,
          },
        })
        .then((response) => {
          this.trips = response.data.results;
          // this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
          // this.nextUrl = response.data.next;
          // this.prevUrl = response.data.previous;
        })
        .catch((error) => {
          console.error("Error fetching trips:", error);
        });
    },
    // nextPage() {
    //   if (this.nextUrl) {
    //     this.page++;
    //     this.fetchTrips();
    //   }
    // },
    // prevPage() {
    //   if (this.prevUrl) {
    //     this.page--;
    //     this.fetchTrips();
    //   }
    // },
    sortTrips(orderBy) {
      this.fetchTrips(orderBy);
    },
    filterTrips() {
      switch (this.filterBy) {
        case "All":
          return this.trips;
        case "Upcoming":
          return this.trips.filter(
            (trip) => new Date(trip.start_date) > new Date(),
          );
        case "Past":
          return this.trips.filter(
            (trip) => new Date(trip.end_date) < new Date(),
          );
        case "Current":
          return this.trips.filter(
            (trip) =>
              new Date(trip.start_date) < new Date() &&
              new Date(trip.end_date) > new Date(),
          );
        default:
          return this.trips;
      }
    },
  },
  computed: {
    filteredTrips() {
      return this.filterTrips();
    },
  },
};
</script>

<style>
.primary {
  background-color: #1976d2;
  color: white;
}

.trip-list {
  display: flex;
  flex-wrap: wrap;
}

.trip-item {
  width: calc(33.33% - 20px);
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  transition: transform 0.4s;
}

.trip-link {
  text-decoration: none;
}

.trip-name {
  color: #666;
  font-weight: bold;
  display: flex;
  justify-content: center;
  transition: transform 0.2s;
}

.trip-item:hover {
  transform: scale(1.1);
}

.trip-info {
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
}

.trip-date {
  color: #666;
}

.button-container {
  display: flex;
  justify-content: center;
}

.order-button {
  margin: 10px;
}

.trip-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
</style>
