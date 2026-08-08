
<template>

  <div class="container mt-4">

    <!-- Header -->
    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >

      <h2>
        My Placement Drives
      </h2>

      <RouterLink
        to="/company/create-drive"
        class="btn btn-primary"
      >
        + Create Drive
      </RouterLink>

    </div>


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
        Loading drives...
      </p>
    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>


    <!-- Drives -->
    <div v-else>

      <table
        class="table table-bordered table-hover"
      >

        <thead class="table-dark">

          <tr>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
            <th width="350">Actions</th>
          </tr>

        </thead>


        <tbody>

          <tr
            v-for="drive in drives"
            :key="drive.id"
          >

            <td>
              {{ drive.job_title }}
            </td>

            <td>
              {{ drive.deadline }}
            </td>

            <td>

              <span
                class="badge"
                :class="
                  drive.status === 'closed'
                    ? 'bg-danger'
                    : 'bg-success'
                "
              >
                {{ drive.status }}
              </span>

            </td>


            <td>
              {{ drive.applicants }}
            </td>


            <td>

              <!-- Applicants -->
              <button
                class="btn btn-primary btn-sm me-2"
                @click="viewApplicants(drive.id)"
              >
                Applicants
              </button>


              <!-- Edit -->
              <button
                class="btn btn-warning btn-sm me-2"
                @click="editDrive(drive.id)"
              >
                Edit
              </button>


              <!-- Close -->
              <button
                class="btn btn-secondary btn-sm me-2"
                @click="closeDrive(drive.id)"
                :disabled="drive.status === 'closed'"
              >
                Close
              </button>


              <!-- Delete -->
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

            <td
              colspan="5"
              class="text-center py-4"
            >
              No placement drives found.
            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../../services/api";


const router = useRouter();

const drives = ref([]);

const loading = ref(true);

const error = ref("");


// Load company drives
async function loadDrives() {

  loading.value = true;

  error.value = "";

  try {

    const response = await api.get(
      "/company/drives"
    );

    console.log(
      "Company Drives:",
      response.data
    );

    drives.value = response.data;

  } catch (err) {

    console.error(
      "Failed to load drives:",
      err
    );

    error.value =
      err.response?.data?.message ||
      "Failed to load drives.";

  } finally {

    loading.value = false;

  }

}


// IMPORTANT
// Send the actual drive ID
function viewApplicants(id) {

  console.log(
    "Opening applicants for drive:",
    id
  );

  router.push(
    `/company/drives/${id}/applicants`
  );

}


// Edit drive
function editDrive(id) {

  router.push(
    `/company/edit-drive/${id}`
  );

}


// Close drive
async function closeDrive(id) {

  try {

    await api.put(
      `/company/drives/${id}/close`
    );

    await loadDrives();

  } catch (err) {

    console.error(err);

    alert(
      err.response?.data?.message ||
      "Failed to close drive."
    );

  }

}


// Delete drive
async function deleteDrive(id) {

  if (
    !confirm(
      "Are you sure you want to delete this drive?"
    )
  ) {
    return;
  }

  try {

    await api.delete(
      `/company/drives/${id}`
    );

    await loadDrives();

  } catch (err) {

    console.error(err);

    alert(
      err.response?.data?.message ||
      "Failed to delete drive."
    );

  }

}


onMounted(() => {

  loadDrives();

});

</script>

