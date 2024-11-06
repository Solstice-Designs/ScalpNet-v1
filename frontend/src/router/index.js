import { createRouter, createWebHistory } from "vue-router";
// Import the components properly
import HomeView from "../views/HomeView.vue";
import ScalpNetDashboard from "../components/ScalpNetDashboard.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView, // Make sure HomeView is properly imported
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: ScalpNetDashboard, // Make sure ScalpNetDashboard is properly imported
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
