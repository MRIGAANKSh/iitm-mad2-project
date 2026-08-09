
<template>

  <!-- =========================================
       HEADER
  ========================================== -->

  <div
    class="d-flex justify-content-between align-items-center mb-4"
  >

    <div>

      <h2 class="mb-1">
        Applications
      </h2>

      <p class="text-muted mb-0">
        View and manage all placement applications.
      </p>

    </div>


    <!-- Refresh -->

    <button
      class="btn btn-outline-primary"
      :disabled="loading"
      @click="loadApplications"
    >

      <span
        v-if="loading"
        class="spinner-border spinner-border-sm me-2"
      ></span>

      🔄 Refresh

    </button>

  </div>


  <!-- =========================================
       LOADING
  ========================================== -->

  <div
    v-if="loading"
    class="text-center py-5"
  >

    <div
      class="spinner-border text-primary"
      role="status"
    ></div>

    <p class="mt-2 text-muted">
      Loading applications...
    </p>

  </div>


  <!-- =========================================
       NO APPLICATIONS
  ========================================== -->

  <div
    v-else-if="applications.length === 0"
    class="alert alert-info"
  >

    No applications found.

  </div>


  <!-- =========================================
       APPLICATIONS
  ========================================== -->

  <div
    v-else
    class="card shadow-sm border-0"
  >


    <!-- =====================================
         FILTER SECTION
    ====================================== -->

    <div class="card-body border-bottom">

      <div class="row g-3">


        <!-- Search -->

        <div class="col-md-6">

          <label class="form-label fw-semibold">
            Search Applications
          </label>

          <input
            v-model="search"
            type="text"
            class="form-control"
            placeholder="Search student, email, ID, company, job..."
          />

        </div>


        <!-- Status -->

        <div class="col-md-3">

          <label class="form-label fw-semibold">
            Status
          </label>

          <select
            v-model="statusFilter"
            class="form-select"
          >

            <option value="all">
              All Statuses
            </option>

            <option value="applied">
              Applied
            </option>

            <option value="shortlisted">
              Shortlisted
            </option>

            <option value="selected">
              Selected
            </option>

            <option value="rejected">
              Rejected
            </option>

          </select>

        </div>


        <!-- Company -->

        <div class="col-md-3">

          <label class="form-label fw-semibold">
            Company
          </label>

          <select
            v-model="companyFilter"
            class="form-select"
          >

            <option value="all">
              All Companies
            </option>

            <option
              v-for="company in companies"
              :key="company"
              :value="company"
            >

              {{ company }}

            </option>

          </select>

        </div>

      </div>


      <!-- Clear Filters -->

      <div
        v-if="
          search ||
          statusFilter !== 'all' ||
          companyFilter !== 'all'
        "
        class="mt-3"
      >

        <button
          class="btn btn-sm btn-outline-secondary"
          @click="clearFilters"
        >

          ✕ Clear Filters

        </button>

      </div>

    </div>


    <!-- =====================================
         CARD BODY
    ====================================== -->

    <div class="card-body">


      <!-- Result Count -->

      <div
        v-if="filteredApplications.length > 0"
        class="mb-3 text-muted"
      >

        Showing

        <strong>
          {{ filteredApplications.length }}
        </strong>

        of

        <strong>
          {{ applications.length }}
        </strong>

        applications

      </div>


      <!-- =====================================
           NO FILTER RESULTS
      ====================================== -->

      <div
        v-if="filteredApplications.length === 0"
        class="alert alert-warning"
      >

        No applications match your current filters.

      </div>


      <!-- =====================================
           TABLE
      ====================================== -->

      <div
        v-else
        class="table-responsive"
      >

        <table
          class="table table-hover table-bordered align-middle"
        >

          <thead class="table-light">

            <tr>

              <th>
                Student
              </th>

              <th>
                Student ID
              </th>

              <th>
                Branch
              </th>

              <th>
                CGPA
              </th>

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
                Applied
              </th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="
                application in filteredApplications
              "
              :key="application.id"
            >


              <!-- Student -->

              <td>

                <strong>
                  {{ application.student_name || "N/A" }}
                </strong>

                <br>

                <small class="text-muted">

                  {{
                    application.student_email ||
                    "No email"
                  }}

                </small>

              </td>


              <!-- Student ID -->

              <td>

                {{ application.student_id || "N/A" }}

              </td>


              <!-- Branch -->

              <td>

                {{ application.branch || "N/A" }}

              </td>


              <!-- CGPA -->

              <td>

                {{ application.cgpa ?? "N/A" }}

              </td>


              <!-- Company -->

              <td>

                {{ application.company || "N/A" }}

              </td>


              <!-- Job -->

              <td>

                {{ application.job_title || "N/A" }}

              </td>


              <!-- Status -->

              <td>

                <span
                  class="badge"
                  :class="
                    statusClass(
                      application.status
                    )
                  "
                >

                  {{
                    application.status ||
                    "Applied"
                  }}

                </span>

              </td>


              <!-- Applied Date -->

              <td>

                {{
                  formatDate(
                    application.applied_at
                  )
                }}

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
  computed,
  onMounted
} from "vue";

import api from "../../services/api";


// =========================================================
// STATE
// =========================================================

const applications = ref([]);

const loading = ref(true);

const search = ref("");

const statusFilter = ref("all");

const companyFilter = ref("all");


// =========================================================
// LOAD APPLICATIONS
// =========================================================

async function loadApplications() {

  loading.value = true;

  try {

    const response =
      await api.get(
        "/admin/applications"
      );


    console.log(
      "Admin Applications:",
      response.data
    );


    applications.value =
      Array.isArray(response.data)
        ? response.data
        : [];

  }

  catch (error) {

    console.error(
      "Failed to load applications:",
      error
    );


    alert(
      error?.response?.data?.message ||
      "Failed to load applications."
    );

  }

  finally {

    loading.value = false;

  }

}


// =========================================================
// COMPANY LIST
// =========================================================

const companies = computed(() => {

  return [

    ...new Set(

      applications.value
        .map(
          application =>
            application.company
        )
        .filter(Boolean)

    )

  ];

});


// =========================================================
// FILTERED APPLICATIONS
// =========================================================

const filteredApplications = computed(() => {

  let result =
    applications.value;


  // -----------------------------------------
  // SEARCH
  // -----------------------------------------

  if (search.value.trim()) {

    const query =
      search.value
        .toLowerCase()
        .trim();


    result =
      result.filter(
        application => {

          const studentName =
            application.student_name
              ?.toString()
              .toLowerCase() || "";


          const studentEmail =
            application.student_email
              ?.toString()
              .toLowerCase() || "";


          const studentId =
            application.student_id
              ?.toString()
              .toLowerCase() || "";


          const company =
            application.company
              ?.toString()
              .toLowerCase() || "";


          const job =
            application.job_title
              ?.toString()
              .toLowerCase() || "";


          const branch =
            application.branch
              ?.toString()
              .toLowerCase() || "";


          return (

            studentName.includes(query) ||

            studentEmail.includes(query) ||

            studentId.includes(query) ||

            company.includes(query) ||

            job.includes(query) ||

            branch.includes(query)

          );

        }
      );

  }


  // -----------------------------------------
  // STATUS FILTER
  // -----------------------------------------

  if (
    statusFilter.value !== "all"
  ) {

    result =
      result.filter(
        application => {

          const status =
            application.status
              ?.toString()
              .toLowerCase();


          return (
            status ===
            statusFilter.value
          );

        }
      );

  }


  // -----------------------------------------
  // COMPANY FILTER
  // -----------------------------------------

  if (
    companyFilter.value !== "all"
  ) {

    result =
      result.filter(
        application => {

          return (
            application.company ===
            companyFilter.value
          );

        }
      );

  }


  return result;

});


// =========================================================
// CLEAR FILTERS
// =========================================================

function clearFilters() {

  search.value = "";

  statusFilter.value = "all";

  companyFilter.value = "all";

}


// =========================================================
// FORMAT DATE
// =========================================================

function formatDate(date) {

  if (!date) {

    return "-";

  }


  const parsed =
    new Date(date);


  if (
    Number.isNaN(
      parsed.getTime()
    )
  ) {

    return date;

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
  );

}


// =========================================================
// STATUS CLASS
// =========================================================

function statusClass(status) {

  switch (
    status?.toString().toLowerCase()
  ) {

    case "selected":

      return "bg-success";


    case "shortlisted":

      return "bg-warning text-dark";


    case "rejected":

      return "bg-danger";


    case "applied":

      return "bg-primary";


    default:

      return "bg-secondary";

  }

}


// =========================================================
// LOAD PAGE
// =========================================================

onMounted(() => {

  loadApplications();

});

</script>

