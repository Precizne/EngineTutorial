import numpy as np

class Mesh:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_list):
        self.nodes = np.vstack((self.nodes, np.hstack((node_list, np.ones((len(node_list), 1))))))

    def addEdges(self, edge_list):
        self.edges += edge_list

    def translate(self, dist = (0, 0, 0)):
        dx, dy, dz = dist
        self.nodes = np.dot(self.nodes, self.translationMatrix(dx, dy, dz))

    def translationMatrix(self, dx, dy, dz):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dx, dy, dz, 1]
        ])

    def scale(self, scale = (1, 1, 1), centre = (0, 0, 0)):
        sx, sy, sz = scale
        cx, cy, cz = centre
        self.translate((-cx, -cy, -cz))
        self.nodes = np.dot(self.nodes, self.scalingMatrix(sx, sy, sz))
        self.translate((cx, cy, cz))

    def scalingMatrix(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def rotate(self, axis, angle = 0, centre = (0, 0, 0)):
        cx, cy, cz = centre
        self.translate((-cx, -cy, -cz))
        self.nodes = np.dot(self.nodes, self.rotationMatrix(axis, angle))
        self.translate((cx, cy, cz))

    def rotationMatrix(self, axis, angle):
        c = np.cos(np.radians(angle))
        s = np.sin(np.radians(angle))
        if axis == "x":
            return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])
        elif axis == "y":
            return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
        elif axis == "z":
            return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def getCentre(self):
        num_nodes = len(self.nodes)
        centre_x = sum([node[0] for node in self.nodes]) / num_nodes
        centre_y = sum([node[1] for node in self.nodes]) / num_nodes
        centre_z = sum([node[2] for node in self.nodes]) / num_nodes
        return (centre_x, centre_y, centre_z)

class UnitCube(Mesh):
    def __init__(self, start, stop):
        super().__init__()
        self.addNodes(np.array([(x, y, z) for x in (start, stop) for y in (start, stop) for z in (start, stop)]))
        self.addEdges([(n, n + 4) for n in range(0, 4)])
        self.addEdges([(n, n + 1) for n in range(0, 8, 2)])
        self.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])