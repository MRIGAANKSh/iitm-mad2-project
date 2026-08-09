
<template>

  <!-- =========================
       HEADER
  ========================== -->

  <div class="d-flex justify-content-between align-items-center mb-4">

    <div>

      <h2>
        Student Dashboard
      </h2>

      <p class="text-muted mb-0">
        Welcome to your placement dashboard.
      </p>

    </div>


    <!-- Refresh -->

    <button
      class="btn btn-outline-primary"
      @click="loadNotifications"
      :disabled="loadingNotifications"
    >

      <span
        v-if="loadingNotifications"
        class="spinner-border spinner-border-sm me-2"
        role="status"
      ></span>

      <span v-else>
        🔄
      </span>

      {{
        loadingNotifications
          ? "Refreshing..."
          : "Refresh"
      }}


      <!-- Unread count -->

      <span
        v-if="unreadCount > 0"
        class="badge bg-danger ms-2"
      >

        {{ unreadCount }}

      </span>

    </button>

  </div>



  <!-- =====================================================
       NOTIFICATIONS
  ====================================================== -->

  <div class="card shadow-sm mb-4">

    <!-- Header -->

    <div
      class="card-header d-flex justify-content-between align-items-center"
    >

      <h5 class="mb-0">

        🔔 Notifications


        <!-- Unread count -->

        <span
          v-if="unreadCount > 0"
          class="badge bg-danger ms-2"
        >

          {{ unreadCount }}

        </span>

      </h5>


      <!-- All read -->

      <span
        v-if="
          notifications.length > 0 &&
          unreadCount === 0
        "
        class="badge bg-success"
      >

        All Read

      </span>

    </div>



    <!-- Notification Body -->

    <div class="card-body">


      <!-- Loading -->

      <div
        v-if="loadingNotifications"
        class="text-center py-3"
      >

        <div
          class="spinner-border text-primary"
          role="status"
        ></div>

        <p class="mt-2 mb-0 text-muted">
          Loading notifications...
        </p>

      </div>



      <!-- No notifications -->

      <div
        v-else-if="notifications.length === 0"
        class="text-muted text-center py-3"
      >

        🔔 No notifications.

      </div>



      <!-- Notifications -->

      <div v-else>

        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="alert mb-2"
          :class="
            notification.is_read
              ? 'alert-light'
              : 'alert-warning'
          "
        >

          <div
            class="d-flex justify-content-between align-items-center"
          >


            <!-- Notification Content -->

            <div>

              <!-- New badge -->

              <strong
                v-if="!notification.is_read"
                class="text-warning-emphasis me-2"
              >

                New

              </strong>


              <!-- Message -->

              <span>

                {{ notification.message }}

              </span>


              <!-- Date -->

              <br>

              <small class="text-muted">

                {{ formatDate(notification.created_at) }}

              </small>

            </div>



            <!-- Mark as read -->

            <button
              v-if="!notification.is_read"
              class="btn btn-sm btn-outline-success ms-3"
              @click="
                markAsRead(notification.id)
              "
              :disabled="
                markingReadId === notification.id
              "
            >

              <span
                v-if="
                  markingReadId ===
                  notification.id
                "
                class="spinner-border spinner-border-sm me-1"
              ></span>

              {{
                markingReadId === notification.id
                  ? "Updating..."
                  : "Mark as read"
              }}

            </button>


            <!-- Already read -->

            <span
              v-else
              class="badge bg-light text-muted ms-3"
            >

              ✓ Read

            </span>

          </div>

        </div>

      </div>

    </div>

  </div>



  <!-- =====================================================
       DASHBOARD CARDS
  ====================================================== -->

  <div class="row">


    <!-- =========================
         PLACEMENT DRIVES
    ========================== -->

    <div class="col-md-4 mb-3">

      <div class="card shadow-sm h-100">

        <div class="card-body">

          <h5>
            Placement Drives
          </h5>

          <p class="text-muted">

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



    <!-- =========================
         APPLICATIONS
    ========================== -->

    <div class="col-md-4 mb-3">

      <div class="card shadow-sm h-100">

        <div class="card-body">

          <h5>
            Applications
          </h5>

          <p class="text-muted">

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



    <!-- =========================
         PROFILE
    ========================== -->

    <div class="col-md-4 mb-3">

      <div class="card shadow-sm h-100">

        <div class="card-body">

          <h5>
            Profile
          </h5>

          <p class="text-muted">

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

</template>



<script setup>

import {
  ref,
  onMounted
} from "vue"

import api from "../../services/api"


// =========================================================
// STATE
// =========================================================

const notifications = ref([])

const unreadCount = ref(0)

const loadingNotifications = ref(false)

const markingReadId = ref(null)



// =========================================================
// LOAD NOTIFICATIONS
// =========================================================

async function loadNotifications() {

  loadingNotifications.value = true

  try {

    const response = await api.get(
      "/student/notifications"
    )


    // Make sure response is an array

    notifications.value =
      Array.isArray(response.data)
        ? response.data
        : []


    // =====================================================
    // CALCULATE UNREAD COUNT
    // =====================================================

    unreadCount.value =
      notifications.value.filter(
        notification =>
          !notification.is_read
      ).length


    console.log(
      "Notifications:",
      notifications.value
    )


    console.log(
      "Unread count:",
      unreadCount.value
    )

  }

  catch (error) {

    console.error(
      "Failed to load notifications:",
      error
    )


    notifications.value = []

    unreadCount.value = 0

  }

  finally {

    loadingNotifications.value = false

  }

}



// =========================================================
// MARK NOTIFICATION AS READ
// =========================================================

async function markAsRead(id) {

  markingReadId.value = id

  try {

    await api.put(
      `/student/notifications/${id}/read`
    )


    // Reload notifications.

    // This automatically recalculates
    // unreadCount.

    await loadNotifications()

  }

  catch (error) {

    console.error(
      "Failed to mark notification:",
      error
    )


    alert(
      error?.response?.data?.message ||
      "Failed to mark notification as read."
    )

  }

  finally {

    markingReadId.value = null

  }

}



// =========================================================
// FORMAT DATE
// =========================================================

function formatDate(date) {

  if (!date) {

    return ""

  }


  const parsedDate =
    new Date(date)


  if (
    Number.isNaN(
      parsedDate.getTime()
    )
  ) {

    return date

  }


  return parsedDate.toLocaleString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }
  )

}



// =========================================================
// LOAD PAGE
// =========================================================

onMounted(() => {

  loadNotifications()

})

</script>

