<template>

<h2>

Student Dashboard

</h2>

<div class="row">

<div class="col-md-4">

<DashboardCard

title="Applications"

:value="applications"

/>

</div>

<div class="col-md-4">

<DashboardCard

title="Selected"

:value="selected"

/>

</div>

<div class="col-md-4">

<DashboardCard

title="Available Drives"

:value="drives"

/>

</div>

</div>

</template>

<script setup>

import DashboardCard from "../../components/DashboardCard.vue"

const applications=0

const selected=0

const drives=0

</script>