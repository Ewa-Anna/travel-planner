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

        <label for="participants">Participants:</label>
        <input
          type="text"
          v-model="userQuery"
          @input="fetchUsers(userQuery)"
          placeholder="Search Users"
        />

        <div id="scroll-form-group" class="form-group">
          <div v-for="user in users" :key="user.id">
            <label>
              <input
                type="checkbox"
                v-model="formData.participants"
                :value="user.id"
              />
              {{ user.first_name }} {{ user.last_name }} ({{ user.username }})
            </label>
          </div>
        </div>

        <label for="pois">POIs:</label>
        <input
          type="text"
          v-model="poiQuery"
          @input="fetchPOIs(poiQuery)"
          placeholder="Search POIs"
        />
        <div id="scroll-form-group" class="form-group">
          <div v-for="poi in pois" :key="poi.id">
            <label>
              <input type="checkbox" v-model="formData.pois" :value="poi.id" />
              {{ poi.name }}
            </label>
          </div>
        </div>

        <label for="accommodations">Accommodations:</label>
        <input
          type="text"
          v-model="accQuery"
          @input="fetchAccommodations(accQuery)"
          placeholder="Search Accommodations"
        />
        <div id="scroll-form-group" class="form-group">
          <div v-for="accommodation in accommodations" :key="accommodation.id">
            <label>
              <input
                type="checkbox"
                v-model="formData.accommodations"
                :value="accommodation.id"
              />
              {{ accommodation.name }}
            </label>
          </div>
        </div>

        <label for="transportations">Transportations:</label>
        <input
          type="text"
          v-model="transpQuery"
          @input="fetchTransportations(transpQuery)"
          placeholder="Search Transportations"
        />
        <div id="scroll-form-group" class="form-group">
          <div
            v-for="transportation in transportations"
            :key="transportation.id"
          >
            <label>
              <input
                type="checkbox"
                v-model="formData.transportations"
                :value="transportation.id"
              />
              {{ transportation.name }}
            </label>
          </div>
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
    this.fetchUsers();
    this.fetchPOIs();
    this.fetchAccommodations();
    this.fetchTransportations();
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
    fetchUsers(query = "") {
      const url = query
        ? `http://localhost:8000/authx/users/?query=${query}`
        : "http://localhost:8000/authx/users/";

      apiClient
        .get(url)
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
    fetchPOIs(query = "") {
      const url = query
        ? `http://localhost:8000/locations/pois/?query=${query}`
        : "http://localhost:8000/locations/pois/";
      apiClient
        .get(url)
        .then((response) => {
          this.pois = response.data;
        })
        .catch((error) => {
          console.error("Error fetching POIs:", error);
        });
    },
    fetchAccommodations(query = "") {
      const url = query
        ? `http://localhost:8000/services/accommodations/?query=${query}`
        : "http://localhost:8000/services/accommodations/";
      apiClient
        .get(url)
        .then((response) => {
          this.accommodations = response.data;
        })
        .catch((error) => {
          console.error("Error fetching accommodations:", error);
        });
    },
    fetchTransportations(query = "") {
      const url = query
        ? `http://localhost:8000/services/transportations/?query=${query}`
        : "http://localhost:8000/services/transportations/";
      apiClient
        .get(url)
        .then((response) => {
          this.transportations = response.data;
        })
        .catch((error) => {
          console.error("Error fetching transportations:", error);
        });
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

#scroll-form-group {
  max-height: 200px;
  overflow-y: auto;
}
</style>
