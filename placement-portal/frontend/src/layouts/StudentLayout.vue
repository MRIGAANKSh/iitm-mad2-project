<template>

<Navbar/>

<div class="container-fluid">

<div class="row">

<div class="col-md-2 bg-light min-vh-100">

<div class="list-group mt-3">

<router-link
to="/student/dashboard"
class="list-group-item">

Dashboard

</router-link>

<router-link
to="/student/drives"
class="list-group-item">

Placement Drives

</router-link>

<router-link
to="/student/applications"
class="list-group-item">

Applications

</router-link>

<router-link
to="/student/profile"
class="list-group-item">

Profile

</router-link>

<router-link
to="/student/resume"
class="list-group-item">

Resume

</router-link>

</div>

</div>

<div class="col-md-10 p-4">

<router-view/>

</div>

</div>

</div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue"

</script>