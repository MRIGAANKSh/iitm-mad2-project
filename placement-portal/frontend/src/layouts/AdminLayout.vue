<template>
  <Navbar />

  <div class="container-fluid">
    <div class="row">

      <div class="col-md-2 bg-light min-vh-100 pt-3">

        <div class="list-group">

          <router-link
            to="/admin/dashboard"
            class="list-group-item"
          >
            Dashboard
          </router-link>

          <router-link
            to="/admin/companies"
            class="list-group-item"
          >
            Companies
          </router-link>

          <router-link
            to="/admin/students"
            class="list-group-item"
          >
            Students
          </router-link>

          <router-link
            to="/admin/drives"
            class="list-group-item"
          >
            Placement Drives
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