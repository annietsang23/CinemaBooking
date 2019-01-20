import sqlite3
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime,date

cln=[]
f_date=''
f_time=''
f_title=''
time_str=[]
db_cidx={}
db = pd.read_csv('screening.csv', parse_dates=True, na_values=['no info', '.'])
seats=[]
film_display=""
firstname=''
lastname=''
profile=''
film_list={}

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''CREATE TABLE film(
            title text,
            description text,
            screening_date text,
            screening_time text,
            booked_seats integer,
            available_seats integer,
            booked_seats_list text)
            ''')

c.execute('''CREATE TABLE booking(
            firstname text,
            lastname text,
            screening_date text,
            screening_time text,
            title text,
            seat text)
            ''')

def read_file():
    '''read screening file in csv'''
    global time_str
    global db_cidx
    global db

    #convert the string to datetime objects
    # db['Time']=pd.to_datetime(db['Time'],format='%I:%M%p')
    # time_str=[datetime.strftime(i,'%I:%M %p')for i in db['Time']] #string rep of time
    # db['Time']=[i.time()for i in db['Time']]
    db=db.set_index('Time')
    db_cidx={v:k for (k,v) in enumerate(list(db))} #dict rep of column names and index
    # db.columns=[datetime.fromisoformat(i) for i in list(db)]

    # fill NaN value with 'vacant'
    db=db.fillna(value='')

def insert_film(m,n,j,i):
    with conn:
        c.execute('''INSERT INTO film VALUES(
                    :title,:description,:screening_date,
                    :screening_time,:booked_seats,:available_seats,:booked_seats_list)''',
                  {'title': m, 'description':n, 'screening_date': i, 'screening_time':j,
                   'booked_seats':0,'available_seats':130,'booked_seats_list':''})

def update_seats(b, dt,t,o='add'):
    with conn:
        c.execute('''SELECT booked_seats,available_seats,booked_seats_list FROM film WHERE screening_date=:date AND screening_time=:time''',
                  {'date':dt,'time':t})
        x=c.fetchall()
        if o=='add':
            booked=x[0][0]+1
            avail=x[0][1]-1
            b_l=x[0][2]+','+b
        else:
            booked=x[0][0]-1
            avail = x[0][1]+1
            b_l=x[0][2].replace((','+b),'')

        c.execute('''UPDATE film SET booked_seats=:seat_total,available_seats=:empty,booked_seats_list=:seatno
                WHERE screening_date=:date AND screening_time=:time''',
                  {'seat_total': booked, 'empty':avail,'seatno': b_l, 'date': dt, 'time': t})


def fetch_film(**kwargs):
    with conn:
        c.execute(f'''SELECT title
                        FROM film WHERE screening_date=:date AND screening_time=:time
                        ''',kwargs)
    return c.fetchall()


class film_B(tk.Button):
    '''create button for each movie shown in the schedule'''
    all_film=[]
    def __init__(self,bottom_frame,d,tm,t):
        super().__init__(bottom_frame)
        self.date=d
        self.time=tm
        self.title=t
        self.configure(text=t, wraplength='160',justify='left',width='20',height='2',
                        fg='green', bd=1,highlightbackground='green',command=self.click_film)
    def click_film(self):
        global f_date
        global f_time
        global f_title

        f_date=self.date
        f_time=self.time
        f_title=self.title

        seatingplan()


def schedule_tk(f,l,p):
    '''Create the tkinter window. Display the movie schedule per date(s) selected by user.'''
    mn = ''
    global film_display
    global firstname
    global lastname
    global profile
    global db_cidx

    firstname=f
    lastname=l
    profile=p

    '''create the tkinter window'''
    film_display=tk.Tk()
    film_display.configure(background='black')
    film_display.geometry('1096x1000')
    film_display.title('Book your movie')
    top_frame=tk.Frame(film_display,height='6',bg='black')
    top_frame.grid(row=0,columnspan=len(cln)+1)
    tk.Label(top_frame,text=f'You are logged in as: {firstname} {lastname}',fg='yellow',bg='black',font=('arial',14,'italic')).grid(row=0,pady='5')


    tk.Label(top_frame,text='AT Cinema Screening Time',fg='green',bg='black',font=('arial',24,'bold')).grid(row=2,pady='10')
    lb1=tk.Label(top_frame, text='Select up to 3 date(s):',fg='yellow', bg='black', font=('arial', 16))
    lb1.grid(row=3)

    #generate a list box with the available dates
    date_frame=tk.Frame(film_display,bg='black')
    date_frame.grid(row=1)
    s = tk.Scrollbar(date_frame)
    lb_date=tk.Listbox(date_frame,selectmode='extended',height='5',yscrollcommand=s.set,width='15')
    s.config(command=lb_date.yview)
    db_cidx = {v: k for (k, v) in enumerate(list(db))}

    for i in db_cidx.keys():
        if date.fromisoformat(i) >= date.today():
            lb_date.insert('end',i)
    lb_date.grid(row=2,column=0,ipadx='1')
    s.grid(row=2,column=1,ipady='2')

    def select_date():
        '''return the list of dates selected in listbox'''
        global cln
        if len(lb_date.curselection()) > 3:
            messagebox.showinfo('', 'select max 3 date(s) only.')
            return
        cln = list(map(lambda x: lb_date.get(x), lb_date.curselection()))

        def screening_table():
            nonlocal bottom_frame
            '''create the tkinter window for list of films per date selected'''
            bottom_frame.destroy()
            bottom_frame = tk.Frame(film_display, bg='black')
            bottom_frame.grid(row=4,columnspan='5')
            # add the column header:selected date
            for k in range(len(cln)):
                tk.Label(bottom_frame, text=cln[k],fg='white',bg='black').grid(row=4, column=k + 1)

            for i in range(len(db)):
                # add the time
                tx = db.index[i]
                # add the film
                x = tk.Label(bottom_frame, text=tx,fg='white',bg='black')
                x.grid(row=i + 6, column=0, sticky='w')

                for j in range(len(cln)):
                    ty = db.iloc[i, db_cidx[cln[j]]]
                    if len(ty):
                        y = film_B(bottom_frame, cln[j], tx, ty)
                    else:
                        y = tk.Label(bottom_frame, bg='black', width='20', height='2')
                    y.grid(row=i + 6, column=1 + j, sticky='w')

        screening_table()


    b_date=tk.Button(date_frame,text='Confirm',command=select_date)
    b_date.grid(row=2,column=2,padx='10',ipadx='10')

    bottom_frame = tk.Frame(film_display, bg='black')
    film_display.mainloop()

    return mn

class Seat(tk.Button):
    '''a button for each seat in the seating plan'''
    all_seat=[]
    def __init__(self,m_frame,seatno):
        super().__init__(m_frame)
        self.name=seatno
        self.configure(text=seatno,width='2',command=self.choose)
        self.selected=False
        Seat.all_seat.append(self)

    def status_f(self,b):
        self.status=b
        if self.status:
            self.configure(text='X',fg='red',highlightbackground='red',state='disabled')
        else:
            self.configure(text=self.name[1:],fg='green',highlightbackground='green',state='normal')

    def choose(self):
        if self.selected:
            self.selected=False
            self.configure(fg='green', highlightbackground='green')
        else:
            self.selected=True
            self.configure(fg='red', highlightbackground='yellow')

def seatingplan():
    '''Construct the seating plans with indication of seat availability'''

    # Obtain the list of booked seats
    with conn:
        c.execute('''SELECT booked_seats_list,available_seats,description
                    FROM film 
                    WHERE screening_date=:date AND screening_time=:time''',
                  {'date': f_date, 'time': f_time})
        x= c.fetchall()[0]
        booked_s=x[0].lstrip(',')
        booked_s=booked_s.split(',')
        avail_s=x[1]
        des=x[2]

    sp = tk.Tk()
    sp.title('Book your movie')
    sp.configure(background='black')

    top_frame=tk.Frame(sp,height='6',bg='black')
    top_frame.grid(row=0)
    tk.Label(top_frame,
             text=f'Section: {f_date} {f_time}\n Movie: {f_title}\n Description: {des}',
             fg='yellow', bg='black', font=('arial', 14, 'italic'),wraplength='550').grid(row=0, pady='5')

    tk.Label(top_frame,text='SCREEN',height='1',width='30',fg='blue',bg='red',font=('arial',16,'bold')).grid(row=1,pady='10')

    def proceed():
        '''Generate messagebox to confirm seat selection'''
        global seats
        l = filter(lambda x: x.selected == True, Seat.all_seat)
        seats = [i.name for i in l]
        if len(seats):
            msg = messagebox.askyesno('Book', f'Confirm seat no: {",".join(seats)}')
            if msg:
                sp.destroy()
                film_display.destroy()
                for i in seats:
                    new_booking([firstname,lastname,f_date,f_time,f_title,i])
                    print('new booking is added to booking database. Seat availability updated in film database.')
                    # update booking text file
                    with open('booking_pre.txt', 'a') as f:
                        f.write(f'\n{firstname},{lastname},{f_date},{f_time},{f_title},{i}')
                    print('new booking is written to booking_pre.txt')
                messagebox.showinfo('Book',
                                    f'''Done! Here\'s your booking details:
                                    Date: {f_date}
                                    Time: {f_time}
                                    Movie: {f_title}
                                    Seat No.: {','.join(seats)}''')
                for x in Seat.all_seat:
                    if not x.status:
                        x.selected=False
                seats=[]
            else:
                for x in Seat.all_seat:
                    if not x.status:
                        x.selected=False
                seats=[]
        else:
            messagebox.showinfo('Book','No seat has been selected.')


    if profile=='customer':
        tk.Button(top_frame, text='Book', width='10',command=proceed).grid(row=2, pady='5')
    else:
        tk.Label(top_frame, text=f'No. of seats available:{avail_s} \t\t Booked seat:{booked_s}',fg='yellow',bg='black').grid(row=2, pady='5')

    #create the seating plan
    m_frame=tk.Frame(sp,bg='black')
    # m_frame.grid(row=2,ipadx='10')
    m_frame.grid(row=2)

    r_n = 1
    for i in range(ord('A'),ord('K')):
        c_n = 1
        tk.Label(m_frame,text=chr(i),width='2',fg='white',bg='black').grid(row=r_n,column=0,padx='5',pady='5')
        for j in range(1,15):
            if j==9:
                tk.Label(m_frame,fg='white',bg='black').grid(row=r_n,column=c_n,padx='10')
                c_n+=1
            #create seat instance from class Seat
            s=Seat(m_frame,chr(i)+str(j))

            #change seat status
            if s.name in booked_s:
                s.status_f(True)
            else:
                s.status_f(False)

            s.grid(row=r_n,column=c_n,padx='5',pady='5')
            c_n+=1
        tk.Label(m_frame, text=chr(i), width='2',fg='white',bg='black').grid(row=r_n, column=15, padx='5', pady='5')
        r_n+=1



    bottom_frame=tk.Frame(sp,bg='black')
    bottom_frame.grid(row=3,ipadx='10')

    sp.mainloop()

#manage booking
def new_booking(y):
    '''Insert new booking record into booking database'''
    v = {}
    v['firstname'] = y[0]
    v['lastname'] = y[1]
    v['screening_date'] = y[2]
    v['screening_time'] = y[3]
    v['title'] = y[4]
    v['seat'] = y[5]
    with conn:
        c.execute("INSERT INTO booking VALUES(:firstname,:lastname,:screening_date,:screening_time,:title,:seat)", v)

    #update film database
    update_seats(v['seat'],v['screening_date'],v['screening_time'],o='add')

def fetch_cus_booking(f,l):
    with conn:
        c.execute('''SELECT screening_date,screening_time,title,seat
         FROM booking WHERE firstname=:firstname AND lastname=:lastname'''
                  ,{'firstname':f,'lastname':l})
        x=c.fetchall()
    return x


def main():
    global film_list
    read_file()
    x = ''
    y = ''
    # create a dictionary of the movie title and description:
    with open('film_pre.txt', 'r') as f:
        for r in f.readlines():
            if r.startswith('Title:'):
                x = r[6:].rstrip()
            elif r.startswith('Description:'):
                y = r[12:].rstrip()
                film_list[x] = y
    for m in film_list.keys():
        for i in db.columns:
            for j in db.index:
                if db.loc[j, i] == m:
                    insert_film(m, film_list[m], j, i)
    print('film data loaded from file(film_pre.txt) into film database.')

    # preload booking data:
    with open('booking_pre.txt', 'r') as f:
        for x in f.readlines():
            y = x.rstrip().split(',')
            if len(y)==6:
                new_booking(y)

        print('booking data loaded from file (booking_pre.txt) into booking database.')

main()
if __name__=='__main__':
    pass
    # fetch_film(**{'title':'Excel Me'})
    # x=schedule_tk('A','T')



#quick statistic summary of count,unique,top,frequency
# db_stats=db.describe()
# print(db_stats)
# # print(db_stats.sort_index(axis=1,ascending=False)) #sort by index, e.g. date
# print(db_stats.T.sort_values(by='freq')) #sort by values in column freq
# print(db.loc['8:40am':'12:10pm',['2019-01-04','2019-01-05']]) #return the slice with index from 8:40am to 12:10pm and columns (with the dates)
# print(db.loc['8:40am','2019-01-05'])
# print(db.iloc[0,20]) #use index and column no.
# print(db.isin(['A Christmas Carol'])) #filter. Return a table of 'true' or 'false' value
# print(db[db.isin(['A Christmas Carol'])]) #filtered: value is either 'a xmas carol' or NaN




