import sqlite3
from datetime import datetime

#create tables for employee data
conn=sqlite3.connect(':memory:')
c=conn.cursor()
c.execute('''CREATE TABLE employees(
            firstname text,
            lastname text,
            username text,
            password text)''')

class Employee:
    '''manage employee profile'''
    emp_list=[]
    def __init__(self,firstname,lastname,username,password):
        self.firstname=firstname
        self.lastname=lastname
        self.username=username
        self.password=password
        self.insert_emp()
        Employee.emp_list.append(self)

    def insert_emp(self):
        with conn:
            c.execute("INSERT INTO employees VALUES(:firstname,:lastname,:username,:password)",
                      {'firstname':self.firstname,'lastname':self.lastname,
                       'username':self.username,'password':self.password})

        print(f'{self.firstname} {self.lastname} added into employees database.')


def main():
    #pre-load employee data from text file
    with open('employee_pre.txt','r') as f:
        for l in f.readlines():
            x=l.rstrip('\n').split(',')
            if len(x)==4:
                Employee(x[0],x[1],x[2],x[3])
            else:
                print('Missing values')
    print('employee data loaded from file: employee_pre.txt')

def get_emp(username,password):
    c.execute("SELECT * FROM employees where username=:username AND password=:password",{'username':username,'password':password})

    x=c.fetchall()
    if len(x):
        return x

main()
if __name__=='__main__':
    main()
