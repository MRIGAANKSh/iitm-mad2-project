<template>

  <div class="container mt-4">


<h2 class="mb-4">
  Student Dashboard
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
    Loading dashboard...
  </p>
</div>


<!-- Error -->
<div
  v-else-if="error"
  class="alert alert-danger"
>
  {{ error }}
</div>


<!-- Dashboard -->
<div v-else>

  <div class="row g-4">

    <!-- Available Drives -->
    <div class="col-md-3">

      <div class="card shadow-sm text-center h-100">

        <div class="card-body">

          <h5 class="card-title">
            Available Drives
          </h5>

          <h2 class="text-primary">
            {{ dashboard.drives || 0 }}
          </h2>

          <p class="text-muted mb-0">
            Approved placement drives
          </p>

        </div>

      </div>

    </div>


    <!-- Applications -->
    <div class="col-md-3">

      <div class="card shadow-sm text-center h-100">

        <div class="card-body">

          <h5 class="card-title">
            Applications
          </h5>

          <h2 class="text-info">
            {{ dashboard.applications || 0 }}
          </h2>

          <p class="text-muted mb-0">
            Applications submitted
          </p>

        </div>

      </div>

    </div>


    <!-- Shortlisted -->
    <div class="col-md-3">

      <div class="card shadow-sm text-center h-100">

        <div class="card-body">

          <h5 class="card-title">
            Shortlisted
          </h5>

          <h2 class="text-warning">
            {{ dashboard.shortlisted || 0 }}
          </h2>

          <p class="text-muted mb-0">
            Applications shortlisted
          </p>

        </div>

      </div>

    </div>


    <!-- Selected -->
    <div class="col-md-3">

      <div class="card shadow-sm text-center h-100">

        <div class="card-body">

          <h5 class="card-title">
            Selected
          </h5>

          <h2 class="text-success">
            {{ dashboard.selected || 0 }}
          </h2>

          <p class="text-muted mb-0">
            Final selections
          </p>

        </div>

      </div>

    </div>

  </div>

</div>


  </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../../services/api";


const dashboard = ref({
  drives: 0,
  applications: 0,
  shortlisted: 0,
  selected: 0
});

const loading = ref(true);
const error = ref("");


async function loadDashboard() {

  loading.value = true;
  error.value = "";

  try {

    const response = await api.get(
      "/student/dashboard"
    );

    dashboard.value = {
      drives: response.data.drives ?? 0,
      applications: response.data.applications ?? 0,
      shortlisted: response.data.shortlisted ?? 0,
      selected: response.data.selected ?? 0
    };

  } catch (err) {

    console.error(
      "Failed to load student dashboard:",
      err
    );

    error.value =
      err.response?.data?.message ||
      "Failed to load dashboard.";

  } finally {

    loading.value = false;

  }

}


onMounted(() => {
  loadDashboard();
});

</script>
