<template>
  <div class="container mt-4">

    <h2 class="mb-4">Placement Drives</h2>

    <input
      class="form-control mb-3"
      placeholder="Search Job Title..."
      v-model="search"
    />

    <table class="table table-bordered table-hover">

      <thead class="table-dark">
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Branch</th>
          <th>Minimum CGPA</th>
          <th>Deadline</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="drive in filteredDrives"
          :key="drive.id"
        >
          <td>{{ drive.company }}</td>
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.eligibility_branch }}</td>
          <td>{{ drive.cgpa }}</td>
          <td>{{ drive.deadline }}</td>

          <td>

            <button
              v-if="!drive.already_applied"
              class="btn btn-primary btn-sm"
              @click="apply(drive.id)"
            >
              Apply
            </button>

            <span
              v-else
              class="badge bg-success"
            >
              Applied
            </span>

          </td>

        </tr>

        <tr v-if="filteredDrives.length === 0">
          <td colspan="6" class="text-center">
            No Placement Drives Found
          </td>
        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../../services/api";

const drives = ref([]);
const search = ref("");

const filteredDrives = computed(() => {
  return drives.value.filter((drive) =>
    drive.job_title
      .toLowerCase()
      .includes(search.value.toLowerCase())
  );
});

async function loadDrives() {
  try {
    const response = await api.get("/student/drives");
    drives.value = response.data;
  } catch (err) {
    console.error(err);
    alert("Failed to load drives.");
  }
}

async function apply(id) {
  try {
    const response = await api.post(
      `/student/drives/${id}/apply`
    );

    alert(response.data.message);

    await loadDrives();
  } catch (err) {
    console.error(err);

    alert(
      err.response?.data?.message ||
      "Application failed."
    );
  }
}

onMounted(() => {
  loadDrives();
});
</script>