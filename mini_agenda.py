import os, sys
import sqlite3 as sq


VERSION = 0.1


def create_db(fname: str) -> str:
    ext = '.sq3'
    db = sq.connect(fname + ext)
    c = db.cursor()
    c.execute(
        f'''
            CREATE TABLE {fname.upper()} 
                (
                 CON_ID INTEGER NOT NULL UNIQUE,
                 FIRST_NAME TEXT,
                 LAST_NAME TEXT,
                 PHONE_NUMBER TEXT,
                 EMAIL TEXT,
                 NOTE TEXT
                )
        '''
    )
    db.commit()
    db.close()

    dbname = fname + ext
    if os.path.exists(dbname):
        print(f'DataBase created as {dbname}')
        return dbname
    else:
        print(f'Fail to creat db: {dbname}')
        return None


def add_contact(**kwarg) -> str:
    pass


def search_contact(name: str) -> str:
    pass


def remove_contact(name: str) -> bool:
    pass


def print_contact(name: str, print_all=False) -> None:
    pass


def menu() -> str:
    opt = None
    print(
        f'''
        Welcome to MiniAgenda v{VERSION}, a Python3 script.
        What do you want to do?

        Options are:

        1.- Create New Agenda.
        2.- Add Contact into Existing Agenda.
        3.- Search Contact.
        4.- Delete Contact.
        5.- Print Full Agenda Content.
        Q.- Exit.

        '''
    )
    opt = input('Your option: ')
    return opt


def call_function(opt: str) -> None:
    if opt == '1':
        print('Calling create_db() function...')
        fname = input('File name: ')
        n = create_db(fname)
        print(n)
    elif opt == '2':
        print('Calling add_contact() function...')
    elif opt == '3':
        print('Calling search_contact() function...')
    elif opt == '4':
        print('Calling remove_contact() function...')
    elif opt == '5':
        print('Calling print_contact() function...')
    else:
        print('Invalid parameter...')
        exit(5)


def main():
    opt = menu()
    if opt.upper() == 'Q':
        print('Bye, bye!!')
        exit(0)
    elif opt in ('1', '2', '3', '4', '5'):
        print(f'Your option was: {opt}')
        call_function(opt)
        exit(1)
    else:
        print('Invalid option!!')
        exit(2)


if __name__ == '__main__':
    main()
