<template>
  <div>
    <h2>Add new POI</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="description"></textarea>
      </div>
      <div class="form-group">
        <label for="city">City:</label>
        <select v-model="city" id="city">
          <option v-for="city in cities" :key="city.id" :value="city.id">
            {{ city.name }} ({{ city.country.name }})
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="latitude">Latitude:</label>
        <input type="text" id="latitude" v-model="latitude" />
      </div>
      <div class="form-group">
        <label for="longitude">Longitude:</label>
        <input type="text" id="longitude" v-model="longitude" />
      </div>
      <div class="form-group">
        <label for="opening_hours">Opening Hours:</label>
        <input type="text" id="opening_hours" v-model="opening_hours" />
      </div>
      <div class="button-container">
        <button type="submit" class="primary">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      name: "",
      description: "",
      cities: [],
      location_latitude: "",
      location_longitude: "",
      opening_hours: "",
    };
  },
  created() {
    this.fetchCities();
  },
  methods: {
    fetchCities() {
      apiClient
        .get("http://localhost:8000/locations/cities/")
        .then((response) => {
          this.cities = response.data;
        })
        .catch((error) => {
          console.error("Error fetching cities:", error);
        });
    },
    submitForm() {
      const poiData = {
        name: this.name,
        description: this.description,
        city: this.city,
        location_latitude: this.latitude,
        location_longitude: this.longitude,
        opening_hours: this.opening_hours,
      };
      apiClient
        .post("http://localhost:8000/locations/pois/", poiData)
        .then((response) => {
          console.log("New POI created:", response.data);
          this.$emit("add-poi", response.data);
          this.$emit("close-popup");
        })
        .catch((error) => {
          console.error("Error creating POI:", error);
        });
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  cursor: pointer;
}

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
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
</style>
