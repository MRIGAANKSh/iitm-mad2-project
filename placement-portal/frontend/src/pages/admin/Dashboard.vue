<template>

<Navbar/>

<div class="container mt-4">

    <h2 class="mb-4">
        Admin Dashboard
    </h2>

    <div class="row">

        <div class="col-md-3">

            <DashboardCard
                title="Students"
                :value="dashboard.students"
            />

        </div>

        <div class="col-md-3">

            <DashboardCard
                title="Companies"
                :value="dashboard.companies"
            />

        </div>

        <div class="col-md-3">

            <DashboardCard
                title="Drives"
                :value="dashboard.drives"
            />

        </div>

        <div class="col-md-3">

            <DashboardCard
                title="Applications"
                :value="dashboard.applications"
            />

        </div>

    </div>

</div>

</template>

<script setup>

import {ref,onMounted} from "vue"

import api from "../../services/api"

import Navbar from "../../components/Navbar.vue"

import DashboardCard from "../../components/DashboardCard.vue"

const dashboard=ref({

students:0,

companies:0,

drives:0,

applications:0

})

async function loadDashboard(){

const response=await api.get(
"/admin/dashboard"
)

dashboard.value=response.data

}

onMounted(loadDashboard)

</script>