
plane = "plane"

cube = None

arrow = [[0, 100], [30, 100], [30, 300], [38, 300], [38, 100], [68, 100], [34, 0]]

class Mesh:
    def __init__(self, mesh):
        self.Mesh = mesh
        self.size = [0, 0]

    def set_mesh(self, mesh):
        pass

    def get_mesh(self, localization=(0, 0), scale=(1, 1)):
        cache_mesh = self.Mesh
        n1 = 0
        for o in cache_mesh:
            n2 = 0
            for n in o:
                if n2 == 0:
                    n = n * scale[0]
                elif n2 == 1:
                    n = n * scale[1]
                cache_mesh[n1][n2] = n
                n2 += 1
            n1 += 1

        return cache_mesh
