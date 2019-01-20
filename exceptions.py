#A list of custom exceptions
from tkinter import messagebox
class DateError(Exception):
    '''raised when inputted date is in the past.
    messagebox.showerror('Error','Cannot create past event.')'''

class PasswordError(Exception):
    '''raised when username and password does not match.
    messagebox.showerror('Error','Username and Password does not match.')'''

class InputError(Exception):
    '''raised when inputs does not meet requirements.
    messagebox.showerror('Error',text)'''