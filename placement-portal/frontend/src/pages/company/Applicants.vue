<template>
  <div class="container mt-4">

    <h3 class="mb-4">Applicants</h3>

    <table class="table table-bordered table-hover">

      <thead class="table-dark">
        <tr>
          <th>Student</th>
          <th>Email</th>
          <th>Branch</th>
          <th>CGPA</th>
          <th>Status</th>
          <th width="260">Actions</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="student in applicants"
          :key="student.application_id"
        >
          <td>{{ student.student_name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.branch }}</td>
          <td>{{ student.cgpa }}</td>

          <td>
            <span class="badge bg-primary">
              {{ student.status }}
            </span>
          </td>

          <td>

            <button
              class="btn btn-warning btn-sm me-2"
              @click="updateStatus(student.application_id, 'Shortlisted')"
            >
              Shortlist
            </button>

            <button
              class="btn btn-danger btn-sm me-2"
              @click="updateStatus(student.application_id, 'Rejected')"
            >
              Reject
            </button>

            <button
              class="btn btn-success btn-sm"
              @click="updateStatus(student.application_id, 'Selected')"
            >
              Select
            </button>

          </td>

        </tr>

        <tr v-if="applicants.length === 0">
          <td colspan="6" class="text-center">
            No Applicants Found
          </td>
        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../../services/api";

const applicants = ref([]);

const route = useRoute();
const driveId = route.params.id;

async function loadApplicants() {
  if (!driveId) {
    alert("Invalid Drive ID");
    return;
  }

  try {
    const { data } = await api.get(
      `/company/drives/${driveId}/applications`
    );

    applicants.value = data;
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.message || "Failed to load applicants.");
  }
}

async function updateStatus(applicationId, status) {
  try {
    const { data } = await api.put(
      `/company/applications/${applicationId}/status`,
      {
        status,
      }
    );

    alert(data.message);

    await loadApplicants();
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.message || "Failed to update status.");
  }
}

onMounted(() => {
  console.log("Drive ID:", driveId);
  loadApplicants();
});
</script>