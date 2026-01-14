import os
import sys
try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ModuleNotFoundError:
    from PySide2 import QtWidgets, QtCore, QtGui
from fhs.shotManager.file_system import create_shot_structure
from fhs.shotManager.database import Database
from fhs.shotManager.usd import create_shot_usd_structure   

class ShotManager(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        """Initialize the Shot Manager GUI."""
        super().__init__(parent)

        self.database = Database()

        self.setWindowTitle("FHS Shot Manager")
        self.instruction_label = QtWidgets.QLabel(
            "FHS Shot Manager - Create New Shot", self
        )

        self.shot_list = QtWidgets.QListWidget(self)
        self.shot_list.addItems(self.database.get_shot_names())     

        self.seq_label = QtWidgets.QLabel("Enter Sequence Name:", self)
        self.seq_name = QtWidgets.QLineEdit(self)
        
        self.shot_label = QtWidgets.QLabel("Enter Shot Name:", self)
        self.shot_name = QtWidgets.QLineEdit(self)
        
        range_layout = QtWidgets.QHBoxLayout()
        
        self.start_frame_label = QtWidgets.QLabel("Start Frame:", self)
        self.start_frame = QtWidgets.QLineEdit(self)
        self.start_frame.setText("1001")
        
        self.end_frame_label = QtWidgets.QLabel("End Frame:", self)
        self.end_frame = QtWidgets.QLineEdit(self)
        self.end_frame.setText("1010")
        
        range_layout.addWidget(self.start_frame_label)
        range_layout.addWidget(self.start_frame)
        range_layout.addWidget(self.end_frame_label)
        range_layout.addWidget(self.end_frame)
        
        # input validation: only allow alphanumeric and underscores
        regex = QtCore.QRegularExpression(r"^[A-Za-z0-9_]*$")

        validator = QtGui.QRegularExpressionValidator(regex)
        self.shot_name.setValidator(validator)
        self.seq_name.setValidator(validator)

        self.create_button = QtWidgets.QPushButton("Create Shot", self)
        self.create_button.clicked.connect(self.create_shot_btn_callback)

        # dynamic spacer to push elements to the top
        spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.instruction_label)
        layout.addWidget(self.shot_list)
        layout.addItem(spacer)
        layout.addWidget(self.seq_label)
        layout.addWidget(self.seq_name)

        layout.addWidget(self.shot_label)
        layout.addWidget(self.shot_name)
        
        layout.addLayout(range_layout)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

        # set fixed size
        self.setFixedSize(600, 400)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Handle the close event to ensure database connection is closed."""
        self.database.close()
        event.accept()
    
    def create_shot_btn_callback(self) -> None:
        """Callback function for the 'Create Shot' button."""
        shot_name: str = self.shot_name.text()
        seq_name: str = self.seq_name.text()
        try:
            start_frame: int = int(self.start_frame.text())
            end_frame: int = int(self.end_frame.text())
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Invalid frame range specified.", "Invalid frame range specified.")
            return

        if self.create_shot(shot_name, seq_name, start_frame, end_frame):
            self.close()
        else:
            return

    def create_shot(self, shot_name: str, seq_name: str, start_frame:int, end_frame:int) -> bool:
        """Create a new shot directory structure.

        Args:
            shot_name (str): shot name to create
            seq_name (str): sequence name to create
            start_frame (int): start frame of the shot
            end_frame (int): end frame of the shot

        Returns:
            bool: _True if shot creation was successful, False otherwise.
        """
        try:
            if start_frame >= end_frame:
                raise ValueError("Invalid frame range specified.")
            
            shot_directory: str = create_shot_structure(shot_name, seq_name)
            usd_file = create_shot_usd_structure(os.path.join(shot_directory, "usd"))
                        
            workfile = self.create_workfile(shot_name, shot_directory, start_frame, end_frame)
            self.insert_shot(shot_name, start_frame, end_frame)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
            return False

        QtWidgets.QMessageBox.information(
            self,
            "Shot Created",
            f"Shot '{seq_name}_{shot_name}' created successfully at \n {shot_directory}!",
        )
        return True
    
    def create_workfile(self, shot_name:str, shot_directory:str, start_frame:int, end_frame:int) -> str:
        """
        This function needs to be implemented in the dcc widget
        
        Args:
            shot_name (str): _name of the shot
            shot_directory (str): _path to the shot directory
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        """
        return ""

    def insert_shot(self, shot_name:str, start_frame:int, end_frame:int):
        """Insert the created shot into the database.
        Args:
            shot_name (str): _name of the shot
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        """
        self.database.create_shot(shot_name, start_frame, end_frame)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShotManager()
    window.show()
    sys.exit(app.exec())
