<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="text-center mb-4">
              Placement Portal Login
            </h3>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                type="email"
                v-model="email"
                class="form-control"
                placeholder="Enter your email"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <input
                type="password"
                v-model="password"
                class="form-control"
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              class="btn btn-primary w-100"
              @click="login"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>

    <hr class="my-4" />

    <div class="text-center">
      <p>
        New Student?
        <router-link to="/register/student">
          Register Here
        </router-link>
      </p>

      <p>
        New Company?
        <router-link to="/register/company">
          Register Here
        </router-link>
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")

async function login(){

    try{

        const response = await api.post("/auth/login",{

            email:email.value,

            password:password.value

        })

        localStorage.setItem(
            "token",
            response.data.access_token
        )

        localStorage.setItem(
            "role",
            response.data.role
        )

        localStorage.setItem(
            "name",
            response.data.name
        )

        if(response.data.role==="admin"){

            router.push("/admin/dashboard")

        }

        else if(response.data.role==="company"){

            router.push("/company/dashboard")

        }

        else{

            router.push("/student/dashboard")

        }

    }

    catch(error){

        alert(

            error.response?.data?.message ||

            "Login Failed"

        )

    }

}
</script>