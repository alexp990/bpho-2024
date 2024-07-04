'''
earth and sky simulation: YES
path calculation: YES
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
        if omega == 0:
            return

        self.state = 1 - self.state
        if self.state:
            self.erotate.pause()
            if self.lexist:
                self.lrotate.pause()
            self.srotate.resume()
            self.alrotate.resume()
            self.dlrotate.resume()
            self.fbutton['frameColor'] = (0.2, 0.2, 0.2, 1)
        else:
            self.erotate.resume()
            if self.lexist:
                self.lrotate.resume()
            self.srotate.pause()
            self.alrotate.pause()
            self.dlrotate.pause()
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
        self.alrotate = ambient_light_node.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.alrotate.loop()
        if self.state:
            self.alrotate.pause()

        directional_light = DirectionalLight("directionalLight")
        directional_light.setColor(Vec4(0.8, 0.8, 0.8, 1))
        directional_light_np = render.attachNewNode(directional_light)
        directional_light_np.setHpr(0, -15, 0)
        render.setLight(directional_light_np)
        self.dlrotate = directional_light_np.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.dlrotate.loop()
        if self.state:
            self.dlrotate.pause()

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
            self.lines_np.removeNode()
            del self.lines_np


# -------------------------------------------- TRAJECTORY --------------------------------------------


    def createpath(self):

        x0, y0, z0 = 0, R, 0  # initial position (m)
        vx0, vy0, vz0 = 1000, 1000, 5000

        state0 = [x0, y0, z0, vx0, vy0, vz0]

        t = np.linspace(0, 10000, 100000)

        sol = odeint(self.projectile_motion, state0, t)
        print(sol)


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

        x, y, z, vx, vy, vz = state
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)

        if r < R - 10:
            return [0, 0, 0, -vx, -vy, -vz]

        # find density at altitude
        rho = 0.000001 * T0 - 9.8 * (r - R) ** 2
        if rho < 0: rho = 0
        
        # Calculate velocity components
        v = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        # print(r)        

        # Calculate drag force components
        F_drag_x = -0.5 * rho * A * C_d * v * vx
        F_drag_y = -0.5 * rho * A * C_d * v * vy
        F_drag_z = -0.5 * rho * A * C_d * v * vz
        
        # Equations of motion with varying gravity
        
        ax = (F_drag_x - 2 * omega * vy - omega ** 2 * x) / m
        ay = (F_drag_y + 2 * omega * vx - omega ** 2 * y - g0 * (R / (R + r)) ** 2 * rho) / m
        az = (F_drag_z - omega ** 2 * z) / m
        
        return [vx, vy, vz, ax, ay, az]





m = 1.0  # mass of the projectile (kg)
A = 0.01  # cross-sectional area of the projectile (m^2)
C_d = 1  # drag coefficient (dimensionless)
omega = 5 # angular velocity of Earth's rotation (rad/s)
g0 = 9.81  # gravitational acceleration at sea level (m/s^2)
R = 1000.0  # radius of the Earth (m)
T0 = 288.15  # standard temperature at sea level (K)

loadPrcFileData('', 'win-size 1024 768') 
base = ShowBase()
w = World()
base.run()
