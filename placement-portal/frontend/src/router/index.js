import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/Login.vue";
import AdminDashboard from "../pages/admin/Dashboard.vue";

const routes = [
  {
    path: "/",
    component: Login
  },
  {
    path: "/admin/dashboard",
    component: AdminDashboard
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;