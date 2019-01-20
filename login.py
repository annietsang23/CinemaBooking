import tkinter as tk
from cust_profile import *
from emp_profile import *
from tkinter import messagebox
from exceptions import *

profile=''
profile=''
firstname=''
lastname=''


def login():
    '''Display the login page for both employees and customers'''
    login_display=tk.Tk()
    login_display.configure(background='black')
    login_display.geometry('1096x1000')
    # #rename title of the window
    login_display.title("Log in to AT cinema management system")


    top_frame = tk.Frame(login_display,bg='black',bd='0')
    top_frame.pack(side='top')

    bottom_frame = tk.Frame(login_display,bg='black',bd='0')
    bottom_frame.pack(side='top')
    #insert the cinema image
    icon = tk.PhotoImage(file="cinema.gif")
    label1=tk.Label(top_frame,image=icon,bg='black',bd='0')
    label1.pack(side='top')

    tk.Label(top_frame,text=
    '\nWelcome to AT Cinema!',fg='purple',bg='black',font=('arial','24')).pack()

    tk.Label(top_frame,text=
    '\nWe bring you truly exclusive movie experience that you never dream of.',fg='purple',bg='black',font=('arial','18','italic')).pack()


    tk.Label(top_frame,text=
    '''
    Please log in to AT cinema booking system using your username and password.
    Click 'I'm New' below if you are new to us.''',fg='green',bg='black',font=('arial','14')).pack()

    tk.Label(bottom_frame,text='Username:',fg='white',bg='black').pack(side='top')
    entry1=tk.Entry(bottom_frame,fg='white',bg='black',bd='0')
    entry1.pack(side='top')

    tk.Label(bottom_frame,text='Password:',fg='white',bg='black').pack(side='top')
    entry2=tk.Entry(bottom_frame,show='*',fg='white',bg='black',bd='0')
    entry2.pack(side='top')

    def match_password():
        global profile
        global firstname
        global lastname
        username=entry1.get()
        password=entry2.get()

        try:
            #check if username and password exists in customer database
            x=get_cus(**{'username':username,'password':password})
            if x:
                messagebox.showinfo('Welcome',f'Welcome back our Customer, {x[0][0]} {x[0][1]}')
                print('Welcome back,',x[0][0],x[0][1])
                profile,firstname,lastname='customer',x[0][0],x[0][1]
                login_display.destroy()

            else:
                # check if username and password exists in employee database
                y=get_emp(username,password)
                if y:
                    messagebox.showinfo('Welcome', f'Welcome back our Staff, {y[0][0]} {y[0][1]}')
                    print('Welcome back,', y[0][0], y[0][1])
                    profile, firstname, lastname = 'employee', y[0][0], y[0][1]
                    login_display.destroy()

                else:
                    raise PasswordError

        except PasswordError:
            messagebox.showerror('Welcome','Username / Password doesn\'t match. Please try again.')

    button1 = tk.Button(bottom_frame, text='Submit', command=match_password,bd='0',width='20')
    button1.pack(pady='10', side='top')

    button2 = tk.Button(bottom_frame, text='I\'m New', command=profile_info,bd='0',width='20')
    button2.pack(pady='5', side='top')

    login_display.mainloop()

    print(profile,firstname,lastname)

    return profile,firstname,lastname


def profile_info(*args):
    '''Display the window for customer to enter and edit profile information'''

    create_new = tk.Tk()
    create_new.configure(background='black')
    create_new.geometry('1096x720')

    # rename title of the window
    create_new.title("Manage your information")
    # create 2 frames TOP and BOTTOM
    top_frame = tk.Frame(create_new,bg='black',bd='0')
    top_frame.pack()

    bottom_frame = tk.Frame(create_new,bg='black',bd='0')
    bottom_frame.pack()

    if len(args):
        cus=args[0]
        tip1=tk.Label(top_frame, text='Edit your profile: ', fg='white', bg='black',font=('arial',16,))
        tip1.pack()

    else:
        tk.Label(top_frame, text=
        '''Welcome to AT cinema! To begin your journey with us,
        here are a few things we ask from you:''',fg='yellow',bg='black',font=('arial',16,)).pack(pady='10')

    tk.Label(bottom_frame, text='First Name*:',fg='white',bg='black').pack()
    entry1 = tk.Entry(bottom_frame)
    entry1.pack(pady='10')

    tk.Label(bottom_frame, text='Last Name*:',fg='white',bg='black').pack()
    entry2 = tk.Entry(bottom_frame)
    entry2.pack(pady='10')

    tk.Label(bottom_frame, text='Email Address*:',fg='white',bg='black').pack()
    entry3 = tk.Entry(bottom_frame)
    entry3.pack(pady='10')

    tk.Label(bottom_frame, text='UK Phone Number*:',fg='white',bg='black').pack()
    entry4 = tk.Entry(bottom_frame)
    entry4.pack(pady='10')

    tk.Label(bottom_frame, text='Username*: \n (6-8 characters)',fg='white',bg='black').pack()
    entry5 = tk.Entry(bottom_frame)
    entry5.pack(pady='10')

    tk.Label(bottom_frame, text="Password*: \n (6-8 characters with at least one special character @%+\/!#$^?:,._)",fg="white",bg="black").pack()
    entry6 = tk.Entry(bottom_frame)
    entry6.pack(pady='10')
    tk.Label(bottom_frame, text='*Mandatory Field',fg='white',bg='black',font='8').pack()

    if 'existing' in args:
        entry1.insert('end',cus.firstname)
        entry2.insert('end', cus.lastname)
        entry3.insert('end', cus.email)
        entry4.insert('end', cus.phone)
        entry5.insert('end', cus.username)
        entry6.insert('end', cus.password)

        entry1.configure(state='disabled')
        entry2.configure(state='disabled')

    def entry_clear():
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry4.delete(0, 'end')
        entry5.delete(0, 'end')
        entry6.delete(0, 'end')

    def valid_entry():
        '''validate the information entered by customer.'''
        global new_cust_details
        text = ''
        e_firstname = entry1.get()
        e_lastname = entry2.get()
        email=entry3.get()
        phone=entry4.get()
        username=entry5.get()
        password=entry6.get()
        try:

            if all([e_firstname,e_lastname,email,phone,username,password]) is False:
                text=text+ 'all mandatory fields must be filled!'
                raise InputError

            #firstname and lastname
            if not 'existing' in args:
                if any(list(map(lambda x: x in '@%+\/!#$^?:,._[]{}()~"',e_firstname))):
                    text = text + 'Invalid firstname\n'
                    raise InputError

                elif any(list(map(lambda x: x in '@%+\/!#$^?:,._[]{}()~"',e_lastname))):
                    text = text + 'Invalid lastname\n'
                    raise InputError

                elif get_cus(**{'first':e_firstname,'last':e_lastname}):
                    text = text + 'Invalid: Name already exist\n'
                    raise InputError

            #email
            if '@' not in email:
                text=text+'Invalid email\n'
                raise InputError

            #phone no
            if phone.isdigit() is False or len(phone) not in (9,10):
                text=text+'Invalid phone no.\n'
                raise InputError

            #username and password
            if 'existing' in args:
                if username != cus.username:
                    if len(username) not in (6, 7, 8):
                        text = text + 'Invalid username\n'
                        raise InputError
                    elif get_cus(**{'username':username}):
                        text = text + 'Invalid: username already exist\n'
                        raise InputError
            else:
                if len(username) not in (6, 7, 8):
                    text = text + 'Invalid username\n'
                    raise InputError
                elif get_cus(**{'username': username}):
                    text = text + 'Invalid: username already exist\n'
                    raise InputError

            if len(password) not in (6,7,8) or not any(list(map(lambda x: x in '@%+\/!#$^?:,._',password))):
                text=text+'Invalid password'
                raise InputError

        #messagebox
        except InputError:
            messagebox.showerror('Error',text)

        else:
            try:
                if len(args):
                    cus.update_cus(email,phone,username,password)
                    #update cust_pre text file
                    with open('cust_pre.txt','w') as f:
                        for c in Customer.cus_list:
                            f.write(f'{c.firstname},{c.lastname},{c.email},{c.phone},{c.username},{c.password}\n')
                    messagebox.showinfo('Manage profile','Successfully updated.')
                else:
                    Customer(e_firstname,e_lastname,email,phone,username,password)
                    # update cust_pre text file
                    with open('cust_pre.txt', 'a') as f:
                        f.write(f'{e_firstname},{e_lastname},{email},{phone},{username},{password}\n')
                        messagebox.showinfo('Welcome', 'Successful! Now log in with your new username and password.')
                profile,firstname,lastname='Customer',e_firstname,e_lastname
                create_new.destroy()
            except:
                print('cannot create new customer')

    button1 = tk.Button(bottom_frame, text='Submit', command=valid_entry)
    button1.pack(pady='10')

    if not len(args):
        button2 = tk.Button(bottom_frame, text='Clear all', command=entry_clear)
        button2.pack(pady='10')

    create_new.mainloop()

    return profile, firstname, lastname

if __name__=='__main__':
    x=login()
