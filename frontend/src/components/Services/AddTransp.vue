<template>
  <div>
    <h2>Add new Transportation</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="departure_location">Departure Location:</label>
        <input
          type="text"
          id="departure_location"
          v-model="departureLocation"
          required
        />
      </div>
      <div class="form-group">
        <label for="arrival_location">Arrival Location:</label>
        <input
          type="text"
          id="arrival_location"
          v-model="arrivalLocation"
          required
        />
      </div>
      <div class="form-group">
        <label for="departure_time">Departure Time:</label>
        <input
          type="datetime-local"
          id="departure_time"
          v-model="departureTime"
          required
        />
      </div>
      <div class="form-group">
        <label for="arrival_time">Arrival Time:</label>
        <input
          type="datetime-local"
          id="arrival_time"
          v-model="arrivalTime"
          required
        />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="description"></textarea>
      </div>
      <div class="form-group">
        <label for="price">Price:</label>
        <input type="text" id="price" v-model="price" required />
      </div>
      <div class="form-group">
        <label for="type">Type:</label>
        <select id="type" v-model="type" required>
          <option
            v-for="(label, value) in transportationTypes"
            :key="value"
            :value="value"
          >
            {{ label }}
          </option>
        </select>
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
      departureLocation: "",
      arrivalLocation: "",
      departureTime: "",
      arrivalTime: "",
      description: "",
      price: "",
      type: "",
      transportationTypes: {},
    };
  },
  mounted() {
    this.fetchTransportationTypes();
  },
  methods: {
    fetchTransportationTypes() {
      apiClient
        .get(
          "http://localhost:8000/analytics/dropdown-list/transportation_types",
        )
        .then((response) => {
          this.transportationTypes = response.data;
        })
        .catch((error) => {
          console.error("Error fetching transportation types", error);
        });
    },
    submitForm() {
      const transportationData = {
        name: this.name,
        departure_location: this.departureLocation,
        arrival_location: this.arrivalLocation,
        departure_time: this.departureTime,
        arrival_time: this.arrivalTime,
        description: this.description,
        price: this.price,
        type: this.type,
      };
      apiClient
        .post(
          "http://localhost:8000/services/transportations/",
          transportationData,
        )
        .then((response) => {
          console.log("New Transportation created:", response.data);
        })
        .catch((error) => {
          console.error("Error creating Transportation:", error);
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
