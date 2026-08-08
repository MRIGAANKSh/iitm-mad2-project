<template>
  <div>
    <!-- Stats Card -->
    <div class="card shadow-sm mb-4">
      <div class="card-body text-center">
        <h6 class="text-muted">{{ title }}</h6>
        <h1 class="display-5">{{ value }}</h1>
      </div>
    </div>

   
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