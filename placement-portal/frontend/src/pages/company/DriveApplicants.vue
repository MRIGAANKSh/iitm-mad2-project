
<template>

  <!-- =========================
       HEADER
  ========================== -->

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


  <!-- =========================
       LOADING
  ========================== -->

  <div
    v-if="loading"
    class="text-center py-5"
  >

    <div
      class="spinner-border text-primary"
      role="status"
    ></div>

    <p class="mt-2 text-muted">
      Loading applicants...
    </p>

  </div>


  <!-- =========================
       ERROR
  ========================== -->

  <div
    v-else-if="error"
    class="alert alert-danger"
  >

    {{ error }}

  </div>


  <!-- =========================
       APPLICANTS
  ========================== -->

  <div v-else>

    <!-- No Applicants -->

    <div
      v-if="applicants.length === 0"
      class="alert alert-info"
    >

      No applicants found for this drive.

    </div>


    <!-- =========================
         TABLE
    ========================== -->

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

            <th style="min-width: 380px;">
              Actions
            </th>

          </tr>

        </thead>


        <tbody>

          <tr
            v-for="student in applicants"
            :key="student.application_id"
          >

            <!-- =========================
                 STUDENT
            ========================== -->

            <td>

              <strong>
                {{ student.student_name || "N/A" }}
              </strong>

            </td>


            <!-- =========================
                 EMAIL
            ========================== -->

            <td>
              {{ student.email || "N/A" }}
            </td>


            <!-- =========================
                 JOB
            ========================== -->

            <td>
              {{ student.job_title || "N/A" }}
            </td>


            <!-- =========================
                 BRANCH
            ========================== -->

            <td>
              {{ student.branch || "N/A" }}
            </td>


            <!-- =========================
                 CGPA
            ========================== -->

            <td>
              {{ student.cgpa ?? "N/A" }}
            </td>


            <!-- =========================
                 RESUME
            ========================== -->

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


            <!-- =========================
                 STATUS
            ========================== -->

            <td>

              <span
                class="badge"
                :class="getStatusClass(student.status)"
              >

                {{ student.status || "Applied" }}

              </span>

            </td>


            <!-- =========================
                 ACTIONS
            ========================== -->

            <td>

              <!-- Shortlist -->

              <button
                class="btn btn-warning btn-sm me-1 mb-1"
                :disabled="
                  processingId === student.application_id
                "
                @click="
                  updateStatus(
                    student.application_id,
                    'Shortlisted'
                  )
                "
              >

                Shortlist

              </button>


              <!-- Reject -->

              <button
                class="btn btn-danger btn-sm me-1 mb-1"
                :disabled="
                  processingId === student.application_id
                "
                @click="
                  updateStatus(
                    student.application_id,
                    'Rejected'
                  )
                "
              >

                Reject

              </button>


              <!-- Select -->

              <button
                class="btn btn-success btn-sm me-1 mb-1"
                :disabled="
                  processingId === student.application_id
                "
                @click="
                  updateStatus(
                    student.application_id,
                    'Selected'
                  )
                "
              >

                Select

              </button>


              <!-- =========================
                   SCHEDULE INTERVIEW
              ========================== -->

              <button
                v-if="
                  !scheduledInterviews.includes(
                    student.application_id
                  )
                "
                class="btn btn-primary btn-sm mb-1"
                @click="openInterview(student)"
              >

                Schedule Interview

              </button>


              <!-- =========================
                   INTERVIEW SCHEDULED
              ========================== -->

              <button
                v-else
                class="btn btn-success btn-sm mb-1"
                disabled
              >

                ✓ Interview Scheduled

              </button>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>


  <!-- =====================================================
       INTERVIEW MODAL
  ====================================================== -->

  <div
    v-if="showInterview"
    class="modal d-block"
    tabindex="-1"
    style="background: rgba(0,0,0,0.5);"
  >

    <div class="modal-dialog">

      <div class="modal-content">


        <!-- =========================
             MODAL HEADER
        ========================== -->

        <div class="modal-header">

          <h5 class="modal-title">
            Schedule Interview
          </h5>


          <button
            type="button"
            class="btn-close"
            @click="closeInterview"
          ></button>

        </div>


        <!-- =========================
             MODAL BODY
        ========================== -->

        <div class="modal-body">


          <!-- Student -->

          <div class="mb-3">

            <p class="mb-1">

              <strong>
                Student:
              </strong>

              {{ selectedStudent?.student_name || "N/A" }}

            </p>


            <p class="mb-0">

              <strong>
                Email:
              </strong>

              {{ selectedStudent?.email || "N/A" }}

            </p>

          </div>


          <!-- Interview Date -->

          <div class="mb-3">

            <label class="form-label">
              Interview Date & Time
            </label>


            <input
              v-model="interviewDate"
              type="datetime-local"
              class="form-control"
            />

          </div>


          <!-- Interview Type -->

          <div class="mb-3">

            <label class="form-label">
              Interview Type
            </label>


            <select
              v-model="interviewType"
              class="form-select"
            >

              <option value="">
                Select type
              </option>

              <option value="Online">
                Online
              </option>

              <option value="Offline">
                Offline
              </option>

              <option value="Phone">
                Phone
              </option>

            </select>

          </div>


          <!-- Remarks -->

          <div class="mb-3">

            <label class="form-label">
              Remarks
            </label>


            <textarea
              v-model="remarks"
              class="form-control"
              rows="3"
              placeholder="Enter interview details or remarks..."
            ></textarea>

          </div>

        </div>


        <!-- =========================
             MODAL FOOTER
        ========================== -->

        <div class="modal-footer">

          <button
            type="button"
            class="btn btn-secondary"
            @click="closeInterview"
          >

            Cancel

          </button>


          <button
            type="button"
            class="btn btn-primary"
            :disabled="scheduling"
            @click="scheduleInterview"
          >

            <span
              v-if="scheduling"
              class="spinner-border spinner-border-sm me-1"
            ></span>

            {{
              scheduling
                ? "Scheduling..."
                : "Schedule Interview"
            }}

          </button>

        </div>

      </div>

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
// DRIVE ID
// =========================================================

const driveId = route.params.id


// =========================================================
// STATE
// =========================================================

const applicants = ref([])

const loading = ref(true)

const error = ref("")


// Application IDs whose interviews
// have already been scheduled
const scheduledInterviews = ref([])


// Currently processing status update
const processingId = ref(null)


// =========================================================
// INTERVIEW STATE
// =========================================================

const showInterview = ref(false)

const selectedStudent = ref(null)

const interviewDate = ref("")

const interviewType = ref("")

const remarks = ref("")

const scheduling = ref(false)


// =========================================================
// BACKEND URL
// =========================================================

const BACKEND_URL =
  "http://localhost:5000"


// =========================================================
// GET AUTH HEADERS
// =========================================================

function getHeaders() {

  return {

    headers: {

      Authorization:
        `Bearer ${localStorage.getItem("token")}`

    }

  }

}


// =========================================================
// LOAD APPLICANTS
// =========================================================

async function loadApplicants() {

  loading.value = true

  error.value = ""


  try {

    if (!driveId) {

      error.value =
        "Drive ID is missing from the URL."

      return

    }


    const response = await axios.get(

      `/api/company/drives/${driveId}/applicants`,

      getHeaders()

    )


    applicants.value =
      Array.isArray(response.data)
        ? response.data
        : []


    /*
      Check which applicants already
      have an interview scheduled.

      This expects the backend applicants
      API to return something like:

      {
        application_id: 1,
        interview_scheduled: true
      }

      OR:

      {
        application_id: 1,
        interview: {...}
      }
    */

    scheduledInterviews.value =
      applicants.value
        .filter(student =>
          student.interview_scheduled === true ||
          student.interview != null
        )
        .map(student =>
          student.application_id
        )


  } catch (err) {

    console.error(
      "Error loading applicants:",
      err
    )


    error.value =
      err.response?.data?.message ||
      "Failed to load applicants."

  } finally {

    loading.value = false

  }

}


// =========================================================
// UPDATE APPLICATION STATUS
// =========================================================

async function updateStatus(
  applicationId,
  status
) {

  processingId.value =
    applicationId


  try {

    await axios.put(

      `/api/company/applications/${applicationId}/status`,

      {
        status: status
      },

      getHeaders()

    )


    /*
      Update UI immediately
    */

    const applicant =
      applicants.value.find(
        student =>
          student.application_id ===
          applicationId
      )


    if (applicant) {

      applicant.status =
        status

    }

  } catch (err) {

    console.error(
      "Error updating status:",
      err
    )


    alert(
      err.response?.data?.message ||
      "Failed to update application status."
    )

  } finally {

    processingId.value = null

  }

}


// =========================================================
// OPEN INTERVIEW MODAL
// =========================================================

function openInterview(student) {

  selectedStudent.value =
    student


  interviewDate.value = ""

  interviewType.value = ""

  remarks.value = ""


  showInterview.value =
    true

}


// =========================================================
// CLOSE INTERVIEW MODAL
// =========================================================

function closeInterview() {

  showInterview.value =
    false


  selectedStudent.value =
    null


  interviewDate.value =
    ""

  interviewType.value =
    ""

  remarks.value =
    ""

}


// =========================================================
// SCHEDULE INTERVIEW
// =========================================================

async function scheduleInterview() {

  if (!selectedStudent.value) {

    alert(
      "Please select a student."
    )

    return

  }


  if (!interviewDate.value) {

    alert(
      "Please select interview date and time."
    )

    return

  }


  if (!interviewType.value) {

    alert(
      "Please select interview type."
    )

    return

  }


  scheduling.value =
    true


  try {

    const applicationId =
      selectedStudent.value.application_id


    await axios.post(

      `/api/company/applications/${applicationId}/interview`,

      {

        interview_date:
          interviewDate.value,

        interview_type:
          interviewType.value,

        remarks:
          remarks.value

      },

      getHeaders()

    )


    /*
      IMPORTANT:

      Add application ID to the
      scheduled interviews list.

      This immediately changes:

      Schedule Interview
              ↓
      ✓ Interview Scheduled
    */

    if (
      !scheduledInterviews.value.includes(
        applicationId
      )
    ) {

      scheduledInterviews.value.push(
        applicationId
      )

    }


    /*
      Close modal
    */

    closeInterview()


    /*
      Success message
    */

    alert(
      "Interview scheduled successfully."
    )


  } catch (err) {

    console.error(
      "Error scheduling interview:",
      err
    )


    alert(
      err.response?.data?.message ||
      "Failed to schedule interview."
    )

  } finally {

    scheduling.value =
      false

  }

}


// =========================================================
// STATUS BADGE
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
// RESUME URL
// =========================================================

function getResumeUrl(resume) {

  if (!resume) {

    return ""

  }


  if (
    resume.startsWith("http://") ||
    resume.startsWith("https://")
  ) {

    return resume

  }


  if (
    resume.startsWith("/uploads/")
  ) {

    return `${BACKEND_URL}${resume}`

  }


  return `${BACKEND_URL}/uploads/${encodeURIComponent(resume)}`

}


// =========================================================
// BACK TO DRIVES
// =========================================================

function goBack() {

  router.push(
    "/company/drives"
  )

}


// =========================================================
// LOAD PAGE
// =========================================================

onMounted(() => {

  loadApplicants()

})

</script>

