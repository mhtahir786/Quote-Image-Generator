from tkinter import ttk, messagebox
from my_functions import *
import tkinter as tk
import threading
import time

# IMPORTANT - Before use check these, or expect problems!
# Ensure API functionality (valid key), my free account has a LIMIT of 50 requests {my_function.py/generate_image_url/apiKey} - 'https://unsplash.com/'
# Ensure proxies are up to date (if you choose to use) {my_function.py/get_with_proxy/proxyList} - 'https://free-proxy-list.net/'
# Font is freeware, acquired from - 'https://www.fontspace.com/ora-urus-font-f119179'

# Initialise quotes website                
url = "https://quotes.toscrape.com/"

# - - User Interface
# Class Window inherits tk.Tk so it can act as a window
class Window(tk.Tk):

    # - - Constructor (default)
    def __init__(self):
        super().__init__()

        # Initialise root window
        self.geometry("800x500")
        self.title("Main")

        # Other Variables
        self.generateSuccess = False
        self.originalURL = ""

        # Design the root window; begin with a description label
        self.descLabel = tk.Label(self, text="Click the generate button for a random Quote Image!", font=("Times", 20))
        self.descLabel.pack(side="top", pady=(50))

        # Progress Bar which is hidden until generation starts
        self.progBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode="determinate", maximum=100)
        self.progBar.pack_forget()  # hide when not required

        # Extra information; including quote author and link to original image
        self.authorLabel = tk.Label(self, text="Quote Author: ", font=("Times New Roman", 10), wraplength=200, width=500)
        self.authorLabel.pack_forget()
        self.linkLabel = tk.Label(self, text="Original Image URL: ", font=("Times New Roman", 10), wraplength=500, width=700)
        self.linkLabel.pack_forget()

        # Button to generate quote on image
        self.generateButton = tk.Button(self, text="Generate", font=("Helvetica 30 bold"), height=3, width=20, bd=5, relief="raised", 
                                   bg="#00ff00", fg="#ffffff", activebackground="#ffff00", anchor="center", command=lambda:self.generate_clicked())
        self.generateButton.pack(side="bottom", pady=(0, 30))

        # Button to end program
        self.endButton = tk.Button(self, text="Exit", font=("Helvetica 10 bold"), height=1, width=3, bg="#ff0000", fg="#000000", command=self.rip)
        self.endButton.place(x=3, y=470)  # bottom left

    
    # - - Functions
    # End program and destroy instance of window
    def rip(self):
        self.destroy()

    # Changes the progress bar value to what is given, to show task completion
    def update_progressBar(self, val):
        self.progBar['value'] = val
        self.update_idletasks()  # ensure update shows, force it
    
    # Shortens a full link to fit window
    def truncate_url(self, textURL):
        MAX_LENGTH = 50  # preset constant
        # Shorten with elipses when beyond max length, otherwise use full size
        if len(textURL) > MAX_LENGTH:
            return textURL[:MAX_LENGTH] + "..."
        else:
            return textURL

    # Shows the full link to an original image in an information window
    def show_full_link(self, event):
        messagebox.showinfo("Full Link", f"Complete URL - {self.originalURL}")

    # Function called when the generate button is clicked
    def generate_clicked(self):
        # Disable button to prevent spamming
        self.generateButton.config(state=tk.DISABLED, bg="#383b39", cursor="watch")

        # Hide any previous author names or image URL's
        self.authorLabel.pack_forget()
        self.linkLabel.pack_forget()

        # Initiate progress bar and begin task
        self.progBar.pack(pady=30)
        self.progBar['value'] = 5  # show task has begun
    
        # Begin displaying image as a new thread (will be main thread)
        threading.Thread(target=lambda:self.display_image()).start()

    # Return an image with a quote on the background
    def display_image(self):
        # Constant Variables for progress bar completion
        GOT_ALL_QUOTES = 45
        GOT_RANDOM_QUOTE = 60
        GOT_SOME_IMAGE = 75
        GOT_COMPLETE_IMAGE = 100

        # Get all quote data
        allQuotes = get_all_quote_data(url)
        self.update_progressBar(GOT_ALL_QUOTES)
        # Get a random quote
        randomQuote = select_random_row(allQuotes)
        self.update_progressBar(GOT_RANDOM_QUOTE)

        # Display image on screen
        image, originalURL = get_image_with_text(randomQuote['Quote'], randomQuote['Tag'])
        self.update_progressBar(GOT_SOME_IMAGE)
        if not image:
            self.descLabel.config(text="Error displaying image, please try again!")
            self.generateSuccess = False
            time.sleep(3)  # pause to show error message
        else:
            self.update_progressBar(GOT_COMPLETE_IMAGE)
            self.generateSuccess = True  # flag a successful operation
            image.show() # only shows and not save, so screenshot if needed
        
        # Once task is complete, reset window so another image can be generated
        self.originalURL = originalURL 
        self.after(0, lambda:self.reset_window(authorName=randomQuote['Author']))

    # Resets window to start up like state
    def reset_window(self, authorName):
        # Show progress bar completion and reset it to disappear
        time.sleep(1)
        self.update_progressBar(0)
        self.progBar.pack_forget()

        # Display author name and original image url when successful
        if self.generateSuccess:
            self.authorLabel.configure(text=f"Quote Author : {authorName}")
            self.authorLabel.pack()
            smallerURL = self.truncate_url(textURL=self.originalURL)
            self.linkLabel.configure(text=f"Original Image URL: {smallerURL}")
            self.linkLabel.bind("<Button-1>", self.show_full_link)
            self.linkLabel.pack()
            self.generateSuccess = False  # reset for reuse

        # Reset label description (if required) & Re-enable generate button
        self.descLabel.config(text="Click the generate button for a random Quote Image!")
        self.generateButton.config(state=tk.NORMAL, bg="#00ff00")

# Run window
mainWindow = Window()
mainWindow.mainloop()