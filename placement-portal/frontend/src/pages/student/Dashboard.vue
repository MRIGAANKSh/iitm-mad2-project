<template>

  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <div>

        <h2>Student Dashboard</h2>

        <p class="text-muted">
          Welcome to your placement dashboard.
        </p>

      </div>

      <button
        class="btn btn-outline-primary"
        @click="loadNotifications"
      >
        🔄 Refresh
      </button>

    </div>


    <!-- Notifications -->

    <div class="card shadow-sm mb-4">

      <div class="card-header">

        <h5 class="mb-0">
          🔔 Notifications
        </h5>

      </div>


      <div class="card-body">

        <div
          v-if="notifications.length === 0"
          class="text-muted"
        >

          No notifications.

        </div>


        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="alert"
          :class="
            notification.is_read
              ? 'alert-light'
              : 'alert-warning'
          "
        >

          <div
            class="d-flex justify-content-between align-items-center"
          >

            <div>

              <strong
                v-if="!notification.is_read"
              >
                New
              </strong>

              {{ notification.message }}

              <br>

              <small class="text-muted">

                {{ formatDate(notification.created_at) }}

              </small>

            </div>


            <button
              v-if="!notification.is_read"
              class="btn btn-sm btn-outline-success"
              @click="markAsRead(notification.id)"
            >

              Mark as read

            </button>

          </div>

        </div>

      </div>

    </div>


    <!-- Dashboard cards -->

    <div class="row">

      <div class="col-md-4 mb-3">

        <div class="card shadow-sm">

          <div class="card-body">

            <h5>Placement Drives</h5>

            <p>
              View approved placement opportunities.
            </p>

            <router-link
              to="/student/drives"
              class="btn btn-primary"
            >

              View Drives

            </router-link>

          </div>

        </div>

      </div>


      <div class="col-md-4 mb-3">

        <div class="card shadow-sm">

          <div class="card-body">

            <h5>Applications</h5>

            <p>
              Track your placement applications.
            </p>

            <router-link
              to="/student/applications"
              class="btn btn-primary"
            >

              My Applications

            </router-link>

          </div>

        </div>

      </div>


      <div class="col-md-4 mb-3">

        <div class="card shadow-sm">

          <div class="card-body">

            <h5>Profile</h5>

            <p>
              Update your student information.
            </p>

            <router-link
              to="/student/profile"
              class="btn btn-primary"
            >

              My Profile

            </router-link>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";

import api from "../../services/api";


const notifications = ref([]);


async function loadNotifications() {

  try {

    const response = await api.get(
      "/student/notifications"
    );

    notifications.value = response.data;

  }

  catch (error) {

    console.error(
      "Failed to load notifications:",
      error
    );

  }

}


async function markAsRead(id) {

  try {

    await api.put(
      `/student/notifications/${id}/read`
    );

    await loadNotifications();

  }

  catch (error) {

    console.error(
      "Failed to mark notification:",
      error
    );

  }

}


function formatDate(date) {

  if (!date) {
    return "";
  }

  return new Date(date).toLocaleString();

}


onMounted(() => {

  loadNotifications();

});

</script>