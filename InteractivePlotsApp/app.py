import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
from tkinter import font
from tasks import Tasks
from matplotlib.animation import FuncAnimation
from PIL import Image
import io
from tkinter import filedialog

tasks = Tasks()

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter and Matplotlib Integration")

        self.current_plot_type = 'Exact Model'
        self.current_plot_subtype = ''

        root.state('zoomed') 
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_app)  

        self.img = tk.PhotoImage(file=r"C:\Users\Alex\Documents\GitHub\bpho-projectile-motion\InteractivePlots\image.png")

        self.start_x = None
        self.start_y = None
        self.scale_factor = 1.1
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.root.bind("<Button-1>", self.on_mouse_down)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind("<MouseWheel>", self.on_mouse_wheel)
        self.root.bind("<Motion>", self.track_mouse_position)

        self.canvas_x = 0
        self.canvas_y = 0

        self.drag_start_x = None
        self.drag_start_y = None

        self.autoscale = True        

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.data_frame_above_sliders = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightgrey")
        self.top_left_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.sliders_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.buttons_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.information_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background="lightgrey")
        self.utils_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.toggle_fixed_axes_button_frame = tk.Frame(self.root, borderwidth=2, relief="solid")

        self.image = tk.Label(self.utils_frame, image=self.img)
        self.image.pack(expand=True)

        self.data_frame_above_sliders.grid(row=0, column=1, sticky="nsew")
        self.top_left_frame.grid(row=1, column=0, sticky="nsew")  
        self.sliders_frame.grid(row=1, column=1, sticky="nsew")
        self.buttons_frame.grid(row=1, column=2, sticky="nsew")  
        self.information_frame.grid(row=2, column=0, rowspan=2, sticky="nsew")
        self.utils_frame.grid(row=2, column=1, rowspan=2, sticky="nsew")
        self.toggle_fixed_axes_button_frame.grid(row=0, column=2, sticky="nsew")

        self.data_frame_above_sliders.grid_rowconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_columnconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_columnconfigure(1, weight=1)
        self.data_frame_above_sliders.grid_rowconfigure(0, weight=1)
        self.data_frame_above_sliders.grid_rowconfigure(1, weight=1)

        self.text_box1 = tk.Label(self.data_frame_above_sliders, height=5, width=20, compound='c')
        self.text_box2 = tk.Label(self.data_frame_above_sliders, height=5, width=20, compound='c')
        self.text_box3 = tk.Label(self.data_frame_above_sliders, height=5, width=20, compound='c')
        self.text_box4 = tk.Label(self.data_frame_above_sliders, height=5, width=20, compound='c')

        self.text_box1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.text_box3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.text_box4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.information_frame.grid_rowconfigure(0, weight=1)
        self.information_frame.grid_rowconfigure(1, weight=1)
        self.information_frame.grid_columnconfigure(0, weight=1)
        self.information_frame.grid_columnconfigure(1, weight=1)
        self.information_frame.grid_columnconfigure(2, weight=1)        


        self.g_label_frame = tk.Frame(self.information_frame, height=2, width=20)
        self.info_box2 = tk.Frame(self.information_frame, height=5, width=20)
        self.info_box3 = tk.Frame(self.information_frame, height=5, width=20)
        self.info_box4 = tk.Frame(self.information_frame, height=5, width=20)
        self.info_box5 = tk.Frame(self.information_frame, height=5, width=20)
        self.info_box6 = tk.Frame(self.information_frame, height=5, width=20)

        self.g_label_frame.grid(row=0, column=0, padx=10, pady=10)
        self.info_box2.grid(row=0, column=1, padx=10, pady=10)
        self.info_box3.grid(row=0, column=2, padx=10, pady=10)
        self.info_box4.grid(row=1, column=0, padx=10, pady=10)
        self.info_box5.grid(row=1, column=1, padx=10, pady=10)
        self.info_box6.grid(row=1, column=2, padx=10, pady=10)

        self.g_label_frame.config(height=330, width=650)
        self.info_box2.config(height=330, width=650)
        self.info_box3.config(height=330, width=650)
        self.info_box4.config(height=330, width=650)
        self.info_box5.config(height=330, width=650)
        self.info_box6.config(height=330, width=650)

        self.g_label_frame.grid_propagate(False)
        self.info_box2.grid_propagate(False)
        self.info_box3.grid_propagate(False)
        self.info_box4.grid_propagate(False)
        self.info_box5.grid_propagate(False)
        self.info_box6.grid_propagate(False)

        self.info_box2.grid_columnconfigure(0, weight=0)
        self.info_box2.grid_columnconfigure(1, weight=0)
        self.info_box2.grid_rowconfigure(0, weight=0)

        self.info_box3.grid_columnconfigure(0, weight=0)
        self.info_box3.grid_columnconfigure(1, weight=0)
        self.info_box3.grid_rowconfigure(0, weight=0)

        self.g_label_frame.grid_columnconfigure(0, weight=0)
        self.g_label_frame.grid_columnconfigure(1, weight=0)
        self.g_label_frame.grid_rowconfigure(0, weight=0)    


        # Initialize DoubleVar instances with default values
        self.g = tk.DoubleVar(value=9.8)  # Example default value
        self.N = tk.IntVar(value=5)    # Example default value
        self.C = tk.DoubleVar(value=0.8)
        self.Cd = tk.DoubleVar(value=0.1)
        self.rho = tk.DoubleVar(value=1)
        self.cs_area = tk.DoubleVar(value=0.005)

        # Create multiple NumberEntryWidget instances
        self.g_widget = self.create_number_entry_widget(
            self.g_label_frame, 
            "Enter g:", 
            "g = ", 
            self.g,
            self.g.get()
        )

        self.C_widget_visible = False

        self.c_widget = self.create_number_entry_widget(
            self.info_box3, 
            "Enter C \n(coefficient of restitution):", 
            "C = ", 
            self.C,
            self.C.get()
        )

        self.show_hide_frame(self.c_widget, self.C_widget_visible)

        self.N_widget_visible = False

        self.n_widget = self.create_number_entry_widget(
            self.info_box2, 
            "Enter N \n(number of bounces):", 
            "N = ", 
            self.N,
            self.N.get()
        )

        self.show_hide_frame(self.n_widget, self.N_widget_visible)

        self.Cd_widget_visible = False

        self.Cd_widget = self.create_number_entry_widget(
            self.info_box5, 
            "Enter Cd \n(drag coefficient):", 
            "Cd = ", 
            self.Cd,
            self.Cd.get()
        )

        self.rho_widget_visible = False

        self.rho_widget = self.create_number_entry_widget(
            self.info_box6, 
            "Enter rho \n(air density):", 
            "Cd = ", 
            self.rho,
            self.rho.get()
        )

        self.show_hide_frame(self.rho_widget, self.rho_widget_visible)

        self.cs_area_widget_visible = False

        self.cs_area_widget = self.create_number_entry_widget(
            self.info_box2, 
            "Enter CS area \n(cross sectional area):", 
            "CS area = ", 
            self.cs_area,
            self.cs_area.get()
        )

        self.show_hide_frame(self.rho_widget, self.rho_widget_visible)

        self.info_box4.grid_columnconfigure(0, weight=1)
        self.info_box4.grid_rowconfigure(0, weight=1)
        self.toggle_range_button = tk.Button(self.info_box4, text="Toggle distance travelled\nby projectile", command=self.toggle_distance_travelled_by_projectile, font=("Helvetica", 30), height=2, width=1)
        self.toggle_range_button.grid(row = 0, column=0, padx=5, pady=5, stick='nsew')

        self.distance_travelled_by_projectile_var = True

        self.options = ["Verlet", "RK4"]
        self.menu_font = font.Font(size=30)
        self.button_font = font.Font(size=35)

        self.integrator_button_visible = False

        self.selected_integration_method = tk.StringVar()
        self.selected_integration_method.set(self.options[0])

        self.info_box3.grid_columnconfigure(0, weight=1)
        self.info_box3.grid_rowconfigure(0, weight=1)
        self.toggle_integration_method = tk.Menubutton(
            self.info_box3, 
            text=f"{self.options[0]}",
            font=self.button_font,
            width=20
        )
        self.toggle_integration_method.grid(row = 0, column=0, padx=5, pady=5, stick='nsew')
        self.toggle_integration_method.bind("<<ComboboxSelected>>", self.on_selection_integrator)

        self.integrator_button_visible == False

        self.menu = tk.Menu(self.toggle_integration_method, tearoff=0)
        for option in self.options:
            self.menu.add_command(
                label=option, 
                command=lambda opt=option: self.on_selection_integrator(opt),
                font=self.menu_font
            )

        self.toggle_integration_method['menu'] = self.menu

        self.distance_travelled_by_projectile_var = True        

        self.info_box5.grid_columnconfigure(0, weight=1)
        self.info_box5.grid_rowconfigure(0, weight=1)
        self.toggle_animation_button = tk.Button(self.info_box5, text="Toggle animation", command=self.toggle_animation, font=("Helvetica", 34), height=2, width=1)
        self.toggle_animation_button.grid(row = 0, column=0, padx=5, pady=5, stick='nsew')
        self.animation_button_visible = False
        self.toggle_animation_button.grid_forget()

        self.toggle_animation_var = False

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_rowconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(2, weight=1)
        self.buttons_frame.grid_rowconfigure(3, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(19, 6))

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.top_left_frame.grid_rowconfigure(0, weight=1)
        self.top_left_frame.grid_columnconfigure(0, weight=1)

        self.fixed_xlim = (0, 20)
        self.fixed_ylim = (0, 10)

        self.toggle_fixed_axes_button_frame.grid_rowconfigure(0, weight=1)
        self.toggle_fixed_axes_button_frame.grid_rowconfigure(1, weight=1)
        self.toggle_fixed_axes_button_frame.grid_columnconfigure(0, weight=1)
        self.toggle_fixed_axes_button_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.toggle_fixed_axes_button = tk.Checkbutton(self.toggle_fixed_axes_button_frame, text="Toggle Autoscale", command=self.toggle_autoscale, font=("Helvetica", 24), height=2, width=30)
        self.toggle_fixed_axes_button.grid(row=0, column=0, padx=5, pady=5)
        self.toggle_fixed_axes_button.select()

        self.take_image_button = tk.Button(self.toggle_fixed_axes_button_frame, text="Take Image", command=self.save_plot_as_image, font=("Helvetica", 24), height=2, width=30)
        self.take_image_button.grid(row=1, column=0, padx=5, pady=5)


        self.cb = None
        self.once = False
        self.create_sliders()
        self.create_plot_controls()

        self.update_plot()

    def save_plot_as_image(self):
        # Prompt the user to select a file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save the Plot"
        )
        
        if file_path:  

            buf = io.BytesIO()
            self.fig.savefig(buf, format='png')
            buf.seek(0)

            # Save the BytesIO object to the chosen file path
            with open(file_path, 'wb') as f:
                f.write(buf.getvalue())

            buf.close()

        buf.close()

    def on_selection_integrator(self, option):
        self.selected_integration_method.set(option)
        self.toggle_integration_method.config(text=f"{option}")
        self.update_plot()

    def create_number_entry_widget(self, frame, title_text, result_text, variable_to_update, initial_value):
        

        title_label = tk.Label(frame, text=title_text, font=("Helvetica", 34))
        title_label.pack(pady=10, padx=10)

        number_entry = tk.Entry(frame, font=("Helvetica", 30), textvariable=variable_to_update)
        number_entry.pack(pady=10, padx=10)

        result_label = tk.Label(frame, text=f"{result_text} {initial_value}", font=("Helvetica", 32))
        result_label.pack(pady=10, padx=10)

        frame.pack_propagate(False)

        def display_number(event=None):

            number = variable_to_update.get()

            result_label.config(text=f"{result_text} {number}")

            self.update_plot()

        number_entry.bind("<Return>", display_number)
        
        return (title_label, number_entry, result_label)
    
    def show_hide_frame(self, widgets, show):
        # Show or hide the widgets based on the boolean 'show'
        for widget in widgets:
            if show:
                widget.pack_propagate(False)
                widget.pack(pady=10, padx=10) 
            else:
                widget.pack_forget() 


    def toggle_visibility(self):
        # Example method to toggle visibility
        self.show_hide_frame(self.frame2, True)

    def toggle_animation(self):
        self.toggle_animation_var = not self.toggle_animation_var
        self.update_plot()


    def toggle_distance_travelled_by_projectile(self):
        self.distance_travelled_by_projectile_var = not self.distance_travelled_by_projectile_var 
                
        self.update_plot()

    def distance_travelled_by_projectile(self, u_vals, theta_vals, range_vals, g):
        distances_flown = []
        for i in range(len(theta_vals)):
            d_flown =tasks.trajectory_length(u_vals[i], theta_vals[i], range_vals[i], g)
            distances_flown.append(d_flown)
        return distances_flown

    def track_mouse_position(self, event):

        x, y = event.x_root, event.y_root

        bbox = self.canvas_widget.bbox(tk.ALL)
        if bbox is None:
            print("Bounding box is None")
            return False

        plot_area_x0, plot_area_y0, plot_area_x1, plot_area_y1 = bbox


        if (plot_area_x0 <= x <= plot_area_x1) and (plot_area_y0 <= y <= plot_area_y1):
            self.in_plot = True
        else:
            self.in_plot = False

    def on_mouse_down(self, event):
        if not self.autoscale and self.in_plot == True:
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    
    def on_mouse_drag(self, event):
        if self.drag_start_x is not None and self.drag_start_y is not None:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            x_range = xlim[1] - xlim[0]
            y_range = ylim[1] - ylim[0]

            new_xlim = [xlim[0] - dx * x_range / self.canvas_widget.winfo_width(), xlim[1] - dx * x_range / self.canvas_widget.winfo_width()]
            new_ylim = [ylim[0] + dy * y_range / self.canvas_widget.winfo_height(), ylim[1] + dy * y_range / self.canvas_widget.winfo_height()]

            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)

            self.canvas.draw()

            self.drag_start_x = event.x
            self.drag_start_y = event.y


    def on_mouse_up(self, event):
        self.drag_start_x = None
        self.drag_start_y = None
        self.fixed_xlim = self.ax.get_xlim()
        self.fixed_ylim = self.ax.get_ylim()

    def on_mouse_wheel(self, event):
        
        if not self.autoscale and self.in_plot == True:
            # Determine zoom direction
            zoom_in = event.delta > 0

            # Get current axis limits
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            self.fixed_xlim = xlim
            self.fixed_ylim = ylim

            # Calculate center and range
            x_center = (xlim[1] + xlim[0]) / 2
            y_center = (ylim[1] + ylim[0]) / 2
            x_range = xlim[1] - xlim[0]
            y_range = ylim[1] - ylim[0]

            # Update range based on zoom direction
            if zoom_in:
                x_range /= self.scale_factor
                y_range /= self.scale_factor
            else:
                x_range *= self.scale_factor
                y_range *= self.scale_factor

            # Set new limits
            self.ax.set_xlim([x_center - x_range / 2, x_center + x_range / 2])
            self.ax.set_ylim([y_center - y_range / 2, y_center + y_range / 2])

            self.canvas.draw()

    def toggle_autoscale(self):
        self.autoscale = not self.autoscale
        self.fixed_xlim = self.ax.get_xlim()
        self.fixed_ylim = self.ax.get_ylim()
        if self.autoscale:
            self.ax.relim()
            self.ax.autoscale_view()
            self.update_plot()
        else:
            self.ax.set_xlim(self.fixed_xlim)
            self.ax.set_ylim(self.fixed_ylim)
            self.update_plot()
        self.canvas.draw()


    def create_sliders(self):
        
        self.sliders_frame.columnconfigure(0, weight=1)
        self.sliders_frame.columnconfigure(1, weight=1)
        self.sliders_frame.columnconfigure(2, weight=1)
        self.sliders_frame.columnconfigure(3, weight=1)

        for i in range(5):  
            self.sliders_frame.rowconfigure(i, weight=1)

        self.h_slider = self.create_slider(self.sliders_frame, 'h (m)', 0.0, 30.0, 5.0, self.update_plot, 0)
        self.u_slider = self.create_slider(self.sliders_frame, 'u (m/s)', 1.0, 100.0, 10.0, self.update_plot, 1)
        self.theta_slider = self.create_slider(self.sliders_frame, 'theta (deg)', 1.0, 90.0, 45.0, self.update_plot, 2)
        self.mass_slider = self.create_slider(self.sliders_frame, 'm (kg)', 0.01, 10.0, 0.01, self.update_plot, 3)

        self.h_slider.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.u_slider.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.theta_slider.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.mass_slider.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(1, weight=1)

        self.X_slider = self.create_XY_slider(self.buttons_frame, 'X target', 1.0, 100.0, 20.0, self.update_plot, 0)
        self.Y_slider = self.create_XY_slider(self.buttons_frame, 'Y target', 1.0, 100.0, 20.0, self.update_plot, 1)

        self.X_slider.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.Y_slider.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
    def create_slider(self, parent, label, min_val, max_val, init_val, update_func, row):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=row)

        label_widget = ttk.Label(frame, text=label, font=("Arial", 25))
        label_widget.grid(row=0, column=row, pady=(0, 10)) 

        if min_val == 0.01:
            slider_font = font.Font(size=25)
            slider = tk.Scale(frame, from_=max_val, to=min_val, orient=tk.VERTICAL, resolution=0.01, length=900, sliderlength=80, width=200, font=slider_font, troughcolor='lightblue', command=lambda val: update_func())
            slider.set(init_val)

            return slider


        slider_font = font.Font(size=25)
        slider = tk.Scale(frame, from_=max_val, to=min_val, orient=tk.VERTICAL, resolution=0.5, length=900, sliderlength=80, width=200, font=slider_font, troughcolor='lightblue', command=lambda val: update_func())
        slider.set(init_val)

        return slider
    
    def create_XY_slider(self, parent, label, min_val, max_val, init_val, update_func, row):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=row)

        label_widget = ttk.Label(frame, text=label, font=("Arial", 25))
        label_widget.grid(row=0, column=row, pady=(0, 10)) 

        slider_font = font.Font(size=25)

        slider = tk.Scale(frame, from_=max_val, to=min_val, orient=tk.VERTICAL, resolution=0.5, length=1000, sliderlength=80, width=180, font=slider_font, troughcolor='lightblue', command=lambda val: update_func())
        slider.set(init_val)

        return slider

    def create_plot_controls(self):

        self.sliders_frame.rowconfigure(1, weight=1)
        self.sliders_frame.rowconfigure(2, weight=1)

        menu_font = font.Font(size=25)
        button_font = font.Font(size=22)

        self.plot_type_var = tk.StringVar()
        self.plot_type_var.set(self.current_plot_type)

        self.plot_type_menu = tk.Menubutton(self.sliders_frame, textvariable=self.plot_type_var, relief=tk.RAISED)
        self.plot_type_menu.grid(row=1, column=0, columnspan=4, rowspan=2, padx=5, pady=5, sticky="nsew")

        plot_type_menu = tk.Menu(self.plot_type_menu, tearoff=0, font=menu_font)
        plot_types = ['Exact Model', 'Analytic Model', 'To Target Model', 'Max Range Model', 'Maxima Minima Model', 'Ball Bounces Model', 'Air Resistance Model']
        for plot_type in plot_types:
            plot_type_menu.add_command(label=plot_type, command=lambda pt=plot_type: self.on_plot_type_change(pt))
        self.plot_type_menu.config(menu=plot_type_menu, font=button_font)

        self.plot_subtype_var = tk.StringVar()
        self.plot_subtype_var.set(self.current_plot_subtype)

        self.plot_subtype_menu = tk.Menubutton(self.sliders_frame, textvariable=self.plot_subtype_var, relief=tk.RAISED)
        self.plot_subtype_menu.grid(row=3, column=0, padx=5, columnspan=4, rowspan=2, pady=5, sticky="nsew")

        self.plot_subtype_menu.config(menu=self.create_subtype_menu([]), font=button_font)

    def reset_textboxes(self):

        self.text_box1.config(text=rf'', font=("Arial", 45), height=1, width=15)
        self.text_box2.config(text=rf'', font=("Arial", 45), height=1, width=15)
        self.text_box3.config(text=rf'', font=("Arial", 45), height=1, width=15)
        self.text_box4.config(text=rf'', font=("Arial", 45), height=1, width=15)

    def on_plot_type_change(self, selected_plot_type):

        self.current_plot_type = selected_plot_type
        self.plot_type_var.set(selected_plot_type)
        #self.delete_colorbar()

        if self.current_plot_type == 'Max Range Model':
            plot_subtypes = ['user input vs max range', 'max range surface graph', 'launch elevation surface graph', 'Rg/u^2 graph', 'alpha graph']
            if self.current_plot_subtype not in plot_subtypes:
                self.current_plot_subtype = 'user input vs max range'

        elif self.current_plot_type == 'Maxima Minima Model':
            plot_subtypes = ['range vs time', 'x displacement vs y displacement']
            if self.current_plot_subtype not in plot_subtypes:
                self.current_plot_subtype = 'range vs time'

        elif self.current_plot_type == 'Air Resistance Model':
            plot_subtypes = ['y vs x', 'y vs t', 'vx vs t', 'vy vs t', 'v vs t']
            if self.current_plot_subtype not in plot_subtypes:
                self.current_plot_subtype = 'y vs x'
        else:
            plot_subtypes = []
            self.current_plot_subtype = ''

        if self.current_plot_type != 'Ball Bounces Model':
            self.animation_button_visible = False

        if self.current_plot_type != 'Air Resistance Model':
            self.integrator_button_visible = False
        else:
            self.integrator_button_visible = True

        if self.current_plot_type != 'Ball Bounces Model':
            self.N_widget_visible = False
            self.C_widget_visible = False
        else:
            self.N_widget_visible = True
            self.C_widget_visible = True

        if self.current_plot_type != 'Air Resistance Model':
            self.Cd_widget_visible = False
            self.rho_widget_visible = False
            self.cs_area_widget_visible = False
        else:
            self.Cd_widget_visible = True
            self.rho_widget_visible = True
            self.cs_area_widget_visible = True

        self.reset_textboxes()

        # Update the plot subtype menu
        self.plot_subtype_menu.config(menu=self.create_subtype_menu(plot_subtypes))
        self.plot_subtype_var.set(self.current_plot_subtype)
        self.update_plot()

    def on_plot_subtype_change(self, selected_plot_subtype):
        self.current_plot_subtype = selected_plot_subtype
        self.plot_subtype_var.set(selected_plot_subtype)

        self.reset_textboxes()

        #self.delete_colorbar()
        self.update_plot()

    def create_subtype_menu(self, subtypes):
        menu_font = font.Font(size=22)
        subtype_menu = tk.Menu(self.plot_subtype_menu, tearoff=0, font=menu_font)
        for subtype in subtypes:
            subtype_menu.add_command(label=subtype, command=lambda ps=subtype: self.on_plot_subtype_change(ps))
        return subtype_menu
    
    """def delete_colorbar(self):
        if hasattr(self, 'cb') and self.cb is not None:
            try:
                self.cb.remove()
                self.cb = None  
            except Exception as e:
                print(self.cb)
                print(f"An error occurred while removing the colorbar: {e}")
        else:
            print("toioeio")"""
    


    def update_plot(self):
        self.ax.clear()

        if self.animation_button_visible == False:
            self.toggle_animation_button.grid_forget()

        if self.integrator_button_visible == False:
            self.toggle_integration_method.grid_forget()
        else:
            self.toggle_integration_method.grid(row = 0, column=0, padx=5, pady=5, stick='nsew')

        self.show_hide_frame(self.n_widget, self.N_widget_visible)
        self.show_hide_frame(self.c_widget, self.C_widget_visible)
        self.show_hide_frame(self.Cd_widget, self.Cd_widget_visible)
        self.show_hide_frame(self.rho_widget, self.rho_widget_visible)
        self.show_hide_frame(self.cs_area_widget, self.cs_area_widget_visible)


        h = self.h_slider.get()
        u = self.u_slider.get()
        theta = self.theta_slider.get()
        mass = self.mass_slider.get()
        X = self.X_slider.get()
        Y = self.Y_slider.get()
        g = self.g.get()
        step = 1000
        dt = 1/1000


        if self.current_plot_type == 'Exact Model':
            x_pos, y_pos, range_ = tasks.task1(h, u, theta, dt, g)
            self.ax.plot(x_pos, y_pos)
            self.ax.set_title('y displacement vs x displacement', fontsize=28)

            self.ax.set_xlabel('X Displacement', fontsize=22)
            self.ax.set_ylabel('Y Displacement', fontsize=22)

            if self.distance_travelled_by_projectile_var == True:

                distance_travelled_by_projectile = self.distance_travelled_by_projectile([u], [np.deg2rad(theta)], [range_], g)

                self.d_travelled_by_projectile_text = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile $\approx$ {round(distance_travelled_by_projectile[0], 2)} m', fontsize=24,
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),transform=self.ax.transAxes)
        
            if self.distance_travelled_by_projectile_var == False:
                    if hasattr(self, 'd_travelled_by_projectile_text'):
                        self.d_travelled_by_projectile_text.remove()
                        delattr(self, 'd_travelled_by_projectile_text')


            self.ax.grid()


        elif self.current_plot_type == 'Analytic Model':
            x_pos, y_pos, x_a, y_a, tof, r = tasks.task2(h, u, theta, step, g)
            self.ax.plot(x_pos, y_pos)
            self.ax.plot(x_a, y_a, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=20) 
            
            labels_font = font.Font(size=22)
            
            self.text_box1.config(text=rf'Range {round(r, 2)} meters', font=("Arial", 35), height=1, width=15)
            self.text_box2.config(text=rf'TOF {round(tof, 2)} seconds', font=("Arial", 35), height=1, width=15)

            self.text_box3.config(height=1, width=15)
            self.text_box4.config(height=1, width=15)

            self.ax.set_title('y displacement vs x displacement', fontsize=28)

            self.ax.set_xlabel('X Displacement', fontsize=22)
            self.ax.set_ylabel('Y Displacement', fontsize=22)

            if self.distance_travelled_by_projectile_var == True:

                distance_travelled_by_projectile = self.distance_travelled_by_projectile([u], [np.deg2rad(theta)], [r], g)

                self.d_travelled_by_projectile_text = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile $\approx$ {round(distance_travelled_by_projectile[0], 2)} m', fontsize=24,
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),transform=self.ax.transAxes)
            else: 
                if hasattr(self, 'd_travelled_by_projectile_text'):
                    self.d_travelled_by_projectile_text.remove()
                    delattr(self, 'd_travelled_by_projectile_text')
 

            self.ax.legend(loc='upper right', fontsize=28)
            self.ax.grid()




        elif self.current_plot_type == 'To Target Model':

            labels_font = font.Font(size=22)


            u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, theta_deg_max_range, range_min_u, range_high, range_low, range_max, x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low, x_pos_bounding, y_pos_bounding, x_pos_max_range, y_pos_max_range = tasks.task5(h, u, step, g, X, Y) 

            target, = self.ax.plot(X, Y, 'o', label=rf'Target at $\approx$ ({round(X, 2)}, {round(Y, 2)})', markersize=20, color="orange") 

            min_u_line, = self.ax.plot(x_pos_min_u, y_pos_min_u, 'r--', label='Minimum u') 
            high_line, = self.ax.plot(x_pos_u_high, y_pos_u_high, 'b-', label='High Ball') 
            low_line, = self.ax.plot(x_pos_u_low, y_pos_u_low, 'g-', label='Low Ball') 
            bounding_line, = self.ax.plot(x_pos_bounding, y_pos_bounding, color='purple', label='Bounding Parabola') 
            max_range_line, = self.ax.plot(x_pos_max_range, y_pos_max_range, color='saddlebrown', label='max range') 

            self.ax.set_title('y displacement vs x displacement', fontsize=28)

            self.ax.set_xlabel('X Displacement', fontsize=22)
            self.ax.set_ylabel('Y Displacement', fontsize=22)

            self.text_box1.config(text=f'Theta (minimum u):\n {round(theta_deg_min_u, 2)} deg', font=("Arial", 34), height=1, width=15)
            self.text_box2.config(text=f'Theta (high ball):\n {round(theta_deg_user_u_high, 2)} deg\nTheta (low ball):\n {round(theta_deg_user_u_low, 2)} deg', font=("Arial", 18), height=1, width=15)
            self.text_box3.config(text=f'Theta (maximum range):\n {round(theta_deg_max_range, 2)} deg', font=("Arial", 34), height=1, width=15)
            self.text_box4.config(text=f'Minimum u:\n {round(u_min, 2)} m/s', font=("Arial", 34), height=1, width=15)

            if self.distance_travelled_by_projectile_var == True:

                distance_travelled_by_projectile = self.distance_travelled_by_projectile([u_min, u, u, u], [np.deg2rad(theta_deg_min_u), np.deg2rad(theta_deg_user_u_high), np.deg2rad(theta_deg_user_u_low), np.deg2rad(theta_deg_max_range)], [range_min_u, range_high, range_low, range_max], g)

                self.d_travelled_by_projectile_text1 = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile at minimum u $\approx$ {round(distance_travelled_by_projectile[0], 2)} m', fontsize=24, color='red',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                self.d_travelled_by_projectile_text2 = self.ax.text(0.03, 0.12, rf'Distance travelled by projectile (high) $\approx$ {round(distance_travelled_by_projectile[1], 2)} m', fontsize=24, color='blue',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                self.d_travelled_by_projectile_text3 = self.ax.text(0.03, 0.19, rf'Distance travelled by projectile (low) $\approx$ {round(distance_travelled_by_projectile[2], 2)} m', fontsize=24, color='green',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                self.d_travelled_by_projectile_text4 = self.ax.text(0.03, 0.26, rf'Distance travelled by projectile (max range) $\approx$ {round(distance_travelled_by_projectile[3], 2)} m', fontsize=24, color='saddlebrown',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                
            else: 
                if hasattr(self, 'd_travelled_by_projectile_text1'):
                    self.d_travelled_by_projectile_text1.remove()
                    delattr(self, 'd_travelled_by_projectile_text1')
                if hasattr(self, 'd_travelled_by_projectile_text2'):
                    self.d_travelled_by_projectile_text2.remove()
                    delattr(self, 'd_travelled_by_projectile_text2')
                if hasattr(self, 'd_travelled_by_projectile_text3'):
                    self.d_travelled_by_projectile_text3.remove()
                    delattr(self, 'd_travelled_by_projectile_text3')
                if hasattr(self, 'd_travelled_by_projectile_text4'):
                    self.d_travelled_by_projectile_text4.remove()
                    delattr(self, 'd_travelled_by_projectile_text4') 

            self.ax.legend(loc='upper right', fontsize=28)
            self.ax.grid()

        elif self.current_plot_type == 'Max Range Model':         


            if self.current_plot_subtype == 'user input vs max range':
            
                x_pos, y_pos, x_pos_max_range, y_pos_max_range, x_a, y_a, x_a_max_r, y_a_max_r, range_, range_max, tof, tof_max_r, theta, theta_max_r = tasks.task4(h, u, theta, step, g)
                self.ax.plot(x_pos, y_pos, '-b', label='User Input')
                self.ax.plot(x_pos_max_range, y_pos_max_range, '--r', label='Max Range')
                self.ax.plot(x_a, y_a, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=20) 
                self.ax.plot(x_a_max_r, y_a_max_r, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=20) 
                
                labels_font = font.Font(size=22)
                
                self.text_box1.config(text=f'Range (user input):\n{round(range_, 2)} meters\nRange (maximum range):\n{round(range_max, 2)} meters', font=("Arial", 20), height=1, width=15)
                self.text_box2.config(text=f'TOF (user input):\n{round(tof, 2)} seconds\nTOF (maximum range):\n{round(tof_max_r, 2)} seconds', font=("Arial", 20), height=1, width=15)
                self.text_box3.config(text=f'Theta (user):\n{round(theta, 2)} deg', font=("Arial", 24), height=1, width=15)
                self.text_box4.config(text=f'Theta (max range):\n{round(theta_max_r, 2)} deg', font=("Arial", 24), height=1, width=15)


                self.ax.set_title('y displacement vs x displacement', fontsize=28)

                self.ax.set_xlabel('X Displacement', fontsize=22)
                self.ax.set_ylabel('Y Displacement', fontsize=22)

                if self.distance_travelled_by_projectile_var == True:

                    distance_travelled_by_projectile = self.distance_travelled_by_projectile([u, u], [np.deg2rad(theta), np.deg2rad(theta_max_r)], [range_, range_max], g)

                    self.d_travelled_by_projectile_text1 = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile (user input)$\approx$ {round(distance_travelled_by_projectile[0], 2)} m', fontsize=24, color='blue',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                    self.d_travelled_by_projectile_text2 = self.ax.text(0.03, 0.15, rf'Distance travelled by projectile (max range) $\approx$ {round(distance_travelled_by_projectile[1], 2)} m', fontsize=24, color='red',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)     
                else:
                    if hasattr(self, 'd_travelled_by_projectile_text1'):
                        self.d_travelled_by_projectile_text.remove()
                        delattr(self, 'd_travelled_by_projectile_text2')     

                self.ax.legend(loc='upper right', fontsize=28)
                self.ax.grid()
                

            elif self.current_plot_subtype == 'max range surface graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im1 = self.ax.imshow(max_range, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Max Range (m)', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

            elif self.current_plot_subtype == 'launch elevation surface graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im2 = self.ax.imshow(launch_elevation, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Theta (degrees)', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

            elif self.current_plot_subtype == 'Rg/u^2 graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im3 = self.ax.imshow(Rg_u2_values, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Rg/u²', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

            elif self.current_plot_subtype == 'alpha graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                for i in range(len(Rg_u2_theta_values)):
                    self.ax.plot(theta_values, Rg_u2_theta_values[i], label=rf'$\alpha$ = {alpha_values[i]}')
                self.ax.set_title('Rg/u² vs Theta', fontsize=28)
                self.ax.set_xlabel('Theta (degrees)', fontsize=22)
                self.ax.set_ylabel('Rg/u²', fontsize=22)
                self.ax.legend(loc='upper right', fontsize=28)
                self.ax.grid(True)


        elif self.current_plot_type == 'Maxima Minima Model':

            task6 = Tasks.Task7()

            theta_degrees = np.arange(45, 90, 5)

            if self.current_plot_subtype == 'range vs time':

                theta_degrees = np.arange(45, 90, 5)

                for theta_deg in theta_degrees:
                    theta = np.deg2rad(theta_deg)
                    range_ = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*0)/(np.square(u)))) 
                    tof = range_ / (u*np.cos(theta))
                    ts = np.arange(0, tof, dt)
                    range_values = task6.r(u, theta, g, ts)
                    
                    t_max = task6.compute_t_max(u, theta, g)
                    t_min = task6.compute_t_min(u, theta, g)

                    if t_max is not None and t_min is not None:
                        range_max = task6.r(u, theta, g, t_max) 
                        range_min = task6.r(u, theta, g, t_min) 

                        self.ax.scatter([t_max], [range_max], color='blue', zorder=3, s=100, marker='X', label=rf'Maxima at at $\approx$ ({round(t_max, 2)}, {round(range_max, 2)})')
                        self.ax.scatter([t_min], [range_min], color='red', zorder=3, s=100, marker='X', label=rf'Minima at at $\approx$ ({round(t_min, 2)}, {round(range_min, 2)})')

                    self.ax.plot(ts, range_values, label=f'θ = {theta_deg}°')

                self.ax.legend(loc='upper left', fontsize=22)
                self.ax.set_title("Range vs Time", fontsize=28)
                self.ax.set_xlabel('Time (s)', fontsize=22)
                self.ax.set_ylabel('Range (m)', fontsize=22)
                self.ax.grid(True)     

            elif self.current_plot_subtype == 'x displacement vs y displacement':

                for theta_deg in theta_degrees:
                    theta = np.deg2rad(theta_deg)
                    range_ = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*h)/(np.square(u)))) 
                    tof = range_ / (u*np.cos(theta))
                    ts = np.arange(0, tof, dt)

                    x_positions = []
                    y_positions = []

                    for t in ts:
                        x, y = task6.projectile_motion(u, theta, g, t)
                        x_positions.append(x)
                        y_positions.append(y)

                    t_max = task6.compute_t_max(u, theta, g)
                    t_min = task6.compute_t_min(u, theta, g)

                    if t_max is not None and t_min is not None:
                        x_max, y_max = task6.projectile_motion(u, theta, g, t_max)
                        x_min, y_min = task6.projectile_motion(u, theta, g, t_min)
                        self.ax.scatter([x_max], [y_max], color='blue', zorder=3, s=100, marker='X', label=rf'Maxima at at $\approx$ ({round(x_max, 2)}, {round(y_max), 2})')
                        self.ax.scatter([x_min], [y_min], color='red', zorder=3, s=100, marker='X', label=rf'Maxima at at $\approx$ ({round(x_min, 2)}, {round(y_min), 2})')

                    self.ax.plot(x_positions, y_positions, label=f'θ = {theta_deg}°')

                self.ax.set_title("Displacement", fontsize=28)
                self.ax.set_xlabel('x displacement (m)', fontsize=22)
                self.ax.set_ylabel('y displacement (m)', fontsize=22)
                self.ax.legend(fontsize=28)
                self.ax.grid(True)
 
        elif self.current_plot_type == 'Ball Bounces Model':
 
            self.animation_button_visible = True

            if self.animation_button_visible == True:
                self.toggle_animation_button.grid(row = 0, column=0, padx=5, pady=5, stick='nsew')

            N = self.N.get() - 1   
            C = self.C.get()  
            dt = 1/25  

            t, x, y, vx, vy = tasks.task8(h, u, theta, dt, g, N, C)

            self.ax.set_xlim(0, np.max(x) * 1.1)
            self.ax.set_ylim(0, np.max(y) * 1.1)

            self.ax.set_xlabel('Distance (m)')
            self.ax.set_ylabel('Height (m)')
            self.ax.set_title('Projectile Trajectory Animation with Bounces (Verlet Method)')

            self.text_box1.config(text=f'Range:\n{round(x[-1], 2)} meters', font=("Arial", 37), height=1, width=15)
            self.text_box2.config(text=f'TOF:\n{round(t[-1], 2)} seconds', font=("Arial", 37), height=1, width=15)

            if self.toggle_animation_var == True:
                line, = self.ax.plot([], [], '.', lw=0.1)

                def update(frame):
                    line.set_data(x[:frame], y[:frame])
                    return line,

                ani = FuncAnimation(self.fig, update, frames=len(t), interval=1, blit=True)

            else:
                self.ax.plot(x, y)


        elif self.current_plot_type == 'Air Resistance Model':

            C_d = self.Cd.get()  # Drag coefficient
            rho = self.rho.get()  # Air density (kg/m^3)
            cs_area = self.cs_area.get()  # Cross-sectional area (m^2)
            dt = 0.01 
            v0 = u  
            m = mass
            angle = theta
           
            task9 = Tasks.Task9(g, dt, rho, C_d, cs_area, m)

            if self.selected_integration_method.get() == "Verlet":
                dnr, xnr, ynr, vnr, vxnr, vynr, tnr  = task9.verlet_without_air_resistance(v0, h, angle)
                dr, xr, yr, vr, vxr, vyr, tr = task9.verlet_with_air_resistance(v0, h, C_d, rho, cs_area, m, angle)

                if self.distance_travelled_by_projectile_var == True:

                    self.d_travelled_by_projectile_text1 = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile with no air resistance (Verlet) $\approx$ {round(dnr, 2)} m', fontsize=24, color='blue',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                    self.d_travelled_by_projectile_text2 = self.ax.text(0.03, 0.15, rf'Distance travelled by projectile with air resistance (Verlet) $\approx$ {round(dr, 2)} m', fontsize=24, color='red',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)     
                else:
                    if hasattr(self, 'd_travelled_by_projectile_text1'):
                        self.d_travelled_by_projectile_text1.remove()
                        delattr(self, 'd_travelled_by_projectile_text1')   
                    if hasattr(self, 'd_travelled_by_projectile_text2'):
                        self.d_travelled_by_projectile_text2.remove()
                        delattr(self, 'd_travelled_by_projectile_text2')   

                self.text_box1.config(text=f'Range (no air resistance):\n{round(xnr[-1], 2)} meters\n(Verlet)', font=("Arial", 30), height=1, width=15)
                self.text_box2.config(text=f'TOF (no air resistance):\n{round(tnr[-1], 2)} seconds\n(Verlet)', font=("Arial", 30), height=1, width=15)
                self.text_box3.config(text=f'Range (air resistance):\n{round(xr[-1], 2)} meters\n(Verlet)', font=("Arial", 30), height=1, width=15)
                self.text_box4.config(text=f'TOF (air resistance):\n{round(tr[-1], 2)} seconds\n(Verlet)', font=("Arial", 30), height=1, width=15)

            if self.selected_integration_method.get() == "RK4":
                xnr, ynr, vnr, vxnr, vynr, tnr, dnr  = task9.trajectory_without_air_resistance(u, angle, h)
                xr, yr, vr, vxr, vyr, tr, dr = task9.trajectory_with_air_resistance(u, angle, h)

                if self.distance_travelled_by_projectile_var == True:

                    self.d_travelled_by_projectile_text1 = self.ax.text(0.03, 0.05, rf'Distance travelled by projectile with no air resistance (RK4) $\approx$ {round(dnr, 2)} m', fontsize=24, color='blue',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)
                    self.d_travelled_by_projectile_text2 = self.ax.text(0.03, 0.15, rf'Distance travelled by projectile with air resistance (RK4) $\approx$ {round(dr, 2)} m', fontsize=24, color='red',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=self.ax.transAxes)     
                else:
                    if hasattr(self, 'd_travelled_by_projectile_text1'):
                        self.d_travelled_by_projectile_text1.remove()
                        delattr(self, 'd_travelled_by_projectile_text1')   
                    if hasattr(self, 'd_travelled_by_projectile_text2'):
                        self.d_travelled_by_projectile_text2.remove()
                        delattr(self, 'd_travelled_by_projectile_text2')   

                self.text_box1.config(text=f'Range (no air resistance):\n{round(xnr[-1], 2)} meters\n(RK4)', font=("Arial", 30), height=1, width=15)
                self.text_box2.config(text=f'TOF (no air resistance):\n{round(tnr[-1], 2)} seconds\n(RK4)', font=("Arial", 30), height=1, width=15)
                self.text_box3.config(text=f'Range (air resistance):\n{round(xr[-1], 2)} meters\n(RK4)', font=("Arial", 30), height=1, width=15)
                self.text_box4.config(text=f'TOF (air resistance):\n{round(tr[-1], 2)} seconds\n(RK4)', font=("Arial", 30), height=1, width=15)

            if self.current_plot_subtype == 'y vs x':

                self.ax.plot(xnr, ynr, label='No air R', linestyle='-', color='blue')
                self.ax.plot(xr, yr, label='Air R', linestyle='--', color='red')
                self.ax.set_xlabel('Distance (m)', fontsize=22)
                self.ax.set_ylabel('Height (m)', fontsize=22)
                self.ax.set_title('X vs Y', fontsize=28)
                self.ax.legend(fontsize=28)
                self.ax.grid(True)
            
            elif self.current_plot_subtype == 'y vs t':

                self.ax.plot(tnr, ynr, label='No air R', linestyle='-', color='blue')
                self.ax.plot(tr, yr, label='Air R', linestyle='--', color='red')
                self.ax.set_xlabel('Time (s)', fontsize=22)
                self.ax.set_ylabel('Height (m)', fontsize=22)
                self.ax.set_title('Y vs T', fontsize=28)
                self.ax.legend(fontsize=28)       
                self.ax.grid(True)

            elif self.current_plot_subtype == 'vx vs t':

                self.ax.plot(tnr, vxnr, label='No air R', linestyle='-', color='blue')
                self.ax.plot(tr, vxr, label='Air R', linestyle='--', color='red')
                self.ax.set_xlabel('Time (s)', fontsize=22)
                self.ax.set_ylabel('Velocity in X (m/s)', fontsize=22)
                self.ax.set_title('VX vs T', fontsize=28)
                self.ax.legend(fontsize=28) 
                self.ax.grid(True)

            elif self.current_plot_subtype == 'vy vs t':
            
                self.ax.plot(tnr, vynr, label='No air R', linestyle='-', color='blue')
                self.ax.plot(tr, vyr, label='Air R', linestyle='--', color='red')
                self.ax.set_xlabel('Time (s)', fontsize=22)
                self.ax.set_ylabel('Velocity in Y (m/s)', fontsize=22)
                self.ax.set_title('VY vs T', fontsize=28)
                self.ax.legend(fontsize=28) 
                self.ax.grid(True)

            elif self.current_plot_subtype == 'v vs t':

                self.ax.plot(tnr, vnr, label='No air R', linestyle='-', color='blue')
                self.ax.plot(tr, vr, label='Air R', linestyle='--', color='red')
                self.ax.set_xlabel('Time (s)', fontsize=22)
                self.ax.set_ylabel('Velocity (m/s)', fontsize=22)
                self.ax.set_title('V vs T', fontsize=28)
                self.ax.legend(fontsize=28)     
                self.ax.grid(True)            

        if self.autoscale and self.current_plot_type != 'Ball Bounces Model':
            self.ax.autoscale()
        if not self.autoscale:
            self.ax.set_xlim(self.fixed_xlim)
            self.ax.set_ylim(self.fixed_ylim)


        self.canvas.draw()


    def exit_app(self, event=None):
        sys.exit() 


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
