
class Camera:
    def __init__(self, x=0, y=0, z=0):
        self.loc_x = x
        self.loc_y = y
        self.loc_z = z

    def set_location(self, loc):
        self.loc_x = loc[0]
        self.loc_y = loc[1]
        # self.loc_z = loc[2]

    def get_location(self):
        return self.loc_x, self.loc_y
