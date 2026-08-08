
<template>

  <div>

    <h4 class="mb-3">
      Upload Resume
    </h4>

    <!-- Select Resume -->
    <input
      type="file"
      class="form-control"
      accept=".pdf,.doc,.docx"
      @change="selectFile"
    />

    <!-- Upload Button -->
    <button
      class="btn btn-primary mt-3"
      :disabled="!selectedFile || uploading"
      @click="upload"
    >
      {{ uploading ? "Uploading..." : "Upload Resume" }}
    </button>


    <!-- Current Resume -->
    <div
      v-if="resume"
      class="mt-4"
    >

      <p class="mb-2 fw-semibold">
        Current Resume:
      </p>

      <div
        class="d-flex align-items-center gap-3"
      >

        <span class="text-muted">
          {{ resume }}
        </span>

        <button
          class="btn btn-outline-primary btn-sm"
          @click="openResume"
        >
          Open Resume
        </button>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"

import api from "../../services/api"


const selectedFile = ref(null)

const resume = ref("")

const uploading = ref(false)


// ----------------------------------------
// Select file
// ----------------------------------------

function selectFile(event) {

  selectedFile.value =
    event.target.files[0] || null

}


// ----------------------------------------
// Get current resume
// ----------------------------------------

async function loadResume() {

  try {

    const response = await api.get(
      "/student/resume"
    )

    resume.value =
      response.data.resume || ""

  } catch (error) {

    console.error(
      "Failed to load resume:",
      error
    )

  }

}


// ----------------------------------------
// Upload resume
// ----------------------------------------

async function upload() {

  if (!selectedFile.value) {

    alert("Please select a resume first.")

    return

  }

  uploading.value = true

  try {

    const formData = new FormData()

    formData.append(
      "resume",
      selectedFile.value
    )


    const response = await api.post(
      "/student/upload-resume",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data"
        }
      }
    )


    alert(
      response.data.message ||
      "Resume uploaded successfully."
    )


    // Update displayed resume
    resume.value =
      response.data.filename || ""


    // Clear selected file
    selectedFile.value = null

  } catch (error) {

    console.error(
      "Resume upload failed:",
      error
    )

    alert(
      error.response?.data?.message ||
      "Failed to upload resume."
    )

  } finally {

    uploading.value = false

  }

}


// ----------------------------------------
// Open resume in new tab
// ----------------------------------------

function openResume() {

  if (!resume.value) {

    alert("No resume available.")

    return

  }


  const resumeUrl =
    `http://localhost:5000/uploads/${encodeURIComponent(resume.value)}`


  window.open(
    resumeUrl,
    "_blank"
  )

}


// ----------------------------------------
// Load on page open
// ----------------------------------------

onMounted(() => {

  loadResume()

})

</script>

