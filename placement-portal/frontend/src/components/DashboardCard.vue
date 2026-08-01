<template>
  <div>
    <!-- Stats Card -->
    <div class="card shadow-sm mb-4">
      <div class="card-body text-center">
        <h6 class="text-muted">{{ title }}</h6>
        <h1 class="display-5">{{ value }}</h1>
      </div>
    </div>

    <!-- Pending Companies -->
    <h4 class="mt-5">Pending Companies</h4>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Name</th>
          <th>HR</th>
          <th>Website</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="company in companies"
          :key="company.id"
        >
          <td>{{ company.company_name }}</td>
          <td>{{ company.hr_name }}</td>
          <td>{{ company.website }}</td>
          <td>
            <button
              class="btn btn-success btn-sm me-2"
              @click="approve(company.id)"
            >
              Approve
            </button>

            <button
              class="btn btn-danger btn-sm"
              @click="reject(company.id)"
            >
              Reject
            </button>
          </td>
        </tr>

        <tr v-if="companies.length === 0">
          <td colspan="4" class="text-center">
            No pending companies
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api"; // Adjust path if needed

defineProps({
  title: String,
  value: Number,
});

const companies = ref([]);

async function loadCompanies() {
  const response = await api.get("/admin/companies/pending");
  companies.value = response.data;
}

async function approve(id) {
  await api.put(`/admin/companies/${id}/approve`);
  await loadCompanies();
}

async function reject(id) {
  await api.put(`/admin/companies/${id}/reject`);
  await loadCompanies();
}

onMounted(() => {
  loadCompanies();
});
</script>