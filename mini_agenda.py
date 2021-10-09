import os, sys
import subprocess as sp
import sqlite3 as sq


VERSION = 0.2


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
            INSERT INTO {tname.upper()} VALUES (?,?,?,?,?,?)
        ''',
        (1, fnam, lnam, pnum, emai, note),
    )

    db.commit()
    c.close()
    db.close()

    return


def search_contact(name: str, tag: str) -> str:

    # dbname = parse_file_name()
    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()
    c.execute(
        f'''
            SELECT * FROM {tname.upper()} 
                WHERE {tag}                    
        '''
    )
    a = c.fetchall()
    print(a)

    c.close()
    db.close()

    return


def remove_contact(name: str) -> bool:
    pass


def print_contact(name: str, tag: str, print_all=False) -> None:

    tname = name.split('.')[0]

    db = sq.connect(name)
    c = db.cursor()

    if print_all == True:
        c.execute(
            f'''
                SELECT * FROM {tname.upper()} ORDER BY FIRST_NAME
            '''
        )
    else:
        c.execute(
            f'''
                SELECT {tag.upper}
            '''
        )


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


def search_menu() -> str:

    print(
        '''
        Wants search by:

        1.- First Name.
        2.- Last Name.
        3.- Phone Number.
        4.- eMail.
        0.- Return to main menu.       
        '''
    )
    opt = input('-> ')
    if opt in ('1', '2', '3', '4'):
        param = input('Search string: ')
        return param
    elif opt == '0':
        return opt
    else:
        print('Invalid option!!')
        search_menu()

    return


def call_function(opt: str) -> None:

    if opt == '1':
        print('Calling create_db() function...')
        n = parse_file_name()
        m = create_db(n)
        print(n, m)

    elif opt == '2':
        print('Calling add_contact() function...')
        n = parse_file_name()
        if dbfile_exists(n):
            add_contact(n)
        else:
            print('DataBase does not exist...')
            return

    elif opt == '3':
        print('Calling search_contact() function...')
        fname = parse_file_name(input('Data Base name: '))
        if not dbfile_exists(fname):
            print(
                f'Data Base {fname} does not exist, first most be create it.\nExiting!!'
            )
            exit(5)

        o = search_menu()
        if o == '0':
            return
        search_contact(fname, o)

    elif opt == '4':
        print('Calling remove_contact() function...')

    elif opt == '5':
        print('Calling print_contact() function...')

    else:
        print('Invalid parameter...')
        exit(5)

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
