# fsnd-udacity-capstone

## Motivation for the project

The application will help:
1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## URL location for the hosted API

You can access this project [here](http://..)

## Run this project

This project contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

```bash
# install dependency
pip install -r requirements.txt

# set up the environment varriable
export FLASK_APP=api.py

# run application
python -m flask run
```

## Hosting instructions


## Documentation For Backend Endpoint

### There are 2 Roles:

1. Barista role:
    - GET:drinks: Can see all drinks
    - GET:drinks-detail: Can see drinks detail
2. Manager role:
    - GET:drinks: Can see all drinks
    - GET:drinks-detail: Can see drinks detail
    - DELETE:drinks: Can remove drinks from database
    - PATCH:drinks: Can edit existing drinks from DB
    - POST:drinks: Can create new drinks

### There are 5 API:

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

`GET /drinks`

- Fetches a list of drinks
- Request Arguments: None
- Results: A json contain drinks

<!-- ```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": True
}
``` -->

`GET /drinks-detail`

- Fetches a drink detail
- Request Arguments: None
- Results: A json contain drink detail

  <!-- ```javascript
  {
    "success": True,
    "questions": [
      {
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou",
        "difficulty": 2,
        "category": 4
      }
    ],
    "totalQuestions": 19,
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "currentCategory": "History"
  }
  ``` -->

`DELETE /drinks/{id}`

- Deletes drink of the given ID if it exists
- Results: drink's ID after delete

  ```javascript
  {
    "success": true,
    "delete": 1
  }
  ```

`POST /drinks`

- Sends a post request to add a new drinks into DB.
- Request Body:
  ```javascript
    {
        "title": "Water3",
        "recipe": {
            "name": "Water",
            "color": "blue",
            "parts": 1
        }
    }
  ```
- Result: Result of that drink we just add

  <!-- ```javascript
  {
    "success": true, 
    "created": 24, 
    "questions": [
      {
        "answer": "Maya Angelou",
        "category": "4", 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      .....
    ], 
    "total_questions": 19
  }
  ``` -->

`PATCH /drinks/{id}`

- Update the exist drink in database
- Request Body:
  ```javascript
  {
    "title": "Water7"
  }
  ```
- results: The drink to update

  <!-- ```javascript
  {
    "question": {
      "answer": "100", 
      "category": "3", 
      "difficulty": 1, 
      "id": 24, 
      "question": "How much?"
    }, 
    "success": True,
    "previousQuestion": 1
  }
  ``` -->