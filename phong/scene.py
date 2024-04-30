from sphere import Sphere
from camera import Camera
from point_light import PointLight
from math import pi, sin, cos, acos, sqrt
from utils import *
import pygame

from random import random

class Scene:
    def __init__(self):
        self.objects = [
            # Sphere(-1.5, 0, 0, 1, (192, 160, 64)),
            # Sphere(1.5, 0, 0, 1, (64, 160, 192)),
            Sphere(-1.5, 0, 0, 1, (192, 160, 64)),
            Sphere(1.5, 0, 0, 1, (64, 192, 255)),
            Sphere(0.5, 1, -2, 1, (64, 192, 64)),
        ]
        self.light = PointLight(0, -2, 2, (255, 255, 255))
        # self.objects.append(Sphere(self.light.x, self.light.y, self.light.z, 0.05, (255, 255, 255)))
        self.camera = Camera(0, 0, 4, -pi/2, 0, pi/2)
    def update(self, events, dt):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d]-keys[pygame.K_a]
        dy = keys[pygame.K_LSHIFT]-keys[pygame.K_SPACE]
        dz = keys[pygame.K_w]-keys[pygame.K_s]
        drot_v = keys[pygame.K_DOWN]-keys[pygame.K_UP]
        drot_h = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]
        forward_x = cos(self.camera.rot_v)*cos(self.camera.rot_h)
        forward_y = sin(self.camera.rot_v)
        forward_z = cos(self.camera.rot_v)*sin(self.camera.rot_h)
        right_x = -forward_z
        right_y = 0
        right_z = forward_x
        self.camera.x += (forward_x*dz+right_x*dx)*dt*4
        self.camera.y += (forward_y*dz+right_y*dx+dy)*dt*4
        self.camera.z += (forward_z*dz+right_z*dx)*dt*4
        self.camera.rot_h += drot_h*dt*pi/4
        self.camera.rot_v += drot_v*dt*pi/4
        # light
        dx = keys[pygame.K_l]-keys[pygame.K_j]
        dz = keys[pygame.K_k]-keys[pygame.K_i]
        self.light.x += dx*dt*4
        self.light.z += dz*dt*4
    def draw(self, screen):
        width, height = screen.get_size()
        camera = self.camera
        light = self.light
        ka = 0.4
        kd = 0.6
        ks = 0.6
        ns = 16
        # step_length = 0.02
        # max_distance = 6
        for screen_x in range(width):
            for screen_y in range(height):
                # if random() > 0.3: continue
                ray_rot_h = camera.rot_h-camera.fov/2+camera.fov*(screen_x/width)
                ray_rot_v = camera.rot_v-camera.fov/2+camera.fov*(screen_y/height)
                ray_x = cos(ray_rot_v)*cos(ray_rot_h)
                ray_y = sin(ray_rot_v)
                ray_z = cos(ray_rot_v)*sin(ray_rot_h)
                ray_x, ray_y, ray_z = normalize((ray_x, ray_y, ray_z))
                nearest_depth = 255
                pixel = (0, 0, 0)
                for object in self.objects:
                    ACx = object.x-camera.x
                    ACy = object.y-camera.y
                    ACz = object.z-camera.z
                    ACx, ACy, ACz = normalize((ACx, ACy, ACz))
                    cosx = ACx*ray_x+ACy*ray_y+ACz*ray_z
                    sinx = sin(acos(cosx))
                    AC = get_distance((object.x, object.y, object.z), (camera.x, camera.y, camera.z))
                    m = AC*sinx
                    if m > object.radius:
                        continue
                    n = sqrt(object.radius**2-m**2)
                    l = AC*cosx
                    k = l-n
                    if 0 < k < nearest_depth:
                        nearest_depth = k
                        x = camera.x+k*ray_x
                        y = camera.y+k*ray_y
                        z = camera.z+k*ray_z
                        # ambient
                        R = ka*object.color[0]
                        G = ka*object.color[1]
                        B = ka*object.color[2]
                        # diffuse
                        Nx = x-object.x
                        Ny = y-object.y
                        Nz = z-object.z
                        Nx, Ny, Nz = normalize((Nx, Ny, Nz))
                        Lx = light.x-x
                        Ly = light.y-y
                        Lz = light.z-z
                        Lx, Ly, Lz = normalize((Lx, Ly, Lz))
                        dotNL = Nx*Lx+Ny*Ly+Nz*Lz
                        if dotNL > 0:
                            R += kd*(light.color[0]*object.color[0]/255)*dotNL
                            G += kd*(light.color[1]*object.color[1]/255)*dotNL
                            B += kd*(light.color[2]*object.color[2]/255)*dotNL
                        # specular
                        Vx = -ray_x
                        Vy = -ray_y
                        Vz = -ray_z
                        Hx = Vx+Lx
                        Hy = Vy+Ly
                        Hz = Vz+Lz
                        Hx, Hy, Hz = normalize((Hx, Hy, Hz))
                        dotNH = Nx*Hx+Ny*Hy+Nz*Hz
                        dotLV = Lx*Vx+Ly*Vy+Lz*Vz
                        if dotNL > 0 and dotLV > 0:
                            R += ks*(light.color[0]*object.color[0]/255)*max(dotNH**ns, 0)
                            G += ks*(light.color[1]*object.color[1]/255)*max(dotNH**ns, 0)
                            B += ks*(light.color[2]*object.color[2]/255)*max(dotNH**ns, 0)
                        # R = int(R/(ka+kd+ks))
                        # G = int(G/(ka+kd+ks))
                        # B = int(B/(ka+kd+ks))
                        R = int(min(max(R, 0), 255))
                        G = int(min(max(G, 0), 255))
                        B = int(min(max(B, 0), 255))
                        pixel = (R, G, B)
                screen.set_at((screen_x, screen_y), pixel)

                # distance = 0
                # hit = False
                # while not hit and distance < max_distance:
                #     distance += step_length
                #     x = camera.x+ray_x*distance
                #     y = camera.y+ray_y*distance
                #     z = camera.z+ray_z*distance
                #     for object in self.objects:
                #         if object.is_colliding_point((x, y, z)):
                #             hit = True
                #             # ambient
                #             R = ka*object.color[0]
                #             G = ka*object.color[1]
                #             B = ka*object.color[2]
                #             # diffuse
                #             Nx = x-object.x
                #             Ny = y-object.y
                #             Nz = z-object.z
                #             l = get_distance((0, 0, 0), (Nx, Ny, Nz))
                #             Nx /= l
                #             Ny /= l
                #             Nz /= l
                #             Lx = light.x-x
                #             Ly = light.y-y
                #             Lz = light.z-z
                #             l = get_distance((0, 0, 0), (Lx, Ly, Lz))
                #             Lx /= l
                #             Ly /= l
                #             Lz /= l
                #             dotNL = Nx*Lx+Ny*Ly+Nz*Lz
                #             if dotNL > 0:
                #                 R += kd*(light.color[0]*object.color[0]/255)*dotNL
                #                 G += kd*(light.color[1]*object.color[1]/255)*dotNL
                #                 B += kd*(light.color[2]*object.color[2]/255)*dotNL
                #             # specular
                #             Vx = -ray_x
                #             Vy = -ray_y
                #             Vz = -ray_z
                #             Hx = Vx+Lx
                #             Hy = Vy+Ly
                #             Hz = Vz+Lz
                #             l = get_distance((0, 0, 0), (Hx, Hy, Hz))
                #             Hx /= l
                #             Hy /= l
                #             Hz /= l
                #             dotNH = Nx*Hx+Ny*Hy+Nz*Hz
                #             dotLV = Lx*Vx+Ly*Vy+Lz*Vz
                #             if dotNL > 0 and dotLV > 0:
                #                 R += ks*(light.color[0]*object.color[0]/255)*max(dotNH**ns, 0)
                #                 G += ks*(light.color[1]*object.color[1]/255)*max(dotNH**ns, 0)
                #                 B += ks*(light.color[2]*object.color[2]/255)*max(dotNH**ns, 0)
                #             # R = int(R/(ka+kd+ks))
                #             # G = int(G/(ka+kd+ks))
                #             # B = int(B/(ka+kd+ks))
                #             R = int(min(max(R, 0), 255))
                #             G = int(min(max(G, 0), 255))
                #             B = int(min(max(B, 0), 255))
                #             screen.set_at((screen_x, screen_y), (R, G, B))
