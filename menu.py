import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from film_database import *
from exceptions import *

class menu(tk.Tk):

    def __init__(self,*args,**kwargs):

        super().__init__()
        self.title('AT Cinema')
        self.menu_option=''
        self.configure(bg='black')
        self.geometry('1096x720')
        self.top_frame=tk.Frame(self,bg='black')
        self.top_frame.pack(side='top')
        # insert the cinema image
        icon = tk.PhotoImage(file="cinema.gif")
        label1 = tk.Label(self.top_frame, image=icon, bg='black', bd='0')
        label1.pack(side='top')

        self.profile=args[0]
        self.firstname=args[1]
        self.lastname=args[2]

        self.bottom_frame=tk.Frame(self,bg='black')
        self.bottom_frame.pack(side='top',pady='5')

        if self.profile=='customer':
            self.label1 = tk.Label(self.top_frame, text=f'Welcome: {self.firstname} {self.lastname}', fg='yellow', bg='black',
                                   font=('arial', 18, 'bold'))
            self.label1.pack(pady='5')
            self.bottom_frame_cust()
        elif self.profile=='employee':
            self.label1 = tk.Label(self.top_frame, text=f'Welcome: {self.firstname} {self.lastname} (Staff)', fg='yellow', bg='black',
                                   font=('arial', 18, 'bold'))
            self.label1.pack(pady='5')
            self.bottom_frame_emp()


        self.logout_bt = tk.Button(self.bottom_frame, text='Logout', width='20',command=self.log_out)
        self.logout_bt.pack(pady='5')

        self.mainloop()

    def bottom_frame_cust(self):
        self.hist_bt=tk.Button(self.bottom_frame,text='See my bookings',width='20',command=self.checkrecord)
        self.hist_bt.pack(pady='5')

        self.book_bt=tk.Button(self.bottom_frame,text='See what\'s on',width='20',command=self.ticketing)
        self.book_bt.pack(pady='5')

        self.profile_bt = tk.Button(self.bottom_frame, text='Manage my profile', width='20', command=self.p_mgt)
        self.profile_bt.pack(pady='5')

    def p_mgt(self):
        self.menu_option="manage_profile"
        self.destroy()

    def checkrecord(self):
        ln = fetch_cus_booking(self.firstname, self.lastname)
        rd = record(self.firstname, self.lastname, **{'history': ln})

    def addfilm(self):
        rd=record(self.firstname,self.lastname)

    def log_out(self):
        self.menu_option='logout'
        self.destroy()

    def ticketing(self):
        self.menu_option='ticket'
        schedule_tk(self.firstname, self.lastname,self.profile)

    def bottom_frame_emp(self):
        self.book_bt=tk.Button(self.bottom_frame,text='See what\'s on',width='20',command=self.ticketing)
        self.book_bt.pack(pady='5')

        self.hist_bt = tk.Button(self.bottom_frame, text='add new film', width='20',command=self.addfilm)
        self.hist_bt.pack(pady='5')

        self.book_bt=tk.Button(self.bottom_frame,text='export all movies details',width='20',command=export)
        self.book_bt.pack(pady='5')

def export():
    '''Export the whole film database to film_data.txt'''
    with conn:
        c.execute('SELECT title,screening_date,screening_time, booked_seats, available_seats, booked_seats_list FROM film')
        x=c.fetchall()
        with open('film_data.txt','w') as f:
            f.write(', '.join(d[0] for d in c.description)+'\n')
            for r in x:
                f.write(', '.join([str(i) for i in r]))
                f.write('\n')
            # csv_out=csv.writer(out_csv_file)
            # #write the header
            # csv_out.writerow(d[0] for d in c.description)
            # #write data
            # for result in c:
            #     csv_out.writerow(result)
    messagebox.showinfo('Export','Exported to film_data.txt')
    print('exported to film_data.txt')

class booking_bt(tk.Button):
    '''create button for booking cancellation'''
    def __init__(self,frame,rd,**kwargs):
        super().__init__(frame)
        self.configure(text='Delete',width='10',command=self.booking_cancel)
        self.date=kwargs['date']
        self.time=kwargs['time']
        self.title=kwargs['title']
        self.seatno=kwargs['seatno']
        self.w=rd

    def booking_cancel(self):
        msg=messagebox.askyesno('Cancel this booking','Confirm cancellation?')
        if msg:
            self.w.destroy()
            with conn:
                c.execute("""DELETE from booking
                            WHERE screening_date=:date AND
                            screening_time=:time AND
                            seat=:seatno""",
                          {'date':self.date,'time':self.time,'seatno':self.seatno})
            update_seats(self.seatno,self.date,self.time,o='remove')
            #update booking_pre text file
            with conn:
                c.execute('SELECT * FROM booking')
                x = c.fetchall()
            with open('booking_pre.txt', 'w') as f:
                for r in x:
                    f.write(','.join([str(i) for i in r]))
                    f.write('\n')
            print('updated booking_pre.txt')
            messagebox.showinfo('Cancel this booking', 'Done')


class record(tk.Tk):

    def __init__(self,*args,**kwargs):

        super().__init__()
        self.title('AT Cinema')
        self.configure(bg='black')

        self.top_frame=tk.Frame(self,bg='black')
        self.top_frame.grid(row=0)

        self.bottom_frame=tk.Frame(self,bg='black')
        self.bottom_frame.grid(row=1)

        tk.Label(self.top_frame,text=f'You are logged in as {args[0]} {args[1]}',fg='yellow',bg='black').grid(row=0,pady='5')

        if 'history' in kwargs:
            self.history(kwargs['history'])
        else:
            self.add_film()

        self.mainloop()


    def history(self,ln):

        tk.Label(self.top_frame, text=f'Your booking(s):', fg='white', bg='black',font=('arial',20,)).grid(row=1,pady='5')
        m=0
        for i in ('Date','Time','Movie','Seat No.'):
            tk.Label(self.bottom_frame, text=i, fg='white',bg='green',width='20').grid(row=0,column=m)
            m+=1

        #add the booking record
        if len(ln):
            r_n = 1
            for j in ln:
                m=0
                for n in j:
                    #check if this is a future booking
                    tk.Label(self.bottom_frame, text=n, fg='white', bg='black').grid(row=r_n, column=m)
                    m+=1
                if date.fromisoformat(j[0])>date.today():
                    keys={'date':j[0],'time':j[1],'title':j[2],'seatno':j[3]}
                    bt=booking_bt(self.bottom_frame,self,**keys)
                    bt.grid(row=r_n,column=m)
                r_n+=1
        else:
            tk.Label(self.bottom_frame, text='No record found', fg='white', bg='black').grid(row=1)

    def add_film(self):
        tk.Label(self.top_frame, text='Add film:', fg='white', bg='black', font=('arial', 20,)).grid(row=1)
        tk.Label(self.top_frame, text='Add film:', fg='white', bg='black', font=('arial', 20,)).grid(row=1)

        # generate a listbox of existing movies
        film_frame = tk.Frame(self, bg='black')
        film_frame.grid(row=1)
        tk.Label(film_frame, text='Choose Existing Movie:', fg='white', bg='black').grid(row=0, pady='5')
        s = tk.Scrollbar(film_frame)
        lb_film = tk.Listbox(film_frame, selectmode='single',height='10', yscrollcommand=s.set, width='40')
        s.config(command=lb_film.yview)

        for i in film_list.keys():
            lb_film.insert('1', i)
        lb_film.grid(row=2, column=0, ipadx='1')
        s.grid(row=2, column=1, ipady='45')

        self.bottom_frame.grid(row=2,column=0,padx='10')

        tk.Label(self.bottom_frame, text='Or: \n\nNew Movie Title:', fg='white', bg='black').grid(row=0, column=2, pady='5')
        entry1 = tk.Entry(self.bottom_frame, width='40')
        entry1.grid(row=1, column=2)

        tk.Label(self.bottom_frame, text='New Movie Description:', fg='white', bg='black').grid(row=3, column=2,pady='5')
        entry2 = tk.Entry(self.bottom_frame, width='40')
        entry2.grid(row=4, column=2,ipady='10')

        date_frame=tk.Frame(self,bg='black')
        date_frame.grid(row=3)
        tk.Label(date_frame, text='Date:', fg='white', bg='black').grid(row=5,column=0, pady='5')
        entry3=tk.Entry(date_frame,width='40')
        entry3.insert('end','e.g.2019-01-01')
        entry3.grid(row=6,column=0,pady='5')

        #generate a dropdown list of time
        time_frame = tk.Frame(self)
        time_frame.grid(row=4)

        opts = [' ']+ list(db.index)
        oMenuWidth = '38'

        v = tk.StringVar(self)
        v.set(opts[0])
        oMenu = tk.OptionMenu(time_frame, v, *opts)
        oMenu.config(width=oMenuWidth)
        oMenu.grid()

        def ValidEntry():
            global film_list
            msg=''
            new_movie=entry1.get().rstrip()
            try:
                d=date.fromisoformat(str(entry3.get()))
                if d<date.today():
                    msg=msg+'Date must be a future date.\n'
                    raise DateError
                d=entry3.get()

                t = v.get()
                if not len(t)>2:
                    msg = msg + 'No time is selected.\n'
                    raise InputError

                x=fetch_film(**{'date':d,'time':t})
                if len(x):
                    msg = msg + f'Time clashes with {x[0][0]}\n'
                    raise InputError

                if len(new_movie):
                    ntitle = new_movie
                    new_des = entry2.get().rstrip()
                    if not len(new_des):
                        msg = msg + 'Description should be filled in.\n'
                        raise InputError
                    film_list[ntitle]=new_des
                    #update film text file
                    with open('film_pre.txt','a') as f:
                        f.write(f'\nTitle:{ntitle}\nDescription:{new_des}\n')
                    print('new movie has been written to film_pre.txt')

                else:
                    if not len(lb_film.curselection()):
                        msg = msg + 'No movie is selected\n'
                        raise InputError
                    ntitle = str(list(map(lambda x: lb_film.get(x), lb_film.curselection()))[0])
                    with conn:
                        c.execute('SELECT description FROM film WHERE title=:title',{'title':ntitle})
                        new_des=c.fetchone()[0]

                if d not in list(db):
                    print('new date:',d)
                    #add new column to dataframe
                    cln = [date.fromisoformat(i) for i in list(db)]
                    i = list(filter(lambda x: x > date.fromisoformat(d), cln))
                    if len(i):
                        db.insert(cln.index(i[0]), d,'')

                # #add film to database
                insert_film(ntitle, new_des, t, d)

                #add film to the schedule
                db.at[t, d] = ntitle
                db.to_csv('screening.csv')
                messagebox.showinfo('Add new movie',f'Done! Movie: {ntitle} added to Date: {d} Time: {t}')
                print(f'Movie: {ntitle} added to Date: {d} Time: {t} in screening.csv')
                self.destroy()

            except DateError:
                messagebox.showerror('Error',msg)
            except InputError:
                messagebox.showerror('Error', msg)
            except ValueError:
                messagebox.showerror('Error','wrong input for date')


        b_frame=tk.Frame(self,bg='black')
        b_frame.grid(row=5)
        button1 = tk.Button(b_frame, text='Submit',command=ValidEntry)
        button1.grid(pady='10')




if __name__=='__main__':
    keys = ['employee','Chris', 'Evan']
    x=menu(*keys)













