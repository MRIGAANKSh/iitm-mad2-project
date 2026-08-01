<template>
  <div class="container mt-4">

    <h3>Applicants</h3>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Student</th>
          <th>Branch</th>
          <th>CGPA</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="student in applicants"
          :key="student.id"
        >
          <td>{{ student.name }}</td>
          <td>{{ student.branch }}</td>
          <td>{{ student.cgpa }}</td>
          <td>{{ student.status }}</td>

          <td>
            <button
              class="btn btn-success btn-sm me-2"
              @click="updateStatus(student.id,'shortlisted')"
            >
              Shortlist
            </button>

            <button
              class="btn btn-danger btn-sm me-2"
              @click="updateStatus(student.id,'rejected')"
            >
              Reject
            </button>

            <button
              class="btn btn-primary btn-sm"
              @click="updateStatus(student.id,'selected')"
            >
              Select
            </button>
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
  const response = await api.get(`/company/drives/${driveId}/applications`);
  applicants.value = response.data;
}

async function updateStatus(id, status) {
  await api.put(`/company/applications/${id}`, {
    status,
  });

  loadApplicants();
}

onMounted(loadApplicants);
</script>