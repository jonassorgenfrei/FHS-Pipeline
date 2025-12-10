import sys
from PySide6 import QtWidgets, QtCore, QtGui
from fhs.shotManager.file_system import create_shot_structure


class ShotManager(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("FHS Shot Manager")
        self.instruction_label = QtWidgets.QLabel(
            "FHS Shot Manager - Create New Shot", self
        )

        self.shot_label = QtWidgets.QLabel("Enter Shot Name:", self)
        self.shot_name = QtWidgets.QLineEdit(self)

        self.seq_label = QtWidgets.QLabel("Enter Sequence Name:", self)
        self.seq_name = QtWidgets.QLineEdit(self)

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
        layout.addItem(spacer)
        layout.addWidget(self.seq_label)
        layout.addWidget(self.seq_name)
        layout.addWidget(self.shot_label)
        layout.addWidget(self.shot_name)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

        # set fixed size
        self.setFixedSize(600, 400)

    def create_shot_btn_callback(self) -> None:
        """Callback function for the 'Create Shot' button."""
        shot_name: str = self.shot_name.text()
        seq_name: str = self.seq_name.text()

        if self.create_shot(shot_name, seq_name):
            self.close()
        else:
            return

    def create_shot(self, shot_name: str, seq_name: str) -> bool:
        """Create a new shot directory structure.

        Args:
            shot_name (str): shot name to create
            seq_name (str): sequence name to create

        Returns:
            bool: _True if shot creation was successful, False otherwise.
        """
        try:
            shot_directory: str = create_shot_structure(shot_name, seq_name)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
            return False

        QtWidgets.QMessageBox.information(
            self,
            "Shot Created",
            f"Shot '{seq_name}_{shot_name}' created successfully at \n {shot_directory}!",
        )
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShotManager()
    window.show()
    sys.exit(app.exec())
