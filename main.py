import pygame
from pygame.locals import *
from utils import Point2D
from obstacle import Obstacle
from source import Source
from player import Player
from ray import Ray
from wall import Wall
from math import cos, sin


class Main():
    _continue_flag = True
    _drawing_mode_flag = True
    _drawing_obstacle_flag = False
    BACKGROUND_COLOR = (40, 40, 40)

    def __init__(self, width,
                 height, precision=2, fps=30):
        pygame.init()
        if (width == 0 or height == 0):
            self.set_fullscreen()
            self.fullscreen = True
        else:
            self.canvas = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE)
            self.fullscreen = False
        self.canvas.fill(self.BACKGROUND_COLOR)
        # Sets the width and height
        screen_details = pygame.display.Info()
        self.width = screen_details.current_w
        self.minuature_width = self.width / 4
        self.height = screen_details.current_h
        self.minuature_height = self.height / 4
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.obstacles = []
        self.source = Player(Point2D(
            self.minuature_width / 2, self.minuature_height / 2), 60, Point2D(0, -1))
        self.source.generate_rays(precision)
        self.make_walls()
        self.ray_canvas = pygame.surface.Surface(
            (self.minuature_width, self.minuature_height))

        self.walk_up = False
        self.walk_down = False
        self.walk_left = False
        self.walk_right = False
        self.mouse_pos = (0, 0)
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_up = False
        self.rotate_down = False

    def make_walls(self):
        self.obstacles.append(
            Wall(Point2D(0, 0), Point2D(self.minuature_width, 0)))
        self.obstacles.append(
            Wall(Point2D(0, 0), Point2D(0, self.minuature_height)))
        self.obstacles.append(
            Wall(Point2D(self.minuature_width, self.minuature_height), Point2D(self.minuature_width, 0)))
        self.obstacles.append(
            Wall(Point2D(self.minuature_width, self.minuature_height), Point2D(0, self.minuature_height)))

    def set_fullscreen(self):
        self.canvas = pygame.display \
                            .set_mode(
                                (0, 0),
                                pygame.FULLSCREEN)
        screen_details = self.canvas.get_size()
        self.width = screen_details[0]
        self.height = screen_details[1]

    def restart(self):
        self._drawing_mode_flag = True
        self.obstacles = []
        self.make_walls()

    def loop(self):
        while self._continue_flag is True:
            self.canvas.fill(self.BACKGROUND_COLOR)
            for obstacle in self.obstacles:
                obstacle.draw(self.ray_canvas)

            if not self._drawing_mode_flag:
                self.source.draw(self.ray_canvas, self.canvas,
                                 self.obstacles, self.width, self.height, self.minuature_width, self.minuature_height)
            else:
                self.source.preview(self.ray_canvas, Point2D.from_tuple(
                    self.mouse_pos
                ) / 4)

            if self._drawing_obstacle_flag:
                Obstacle.preview(self.ray_canvas, self.starting_edge_of_obstacle, Point2D.from_tuple(
                    self.mouse_pos
                ) / 4)

            self.canvas.blit(
                self.ray_canvas, (0, 0))
            self.ray_canvas.fill(self.BACKGROUND_COLOR)
            self.handle_events()
            self.clock.tick(self.fps)
            pygame.display.flip()

    def handle_events(self):
        if self.walk_up:
            self.source.walk_front(
                self.clock, self.minuature_width, self.minuature_height)
        if self.walk_down:
            self.source.walk_backwards(
                self.clock, self.minuature_width, self.minuature_height)
        if self.walk_left:
            self.source.walk_paralel_left(
                self.clock, self.minuature_width, self.minuature_height)
        if self.walk_right:
            self.source.walk_paralel_right(
                self.clock, self.minuature_width, self.minuature_height)
        if self.rotate_left:
            self.source.rotate_left(
                self.clock, self.minuature_width, self.minuature_height)
        if self.rotate_right:
            self.source.rotate_rigth(
                self.clock, self.minuature_width, self.minuature_height)
        if self.rotate_up:
            self.source.rotate_up(
                self.clock, self.minuature_width, self.minuature_height)
        if self.rotate_down:
            self.source.rotate_down(
                self.clock, self.minuature_width, self.minuature_height)

        for event in pygame.event.get():
            # Quit the program if the user close the windows
            if event.type == pygame.QUIT:
                pygame.quit()
                self._continue_flag = False
            # Or press ESCAPE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self._continue_flag = False
                elif event.key == pygame.K_F11:
                    if (self.fullscreen is False):
                        self.fullscreen = True
                        pygame.display.quit()
                        pygame.display.init()
                        self.set_fullscreen()
                    else:
                        self.fullscreen = False
                        self.canvas = pygame.display.set_mode((self.width, self.height),
                                                              pygame.RESIZABLE)

                elif event.key == pygame.K_q:
                    self._drawing_mode_flag = not self._drawing_mode_flag

                elif event.key == pygame.K_r:
                    self.restart()

                elif event.key == pygame.K_w:
                    self.walk_up = True

                elif event.key == pygame.K_a:
                    self.walk_left = True

                elif event.key == pygame.K_s:
                    self.walk_down = True

                elif event.key == pygame.K_d:
                    self.walk_right = True

                elif event.key == pygame.K_LEFT:
                    self.rotate_left = True
                elif event.key == pygame.K_RIGHT:
                    self.rotate_right = True

                elif event.key == pygame.K_UP:
                    self.rotate_up = True
                elif event.key == pygame.K_DOWN:
                    self.rotate_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.walk_up = False

                elif event.key == pygame.K_a:
                    self.walk_left = False

                elif event.key == pygame.K_s:
                    self.walk_down = False

                elif event.key == pygame.K_d:
                    self.walk_right = False

                elif event.key == pygame.K_LEFT:
                    self.rotate_left = False
                elif event.key == pygame.K_RIGHT:
                    self.rotate_right = False

                elif event.key == pygame.K_UP:
                    self.rotate_up = False
                elif event.key == pygame.K_DOWN:
                    self.rotate_down = False

            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
                if not self.fullscreen:
                    self.canvas = pygame.display.set_mode((self.width, self.height),
                                                          pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = event.pos
                if self._drawing_mode_flag:
                    self._drawing_obstacle_flag = True
                    self.starting_edge_of_obstacle = Point2D.from_tuple(
                        self.mouse_pos) / 4

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pos = event.pos
                if self._drawing_mode_flag:
                    self._drawing_obstacle_flag = False
                    self.obstacles.append(Obstacle(self.starting_edge_of_obstacle, Point2D.from_tuple(
                        self.mouse_pos
                    ) / 4))

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos


if __name__ == "__main__":
    main = Main(900, 900, 1000, 60)
    main.loop()
