
import {
  createRouter,
  createWebHistory
} from "vue-router";

// =====================================================
// AUTH
// =====================================================

import Login from "../pages/Login.vue";
import RegisterStudent from "../pages/RegisterStudent.vue";
import RegisterCompany from "../pages/RegisterCompany.vue";


// =====================================================
// LAYOUTS
// =====================================================

import AdminLayout from "../layouts/AdminLayout.vue";
import CompanyLayout from "../layouts/CompanyLayout.vue";
import StudentLayout from "../layouts/StudentLayout.vue";


// =====================================================
// ADMIN
// =====================================================

import AdminDashboard from "../pages/admin/Dashboard.vue";
import Students from "../pages/admin/Students.vue";
import Companies from "../pages/admin/Companies.vue";
import AdminDrives from "../pages/admin/Drives.vue";
import Reports from "../pages/admin/Reports.vue";
import AdminApplications from "../pages/admin/Applications.vue";


// =====================================================
// COMPANY
// =====================================================

import CompanyDashboard from "../pages/company/Dashboard.vue";
import CreateDrive from "../pages/company/CreateDrive.vue";
import Drives from "../pages/company/Drives.vue";
import Applicants from "../pages/company/Applicants.vue";
import EditDrive from "../pages/company/EditDrives.vue";
import DriveApplicants from "../pages/company/DriveApplicants.vue";
import CompanyProfile from "../pages/company/Profile.vue";


// =====================================================
// STUDENT
// =====================================================

import StudentDashboard from "../pages/student/Dashboard.vue";
import StudentDrives from "../pages/student/Drives.vue";
import Applications from "../pages/student/Applications.vue";
import Profile from "../pages/student/Profile.vue";
import Resume from "../pages/student/Resume.vue";


// =====================================================
// ROUTES
// =====================================================

const routes = [

  // ===================================================
  // LOGIN
  // ===================================================

  {
    path: "/",
    component: Login
  },


  // ===================================================
  // ADMIN
  // ===================================================

  {
    path: "/admin",
    component: AdminLayout,

    children: [

      // Admin Dashboard
      {
        path: "dashboard",
        component: AdminDashboard
      },

      // Students
      {
        path: "students",
        component: Students
      },

      // Companies
      {
        path: "companies",
        component: Companies
      },

      // Placement Drives
      {
        path: "drives",
        component: AdminDrives
      },

      // Reports
      {
        path: "reports",
        component: Reports
      },

      // Applications
      {
        path: "applications",
        component: AdminApplications
      }

    ]
  },


  // ===================================================
  // COMPANY
  // ===================================================

  {
    path: "/company",
    component: CompanyLayout,

    children: [

      // Company Dashboard
      {
        path: "dashboard",
        component: CompanyDashboard
      },

      // Create Drive
      {
        path: "create-drive",
        component: CreateDrive
      },

      // All Drives
      {
        path: "drives",
        component: Drives
      },

      // All Applicants
      {
        path: "applicants",
        component: Applicants
      },

      // Applicants of One Drive
      {
        path: "drives/:id/applicants",
        component: DriveApplicants
      },

      // Edit Drive
      {
        path: "edit-drive/:id",
        component: EditDrive
      },

      // Company Profile
      {
        path: "profile",
        component: CompanyProfile
      }

    ]
  },


  // ===================================================
  // STUDENT
  // ===================================================

  {
    path: "/student",
    component: StudentLayout,

    children: [

      // Student Dashboard
      {
        path: "dashboard",
        component: StudentDashboard
      },

      // Placement Drives
      {
        path: "drives",
        component: StudentDrives
      },

      // My Applications
      {
        path: "applications",
        component: Applications
      },

      // Student Profile
      {
        path: "profile",
        component: Profile
      },

      // Resume
      {
        path: "resume",
        component: Resume
      }

    ]
  },


  // ===================================================
  // REGISTRATION
  // ===================================================

  {
    path: "/register/student",
    component: RegisterStudent
  },

  {
    path: "/register/company",
    component: RegisterCompany
  }

];


// =====================================================
// CREATE ROUTER
// =====================================================

const router = createRouter({

  history: createWebHistory(),

  routes

});


// =====================================================
// ROUTE GUARD
// =====================================================

router.beforeEach((to, from, next) => {

  const token =
    localStorage.getItem("token");

  const role =
    localStorage.getItem("role");


  // ===================================================
  // PUBLIC PAGES
  // ===================================================

  const publicPages = [
    "/",
    "/register/student",
    "/register/company"
  ];


  if (publicPages.includes(to.path)) {

    next();

    return;

  }


  // ===================================================
  // USER NOT LOGGED IN
  // ===================================================

  if (!token) {

    next("/");

    return;

  }


  // ===================================================
  // ADMIN ACCESS
  // ===================================================

  if (to.path.startsWith("/admin")) {

    if (role !== "admin") {

      alert(
        "Admin access required."
      );

      next("/");

      return;

    }

  }


  // ===================================================
  // COMPANY ACCESS
  // ===================================================

  if (to.path.startsWith("/company")) {

    if (role !== "company") {

      alert(
        "Company access required."
      );

      next("/");

      return;

    }

  }


  // ===================================================
  // STUDENT ACCESS
  // ===================================================

  if (to.path.startsWith("/student")) {

    if (role !== "student") {

      alert(
        "Student access required."
      );

      next("/");

      return;

    }

  }


  // ===================================================
  // ALLOW ROUTE
  // ===================================================

  next();

});


export default router;

