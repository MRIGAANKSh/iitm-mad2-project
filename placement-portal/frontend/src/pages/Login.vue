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
              <label>Email</label>
              <input
                v-model="email"
                class="form-control"
              />
            </div>

            <div class="mb-3">
              <label>Password</label>
              <input
                type="password"
                v-model="password"
                class="form-control"
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
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const email = ref("");
const password = ref("");

async function login() {
  try {
    const response = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    localStorage.setItem("token", response.data.access_token);
    localStorage.setItem("role", response.data.role);

    if (response.data.role === "admin") {
      router.push("/admin/dashboard");
    } else if (response.data.role === "company") {
      router.push("/company/dashboard");
    } else {
      router.push("/student/dashboard");
    }
  } catch (error) {
    alert(
      error.response?.data?.message || "Login failed"
    );
  }
}
</script>