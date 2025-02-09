"""
Lab 3 Base de Datos 2
Juan Gonzalez-Campo 21077
Pedro Marroquin 21801
Paulo Sanchez 21401
"""
#Importacion de librerias
from neo4j import GraphDatabase
#Datos de conexión
URI="neo4j+s://f955a66e.databases.neo4j.io"
AUTH=("neo4j","9h4UWCWtkxjqM90NQrXDmDmF8O342uMJrrpRsyP58mU")
AURA_INSTANCEID="f955a66e"
AURA_INSTANCENAME="Instance01"
#Conexión
#Creando el driver de neo4j
driver = GraphDatabase.driver(URI, auth=AUTH)

# Test the connection with a simple query
def test_connection(driver):
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful' AS message")
        print(result.single()["message"])

# Run the test
test_connection(driver)

#Definicion de funciones
#Ejercicio1
def USER(driver,name,userID,movie_name,rate):
    result=driver.execute_query(
        """
        MERGE (u:USER {name: $name, user:$userID}) 
        MERGE (m:Movie {movie_name:$movie_name})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating=$rate,r.timestamp=datetime()
        RETURN u,r,m
        """,
        name=name,userID=userID,movie_name=movie_name,rate=rate,database="neo4j"
    )
    print(f"Usuario '{name}' (ID: {userID}) ha calificado la película '{movie_name}' con {rate} estrellas.")
    return result
def MOVIE1(driver,title,movieId,year,plot):
    result=driver.execute_query(
    """
    MERGE (m:Movie{title:$title,movieId:$movieId,year:$year,plot:$plot})
    RETURN m
    """,
    title=title,movieId=movieId,year=year,plot=plot,database="neo4j"
    )
    print(f"Película '{title}' (ID: {movieId}) añadida correctamente.")
    return result

def find_user_by_id(driver, userID):
    result = driver.execute_query(
        """
        MATCH (u:USER {userID: $userID})
        RETURN u
        """,
        userID=userID, database="neo4j"
    )
    if result.records:
        print(f"Usuario encontrado: {result.records[0]['u']}")
    else:
        print(f"No se encontró ningún usuario con ID: {userID}")
    return result
def find_movie_by_id(driver, movieId):
    result = driver.execute_query(
        """
        MATCH (m:Movie {movieId: $movieId})
        RETURN m
        """,
        movieId=movieId, database="neo4j"
    )
    if result.records:
        print(f"Película encontrada: {result.records[0]['m']}")
    else:
        print(f"No se encontró ninguna película con ID: {movieId}")
    return result
def find_user_movie_rating(driver, user_id, movie_id):
    result = driver.execute_query(
        """
        MATCH (u:USER {user: $user_id})-[r:RATED]->(m:Movie {movieId: $movie_id})
        RETURN u, r, m
        """,
        user_id=user_id, movie_id=movie_id, database="neo4j"
    )

    # Verificar si hay resultados
    if result.records:  # Usar .records para acceder a los registros
        record = result.records[0]  # Tomar el primer registro
        user = record["u"]
        movie = record["m"]
        rating = record["r"]

        return {
            "User": {"id": user["user"], "name": user["name"]},
            "Movie": {"id": movie["movieId"], "title": movie["title"], "year": movie["year"]},
            "Rating": {"score": rating["rating"], "timestamp": rating["timestamp"]}
        }
    else:
        return "No rating found between the user and movie."

#Ejercicio2
def MOVIE(driver,title,tmdbld,released,imdbrating,movieID,year,imdbld,runtime,countries,imdbVotes,url,revenue,plot,poster,budget,languages,genre):
    driver.execute_query(
        """
        MERGE (m:Movie{title:$title,tmdbld:$tmdbld,released:$released,imdbrating:$imdbrating,movieID:$movieID,year:$year,imdbld:$imdbld,runtime:$runtime,countries:$countries,imdbVotes:$imdbVotes,url:$url,revenue:$revenue,plot:$plot,poster:$poster,budget:$budget,languages:$languages})
        MERGE (g:genre{name:$genre})
        MERGE (m)-[r:IN_GENRE]->(g)
        RETURN m,r,g
        """,
        title=title,tmdbld=tmdbld,released=released,imdbrating=imdbrating,movieID=movieID,year=year,imdbld=imdbld,runtime=runtime,countries=countries,imdbVotes=imdbVotes,url=url,revenue=revenue,plot=plot,poster=poster,budget=budget,languages=languages,genre=genre,database="neo4j"
    )

def Person(driver,name,tmdbld,born,died,bornIn,url,imdbld,bio,poster,relation,role,movie_name):
    driver.execute_query(
        """
        MERGE (p:Person{name:$name,tmdbld=$tmdbld,born:$born,died:$died,bornIn:$bornIn,url:$url,imdbld:$imdbld,bio:$bio})
        MERGE (m:Movie{movie_name=$movie_name})
        MERGE (u)-[r:relation]->(m)
        SET r.role=role
        RETURN u,r,m
        """,
        name=name,tmdbld=tmdbld,born=born,died=died,bornIn=bornIn,url=url,imdbld=imdbld,bio=bio,poster=poster,relation=relation,role=role,movie_name=movie_name,database="neo4j"
    )

#Poblando ejercicio#1

# Datos de películas
peliculas = [
    {"title": "Inception", "movieId": 101, "year": 2010, "plot": "A thief who steals corporate secrets through the use of dream-sharing technology."},
    {"title": "The Matrix", "movieId": 102, "year": 1999, "plot": "A computer hacker learns from mysterious rebels about the true nature of his reality."}
]

# Calificaciones de películas por usuarios
usuarios_y_calificaciones = [
    {"name": "Alice", "user": 1, "movie_name": "Inception", "rate": 5},
    {"name": "Bob", "user": 2, "movie_name": "Inception", "rate": 4},
    {"name": "Charlie", "user": 3, "movie_name": "The Matrix", "rate": 5},
    {"name": "David", "user": 4, "movie_name": "The Matrix", "rate": 4},
    {"name": "Eve", "user": 5, "movie_name": "Inception", "rate": 3}
]
"""
# Poblar películas
for pelicula in peliculas:
    MOVIE1(driver, pelicula["title"], pelicula["movieId"], pelicula["year"], pelicula["plot"])

# Poblar usuarios y sus calificaciones
for usuario in usuarios_y_calificaciones:
    USER(driver, usuario["name"], usuario["user"], usuario["movie_name"], usuario["rate"])

"""
"""
print(find_user_by_id(driver,1))
print(find_movie_by_id(driver,102))
print(find_user_movie_rating(driver,1,102))"""
# Cerrar la conexión
driver.close()