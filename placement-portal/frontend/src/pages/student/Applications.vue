
<template>

  <!-- Page Title -->
  <h2 class="mb-4">
    My Applications
  </h2>


  <!-- Export Button -->
  <button
    class="btn btn-success mb-3"
    @click="exportApplications"
  >
    Export Applications CSV
  </button>


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

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"


// =========================================================
// STATE
// =========================================================

const applications = ref([])

const loading = ref(true)

const error = ref("")


// =========================================================
// LOAD APPLICATIONS
// =========================================================

async function loadApplications() {

  try {

    loading.value = true

    const response = await api.get(
      "/student/applications"
    )

    applications.value =
      Array.isArray(response.data)
        ? response.data
        : []

  } catch (err) {

    console.error(
      "Error loading applications:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to load applications."

  } finally {

    loading.value = false

  }

}


// =========================================================
// STATUS CLASS
// =========================================================

function getStatusClass(status) {

  switch (status) {

    case "Selected":
      return "bg-success"

    case "Rejected":
      return "bg-danger"

    case "Shortlisted":
      return "bg-warning text-dark"

    case "Applied":
      return "bg-primary"

    default:
      return "bg-secondary"

  }

}


// =========================================================
// EXPORT APPLICATIONS
// =========================================================

async function exportApplications() {

    try {

        const response = await api.post(
            "/student/applications/export",
            {},
            {
                responseType: "blob"
            }
        );


        const blob = new Blob(
            [response.data],
            {
                type: "text/csv"
            }
        );


        const url =
            window.URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;

        link.download =
            "my_applications.csv";


        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);


        window.URL.revokeObjectURL(url);

    } catch (error) {

        console.error(
            "Export failed:",
            error
        );


        alert(
            "Application export failed."
        );
    }
}




// =========================================================
// LOAD PAGE
// =========================================================

onMounted(() => {

  loadApplications()

})

</script>

