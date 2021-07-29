import tkinter as tk
from .Contact import Contact
from .ContactList import ContactList
from .ContactList import FileCorrupted

class App:
    """
    Main class for the app
    Creates the windows and manages the interactions between data structures
    Contains a ContactList
    """
    def __init__(self):
        # Creating the main window
        self.win = tk.Tk()
        self.win.title('Contact Management')
        self.win.geometry('300x250')
        self.button_frame = tk.Frame(self.win)
        self.button_frame.place(anchor='c', relx=0.5, rely=0.5)
        tk.Button(self.button_frame, text='Add a contact', command=self.add_contact).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.button_frame, text='Read contact list', command=self.read_list).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.button_frame, text='Exit', command=self.win.destroy).grid(row=2, column=0, padx=10, pady=10)
        self.can = tk.Canvas(self.button_frame, width=200, height=50, bg='light gray')
        self.can.grid(row=4, column=0, padx=10, pady=5)
        self.logo = tk.PhotoImage(file='./image/ck.png')
        self.can.create_image(100, 20, image=self.logo)

        # Creating the contact list form file, dealing with errors
        self.error_label = tk.Label(self.button_frame, text='', fg='red')
        self.error_label.grid(row=3, column=0, padx=10, pady=5)
        self.error = False
        try:
            self.contact_list = ContactList()
        except (FileNotFoundError):
            # If the file does not exist, we create it and create an empty contact list
            fd = open('contacts.txt', 'w')
            fd.close()
            self.error_label.config(text='Contact file created', fg='green')
            self.contact_list = ContactList()
        except FileCorrupted:
            # If the file exists but does not have the correct structure, the app is locked and the user is supposed to solve the problem
            self.error = True
            self.error_label.config(text='ERROR - Contact file corrupted')
        
        self.win.mainloop()

    def add_contact(self, contact=None, read_win=None):
        """
        Displays the add/edit contact window
        If contact argument is None, then we manage contact addition
        Else, we manage contact editing
        """
        if (self.error):
            return
        
        # Creating the window
        add_win = tk.Toplevel(self.win)
        add_form_frame = tk.Frame(add_win)
        add_form_frame.grid(row= 0, column=0)
        tk.Label(add_form_frame, text='First Name :').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        fname_entry = tk.Entry(add_form_frame)

        # Feeding the entries with contact info in case of editing
        if (contact):
            fname_entry.insert(0, contact.fname)
        fname_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Last Name :').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        lname_entry = tk.Entry(add_form_frame)
        if (contact):
            lname_entry.insert(0, contact.lname)
        lname_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Mailing Address :').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        address_entry = tk.Entry(add_form_frame)
        if (contact):
            address_entry.insert(0, contact.address)
        address_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Postal Code :').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        cp_entry = tk.Entry(add_form_frame)
        if (contact):
            cp_entry.insert(0, contact.cp)
        cp_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Phone Number :').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        phone_entry = tk.Entry(add_form_frame)
        if (contact):
            phone_entry.insert(0, contact.phone)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)
        error_label = tk.Label(add_form_frame, text='', fg='red')
        error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        add_button_frame = tk.Frame(add_win)
        add_button_frame.grid(row= 1, column=0)

        # Adding the saving button calling a save or an edit function according to contact argument
        if (contact):
            tk.Button(add_button_frame, text='Save', command=lambda: self.edit_contact(contact, fname_entry.get(), lname_entry.get(), address_entry.get(), cp_entry.get(), phone_entry.get(), add_win, read_win, error_label)).grid(row=0, column=0, padx=10, pady=10)
        else:
            tk.Button(add_button_frame, text='Save', command=lambda: self.save_contact(fname_entry.get(), lname_entry.get(), address_entry.get(), cp_entry.get(), phone_entry.get(), add_win, error_label)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(add_button_frame, text='Exit', command=lambda: self.close_top_level(add_win)).grid(row=0, column=1, padx=10, pady=10)
        add_win.mainloop()

    def consult_contact(self, contact):
        """
        Displays the contact profile window
        """
        if (self.error):
            return
        add_win = tk.Toplevel(self.win)
        add_form_frame = tk.Frame(add_win)
        add_form_frame.grid(row= 0, column=0)

        tk.Label(add_form_frame, text='First Name :').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_form_frame, text=contact.fname).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Last Name :').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_form_frame, text=contact.lname).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Address :').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_form_frame, text=contact.address).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='CP :').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_form_frame, text=contact.cp).grid(row=3, column=1, padx=5, pady=5)
        tk.Label(add_form_frame, text='Phone :').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_form_frame, text=contact.phone).grid(row=4, column=1, padx=5, pady=5)

        add_button_frame = tk.Frame(add_win)
        add_button_frame.grid(row= 1, column=0)
        tk.Button(add_button_frame, text='Exit', command=lambda: self.close_top_level(add_win)).grid(row=0, column=0, padx=10, pady=10)
        add_win.mainloop()
    
    def read_list(self):
        if (self.error):
            return
        # Crating the reading window
        read_win = tk.Toplevel(self.win)
        read_list_frame = tk.Frame(read_win)
        read_list_frame.grid(row= 0, padx=10, pady=15)
        list_contact_interaction = []
        index = 0
        for contact in self.contact_list.contacts:
            # For each contact, we create a line with its fname and lname and three buttons
            # All the buttons are stored with the contact in a list
            tk.Label(read_list_frame, text=contact.fname).grid(row = index, column=0, padx=10, pady=10)
            tk.Label(read_list_frame, text=contact.lname).grid(row = index, column=1, padx=10, pady=10)
            # Tip: we bind each button with a function and set an argument to save the information of the contact linked to the button
            contact_consult = tk.Button(read_list_frame, text='Consult', command=lambda contact=contact: self.consult_contact(contact))
            contact_consult.grid(row = index, column=2, padx=10, pady=10)
            contact_edit = tk.Button(read_list_frame, text='Edit', command=lambda contact=contact: self.add_contact(contact, read_win))
            contact_edit.grid(row = index, column=3, padx=10, pady=10)
            contact_delete = tk.Button(read_list_frame, text='Delete', command=lambda index=index: self.delete_contact(index, list_contact_interaction, read_win))
            contact_delete.grid(row = index, column=4, padx=10, pady=10)
            temp_list = [contact, contact_consult, contact_edit, contact_delete]
            list_contact_interaction.append(temp_list)
            index += 1
        read_button_frame = tk.Frame(read_win)
        read_button_frame.grid(row= 1)
        tk.Button(read_button_frame, text='Exit', command=lambda: self.close_top_level(read_win)).grid(row=0, column=1, padx=10, pady=10)
        read_win.mainloop()

    def delete_contact(self, index, list_contact_interaction, read_win):
        """
        Manages the contact deleting
        Deletes the contact from the contact list, saves the new list into the file and refreshes the window
        """
        contact = list_contact_interaction[index][0]
        list_contact_interaction.pop(0)
        index_to_rm = self.contact_list.contacts.index(contact)
        self.contact_list.contacts.pop(index_to_rm)
        self.contact_list.save_file()
        self.close_top_level(read_win)
        self.read_list()

    def save_contact(self, fname, lname, address, cp, phone, add_win, error_label):
        """
        Saves a new contact into the list and writes it into the file
        """
        address = address if address != '' else ' '
        cp = cp if cp != '' else ' '
        phone = phone if phone != '' else ' '
        if (fname != '' and lname != ''):
            contact = Contact(fname, lname, address, cp, phone)
            self.contact_list.contacts.append(contact)
            self.contact_list.save_file()
            self.close_top_level(add_win)
        else:
            error_label.config(text='ERROR - First name and last name required')

    def edit_contact(self, contact, fname, lname, address, cp, phone, add_win, read_win, error_label):
        """
        Modifies a given contact info into the contact list and saves it into the file
        """
        # Dealing with empty fields
        address = address if address != '' else ' '
        cp = cp if cp != '' else ' '
        phone = phone if phone != '' else ' '
        # Rejecting if fname or lname are empty
        if (fname == '' or lname == ''):
            error_label.config(text='ERROR - First name and last name required')
            return
        # Editing contact
        contact_index = self.contact_list.contacts.index(contact)
        contact_registered = self.contact_list.contacts[contact_index]
        contact_registered.fname = fname
        contact_registered.lname = lname
        contact_registered.address = address
        contact_registered.cp = cp
        contact_registered.phone = phone
        self.contact_list.save_file()
        self.close_top_level(add_win)
        self.close_top_level(read_win)
        self.read_list()

    def close_top_level(self, to_close):
        """
        Closes a window and destroys the associated event loop
        """
        to_close.destroy()
        to_close.update()
        to_close.quit()