<template>
  <div class="container">

    <h2 class="mb-4">Create Placement Drive</h2>

    <form @submit.prevent="createDrive">

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
          <label class="form-label">Branch</label>
          <input
            class="form-control"
            v-model="form.branch"
          />
        </div>

        <div class="col-md-4">
          <label class="form-label">Minimum CGPA</label>
          <input
            type="number"
            step="0.01"
            class="form-control"
            v-model="form.cgpa"
          />
        </div>

        <div class="col-md-4">
          <label class="form-label">Passing Year</label>
          <input
            type="number"
            class="form-control"
            v-model="form.year"
          />
        </div>

      </div>

      <div class="row mt-3">

        <div class="col-md-6">
          <label class="form-label">Application Deadline</label>
          <input
            type="date"
            class="form-control"
            v-model="form.deadline"
          />
        </div>

        <div class="col-md-6">
          <label class="form-label">Salary Package (LPA)</label>
          <input
            type="number"
            class="form-control"
            v-model="form.salary"
          />
        </div>

      </div>

      <button class="btn btn-primary mt-4">
        Create Drive
      </button>

    </form>

  </div>
</template>

<script setup>
import { reactive } from "vue"
import api from "../../services/api"

const form = reactive({
  job_title: "",
  job_description: "",
  branch: "",
  cgpa: "",
  year: "",
  deadline: "",
  salary: ""
})

async function createDrive() {
  try {
    await api.post("/company/drives", form)

    alert("Placement Drive Created Successfully!")

    form.job_title = ""
    form.job_description = ""
    form.branch = ""
    form.cgpa = ""
    form.year = ""
    form.deadline = ""
    form.salary = ""

  } catch (err) {
    alert(err.response?.data?.message || "Error creating drive")
  }
}
</script>