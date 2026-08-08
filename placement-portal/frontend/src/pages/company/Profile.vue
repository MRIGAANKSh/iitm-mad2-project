<template>

  <div class="container mt-4">

    <h2 class="mb-4">
      Company Profile
    </h2>


    <div class="card shadow-sm">

      <div class="card-body">

        <div class="row">

          <div class="col-md-6">

            <div class="mb-3">

              <label class="form-label">
                Company Name
              </label>

              <input
                v-model="profile.company_name"
                class="form-control"
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                Account Name
              </label>

              <input
                v-model="profile.name"
                class="form-control"
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                Email
              </label>

              <input
                :value="profile.email"
                class="form-control"
                disabled
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                HR Name
              </label>

              <input
                v-model="profile.hr_name"
                class="form-control"
              />

            </div>

          </div>


          <div class="col-md-6">

            <div class="mb-3">

              <label class="form-label">
                HR Email
              </label>

              <input
                v-model="profile.hr_email"
                type="email"
                class="form-control"
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                Phone
              </label>

              <input
                v-model="profile.phone"
                class="form-control"
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                Website
              </label>

              <input
                v-model="profile.website"
                class="form-control"
              />

            </div>


            <div class="mb-3">

              <label class="form-label">
                Description
              </label>

              <textarea
                v-model="profile.description"
                class="form-control"
                rows="4"
              ></textarea>

            </div>

          </div>

        </div>


        <hr>


        <div class="mb-3">

          <strong>
            Approval Status:
          </strong>

          <span
            class="badge ms-2"
            :class="
              profile.approval_status === 'approved'
                ? 'bg-success'
                : 'bg-warning text-dark'
            "
          >

            {{ profile.approval_status }}

          </span>


          <span
            v-if="profile.is_blacklisted"
            class="badge bg-danger ms-2"
          >

            Blacklisted

          </span>

        </div>


        <button
          class="btn btn-primary"
          @click="updateProfile"
        >

          Save Changes

        </button>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";

import api from "../../services/api";


const profile = ref({

  name: "",

  email: "",

  company_name: "",

  hr_name: "",

  hr_email: "",

  phone: "",

  website: "",

  description: "",

  approval_status: "",

  is_blacklisted: false

});


async function loadProfile() {

  try {

    const response = await api.get(
      "/company/profile"
    );

    profile.value = response.data;

  }

  catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to load company profile."
    );

  }

}


async function updateProfile() {

  try {

    await api.put(
      "/company/profile",
      {

        name:
          profile.value.name,

        company_name:
          profile.value.company_name,

        hr_name:
          profile.value.hr_name,

        hr_email:
          profile.value.hr_email,

        phone:
          profile.value.phone,

        website:
          profile.value.website,

        description:
          profile.value.description

      }
    );

    alert(
      "Profile updated successfully."
    );

    await loadProfile();

  }

  catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to update profile."
    );

  }

}


onMounted(() => {

  loadProfile();

});

</script>