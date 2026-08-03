<template>

<div class="container">

<h2 class="mb-4">
Placement Drives
</h2>

<input
class="form-control mb-3"
placeholder="Search Job Title..."
v-model="search"
/>

<table class="table table-bordered">

<thead class="table-dark">

<tr>

<th>Company</th>

<th>Job</th>

<th>Branch</th>

<th>CGPA</th>

<th>Deadline</th>

<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="drive in filteredDrives"
:key="drive.id"
>

<td>{{ drive.company }}</td>

<td>{{ drive.job_title }}</td>

<td>{{ drive.branch }}</td>

<td>{{ drive.cgpa }}</td>

<td>{{ drive.deadline }}</td>

<td>

<button
v-if="!drive.already_applied"
class="btn btn-primary btn-sm"
@click="apply(drive.id)"
>

Apply

</button>

<span
v-else
class="badge bg-success"
>

Applied

</span>

</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue"
import api from "../../services/api"

const drives = ref([])
const search = ref("")

const filteredDrives = computed(() => {

    return drives.value.filter(d =>
        d.job_title.toLowerCase().includes(
            search.value.toLowerCase()
        )
    )

})

async function loadDrives() {

    const response = await api.get("/student/drives")

    drives.value = response.data

}

async function apply(id) {

    await api.post(`/student/apply/${id}`)

    loadDrives()

}

onMounted(loadDrives)

</script>