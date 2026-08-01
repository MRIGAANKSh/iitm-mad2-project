<template>

<div class="input-group mb-3">

<input
class="form-control"
placeholder="Search..."
v-model="keyword"
/>

<button
class="btn btn-primary"
@click="$emit('search',keyword)"
>

Search

</button>

</div>

</template>

<script setup>

import {ref} from "vue"

const keyword=ref("")

</script>