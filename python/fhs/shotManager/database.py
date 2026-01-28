import os
import sqlite3
from fhs.shotManager.environment import FHS_PIPELINE_ROOT

class Database():
    def __init__(self):
        """Initialize the database connection and create tables if they do not exist."""
        self.conn = sqlite3.connect(os.path.join(FHS_PIPELINE_ROOT, "database.db"))

        self.conn.execute(            
            """
            CREATE TABLE IF NOT EXISTS SHOT (
                id INTEGER PRIMARY KEY, 
                name TEXT UNIQUE NOT NULL, 
                start_frame INTEGER, 
                end_frame INTEGER
            )
            """
        )
        
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS WORKFILE (
                id INTEGER PRIMARY KEY,
                shot_id INTEGER,
                file_path TEXT,
                FOREIGN KEY (shot_id)
                REFERENCES SHOT(id)
                ON DELETE CASCADE
            )
            """
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
    
    def get_shot_id(self, name: str) -> int | None:
        """Get a shot id from its shotname

        Args:
            name (str): shot naem

        Returns:
            int | None: shot id if it exists
        """
        cursor = self.conn.cursor()
        
        command = """
        SELECT id FROM SHOT WHERE name = ?
        """
        cursor.execute(command, (name,))
        result = cursor.fetchone()
        
        return result[0] if result else None
        

    def create_workfile(self, shot_id:int, file_path:str):
        """Insert a new shot into the database.
        Args:
            shot_id (int): id of the connected shot
            file_path (str): filepath to the workfile
        """
        command = """
                    INSERT INTO WORKFILE 
                    (shot_id, file_path) 
                    VALUES 
                    (?, ?)
                    """
        data = (shot_id, file_path)
        self.conn.execute(command, data)
        self.conn.commit()

    def get_shot_workfiles(self, shot_id: int) -> list[str]:
        """Retrieve all workfiles for a shot idfrom the database.
        Args:
            shot_id (int): id of the shot
        Return:
            list[str]: workfiles connected to the shot
        """
        cursor = self.conn.cursor()

        command = """
        SELECT file_path FROM WORKFILE WHERE shot_id = ?
        """
        cursor.execute(command, (shot_id,))
        
        return  [workfile[0] for workfile in cursor.fetchall()]

    def close(self):
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    database = Database()
    #database.create_shot("shot002", 1001, 1010)
    #print(database.get_shot_names())
    
    shot_id = database.get_shot_id("shot002")
    database.create_workfile(shot_id, "my_hipfile.shot002.v002.ma")
    print(database.get_shot_workfiles(shot_id))