import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import Home from "../views/Home.vue";

import Login from "../components/Auth/Login.vue";
import Register from "../components/Auth/Register.vue";

import Profile from "../components/Auth/Profile.vue";
import EditProfile from "../components/Auth/EditProfile.vue";
import Users from "../components/Auth/Users.vue";

import TripView from "../components/Trip/TripView.vue";
import TripDetail from "../components/Trip/TripDetail.vue";
import MyTrips from "../components/Trip/MyTrips.vue";
import AddTrip from "../components/Trip/AddTrip.vue";
import EditTrip from "../components/Trip/EditTrip.vue";

import JournalView from "../components/Journal/JournalView.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/users",
    name: "Users",
    component: Users,
  },
  {
    path: "/editprofile",
    name: "EditProfile",
    component: EditProfile,
  },
  {
    path: "/about",
    name: "About",
    component: async () => await import("../views/About.vue"),
  },
  {
    path: "/trips",
    name: "TripView",
    component: TripView,
  },
  {
    path: "/addtrip",
    name: "AddTrip",
    component: AddTrip,
  },
  {
    path: "/edittrip/:id",
    name: "EditTrip",
    component: EditTrip,
  },
  {
    path: "/mytrips",
    name: "MyTrips",
    component: MyTrips,
  },
  {
    path: "/trips/:id",
    name: "TripDetail",
    component: TripDetail,
  },
  {
    path: "/journal",
    name: "JournalView",
    component: JournalView,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
