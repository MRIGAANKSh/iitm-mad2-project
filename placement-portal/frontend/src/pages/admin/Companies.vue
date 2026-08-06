<template>
<div class="container">

<h2 class="mb-4">Manage Companies</h2>

<table class="table table-bordered table-hover">

<thead class="table-dark">

<tr>

<th>Company</th>
<th>Email</th>
<th>HR</th>
<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="company in companies"
:key="company.id"
>

<td>{{ company.company_name }}</td>

<td>{{ company.email }}</td>

<td>{{ company.hr_name }}</td>

<td>

<span
class="badge"
:class="{
'bg-warning': company.approval_status=='pending',
'bg-success': company.approval_status=='approved',
'bg-danger': company.approval_status=='rejected'
}"
>

{{ company.approval_status }}

</span>

</td>

<td>

<button
class="btn btn-success btn-sm me-2"
@click="approve(company.id)"
>

Approve

</button>

<button
class="btn btn-warning btn-sm me-2"
@click="reject(company.id)"
>

Reject

</button>

<button
class="btn btn-danger btn-sm"
@click="blacklist(company.id)"
>

Blacklist

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

const companies = ref([])

async function loadCompanies(){

    const response = await api.get(
        "/admin/companies"
    )

    companies.value = response.data

}

async function approve(id){

    await api.put(
        `/admin/companies/${id}/approve`
    )

    loadCompanies()

}

async function reject(id){

    await api.put(
        `/admin/companies/${id}/reject`
    )

    loadCompanies()

}

async function blacklist(id){

    await api.put(
        `/admin/companies/${id}/blacklist`
    )

    loadCompanies()

}

onMounted(loadCompanies)

</script>