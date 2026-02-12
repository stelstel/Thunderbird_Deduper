# app_gui.py

import sys
import os
import logging

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QListWidget, QTextEdit, QMessageBox, QProgressBar,
    QCheckBox
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from config import load_config, save_config
from functions.scanner import find_mbox_files, parse_all_mailboxes
from functions.backup_mail_folder import backup_folder
from functions.process_mboxes import process_mboxes
from functions.logging_setup import setup_logging
from datetime import datetime
from functions.functions import log_uncaught_exceptions, is_thunderbird_running, calc_duration, format_size

DEBUG_MODE = True

setup_logging(debug=DEBUG_MODE)
logging.info("-" * 80)
logging.info("Started Thunderbird Duplicate Email Remover.")
LOG_FILE = os.path.join("logs", "thunderbird_deduper.log")

# Set global exception handler
sys.excepthook = log_uncaught_exceptions



class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the Thunderbird Duplicate Email Remover GUI application.
        Sets up the main window with:
        - Window properties (title, icon, minimum size)
        - Progress bar and status label
        - Configuration loading from config file
        - Menu bar with File (Exit) and Help (About, View Log) menus
        - Main widgets including:
            - Folder selection input with browse button
            - Checkbox to exclude trash folders
            - Start scan button
            - Mailbox files list display
            - Status output text area
            - Exit button
        - Layout organization using QVBoxLayout and QHBoxLayout
        """
        super().__init__()

        self.setWindowTitle("Thunderbird Duplicate Email Remover")
        self.setWindowIcon(QIcon("icons/thunderbird_deduper.ico"))
        self.setMinimumSize(700, 600)

        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("")
        self.progress_label.setFixedWidth(170)
        self.progress_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        # Load config
        self.config = load_config()
        initial_folder = self.config.get("thunderbird_folder", "")
        self.version = self.config.get("version", "")

        # -------------------------------------------------
        # MENU BAR
        # -------------------------------------------------
        menubar = self.menuBar()

        # FILE MENU
        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # HELP MENU
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        view_log_action = help_menu.addAction("View Log")
        view_log_action.triggered.connect(self.open_log_file)

        # -------------------------------------------------
        # WIDGETS
        # -------------------------------------------------

        folder_label = QLabel("Select Thunderbird Local Folders directory:")

        self.folder_input = QLineEdit(initial_folder)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)

        self.checkbox_trash = QCheckBox('Exclude trash folders', self)
        self.checkbox_trash.setChecked(eval( self.config["exclude_trash_folders"] ) )

        self.scan_button = QPushButton("Start")
        self.scan_button.setFixedWidth(125)
        self.scan_button.clicked.connect(self.start_scan)
        
        scan_layout = QHBoxLayout()
        scan_layout.addWidget(self.checkbox_trash)
        scan_layout.addWidget(self.scan_button)

        mbox_label = QLabel("Mailbox files found:")
        self.mbox_list = QListWidget()

        status_label = QLabel("Status:")
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        exit_button = QPushButton("Exit")
        exit_button.setFixedWidth(100)
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(folder_label)
        layout.addLayout(folder_layout)
        layout.addLayout(scan_layout)
        layout.addLayout(progress_layout)
        layout.addWidget(mbox_label)
        layout.addWidget(self.mbox_list)
        layout.addWidget(status_label)
        layout.addWidget(self.output_box)
        layout.addWidget(exit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



    # -------------------------------------------------
    # File → Browse…
    # -------------------------------------------------
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Thunderbird Folder",
            self.folder_input.text() or os.path.expanduser("~")
        )

        if folder:
            self.folder_input.setText(folder)



    # -------------------------------------------------
    # Help → About
    # -------------------------------------------------
    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About Thunderbird Duplicate Email Remover",
            (
                "Thunderbird Duplicate Email Remover\n\n"
                "A tool to locate mailbox files and assist in removing email duplicates.\n\n"
                f"Version {self.version}"
            )
        )



    # -------------------------------------------------
    # Help → View Log
    # -------------------------------------------------
    def open_log_file(self):
        if os.path.exists(LOG_FILE):
            os.startfile(LOG_FILE)
        else:
            QMessageBox.warning(
                self,
                "Log file not found",
                "The log file does not exist yet."
            )



    # -------------------------------------------------
    # Scan Button Logic
    # -------------------------------------------------
    def start_scan(self):
        """
        Initiates a scan of Thunderbird mailboxes to find and remove duplicate messages.
        This method performs the following operations:
        1. Checks if Thunderbird is currently running and prompts user to close it if necessary
        2. Disables UI controls and updates scan button to show "Processing..." state
        3. Validates the selected folder path
        4. Creates a backup of the mailbox folder
        5. Scans for mbox files and identifies duplicate messages
        6. Processes mboxes to remove duplicates
        7. Displays results and statistics
        8. Re-enables UI controls upon completion or error
        The method handles user configuration persistence, progress bar updates,
        logging at various stages, and displays appropriate messages to the user
        via the output box and message dialogs.
        Raises:
            Implicitly handles exceptions through try/finally block to ensure
            UI controls are restored regardless of success or failure.
        """

        # -------------------------------------------------
        # THUNDERBIRD RUNNING CHECK
        # -------------------------------------------------
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Thunderbird is running")
        
        msg_box.setText(
            "Thunderbird locks mailbox files while running.\n\n"
            "Please exit this program, close Thunderbird and start this program again."
        )

        exit_button = msg_box.addButton("Exit", QMessageBox.RejectRole)
        exit_button.clicked.connect(QApplication.quit)

        if is_thunderbird_running():
            msg_box.open()

        start_time = datetime.now()

        # Disable button & change text
        self.browse_button.setEnabled(False)
        self.scan_button.setEnabled(False)
        original_text = self.scan_button.text()
        self.scan_button.setText("Processing...")
        QApplication.processEvents()   # Force GUI refresh

        self.progress_label.setText("Backing up mailboxes...")

        try:
            folder = self.folder_input.text().strip()

            if folder:
                self.config["thunderbird_folder"] = folder
                save_config(self.config)

            if not folder or not os.path.isdir(folder):
                self.output_box.setPlainText("❌ Please select a valid folder.\n")
                return
            
            self.output_box.setPlainText(f"✔ Folder selected:\n{folder}\n")
            self.progress_bar.setValue(1)
            logging.info(f"Folder selected: {folder}")
            QApplication.processEvents()   # Force GUI refresh
            
            # ------------- Backing up ------------------------
            backup_file = backup_folder(folder, self.config)


            file_size = os.path.getsize(backup_file)
            backup_file_absolute_path = os.path.abspath(backup_file)
            formatted_file_size = format_size(file_size)

            self.output_box.append(f"✔ Backup created:\nSize: {formatted_file_size}, {backup_file_absolute_path}\n")
            logging.info(f"✔ Backup created:\nSize: {formatted_file_size}, {backup_file_absolute_path}\n")
                        
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                backup_finished_time = datetime.now()
                duration_mins_secs = calc_duration(start_time, backup_finished_time) 
                logging.debug(f"Backup duration: {duration_mins_secs}")

            self.progress_bar.setValue(29)
            self.progress_label.setText("Scanning for duplicate mails...") 
            mboxes = find_mbox_files(folder, self.checkbox_trash.isChecked() )
            self.mbox_list.clear()
            self.mbox_list.addItems(mboxes)

            mboxes, msg_for_output_box, total_messages_deleted = process_mboxes(mboxes, self.progress_bar) 
            
            if total_messages_deleted == 0:
                msg_for_output_box += f"\n❌ No duplicates were found\n"
            else:   
                msg_for_output_box += f"\n✔ Total duplicate messages deleted across all mailboxes: {total_messages_deleted}"
            
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.progress_label.setText("Finished")
            self.output_box.append(msg_for_output_box)
            
            end_time = datetime.now()
            duration_mins_secs = calc_duration(start_time, end_time)
            logging.info(f"Finished. Execution duration: {duration_mins_secs}")

            # Show summary message box
            QMessageBox.information(
                self,
                "Scan complete",
                f"\nTotal duplicate messages deleted across all mailboxes: {total_messages_deleted}"
            )
        finally:
            # Re-enable scan button & restore text
            self.browse_button.setEnabled(True)
            self.scan_button.setEnabled(True)
            self.scan_button.setText(original_text)

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())