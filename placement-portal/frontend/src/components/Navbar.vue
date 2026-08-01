<template>

<nav class="navbar navbar-dark bg-dark">

<div class="container-fluid">

<span class="navbar-brand">

Placement Portal

</span>

<button
class="btn btn-danger"
@click="logout">

Logout

</button>

</div>

</nav>

</template>

<script setup>

function logout(){

localStorage.clear()

window.location="/"

}

</script>