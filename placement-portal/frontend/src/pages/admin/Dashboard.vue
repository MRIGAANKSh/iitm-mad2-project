
<template>

  <div>

    <!-- ============================= -->
    <!-- Page Header -->
    <!-- ============================= -->

    <div class="mb-4">

      <h2 class="fw-bold mb-1">
        Admin Dashboard
      </h2>

      <p class="text-muted mb-0">
        Overview of the placement portal
      </p>

    </div>


    <!-- ============================= -->
    <!-- Statistics -->
    <!-- ============================= -->

    <div class="row g-4 mb-4">

      <!-- Students -->
      <div class="col-lg-3 col-md-6">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <div class="d-flex justify-content-between align-items-center">

              <div>

                <p class="text-muted mb-2">
                  Students
                </p>

                <h2 class="fw-bold mb-0">
                  {{ dashboard.students }}
                </h2>

              </div>

              <div class="fs-1">
                
              </div>

            </div>

          </div>

        </div>

      </div>


      <!-- Companies -->
      <div class="col-lg-3 col-md-6">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <div class="d-flex justify-content-between align-items-center">

              <div>

                <p class="text-muted mb-2">
                  Companies
                </p>

                <h2 class="fw-bold mb-0">
                  {{ dashboard.companies }}
                </h2>

              </div>

              <div class="fs-1">
                
              </div>

            </div>

          </div>

        </div>

      </div>


      <!-- Placement Drives -->
      <div class="col-lg-3 col-md-6">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <div class="d-flex justify-content-between align-items-center">

              <div>

                <p class="text-muted mb-2">
                  Placement Drives
                </p>

                <h2 class="fw-bold mb-0">
                  {{ dashboard.drives }}
                </h2>

              </div>

              <div class="fs-1">
                
              </div>

            </div>

          </div>

        </div>

      </div>


      <!-- Applications -->
      <div class="col-lg-3 col-md-6">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <div class="d-flex justify-content-between align-items-center">

              <div>

                <p class="text-muted mb-2">
                  Applications
                </p>

                <h2 class="fw-bold mb-0">
                  {{ dashboard.applications }}
                </h2>

              </div>

              <div class="fs-1">
                
              </div>

            </div>

          </div>

        </div>

      </div>

    </div>


    <!-- ============================= -->
    <!-- Pending Companies -->
    <!-- ============================= -->

    <div class="card border-0 shadow-sm">

      <!-- Header -->

      <div class="card-body border-bottom">

        <div
          class="d-flex justify-content-between align-items-center"
        >

          <div>

            <h5 class="fw-bold mb-1">
              Pending Companies
            </h5>

            <p class="text-muted mb-0">
              Review companies waiting for approval
            </p>

          </div>


          <span class="badge bg-warning text-dark px-3 py-2">

            {{ pendingCompanies.length }}

            Pending

          </span>

        </div>

      </div>


      <!-- Loading -->

      <div
        v-if="loadingCompanies"
        class="card-body text-center py-4"
      >

        <div
          class="spinner-border text-primary"
          role="status"
        ></div>

        <p class="text-muted mt-2 mb-0">
          Loading pending companies...
        </p>

      </div>


      <!-- Error -->

      <div
        v-else-if="companyError"
        class="card-body"
      >

        <div class="alert alert-danger mb-0">
          {{ companyError }}
        </div>

      </div>


      <!-- No pending companies -->

      <div
        v-else-if="pendingCompanies.length === 0"
        class="card-body text-center py-4"
      >

        <div class="fs-1 mb-2">
          
        </div>

        <h6 class="fw-bold">
          No Pending Companies
        </h6>

        <p class="text-muted mb-0">
          All company registrations have been reviewed.
        </p>

      </div>


      <!-- Pending Companies List -->

      <div
        v-else
        class="list-group list-group-flush"
      >

        <div
          v-for="company in pendingCompanies"
          :key="company.id"
          class="list-group-item py-3"
        >

          <div
            class="row align-items-center"
          >

            <!-- Company Details -->

            <div class="col-md-7">

              <h6 class="fw-bold mb-1">
                {{ company.company_name }}
              </h6>

              <div class="text-muted small">

                <span>
                  HR:
                  {{ company.hr_name || "N/A" }}
                </span>

                <span
                  v-if="company.website"
                  class="ms-3"
                >

                  Website:
                  <a
                    :href="company.website"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Visit Website
                  </a>

                </span>

              </div>

            </div>


            <!-- Status -->

            <div class="col-md-2 text-md-center my-2 my-md-0">

              <span class="badge bg-warning text-dark">
                Pending
              </span>

            </div>


            <!-- Actions -->

            <div class="col-md-3 text-md-end">

              <button
                class="btn btn-success btn-sm me-2"
                :disabled="processingCompany === company.id"
                @click="approveCompany(company.id)"
              >

                <span
                  v-if="processingCompany === company.id"
                  class="spinner-border spinner-border-sm me-1"
                ></span>

                Approve

              </button>


              <button
                class="btn btn-outline-danger btn-sm"
                :disabled="processingCompany === company.id"
                @click="rejectCompany(company.id)"
              >

                Reject

              </button>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"


// ==========================================
// Dashboard Statistics
// ==========================================

const dashboard = ref({

  students: 0,

  companies: 0,

  drives: 0,

  applications: 0

})


// ==========================================
// Pending Companies
// ==========================================

const pendingCompanies = ref([])

const loadingCompanies = ref(false)

const companyError = ref("")

const processingCompany = ref(null)


// ==========================================
// Load Dashboard
// ==========================================

async function loadDashboard() {

  try {

    const response = await api.get(
      "/admin/dashboard"
    )

    dashboard.value = {

      students:
        response.data.students ?? 0,

      companies:
        response.data.companies ?? 0,

      drives:
        response.data.drives ?? 0,

      applications:
        response.data.applications ?? 0

    }

  } catch (error) {

    console.error(
      "Dashboard loading failed:",
      error
    )

  }

}


// ==========================================
// Load Pending Companies
// ==========================================

async function loadPendingCompanies() {

  loadingCompanies.value = true

  companyError.value = ""

  try {

    const response = await api.get(
      "/admin/companies/pending"
    )

    pendingCompanies.value =
      Array.isArray(response.data)
        ? response.data
        : []

  } catch (error) {

    console.error(
      "Pending companies loading failed:",
      error
    )

    companyError.value =
      error.response?.data?.message ||
      "Failed to load pending companies."

  } finally {

    loadingCompanies.value = false

  }

}


// ==========================================
// Approve Company
// ==========================================

async function approveCompany(id) {

  processingCompany.value = id

  try {

    const response = await api.put(
      `/admin/companies/${id}/approve`
    )

    alert(
      response.data.message ||
      "Company approved successfully."
    )

    // Remove company from pending list
    pendingCompanies.value =
      pendingCompanies.value.filter(
        company => company.id !== id
      )

    // Update company count
    dashboard.value.companies++

  } catch (error) {

    console.error(
      "Company approval failed:",
      error
    )

    alert(
      error.response?.data?.message ||
      "Failed to approve company."
    )

  } finally {

    processingCompany.value = null

  }

}


// ==========================================
// Reject Company
// ==========================================

async function rejectCompany(id) {

  processingCompany.value = id

  try {

    const response = await api.put(
      `/admin/companies/${id}/reject`
    )

    alert(
      response.data.message ||
      "Company rejected successfully."
    )

    // Remove company from pending list
    pendingCompanies.value =
      pendingCompanies.value.filter(
        company => company.id !== id
      )

  } catch (error) {

    console.error(
      "Company rejection failed:",
      error
    )

    alert(
      error.response?.data?.message ||
      "Failed to reject company."
    )

  } finally {

    processingCompany.value = null

  }

}


// ==========================================
// Initial Load
// ==========================================

onMounted(() => {

  loadDashboard()

  loadPendingCompanies()

})

</script>
