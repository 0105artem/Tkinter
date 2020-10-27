#! python3
"""
A program that stores this book information:
Title, Author, Year, ISBN

User can:
View all records
Search an entry
Add entry
Delete
Close
"""

from backend_oop import Database
from tkinter import *


class Application():
    def __init__(self):
        self.window = Tk()
        self.window.wm_title("Book Store")

        self.database = Database("books.db")

        # Creating labels to the app.
        self.title_label = Label(self.window, text='Title')
        self.year_label = Label(self.window, text='Year')
        self.auth_label = Label(self.window, text='Author')
        self.isbn_label = Label(self.window, text='ISBN')

        # Creating inputs to the labels.
        self.title = StringVar()
        self.title_ent = Entry(self.window, textvariable=self.title)
        self.year = StringVar()
        self.year_ent = Entry(self.window, textvariable=self.year)
        self.author = StringVar()
        self.auth_ent = Entry(self.window, textvariable=self.author)
        self.isbn = StringVar()
        self.isbn_ent = Entry(self.window, textvariable=self.isbn)

        # Creating the listbox and its scrollbar.
        self.output = Listbox(self.window, height=8, width=35)

        self.scrollbar = Scrollbar(self.window)

        self.output.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.output.yview)

        self.output.bind("<<ListboxSelect>>", self.get_selected_row)

        # Creating buttons to the app.
        self.view_all_bt = Button(self.window, text='View All', width=12, command=self.view_command)
        self.search_bt = Button(self.window, text='Search Entry', width=12, command=self.search_command)
        self.add_bt = Button(self.window, text='Add Entry', width=12, command=self.add_command)
        self.updt_bt = Button(self.window, text='Update Selected', width=12, command=self.update_command)
        self.del_bt = Button(self.window, text='Delete Selected', width=12, command=self.delete_command)
        self.close_bt = Button(self.window, text='Close', width=12, command=self.window.destroy)


    def grid_all(self):
        # Placing every vidget to the app.
        self.title_label.grid(row=0, column=0)
        self.year_label.grid(row=1, column=0)
        self.auth_label.grid(row=0, column=2)
        self.isbn_label.grid(row=1, column=2)

        self.title_ent.grid(row=0, column=1)
        self.year_ent.grid(row=1, column=1)
        self.auth_ent.grid(row=0, column=3)
        self.isbn_ent.grid(row=1, column=3)

        self.scrollbar.grid(row=2, column=2, rowspan=6)

        self.output.grid(row=2, column=0, rowspan=6, columnspan=2)

        self.view_all_bt.grid(row=2, column=3)
        self.search_bt.grid(row=3, column=3)
        self.add_bt.grid(row=4, column=3)
        self.updt_bt.grid(row=5, column=3)
        self.del_bt.grid(row=6, column=3)
        self.close_bt.grid(row=7, column=3)


    def get_selected_row(self, event):
        '''Returns a selected row in the listbox of books.'''
        try:
            index = self.output.curselection()[0]
            self.selected_tuple = self.output.get(index)
            self.title_ent.delete(0, END)
            self.title_ent.insert(END, self.selected_tuple[1])
            self.year_ent.delete(0, END)
            self.year_ent.insert(END, self.selected_tuple[2])
            self.auth_ent.delete(0, END)
            self.auth_ent.insert(END, self.selected_tuple[3])
            self.isbn_ent.delete(0, END)
            self.isbn_ent.insert(END, self.selected_tuple[4])
        except IndexError:
            print("The listbox shouldn't be empty")


    def view_command(self):
        '''Shows every entry at the listbox.''' 
        self.output.delete(0, END)
        for row in self.database.view():
            self.output.insert(END, row)


    def search_command(self):
        '''Searching for an entry with given title, author, year or isbn.'''
        rows = self.database.search(self.title.get(), self.author.get(), self.year.get(), self.isbn.get())
        self.output.delete(0, END)
        for row in rows:
            self.output.insert(END, row)


    def add_command(self):
        '''Adds a new entry.''' 
        self.database.insert(self.title.get(), self.author.get(), self.year.get(), self.isbn.get())
        self.output.delete(0, END)
        self.output.insert(END, (self.title.get(), self.author.get(), self.year.get(), self.isbn.get()))


    def delete_command(self):
        ''' Deletes selected row in the listbox.'''
        try:
            self.database.delete(self.selected_tuple[0])
            self.view_command()
        except NameError:
            pass
        

    def update_command(self):
        ''' Changing the entry's attributes for new ones.'''
        try:
            self.database.update(self.selected_tuple[0], self.title.get(), self.author.get(),\
                self.year.get(), self.isbn.get())
            self.view_command()
        except NameError:
            pass

    
    def execute(self):
        '''Main method to run the app'''
        self.window.mainloop()


app = Application()
app.grid_all()
app.execute()