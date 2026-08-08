
<template>

  <div class="container-fluid">

    <!-- =========================
         HEADER
    ========================== -->

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >

      <h2 class="mb-0">
        {{ dashboard.company_name || "Company" }} Dashboard
      </h2>

      <!-- Logout -->
      <button
        class="btn btn-danger"
        @click="logout"
      >
        Logout
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

      <p class="mt-2">
        Loading dashboard...
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
         DASHBOARD
    ========================== -->

    <div v-else>

      <div class="row g-4">


        <!-- =========================
             PLACEMENT DRIVES
        ========================== -->

        <div class="col-md-4">

          <div
            class="card shadow-sm text-center h-100"
          >

            <div class="card-body">

              <h5 class="card-title">
                Placement Drives
              </h5>

              <h2 class="text-primary">
                {{ dashboard.total_drives || 0 }}
              </h2>

              <p class="text-muted mb-3">
                Drives created by your company
              </p>

              <RouterLink
                to="/company/drives"
                class="btn btn-primary btn-sm"
              >
                View Drives
              </RouterLink>

            </div>

          </div>

        </div>


        <!-- =========================
             APPLICANTS
        ========================== -->

        <div class="col-md-4">

          <div
            class="card shadow-sm text-center h-100"
          >

            <div class="card-body">

              <h5 class="card-title">
                Applicants
              </h5>

              <h2 class="text-info">
                {{ dashboard.total_applicants || 0 }}
              </h2>

              <p class="text-muted mb-3">
                Students who applied to your drives
              </p>

              <!--
                Opens ALL applicants belonging
                to this company.
              -->
              <RouterLink
                to="/company/applicants"
                class="btn btn-info btn-sm text-white"
              >
                View Applicants
              </RouterLink>

            </div>

          </div>

        </div>


        <!-- =========================
             COMPANY STATUS
        ========================== -->

        <div class="col-md-4">

          <div
            class="card shadow-sm text-center h-100"
          >

            <div class="card-body">

              <h5 class="card-title">
                Company Status
              </h5>

              <h2
                :class="
                  dashboard.approval_status === 'approved'
                    ? 'text-success'
                    : 'text-warning'
                "
              >
                {{ dashboard.approval_status || "Unknown" }}
              </h2>

              <p class="text-muted mb-0">
                Current company approval status
              </p>

            </div>

          </div>

        </div>


      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import { useRouter } from "vue-router"

import api from "../../services/api"


// =========================
// ROUTER
// =========================

const router = useRouter()


// =========================
// DASHBOARD DATA
// =========================

const dashboard = ref({

  company_name: "",

  approval_status: "",

  total_drives: 0,

  total_applicants: 0

})


// =========================
// STATES
// =========================

const loading = ref(true)

const error = ref("")


// =========================
// LOAD DASHBOARD
// =========================

async function loadDashboard() {

  loading.value = true

  error.value = ""

  try {

    const response = await api.get(
      "/company/dashboard"
    )

    dashboard.value = response.data

  }

  catch (err) {

    console.error(
      "Dashboard Error:",
      err
    )

    if (
      err.response &&
      err.response.status === 401
    ) {

      error.value =
        "Your session has expired. Please login again."

      localStorage.removeItem("token")

      setTimeout(() => {

        router.push("/")

      }, 1000)

    }

    else {

      error.value =
        err.response?.data?.message ||
        "Failed to load company dashboard."

    }

  }

  finally {

    loading.value = false

  }

}


// =========================
// LOGOUT
// =========================

function logout() {

  localStorage.removeItem("token")

  router.push("/")

}


// =========================
// LOAD ON PAGE OPEN
// =========================

onMounted(() => {

  loadDashboard()

})

</script>

