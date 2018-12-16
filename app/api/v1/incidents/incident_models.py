import psycopg2
import os
DATABASE_URL = os.getenv('DATABASE_URL')


class IncidentsDatabase():
    def connect(self):
        connect = psycopg2.connect(DATABASE_URL)
        return connect

    def create_tables(self):
        """Create an 'incidents' table in database "
        if it does not already exist"""
        con = self.connect()
        cursor = con.cursor()
        queries = self.tables()
        for query in queries:
            cursor.execute(query)
        cursor.close()
        con.commit()
        con.close()
    
    def check_user(self, check_data):
        """Check if the session username \
        matches username in incident record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s AND \
              createdBy = %s"""
        cursor.execute(sql, check_data)
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return True
    
    def check_rank(self, username):
        """Check if given user has elevated permissions"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM users WHERE username = %s AND \
              isAdmin = TRUE"""
        cursor.execute(sql, (username,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return True

    def delete_record(self, intervention_id):
        """Delete a specific intervention record"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("DELETE FROM incidents WHERE id = %s", 
                       (intervention_id,))   
        cursor.close()
        con.commit()
        con.close()

    def drop_tables(self):
        """Drop 'incidents' table from database"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("""DROP TABLE IF EXISTS incidents CASCADE""")
        cursor.close()
        con.commit()
        con.close()
    
    def fetch_type(self, incident_id):
        """Returns the 'type' of a given incident"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT type,id FROM incidents WHERE id = %s"""
        cursor.execute(sql, (incident_id,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return record[0]
    
    def get_all_interventions(self):
        """Fetch all intervention records"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM incidents WHERE type = 'Intervention'")
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list

    def get_all_redflags(self):
        """Fetch all redflag records"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM incidents WHERE type = 'Redflag'")
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list
    
    def get_intervention(self, intervention_id):
        """Fetch a specific intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s AND \
              type = 'Intervention'"""
        cursor.execute(sql, (intervention_id,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return record
    
    def get_latest_id(self):
        """Fetch the 'id' of the latest incident record"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT id FROM incidents ORDER BY id DESC")
        record = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        return record
    
    def get_redflag(self, redflag_id):
        """Fetch a specific redflag record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s AND \
              type = 'Redflag'"""
        cursor.execute(sql, (redflag_id,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return record

    def insert_intervention(self, post_data):
        """Insert a new intervention row into the database"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO incidents(type,location,Images,
                 Videos,comment,createdOn,createdBy)
                 VALUES(%s, %s, %s,
                 %s, %s, %s, %s)"""
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
    
    def update_intervention_status(self, patch_data):
        """Edit the 'status' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Intervention'"""
        cursor.execute(sql, patch_data)
        cursor.close()
        con.commit()
        con.close()
    
    def update_redflag_status(self, patch_data):
        """Edit the 'status' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Redflag'"""
        cursor.execute(sql, patch_data)
        cursor.close()
        con.commit()
        con.close()

    def tables(self):
        incidents = """CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            createdOn VARCHAR(25) DEFAULT 'Date-time placeholder',
            createdBy VARCHAR DEFAULT 'Anon',
            type VARCHAR NOT NULL,
            location VARCHAR,
            status VARCHAR DEFAULT 'Under investigation',
            Images VARCHAR,
            Videos VARCHAR,
            comment VARCHAR(500) NOT NULL )"""
        tables_query = [incidents]
        return tables_query