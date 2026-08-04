<template>

<nav class="navbar navbar-dark bg-dark">

<div class="container-fluid">

<span class="navbar-brand">

Placement Portal - Admin

</span>

<button
class="btn btn-danger"
@click="logout"
>

Logout

</button>

</div>

</nav>

<div class="container-fluid">

<div class="row">

<div class="col-md-2 bg-light min-vh-100">

<div class="list-group mt-3">

<router-link
to="/admin/dashboard"
class="list-group-item"
>

Dashboard

</router-link>

<router-link
to="/admin/students"
class="list-group-item"
>

Students

</router-link>

<router-link
to="/admin/companies"
class="list-group-item"
>

Companies

</router-link>

<router-link
to="/admin/drives"
class="list-group-item"
>

Placement Drives

</router-link>

<router-link
to="/admin/reports"
class="list-group-item"
>

Reports

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

import { useRouter } from "vue-router"

const router = useRouter()

function logout(){

localStorage.clear()

router.push("/")

}

</script>   