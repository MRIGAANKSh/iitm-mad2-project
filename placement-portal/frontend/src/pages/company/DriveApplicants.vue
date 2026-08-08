
<template>

  <!-- Header -->
  <div class="d-flex justify-content-between align-items-center mb-4">

    <div>
      <h2>
        Drive Applicants
      </h2>

      <p class="text-muted mb-0">
        Applicants for this placement drive
      </p>
    </div>

    <button
      class="btn btn-secondary"
      @click="goBack"
    >
      Back to Drives
    </button>

  </div>


  <!-- Error -->
  <div
    v-if="error"
    class="alert alert-danger"
  >
    {{ error }}
  </div>


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
      Loading applicants...
    </p>

  </div>


  <!-- Content -->
  <div v-else-if="!error">

    <!-- No Applicants -->
    <div
      v-if="applicants.length === 0"
      class="alert alert-info"
    >
      No applicants found for this drive.
    </div>


    <!-- Applicants Table -->
    <div
      v-else
      class="table-responsive"
    >

      <table
        class="table table-bordered table-hover align-middle"
      >

        <thead class="table-dark">

          <tr>

            <th>
              Student
            </th>

            <th>
              Email
            </th>

            <th>
              Job
            </th>

            <th>
              Branch
            </th>

            <th>
              CGPA
            </th>

            <th>
              Resume
            </th>

            <th>
              Status
            </th>

            <th style="min-width: 250px;">
              Actions
            </th>

          </tr>

        </thead>


        <tbody>

          <tr
            v-for="student in applicants"
            :key="student.application_id"
          >

            <!-- Student -->
            <td>
              {{ student.student_name || "N/A" }}
            </td>


            <!-- Email -->
            <td>
              {{ student.email || "N/A" }}
            </td>


            <!-- Job -->
            <td>
              {{ student.job_title || "N/A" }}
            </td>


            <!-- Branch -->
            <td>
              {{ student.branch || "N/A" }}
            </td>


            <!-- CGPA -->
            <td>
              {{ student.cgpa ?? "N/A" }}
            </td>


            <!-- Resume -->
            <td>

              <a
                v-if="student.resume"
                :href="getResumeUrl(student.resume)"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-outline-primary btn-sm"
              >
                View Resume
              </a>

              <span
                v-else
                class="text-muted"
              >
                No Resume
              </span>

            </td>


            <!-- Status -->
            <td>

              <span
                class="badge"
                :class="getStatusClass(student.status)"
              >
                {{ student.status || "Applied" }}
              </span>

            </td>


            <!-- Actions -->
            <td>

              <button
                class="btn btn-warning btn-sm me-2"
                @click="
                  updateStatus(
                    student.application_id,
                    'Shortlisted'
                  )
                "
              >
                Shortlist
              </button>


              <button
                class="btn btn-danger btn-sm me-2"
                @click="
                  updateStatus(
                    student.application_id,
                    'Rejected'
                  )
                "
              >
                Reject
              </button>


              <button
                class="btn btn-success btn-sm"
                @click="
                  updateStatus(
                    student.application_id,
                    'Selected'
                  )
                "
              >
                Select
              </button>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import axios from "axios"


// =========================================================
// ROUTER
// =========================================================

const route = useRoute()
const router = useRouter()


// =========================================================
// STATE
// =========================================================

const applicants = ref([])

const loading = ref(true)

const error = ref("")


// =========================================================
// GET DRIVE ID FROM URL
// =========================================================

// URL:
// /company/drives/2/applicants
//
// route.params.id = 2

const driveId = route.params.id


console.log(
  "Drive ID:",
  driveId
)


// =========================================================
// LOAD APPLICANTS
// =========================================================

const loadApplicants = async () => {

  loading.value = true

  error.value = ""


  try {

    // Make sure drive ID exists
    if (!driveId) {

      error.value =
        "Drive ID is missing from the URL."

      return
    }


    // API URL
    const url =
      `/api/company/drives/${driveId}/applicants`


    console.log(
      "Fetching applicants:",
      url
    )


    // API request
    const response = await axios.get(
      url,
      {
        headers: {
          Authorization:
            `Bearer ${localStorage.getItem("token")}`
        }
      }
    )


    console.log(
      "Applicants API response:",
      response.data
    )


    // Make sure response is an array
    if (Array.isArray(response.data)) {

      applicants.value =
        response.data

    } else {

      applicants.value = []

      console.error(
        "Expected array but received:",
        response.data
      )

    }

  } catch (err) {

    console.error(
      "Error loading drive applicants:",
      err
    )


    if (err.response) {

      console.error(
        "HTTP status:",
        err.response.status
      )


      console.error(
        "Backend response:",
        err.response.data
      )


      error.value =
        err.response.data?.message ||
        "Failed to load applicants."

    } else {

      error.value =
        "Unable to connect to the server."

    }

  } finally {

    loading.value = false

  }

}


// =========================================================
// UPDATE APPLICATION STATUS
// =========================================================

const updateStatus = async (
  applicationId,
  status
) => {

  try {

    await axios.put(

      `/api/company/applications/${applicationId}/status`,

      {
        status: status
      },

      {
        headers: {
          Authorization:
            `Bearer ${localStorage.getItem("token")}`
        }
      }

    )


    // Reload applicants
    await loadApplicants()


  } catch (err) {

    console.error(
      "Error updating application status:",
      err
    )


    if (err.response) {

      alert(
        err.response.data?.message ||
        "Failed to update application status."
      )

    } else {

      alert(
        "Unable to connect to the server."
      )

    }

  }

}


// =========================================================
// STATUS BADGE
// =========================================================

const getStatusClass = (status) => {

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
// RESUME URL
// =========================================================


const getResumeUrl = (resume) => {

  if (!resume) {
    return ""
  }

  // If database already contains a complete URL
  if (
    resume.startsWith("http://") ||
    resume.startsWith("https://")
  ) {
    return resume
  }

  // If database contains /uploads/filename.pdf
  if (resume.startsWith("/uploads/")) {
    return `http://localhost:5000${resume}`
  }

  // If database contains only filename
  return `http://localhost:5000/uploads/${resume}`
}




// =========================================================
// BACK TO DRIVES
// =========================================================

const goBack = () => {

  router.push(
    "/company/drives"
  )

}


// =========================================================
// LOAD WHEN PAGE OPENS
// =========================================================

onMounted(() => {

  loadApplicants()

})

</script>

