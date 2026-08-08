
<template>

  <div class="container">

    <!-- Page Title -->
    <h2 class="mb-4">
      My Profile
    </h2>


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
        Loading profile...
      </p>

    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>


    <!-- Profile -->
    <div v-else>

      <div class="card shadow-sm">

        <div class="card-header bg-primary text-white">

          <h5 class="mb-0">
            Student Profile
          </h5>

        </div>


        <div class="card-body">

          <!-- Name -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              Name
            </label>

            <input
              type="text"
              class="form-control"
              :value="profile.name"
              disabled
            />

          </div>


          <!-- Email -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              Email
            </label>

            <input
              type="email"
              class="form-control"
              :value="profile.email"
              disabled
            />

          </div>


          <!-- Phone -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              Phone
            </label>

            <input
              type="text"
              class="form-control"
              v-model="profile.phone"
            />

          </div>


          <!-- Branch -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              Branch
            </label>

            <input
              type="text"
              class="form-control"
              v-model="profile.branch"
            />

          </div>


          <!-- CGPA -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              CGPA
            </label>

            <input
              type="number"
              step="0.01"
              class="form-control"
              v-model="profile.cgpa"
            />

          </div>


          <!-- Resume -->
          <div class="mb-3">

            <label class="form-label fw-bold">
              Resume
            </label>

            <div v-if="profile.resume">

              <span class="text-success">
                Resume uploaded
              </span>

              <br />

              <RouterLink
                to="/student/resume"
                class="btn btn-outline-primary btn-sm mt-2"
              >
                Manage Resume
              </RouterLink>

            </div>


            <div v-else>

              <span class="text-muted">
                No resume uploaded
              </span>

              <br />

              <RouterLink
                to="/student/resume"
                class="btn btn-primary btn-sm mt-2"
              >
                Upload Resume
              </RouterLink>

            </div>

          </div>


          <!-- Save -->
          <button
            class="btn btn-primary"
            @click="updateProfile"
            :disabled="saving"
          >

            <span v-if="saving">
              Saving...
            </span>

            <span v-else>
              Save Changes
            </span>

          </button>


          <!-- Success -->
          <div
            v-if="success"
            class="alert alert-success mt-3 mb-0"
          >
            {{ success }}
          </div>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"


// Profile data
const profile = ref({

  name: "",

  email: "",

  phone: "",

  branch: "",

  cgpa: "",

  resume: null

})


// States
const loading = ref(true)

const saving = ref(false)

const error = ref("")

const success = ref("")


// Load profile
async function loadProfile() {

  loading.value = true

  error.value = ""

  try {

    const response = await api.get(
      "/student/profile"
    )

    console.log(
      "Student Profile:",
      response.data
    )

    profile.value = {

      name: response.data.name || "",

      email: response.data.email || "",

      phone: response.data.phone || "",

      branch: response.data.branch || "",

      cgpa: response.data.cgpa ?? "",

      resume: response.data.resume || null

    }

  } catch (err) {

    console.error(
      "Profile loading error:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to load profile."

  } finally {

    loading.value = false

  }

}


// Update profile
async function updateProfile() {

  saving.value = true

  error.value = ""

  success.value = ""

  try {

    const response = await api.put(
      "/student/profile",
      {

        phone: profile.value.phone,

        branch: profile.value.branch,

        cgpa: profile.value.cgpa

      }
    )

    console.log(
      "Profile update:",
      response.data
    )

    success.value =
      response.data.message ||
      "Profile updated successfully."

  } catch (err) {

    console.error(
      "Profile update error:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to update profile."

  } finally {

    saving.value = false

  }

}


onMounted(() => {

  loadProfile()

})

</script>
