<template>
    <div>
      <h2>Add new Accommodation</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" required />
        </div>
        <div class="form-group">
          <label for="location">Location:</label>
          <input type="text" id="location" v-model="location" required />
        </div>
        <div class="form-group">
          <label for="details">Details:</label>
          <textarea id="details" v-model="details"></textarea>
        </div>
        <div class="form-group">
          <label for="price_per_night">Price per Night:</label>
          <input type="text" id="price_per_night" v-model="pricePerNight" required />
        </div>
        <div class="form-group">
          <label for="checkin_date">Check-in Date:</label>
          <input type="date" id="checkin_date" v-model="checkinDate" required />
        </div>
        <div class="form-group">
          <label for="checkout_date">Check-out Date:</label>
          <input type="date" id="checkout_date" v-model="checkoutDate" required />
        </div>
        <div class="form-group">
          <label for="amenities">Amenities:</label>
          <input type="text" id="amenities" v-model="amenities" />
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
        location: "",
        details: "",
        pricePerNight: "",
        checkinDate: "",
        checkoutDate: "",
        amenities: ""
      };
    },
    methods: {
      submitForm() {
        const accommodationData = {
          name: this.name,
          location: this.location,
          details: this.details,
          price_per_night: this.pricePerNight,
          checkin_date: this.checkinDate,
          checkout_date: this.checkoutDate,
          amenities: this.amenities
        };
        apiClient
          .post("http://localhost:8000/services/accommodations/", accommodationData)
          .then((response) => {
            console.log("New Accommodation created:", response.data);
          })
          .catch((error) => {
            console.error("Error creating Accommodation:", error);
          });
      }
    }
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
