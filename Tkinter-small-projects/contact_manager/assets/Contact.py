import uuid

class Contact:
    """
    Contact class
    A counter is created using a class attribute
    An id is associated to a contact but this is not used in the app for the moment (need to clarify the id creation)
    """
    num = 0
    def __init__(self, fname, lname, address, cp, phone):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.cp = cp
        self.phone = phone
        Contact.num += 1
        self.id = str(uuid.uuid1(Contact.num))
            
    def __str__(self):
        return (self.fname + ' ' + self.lname + ' - ID: ' + self.id)