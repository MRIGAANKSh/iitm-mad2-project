
<template>

  <div class="container-fluid">

    <div class="row min-vh-100">

      <!-- =========================
           COMPANY SIDEBAR
      ========================== -->

      <div class="col-md-2 bg-light border-end p-3">

        <!-- Portal Title -->
        <div class="mb-4">

          <h5 class="fw-bold mb-1">
            Company Portal
          </h5>

          <small class="text-muted">
            Placement Management
          </small>

        </div>


        <!-- Navigation -->
        <div class="list-group">

          <!-- Dashboard -->
          <router-link
            to="/company/dashboard"
            class="list-group-item list-group-item-action"
            active-class="active"
          >
            Dashboard
          </router-link>


          <!-- Create Drive -->
          <router-link
            to="/company/create-drive"
            class="list-group-item list-group-item-action"
            active-class="active"
          >
            Create Drive
          </router-link>


          <!-- My Drives -->
          <router-link
            to="/company/drives"
            class="list-group-item list-group-item-action"
            active-class="active"
          >
            My Drives
          </router-link>


          <!-- Applicants -->
          <router-link
            to="/company/applicants"
            class="list-group-item list-group-item-action"
            active-class="active"
          >
            Applicants
          </router-link>


          <!-- Profile -->
          <router-link
            to="/company/profile"
            class="list-group-item list-group-item-action"
            active-class="active"
          >
            Profile
          </router-link>

        </div>

      </div>


      <!-- =========================
           MAIN CONTENT
      ========================== -->

      <div class="col-md-10 p-4">

        <!-- Child routes render here -->

        <router-view />

      </div>

    </div>

  </div>

</template>


<script setup>

// No JavaScript required for the layout.
// Vue Router automatically renders the
// selected child route inside <router-view />.

</script>

