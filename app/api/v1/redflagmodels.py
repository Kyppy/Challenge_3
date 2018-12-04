redflag_incidents = []

class RedFlagModel():

    def __init__(self):
        self.db = redflag_incidents
    
    def store(self, redflag_incidents):
        self.db.append(redflag_incidents)
    
    def get_flags(self):
        return self.db