
<template>

  <div class="container-fluid">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">

      <div>
        <h2>All Applicants</h2>

        <p class="text-muted mb-0">
          Applicants from all your placement drives
        </p>
      </div>

      <button
        class="btn btn-secondary"
        @click="goBack"
      >
        Back to Drives
      </button>

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


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>


    <!-- Applicants -->
    <div v-else>

      <div
        v-if="applicants.length === 0"
        class="alert alert-info"
      >
        No applicants found.
      </div>


      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-bordered table-hover align-middle">

          <thead class="table-dark">

            <tr>

              <th>Student</th>

              <th>Email</th>

              <th>Job</th>

              <th>Branch</th>

              <th>CGPA</th>

              <th>Resume</th>

              <th>Status</th>

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
                {{ student.student_name }}
              </td>


              <!-- Email -->
              <td>
                {{ student.email }}
              </td>


              <!-- Job -->
              <td>
                {{ student.job_title }}
              </td>


              <!-- Branch -->
              <td>
                {{ student.branch }}
              </td>


              <!-- CGPA -->
              <td>
                {{ student.cgpa }}
              </td>


              <!-- Resume -->
              <td>

                <a
                  v-if="student.resume"
                  :href="student.resume"
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
                  {{ student.status }}
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

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import { useRouter } from "vue-router"

import api from "../../services/api"


const router = useRouter()


const applicants = ref([])

const loading = ref(false)

const error = ref("")


// ========================================
// LOAD ALL COMPANY APPLICANTS
// ========================================

async function loadApplicants() {

  loading.value = true

  error.value = ""

  try {

    /*
      IMPORTANT:

      This is NOT:

      /company/drives/:id/applications

      because this page is for ALL applicants.

      We use:

      /company/applications
    */

    const response = await api.get(
      "/company/applications"
    )

    applicants.value = response.data || []

  }

  catch (err) {

    console.error(
      "Failed to load applicants:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to load applicants."

  }

  finally {

    loading.value = false

  }

}


// ========================================
// UPDATE STATUS
// ========================================

async function updateStatus(
  applicationId,
  status
) {

  try {

    await api.put(
      `/company/applications/${applicationId}/status`,
      {
        status: status
      }
    )

    // Update UI immediately
    const applicant =
      applicants.value.find(
        item =>
          item.application_id === applicationId
      )

    if (applicant) {

      applicant.status = status

    }

  }

  catch (err) {

    console.error(
      "Status update failed:",
      err
    )

    alert(
      err.response?.data?.message ||
      "Failed to update application status."
    )

  }

}


// ========================================
// STATUS BADGE
// ========================================

function getStatusClass(status) {

  switch (status) {

    case "Shortlisted":
      return "bg-warning text-dark"

    case "Rejected":
      return "bg-danger"

    case "Selected":
      return "bg-success"

    case "Applied":
      return "bg-primary"

    default:
      return "bg-secondary"

  }

}


// ========================================
// BACK TO DRIVES
// ========================================

function goBack() {

  router.push("/company/drives")

}


// ========================================
// LOAD WHEN PAGE OPENS
// ========================================

onMounted(() => {

  loadApplicants()

})

</script>

