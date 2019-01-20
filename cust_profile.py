import sqlite3from datetime import datetime#create tables for customer and booking dataconn=sqlite3.connect(':memory:')c=conn.cursor()c.execute('''CREATE TABLE customers(            firstname text,            lastname text,            email text,            phone text,            username text,            password text)''')c.execute('''CREATE TABLE booking(            firstname text            lastname text,            date text,            time text,            title text,            seat integer)            ''')class Customer:    #manage customer profile    cus_list=[]    def __init__(self,firstname,lastname,email,phone,username,password):        self.firstname=firstname        self.lastname=lastname        self.email=email        self.phone=phone        self.username=username        self.password=password        self.insert_cus()        Customer.cus_list.append(self)    def insert_cus(self):        with conn:            c.execute("INSERT INTO customers VALUES(:firstname,:lastname,:email,:phone,:username,:password)",                      {'firstname':self.firstname,'lastname':self.lastname,'email':self.email,'phone':self.phone,                       'username':self.username,'password':self.password})        print(f'{self.firstname} {self.lastname} added into database.')    def update_cus(self,email,phone,username,password):        self.email=email        self.phone=phone        self.username=username        self.password=password        with conn:            c.execute("""UPDATE customers SET email=:email, phone=:phone, username=:username, password=:password                    WHERE firstname=:first AND lastname=:last""",                  {'first':self.firstname,'last':self.lastname,'email':email,'phone':phone,'username':username,'password':password})    def fetch_booking(self):        c.execute("SELECT * FROM booking where firstname=:first AND lastname=:last",                  {'first': self.firstname, 'last': self.lastname})        print(c.fetchall())def get_cus(**kwargs):    if 'first' in kwargs:        c.execute("SELECT * FROM customers where firstname=:first AND lastname=:last",kwargs)    elif 'password' in kwargs:        c.execute("SELECT * FROM customers where username=:username AND password=:password",kwargs)    elif 'username' in kwargs:        c.execute("SELECT * FROM customers where username=:username",kwargs)    x=c.fetchall()    if len(x):        return xdef main():    #pre-load customer and booking data from text files    with open('cust_pre.txt','r') as f:        for l in f.readlines():            x=l.rstrip('\n').split(',')            if len(x)==6:                Customer(x[0],x[1],x[2],x[3],x[4],x[5])            else:                raise ValueError('missing customer values')        # lines=[l.rstrip('\n') for l in f.readlines()]        print('customer data loaded from file: cust_pre.txt')    # with open('booking_pre.txt', 'r') as f:    #     for x in f.readlines():    #         y = x.rstrip().split(',')    #         new_booking(y)    #     print('booking data loaded from file: booking_pre.txt')main()if __name__=='__main__':    main()