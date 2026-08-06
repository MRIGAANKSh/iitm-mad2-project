<template>

<div class="container">

<h2 class="mb-4">

Student Dashboard

</h2>

<div class="row">

<div class="col-md-3">

<div class="card text-center">

<div class="card-body">

<h5>Available Drives</h5>

<h2>{{dashboard.drives}}</h2>

</div>

</div>

</div>

<div class="col-md-3">

<div class="card text-center">

<div class="card-body">

<h5>Applications</h5>

<h2>{{dashboard.applications}}</h2>

</div>

</div>

</div>

<div class="col-md-3">

<div class="card text-center">

<div class="card-body">

<h5>Shortlisted</h5>

<h2>{{dashboard.shortlisted}}</h2>

</div>

</div>

</div>

<div class="col-md-3">

<div class="card text-center">

<div class="card-body">

<h5>Selected</h5>

<h2>{{dashboard.selected}}</h2>

</div>

</div>

</div>

</div>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue"

import api from "../../services/api"

const dashboard = ref({})

async function loadDashboard(){

    const response = await api.get(
        "/student/dashboard"
    )

    dashboard.value = response.data

}

onMounted(loadDashboard)

</script>