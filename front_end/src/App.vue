<script setup>
import axios from 'axios';
import logo from '@/assets/logo.jpeg';
import { ref } from 'vue'

const scrapeUrl = ref('');
const vectorizeUrl = ref('');
const question = ref('');
const result = ref('');

const processScrape = async () => {
  try {
    const response = await axios.post('http://localhost:8000/URL', { input_text: scrapeUrl.value });
    alert(response.data.message);
  } catch (error) {
    console.error(error);
    alert('Scraping failed');
  }
}

const processVectorize = async () => {
  try {
    const response = await axios.post('http://localhost:8000/collection', { input_text: vectorizeUrl.value });
    alert('Vectorization completed');
  } catch (error) {
    console.error(error);
    alert('Vectorization failed');
  }
}

const processQuestion = async () => {
  try {
    const response = await axios.post('http://localhost:8000/ask', { input_text: question.value });
    result.value = response.data;
  } catch (error) {
    console.error(error);
    alert('Question processing failed');
  }
}
</script>

<template>
  <div>
    <div class="text-center pb-3 mt-2">
      <img
        :src="logo"
        style="height: 100px;"
        alt="Gigalogy"
      />
    </div>
    <div class="mt-5 mx-auto" style="width: 500px;">
      <form
        class="row mx-auto my-3"
        @submit.prevent="processScrape"
      >
        <span class="fs-5 fw-bold p-0 pb-1">Provide website URL you like to scrape:</span>
        <input
          type="text"
          v-model="scrapeUrl"
          class="form-control col"
        />
        <button
          type="submit"
          class="btn btn-primary ms-2"
          style="width: 100px;"
        >
          Scrape
        </button>

        <span class="mt-3">Your scraped file is saved to path/to/some/where (output print)</span>
      </form>

      <form
        class="row mx-auto my-4"
        @submit.prevent="processVectorize"
      >
        <input
          type="text"
          v-model="vectorizeUrl"
          class="form-control col"
        />
        <button
          type="submit"
          class="btn btn-primary ms-2"
          style="width: 100px;"
        >
          Vectorize
        </button>
      </form>

      <form
        class="row mx-auto my-4"
        @submit.prevent="processQuestion"
      >
        <span class="fs-5 fw-bold p-0 pb-1 text-center">Ask Questions:</span>
        <input
          type="text"
          v-model="question"
          class="form-control col"
        />
        <button
          type="submit"
          class="btn btn-primary ms-2"
          style="width: 100px;"
        >
          Enter
        </button>
      </form>
    </div>
    <div class="border rounded mx-auto mt-5" style="width: 700px; height: 150px;">
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<style scoped>
/* Add your custom styles here */
</style>
