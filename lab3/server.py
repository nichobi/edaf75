from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote
import inspect

db = sqlite3.connect("movies.sqlite")

db.execute("PRAGMA foreign_keys = ON")

@get('/ping')
def ping():
    return 'pong'

@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        PRAGMA foreign_keys = OFF;
        DELETE FROM theaters;
        DELETE FROM performances;
        DELETE FROM movies;
        DELETE FROM tickets;
        DELETE FROM customers;
        PRAGMA foreign_keys = ON;

        INSERT
        INTO    theaters(theater_name, capacity)
        VALUES  ('Kino', 10),
                ('Regal', 16),
                ('Skandia', 100)
        """
    )
    db.commit()

@post('/users')
def create_user():
    try:
        with db:
            user = request.json
            c = db.cursor()
            c.execute(
                """
                INSERT
                INTO    customers(username, full_name, password)
                VALUES  (?, ?, ?)
                RETURNING username
                """,
                [ user['username']
                , user['fullName']
                , hash(user['pwd'])
                ]
            )
            username, = c.fetchone()
            response.status = 201
            return '/users/' + username
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@post('/movies')
def create_movie():
    try:
        with db:
            movie = request.json
            c = db.cursor()
            c.execute(
                """
                INSERT
                INTO    movies(imdb_key, title, year)
                VALUES  (?, ?, ?)
                RETURNING imdb_key
                """,
                [ movie['imdbKey']
                , movie['title']
                , movie['year']
                ]
            )
            imdb_key, = c.fetchone()
            response.status = 201
            return '/movies/' + imdb_key
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''


@post('/performances')
def create_performance():
    try:
        with db:
            performance = request.json
            c = db.cursor()
            c.execute(
                """
                INSERT
                INTO    performances(imdb_key, theater_name, date, start_time)
                VALUES  (?, ?, ?, ?)
                RETURNING performance_id
                """,
                [ performance['imdbKey']
                , performance['theater']
                , performance['date']
                , performance['time']
                ]
            )
            performance_id, = c.fetchone()
            response.status = 201
            return '/performances/' + performance_id
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@get('/movies')
def get_movies():
    try:
        with db:
            c = db.cursor()
            query = """
                SELECT  imdb_key, title, year
                FROM    movies
                WHERE 1 = 1
                """
            params = []
            if request.query.title:
                query += " AND title = ?"
                params.append(unquote(request.query.name))
            if request.query.year:
                query += " AND year = ?"
                params.append(request.query.minGpa)
            c.execute(query, params)
            found = [{'imdbKey': imdb_key, 'title': title, 'year': year}
                     for imdb_key, title, year in c]
            response.status = 200
            return {'data': found}
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@get('/movies/<imdb_key>')
def get_movie(imdb_key):
    try:
        with db:
            c = db.cursor()
            c.execute(
                """
                SELECT  imdb_key, title, year
                FROM    movies
                WHERE imdb_key = ?
                """,
                [imdb_key]
            )
            found = [{'imdbKey': imdb_key, 'title': title, 'year': year}
                     for imdb_key, title, year in c]
            response.status = 200
            return {'data': found}
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@get('/performances')
def get_performances():
    try:
        with db:
            c = db.cursor()
            c.execute("""
                WITH sales(performance_id, sold_tickets) AS (
                    SELECT performance_id, count()
                    FROM tickets
                    GROUP BY performance_id
                )

                SELECT  performance_id, date, start_time, title, year, theater_name, capacity - coalesce(sold_tickets, 0)
                FROM    performances
                JOIN    movies
                using   (imdb_key)
                JOIN    theaters
                USING   (theater_name)
                LEFT OUTER JOIN sales
                USING   (performance_id)
                """
            )
            found = [{'performanceId': performance_id, 'date': date, 'startTime': start_time,
                      'title': title, 'year': year, 'theater': theater, 'remainingSeats': remaining_seats}
                     for performance_id, date, start_time, title, year, theater, remaining_seats in c]
            response.status = 200
            return {'data': found}
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@post('/tickets')
def get_performances():
    try:
        with db:
            ticket = request.json
            c = db.cursor()
            c.execute("""
                WITH sales(performance_id, sold_tickets) AS (
                    SELECT performance_id, count()
                    FROM tickets
                    GROUP BY performance_id
                )

                SELECT  capacity - coalesce(sold_tickets, 0)
                FROM    performances
                JOIN    theaters
                USING   (theater_name)
                LEFT OUTER JOIN sales
                USING   (performance_id)
                WHERE   performance_id = ?
                """,
                [ticket['performanceId']]
            )
            remaining_seats, = c.fetchone()
            print(remaining_seats)
            if remaining_seats < 1:
                response.status = 400
                return 'No tickets left'

            c.execute("""
                SELECT  1
                FROM    customers
                WHERE   username = ? AND password = ?
                """,
                [ ticket['username']
                , hash(ticket['pwd'])
                ]
            )
            match, = c.fetchone()
            if (match != 1):
                print('match:')
                print(match)
                response.status = 400
                return 'Wrong user credentials'

            c.execute("""
                INSERT
                INTO    tickets(username, performance_id)
                VALUES  (?, ?)
                RETURNING ticket_id
                """,
                [ ticket['username']
                , ticket['performanceId']
                ]
            )
            ticket_id, = c.fetchone()
            response.status = 201
            return '/tickets/' + ticket_id
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        print(e)
        response.status = 400
        return ''

@get('/users/<username>/tickets')
def get_movie(username):
    try:
        with db:
            c = db.cursor()
            c.execute(
                """
                SELECT  date, start_time, theater_name, title, year, count()
                FROM    tickets
                JOIN    performances
                USING   (performance_id)
                JOIN    movies
                USING   (imdb_key)
                WHERE   username = ?
                GROUP BY performance_id
                """,
                [username]
            )

            found = [{'date': date, 'startTime': start_time, 'theater': theater_name, 'title': title, 'year': year, 'nbrOfTickets': nbr_of_tickets,}
                     for date, start_time, theater_name, title, year, nbr_of_tickets in c]
            response.status = 200
            return {'data': found}
    except Exception as e:
        print('Exception occured on line' + str(inspect.currentframe().f_lineno))

        raise(e)
        response.status = 400
        return ''

run(host='localhost', port=7007)

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

db.close()
