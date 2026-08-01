import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/Login.vue";
import AdminDashboard from "../pages/admin/Dashboard.vue";
import CompanyLayout from "../layouts/CompanyLayout.vue"

import CompanyDashboard from "../pages/company/Dashboard.vue"
import CreateDrive from "../pages/company/CreateDrive.vue"
import Drives from "../pages/company/Drives.vue"
import Applicants from "../pages/company/Applicants.vue"

const routes = [
  {
    path: "/",
    component: Login
  },
  {
    path: "/admin/dashboard",
    component: AdminDashboard
  },

{
    path: "/company",
    component: CompanyLayout,
    children: [

        {
            path: "dashboard",
            component: CompanyDashboard
        },

        {
            path: "create-drive",
            component: CreateDrive
        },

        {
            path: "drives",
            component: Drives
        },

        {
            path: "applicants",
            component: Applicants
        }

    ]
}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

