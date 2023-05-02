# CAPSTONE - Final Project

## Filmopedia App

Flimopedia is a casting agency that is responsible for creating movies and managing and assigning actors to those movies. This app is used to maintain the data of movies and the actors.

Roles:
Any one or Casting Assistant - Can view actors and movies
Casting Director - All permissions a Casting Assistant has and Add or delete an actor from the database, Modify actors or movies
Executive Producer - All permissions a Casting Director has and Add or delete a movie from the database

### Getting Started
- Base URL: This app is hosted in render and below is the URL.
https://capstone170204.us.auth0.com/authorize?audience=MovieActor&response_type=token&client_id=NCSOQvOaUTnisD0gvfrfcZrJXlDrp7mM&redirect_uri=https://capstone170204.onrender.com/movies
- Authentication: Role based authentication is provisioned.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: method not allowed
- 422: Not Processable 
- AuthError 

### Endpoints 
#### GET /movies
- General:
    - Returns a list of movies, success value, total movies.
    - The movies are listed 10 per page
- Sample: `curl https://capstone170204.onrender.com/movies`
- With Authorization: `Curl https://capstone170204.onrender.com/movies -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
  "movies": [
    {
      "id": 1,
      "release_date": "Fri, 28 Apr 2023 00:00:00 GMT",
      "title": "PS2"
    }
  ],
  "success": true,
  "total_movies": 1
}
```

#### GET /actors
- General:
    - Returns a list of actors, success value, total actors.
    - The actors are listed 10 per page
- Sample: `curl https://capstone170204.onrender.com/actors`
- With Authorization: `Curl https://capstone170204.onrender.com/actors -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
  "actors": [
    {
      "age": 70,
      "gend": "M",
      "id": 1,
      "name": "RajiniKanth"
    }
  ],
  "success": true,
  "total_actors": 1
}
```
#### POST /movies

- General:
    - Adds a movie using the movie title and release date.
    - Returns success value and title of the created movie.
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"title\":\"NeverWhere\",\"release_date\":\"2023-06-01\"}" https://capstone170204.onrender.com/movies`

```{
  "created":4,
  "success":true,
  "title":"NeverWhere"
  }
```
#### POST /actors

- General:
    - Adds an actor using the actor name, age and gender.
    - Returns success value and name of the created actor.
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"name\":\"Karthi\",\"age\":42,\"gender\":\"M\"}" https://capstone170204.onrender.com/actors`

```{
  "actor name":"Karthi",
  "created":6,
  "success":true
}
```
#### POST /actors

- General:
    - Adds an actor using the actor name, age and gender.
    - Returns success value and name of the created actor.
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"name\":\"Karthi\",\"age\":42,\"gender\":\"M\"}" https://capstone170204.onrender.com/actors`

```{
  "actor name":"Karthi",
  "created":6,
  "success":true
}
```
#### POST /movieactors

- General:
    - Actors are mapped to movies.
    - Returns success value, actor and movie information.
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"movie_id\":4,\"actor_id\":6}" https://capstone170204.onrender.com/movieactors`

```{
    "Actor in the movie": [
        {
            "age": 42,
            "gend": "M",
            "id": 6,
            "name": "Karthi"
        }
    ],
    "Movie details": [
        {
            "id": 4,
            "release_date": "Thu, 01 Jun 2023 00:00:00 GMT",
            "title": "NeverWhere"
        }
    ],
    "success": true
}
```
#### PATCH /actors/<actor-id>

- General:
    - Updates the actor information with the actor age and gender.
    - Returns success value and information of the updated actor.
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"age\": 50}" https://capstone170204.onrender.com/actors/2`

```{
    "Updated details": [
        {
            "age": 50,
            "gend": "M",
            "id": 2,
            "name": "Surya"
        }
    ],
    "success": true
}
```
#### PATCH /movies/<movie-id>

- General:
    - Updates the movie information with the release date.
    - Returns success value and information of the updated movie.
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d "{\"reldate\": \"2023-10-23\"}" https://capstone170204.onrender.com/movies/4`

```{
    "Updated details": [
        {
            "id": 4,
            "release_date": "Mon, 23 Oct 2023 00:00:00 GMT",
            "title": "NeverWhere"
        }
    ],
    "success": true
}
```
#### DELETE /movies/<movie-id>

- General:
    - Delete the movie 
    - Returns success value and information of the deleted movie.
- Sample: `curl -X DELETE -H "Authorization: Bearer {token}" https://capstone170204.onrender.com/movies/3`

```{
    "deleted movie": [
        {
            "id": 3,
            "release_date": "Mon, 19 Dec 2022 00:00:00 GMT",
            "title": "KGF-2"
        }
    ],
    "success": true
}
```
#### DELETE /actors/<actor-id>

- General:
    - Delete the actor 
    - Returns success value and information of the deleted actor.
- Sample: `curl -X DELETE -H "Authorization: Bearer {token}" https://capstone170204.onrender.com/actors/1`

```{
    "deleted actor": [
        {
            "age": 70,
            "gend": "M",
            "id": 1,
            "name": "Rajini"
        }
    ],
    "success": true
}
```