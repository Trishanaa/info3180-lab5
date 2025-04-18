<template>
  <div class="container mt-5">
    <h1>Movies</h1>
    <div class="row">
      <div class="col-md-6 mb-4" v-for="movie in movies" :key="movie.id">
        <div class="card h-100">
          <div class="row g-0 h-100">
            <!-- Image Column -->
            <div class="col-md-5">
              <img :src="movie.poster" 
                   class="img-fluid h-100 object-fit-cover"
                   :alt="movie.title + ' Poster'">
            </div>
            
            <!-- Content Column -->
            <div class="col-md-7">
              <div class="card-body d-flex flex-column h-100">
                <h3 class="card-title mb-3">{{ movie.title }}</h3>
                <p class="card-text flex-grow-1">{{ movie.description }}</p>
                <small class="text-muted">{{ movie.copyright }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

let movies = ref([
  {
    id: 1,
    title: "The Eye",
    description: "In a distant galaxy, far beyond the reach of human civilization, an ancient civilization's secrets are uncovered. This film follows a group of astronauts as they embark on a perilous mission to explore a forgotten planet. Along their journey, they face challenges that test their limits.",
    poster: "https://example.com/the-eye-poster.jpg",
    copyright: "Copyright © 2025 Flask Inc."
  },
  {
    id: 2,
    title: "Anime",
    description: "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
    poster: "https://example.com/anime-poster.jpg",
    copyright: "Copyright © 2025 Flask Inc."
  }
]);

const fetchMovies = async () => {
  try {
    const response = await fetch('/api/v1/movies');
    const data = await response.json();
    movies.value = data.movies;
  } catch (error) {
    console.error('Error fetching movies:', error);
  }
};

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.object-fit-cover {
  object-fit: cover;
  object-position: center;
}

.img-fluid {
  border-radius: 0.375rem 0 0 0.375rem;
}

.card-title {
  font-weight: 600;
  color: #2c3e50;
}

.card-text {
  color: #666;
  line-height: 1.6;
}
</style>