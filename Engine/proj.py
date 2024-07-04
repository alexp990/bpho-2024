'''
earth and sky simulation: YES
path calculation:
path plotting: YES
follow earth: YES
gui: 
app: 
'''


from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import AmbientLight, DirectionalLight, Vec4
from panda3d.core import loadPrcFileData 
from panda3d.core import LineSegs, LVector4f
from direct.task import Task
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


m = 1.0  # mass of the projectile (kg)
rho0 = 1.225  # air density at sea level (kg/m^3)
A = 0.01  # cross-sectional area of the projectile (m^2)
C_d = 1  # drag coefficient (dimensionless)
omega = 10  # angular velocity of Earth's rotation (rad/s)
g0 = 9.81  # gravitational acceleration at sea level (m/s^2)
R = 1000.0  # radius of the Earth (m)
T0 = 288.15  # standard temperature at sea level (K)
L = 0.0065  # temperature lapse rate (K/m)


class World(object):

    def __init__(self):
        base.setBackgroundColor(0, 0, 0)
        self.show_engine()

    def show_engine(self):
        self.state = 0
        self.lexist = 0
        camera.setPos(0, 30, 0)
        camera.lookAt(0, 0, 0)
        base.camLens.setFov(90)

        self.planet()
        self.lights()


# -------------------------------------------- BUTTONS --------------------------------------------


        self.fbutton = DirectButton(
            text="FOLLOW",
            scale=0.1,
            command=self.followClick,
            color = (0.2, 0.2, 0.2, 1))
        self.fbutton.setPos(1.1, 0.9, 0.9)

        self.sbutton = DirectButton(
            text="SETTINGS",
            scale=0.1,
            command=self.gui,
            color = (0.2, 0.2, 0.2, 1))
        self.sbutton.setPos(1.1, 0.9, 0.7)

        self.pbutton = DirectButton(
            text="PLOT",
            scale=0.1,
            command=self.createpath,
            color = (0.2, 0.2, 0.2, 1))
        self.pbutton.setPos(1.1, 0.9, 0.5)


    def followClick(self):
        self.state = 1 - self.state
        if self.state:
            self.erotate.pause()
            if self.lexist:
                self.lrotate.pause()
            self.srotate.resume()
            self.fbutton['frameColor'] = (0.2, 0.2, 0.2, 1)
        else:
            self.erotate.resume()
            if self.lexist:
                self.lrotate.resume()
            self.srotate.pause()
            self.fbutton['frameColor'] = (0.5, 0.5, 0.5, 1)
    

# -------------------------------------------- GUI --------------------------------------------


    def gui(self):
        pass


# -------------------------------------------- SCENERY --------------------------------------------


    def planet(self):
        self.sky = loader.loadModel("solar_sky_sphere")
        self.sky_tex = loader.loadTexture("stars.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(200)
        self.srotate = self.sky.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.srotate.loop()
        self.srotate.pause()

        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')
        self.earth = loader.loadModel("planet_sphere")
        self.earth_tex = loader.loadTexture("earth.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(10)
        self.earth.setPos(0, 0, 0)

        self.erotate = self.earth.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.erotate.loop()

    def lights(self):
        ambient_light = AmbientLight("ambientLight")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        ambient_light_node = render.attachNewNode(ambient_light)
        render.setLight(ambient_light_node)

        directional_light = DirectionalLight("directionalLight")
        directional_light.setColor(Vec4(0.8, 0.8, 0.8, 1))
        directional_light_np = render.attachNewNode(directional_light)
        directional_light_np.setHpr(0, -15, 0)
        render.setLight(directional_light_np)


    def clearScreen(self):

        if hasattr(self, 'sky') and self.sky:
            self.sky.removeNode()
            del self.sky

        if hasattr(self, 'earth') and self.earth:
            self.earth.removeNode()
            del self.earth

        render.clearLight()

        if hasattr(self, 'fbutton') and self.fbutton:
            self.fbutton.destroy()
            del self.fbutton

        if hasattr(self, 'sbutton') and self.sbutton:
            self.sbutton.destroy()
            del self.sbutton
        
        if hasattr(self, 'earth') and self.earth:
            self.earth.removeNode()
            del self.earth
        
        if hasattr(self, 'lines_np') and self.lines_np:
            self.lines_np.destroy()
            del self.lines_np


# -------------------------------------------- TRAJECTORY --------------------------------------------


    def createpath(self):

        x0, y0, z0 = R, R, 0  # initial position (m)
        vx0, vy0, vz0 = 1000, 1000, 1000

        state0 = [x0, y0, z0, vx0, vy0, vz0]

        t = np.linspace(0, 1000, 1000000)

        sol = odeint(self.projectile_motion, state0, t)


        if hasattr(self, 'lines_np') and self.lines_np:
            self.lines_np.removeNode()
            del self.lines_np

        lines = LineSegs()
        
        lines.set_color(LVector4f(1, 0, 0, 1))
        lines.set_thickness(3)
        
        # draw path
        c = 10 / R
        for i, (x, y, z, vx, vy, vz) in enumerate(sol):
            x *= c
            y *= c
            z *= c
            if i == 0:
                lines.move_to(x, y, z)
            else:
                lines.draw_to(x, y, z)
        
        # render path
        self.lines_np = render.attach_new_node(lines.create())
        self.lines_np.set_pos(0, 0, 0)
        self.lrotate = self.lines_np.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.lrotate.loop()
        if self.state:
            self.lrotate.pause()
        self.lexist = 1

    def projectile_motion(self, state, t):
    
        x, y, z, dx, dy, dz = state
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        if r < R - 10:
            dx *= -1
            dy *= -1
            dz *= -1
        
        # find density at altitude
        rho = rho0 * np.exp(-(g0 * r * 0.0289644 / (8.31447 * T0)) + ((g0 * r) / (R * T0)) - (L * r) / T0)
        
        # Calculate velocity components
        v = np.sqrt(dx**2 + dy**2 + dz**2)
        v_x = dx
        v_y = dy
        v_z = dz
        
        # Calculate drag force components
        F_drag_x = -0.5 * rho * A * C_d * v * v_x
        F_drag_y = -0.5 * rho * A * C_d * v * v_y
        F_drag_z = -0.5 * rho * A * C_d * v * v_z
        
        # Equations of motion with varying gravity
        dxdt = v_x
        dydt = v_y
        dzdt = v_z
        
        dvxdt = (F_drag_x - 2 * omega * dy - omega**2 * x) / m
        dvydt = (F_drag_y + 2 * omega * dx - omega**2 * y - g0 * (R / (R + z))**2 * rho) / m
        dvzdt = (F_drag_z - omega**2 * z) / m
        
        return [dxdt, dydt, dzdt, dvxdt, dvydt, dvzdt]


loadPrcFileData('', 'win-size 1024 768') 
base = ShowBase()
w = World()
base.run()
