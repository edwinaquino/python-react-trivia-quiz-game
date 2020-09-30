# Full Stack Trivia Quiz Game - Backend

## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Database Settings

Open the /backend/models.py file and edit the database credentials to connect to your local postgresql database:
```
database_path = "postgres://{}:{}@{}/{}".format('USERNAME', 'PASSWORD', 'localhost:5432', database_name)
```    

## Running the server

Open a terminal and from within the `backend/` directory run the server with the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
__ERROR__: If you get this error: `OSError: [Errno 98] Address already in use` - The default port is 5001, you can choose to run the Flask server on a different port with the following command:

```bash
flask run --port 5001
```

__NOTE:__ Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

__NOTE:__ Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Open a broswer to test successful running of Flask server and navigate to: http://127.0.0.1:5000/questions

## Testing
This repository includes a file `development` to test your API requests. To run the included tests, open a terminal in the `backend/` directory and execute the following commands:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 
- Open a broswer navigate to: http://127.0.0.1:5000/questions


### Error Handling
Errors are returned in the following json format:

```json
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500 – internal server error

### Endpoints 

#### GET '/categories'

- Gets a list of all the available categories.
- Example CURL command: `curl http://127.0.0.1:5000/categories`

Example:  
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```

#### GET '/questions'

- Returns all available questions.
- Questions are returned in paginated format.
- Example CURL command: `curl http://127.0.0.1:5000/questions`

Example:
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

}
```

### DELETE '/questions/[question_id]'

- Deletes the requested question_id from the questions list 
- Example: `curl http://127.0.0.1:5000/questions/1 -X DELETE`

Example:
```json 
{
    "success":true, 
    "deleted": id}
}
```

### POST '/questions'
- Validates if duplicate question already exists
- Creates a new questions
- The following example creates a Geography question with a difficulty level of 2:
- Example Command: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the capital of California?", "answer": "Sacramento", "difficulty": 2, "category": "3" }'`

```json
Example 
{
    "success":true
}
```

### POST '/questions/search'

- Searches for keywords in question list
- Example: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "royal palace"}'`

Example: 
```json
{
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 23
}


```


### GET /categories/[category_id]/questions

- Get all questions under a specific category
- Example: `curl http://127.0.0.1:5000/categories/1/questions`

Example:
```json
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```


### POST '/quizzes'

- To get a category the a previous questions to play the quiz.
- Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 4], "quiz_category": {"type": "Geography", "id": "3"}}'`

Example Request Payload {"previous_questions":[],"quiz_category":{"type":"Science","id":1}}

Example:
```json 
{
  "question": {
    "answer": "Sacramento", 
    "category": 3, 
    "difficulty": 3, 
    "id": 24, 
    "question": "what is the capital of California"
  }, 
  "success": true
}

```

## Next, Start the Frontend

[View the README.md within ./frontend for more details.](../frontend/README.md)


## Authors
- API models, controllers and documentations added by Edwin Aquino to add API functionality with the React front-end view.

- Udacity Team who provided a template to start this project.
