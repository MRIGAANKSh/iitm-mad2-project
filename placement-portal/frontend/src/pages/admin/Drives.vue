<template>

<div class="container">

<h2 class="mb-4">

Placement Drives

</h2>

<table class="table table-bordered">

<thead class="table-dark">

<tr>

<th>Company</th>
<th>Job</th>
<th>Salary</th>
<th>Location</th>
<th>Deadline</th>
<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="drive in drives"
:key="drive.id"
>

<td>{{ drive.company }}</td>

<td>{{ drive.job_title }}</td>

<td>{{ drive.salary }}</td>

<td>{{ drive.location }}</td>

<td>{{ drive.deadline }}</td>

<td>

<span
class="badge"
:class="{

'bg-warning': drive.status=='pending',

'bg-success': drive.status=='approved',

'bg-danger': drive.status=='rejected',

'bg-secondary': drive.status=='closed'

}"
>

{{ drive.status }}

</span>

</td>

<td>

<button
class="btn btn-success btn-sm me-1"
@click="approve(drive.id)"
>

Approve

</button>

<button
class="btn btn-warning btn-sm me-1"
@click="reject(drive.id)"
>

Reject

</button>

<button
class="btn btn-danger btn-sm"
@click="closeDrive(drive.id)"
>

Close

</button>

</td>

</tr>

</tbody>

</table>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue"

import api from "../../services/api"

const drives = ref([])

async function loadDrives(){

    const response = await api.get(
        "/admin/drives"
    )

    drives.value = response.data

}

async function approve(id){

    await api.put(
        `/admin/drives/${id}/approve`
    )

    loadDrives()

}

async function reject(id){

    await api.put(
        `/admin/drives/${id}/reject`
    )

    loadDrives()

}

async function closeDrive(id){

    await api.put(
        `/admin/drives/${id}/close`
    )

    loadDrives()

}

onMounted(loadDrives)

</script>