
<template>

  <div>

    <!-- =====================================================
         HEADER
    ====================================================== -->

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >

      <div>

        <h2>
          My Applications
        </h2>

        <p class="text-muted mb-0">
          Track your placement applications and interviews
        </p>

      </div>


      <!-- Export -->

      <button
        class="btn btn-success"
        :disabled="exporting || loading"
        @click="exportApplications"
      >

        <span
          v-if="exporting"
          class="spinner-border spinner-border-sm me-2"
          role="status"
        ></span>

        {{
          exporting
            ? "Exporting..."
            : "Export Applications CSV"
        }}

      </button>

    </div>


    <!-- =====================================================
         LOADING
    ====================================================== -->

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


    <!-- =====================================================
         ERROR
    ====================================================== -->

    <div
      v-else-if="error"
      class="alert alert-danger"
    >

      {{ error }}

    </div>


    <!-- =====================================================
         APPLICATION CONTENT
    ====================================================== -->

    <div v-else>


      <!-- =================================================
           NO APPLICATIONS
      ================================================== -->

      <div
        v-if="applications.length === 0"
        class="alert alert-info"
      >

        You have not applied to any placement drives yet.

      </div>


      <!-- =================================================
           APPLICATION TABLE
      ================================================== -->

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

              <th style="min-width: 280px;">
                Interview
              </th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="(app, index) in applications"
              :key="
                app.application_id || index
              "
            >

              <!-- ==========================================
                   COMPANY
              =========================================== -->

              <td>

                <strong>
                  {{ app.company || "N/A" }}
                </strong>

              </td>


              <!-- ==========================================
                   JOB
              =========================================== -->

              <td>

                {{ app.job_title || "N/A" }}

              </td>


              <!-- ==========================================
                   APPLICATION STATUS
              =========================================== -->

              <td>

                <span
                  class="badge"
                  :class="
                    getStatusClass(app.status)
                  "
                >

                  {{
                    app.status ||
                    "Applied"
                  }}

                </span>

              </td>


              <!-- ==========================================
                   APPLIED DATE
              =========================================== -->

              <td>

                {{ formatDate(app.date) }}

              </td>


              <!-- ==========================================
                   INTERVIEW
              =========================================== -->

              <td>


                <!-- ========================================
                     INTERVIEW EXISTS
                ========================================= -->

                <div
                  v-if="app.interview"
                >

                  <!-- Interview Scheduled -->

                  <div class="mb-2">

                    <span
                      class="badge bg-success"
                    >

                      ✓ Interview Scheduled

                    </span>

                  </div>


                  <!-- Interview Date -->

                  <div class="small mb-2">

                    <strong>
                      Date & Time:
                    </strong>

                    <br>

                    {{
                      formatInterviewDate(
                        app.interview.date
                      )
                    }}

                  </div>


                  <!-- Interview Type -->

                  <div class="small mb-2">

                    <strong>
                      Type:
                    </strong>

                    {{
                      app.interview.type ||
                      "N/A"
                    }}

                  </div>


                  <!-- Interview Status -->

                  <div class="small mb-2">

                    <strong>
                      Status:
                    </strong>

                    <span
                      class="badge ms-1"
                      :class="
                        getInterviewStatusClass(
                          app.interview.status
                        )
                      "
                    >

                      {{
                        app.interview.status ||
                        "Scheduled"
                      }}

                    </span>

                  </div>


                  <!-- Interview Remarks -->

                  <div
                    v-if="
                      app.interview.remarks
                    "
                    class="small"
                  >

                    <strong>
                      Remarks:
                    </strong>

                    <br>

                    <span class="text-muted">

                      {{
                        app.interview.remarks
                      }}

                    </span>

                  </div>

                </div>


                <!-- ========================================
                     NO INTERVIEW
                ========================================= -->

                <span
                  v-else
                  class="text-muted"
                >

                  No interview scheduled

                </span>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>

</template>


<script setup>

import {
  ref,
  onMounted
} from "vue"

import api from "../../services/api"


// =========================================================
// STATE
// =========================================================

const applications = ref([])

const loading = ref(true)

const error = ref("")

const exporting = ref(false)


// =========================================================
// LOAD APPLICATIONS
// =========================================================

async function loadApplications() {

  loading.value = true

  error.value = ""


  try {

    const response =
      await api.get(
        "/student/applications"
      )


    console.log(
      "Applications:",
      response.data
    )


    applications.value =
      Array.isArray(
        response.data
      )
        ? response.data
        : []


  } catch (err) {

    console.error(
      "Failed to load applications:",
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
// EXPORT APPLICATIONS CSV
// =========================================================
//
// CSV includes:
//
// Application ID
// Company
// Job
// Application Status
// Applied Date
// Interview Status
// Interview Date & Time
// Interview Type
// Interview Remarks
//
// =========================================================

async function exportApplications() {

  exporting.value = true


  try {

    // -------------------------------------------------------
    // Make sure we have application data
    // -------------------------------------------------------

    if (
      !applications.value.length
    ) {

      await loadApplications()

    }


    // -------------------------------------------------------
    // Stop if there are no applications
    // -------------------------------------------------------

    if (
      !applications.value.length
    ) {

      alert(
        "No applications available to export."
      )

      return

    }


    // -------------------------------------------------------
    // CSV HEADERS
    // -------------------------------------------------------

    const headers = [

      "Application ID",

      "Company",

      "Job Title",

      "Application Status",

      "Applied Date",

      "Interview Status",

      "Interview Date & Time",

      "Interview Type",

      "Interview Remarks"

    ]


    // -------------------------------------------------------
    // CSV ESCAPE FUNCTION
    // -------------------------------------------------------

    function escapeCSV(value) {

      if (
        value === null ||
        value === undefined
      ) {

        return ""

      }


      const stringValue =
        String(value)
          .replace(
            /"/g,
            '""'
          )


      return `"${stringValue}"`

    }


    // -------------------------------------------------------
    // CREATE CSV ROWS
    // -------------------------------------------------------

    const rows =
      applications.value.map(
        (app) => {

          const interview =
            app.interview || null


          return [

            // Application ID

            app.application_id ||
              "",


            // Company

            app.company ||
              "",


            // Job

            app.job_title ||
              "",


            // Application Status

            app.status ||
              "Applied",


            // Applied Date

            app.date
              ? formatDate(
                  app.date
                )
              : "",


            // Interview Status

            interview
              ? (
                  interview.status ||
                  "Scheduled"
                )
              : "No Interview",


            // Interview Date

            interview
              ? formatInterviewDate(
                  interview.date
                )
              : "",


            // Interview Type

            interview
              ? (
                  interview.type ||
                  ""
                )
              : "",


            // Interview Remarks

            interview
              ? (
                  interview.remarks ||
                  ""
                )
              : ""

          ]

        }
      )


    // -------------------------------------------------------
    // BUILD CSV
    // -------------------------------------------------------

    const csv = [

      headers
        .map(
          escapeCSV
        )
        .join(","),


      ...rows.map(
        row =>
          row
            .map(
              escapeCSV
            )
            .join(",")
      )

    ].join("\n")


    // -------------------------------------------------------
    // UTF-8 BOM
    // Helps Excel display CSV correctly
    // -------------------------------------------------------

    const csvWithBOM =
      "\uFEFF" + csv


    // -------------------------------------------------------
    // CREATE BLOB
    // -------------------------------------------------------

    const blob =
      new Blob(
        [
          csvWithBOM
        ],
        {
          type:
            "text/csv;charset=utf-8;"
        }
      )


    // -------------------------------------------------------
    // CREATE DOWNLOAD URL
    // -------------------------------------------------------

    const url =
      window.URL.createObjectURL(
        blob
      )


    // -------------------------------------------------------
    // CREATE DOWNLOAD LINK
    // -------------------------------------------------------

    const link =
      document.createElement(
        "a"
      )


    link.href = url


    link.download =
      "my_applications.csv"


    document.body.appendChild(
      link
    )


    link.click()


    document.body.removeChild(
      link
    )


    // -------------------------------------------------------
    // CLEANUP
    // -------------------------------------------------------

    window.URL.revokeObjectURL(
      url
    )


  } catch (err) {

    console.error(
      "Failed to export applications:",
      err
    )


    alert(
      err.response?.data?.message ||
      "Failed to export applications."
    )


  } finally {

    exporting.value = false

  }

}


// =========================================================
// APPLICATION STATUS CLASS
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
// INTERVIEW STATUS CLASS
// =========================================================

function getInterviewStatusClass(
  status
) {

  switch (status) {

    case "Scheduled":

      return "bg-success"


    case "Completed":

      return "bg-primary"


    case "Cancelled":

      return "bg-danger"


    default:

      return "bg-secondary"

  }

}


// =========================================================
// FORMAT APPLICATION DATE
// =========================================================

function formatDate(date) {

  if (!date) {

    return "N/A"

  }


  const parsed =
    new Date(date)


  if (
    Number.isNaN(
      parsed.getTime()
    )
  ) {

    return date

  }


  return parsed.toLocaleDateString(
    "en-IN",
    {

      day: "2-digit",

      month: "short",

      year: "numeric"

    }
  )

}


// =========================================================
// FORMAT INTERVIEW DATE
// =========================================================

function formatInterviewDate(
  date
) {

  if (!date) {

    return "N/A"

  }


  const parsed =
    new Date(date)


  if (
    Number.isNaN(
      parsed.getTime()
    )
  ) {

    return date

  }


  return parsed.toLocaleString(
    "en-IN",
    {

      day: "2-digit",

      month: "short",

      year: "numeric",

      hour: "2-digit",

      minute: "2-digit"

    }
  )

}


// =========================================================
// LOAD PAGE
// =========================================================

onMounted(() => {

  loadApplications()

})

</script>
