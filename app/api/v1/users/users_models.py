import psycopg2
import os
from passlib.hash import sha256_crypt
DATABASE_URL = os.getenv('DATABASE_URL')


class UsersDatabase():
    def authorise_login(self, username, password):
        """Compare login data to existing users in database.
        If data matches produce access token for user."""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT username,password \
                        FROM users WHERE password = %s", (password,))
        credentials = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        if credentials is None:
            return False
        if username != credentials[0]:
            return False
        if password != credentials[1]:
            return False
        return True

    def authorise_signup(self, username, password, email):
        """Compare signup data to existing user data.
        Prevent duplicate entries of unique fields."""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT username FROM users\
                         WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is not None:
            return False
        cursor.execute("SELECT password FROM users\
                         WHERE password = %s", (password,))
        pass_word = cursor.fetchone()
        if pass_word is not None:
            return False
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        mail = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        if mail is not None:
            return False
        return True

    def connect(self):
        connect = psycopg2.connect(DATABASE_URL)
        return connect

    def create_tables(self):
        """Create a 'users' table in database "
        if it does not already exist"""
        con = self.connect()
        cursor = con.cursor()
        queries = self.tables()
        for query in queries:
            cursor.execute(query)
        cursor.close()
        con.commit()
        con.close()
    
    def check_valid(self, username, password):
        """Compare input username to existing usernames in database.
        If username matches return hashed password."""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT username,password \
                        FROM users WHERE username = %s", (username,))
        credentials = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        if credentials is None:
            return False
        if username != credentials[0]:
            return False
        if sha256_crypt.verify(password, credentials[1]):
            return True
        return False
    
    def drop_tables(self):
        """Drop 'users' table from database"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("""DROP TABLE IF EXISTS users CASCADE""")
        cursor.close()
        con.commit()
        con.close()
    
    def insert_user(self, post_data):
        """Insert a new user row into the database"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO users(firstname, lastname, othername, email,
                 phoneNumber, username, password, isAdmin) VALUES(%s, %s, %s, 
                 %s, %s, %s, %s, %s)"""
        cursor.execute(sql, post_data)
        cursor.close()
        con.commit()
        con.close()
    
    def user_list(self):
        """Selects list of users in descending id order"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT id FROM users ORDER BY id DESC")
        record = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        return record
    
    def tables(self):
        users = """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(25) NOT NULL,
            lastname VARCHAR(25) NOT NULL,
            othername VARCHAR(25),
            email VARCHAR UNIQUE NOT NULL,
            phoneNumber VARCHAR,
            username VARCHAR(25) UNIQUE NOT NULL,
            password VARCHAR UNIQUE NOT NULL,
            registered VARCHAR(25) DEFAULT 'Date-time placeholder',
            isAdmin BOOLEAN DEFAULT 'False' NOT NULL )"""
        tables_query = [users]
        return tables_query