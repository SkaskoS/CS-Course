import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor

class HighlighterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Keyword Highlighter')
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.load_button = QPushButton('Load Document', self)
        self.highlight_button = QPushButton('Highlight Keywords', self)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.highlight_button)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_button.clicked.connect(self.load_document)
        self.highlight_button.clicked.connect(self.highlight_keywords)

        self.keywords = []
        self.highlight_color = 'yellow'
        self.highlight_count = 0

    def load_document(self):
        # Implement document loading logic here
        # Example: Open a file dialog and load the selected document
        pass

    def highlight_keywords(self):
        if not self.keywords:
            return

        document = self.text_edit.toPlainText()

        for keyword in self.keywords:
            cursor = QTextCursor(self.text_edit.document())
            format = cursor.charFormat()
            format.setBackground(self.highlight_color)

            while cursor.find(keyword):
                cursor.mergeCharFormat(format)
                self.highlight_count += 1

        self.setWindowTitle(f'Keyword Highlighter - Highlighted Count: {self.highlight_count}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HighlighterApp()
    window.show()
    sys.exit(app.exec_())
