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
          <label for="visibility"> Visibility: </label>
          <input type="checkbox" id="visibility" v-model="formData.visibility" />
          Public
        </div>
        <div class="form-group">
          <label for="start_date">Start Date:</label>
          <input type="date" id="start_date" v-model="formData.start_date" required />
        </div>
        <div class="form-group">
          <label for="end_date">End Date:</label>
          <input type="date" id="end_date" v-model="formData.end_date" required />
        </div>

        <label for="participants">Participants:</label>
        <input type="text" v-model="userQuery" @input="fetchUsers(userQuery)" placeholder="Search Users" />

        <p class="info">
          Your friends are not on the list? Don't forget to
          <a href="#" class="add-button">add them</a> and refresh the page!
        </p>

        <div id="scroll-form-group" class="form-group">
          <div v-for="user in users" :key="user.id">
            <label>
              <input type="checkbox" v-model="formData.participants" :value="user.id" />
              {{ user.first_name }} {{ user.last_name }} ({{ user.username }})
            </label>
          </div>
        </div>

        <label for="pois">POIs:</label>

        <input type="text" v-model="poiQuery" @input="fetchPOIs(poiQuery)" placeholder="Search POIs" />
        <select v-model="selectedCity" @change="fetchCityPOIs(selectedCity)">
          <option value="">All cities</option>
          <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }} ({{ city.country.name }})
          </option>
        </select>

        <div>
          <p class="info">
            Your POI is not on the list?
            <a href="#" @click.prevent="openAddPOIPopup" class="add-button">Add one</a>
          </p>
        </div>

        <div v-if="showAddPOIPopup" class="popup-overlay" @click="closeAddPOIPopup">
          <div class="popup-content" @click.stop>
            <AddPOI @add-poi="handleAddPOI" @close-popup="closeAddPOIPopup" />
          </div>
        </div>

        <div id="scroll-form-group" class="form-group">
          <div v-for="poi in pois" :key="poi.id">
            <label>
              <input type="checkbox" v-model="formData.pois" :value="poi.id" />
              {{ poi.name }} ({{ poi.city.name }})
            </label>
          </div>
        </div>

        <label for="accommodations">Accommodations:</label>
        <input type="text" v-model="accQuery" @input="fetchAccommodations(accQuery)"
          placeholder="Search Accommodations" />

        <div>
          <p class="info">
            Your accommodation is not on the list?
            <a href="#" @click.prevent="openAddAccPopup" class="add-button">Add one</a>
          </p>
        </div>

        <div v-if="showAddAccPopup" class="popup-overlay" @click="closeAddAccPopup">
          <div class="popup-content" @click.stop>
            <AddAcc @add-acc="handleAddAcc" @close-popup="closeAddAccPopup" />
          </div>
        </div>

        <div id="scroll-form-group" class="form-group">
          <div v-for="accommodation in accommodations" :key="accommodation.id">
            <div style="display: flex; align-items: center;">
              <label>
                <input type="checkbox" v-model="formData.accommodations" :value="accommodation.id" />
                {{ accommodation.name }} ({{ accommodation.checkin_date }} -
                {{ accommodation.checkout_date }})
              </label>
              <button @click="deleteAccommodation(accommodation.id)" style="margin-left: 10px;">
                <font-awesome-icon class="delete-text" icon="fa-regular fa-trash-can" />
              </button>
            </div>
          </div>
        </div>

        <label for="transportations">Transportations:</label>
        <input type="text" v-model="transpQuery" @input="fetchTransportations(transpQuery)"
          placeholder="Search Transportations" />

        <div>
          <p class="info">
            Your transportation is not on the list?
            <a href="#" @click.prevent="openAddTranspPopup" class="add-button">Add one</a>
          </p>
        </div>

        <div v-if="showAddTranspPopup" class="popup-overlay" @click="closeAddTranspPopup">
          <div class="popup-content" @click.stop>
            <AddTransp @add-transp="handleAddTransp" @close-popup="closeAddTranspPopup" />
          </div>
        </div>

        <div id="scroll-form-group" class="form-group">
          <div v-for="transportation in transportations" :key="transportation.id">
            <div style="display: flex; align-items: center;">
              <label>
                <input type="checkbox" v-model="formData.transportations" :value="transportation.id" />
                {{ transportation.name }}
              </label>
              <button @click="deleteTransportation(transportation.id)" style="margin-left: 10px;">
                <font-awesome-icon class="delete-text" icon="fa-regular fa-trash-can" />
              </button>
            </div>
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
import AddPOI from "../../components/Locations/AddPOI.vue";
import AddAcc from "../../components/Services/AddAcc.vue";
import AddTransp from "../../components/Services/AddTransp.vue";

export default {
  components: {
    Alert,
    AddPOI,
    AddAcc,
    AddTransp,
  },
  data() {
    return {
      cities: [],
      selectedCity: '',
      showAddPOIPopup: false,
      showAddAccPopup: false,
      showAddTranspPopup: false,
      formData: {
        name: "",
        start_date: "",
        end_date: "",
        visibility: true,
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
    this.fetchCities();
    this.fetchCityPOIs();
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
    fetchCityPOIs(cityName) {
      const url = cityName
        ? `http://localhost:8000/locations/pois/?city=${encodeURIComponent(cityName)}`
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
    async fetchCities() {
      try {
        const response = await apiClient.get('http://localhost:8000/locations/cities/', {
          headers: {
            'Accept': 'application/json'
          }
        });
        this.cities = response.data;
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },

    handleAddPOI(poi) {
      this.formData.pois.push(poi);
      this.closeAddPOIPopup();
      this.fetchPOIs();
    },
    openAddPOIPopup() {
      this.showAddPOIPopup = true;
    },
    closeAddPOIPopup() {
      this.showAddPOIPopup = false;
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

    handleAddAcc(accommodation) {
      this.formData.accommodations.push(accommodation);
      this.closeAddAccPopup();
      this.fetchAccommodations();
    },
    openAddAccPopup() {
      this.showAddAccPopup = true;
    },
    closeAddAccPopup() {
      this.showAddAccPopup = false;
    },
    deleteAccommodation(id) {
      if (confirm('Are you sure you want to delete this accommodation?')) {
        apiClient
          .delete(`http://127.0.0.1:8000/services/accommodations/${id}/`)
          .then(() => {
            this.accommodations = this.accommodations.filter(acc => acc.id !== id);
          })
          .catch(error => {
            console.error('Error deleting accommodation:', error);
          });
      }
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

    handleAddTransp(transportation) {
      this.formData.transportations.push(transportation);
      this.closeAddTranspPopup();
      this.fetchTransportations();
    },
    openAddTranspPopup() {
      this.showAddTranspPopup = true;
    },
    closeAddTranspPopup() {
      this.showAddTranspPopup = false;
    },
    deleteTransportation(id) {
      if (confirm('Are you sure you want to delete this transportation?')) {
        apiClient
          .delete(`http://127.0.0.1:8000/services/transportations/${id}/`)
          .then(() => {
            this.transportations = this.transportations.filter(transp => transp.id !== id);
          })
          .catch(error => {
            console.error('Error deleting transportation:', error);
          });
      }
    },
    submitForm() {
      this.formData.visibility = document.getElementById("visibility").checked;
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
            visibility: false,
            participants: [],
            pois: [],
            accommodations: [],
            transportations: [],
          };
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            console.error("Error submitting form:", error.response.data);
            let errorMessage = "An unexpected error occurred";
            if (Array.isArray(error.response.data)) {
              errorMessage = error.response.data[0];
            } else if (typeof error.response.data === "object") {
              errorMessage = Object.values(error.response.data).flat()[0];
            }
            this.emitter.emit("showAlert", {
              message: errorMessage,
              backgroundColor: "#f44336",
              textColor: "white",
            });
          } else {
            console.error("Error submitting form:", error);
            if (
              error.response &&
              error.response.data &&
              error.response.data.detail
            ) {
              this.emitter.emit("showAlert", {
                message: error.response.data.detail,
                backgroundColor: "#f44336",
                textColor: "white",
              });
            } else {
              this.emitter.emit("showAlert", {
                message: "An unexpected error occurred",
                backgroundColor: "#f44336",
                textColor: "white",
              });
            }
          }
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

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  width: 400px;
  max-height: 800px;
  margin: 20px;
  overflow-y: auto;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.info {
  font-size: 14px;
  font-style: italic;
}

.add-button {
  background-color: #1976d2;
  color: white;
  padding: 2px 4px;
  text-decoration: none;
  border-radius: 4px;
  display: inline-block;
}

.add-button:hover {
  background-color: #1565c0;
}

.delete-text {
  color: red;
  font-style: italic;
}
</style>
