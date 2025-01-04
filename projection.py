import sys
from mesh import *
import pygame
from pygame.locals import *

class ProjectionViewer:
    def __init__(self, width = 1280, height = 720, fps = 60, mode = "perspective", fov = 90, z_near = 0.1, z_far = 1000):
        self.width = width
        self.height = height
        self.fps = fps
        self.mode = mode
        self.fov = fov
        self.aspect = width / height
        self.z_near = z_near
        self.z_far = z_far

        self.frame_update = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D PyGame Engine")
        self.bg_color = (10, 10, 50)

        self.meshes = {}
        self.display_nodes = True
        self.display_edges = True
        self.node_color = (255, 255, 255)
        self.edge_color = (200, 200, 200)
        self.node_radius = 4

        self.debug = True

    def run(self):
        running = True
        key_to_function = {
            pygame.K_LEFT: (lambda x : x.translateAll((-10, 0, 0))),
            pygame.K_RIGHT: (lambda x : x.translateAll((10, 0, 0))),
            pygame.K_UP: (lambda x : x.translateAll((0, -10, 0))),
            pygame.K_DOWN: (lambda x : x.translateAll((0, 10, 0))),
            pygame.K_s: (lambda x : x.translateAll((0, 0, -10))),
            pygame.K_w: (lambda x : x.translateAll((0, 0, 10))),
            pygame.K_x: (lambda x : x.scaleAll((1.25, 1.25, 1.25))),
            pygame.K_z: (lambda x : x.scaleAll((0.8, 0.8, 0.8))),
            pygame.K_r: (lambda x : x.rotateAll("x", -5)),
            pygame.K_f: (lambda x : x.rotateAll("x", 5)),
            pygame.K_t: (lambda x : x.rotateAll("y", -5)),
            pygame.K_g: (lambda x : x.rotateAll("y", 5)),
            pygame.K_y: (lambda x : x.rotateAll("z", -5)),
            pygame.K_h: (lambda x : x.rotateAll("z", 5)),
        }

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function.keys():
                        key_to_function[event.key](self)

            self.rotateAll("x", 0.05)
            self.rotateAll("y", 0.05)
            self.rotateAll("z", 0.05)
            self.display()

            pygame.display.update()
            self.frame_update.tick(self.fps)

    def display(self):
        self.screen.fill(self.bg_color)

        for mesh in self.meshes.values():
            p_nodes = self.project(mesh.nodes)

            if self.display_nodes:
                for node in p_nodes:
                    pygame.draw.circle(self.screen, self.node_color, node[:2], self.node_radius, 0)

            if self.display_edges:
                for start, stop in mesh.edges:
                    pygame.draw.aaline(self.screen, self.edge_color, p_nodes[start][:2], p_nodes[stop][:2], 1)

    def project(self, nodes):
        p_nodes = np.dot(nodes, self.projectionMatrix())
        print(p_nodes)
        p_nodes /= p_nodes[:, 3].reshape(-1, 1) 
        p_nodes[:, 0] = (p_nodes[:, 0] + 1) * self.width * 0.5
        p_nodes[:, 1] = (p_nodes[:, 1] + 1) * self.height * 0.5
        return p_nodes

    def projectionMatrix(self):
        f = 1 / np.tan(np.radians(self.fov) / 2)
        z_range = self.z_far - self.z_near
        if self.mode == "perspective":
            return np.array([
                [f / self.aspect, 0, 0, 0],
                [0, f, 0, 0],
                [0, 0, (self.z_far + self.z_near) / z_range, 1],
                [0, 0, (2 * self.z_far * self.z_near) / z_range, 0]
            ])
        elif self.mode == "orthographic":
            return np.array([
                [2 / self.width, 0, 0, 0],
                [0, 2 / self.height, 0, 0],
                [0, 0, 2 / z_range, 0],
                [0, 0, (self.z_far + self.z_near) / z_range, 1]
            ])
        else: 
            ValueError("Incorrect Mode Parameter")

    def addMesh(self, name, mesh):
        self.meshes[name] = mesh

    def translateAll(self, dist):
        for mesh in self.meshes.values():
            mesh.translate(dist)

    def scaleAll(self, scale):
        for mesh in self.meshes.values():    
            mesh.scale(scale, mesh.getCentre())

    def rotateAll(self, axis, angle):
        for mesh in self.meshes.values():
            mesh.rotate(axis, angle, mesh.getCentre())