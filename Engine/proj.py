'''
earth and sky simulation: YES
path calculation: YES
path plotting: YES
follow earth: YES
input: YES
projection: 
app: 
'''


from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import AmbientLight, DirectionalLight, Vec4
from panda3d.core import loadPrcFileData 
from panda3d.core import LineSegs, LVector4f
from panda3d.core import TextNode
from direct.task import Task
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def fl(n, ex = 0):
    try:
        float(n)
        return float(n)
    except ValueError:
        return ex
    
def nexp(n):
        if n < -5000:
            return 1
        elif n > 100:
            return 10e40 
        return np.exp(n)

class World(object):

    def __init__(self):
        base.setBackgroundColor(0, 0, 0)
        self.state0 = [0, R, 0, 0, 0, 0]
        self.show_engine()

    def show_engine(self):
        self.state = 0
        self.lexist = 0
        camera.setPos(0, 30, 0) # type: ignore
        camera.lookAt(0, 0, 0) # type: ignore
        base.camLens.setFov(90)
        self.planet()
        self.lights()

        # drag coefficient choices
        self.drag_image = OnscreenImage(image='drag.png', scale=(0.35, 0, 0.45))
        self.drag_image.setPos(0.4, 0, 0.1)
        self.drag_image.setBin('gui-popup', 1)
        self.drag_image.hide()
        self.drag_image.setDepthWrite(False)


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
            command=self.show_input_gui,
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
            self.fbutton['frameColor'] = (-0.5, 0.5, 0.5, 1)
    

# -------------------------------------------- INPUT --------------------------------------------


    def show_input_gui(self):

        self.input_frame = DirectFrame(frameColor=(1, 1, 1, 1), frameSize=(-1, 1, -0.7, 0.7), pos=(0, 0, 0))

        # Add labels
        self.lat_label = DirectLabel(parent=self.input_frame, text="LATITUDE:", scale=0.05, pos=(-0.95, 0, 0.6), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.lon_label = DirectLabel(parent=self.input_frame, text="LONGITUDE:", scale=0.05, pos=(-0.95, 0, 0.5), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.angle1_label = DirectLabel(parent=self.input_frame, text="LAUNCH ANGLE:", scale=0.05, pos=(-0.95, 0, 0.4), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.angle2_label = DirectLabel(parent=self.input_frame, text="AZIMUTH ANGLE:", scale=0.05, pos=(-0.95, 0, 0.3), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.velocity_label = DirectLabel(parent=self.input_frame, text="VELOCITY:", scale=0.05, pos=(-0.95, 0, 0.2), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.radius_label = DirectLabel(parent=self.input_frame, text="PLANET RADIUS:", scale=0.05, pos=(-0.95, 0, 0.1), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.omass_label = DirectLabel(parent=self.input_frame, text="OBJECT MASS:", scale=0.05, pos=(-0.95, 0, 0.0), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.pmass_label = DirectLabel(parent=self.input_frame, text="PLANET MASS:", scale=0.05, pos=(-0.95, 0, -0.1), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.area_label = DirectLabel(parent=self.input_frame, text="AREA:", scale=0.05, pos=(-0.95, 0, -0.2), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.omega_label = DirectLabel(parent=self.input_frame, text="ANG VELOCITY:", scale=0.05, pos=(-0.95, 0, -0.3), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)
        self.drag_label = DirectLabel(parent=self.input_frame, text="DRAG COEFF:", scale=0.05, pos=(0.05, 0, 0.6), frameColor=(1, 1, 1, 0), text_align=TextNode.ALeft)

        # Create input
        self.lat_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.6), numLines=1, width=5, text_align=TextNode.ALeft)
        self.lon_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.5), numLines=1, width=5, text_align=TextNode.ALeft)
        self.angle1_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.4), numLines=1, width=5, text_align=TextNode.ALeft)
        self.angle2_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.3), numLines=1, width=5, text_align=TextNode.ALeft)
        self.velocity_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.2), numLines=1, width=5, text_align=TextNode.ALeft)
        self.radius_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.1), numLines=1, width=5, text_align=TextNode.ALeft)
        self.omass_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, 0.0), numLines=1, width=5, text_align=TextNode.ALeft)
        self.pmass_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, -0.1), numLines=1, width=5, text_align=TextNode.ALeft)
        self.area_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, -0.2), numLines=1, width=5, text_align=TextNode.ALeft)
        self.omega_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(-0.5, 0, -0.3), numLines=1, width=5, text_align=TextNode.ALeft)
        self.drag_input = DirectEntry(parent=self.input_frame, scale=0.05, pos=(0.5, 0, 0.6), numLines=1, width=5, text_align=TextNode.ALeft)

        self.drag_image.show()

        self.submit_button = DirectButton(parent=self.input_frame, text="SUBMIT", scale=0.05, command=self.get_input_values)
        self.submit_button.setPos(0, 0, -0.5)

    def get_input_values(self):
        global lat, lon, angle1, angle2, velo, R, m, M, A, omega, C_d
        lat = fl(self.lat_input.get(), lat)
        lon = fl(self.lon_input.get(), lon)
        angle1 = fl(self.angle1_input.get(), angle1)
        angle2 = fl(self.angle2_input.get(), angle2)
        velo = fl(self.velocity_input.get(), velo)
        R = fl(self.radius_input.get(), R)
        m = fl(self.omass_input.get(), m)
        M = fl(self.pmass_input.get(), M)
        A = fl(self.area_input.get(), A)
        omega = fl(self.omega_input.get(), omega)
        C_d = fl(self.drag_input.get(), C_d)


        # Calculate initial components based on angles
        self.state0[0] = R * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
        self.state0[1] = R * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
        self.state0[2] = R * np.sin(np.radians(lat))
        self.state0[3] = np.cos(np.radians(angle1)) * np.cos(np.radians(angle2)) * velo
        self.state0[4] = np.sin(np.radians(angle1)) * np.cos(np.radians(angle2)) * velo
        self.state0[5] = np.sin(np.radians(angle2)) * velo

        # Remove the input frame
        self.drag_image.hide()
        self.input_frame.destroy()


# -------------------------------------------- SCENERY --------------------------------------------


    def planet(self):
        self.sky = loader.loadModel("solar_sky_sphere") # type: ignore
        self.sky_tex = loader.loadTexture("stars.jpg") # type: ignore
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render) # type: ignore
        self.sky.setScale(200)
        self.srotate = self.sky.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.srotate.loop()
        self.srotate.pause()

        self.orbit_root_earth = render.attachNewNode('orbit_root_earth') # type: ignore
        self.earth = loader.loadModel("planet_sphere") # type: ignore
        self.earth_tex = loader.loadTexture("earth.jpg") # type: ignore # type: ignore
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(10)
        self.earth.setPos(0, 0, 0)

        self.erotate = self.earth.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.erotate.loop()


    def lights(self):
        ambient_light = AmbientLight("ambientLight")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        ambient_light_node = render.attachNewNode(ambient_light) # type: ignore
        render.setLight(ambient_light_node) # type: ignore
        self.alrotate = ambient_light_node.hprInterval(360 / np.rad2deg(omega), (360, 0, 0))
        self.alrotate.loop()
        if self.state:
            self.alrotate.pause()

        directional_light = DirectionalLight("directionalLight")
        directional_light.setColor(Vec4(0.8, 0.8, 0.8, 1))
        directional_light_np = render.attachNewNode(directional_light) # type: ignore # type: ignore
        directional_light_np.setHpr(0, -15, 0)
        render.setLight(directional_light_np) # type: ignore
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

        render.clearLight() # type: ignore

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

        t = np.linspace(0, 100000, 1000000)
        sol = odeint(self.projectile_motion, self.state0, t)

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
        self.lines_np = render.attach_new_node(lines.create()) # type: ignore
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
        rho = r0 * nexp(G * M / R_ / T0 / r + omega * omega * R * (r - R) * (x * x + y * y) / r / r / R_ / T0)
        
        # Calculate velocity components
        v = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

        # gravitational force
        ax_g = -G * M * x / r ** 3
        ay_g = -G * M * y / r ** 3
        az_g = -G * M * z / r ** 3
        
        # coriolis force
        ax_c = 2 * omega * vy
        ay_c = -2 * omega * vx
        az_c = 0
        
        # centrifugal force
        ax_cf = -omega ** 2 * x
        ay_cf = -omega ** 2 * y
        az_cf = 0
        
        # drag force
        ax_d = -0.5 * C_d * rho * A * v * vx / m
        ay_d = -0.5 * C_d * rho * A * v * vy / m
        az_d = -0.5 * C_d * rho * A * v * vz / m
        
        # total acceleration
        ax = ax_g + ax_c + ax_cf + ax_d
        ay = ay_g + ay_c + ay_cf + ay_d
        az = az_g + az_c + az_cf + az_d
            
        return [vx, vy, vz, ax, ay, az]

lat = 0
lon = 0
angle1 = 90
angle2 = 0
velo = 100
m = 1.0  # mass of the projectile (kg)
A = 0.01  # cross-sectional area of the projectile (m^2)
C_d = 0.47  # drag coefficient (dimensionless)
omega = 0.1 # angular velocity of Earth's rotation (rad/s)
r0 = 1.225 # air density at sea level, kg/m^3
R = 1000.0  # radius of the Earth (m)
R_ = 8.314 # specific gas constant J/K/mol
T0 = 2.5  # standard temperature at sea level (K)
G = 6.67430e-11 # gravitational constant, m^3 kg^-1 s^-2
M = 1e10 # mass of the planet, kg

loadPrcFileData('', 'win-size 1024 768') 
base = ShowBase()
w = World()
base.run()
