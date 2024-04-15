<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title id="trip-title" class="primary">
        <span class="headline">All Trips</span>
        <router-link to="/addtrip" class="new-trip">Add new trip</router-link>
      </v-card-title>

      <v-card-text>
        <div class="button-container">
          <v-btn
            @click="sortTrips('name')"
            :class="{ active: orderBy === 'name' }"
            class="order-button"
            >Order by Name</v-btn
          >
          <v-btn
            @click="sortTrips('start_date')"
            :class="{ active: orderBy === 'start_date' }"
            class="order-button"
            >Order by Start Date</v-btn
          >
          <v-btn
            @click="sortTrips('end_date')"
            :class="{ active: orderBy === 'end_date' }"
            class="order-button"
            >Order by End Date</v-btn
          >
        </div>
        <v-select
          v-model="filterBy"
          :items="filterOptions"
          label="Filter by date"
          dense
          outlined
        ></v-select>

        <div class="search-container">
          <v-text-field
            v-model="searchQuery"
            label="Search"
            outlined
          ></v-text-field>
          <v-btn @click="searchTrips" class="search-button">Search</v-btn>
          <v-btn @click="clearSearch" class="clear-button">Clear</v-btn>
        </div>

        <div v-if="filteredTrips.length === 0" class="no-trips-message">
          No matching trips found.
        </div>

        <div class="trip-row">
          <div v-for="trip in filteredTrips" :key="trip.id" class="trip-item">
            <router-link :to="'/trips/' + trip.id" class="trip-link">
              <div class="trip-name">{{ trip.name }}</div>
              <div class="trip-info">
                <div class="trip-date">Start date: {{ trip.start_date }}</div>
                <div class="trip-date">End date: {{ trip.end_date }}</div>
                <div class="trip-destination">
                  Destination:
                  <span
                    v-for="(city, index) in uniqueCities(trip.pois)"
                    :key="index"
                    >{{ city
                    }}<span v-if="index !== uniqueCities(trip.pois).length - 1"
                      >,
                    </span>
                  </span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </v-card-text>
    </v-card>
    <v-pagination
      v-model="page"
      :length="totalPages"
      :total-visible="4"
      @click="fetchTrips"
    ></v-pagination>
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
      page: 1,
      totalPages: 1,
      itemsPerPage: 9,
      orderBy: "name",
      searchQuery: "",
    };
  },
  created() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    } else {
      this.fetchTrips();
    }
  },
  methods: {
    uniqueCities(pois) {
      const cities = [];
      pois.forEach((poi) => {
        if (!cities.includes(poi.city.name)) {
          cities.push(poi.city.name);
        }
      });
      return cities;
    },
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchTrips(orderBy = "name", page = 1) {
      const limit = this.itemsPerPage;
      const offset = (this.page - 1) * limit;

      apiClient
        .get("http://localhost:8000/trip/trips/", {
          params: {
            limit: limit,
            offset: offset,
            order_by: this.orderBy,
            query: this.searchQuery,
          },
        })
        .then((response) => {
          this.trips = response.data.results;
          this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        })
        .catch((error) => {
          console.error("Error fetching trips:", error);
        });
    },
    sortTrips(orderBy) {
      this.orderBy = orderBy;
      this.fetchTrips(orderBy, this.page);
    },
    searchTrips() {
      this.fetchTrips(this.orderBy, this.page);
    },
    clearSearch() {
      this.searchQuery = "";
      this.fetchTrips(this.orderBy, this.page);
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
  watch: {
    searchQuery(newValue) {
      this.fetchTrips(this.orderBy, this.page);
    },
  },
};
</script>

<style>
.primary {
  background-color: #1976d2;
  color: white;
}

#trip-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.new-trip {
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

.new-trip:hover {
  text-decoration: none;
  background-color: #0056b3;
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

.trip-destination {
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
  justify-content: flex-start;
}

.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.search-button {
  margin-left: 16px;
}

.clear-button {
  margin-left: 8px;
}

.no-trips-message {
  margin-top: 16px;
  color: #888;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.order-button {
  color: gray;
}
.order-button.active {
  color: black;
}
</style>
