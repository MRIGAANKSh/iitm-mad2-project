<template>
  <Navbar />

  <div class="container-fluid">
    <div class="row">

      <div class="col-md-2 bg-light min-vh-100 p-3">
        <div class="list-group">

          <router-link
            to="/company/dashboard"
            class="list-group-item"
          >
            Dashboard
          </router-link>

          <router-link
            to="/company/create-drive"
            class="list-group-item"
          >
            Create Drive
          </router-link>

          <router-link
            to="/company/drives"
            class="list-group-item"
          >
            My Drives
          </router-link>

          <router-link
            to="/company/applicants"
            class="list-group-item"
          >
            Applicants
          </router-link>

        </div>
      </div>

      <div class="col-md-10 p-4">
        <router-view />
      </div>

    </div>
  </div>

</template>

<script setup>
import Navbar from "../components/Navbar.vue"
</script>