from .Global_Cache import Cache

class Button:
    def __init__(self, object_2d, object_text=None, text_align="center", object_2d_material_not_over=None, object_2d_material_over=None, text_color_not_over=(200, 200, 200), text_color_over=(255, 255, 255)):
        self.object_2d = object_2d

        self.cache_checkbox = False

        self.text_align = text_align

        self.button_active = False

        if object_2d_material_over is not None:
            self.object_2d_material_over = object_2d_material_over
        if object_2d_material_not_over is not None:
            self.object_2d_material_not_over = object_2d_material_not_over
        self.object_text = object_text
        self.object_text_color_over = text_color_over
        self.object_text_color_not_over = text_color_not_over

    def draw_button(self, screen, camera=None):
        if (self.object_2d.over(screen, camera) or self.cache_checkbox) and not Cache.Temp.Button["button_active"] and self.button_active:
            self.button_active = False
            self.object_2d.set_material(self.object_2d_material_over)
            if self.object_text is not None:
                self.object_text.set_color(self.object_text_color_over)
            Cache.Temp.Button["button_active"] = True
        else:
            self.object_2d.set_material(self.object_2d_material_not_over)
            if self.object_text is not None:
                self.object_text.set_color(self.object_text_color_not_over)
        self.object_2d.draw_object(screen, camera)

        if self.object_text is not None:
            if self.text_align.lower() == "center":
                self.object_text.set_localization((self.object_2d.get_localization()[0] + (self.object_2d.get_size()[0] - self.object_text.get_text_size()[0]) / 2, self.object_2d.get_localization()[1] + (self.object_2d.get_size()[1] - self.object_text.get_text_size()[1]) / 2))
            #elif self.text_align.lower() == "":
            #    pass
            else:
                self.object_text.set_localization((self.object_2d.get_localization()))
            self.object_text.draw_object(screen, camera, True)

    def button(self, button, screen, camera=None, multiple_click=False, button_type=""):
        self.button_active = True
        if button_type == "":
            return self.object_2d.button(button, screen, camera, multiple_click)
        elif button_type == "checkbox":
            if self.object_2d.button(button, screen, camera):
                if self.cache_checkbox:
                    self.cache_checkbox = False
                else:
                    self.cache_checkbox = True
            return self.cache_checkbox

    def over(self, screen, camera=None):
        return self.object_2d.over(screen, camera)
