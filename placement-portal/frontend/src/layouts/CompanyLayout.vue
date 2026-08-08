
<template>

  <div class="row g-0 min-vh-100">

    <!-- =========================
         COMPANY SIDEBAR
    ========================== -->

    <div class="col-md-2 bg-light border-end p-3">

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


        <!-- ALL COMPANY APPLICANTS -->
        <router-link
          to="/company/applicants"
          class="list-group-item list-group-item-action"
          active-class="active"
        >
          Applicants
        </router-link>

      </div>

    </div>


    <!-- =========================
         MAIN CONTENT
    ========================== -->

    <div class="col-md-10 p-4">

      <!--
        Child pages are rendered here.

        /company/dashboard
        /company/create-drive
        /company/drives
        /company/applicants
        /company/drives/:id/applicants
      -->

      <router-view />

    </div>

  </div>

</template>

<script setup>
// No special JavaScript is required in CompanyLayout.vue.
// Vue Router handles the navigation and <router-view>
// renders the selected company page.
</script>

