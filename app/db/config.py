#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            forename TEXT NOT NULL,
            surname  TEXT NOT NULL,
            username TEXT NOT NULL,
            pw_hash  TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL
        )
    """

    SEED_DATA = """
         INSERT INTO users (forename, surname, username, pw_hash, is_admin)
         values ('admin', 'person', 'admin', 'scrypt:32768:8:1$bWFxNHmhbwCRY5lc$7f093fbd397c96d03868f046e2e51cac69ea72598b0c267933982c2b029f7cf8a4f219ca08d37ffe2f6f3bbeeffd5171f253c9291722eb58ff60e01bf262ebec', TRUE)

    """

# Add more table classes here...
class MessageTable:

    NAME = "messages"

    SCHEMA = """
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """

    SEED_DATA = """
        INSERT INTO messages (user_id, title, body)
        values (1, 'Why hello there', 'post everything')
    """

class ReplyTable:

    NAME = "replies"

    SCHEMA = """
        CREATE TABLE replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            body TEXT NOT NULL,

            FOREIGN KEY(message_id) REFERENCES message(id)
        )
    """

    SEED_DATA = """

    """

#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable,
    MessageTable
    # Add more tables here...
]

