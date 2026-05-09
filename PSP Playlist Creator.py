import os
import re
import sys
import shutil

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout
)

# -----------------------------------
# NATURAL SORT
# -----------------------------------
def natural_sort_key(s):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', s)
    ]


class PSPPlaylistGenerator(QWidget):

    def __init__(self):
        super().__init__()

        self.psp_root = ""
        self.music_source_folder = ""

        self.init_ui()
        self.show_startup_message()

    # -----------------------------------
    # STARTUP MESSAGE
    # -----------------------------------
    def show_startup_message(self):

        QMessageBox.information(
            self,
            "How It Works",
            (
                "This tool automatically creates PSP playlists from folders.\n\n"
                "1. Select your PSP root.\n"
                "2. Select a music folder from anywhere on your computer.\n\n"
                "The program will:\n"
                "- Scan all subfolders\n"
                "- Detect folders containing music files\n"
                "- Copy all music files directly into PSP/MUSIC\n"
                "- Automatically create one .m3u8 playlist per folder\n\n"
                "Playlist names are automatically based on source folder names.\n"
                "Music filenames are kept unchanged.\n\n"
		"© K0MA.dll : https://github.com/K0MA-dll/"
            )
        )

    # -----------------------------------
    # UI
    # -----------------------------------
    def init_ui(self):

        self.setWindowTitle("PSP Playlist Generator")
        self.setFixedSize(720, 220)

        layout = QVBoxLayout()

        # -------------------------------
        # PSP ROOT
        # -------------------------------
        label_psp = QLabel("PSP Root")

        psp_layout = QHBoxLayout()

        self.entry_psp = QLineEdit()
        self.entry_psp.setReadOnly(True)

        btn_psp = QPushButton("Browse")
        btn_psp.clicked.connect(self.choose_psp)

        psp_layout.addWidget(self.entry_psp)
        psp_layout.addWidget(btn_psp)

        # -------------------------------
        # MUSIC SOURCE FOLDER
        # -------------------------------
        label_music = QLabel("Music Source Folder")

        music_layout = QHBoxLayout()

        self.entry_music = QLineEdit()
        self.entry_music.setReadOnly(True)

        btn_music = QPushButton("Browse")
        btn_music.clicked.connect(self.choose_music_folder)

        music_layout.addWidget(self.entry_music)
        music_layout.addWidget(btn_music)

        # -------------------------------
        # GENERATE BUTTON
        # -------------------------------
        btn_generate = QPushButton("Generate Playlists")
        btn_generate.setFixedHeight(40)
        btn_generate.clicked.connect(self.generate_playlists)

        # -------------------------------
        # ADD TO LAYOUT
        # -------------------------------
        layout.addWidget(label_psp)
        layout.addLayout(psp_layout)

        layout.addSpacing(15)

        layout.addWidget(label_music)
        layout.addLayout(music_layout)

        layout.addSpacing(25)

        layout.addWidget(btn_generate)

        self.setLayout(layout)

    # -----------------------------------
    # CHOOSE PSP ROOT
    # -----------------------------------
    def choose_psp(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select PSP Root"
        )

        if not folder:
            return

        required_folders = ["PSP", "VIDEO"]

        valid = all(
            os.path.isdir(os.path.join(folder, d))
            for d in required_folders
        )

        if not valid:

            QMessageBox.critical(
                self,
                "Invalid PSP Root",
                (
                    "This folder does not appear to be a PSP root.\n\n"
                    "The root must contain:\n"
                    "- PSP\n"
                    "- VIDEO"
                )
            )

            return

        self.psp_root = folder
        self.entry_psp.setText(folder)

    # -----------------------------------
    # CHOOSE MUSIC SOURCE
    # -----------------------------------
    def choose_music_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Music Folder"
        )

        if not folder:
            return

        self.music_source_folder = folder
        self.entry_music.setText(folder)

    # -----------------------------------
    # FIND MUSIC FOLDERS
    # -----------------------------------
    def find_music_folders(self):

        supported_formats = (
            ".mp3",
            ".flac",
            ".wav",
            ".ogg",
            ".m4a"
        )

        music_folders = []

        for root, dirs, files in os.walk(self.music_source_folder):

            has_music = any(
                file.lower().endswith(supported_formats)
                for file in files
            )

            if has_music:
                music_folders.append(root)

        return music_folders

    # -----------------------------------
    # GENERATE PLAYLISTS
    # -----------------------------------
    def generate_playlists(self):

        if not self.psp_root:

            QMessageBox.critical(
                self,
                "Error",
                "Please select the PSP root."
            )

            return

        if not self.music_source_folder:

            QMessageBox.critical(
                self,
                "Error",
                "Please select a music source folder."
            )

            return

        music_folders = self.find_music_folders()

        if not music_folders:

            QMessageBox.information(
                self,
                "No Music Found",
                "No music folders were found."
            )

            return

        psp_music_dir = os.path.join(
            self.psp_root,
            "MUSIC"
        )

        playlist_dir = os.path.join(
            self.psp_root,
            "PSP",
            "PLAYLIST",
            "MUSIC"
        )

        os.makedirs(psp_music_dir, exist_ok=True)
        os.makedirs(playlist_dir, exist_ok=True)

        total_playlists = 0

        supported_formats = (
            ".mp3",
            ".flac",
            ".wav",
            ".ogg",
            ".m4a"
        )

        for folder in music_folders:

            # USE SOURCE FOLDER NAME
            folder_name = os.path.basename(
                os.path.normpath(folder)
            )

            # CLEAN INVALID WINDOWS CHARACTERS
            safe_folder_name = re.sub(
                r'[<>:"/\\\\|?*]',
                "_",
                folder_name
            )

            playlist_entries = []

            for filename in os.listdir(folder):

                source_file = os.path.join(
                    folder,
                    filename
                )

                if not os.path.isfile(source_file):
                    continue

                if not filename.lower().endswith(
                    supported_formats
                ):
                    continue

                destination_file = os.path.join(
                    psp_music_dir,
                    filename
                )

                # COPY ONLY IF FILE DOES NOT EXIST
                # NO WARNING FOR DUPLICATES
                if not os.path.exists(destination_file):

                    shutil.copy2(
                        source_file,
                        destination_file
                    )

                # ALWAYS ADD TO PLAYLIST
                playlist_entries.append(filename)

            if not playlist_entries:
                continue

            # NATURAL SORT
            playlist_entries.sort(
                key=natural_sort_key
            )

            # PLAYLIST FILE PATH
            playlist_path = os.path.join(
                playlist_dir,
                f"{safe_folder_name}.m3u8"
            )

            # WRITE PLAYLIST
            with open(
                playlist_path,
                "w",
                encoding="utf-8"
            ) as f:

                for filename in playlist_entries:

                    line = f"\\MUSIC\\{filename}"

                    f.write(line + "\n")

            total_playlists += 1

        QMessageBox.information(
            self,
            "Success",
            (
                f"{total_playlists} playlist(s) created successfully.\n\n"
                f"All music files were copied into:\n"
                f"{psp_music_dir}"
            )
        )


# -----------------------------------
# MAIN
# -----------------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PSPPlaylistGenerator()
    window.show()

    sys.exit(app.exec())