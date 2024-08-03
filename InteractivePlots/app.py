import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter and Matplotlib Integration")

        # Initialize plot type and subtype
        self.current_plot_type = 'Plot Type 1'
        self.current_plot_subtype = 'Plot 1'

        # Configure fullscreen mode
        root.state('zoomed') 
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_app)  # Bind Escape to exit the application

        # Create main grid layout with 4 quadrants
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create frames for each quadrant
        self.top_left_frame = ttk.Frame(self.root)
        self.top_right_frame = ttk.Frame(self.root)
        self.bottom_left_frame = ttk.Frame(self.root)
        self.bottom_right_frame = ttk.Frame(self.root)

        self.top_left_frame.grid(row=0, column=0, sticky="nsew")
        self.top_right_frame.grid(row=0, column=1, sticky="nsew")
        self.bottom_left_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_right_frame.grid(row=1, column=1, sticky="nsew")

        # Create a figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(17, 11))
        #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Create canvas for the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.top_left_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Create sliders and controls
        self.create_sliders()
        self.create_plot_controls()

        # Initialize the plot
        self.update_plot()

    def create_sliders(self):
        self.top_right_frame.columnconfigure(0, weight=1)
        self.top_right_frame.columnconfigure(1, weight=1)
        self.top_right_frame.columnconfigure(2, weight=1)
        self.top_right_frame.columnconfigure(3, weight=1)
        # Create sliders in the top-right quadrant
        self.top_right_frame.columnconfigure(0, weight=1)
        for i in range(5):  # Ensure enough rows are configured
            self.top_right_frame.rowconfigure(i, weight=1)

        # Create sliders
        self.slider1 = self.create_slider(self.top_right_frame, 'Parameter 1', 0.0, 10.0, 5.0, self.update_plot, 0)
        self.slider2 = self.create_slider(self.top_right_frame, 'Parameter 2', 0.0, 20.0, 10.0, self.update_plot, 1)
        self.slider3 = self.create_slider(self.top_right_frame, 'Parameter 3', 0.0, 30.0, 15.0, self.update_plot, 2)
        self.slider4 = self.create_slider(self.top_right_frame, 'Parameter 4', 0.0, 40.0, 20.0, self.update_plot, 3)

        # Grid sliders to fill the top-right quadrant
        self.slider1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.slider2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.slider3.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.slider4.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

    def create_slider(self, parent, label, min_val, max_val, init_val, update_func, row):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=row, padx=5, pady=5, sticky="nsew")

        # Create label and place it above the slider
        label_widget = ttk.Label(frame, text=label, font=("Arial", 20))
        label_widget.grid(row=0, column=row, pady=(0, 10))  # Add some padding below the label

        # Create slider and place it below the label
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.VERTICAL, resolution=0.1, length=700, sliderlength=50, width=200, troughcolor='lightblue', command=lambda val: update_func())
        slider.set(init_val)
        slider.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        return slider

    def create_plot_controls(self):
        # Create dropdown menus in the bottom-left quadrant
        self.bottom_left_frame.columnconfigure(0, weight=1)
        self.bottom_left_frame.rowconfigure(0, weight=1)
        self.bottom_left_frame.rowconfigure(1, weight=1)

        # Plot Type Dropdown
        self.plot_type_var = tk.StringVar()
        self.plot_type_var.set(self.current_plot_type)
        self.plot_type_menu = ttk.Combobox(self.bottom_left_frame, textvariable=self.plot_type_var, values=['Plot Type 1', 'Plot Type 2', 'Plot Type 3'])
        self.plot_type_menu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.plot_type_menu.bind("<<ComboboxSelected>>", self.on_plot_type_change)

        # Plot Subtype Dropdown
        self.plot_subtype_var = tk.StringVar()
        self.plot_subtype_var.set(self.current_plot_subtype)
        self.plot_subtype_menu = ttk.Combobox(self.bottom_left_frame, textvariable=self.plot_subtype_var, values=['Plot 1', 'Plot 2'])
        self.plot_subtype_menu.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.plot_subtype_menu.bind("<<ComboboxSelected>>", self.on_plot_subtype_change)

    def on_plot_type_change(self, event):
        self.current_plot_type = self.plot_type_var.get()
        if self.current_plot_type == 'Plot Type 2':
            # Ensure valid subtype
            if self.current_plot_subtype not in ['Plot 1', 'Plot 2']:
                self.current_plot_subtype = 'Plot 1'
            self.plot_subtype_menu.config(values=['Plot 1', 'Plot 2'])
        else:
            self.plot_subtype_menu.config(values=[])  # Disable if not applicable

        self.update_plot()

    def on_plot_subtype_change(self, event):
        self.current_plot_subtype = self.plot_subtype_var.get()
        self.update_plot()

    def update_plot(self):
        self.ax.clear()

        # Get the values from sliders
        param1 = self.slider1.get()
        param2 = self.slider2.get()
        param3 = self.slider3.get()
        param4 = self.slider4.get()

        if self.current_plot_type == 'Plot Type 1':
            self.plot_type_1(param1, param2)
            self.ax.set_title('Plot Type 1')
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')

        elif self.current_plot_type == 'Plot Type 2':
            if self.current_plot_subtype == 'Plot 1':
                self.plot_type_2_plot1(param1, param2, param3, param4)
                self.ax.set_title('Plot Type 2 - Plot 1')
            elif self.current_plot_subtype == 'Plot 2':
                self.plot_type_2_plot2(param1, param2, param3, param4)
                self.ax.set_title('Plot Type 2 - Plot 2')
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')

        elif self.current_plot_type == 'Plot Type 3':
            self.plot_type_3(param1, param2, param3, param4)
            self.ax.set_title('Plot Type 3')
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')

        self.canvas.draw()

    def exit_app(self, event=None):
        sys.exit()  # Close the application

    def plot_type_1(self, param1, param2):
        x = np.linspace(0, 10, 100)
        y = param1 * np.sin(param2 * x)
        self.ax.plot(x, y, 'r-', label='Plot 1 - Sin Component')
        self.ax.legend()

    def plot_type_2_plot1(self, param1, param2, param3, param4):
        x = np.linspace(0, 10, 100)
        y = param1 * np.sin(param2 * x) + param3 * np.cos(param4 * x)
        self.ax.plot(x, y, 'r-', label='Plot 2 - Combined Sin and Cos Components')
        self.ax.legend()

    def plot_type_2_plot2(self, param1, param2, param3, param4):
        x = np.linspace(0, 10, 100)
        y = param2 * np.cos(param1 * x) + param3 * np.sin(param4 * x)
        self.ax.plot(x, y, 'g-', label='Plot 2 - Mixed Components')
        self.ax.legend()

    def plot_type_3(self, param1, param2, param3, param4):
        x = np.linspace(0, 10, 100)
        y = param1 * np.exp(-param2 * x) + param3 * np.sin(param4 * x)
        self.ax.plot(x, y, 'b-', label='Plot Type 3 - Exp and Sin Components')
        self.ax.legend()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
