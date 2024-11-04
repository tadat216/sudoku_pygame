import pygame
import sys
import os

folder_path = os.path.dirname(__file__)

class Button:
    def __init__(self, x, y, w, h, color_default, color_hover, color_click, color_text, text = "", image_path = "", font_size=20, border_rad=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.w = w
        self.h = h
        self.color_default = color_default
        self.color_hover = color_hover
        self.color_click = color_click
        self.current_color = self.color_default
        self.is_hovered = False
        self.is_clicked = False
        self.clicked_once = False  # New variable to track if clicked once
        self.font = pygame.font.SysFont('segoeuisemibold', font_size)
        self.image_path = ""
        if image_path != "":
            self.image_path = os.path.join(folder_path, "img", image_path)
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (w, h))
        self.text = text
        if self.text != "":
            self.color_text = color_text
            self.text_render = self.font.render(self.text, True, color_text)
            self.text_rect = self.text_render.get_rect(center=self.rect.center)
        self.border_rad = border_rad
        self.clicked_once = False

    def update_text(self, new_text):
        self.text = new_text
        self.text_render = self.font.render(self.text, True, self.color_text)

    def update_text_color(self, new_color):
        self.color_text = (new_color)
        self.text_render = self.font.render(self.text, True, self.color_text)

    def update_img(self, new_img):
        folder_path = os.path.dirname(__file__)
        self.image_path = os.path.join(folder_path, "img", new_img)
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=self.border_rad)
        if self.text != "":
            screen.blit(self.text_render, self.text_rect)
        if self.image_path != "":
            screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_release(event.pos)

    def handle_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            self.current_color = self.color_hover
        else:
            self.is_hovered = False
            self.current_color = self.color_default

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.is_clicked == False:
                self.is_clicked = True
                self.current_color = self.color_click

    def handle_release(self, mouse_pos):
        self.is_clicked = False
        self.is_hovered = False
        self.handle_hover(mouse_pos)
        self.clicked_once = False

    def clicked(self):
        if not self.is_clicked: return False
        if self.clicked_once: return False
        else:
            self.clicked_once = True
            return True
