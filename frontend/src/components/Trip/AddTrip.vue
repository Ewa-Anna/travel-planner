<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">Trip Details</v-card-title>

      <form @submit.prevent="submitForm" class="trip-form">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" required />
        </div>
        <div class="form-group">
          <label for="start_date">Start Date:</label>
          <input
            type="date"
            id="start_date"
            v-model="formData.start_date"
            required
          />
        </div>
        <div class="form-group">
          <label for="end_date">End Date:</label>
          <input
            type="date"
            id="end_date"
            v-model="formData.end_date"
            required
          />
        </div>
        <div class="form-group">
          <label for="participants">Participants:</label>
          <select id="participants" v-model="formData.participants" multiple>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="pois">POIs:</label>
          <select id="pois" v-model="formData.pois" multiple>
            <option v-for="poi in pois" :key="poi.id" :value="poi.id">
              {{ poi.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="accommodations">Accommodations:</label>
          <select
            id="accommodations"
            v-model="formData.accommodations"
            multiple
          >
            <option
              v-for="accommodation in accommodations"
              :key="accommodation.id"
              :value="accommodation.id"
            >
              {{ accommodation.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="transportations">Transportations:</label>
          <select
            id="transportations"
            v-model="formData.transportations"
            multiple
          >
            <option
              v-for="transportation in transportations"
              :key="transportation.id"
              :value="transportation.id"
            >
              {{ transportation.name }}
            </option>
          </select>
        </div>
        <button type="submit" class="primary">Submit</button>
      </form>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";
import { mapActions } from "vuex";
import Alert from "../../components/Utils/Alert.vue";

export default {
  components: {
    Alert,
  },
  data() {
    return {
      formData: {
        name: "",
        start_date: "",
        end_date: "",
        participants: [],
        pois: [],
        accommodations: [],
        transportations: [],
      },
      users: [],
      pois: [],
      accommodations: [],
      transportations: [],
    };
  },
  created() {
    this.checkAuthentication();
  },
  methods: {
    ...mapActions(["fetchTrips"]),

    checkAuthentication() {
      if (!this.isAuthenticated()) {
        this.$router.push("/login");
      }
    },
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    submitForm() {
      apiClient
        .post("http://localhost:8000/trip/trips/", this.formData)
        .then((response) => {
          console.log("Form data:", response.data);
          this.$router.push("/mytrips");
          this.emitter.emit("showAlert", {
            message: response.data.message,
            backgroundColor: "#4CAF50",
            textColor: "white",
          });
          this.formData = {
            name: "",
            start_date: "",
            end_date: "",
            participants: [],
            pois: [],
            accommodations: [],
            transportations: [],
          };
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
          this.emitter.emit("showAlert", {
            message: "An unexpected error occurred",
            backgroundColor: "#f44336",
            textColor: "white",
          });
        });
    },
  },
};
</script>

<style scoped>
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

.trip-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
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
</style>
