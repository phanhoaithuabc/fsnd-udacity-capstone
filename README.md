# fsnd udacity capstone restaurant management

## Motivation for the project

The application will help manage restaurant:
1. Allow chef and manager to list all food in restaurant DB.
2. Allow chef and manager to view the ingredients in each food.
3. Allow the managers to delete food in restaurant DB.
4. Allow the managers to add new food into restaurant DB.
5. Allow the managers to modify existing food in restaurant DB.

## URL location for the hosted API

You can access this project [here](https://fsnd-udacity-capstone.onrender.com/)

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

`GET /drinks-detail`

- Fetches a drink detail
- Request Arguments: None
- Results: A json contain drink detail


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

`PATCH /drinks/{id}`

- Update the exist drink in database
- Request Body:
  ```javascript
  {
    "title": "Water7"
  }
  ```
- results: The drink to update