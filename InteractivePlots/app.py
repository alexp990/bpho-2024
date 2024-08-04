import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
from tkinter import font
from tasks import Tasks

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

        self.start_x = None
        self.start_y = None
        self.scale_factor = 1.1
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.root.bind("<Button-1>", self.on_mouse_down)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind("<MouseWheel>", self.on_mouse_wheel)

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

        self.data_frame_above_sliders = tk.Frame(self.root, borderwidth=2, relief="solid", background='blue')
        self.top_left_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.sliders_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.buttons_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.information_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.utils_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        self.toggle_fixed_axes_button_frame = tk.Frame(self.root, borderwidth=2, relief="solid", background='red')

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

        self.take_image_button = tk.Button(self.toggle_fixed_axes_button_frame, text="Take Image", command=self.toggle_autoscale, font=("Helvetica", 24), height=2, width=30)
        self.take_image_button.grid(row=1, column=0, padx=5, pady=5)

        self.cb = None
        self.create_sliders()
        self.create_plot_controls()

        self.update_plot()

    def on_mouse_down(self, event):
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
        
        if not self.autoscale:
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
        self.mass_slider = self.create_slider(self.sliders_frame, 'm (kg)', 1.0, 40.0, 20.0, self.update_plot, 3)

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

        self.X_slider = self.create_XY_slider(self.buttons_frame, 'X target', 0.0, 100.0, 20.0, self.update_plot, 0)
        self.Y_slider = self.create_XY_slider(self.buttons_frame, 'Y target', 0.0, 100.0, 20.0, self.update_plot, 1)

        self.X_slider.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.Y_slider.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
    def create_slider(self, parent, label, min_val, max_val, init_val, update_func, row):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=row)

        label_widget = ttk.Label(frame, text=label, font=("Arial", 25))
        label_widget.grid(row=0, column=row, pady=(0, 10)) 

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
        plot_types = ['Exact Model', 'Analytic Model', 'To Target Model', 'Max Range Model', 'Distance Travelled Model', 'Maxima Minima Model', 'Ball Bounces Model', 'Air Resistance Model']
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

        # Determine the subtypes based on the selected plot type
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

        self.reset_textboxes()

        # Update the plot subtype menu
        self.plot_subtype_menu.config(menu=self.create_subtype_menu(plot_subtypes))
        self.plot_subtype_var.set(self.current_plot_subtype)
        self.update_plot()

    def on_plot_subtype_change(self, selected_plot_subtype):
        self.current_plot_subtype = selected_plot_subtype
        self.plot_subtype_var.set(selected_plot_subtype)
        self.reset_textboxes()
        self.update_plot()

    def create_subtype_menu(self, subtypes):
        menu_font = font.Font(size=22)
        subtype_menu = tk.Menu(self.plot_subtype_menu, tearoff=0, font=menu_font)
        for subtype in subtypes:
            subtype_menu.add_command(label=subtype, command=lambda ps=subtype: self.on_plot_subtype_change(ps))
        return subtype_menu

    


    def update_plot(self):
        self.ax.clear()

        h = self.h_slider.get()
        u = self.u_slider.get()
        theta = self.theta_slider.get()
        mass = self.mass_slider.get()
        X = self.X_slider.get()
        Y = self.Y_slider.get()

        if self.current_plot_type == 'Exact Model':
            x_pos, y_pos = tasks.task1(h, u, theta, dt=1/1000, g=9.81)
            self.ax.plot(x_pos, y_pos)
            self.ax.set_title('y displacement vs x displacement', fontsize=28)

            self.ax.set_xlabel('X Displacement', fontsize=22)
            self.ax.set_ylabel('Y Displacement', fontsize=22)

            self.ax.grid()


        elif self.current_plot_type == 'Analytic Model':
            x_pos, y_pos, x_a, y_a, tof, r = tasks.task2(h, u, theta, step=1000, g=9.81)
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

            self.ax.legend(loc='upper right', fontsize=28)
            self.ax.grid()



        elif self.current_plot_type == 'To Target Model':

            labels_font = font.Font(size=22)

            step = 1000
            g = 9.81

            u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, theta_deg_max_range, range_min_u, x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low, x_pos_bounding, y_pos_bounding, x_pos_max_range, y_pos_max_range = tasks.task5(h, u, step, g, X, Y) 

            target, = self.ax.plot(X, Y, 'o', label=rf'Target at $\approx$ ({round(X, 2)}, {round(Y, 2)})', markersize=20, color="orange") 

            min_u_line, = self.ax.plot(x_pos_min_u, y_pos_min_u, 'r--', label='Minimum u') 
            high_line, = self.ax.plot(x_pos_u_high, y_pos_u_high, 'b-', label='High Ball') 
            low_line, = self.ax.plot(x_pos_u_low, y_pos_u_low, 'g-', label='Low Ball') 
            bounding_line, = self.ax.plot(x_pos_bounding, y_pos_bounding, color='purple', label='Bounding Parabola') 
            max_range_line, = self.ax.plot(x_pos_max_range, y_pos_max_range, color='saddlebrown', label='max range') 

            self.ax.set_title('y displacement vs x displacement', fontsize=28)

            self.ax.set_xlabel('X Displacement', fontsize=22)
            self.ax.set_ylabel('Y Displacement', fontsize=22)

            self.text_box1.config(text=f'Theta (minimum u):\n {round(theta_deg_min_u, 2)} deg', font=("Arial", 30), height=1, width=15)
            self.text_box2.config(text=f'Theta (high ball):\n {round(theta_deg_user_u_high, 2)} deg\nTheta (low ball):\n {round(theta_deg_user_u_low, 2)} deg', font=("Arial", 30), height=1, width=15)
            self.text_box3.config(text=f'Theta (maximum range):\n {round(theta_deg_max_range, 2)} deg', font=("Arial", 30), height=1, width=15)
            self.text_box4.config(text=f'Minimum u:\n {round(u_min, 2)} m/s', font=("Arial", 30), height=1, width=15)

            self.ax.legend(loc='upper right', fontsize=28)
            self.ax.grid()

        elif self.current_plot_type == 'Max Range Model':


            if self.current_plot_subtype == 'user input vs max range':
            
                x_pos, y_pos, x_pos_max_range, y_pos_max_range, x_a, y_a, x_a_max_r, y_a_max_r, range_, range_max, tof, tof_max_r, theta, theta_max_r = tasks.task4(h, u, theta, step=1000, g=9.81)
                self.ax.plot(x_pos, y_pos)
                self.ax.plot(x_pos_max_range, y_pos_max_range)
                self.ax.plot(x_a, y_a, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=20) 
                self.ax.plot(x_a_max_r, y_a_max_r, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=20) 
                
                labels_font = font.Font(size=22)
                
                self.text_box1.config(text=f'Range (user input):\n{round(range_, 2)} meters\nRange (maximum range):\n{round(range_max, 2)} meters', font=("Arial", 24), height=1, width=15)
                self.text_box2.config(text=f'TOF (user input):\n{round(tof, 2)} seconds\nTOF (maximum range):\n{round(tof_max_r, 2)} seconds', font=("Arial", 24), height=1, width=15)
                self.text_box3.config(text=f'Theta (user):\n{round(theta, 2)} deg', font=("Arial", 30), height=1, width=15)
                self.text_box4.config(text=f'Theta (max range):\n{round(theta_max_r, 2)} deg', font=("Arial", 30), height=1, width=15)


                self.ax.set_title('y displacement vs x displacement', fontsize=28)

                self.ax.set_xlabel('X Displacement', fontsize=22)
                self.ax.set_ylabel('Y Displacement', fontsize=22)

                self.ax.legend(loc='upper right', fontsize=28)
                self.ax.grid()

            elif self.current_plot_subtype == 'max range surface graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im1 = self.ax.imshow(max_range, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Max Range (m)', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

                self.cb = self.fig.colorbar(im1, ax=self.ax)

            elif self.current_plot_subtype == 'launch elevation surface graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im2 = self.ax.imshow(launch_elevation, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Theta (degrees)', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

                self.cb = self.fig.colorbar(im2, ax=self.ax)

            elif self.current_plot_subtype == 'Rg/u^2 graph':

                max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values = tasks.task4_surface_plots()

                im3 = self.ax.imshow(Rg_u2_values, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
                self.ax.set_title('Rg/u²', fontsize=28)
                self.ax.set_xlabel('Initial Velocity u (m/s)', fontsize=22)
                self.ax.set_ylabel('Initial Height h (m)', fontsize=22)

                self.cb = self.fig.colorbar(im3, ax=self.ax)

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
            if self.current_plot_subtype == 'range vs time':
                x = np.linspace(0, 10, 100)
                y = np.cos(x)
                self.ax.plot(x, y)
                self.ax.set_title('Range vs Time')

        elif self.current_plot_type == 'Air Resistance Model':
            if self.current_plot_subtype == 'y vs x':
                x = np.linspace(0, 10, 100)
                y = np.tan(x)
                self.ax.plot(x, y)
                self.ax.set_title('Y vs X')

        if self.autoscale:
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
