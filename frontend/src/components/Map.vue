<template>
  <div class="container">
    <div ref="mapContainer" id="map" class="map"></div>
  </div>
</template>

<script>
import L from "leaflet";
import apiClient from "../utils/apiClient";

export default {
  props: {
    tripId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      lat: 0,
      lng: 0,
      map: null,
      zoom: 5,
      center: [51.505, -0.09],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      pois: [],
    };
  },
  mounted() {
    this.map = L.map(this.$refs.mapContainer).setView([51.505, -0.09], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.map);
    this.map.invalidateSize();
    this.fetchPOIs(this.tripId);
  },
  methods: {
    getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition((position) => {
          this.lat = position.coords.latitude;
          this.lng = position.coords.longitude;
          this.map.setView([this.lat, this.lng], 13);

          L.marker([this.lat, this.lng], { draggable: true })
            .addTo(this.map)
            .on("dragend", (event) => {
              console.log(event);
            });
        });
      }
    },
    fetchPOIs(tripId) {
      apiClient
        .get(`http://localhost:8000/trip/trips/${tripId}/`)
        .then((response) => {
          this.pois = response.data.pois;
          this.pois.forEach((poi) => {
            L.marker([poi.location_latitude, poi.location_longitude])
              .addTo(this.map)
              .bindPopup(
                `<b>${poi.name}</b><br>${poi.description}<br>Location: ${poi.location_latitude}, ${poi.location_longitude}<br>Opening Hours: ${poi.opening_hours}`,
              )
              .openPopup();
          });
        })
        .catch((error) => {
          console.error("Error fetching POIs:", error);
        });
    },
  },
};
</script>

<style scoped>
#mapContainer {
  width: 100%;
  height: 400px;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.map {
  width: 400px;
  height: 400px;
}
</style>
