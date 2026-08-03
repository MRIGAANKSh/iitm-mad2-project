<template>
  <div class="container mt-5">

    <div class="row justify-content-center">

      <div class="col-md-8">

        <div class="card shadow">

          <div class="card-header bg-success text-white">
            <h3>Company Registration</h3>
          </div>

          <div class="card-body">

            <form @submit.prevent="registerCompany">

              <div class="mb-3">
                <label>Company Name</label>
                <input
                  class="form-control"
                  v-model="form.company_name"
                  required
                >
              </div>

              <div class="mb-3">
                <label>Email</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="form.email"
                  required
                >
              </div>

              <div class="mb-3">
                <label>Password</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="form.password"
                  required
                >
              </div>

              <div class="mb-3">
                <label>HR Name</label>
                <input
                  class="form-control"
                  v-model="form.hr_name"
                >
              </div>

              <div class="mb-3">
                <label>HR Email</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="form.hr_email"
                >
              </div>

              <div class="mb-3">
                <label>Phone</label>
                <input
                  class="form-control"
                  v-model="form.phone"
                >
              </div>

              <div class="mb-3">
                <label>Website</label>
                <input
                  class="form-control"
                  v-model="form.website"
                >
              </div>

              <div class="mb-3">
                <label>Description</label>
                <textarea
                  rows="4"
                  class="form-control"
                  v-model="form.description"
                ></textarea>
              </div>

              <button
                class="btn btn-success w-100"
              >
                Register Company
              </button>

            </form>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

import { reactive } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const form = reactive({

    company_name:"",
    email:"",
    password:"",
    hr_name:"",
    hr_email:"",
    phone:"",
    website:"",
    description:""

})

async function registerCompany(){

    try{

        await api.post(
            "/auth/register/company",
            form
        )

        alert(
            "Registration Submitted.\nWaiting for Admin Approval."
        )

        router.push("/")

    }

    catch(error){

        alert(
            error.response?.data?.message ||
            "Registration Failed"
        )

    }

}

</script>