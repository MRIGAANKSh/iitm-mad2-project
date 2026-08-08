
<template>

  <div class="container">

    <!-- Page Title -->
    <h2 class="mb-4">
      My Applications
    </h2>


    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center py-5"
    >

      <div
        class="spinner-border text-primary"
        role="status"
      ></div>

      <p class="mt-2">
        Loading applications...
      </p>

    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>


    <!-- Applications -->
    <div v-else>

      <!-- No Applications -->
      <div
        v-if="applications.length === 0"
        class="alert alert-info"
      >
        You have not applied to any placement drives yet.
      </div>


      <!-- Applications Table -->
      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-bordered table-hover">

          <thead class="table-dark">

            <tr>

              <th>
                Company
              </th>

              <th>
                Job
              </th>

              <th>
                Status
              </th>

              <th>
                Applied Date
              </th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="(app, index) in applications"
              :key="index"
            >

              <!-- Company -->
              <td>
                {{ app.company || "N/A" }}
              </td>


              <!-- Job -->
              <td>
                {{ app.job_title || "N/A" }}
              </td>


              <!-- Status -->
              <td>

                <span
                  class="badge"
                  :class="getStatusClass(app.status)"
                >
                  {{ app.status || "Applied" }}
                </span>

              </td>


              <!-- Date -->
              <td>
                {{ app.date || "N/A" }}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"


// Applications
const applications = ref([])


// Loading state
const loading = ref(true)


// Error state
const error = ref("")


// Status badge
function getStatusClass(status) {

  switch (status) {

    case "Selected":
      return "bg-success"

    case "Shortlisted":
      return "bg-warning text-dark"

    case "Rejected":
      return "bg-danger"

    case "Applied":
      return "bg-primary"

    default:
      return "bg-secondary"

  }

}


// Load applications
async function loadApplications() {

  loading.value = true

  error.value = ""

  try {

    const response = await api.get(
      "/student/applications"
    )


    console.log(
      "Student Applications:",
      response.data
    )


    // Make sure response is an array
    if (Array.isArray(response.data)) {

      applications.value = response.data

    } else {

      applications.value = []

      error.value =
        "Invalid applications response from server."

    }

  } catch (err) {

    console.error(
      "Failed to load applications:",
      err
    )


    if (err.response) {

      error.value =
        err.response.data?.message ||
        `Failed to load applications (${err.response.status})`

    } else {

      error.value =
        "Unable to connect to the server."

    }

  } finally {

    loading.value = false

  }

}


onMounted(() => {

  loadApplications()

})

</script>

