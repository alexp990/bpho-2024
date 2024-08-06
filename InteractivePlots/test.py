import tkinter as tk

class NumberEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Entry Example")

        # Title Label
        self.title_label = tk.Label(root, text="Enter a number:", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Entry Widget for number input
        self.number_entry = tk.Entry(root, font=("Helvetica", 14))
        self.number_entry.pack(pady=5)

        # Bind the Enter key to the submission function
        self.number_entry.bind("<Return>", self.display_number)

        # Button to submit the number
        self.submit_button = tk.Button(root, text="Submit", font=("Helvetica", 14), command=self.display_number)
        self.submit_button.pack(pady=10)

        # Label to display the entered number
        self.result_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=10)

    def display_number(self, event=None):
        # Retrieve the number from the Entry widget
        number = self.number_entry.get()
        
        # Update the result label to show the entered number
        self.result_label.config(text=f"Entered number: {number}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberEntryApp(root)
    root.mainloop()
