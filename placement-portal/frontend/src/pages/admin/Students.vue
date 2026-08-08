<template>

  <div class="container mt-4">

    <div
      class="d-flex justify-content-between align-items-center mb-4"
    >

      <div>

        <h2>Students</h2>

        <p class="text-muted mb-0">
          Manage registered students.
        </p>

      </div>


      <div class="d-flex gap-2">

        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Search students..."
          @keyup.enter="searchStudents"
        />

        <button
          class="btn btn-primary"
          @click="searchStudents"
        >
          Search
        </button>

      </div>

    </div>


    <!-- Students table -->

    <div class="card shadow-sm">

      <div class="card-body">

        <div class="table-responsive">

          <table class="table table-hover align-middle">

            <thead>

              <tr>

                <th>Student ID</th>

                <th>Name</th>

                <th>Email</th>

                <th>Branch</th>

                <th>CGPA</th>

                <th>Graduation</th>

                <th>Status</th>

                <th>Action</th>

              </tr>

            </thead>


            <tbody>

              <tr
                v-for="student in students"
                :key="student.id"
              >

                <td>
                  {{ student.student_id || "-" }}
                </td>

                <td>
                  {{ student.name }}
                </td>

                <td>
                  {{ student.email }}
                </td>

                <td>
                  {{ student.branch || "-" }}
                </td>

                <td>
                  {{ student.cgpa ?? "-" }}
                </td>

                <td>
                  {{ student.graduation_year || "-" }}
                </td>


                <td>

                  <span
                    v-if="student.is_active"
                    class="badge bg-success"
                  >
                    Active
                  </span>

                  <span
                    v-else
                    class="badge bg-danger"
                  >
                    Inactive
                  </span>

                </td>


                <td>

                  <button
                    v-if="student.is_active"
                    class="btn btn-sm btn-warning"
                    @click="deactivateStudent(student.id)"
                  >

                    Deactivate

                  </button>


                  <button
                    v-else
                    class="btn btn-sm btn-success"
                    @click="activateStudent(student.id)"
                  >

                    Activate

                  </button>

                </td>

              </tr>


              <tr v-if="students.length === 0">

                <td
                  colspan="8"
                  class="text-center text-muted py-4"
                >

                  No students found.

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";

import api from "../../services/api";


const students = ref([]);

const search = ref("");


async function searchStudents() {

  try {

    const response = await api.get(
      "/admin/students/search",
      {
        params: {
          q: search.value
        }
      }
    );

    students.value = response.data;

  }

  catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to load students."
    );

  }

}


async function deactivateStudent(id) {

  if (
    !confirm(
      "Are you sure you want to deactivate this student?"
    )
  ) {

    return;

  }


  try {

    await api.put(
      `/admin/students/${id}/deactivate`
    );

    await searchStudents();

  }

  catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to deactivate student."
    );

  }

}


async function activateStudent(id) {

  try {

    await api.put(
      `/admin/students/${id}/activate`
    );

    await searchStudents();

  }

  catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to activate student."
    );

  }

}


onMounted(() => {

  searchStudents();

});

</script>