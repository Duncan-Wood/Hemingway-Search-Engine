# Hemmingway Search Engine

Welcome to my first search engine! This project showcases my skills as a full-stack developer through a search engine application for hemmingway texts. Below, you'll find instructions on how to set up both the backend RESTful API and the frontend React app, along with other relevant project details.

This app can allow users to search words from the corpus of text, create new words, update existing words, and delete words.

## Instructions

Follow the steps below to set up and run both the backend and frontend components of the search engine application.

## Getting Started

Begin by cloning this repository and navigating into the project directory:

```
git clone https://github.com/Duncan-Wood/Hemmingway-Search-Engine.git
cd FullStackDeveloperChallenge
```

### Backend RESTful API for Search Engine

**Prerequisites**
Before you begin, make sure you have Python3 installed on your system.

**Create the Virtual Environment**
Navigate to the backend directory and set up a virtual environment:

```
cd Backend
python3 -m venv search-engine-venv
source search-engine-venv/bin/activate  # On macOS and Linux
# For Windows Command Prompt:
# search-engine-venv\Scripts\activate
# For Windows PowerShell:
# search-engine-venv\Scripts\Activate.ps1
```

**Install the dependencies**
Install the required dependencies for the backend API:

```
pip install -r requirements.txt
```

**Run the API**
Navigate to the search engine Flask app and run the API:

```
cd search-engine-flask
./bootstrap.sh
```

_The bootstrap.sh script prepares the environment and executes the Flask application, making it accessible on all network interfaces._

**Open the API in browser**

Access the API's home page in your browser by visiting the [API Home Page](http://localhost:5000/)

_The home page provides direct links to various API endpoints, making it easy for users to explore and understand the functionalities offered by the API._

## Frontend React App for Search Engine

**Prerequisites**
Before you start, ensure that you have Node.js installed on your system.

**Navigate to the Frontend folder**
Open a separate terminal window and navigate to the frontend app's directory:

```
cd Frontend/search-engine-app
```

**Install Dependencies using NPM**
Install the necessary dependencies for the frontend app:

```
npm install
```

**Run the App**
Start the development server to run the frontend app:

```
npm start
```

This will automatically open the app in your default web browser. Alternatively, you can access the app at [here](http://localhost:3000)

## Technologies Used

**Frontend**

- React: A JavaScript library for building user interfaces.
- axios: A promise-based HTTP client for making requests to the backend.
- pspdfkit: Used for displaying PDF documents.

**Backend**

- Flask: A lightweight web framework for building APIs.
- Flask-Cors: Enables Cross-Origin Resource Sharing (CORS) support in Flask applications.
- Gensim: A Python library for topic modelling, document indexing and similarity retrieval with large corpora.
- Word2Vec: A pre-trained model for generating word embeddings.
- NumPy: A fundamental package for scientific computing with Python.


## Known Issues
- Currently, the similar word only works if at least one instance of the searched word is found in the corpus. This should be an easy fix when I can update my pkl file.
- When similar sentances are returned in the results, the correlating similar word is not highlighted, only the matching word.
- Currently, the API does not interact with the actual pdf. In the future, I would like to add the ability to see results in the pdf, and directly alter the pdf when CRUD is used. 

## Future Improvements
- Add the ability to see results in the pdf, and directly alter the pdf when CRUD is used.
- Improve robustness of similarity search.
- Add tests

## Notes
- The pspdfkit watermark can be removed with purchase.
- The hemingway-clean file is used to restore the corpus to its original state. This is useful if you want to start over with a new corpus.
- The pdf file is used for PSDFKit and is not used by the API.

## Sources

- [ChatGPT](https://chat.openai.com/)
- [PSPDFKit](https://pspdfkit.com/) (watermark can be removed with purchase)
- [Stack Overflow](https://stackoverflow.com/)
- [Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [NumPy](https://numpy.org/)
