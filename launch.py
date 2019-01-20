from login import *
from menu import *
from exceptions import *
from film_database import *
#launch module for the cinema booking system.

def launch_system():
    try:
        #launch the login page for customer and employee
        kys=login()
        if len(kys[0]):
            profile, fname, lname=kys

            def run_menu():
                #open the menu window and return the selected option
                ms = menu(profile,fname,lname)
                if ms.menu_option=='manage_profile':
                    for i in Customer.cus_list:
                        if i.firstname==ms.firstname and i.lastname==ms.lastname:
                            profile_info(*(i,'existing'))
                            run_menu()

                elif ms.menu_option=='logout':
                    launch_system()
                    quit()
            run_menu()
        else:
            raise InputError('No input supplied.')

    except KeyboardInterrupt:
        print('Program halted by user.')

launch_system()





