import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
from tkinter import font

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

        # Create main grid layout with 6 quadrants
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Create frames for each quadrant
        self.data_frame_above_sliders = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightblue")
        self.top_left_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightgreen")
        self.middle_left_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightyellow")  # New frame for middle-left grid
        self.sliders_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightcoral")
        self.buttons_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightyellow")
        self.information_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightpink")
        self.utils_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightgrey")

        # Layout the frames
        self.data_frame_above_sliders.grid(row=0, column=1, sticky="nsew")
        self.top_left_frame.grid(row=1, column=0, sticky="nsew")  # Place new frame in the middle-left grid
        self.sliders_frame.grid(row=1, column=1, sticky="nsew")
        self.buttons_frame.grid(row=1, column=2, sticky="nsew")  
        self.information_frame.grid(row=2, column=0, rowspan=2, sticky="nsew")
        self.utils_frame.grid(row=2, column=1, rowspan=2, sticky="nsew")

        # Configure grid for data_frame_above_sliders
        self.data_frame_above_sliders.grid_rowconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_columnconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_columnconfigure(1, weight=1)
        self.data_frame_above_sliders.grid_rowconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_rowconfigure(1, weight=1)

        # Create and layout text boxes in the data_frame_above_sliders
        self.text_box1 = tk.Text(self.data_frame_above_sliders, height=5, width=20)
        self.text_box2 = tk.Text(self.data_frame_above_sliders, height=5, width=20)
        self.text_box3 = tk.Text(self.data_frame_above_sliders, height=5, width=20)
        self.text_box4 = tk.Text(self.data_frame_above_sliders, height=5, width=20)

        self.text_box1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.text_box3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Configure grid for buttons_frame
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_rowconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(2, weight=1)
        self.buttons_frame.grid_rowconfigure(3, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        # Create and layout text boxes in the buttons_frame
        self.text_box1 = tk.Text(self.buttons_frame, height=5, width=20)
        self.text_box2 = tk.Text(self.buttons_frame, height=5, width=20)
        self.text_box3 = tk.Text(self.buttons_frame, height=5, width=20)
        self.text_box4 = tk.Text(self.buttons_frame, height=5, width=20)

        self.text_box1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box4.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Create figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(19, 6))
        # Adjust layout to ensure labels and titles are visible
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Create canvas for the top_left_frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, rowspan=2, sticky="nsew")


        # Ensure the canvases resize with the window
        self.top_left_frame.grid_rowconfigure(0, weight=1)
        self.top_left_frame.grid_columnconfigure(0, weight=1)

        self.middle_left_frame.grid_rowconfigure(0, weight=1)
        self.middle_left_frame.grid_columnconfigure(0, weight=1)

        # Create sliders and controls
        self.create_sliders()
        self.create_plot_controls()

        # Initialize the plot
        self.update_plot()


    def create_sliders(self):
        
        self.sliders_frame.columnconfigure(0, weight=1)
        self.sliders_frame.columnconfigure(1, weight=1)
        self.sliders_frame.columnconfigure(2, weight=1)
        self.sliders_frame.columnconfigure(3, weight=1)

        for i in range(5):  # Ensure enough rows are configured
            self.sliders_frame.rowconfigure(i, weight=1)

        # Create sliders
        self.slider1 = self.create_slider(self.sliders_frame, 'Parameter 1', 0.0, 10.0, 5.0, self.update_plot, 0)
        self.slider2 = self.create_slider(self.sliders_frame, 'Parameter 2', 0.0, 20.0, 10.0, self.update_plot, 1)
        self.slider3 = self.create_slider(self.sliders_frame, 'Parameter 3', 0.0, 30.0, 15.0, self.update_plot, 2)
        self.slider4 = self.create_slider(self.sliders_frame, 'Parameter 4', 0.0, 40.0, 20.0, self.update_plot, 3)

        # Grid sliders to fill the top-right quadrant
        self.slider1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.slider2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.slider3.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.slider4.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_slider(self, parent, label, min_val, max_val, init_val, update_func, row):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=row)

        # Create label and place it above the slider
        label_widget = ttk.Label(frame, text=label, font=("Arial", 20))
        label_widget.grid(row=0, column=row, pady=(0, 10))  # Add some padding below the label

        # Create slider and place it below the label # Ensure the layout is updated
        width = self.sliders_frame.winfo_width()
        print(f"Frame width: {width}")
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.VERTICAL, resolution=0.1, length=900, sliderlength=50, width=200, troughcolor='lightblue', command=lambda val: update_func())
        slider.set(init_val)

        return slider

    def create_plot_controls(self):
        # Configure grid rows
        self.sliders_frame.rowconfigure(1, weight=1)
        self.sliders_frame.rowconfigure(2, weight=1)

        menu_font = font.Font(size=25)
        button_font = font.Font(size=22)

        # Plot Type Menubutton
        self.plot_type_var = tk.StringVar()
        self.plot_type_var.set(self.current_plot_type)

        self.plot_type_menu = tk.Menubutton(self.sliders_frame, textvariable=self.plot_type_var, relief=tk.RAISED)
        self.plot_type_menu.grid(row=1, column=0, columnspan=4, rowspan=2, padx=5, pady=5, sticky="nsew")

        # Create a menu for plot types
        plot_type_menu = tk.Menu(self.plot_type_menu, tearoff=0, font=menu_font)
        plot_types = ['Plot Type 1', 'Plot Type 2', 'Plot Type 3']
        for plot_type in plot_types:
            plot_type_menu.add_command(label=plot_type, command=lambda pt=plot_type: self.on_plot_type_change(pt))
        self.plot_type_menu.config(menu=plot_type_menu, font=button_font)

        # Plot Subtype Menubutton
        self.plot_subtype_var = tk.StringVar()
        self.plot_subtype_var.set(self.current_plot_subtype)

        self.plot_subtype_menu = tk.Menubutton(self.sliders_frame, textvariable=self.plot_subtype_var, relief=tk.RAISED)
        self.plot_subtype_menu.grid(row=3, column=0, padx=5, columnspan=4, rowspan=2, pady=5, sticky="nsew")

        # Create a menu for plot subtypes
        plot_subtype_menu = tk.Menu(self.plot_subtype_menu, tearoff=0, font=menu_font)
        plot_subtypes = ['Plot 1', 'Plot 2']
        for plot_subtype in plot_subtypes:
            plot_subtype_menu.add_command(label=plot_subtype, command=lambda ps=plot_subtype: self.on_plot_subtype_change(ps))
        self.plot_subtype_menu.config(menu=plot_subtype_menu, font=button_font)

    def on_plot_type_change(self, selected_plot_type):
        button_font = font.Font(size=22)
        self.current_plot_type = selected_plot_type
        self.plot_type_var.set(selected_plot_type)

        if self.current_plot_type == 'Plot Type 2':
            # Ensure valid subtype
            if self.current_plot_subtype not in ['Plot 1', 'Plot 2']:
                self.current_plot_subtype = 'Plot 1'
            self.plot_subtype_menu.config(menu=self.create_subtype_menu(['Plot 1', 'Plot 2']))
        else:
            self.plot_subtype_menu.config(menu=self.create_subtype_menu([]))  # Disable if not applicable

        self.update_plot()

    def on_plot_subtype_change(self, selected_plot_subtype):
        self.current_plot_subtype = selected_plot_subtype
        self.plot_subtype_var.set(selected_plot_subtype)
        self.update_plot()

    def create_subtype_menu(self, subtypes):
        menu_font = font.Font(size=22)
        subtype_menu = tk.Menu(self.plot_subtype_menu, tearoff=0, font=menu_font)
        for subtype in subtypes:
            subtype_menu.add_command(label=subtype, command=lambda ps=subtype: self.on_plot_subtype_change(ps))
        return subtype_menu

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
