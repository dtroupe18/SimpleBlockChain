
class EHR(object):
    """
    Class designed to store an electronic health record for the POC blockChain


    """
    def __init__(self, first_name, last_name, date, physicians_name, notes):
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.physicians_name = physicians_name
        self.notes = notes

