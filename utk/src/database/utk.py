import sqlite3 

con = sqlite3.connect('utk.db')

cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Operation (
        id integer PRIMARY KEY AUTOINCREMENT, 
        time datetime,
        type text,
        grammar_json text
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id integer PRIMARY KEY AUTOINCREMENT, 
        ip text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Grid (
        id integer PRIMARY KEY AUTOINCREMENT,
        width integer,
        height integer,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
               
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Grammar_Position (
        id integer PRIMARY KEY AUTOINCREMENT,
        width text,
        height text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Position (
        id integer PRIMARY KEY AUTOINCREMENT,
        width text,
        height text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plots (
        id integer PRIMARY KEY AUTOINCREMENT,
        description text,
        arg text,
        arrangement text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)  
    );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS Knots (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text,
        integration_scheme text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Maps (
        id integer PRIMARY KEY AUTOINCREMENT,
        position text,
        direction_right text,
        direction_lookAt text,
        direction_up text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Maps_Knots (
        id integer PRIMARY KEY AUTOINCREMENT,
        knots text,
        maps interger,
        foreign key (maps) references Maps (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Interactions (
        id integer PRIMARY KEY AUTOINCREMENT,
        interaction text,
        maps integer,
        foreign key (maps) references Maps (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Widgets (
        id integer PRIMARY KEY AUTOINCREMENT,
        type text,
        id_operation integer,
        foreign key (id_operation) references Operation (id)
    );
""")

print("Tabela criada com sucesso!")

#desconectando do bando de dados
con.close()

