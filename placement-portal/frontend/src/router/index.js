import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/Login.vue";
import AdminDashboard from "../pages/admin/Dashboard.vue";
import CompanyLayout from "../layouts/CompanyLayout.vue"

import CompanyDashboard from "../pages/company/Dashboard.vue"
import CreateDrive from "../pages/company/CreateDrive.vue"
import Drives from "../pages/company/Drives.vue"
import Applicants from "../pages/company/Applicants.vue"
import RegisterStudent from "../pages/RegisterStudent.vue"
import RegisterCompany from "../pages/RegisterCompany.vue"

import StudentLayout from "../layouts/StudentLayout.vue"

import StudentDashboard from "../pages/student/Dashboard.vue"

import StudentDrives from "../pages/student/Drives.vue"

import Applications from "../pages/student/Applications.vue"

import Profile from "../pages/student/Profile.vue"

import Resume from "../pages/student/Resume.vue"

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
},
{

path:"/student",

component:StudentLayout,

children:[

{

path:"dashboard",

component:StudentDashboard

},

{

path:"drives",

component:StudentDrives

},

{

path:"applications",

component:Applications

},

{

path:"profile",

component:Profile

},

{

path:"resume",

component:Resume

}

]

},
{
    path: "/register/student",
    component: RegisterStudent
},
{
    path: "/register/company",
    component: RegisterCompany
}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

