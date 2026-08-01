<template>

<h2>Company Dashboard</h2>

<div class="row">

    <div class="col-md-4">

        <DashboardCard
            title="Placement Drives"
            :value="drives"
        />

    </div>

    <div class="col-md-4">

        <DashboardCard
            title="Applicants"
            :value="applications"
        />

    </div>

</div>

</template>

<script setup>

import DashboardCard from "../../components/DashboardCard.vue"

const drives = 0
const applications = 0

</script>