<template>

<div class="container">

<h2 class="mb-4">

My Applications

</h2>

<table class="table table-bordered">

<thead class="table-dark">

<tr>

<th>Company</th>

<th>Job</th>

<th>Status</th>

<th>Date</th>

</tr>

</thead>

<tbody>

<tr
v-for="app in applications"
:key="app.date + app.company"
>

<td>{{app.company}}</td>

<td>{{app.job_title}}</td>

<td>{{app.status}}</td>

<td>{{app.date}}</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue"

import api from "../../services/api"

const applications = ref([])

async function loadApplications(){

const response = await api.get(
"/student/applications"
)

applications.value = response.data

}

onMounted(loadApplications)

</script>