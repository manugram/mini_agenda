import os, sys
import subprocess as sp
import sqlite3 as sq


VERSION = 0.3


def parse_file_name() -> str:

    ext = '.sq3'
    n = input('File name: ')
    fname = None

    if ' ' in n:
        fname = n.replace(' ', '_') + ext
        return fname

    fname = n + ext

    return fname


def dbfile_exists(n: str) -> bool:

    # ext = '.sq3'
    return os.path.exists(n)


def create_db(name: str) -> str:

    # fname = parse_file_name(name)
    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()
    c.execute(
        f'''
            CREATE TABLE {tname.upper()} 
                (
                 "ID" INTEGER NOT NULL UNIQUE,                 
                 "FIRST_NAME" TEXT,
                 "LAST_NAME" TEXT,
                 "PHONE_NUMBER" TEXT,
                 "EMAIL" TEXT,
                 "NOTE" TEXT,
                 PRIMARY KEY("ID" AUTOINCREMENT)
                )
        '''
    )
    db.commit()
    c.close()
    db.close()

    if os.path.exists(name):
        print(f'DataBase created as {name}')
        return name
    else:
        print(f'Fail to creat db: {name}')
        return None


def add_contact(name: str) -> None:

    # fname = parse_file_name(name)
    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()

    fnam = input('First Name: ')
    lnam = input('Last Name: ')
    pnum = input('Phone Number: ')
    emai = input('eMail: ')
    note = input('Note: ')

    c.execute(
        f'''
            INSERT INTO {tname.upper()} (FIRST_NAME, LAST_NAME, PHONE_NUMBER, EMAIL, NOTE)
            VALUES ("{fnam}","{lnam}","{pnum}","{emai}","{note}")
        '''  # ,
        # (fnam, lnam, pnum, emai, note),
    )

    db.commit()
    c.close()
    db.close()

    return


def search_contact(name: str, tag: str, pattern: str) -> list:

    # dbname = parse_file_name()
    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()

    c.execute(
        f'''
            SELECT * FROM {tname.upper()} WHERE {tag} = ?                    
        ''',
        (pattern,),
    )

    a = c.fetchall()

    c.close()
    db.close()

    return a


def remove_contact(name: str) -> bool:
    pass


def print_contact(name: str, row: str, print_all=False) -> None:

    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()

    if row == '' and print_all == True:
        t = c.execute(
            f'''
            SELECT * FROM {tname.upper()} ORDER BY ID
            '''
        ).fetchall()
    # else:
    #     t = search_contact()

    for x in t:
        print(x)

    return


def menu() -> str:

    opt = None
    print(
        f'''
        Welcome to MiniAgenda v{VERSION}, a Python3 script.
        What do you want to do?

        Options are:

        1.- Create New Agenda.
        2.- Add Contact into Existing Agenda.
        3.- Search a Contact.
        4.- Delete Contact.
        5.- Print Full Agenda Content.
        Q.- Exit.

        '''
    )
    opt = input('Your option: ')
    return opt


def search_menu(db: str) -> str:

    print(
        '''
        Wants search by:

        1.- First Name.
        2.- Last Name.
        3.- Phone Number.
        4.- eMail.
        R.- Return to main menu.       
        '''
    )
    opt = input('-> ')
    if opt in ('1', '2', '3', '4'):
        pattern = input('Search string: ')

        if opt == '1':
            a = search_contact(db, 'FIRST_NAME', pattern)
            print(a)
            return
        elif opt == '2':
            a = search_contact(db, 'LAST_NAME', pattern)
            print(a)
            return
        elif opt == '3':
            a = search_contact(db, 'PHONE_NUMBER', pattern)
            print(a)
            return
        elif opt == '4':
            a = search_contact(db, 'EMAIL', pattern)
            print(a)
            return

    elif opt.upper() == 'R':
        return
    else:
        print('Invalid option!!')
        search_menu()

    return


def call_function(opt: str) -> None:

    if opt == '1':
        # Calling create_db() function...

        n = parse_file_name()
        if dbfile_exists(n):
            print('DataBase already exists!!')
            # return
        else:
            create_db(n)
        # print(n, m)

    elif opt == '2':
        # Calling add_contact() function...

        n = parse_file_name()
        if dbfile_exists(n):
            add_contact(n)
            print('Contact added!!')
        else:
            print('DataBase does not exist...')
            return

    elif opt == '3':
        # Calling search_contact() function...

        fname = parse_file_name()
        if not dbfile_exists(fname):
            print(
                f'Data Base {fname} does not exist, first most be created.\nTry again!!'
            )
            return
        else:
            search_menu(fname)
            return

    elif opt == '4':
        # Calling remove_contact() function...
        return

    elif opt == '5':
        # Calling print_contact() function...

        n = parse_file_name()
        if dbfile_exists(n):
            print_contact(n, row='', print_all=True)
            return
        else:
            print('DataBase file does not exist...')
            return

    else:
        print('Invalid parameter...')
        # return

    return


def main():

    while True:

        if os.uname()[0].lower() == 'linux':
            sp.run('clear')
        elif os.uname()[0].lower() == 'nt':
            sp.run('cls')

        opt = menu()
        if opt.upper() == 'Q':
            print('Bye, bye!!')
            exit(0)
        elif opt in ('1', '2', '3', '4', '5'):
            print(f'Your option was: {opt}')
            call_function(opt)
            # exit(1)
            input()
            continue
        else:
            print('Invalid option!!\nPress any key to continue...')
            input()
            continue


if __name__ == '__main__':
    main()
