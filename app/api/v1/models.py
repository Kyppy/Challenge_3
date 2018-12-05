import psycopg2

url = "dbname='ireporter' host='localhost'\
             port='5432' user='postgres' password='Nanbada13'"


class Database():
    def connect(self):
        connect = psycopg2.connect(url)
        return connect

    def create_tables(self):
        """Create 'users' and 'incidents' tables
        in database if they do not already exist"""
        con = self.connect()
        cursor = con.cursor()
        queries = self.tables()
        for query in queries:
            cursor.execute(query)
        cursor.close()
        con.commit()
        con.close()

    def insert_intervention(self, post_data):
        """Insert a new intervention row into the database"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO incidents(id,type,location,Images,Videos,comment)
                 VALUES(%s, %s, %s, %s,
                 %s, %s)"""
        cursor.execute(sql, post_data)
        cursor.close()
        con.commit()
        con.close()

    def insert_user(self, post_data):
        """Insert a new user row into the database"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO users(firstname, lastname, othername, email,
                 phoneNumber, username, password) VALUES(%s, %s, %s, %s,
                 %s, %s, %s)"""
        cursor.execute(sql, post_data)
        cursor.close()
        con.commit()
        con.close()

    def update_intervention_location(self, patch_data):
        """Edit the 'location' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET location = %s
                    WHERE id = %s"""
        cursor.execute(sql, patch_data)
        cursor.close()
        con.commit()
        con.close()

    def update_intervention_comment(self, patch_data):
        """Edit the 'comment' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET comment = %s
                    WHERE id = %s"""
        cursor.execute(sql, patch_data)
        cursor.close()
        con.commit()
        con.close()

    def get_all_interventions(self):
        """Fetch all intervention records"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM incidents")
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list

    def get_intervention(self, intervention_id):
        """Fetch a specific intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s"""
        cursor.execute(sql, (intervention_id,))
        record = cursor.fetchone()   
        cursor.close()
        con.commit()
        con.close()
        return record

    def delete_record(self, intervention_id):
        """Delete a specific intervention record"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("DELETE FROM incidents WHERE id = %s", 
                       (intervention_id,))   
        cursor.close()
        con.commit()
        con.close()

    def tables(self):
        users = """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(25) NOT NULL,
            lastname VARCHAR(25) NOT NULL,
            othername VARCHAR(25),
            email VARCHAR(50) UNIQUE NOT NULL,
            phoneNumber INTEGER,
            username VARCHAR(25) UNIQUE NOT NULL,
            password VARCHAR(50) UNIQUE NOT NULL,
            registered VARCHAR(25) DEFAULT 'Date-time placeholder',
            isAdmin BOOLEAN DEFAULT 'false' NOT NULL )"""
        incidents = """CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER UNIQUE PRIMARY KEY,
            createdOn VARCHAR(25) DEFAULT 'Date-time placeholder',
            createdBy INTEGER DEFAULT '10',
            type VARCHAR NOT NULL,
            location VARCHAR,
            status VARCHAR DEFAULT 'Unresolved',
            Images VARCHAR,
            Videos VARCHAR,
            comment VARCHAR(500) NOT NULL )"""
        tables_query = [users, incidents]
        return tables_query
                