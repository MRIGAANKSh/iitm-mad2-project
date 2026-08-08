<template>

<div class="container">

    <h2 class="mb-4">
        Placement Drives
    </h2>

    <!-- Search -->

    <div class="row mb-4">

        <div class="col-md-5">

            <input
                v-model="search"
                @input="loadDrives"
                class="form-control"
                placeholder="Search job title..."
            >

        </div>

        <div class="col-md-3">

            <input
                v-model="branch"
                @input="loadDrives"
                class="form-control"
                placeholder="Branch"
            >

        </div>

        <div class="col-md-3">

            <input
                v-model="cgpa"
                @input="loadDrives"
                type="number"
                step="0.1"
                class="form-control"
                placeholder="CGPA"
            >

        </div>

    </div>


    <!-- Drives -->

    <div
        v-if="drives.length === 0"
        class="alert alert-info"
    >

        No placement drives found.

    </div>


    <div class="row">

        <div
            v-for="drive in drives"
            :key="drive.id"
            class="col-md-6 mb-4"
        >

            <div class="card shadow h-100">

                <div class="card-body">

                    <h4>
                        {{ drive.job_title }}
                    </h4>

                    <h6 class="text-primary">
                        {{ drive.company }}
                    </h6>

                    <hr>

                    <p>
                        {{ drive.job_description }}
                    </p>

                    <p>
                        <strong>Branch:</strong>
                        {{ drive.eligibility_branch }}
                    </p>

                    <p>
                        <strong>Minimum CGPA:</strong>
                        {{ drive.minimum_cgpa }}
                    </p>

                    <p>
                        <strong>Graduation Year:</strong>
                        {{ drive.graduation_year }}
                    </p>

                    <p>
                        <strong>Salary:</strong>
                        {{ drive.salary || "Not specified" }}
                    </p>

                    <p>
                        <strong>Location:</strong>
                        {{ drive.location || "Not specified" }}
                    </p>

                    <p>
                        <strong>Deadline:</strong>
                        {{ drive.deadline }}
                    </p>

                    <button
                        v-if="!drive.already_applied"
                        class="btn btn-primary"
                        @click="apply(drive.id)"
                    >

                        Apply

                    </button>

                    <button
                        v-else
                        class="btn btn-secondary"
                        disabled
                    >

                        Already Applied

                    </button>

                </div>

            </div>

        </div>

    </div>

</div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"

const drives = ref([])

const search = ref("")

const branch = ref("")

const cgpa = ref("")


async function loadDrives(){

    try{

        const response = await api.get(
            "/student/drives",
            {
                params: {

                    search: search.value,

                    branch: branch.value,

                    min_cgpa:
                        cgpa.value || undefined

                }
            }
        )

        drives.value = response.data

    }

    catch(error){

        console.error(error)

    }

}


async function apply(id){

    try{

        const response = await api.post(
            `/student/drives/${id}/apply`
        )

        alert(response.data.message)

        loadDrives()

    }

    catch(error){

        alert(
            error.response?.data?.message ||
            "Unable to apply."
        )

    }

}


onMounted(loadDrives)

</script>