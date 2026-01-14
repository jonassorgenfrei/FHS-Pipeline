import sys
from PySide6.QtWidgets import QApplication
from fhs.shotManager.shotManager import ShotManager

app = QApplication(sys.argv)
window = ShotManager()
window.show()

sys.exit(app.exec())