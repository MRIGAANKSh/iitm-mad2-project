<template>
  <div class="container mt-4">
    <h3>My Drives</h3>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Job Title</th>
          <th>Deadline</th>
          <th>Status</th>
          <th>Applicants</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="drive in drives"
          :key="drive.id"
        >
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.deadline }}</td>
          <td>{{ drive.status }}</td>
          <td>{{ drive.applicants }}</td>

          <td>
            <button
              class="btn btn-warning btn-sm me-2"
              @click="editDrive(drive.id)"
            >
              Edit
            </button>

            <button
              class="btn btn-secondary btn-sm me-2"
              @click="closeDrive(drive.id)"
            >
              Close
            </button>

            <button
              v-if="drive.applicants === 0"
              class="btn btn-danger btn-sm"
              @click="deleteDrive(drive.id)"
            >
              Delete
            </button>
          </td>
        </tr>

        <tr v-if="drives.length === 0">
          <td colspan="5" class="text-center">
            No drives found.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const drives = ref([]);

async function loadDrives() {
  const response = await api.get("/company/drives");
  drives.value = response.data;
}

async function deleteDrive(id) {
  await api.delete(`/company/drives/${id}`);
  loadDrives();
}

async function closeDrive(id) {
  await api.put(`/company/drives/${id}/close`);
  loadDrives();
}

function editDrive(id) {
  console.log("Edit drive:", id);
}

onMounted(loadDrives);
</script>