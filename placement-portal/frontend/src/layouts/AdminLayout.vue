
<template>

  <div class="admin-layout">

    <!-- =========================================
         SIDEBAR
    ========================================== -->

    <aside class="admin-sidebar">

      <!-- Brand -->

      <div class="sidebar-brand">

        <div class="brand-icon">
          P
        </div>

        <div>

          <h5 class="brand-title">
            Placement Portal
          </h5>

          <small class="brand-subtitle">
            Admin Panel
          </small>

        </div>

      </div>


      <!-- Divider -->

      <div class="sidebar-divider"></div>


      <!-- Navigation -->

      <nav class="sidebar-nav">


        <!-- Dashboard -->

        <router-link
          to="/admin/dashboard"
          class="sidebar-link"
        >

          

          <span>
            Dashboard
          </span>

        </router-link>


        <!-- Students -->

        <router-link
          to="/admin/students"
          class="sidebar-link"
        >

         
          <span>
            Students
          </span>

        </router-link>


        <!-- Companies -->

        <router-link
          to="/admin/companies"
          class="sidebar-link"
        >

         
          <span>
            Companies
          </span>

        </router-link>


        <!-- Placement Drives -->

        <router-link
          to="/admin/drives"
          class="sidebar-link"
        >

         

          <span>
            Placement Drives
          </span>

        </router-link>


        <!-- Applications -->

        <router-link
          to="/admin/applications"
          class="sidebar-link"
        >

          

          <span>
            Applications
          </span>

        </router-link>


        <!-- Reports -->

        <router-link
          to="/admin/reports"
          class="sidebar-link"
        >

          

          <span>
            Reports
          </span>

        </router-link>


      </nav>


      <!-- Sidebar Bottom -->

      <div class="sidebar-bottom">

        <div class="sidebar-divider"></div>


        <!-- Admin Info -->

        <div class="admin-info">

          <div class="admin-avatar">
            A
          </div>

          <div class="admin-details">

            <strong>
              Administrator
            </strong>

            <small>
              Placement Admin
            </small>

          </div>

        </div>


        <!-- Logout -->

        <button
          class="logout-btn"
          @click="logout"
        >

          <span>
            ⇥
          </span>

          Logout

        </button>

      </div>

    </aside>


    <!-- =========================================
         MAIN CONTENT
    ========================================== -->

    <main class="admin-main">

      <!-- Top Bar -->

      <header class="admin-topbar">

        <div>

          <h6 class="mb-1">
            Administration
          </h6>

          <span class="topbar-subtitle">
            Manage your placement portal
          </span>

        </div>


        <div class="topbar-right">

          <div class="status-dot"></div>

          <span>
            System Online
          </span>

        </div>

      </header>


      <!-- Page Content -->

      <section class="admin-content">

        <router-view />

      </section>

    </main>

  </div>

</template>


<script setup>

import { useRouter } from "vue-router"


const router = useRouter()


// ==========================================
// LOGOUT
// ==========================================

function logout() {

  localStorage.clear()

  router.push("/")

}

</script>


<style scoped>

/* =========================================
   GLOBAL LAYOUT
========================================= */

.admin-layout {

  min-height: 100vh;

  display: flex;

  background: #f5f7fb;

  color: #1f2937;

}


/* =========================================
   SIDEBAR
========================================= */

.admin-sidebar {

  width: 255px;

  min-height: 100vh;

  background: #ffffff;

  border-right: 1px solid #e5e7eb;

  display: flex;

  flex-direction: column;

  padding: 24px 16px;

  position: fixed;

  left: 0;

  top: 0;

  bottom: 0;

  z-index: 100;

}


/* =========================================
   BRAND
========================================= */

.sidebar-brand {

  display: flex;

  align-items: center;

  gap: 12px;

  padding: 4px 8px;

}


.brand-icon {

  width: 42px;

  height: 42px;

  border-radius: 10px;

  background: #2563eb;

  color: #ffffff;

  display: flex;

  align-items: center;

  justify-content: center;

  font-size: 20px;

  font-weight: 700;

}


.brand-title {

  margin: 0;

  font-size: 16px;

  font-weight: 700;

  color: #111827;

}


.brand-subtitle {

  color: #6b7280;

  font-size: 12px;

}


/* =========================================
   DIVIDER
========================================= */

.sidebar-divider {

  height: 1px;

  background: #e5e7eb;

  margin: 22px 4px;

}


/* =========================================
   NAVIGATION
========================================= */

.sidebar-nav {

  display: flex;

  flex-direction: column;

  gap: 5px;

}


.sidebar-link {

  display: flex;

  align-items: center;

  gap: 12px;

  padding: 11px 13px;

  border-radius: 8px;

  color: #4b5563;

  text-decoration: none;

  font-size: 14px;

  font-weight: 500;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;

}


.sidebar-link:hover {

  background: #f1f5f9;

  color: #2563eb;

}


.sidebar-link.router-link-active {

  background: #eff6ff;

  color: #2563eb;

  font-weight: 600;

}


.nav-icon {

  width: 25px;

  text-align: center;

  font-size: 17px;

}


/* =========================================
   SIDEBAR BOTTOM
========================================= */

.sidebar-bottom {

  margin-top: auto;

}


.admin-info {

  display: flex;

  align-items: center;

  gap: 10px;

  padding: 10px 8px 14px;

}


.admin-avatar {

  width: 38px;

  height: 38px;

  border-radius: 50%;

  background: #dbeafe;

  color: #2563eb;

  display: flex;

  align-items: center;

  justify-content: center;

  font-weight: 700;

}


.admin-details {

  display: flex;

  flex-direction: column;

  min-width: 0;

}


.admin-details strong {

  font-size: 13px;

  color: #111827;

}


.admin-details small {

  font-size: 11px;

  color: #6b7280;

}


/* =========================================
   LOGOUT
========================================= */

.logout-btn {

  width: 100%;

  border: 1px solid #fee2e2;

  background: #fff;

  color: #dc2626;

  border-radius: 8px;

  padding: 10px 12px;

  font-size: 14px;

  font-weight: 500;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  cursor: pointer;

  transition:
    background 0.2s ease,
    border-color 0.2s ease;

}


.logout-btn:hover {

  background: #fef2f2;

  border-color: #fecaca;

}


/* =========================================
   MAIN
========================================= */

.admin-main {

  margin-left: 255px;

  width: calc(100% - 255px);

  min-height: 100vh;

}


/* =========================================
   TOP BAR
========================================= */

.admin-topbar {

  height: 70px;

  background: #ffffff;

  border-bottom: 1px solid #e5e7eb;

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 0 30px;

}


.admin-topbar h6 {

  color: #111827;

  font-weight: 600;

  font-size: 14px;

}


.topbar-subtitle {

  color: #6b7280;

  font-size: 12px;

}


.topbar-right {

  display: flex;

  align-items: center;

  gap: 7px;

  font-size: 12px;

  color: #6b7280;

}


.status-dot {

  width: 8px;

  height: 8px;

  border-radius: 50%;

  background: #22c55e;

}


/* =========================================
   CONTENT
========================================= */

.admin-content {

  padding: 30px;

}


/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 768px) {

  .admin-sidebar {

    width: 210px;

  }


  .admin-main {

    margin-left: 210px;

    width: calc(100% - 210px);

  }


  .admin-content {

    padding: 20px;

  }


  .admin-topbar {

    padding: 0 20px;

  }

}


@media (max-width: 576px) {

  .admin-sidebar {

    width: 70px;

    padding: 20px 10px;

  }


  .brand-title,

  .brand-subtitle,

  .sidebar-link span:not(.nav-icon),

  .admin-details,

  .logout-btn span:not(:first-child) {

    display: none;

  }


  .sidebar-brand {

    justify-content: center;

  }


  .sidebar-link {

    justify-content: center;

    padding: 12px;

  }


  .nav-icon {

    width: auto;

  }


  .admin-main {

    margin-left: 70px;

    width: calc(100% - 70px);

  }


  .admin-topbar {

    padding: 0 15px;

  }


  .topbar-right {

    display: none;

  }


  .admin-content {

    padding: 15px;

  }

}

</style>

