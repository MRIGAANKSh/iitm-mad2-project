<template>
  <div class="container mt-4">

    <h2 class="mb-4">Edit Placement Drive</h2>

    <form @submit.prevent="updateDrive">

      <div class="mb-3">
        <label class="form-label">Job Title</label>
        <input
          type="text"
          class="form-control"
          v-model="form.job_title"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Job Description</label>
        <textarea
          class="form-control"
          rows="4"
          v-model="form.job_description"
          required
        ></textarea>
      </div>

      <div class="row">

        <div class="col-md-4">
          <label class="form-label">Eligible Branch</label>
          <input
            class="form-control"
            v-model="form.eligibility_branch"
          />
        </div>

        <div class="col-md-4">
          <label class="form-label">Minimum CGPA</label>
          <input
            type="number"
            class="form-control"
            v-model="form.minimum_cgpa"
          />
        </div>

        <div class="col-md-4">
          <label class="form-label">Graduation Year</label>
          <input
            type="number"
            class="form-control"
            v-model="form.graduation_year"
          />
        </div>

      </div>

      <div class="row mt-3">

        <div class="col-md-6">
          <label class="form-label">Deadline</label>
          <input
            type="date"
            class="form-control"
            v-model="form.application_deadline"
          />
        </div>

        <div class="col-md-6">
          <label class="form-label">Salary</label>
          <input
            type="number"
            class="form-control"
            v-model="form.salary"
          />
        </div>

      </div>

      <div class="row mt-3">

        <div class="col-md-4">
          <label class="form-label">Location</label>
          <input
            class="form-control"
            v-model="form.location"
          />
        </div>

        <div class="col-md-4">
          <label class="form-label">Employment Type</label>

          <select
            class="form-select"
            v-model="form.employment_type"
          >
            <option value="">Select</option>
            <option>Full Time</option>
            <option>Internship</option>
            <option>Internship + PPO</option>
          </select>

        </div>

        <div class="col-md-4">
          <label class="form-label">Vacancies</label>
          <input
            type="number"
            class="form-control"
            v-model="form.vacancies"
          />
        </div>

      </div>

      <button class="btn btn-success mt-4">
        Update Drive
      </button>

    </form>

  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../../services/api";

const route = useRoute();
const router = useRouter();

const form = reactive({
  job_title: "",
  job_description: "",
  eligibility_branch: "",
  minimum_cgpa: "",
  graduation_year: "",
  application_deadline: "",
  salary: "",
  location: "",
  employment_type: "",
  vacancies: ""
});

async function loadDrive() {

  const res = await api.get(
    `/company/drives/${route.params.id}`
  );

  Object.assign(form, res.data);

}

async function updateDrive() {

  await api.put(
    `/company/drives/${route.params.id}`,
    form
  );

  alert("Drive Updated Successfully");

  router.push("/company/drives");

}

onMounted(loadDrive);
</script>