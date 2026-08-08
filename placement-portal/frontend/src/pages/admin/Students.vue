
<template>

  <div class="container-fluid">

    <!-- Page Header -->
    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >

      <div>

        <h2 class="mb-1">
          Students
        </h2>

        <p class="text-muted mb-0">
          View and manage all registered students
        </p>

      </div>


      <!-- Refresh -->
      <button
        class="btn btn-outline-primary"
        @click="loadStudents"
        :disabled="loading"
      >

        <span v-if="loading">
          Loading...
        </span>

        <span v-else>
          Refresh
        </span>

      </button>

    </div>


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
        Loading students...
      </p>

    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >

      {{ error }}

      <button
        class="btn btn-sm btn-danger ms-3"
        @click="loadStudents"
      >
        Try Again
      </button>

    </div>


    <!-- Students -->
    <div v-else>

      <!-- Search -->
      <div class="card shadow-sm mb-4">

        <div class="card-body">

          <div class="row">

            <div class="col-md-6">

              <label class="form-label">
                Search Students
              </label>

              <input
                type="text"
                class="form-control"
                v-model="search"
                placeholder="Search by name or email..."
              />

            </div>

          </div>

        </div>

      </div>


      <!-- No Students -->
      <div
        v-if="filteredStudents.length === 0"
        class="alert alert-info"
      >

        No students found.

      </div>


      <!-- Students Table -->
      <div
        v-else
        class="card shadow-sm"
      >

        <div class="card-body p-0">

          <div class="table-responsive">

            <table
              class="table table-bordered table-hover mb-0"
            >

              <thead class="table-dark">

                <tr>

                  <th>
                    #
                  </th>

                  <th>
                    Student
                  </th>

                  <th>
                    Email
                  </th>

                  <th>
                    Branch
                  </th>

                  <th>
                    CGPA
                  </th>

                  <th>
                    Placement Status
                  </th>

                  <th>
                    Actions
                  </th>

                </tr>

              </thead>


              <tbody>

                <tr
                  v-for="(student, index) in filteredStudents"
                  :key="student.id"
                >

                  <!-- ID -->
                  <td>
                    {{ index + 1 }}
                  </td>


                  <!-- Name -->
                  <td>

                    <strong>
                      {{ student.name }}
                    </strong>

                  </td>


                  <!-- Email -->
                  <td>
                    {{ student.email }}
                  </td>


                  <!-- Branch -->
                  <td>
                    {{ student.branch || "N/A" }}
                  </td>


                  <!-- CGPA -->
                  <td>
                    {{ student.cgpa ?? "N/A" }}
                  </td>


                  <!-- Placement -->
                  <td>

                    <span
                      v-if="student.placed"
                      class="badge bg-success"
                    >
                      Placed
                    </span>

                    <span
                      v-else
                      class="badge bg-secondary"
                    >
                      Not Placed
                    </span>

                  </td>


                  <!-- Actions -->
                  <td>

                    <button
                      class="btn btn-danger btn-sm"
                      @click="deactivateStudent(student)"
                      :disabled="deactivatingId === student.id"
                    >

                      <span
                        v-if="deactivatingId === student.id"
                      >
                        Deactivating...
                      </span>

                      <span v-else>
                        Deactivate
                      </span>

                    </button>

                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import {
  ref,
  computed,
  onMounted
} from "vue"

import api from "../../services/api"


// ==========================================
// STATE
// ==========================================

const students = ref([])

const loading = ref(true)

const error = ref("")

const search = ref("")

const deactivatingId = ref(null)


// ==========================================
// LOAD STUDENTS
// ==========================================

async function loadStudents() {

  loading.value = true

  error.value = ""

  try {

    const response = await api.get(
      "/admin/students"
    )

    console.log(
      "Admin Students:",
      response.data
    )

    if (Array.isArray(response.data)) {

      students.value = response.data

    } else {

      students.value = []

      error.value =
        "Invalid students response from server."

    }

  } catch (err) {

    console.error(
      "Failed to load students:",
      err
    )

    error.value =
      err.response?.data?.message ||
      `Failed to load students (${err.response?.status || "Network Error"})`

  } finally {

    loading.value = false

  }

}


// ==========================================
// SEARCH
// ==========================================

const filteredStudents = computed(() => {

  const keyword =
    search.value
      .trim()
      .toLowerCase()

  if (!keyword) {

    return students.value

  }

  return students.value.filter(student => {

    return (

      (student.name || "")
        .toLowerCase()
        .includes(keyword)

      ||

      (student.email || "")
        .toLowerCase()
        .includes(keyword)

      ||

      (student.branch || "")
        .toLowerCase()
        .includes(keyword)

    )

  })

})


// ==========================================
// DEACTIVATE STUDENT
// ==========================================

async function deactivateStudent(student) {

  const confirmed = window.confirm(
    `Are you sure you want to deactivate ${student.name}?`
  )

  if (!confirmed) {

    return

  }


  deactivatingId.value = student.id

  error.value = ""


  try {

    const response = await api.put(
      `/admin/students/${student.id}/deactivate`
    )


    console.log(
      "Student deactivated:",
      response.data
    )


    // Remove student from current list
    students.value =
      students.value.filter(
        item => item.id !== student.id
      )


  } catch (err) {

    console.error(
      "Failed to deactivate student:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to deactivate student."

  } finally {

    deactivatingId.value = null

  }

}


// ==========================================
// INITIAL LOAD
// ==========================================

onMounted(() => {

  loadStudents()

})

</script>
