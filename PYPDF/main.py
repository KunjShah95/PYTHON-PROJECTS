import pyttsx3
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfReader

class PDFReaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Reader")
        self.master.geometry("900x700")
        self.master.resizable(True, True)

        self.pdfReader = None
        self.text_content = ""
        self.player = pyttsx3.init()
        self.is_paused = False
        self.is_stopped = True
        self.current_page = 0

        # Create a frame for the text area and scrollbar
        text_frame = Frame(master)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create a text area for displaying the PDF content
        self.text_area = Text(text_frame, wrap='word', height=30, width=80, state=DISABLED)
        self.text_area.pack(side=LEFT, fill=BOTH, expand=True)

        # Create a scrollbar
        self.scrollbar = Scrollbar(text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # Frame for buttons
        button_frame = Frame(master, bg="#f4f4f4")
        button_frame.pack(fill=X, pady=10)

        # Create buttons
        open_button = Button(button_frame, text="Open PDF", command=self.open_pdf, width=15, bg="#007BFF", fg="white")
        open_button.grid(row=0, column=0, padx=10, pady=5)

        self.play_button = Button(button_frame, text="Play", command=self.read_aloud, width=15, bg="#28A745", fg="white", state=DISABLED)
        self.play_button.grid(row=0, column=1, padx=10, pady=5)

        self.pause_button = Button(button_frame, text="Pause", command=self.pause, width=15, bg="#FFC107", fg="black", state=DISABLED)
        self.pause_button.grid(row=0, column=2, padx=10, pady=5)

        self.stop_button = Button(button_frame, text="Stop", command=self.stop, width=15, bg="#DC3545", fg="white", state=DISABLED)
        self.stop_button.grid(row=0, column=3, padx=10, pady=5)

        # Bind the close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        # Initialize the PDF reader and extract text
        self.pdfReader = PdfReader(file_path)
        self.text_content = ""
        for page in self.pdfReader.pages:
            self.text_content += page.extract_text() + "\n"

        # Display the full text in the text area
        self.text_area.config(state=NORMAL)  # Enable editing to insert text
        self.text_area.delete(1.0, END)  # Clear the text area
        self.text_area.insert(END, self.text_content.strip())  # Insert the full text
        self.text_area.config(state=DISABLED)  # Disable editing to prevent user changes

        # Enable the buttons
        self.play_button.config(state=NORMAL)
        self.pause_button.config(state=DISABLED)
        self.stop_button.config(state=DISABLED)

    def read_aloud(self):
        if not self.text_content.strip():
            messagebox.showwarning("Warning", "Please open a PDF file first.")
            return

        self.is_stopped = False
        self.is_paused = False

        # Set properties for speech
        try:
            rate = simpledialog.askinteger("Input", "Enter speech rate (default is 200):", minvalue=50, maxvalue=400, initialvalue=200)
            volume = simpledialog .askfloat("Input", "Enter volume (0.0 to 1.0):", minvalue=0.0, maxvalue=1.0, initialvalue=1.0)

            if rate is not None:
                self.player.setProperty('rate', rate)
            if volume is not None:
                self.player.setProperty('volume', volume)

            # Disable play button and enable pause/stop buttons
            self.play_button.config(state=DISABLED)
            self.pause_button.config(state=NORMAL)
            self.stop_button.config(state=NORMAL)

            # Read aloud the entire text content
            self.player.say(self.text_content)
            self.player.runAndWait()

            # Reset buttons after playback
            self.play_button.config(state=NORMAL)
            self.pause_button.config(state=DISABLED)
            self.stop_button.config(state=DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def pause(self):
        if not self.is_stopped:
            self.is_paused = True
            self.player.stop()  # Pause the current speech

            # Update button states
            self.play_button.config(state=NORMAL)
            self.pause_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)

    def stop(self):
        self.is_stopped = True
        self.is_paused = False
        self.player.stop()  # Stop the current speech

        # Update button states
        self.play_button.config(state=NORMAL)
        self.pause_button.config(state=DISABLED)
        self.stop_button.config(state=DISABLED)

    def on_closing(self):
        self.stop()  # Ensure any ongoing speech is stopped
        self.master.destroy()  # Close the application

# Create the main window
root = Tk()
app = PDFReaderApp(root)

# Start the GUI event loop
root.mainloop()