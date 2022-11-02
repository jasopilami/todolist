from ast import Delete
from rich.console import Console
from rich.table import Table

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

"""
Datenbank Queries:

C: Create       = `INSERT INTO table VALUES (...);`
R: Read         = `SELECT * FROM table;`
U: Update       = `UPDATE table SET colum1 = value1 WHERE condition;`
D: Delete       = `DELETE FROM table WHERE condition;`


Examples:

C:      `INSERT INTO friends (first_name, last_name) VALUES ('Gustav', 'Gans');
R:      `SELECT * FROM friends;`
U:      `UPDATE friends SET first_name = 'Dagobert' WHERE id = 4;`
D:      `DELETE FROM friends WHERE id = 4;`
"""

# # # ###########################################
# # Do not touch!
# # Database Connection stuff!
# Erzeugen einer neuen Datenbank Engine
database = create_engine("sqlite:///friendbook.db")
# Basisklasse für Klassen
Base = declarative_base()

# Öffne Verbindung zur Datenbank
Session = sessionmaker(bind=database)
# Offene Verbindung zur Datenbank
session = Session()

# Rich Initialization
console = Console()
# # # ###########################################


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    done = Column(bool)

    def __repr__(self) -> str:
        return f"<{self.id}, {self.name}, {self.done} >"


def initialize_database():
    """
    Initializes the database and creates all tables.

    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Base.metadata.create_all(database)


# # # ###########################################
# # # Menu
# # # ###########################################
def show_menu():
    """
    Displays a menu.
    """

    MENU_TEXT = """
    Menu: 
    - (A)dd new task
    - (L)ist (C)ompleted task
    - (L)ist uncomplete tasks
    - (D)elete a task
    - (C)omplete a task
    - (E)xit
    """
    print(MENU_TEXT)


def get_users_menu_input():
    menu_choice = input("Choose menu option: ")

    if menu_choice == "A":
        add_new_task()
    elif menu_choice == "D":
        delete_a_task()
    elif menu_choice == "E":
        console.print(f"Bye!", style="bold red")
        exit(1)
    elif menu_choice == "C":
        complete_a_task()
    elif menu_choice == "LC":
        list_completed_task()
    elif menu_choice == "L":
        list_uncompleted_task()
  
  # # # ###########################################
# # # User choices
# # # ###########################################
def add_new_task():
    """
    Asks the user for the information about the new task. 
    Adds the task to the database.
    """
    print("Einen neuen Freund hinzufügen")
    name = input("task\t:")
    new_task = Task(name=name)
    database_add_task(new_task)

def delete_a_task():
    to_delete_id = int(input("ID of task you want to delete: "))
    session.query(Task).filter_by(id = to_delete_id).delete()
    session.commit()

def complete_a_task():
    # zu updatende ID Benutzer
    # first und last name Abfrage
    # updaten in der Datenbank
    # committen
     task_to_complete = int(input("id of task to complete?"))
     id = input("name\t:")
     session.query(Task).filter_by(id = task_to_complete).update({Task.done: True})
     session.commit()

def list_all_tasks():
    tasks = database_get_all_tasks()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("ID", style="dim")
    table.add_column("name")
    
    for task in tasks:
        table.add_row(str(tasks.id), task.name)

    console.print(table)

def database_add_friend(task: Task):
    """
    Database command to add a new task.
    ORM = Object Relational Mapper
    """
    session.add(task)
    session.commit()
    
def database_get_all_tasks():
    """
    Database command to get all tasks.
    `tasks = session.query(Task).all()` is a query call made with the sqlalchemy ORM. 
    The SQL query that is made is: `SELECT * FROM tasks;`
    Alternative to this with raw sql:
    `all_tasks_raw = session.execute("SELECT * FROM tasks;").fetchall()`
    """
    return session.query(Task).all()

# # # ###########################################
# # # Main
# # # ###########################################
if __name__ == "__main__":
    initialize_database()

    while True:
        show_menu()
        get_users_menu_input()
    

        