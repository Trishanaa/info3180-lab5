<template>
  <div class="card shadow p-4">
    <h2 class="mb-4 text-center">🎥 Add a New Movie</h2>

    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <div v-if="errors.length" class="alert alert-danger">
      <ul class="mb-0">
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="title" class="form-label">🎬 Movie Title</label>
        <input type="text" name="title" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">📝 Description</label>
        <textarea name="description" class="form-control" rows="4" required></textarea>
      </div>

      <div class="mb-3">
        <label for="poster" class="form-label">🖼️ Poster Image</label>
        <input
          type="file"
          name="poster"
          class="form-control"
          accept="image/*"
          @change="previewImage"
          required
        />
        <div v-if="posterPreview" class="image-preview mt-3">
          <img :src="posterPreview" class="img-fluid rounded" alt="Preview" />
        </div>
      </div>

      <div class="text-end">
        <button type="submit" class="btn btn-primary px-4">
          Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let errors = ref([]);
let successMessage = ref("");
let posterPreview = ref(null);

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

function previewImage(event) {
  const file = event.target.files[0];
  if (file) {
    posterPreview.value = URL.createObjectURL(file);
  } else {
    posterPreview.value = null;
  }
}

function saveMovie() {
  errors.value = [];
  successMessage.value = "";
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.errors) {
        errors.value = data.errors;
      } else {
        successMessage.value = data.message;
        movieForm.reset();
        posterPreview.value = null;
      }
    })
    .catch((error) => {
      console.error("Movie upload error:", error);
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>

<style scoped>
.image-preview img {
  max-height: 250px;
  max-width: 100%;
  object-fit: contain;
  border: 1px solid #ddd;
  padding: 5px;
}
</style>
