<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>My Placement Drives</h2>

      <RouterLink
        to="/company/create-drive"
        class="btn btn-primary"
      >
        + Create Drive
      </RouterLink>
    </div>

    <table class="table table-bordered table-hover">

      <thead class="table-dark">
        <tr>
          <th>Job Title</th>
          <th>Deadline</th>
          <th>Status</th>
          <th>Applicants</th>
          <th width="230">Actions</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="drive in drives"
          :key="drive.id"
        >
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.deadline }}</td>
          <td>
            <span
              class="badge"
              :class="drive.status === 'closed'
                ? 'bg-danger'
                : 'bg-success'"
            >
              {{ drive.status }}
            </span>
          </td>

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
              :disabled="drive.status === 'closed'"
            >
              Close
            </button>

            <button
              class="btn btn-danger btn-sm"
              v-if="drive.applicants === 0"
              @click="deleteDrive(drive.id)"
            >
              Delete
            </button>

          </td>

        </tr>

        <tr v-if="drives.length === 0">
          <td colspan="5" class="text-center py-4">
            No placement drives found.
          </td>
        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../../services/api";

const router = useRouter();

const drives = ref([]);

async function loadDrives() {
  try {
    const response = await api.get("/company/drives");
    drives.value = response.data;
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.message || "Failed to load drives.");
  }
}

function editDrive(id) {
  router.push(`/company/edit-drive/${id}`);
}

async function closeDrive(id) {
  if (!confirm("Are you sure you want to close this drive?"))
    return;

  try {
    await api.put(`/company/drives/${id}/close`);
    alert("Drive closed successfully.");
    loadDrives();
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.message || "Unable to close drive.");
  }
}

async function deleteDrive(id) {
  if (!confirm("Are you sure you want to delete this drive?"))
    return;

  try {
    await api.delete(`/company/drives/${id}`);
    alert("Drive deleted successfully.");
    loadDrives();
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.message || "Unable to delete drive.");
  }
}

onMounted(() => {
  loadDrives();
});
</script>