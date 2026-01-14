import os
import sqlite3
from fhs.shotManager.environment import FHS_PIPELINE_ROOT

class Database():
    def __init__(self):
        """Initialize the database connection and create tables if they do not exist."""
        self.conn = sqlite3.connect(os.path.join(FHS_PIPELINE_ROOT, "database.db"))

        self.conn.execute(            
            "CREATE TABLE IF NOT EXISTS SHOT (id INTEGER PRIMARY KEY, name TEXT, start_frame INTEGER, end_frame INTEGER)"
        )

    def create_shot(self, name:str, start_frame:int, end_frame:int):
        """Insert a new shot into the database.
        Args:
            name (str): _name of the shot
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        """
        command = """
                    INSERT INTO SHOT 
                    (name, start_frame, end_frame) 
                    VALUES 
                    (?, ?, ?)
                    """
        data = (name, start_frame, end_frame)
        self.conn.execute(command, data)
        self.conn.commit()

    def get_shot_names(self) -> list[str]:
        """Retrieve all shot names from the database."""
        cursor = self.conn.cursor()

        command = """
        SELECT SHOT.name FROM SHOT
        """
        cursor.execute(command)
        shot_names = [shot[0] for shot in cursor.fetchall()]
        return shot_names

    def close(self):
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    database = Database()
    # database.create_shot("shot001", 1001, 1010)
    print(database.get_shot_names())