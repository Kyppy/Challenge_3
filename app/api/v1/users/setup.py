import re


class Regex():
    def __init__(self):
        self.names_pattern = re.compile(r'^[a-zA-Z]{1,25}$')
        self.othername_pattern = re.compile(r'^[a-zA-Z]{0,25}$')
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$')
        self.phone_pattern = re.compile(r'\d{3}-\d{3}-\d{4}')
        self.username_pattern = re.compile(r'^[a-zA-z0-9_.+!?@&-]{1,25}$')
        self.password_pattern = re.compile(r'^[a-zA-z0-9_.+!?@&-]{1,50}$')
        self.id_pattern = re.compile(r'^[0-9]+$')
        self.latlong_pattern = re.compile(r'^[0-9]{1,2}[NS],[0-9]{1,2}[EW]$')