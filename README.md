# Loja Integrada Cart API
Cart API with items management

## Configuring and Running the Project
We use Docker to generate a container with all the requirements needed to run the API.
Follow these steps to run the project:
 - Install Docker on your machine ([Click here to get Docker](https://docs.docker.com/get-docker/))
 - Run the command `docker build -t loja-integrada .` to build the image
 - Run the command `docker run -d --name loja-integrada -p 8000:8000 loja-integrada` to start the container
 - Done! You can access the API at [http://localhost:8000/](http://localhost:8000/)


## Testing the API
- To test the API endpoints, access [http://localhost:8000/docs](http://localhost:8000/docs)
The documentation is generated by FastAPI and you can use it to try the endpoints and their responses


## Work Flow
- Generate a new cart using the Create Cart (POST /cart) endpoint
- Using its id, you can test all the others endpoints


## General Information
- To keep it simple, the database is structured in a JSON file (database.json), present on project's root
- In the same note, the items.json file works as a makeshift product API
- You can run the command `pytest --cov` to see the project's test coverage

## Technologies Used
- Python 3.10
- FastAPI 0.78.0
- uvicorn 0.17.6


