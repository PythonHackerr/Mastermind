import pygame
pygame.init()  # Initialize pygame to access fonts


class Button:
    ''' Button class'''

    def __init__(self, screen, text, position, font_size, inactive_img, active_img, text_color, feedback=None, param=None):
        self.screen = screen
        self.text = text
        self.x, self.y = position
        if (text != "" and font_size != 0):
            self.font = pygame.font.SysFont("arial.ttf", font_size)
        else:
            self.font = None
        self.inactive_img = inactive_img
        self.active_img = active_img
        self.text_color = text_color
        self.feedback = feedback
        self.is_active = False
        self.last_active_state = False
        self.param = param
        self.render(inactive_img)

    def set_active(self):
        self.is_active = True

    def set_inactive(self):
        self.is_active = False

    def render(self, img=None):
        ''' Render button '''
        if (img == None):
            if (self.is_active):
                img = self.active_img
            else:
                img = self.inactive_img
        self.screen.blit(img, (self.x, self.y))
        if (self.font != None):
            text_render = self.font.render(self.text, True, self.text_color)
            text_rect = text_render.get_rect(
                center=(self.x + self.inactive_img.get_width()/2, self.y + self.inactive_img.get_height()/2))
            self.screen.blit(text_render, text_rect)

    def check_for_update(self):
        ''' Check if button state has changed '''
        if (self.last_active_state == self.is_active):
            return False
        else:
            self.last_active_state = self.is_active
            return True

    def point_inside(self, position):
        ''' Check if mouse is over button '''
        width = self.inactive_img.get_width()
        height = self.inactive_img.get_height()
        return (self.y <= position[1] <= self.y + height and
                self.x <= position[0] <= self.x + width)

    def on_click(self, event):
        ''' Detect button click '''
        if event.button == 1 and self.feedback != None and self.is_active == True:  # 1 - left mouse button
            if (self.param != None):
                self.feedback(self.param)
            else:
                self.feedback()

    def on_hover_over(self, mouse_pos):
        ''' Activate button if mouse is over button '''
        if self.point_inside(mouse_pos):
            self.set_active()
        else:
            self.set_inactive()
