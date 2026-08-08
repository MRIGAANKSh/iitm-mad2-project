<template>

<div class="container">

<h2 class="mb-4">

Upload Resume

</h2>

<div class="card">

<div class="card-body">

<input

type="file"

class="form-control"

@change="selectFile"

/>

<button

class="btn btn-primary mt-3"

@click="upload"

>

Upload Resume

</button>

<div
v-if="resume"
class="alert alert-success mt-3"
>

Current Resume:

<b>

{{ resume }}

</b>

</div>

</div>

</div>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue"

import api from "../../services/api"

const file = ref(null)

const resume = ref("")

function selectFile(event){

    file.value = event.target.files[0]

}

async function upload(){

    const form = new FormData()

    form.append(
        "resume",
        file.value
    )

    const response = await api.post(

        "/student/upload-resume",

        form,

        {

            headers:{

                "Content-Type":

                "multipart/form-data"

            }

        }

    )

    alert(response.data.message)

    loadResume()

}

async function loadResume(){

    const response = await api.get(
        "/student/resume"
    )

    resume.value = response.data.resume

}

onMounted(loadResume)

</script>