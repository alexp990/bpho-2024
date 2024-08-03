from tokenize import PlainToken
from tasks import Tasks 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

tsks = Tasks()

def plot_task_1(h, u, theta, dt, g):

    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.22)

    x_pos, y_pos = tsks.task1(h, u, theta, dt, g)

    line, = ax1.plot(x_pos, y_pos, 'r-') 
    ax1.set_title('Exact Model')
    ax1.set_xlabel('x displacement (m)')

    axcolor = 'lightgoldenrodyellow'
    ax_h = plt.axes([0.2, 0.01, 0.65, 0.04], facecolor=axcolor)
    ax_u = plt.axes([0.2, 0.045, 0.65, 0.04], facecolor=axcolor)
    ax_theta = plt.axes([0.2, 0.075, 0.65, 0.04], facecolor=axcolor)
    ax_g = plt.axes([0.2, 0.105, 0.65, 0.04], facecolor=axcolor)

    s_h = Slider(ax_h, 'Height (h)', 0.0, 50.0, valinit=h)
    s_u = Slider(ax_u, 'Initial Velocity (u)', 0.0, 100.0, valinit=u)
    s_theta = Slider(ax_theta, 'Angle (theta)', 0.0, 90, valinit=theta)
    s_g = Slider(ax_g, 'Gravity (g)', 0.0, 20.0, valinit=g)

    autoscale_x = True
    autoscale_y = True

    ax1.grid(True)

    ax1.relim()
    ax1.autoscale_view()

    def update(val):
        h = s_h.val
        u = s_u.val
        theta = s_theta.val
        g = s_g.val
        
        x_pos, y_pos = tsks.task1(h, u, theta, dt, g)
        line.set_xdata(x_pos)
        line.set_ydata(y_pos)
        
        ax1.relim()
        ax1.autoscale_view()

        fig.canvas.draw_idle()

    s_h.on_changed(update)
    s_u.on_changed(update)
    s_theta.on_changed(update)
    s_g.on_changed(update)

    plt.show()

def plot_task_2(h, u, theta, step, g):

    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.22)

    x_pos, y_pos, x_a, y_a, tof, r = tsks.task2(h, u, theta, step, g)

    line, = ax1.plot(x_pos, y_pos, 'r-') 
    ax1.set_title('Analytic Model')
    ax1.set_xlabel('x displacement (m)')
    ax1.set_ylabel('y displacement (m)')

    apogee, = ax1.plot(x_a, y_a, 'o', label=rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})', markersize=7) 

    axcolor = 'lightgoldenrodyellow'
    ax_h = plt.axes([0.2, 0.01, 0.65, 0.04], facecolor=axcolor)
    ax_u = plt.axes([0.2, 0.045, 0.65, 0.04], facecolor=axcolor)
    ax_theta = plt.axes([0.2, 0.075, 0.65, 0.04], facecolor=axcolor)
    ax_g = plt.axes([0.2, 0.105, 0.65, 0.04], facecolor=axcolor)

    s_h = Slider(ax_h, 'Height (h)', 0.0, 50.0, valinit=h)
    s_u = Slider(ax_u, 'Initial Velocity (u)', 0.0, 100.0, valinit=u)
    s_theta = Slider(ax_theta, 'Angle (theta)', 0.0, 90, valinit=theta)
    s_g = Slider(ax_g, 'Gravity (g)', 0.0, 20.0, valinit=g)

    tof_text = ax1.text(0.03, 0.05, rf'TOF $\approx$ {round(tof, 2)} seconds', fontsize=12,
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),transform=ax1.transAxes)
    range_text = ax1.text(0.03, 0.15, rf'Range $\approx$ {round(r, 2)} meters', fontsize=12,
                      bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'), transform=ax1.transAxes)
    
    ax1.relim()
    ax1.autoscale_view()

    ax1.grid(True)

    autoscale_x = True
    autoscale_y = True

    def update(val):
        h = s_h.val
        u = s_u.val
        theta = s_theta.val
        g = s_g.val
        
        x_pos, y_pos, x_a, y_a, tof, r = tsks.task2(h, u, theta, step, g)

        line.set_xdata(x_pos)
        line.set_ydata(y_pos)

        apogee.set_data([x_a], [y_a])
        label = rf'Apogee at $\approx$ ({round(x_a, 2)}, {round(y_a, 2)})'
        apogee.set_label(label)

        ax1.legend()
        
        tof_text.set_text(rf'TOF $\approx$ {round(tof, 2)} seconds')
        range_text.set_text(rf'Range $\approx$ {round(r, 2)} meters')
        
        ax1.relim()
        ax1.autoscale_view()
        
        ax1.autoscale()

        fig.canvas.draw_idle()

    s_h.on_changed(update)
    s_u.on_changed(update)
    s_theta.on_changed(update)
    s_g.on_changed(update)

    ax1.legend()

    plt.show()

def plot_task_3_and_5(h, user_u, step, g, X, Y):

    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.24)

    u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, theta_deg_max_range, range_min_u, x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low, x_pos_bounding, y_pos_bounding, x_pos_max_range, y_pos_max_range = tsks.task5(h, u, step, g, X, Y)       

    min_u_line, = ax1.plot(x_pos_min_u, y_pos_min_u, 'r--') 
    high_line, = ax1.plot(x_pos_u_high, y_pos_u_high, 'b-') 
    low_line, = ax1.plot(x_pos_u_low, y_pos_u_low, 'g-') 
    bounding_line, = ax1.plot(x_pos_bounding, y_pos_bounding, color='purple') 
    max_range_line, = ax1.plot(x_pos_max_range, y_pos_max_range, color='saddlebrown') 

    ax1.set_title('To Target')
    ax1.set_xlabel('x displacement (m)')
    ax1.set_ylabel('y displacement (m)')

    axcolor = 'lightgoldenrodyellow'
    ax_h = plt.axes([0.2, 0.01, 0.65, 0.04], facecolor=axcolor)
    ax_user_u = plt.axes([0.2, 0.045, 0.65, 0.04], facecolor=axcolor)
    ax_g = plt.axes([0.2, 0.07, 0.65, 0.04], facecolor=axcolor)
    ax_X = plt.axes([0.2, 0.105, 0.65, 0.04], facecolor=axcolor)
    ax_Y = plt.axes([0.2, 0.14, 0.65, 0.04], facecolor=axcolor)

    s_h = Slider(ax_h, 'Height (h)', 0.0, 50.0, valinit=h)
    s_u = Slider(ax_user_u, 'Initial Velocity (u)', 0.1, u_min*8, valinit=user_u)
    s_g = Slider(ax_g, 'Gravity (g)', 0.01, 20.0, valinit=g)
    s_X = Slider(ax_X, 'X coordinate of target', 0.01, 1000.0, valinit=X)
    s_Y = Slider(ax_Y, 'Y coordinate of target', 0.01, 1000.0, valinit=Y)

    target, = ax1.plot(X, Y, 'o', label=rf'Target at $\approx$ ({round(X, 2)}, {round(Y, 2)})', markersize=7, color="orange") 

    theta_min_u_label = ax1.text(0.03, 0.05, rf'$\theta_{{\text{{min u}}}}$ $\approx$ {round(theta_deg_min_u, 2)}$^\circ$', fontsize=12, color="red",
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7),transform=ax1.transAxes)
    theta_high_label = ax1.text(0.03, 0.12, rf'$\theta_{{\text{{high}}}}$ $\approx$ {round(theta_deg_user_u_high, 2)}$^\circ$', fontsize=12, color="blue",
                      bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7), transform=ax1.transAxes)
    theta_low_label = ax1.text(0.03, 0.19, rf'$\theta_{{\text{{high}}}}$ $\approx$ {round(theta_deg_user_u_low, 2)}$^\circ$', fontsize=12, color="green",
                      bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7), transform=ax1.transAxes)
    max_range_theta_label = ax1.text(0.03, 0.26, rf'$\theta_{{\text{{max range}}}}$ $\approx$ {round(theta_deg_max_range, 2)}$^\circ$', fontsize=12, color="saddlebrown",
                      bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7), transform=ax1.transAxes)
    u_min_label = ax1.text(0.03, 0.33, rf'$u_{{\text{{min}}}}$ $\approx$ {round(u_min, 2)} m/s', fontsize=12, color="red",
                      bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.7), transform=ax1.transAxes)
    
    ax1.grid(True)

    def update(val):

        nonlocal s_u
        
        h = s_h.val
        u = s_u.val
        g = s_g.val
        X = s_X.val
        Y = s_Y.val
        
        u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, theta_deg_max_range, range_min_u, x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low, x_pos_bounding, y_pos_bounding, x_pos_max_range, y_pos_max_range = tsks.task5(h, u, step, g, X, Y)

        min_u_line.set_xdata(x_pos_min_u)
        min_u_line.set_ydata(y_pos_min_u)

        high_line.set_xdata(x_pos_u_high)
        high_line.set_ydata(y_pos_u_high)
        
        low_line.set_xdata(x_pos_u_low)
        low_line.set_ydata(y_pos_u_low)

        bounding_line.set_xdata(x_pos_bounding)
        bounding_line.set_ydata(y_pos_bounding)

        max_range_line.set_xdata(x_pos_max_range)
        max_range_line.set_ydata(y_pos_max_range)

        target.set_data([X], [Y])
        label = rf'Target at $\approx$ ({round(X, 2)}, {round(Y, 2)})'
        target.set_label(label)

        theta_min_u_label.set_text(rf'$\theta_{{\text{{min u}}}}$ $\approx$ {round(theta_deg_min_u, 2)}$^\circ$')
        theta_high_label.set_text(rf'$\theta_{{\text{{high}}}}$ $\approx$ {round(theta_deg_user_u_high, 2)}$^\circ$')
        theta_low_label.set_text(rf'$\theta_{{\text{{low}}}}$ $\approx$ {round(theta_deg_user_u_low, 2)}$^\circ$')
        u_min_label.set_text(rf'$u_{{\text{{min}}}}$ $\approx$ {round(u_min, 2)} m/s')
        max_range_theta_label.set_text(rf'$u_{{\text{{min}}}}$ $\approx$ {round(theta_deg_max_range, 2)}$^\circ$')
            
        ax1.legend()

        ax1.relim()
        ax1.autoscale_view()

        fig.canvas.draw_idle()

    s_h.on_changed(update)
    s_u.on_changed(update)
    s_g.on_changed(update)
    s_X.on_changed(update)
    s_Y.on_changed(update)

    ax1.legend()

    plt.show()

def plot_task_7(u, dt, g):

    task6 = Tasks.Task7()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.3)

    theta_degrees = np.arange(45, 90, 5)

    for theta_deg in theta_degrees:
        theta = np.deg2rad(theta_deg)
        range = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*h)/(np.square(u)))) 
        tof = range / (u*np.cos(theta))
        ts = np.arange(0, tof, dt)
        range_values = task6.r(u, theta, g, ts)
        
        t_max = task6.compute_t_max(u, theta, g)
        t_min = task6.compute_t_min(u, theta, g)

        if t_max is not None and t_min is not None:
            range_max = task6.r(u, theta, g, t_max) 
            range_min = task6.r(u, theta, g, t_min) 

            ax1.scatter([t_max], [range_max], color='blue', zorder=3, s=15, marker='X', label=rf'Maxima at at $\approx$ ({round(t_max)}, {round(range_max)})')
            ax1.scatter([t_min], [range_min], color='red', zorder=3, s=15, marker='X', label=rf'Minima at at $\approx$ ({round(t_min)}, {round(range_min)})')

        ax1.plot(ts, range_values, label=f'θ = {theta_deg}°')

    ax1.legend(loc='upper left')
    ax1.set_title("Range vs Time")
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Range (m)')
    ax1.grid(True)

    for theta_deg in theta_degrees:
        theta = np.deg2rad(theta_deg)
        range = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*h)/(np.square(u)))) 
        tof = range / (u*np.cos(theta))
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
            ax2.scatter([x_max], [y_max], color='blue', zorder=3, s=15, marker='X', label=rf'Maxima at at $\approx$ ({round(x_max)}, {round(y_max)})')
            ax2.scatter([x_min], [y_min], color='red', zorder=3, s=15, marker='X', label=rf'Maxima at at $\approx$ ({round(x_min)}, {round(y_min)})')

        ax2.plot(x_positions, y_positions, label=f'θ = {theta_deg}°')

    ax2.set_title("Displacement")
    ax2.set_xlabel('x displacement (m)')
    ax2.set_ylabel('y displacement (m)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()

    plt.show()       

h = 10
u = 60
theta = 45
dt = 1/1000
g = 9.81
step = 1000
X = 100
Y = 100

#plot_task_2(h, u, theta, step, g)
#plot_task_3(h, u, step, g, X, Y)

#plot_task_3_and_5(h, u, step, g, X, Y)

#plot_task_7(h, u, dt, g)


