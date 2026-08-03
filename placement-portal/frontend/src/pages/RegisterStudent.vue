<template>
  <div class="container mt-5">

    <div class="row justify-content-center">

      <div class="col-md-7">

        <div class="card shadow">

          <div class="card-header bg-primary text-white">
            <h3>Student Registration</h3>
          </div>

          <div class="card-body">

            <form @submit.prevent="registerStudent">

              <div class="mb-3">
                <label>Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.name"
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
                <label>Student ID</label>
                <input
                  class="form-control"
                  v-model="form.student_id"
                  required
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
                <label>Branch</label>
                <input
                  class="form-control"
                  v-model="form.branch"
                >
              </div>

              <div class="mb-3">
                <label>CGPA</label>
                <input
                  type="number"
                  step="0.01"
                  class="form-control"
                  v-model="form.cgpa"
                >
              </div>

              <div class="mb-3">
                <label>Graduation Year</label>
                <input
                  type="number"
                  class="form-control"
                  v-model="form.graduation_year"
                >
              </div>

              <button
                class="btn btn-primary w-100"
              >
                Register
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

    name:"",
    email:"",
    password:"",
    student_id:"",
    phone:"",
    branch:"",
    cgpa:"",
    graduation_year:""

})

async function registerStudent(){

    try{

        await api.post(
            "/auth/register/student",
            form
        )

        alert("Student Registered Successfully!")

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