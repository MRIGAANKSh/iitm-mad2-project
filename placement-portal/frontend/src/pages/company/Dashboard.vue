<template>
  <div class="container mt-4">

    <h2 class="mb-4">{{ companyName }} Dashboard</h2>

    <div class="row">

      <div class="col-md-4">
        <DashboardCard
          title="Placement Drives"
          :value="drives"
        />
      </div>

      <div class="col-md-4">
        <DashboardCard
          title="Applicants"
          :value="applications"
        />
      </div>

      <div class="col-md-4">
        <DashboardCard
          title="Approval Status"
          :value="approvalStatus"
        />
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DashboardCard from "../../components/DashboardCard.vue";
import api from "../../services/api";

const companyName = ref("");
const approvalStatus = ref("");

const drives = ref(0);
const applications = ref(0);

async function loadDashboard() {
  try {
    const res = await api.get("/company/dashboard");

    companyName.value = res.data.company_name;
    approvalStatus.value = res.data.approval_status;
    drives.value = res.data.total_drives;
    applications.value = res.data.total_applicants;

  } catch (err) {
    console.error(err);
    alert("Failed to load dashboard.");
  }
}

onMounted(() => {
  loadDashboard();
});
</script>