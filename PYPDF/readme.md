# PDF Reader with Text-to-Speech

## Overview

The **PDF Reader with Text-to-Speech** is a Python-based application designed to enable users to open and read PDF files while listening to the content being read aloud. The application features a user-friendly graphical interface developed using Tkinter, and it utilizes PyPDF2 for PDF parsing and pyttsx3 for text-to-speech (TTS) functionality.

## Features

- **Open PDF Files**: Load and display the content of any PDF file.
- **Text-to-Speech Playback**: Listen to the content of the PDF read aloud, with adjustable speech rate and volume.
- **Playback Controls**: Play, pause, and stop TTS playback using intuitive buttons.
- **Scrollable Content Viewer**: View the entire content of the PDF in a scrollable text area.
- **Dynamic and Responsive GUI**: A clean and responsive graphical user interface for easy navigation.

## Technologies Used

- **Python**: The core programming language used for development.
- **Tkinter**: For creating the graphical user interface.
- **PyPDF2**: For parsing and extracting text from PDF files.
- **pyttsx3**: For implementing text-to-speech functionality.

## Installation

### Prerequisites

- Python 3.8 or later must be installed on your system.
- Required Python libraries: `pyttsx3`, `PyPDF2`, and `tkinter` (bundled with Python).

### Steps

1. **Clone the Repository**:

   git clone https://github.com/KunjShah95/PYPDF.git
   cd PYPDF
Install the Dependencies:

pip install pyttsx3 PyPDF2
Run the Application:


python PYPDF.py
Usage:

Click the Open PDF button to load a PDF file.
Click Play to start the text-to-speech playback.
Use Pause or Stop to control the playback.
Code Structure
pdf_reader_tts.py: The main application file containing the GUI logic, PDF handling, and TTS implementation.
Contribution
Contributions are welcome! If you would like to improve this project, please follow these steps:

Fork this repository.
Create a new branch:
git checkout -b feature-new-feature
Commit your changes:
git commit -m "Add some feature"
Push to the branch:
git push origin feature-new-feature
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.