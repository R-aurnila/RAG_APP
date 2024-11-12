# RAG-APP: Retrieval-Augmented Generation Application

This project is a **Retrieval-Augmented Generation (RAG)** application designed to answer queries about the website [Gigalogy](https://gigalogy.com/). The application scrapes real-time data from the website using **Playwright** and integrates a powerful backend powered by **Python**, **LLM**, **Gemini**, and **FastAPI**. The frontend is built with **HTML**, **CSS**, and **Vue.js** for a seamless user experience.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

The RAG-APP is designed to answer user queries by pulling real-time information from Gigalogy.com through web scraping. It uses advanced language models (LLM) and APIs like Gemini and Qdrant for retrieving and generating relevant responses. The backend is powered by Python and FastAPI, and the frontend is built with Vue.js to ensure an interactive and responsive interface.

## Features

- **Real-time Data Scraping**: Uses Playwright for scraping data from Gigalogy.
- **Intelligent Query Responses**: Retrieves and generates relevant responses using Gemini and LLM.
- **Seamless User Experience**: Frontend built with Vue.js, ensuring smooth interaction.
- **Fast Backend**: Powered by Python and FastAPI to serve data efficiently.

## Technologies Used

- **Backend**: Python, FastAPI, LLM, Gemini API
- **Frontend**: HTML, CSS, Vue.js
- **Web Scraping**: Playwright
- **Data Storage and Retrieval**: Qdrant
- **APIs**: Gemini, Qdrant

## Installation

### Prerequisites

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/RAG-APP.git
   cd RAG-APP
   ```

2. Obtain the following API credentials:

- **Gemini API**: [Get Gemini API credentials](https://gemini.com/)
- **Qdrant API**: [Get Qdrant API credentials](https://qdrant.tech/)

3. Place the API credentials in the project folder as `gemini_api_credentials.json` and `qdrant_api_credentials.json`.

## Setup and Run

1. **Build and run the application using Docker Compose**:

   ```bash
   docker-compose up --build
   ```
2. After the project starts, the frontend should be available in your browser.

## Usage:
Once the application is up and running, you can:

1. Visit the frontend to enter queries.
2. The backend will scrape data from Gigalogy.com and generate responses using the Gemini API.
3. The frontend will display the results in real-time.




