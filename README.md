# Description

### Simple Python Rest API which seeks for and store events by given date in MongoDB. Four endpoints were created:

1 Upload new date (day and month specified in content type: application/json;charset=UTF-8)

    POST /dates 
    
    Content-Type: application/json;charset=UTF-8
    {
        "month": #,
        "day": #,
    }

2 Delete the date with the given id from the database (required additional header)

    DELETE /dates/{id}
    
    Header:
    X-API-KEY: BASIC_KEY

3 Fetch a list of all the dates present in the application database with their fun fact

    GET /dates

4 Return the ranking of months present in the database based on the number of
days that have been checked

    GET /popular
## Running on Heroku

REST API working under url:

    mysterious-bastion-72045.herokuapp.com

All endpoints described in first chapter work with this url.

Note: First request might take a longer time to response caused by the 
need to wake up the application 

## Pre-requisites 
REST API implemented using Flask framework.

MongoDB as a database.

Docker and docker-compose installed with linux containers.

Pytest to test endpoints.

## Building and running

To build the project run docker-compose build command.

Once the build finishes run docker-compose up -d. Application should start and be reachable at localhost

## Testing

To test the project run pytest test_routes.py command. Unit tests are checking the endpoints.

