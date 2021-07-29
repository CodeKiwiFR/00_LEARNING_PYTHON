from .Contact import Contact

class FileCorrupted(Exception):
    """
    My own exception for dealing with file content problems
    """
    pass

class ContactList:
    """
    Manages a list of contacts
    """
    def __init__(self):
        """
        The list is created
        We read from the contacts.txt file which is supposed to be in the same folder
        If the file does not exist or is not well formatted, then an exception is thrown
        """
        self.contacts = []
        try:
            self.readFromFile()
        except (FileNotFoundError, FileExistsError):
            raise FileNotFoundError
        except FileCorrupted:
            raise FileCorrupted

    def __str__(self):
        """
        Just the string output of the class
        """
        my_str = ''
        for contact in self.contacts:
            my_str += str(contact) + '\n'
        return (my_str)

    def readFromFile(self):
        """
        Reads from the contacts file
        Feeds the contact list with the file content
        Throws an exception if the file does not exist or if it is not well formatted
        """
        try:
            fd = open('contacts.txt', 'r')
        except (FileNotFoundError, FileExistsError):
            raise FileNotFoundError
        while True:
            try:
                contact = self.readContact(fd)
            except:
                raise FileCorrupted
            if (contact == None):
                break
            self.contacts.append(contact)
        fd.close()

    def readContact(self, fd):
        """
        Decoding the file for extracting one contact from it
        Returns the contact if it exists
        Throws an exception if there is a problem during the exctratction
        Returns None if it reaches the end of file
        """
        fname_line = fd.readline()
        # Checking if end of file or if we have read an empty line
        if (fname_line == ''):
            return None
        elif (fname_line == '\n'):
            fname_line = fd.readline()
            if (fname_line == ''):
                return None
        # Extracting the different contact fields
        fname_line_split = fname_line.split('-|-')
        lname_line = fd.readline()
        lname_line_split = lname_line.split('-|-')
        address_line = fd.readline()
        address_line_split = address_line.split('-|-')
        cp_line = fd.readline()
        cp_line_split = cp_line.split('-|-')
        phone_line = fd.readline()
        phone_line_split = phone_line.split('-|-')
        # Checking validity of the fields
        if (
            fname_line_split[0] != 'fname' or
            lname_line_split[0] != 'lname' or
            address_line_split[0] != 'address' or
            cp_line_split[0] != 'cp' or
            phone_line_split[0] != 'phone'
        ):
            raise FileCorrupted
        try:
            fname = fname_line_split[1].replace('\n', '')
            lname = lname_line_split[1].replace('\n', '')
            address = address_line_split[1].replace('\n', '')
            cp = cp_line_split[1].replace('\n', '')
            phone = phone_line_split[1].replace('\n', '')
        except:
            raise FileCorrupted
        return (Contact(fname, lname, address, cp, phone))

    def sort(self):
        """
        Sorts the contact list according to contacts last names / first names
        """
        print('sorting or not...')

    def save_file(self):
        """
        Writes all the contact list into the contacts.txt file
        The file is entirely overwritten
        """
        fd = open('contacts.txt', 'w')
        for contact in self.contacts:
            fd.write('fname-|-' + contact.fname + '\n')
            fd.write('lname-|-' + contact.lname + '\n')
            fd.write('address-|-' + contact.address + '\n')
            fd.write('cp-|-' + contact.cp + '\n')
            fd.write('phone-|-' + contact.phone + '\n\n')
        fd.close()
