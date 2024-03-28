<template>
  <div>
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-marker
        v-for="(coord, index) in coordinates"
        :key="index"
        :lat-lng="coord"
      ></l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  props: {
    pois: Array,
  },
  data() {
    return {
      zoom: 10,
      center: [51.505, -0.09],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    };
  },
};
</script>

<style scoped></style>
