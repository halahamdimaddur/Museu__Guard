import pygame
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("لعبة حارس المتحف")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_FLASH = (144, 238, 144)
RED_FLASH = (255, 99, 71)
GOLD = (255, 215, 0)

font = pygame.font.SysFont(None, 60)
#تحميل الصور
def load_images():
    move_right = [
        pygame.image.load("p11.png").convert_alpha(),
        pygame.image.load("p22.png").convert_alpha(),
        pygame.image.load("p33.png").convert_alpha(),
        pygame.image.load("p44.png").convert_alpha(),
        pygame.image.load("p55.png").convert_alpha(),
        pygame.image.load("p66.png").convert_alpha(),
        pygame.image.load("p77.png").convert_alpha(),
        pygame.image.load("p88.png").convert_alpha()
    ]
    move_right = [pygame.transform.scale(img, (60, 60)) for img in move_right]
    move_left = [pygame.transform.flip(img, True, False) for img in move_right]
    police_idle = move_right[0]

    thief_img = [
        pygame.image.load("t11.png").convert_alpha(),
        pygame.image.load("t2.png").convert_alpha(),
        pygame.image.load("t33.png").convert_alpha(),
        pygame.image.load("t4.png").convert_alpha(),
        pygame.image.load("t5.png").convert_alpha(),
        pygame.image.load("t6.png").convert_alpha(),
        pygame.image.load("t7.png").convert_alpha(),
        pygame.image.load("t8.png").convert_alpha()
    ]
    thief_img = [pygame.transform.scale(img, (70, 70)) for img in thief_img]
    thief_imgs_left = [pygame.transform.flip(img, True, False) for img in thief_img]
    thief_idle = thief_img[0]

    return move_right, move_left, police_idle, thief_img, thief_imgs_left, thief_idle

move_right, move_left, police_idle, thief_img, thief_imgs_left, thief_idle = load_images()


background_easy = pygame.image.load("photo_2025-05-30_20-28-24.jpg").convert()
background_easy = pygame.transform.scale(background_easy, (900, 600))

background_medium = pygame.image.load("photo_2025-05-30_15-16-43.jpg").convert()
background_medium = pygame.transform.scale(background_medium, (900, 600))

background_hard = pygame.image.load("photo_2025-05-30_20-28-34.jpg").convert()
background_hard = pygame.transform.scale(background_hard, (900, 600))

bg = pygame.image.load("photo_2025-05-30_15-13-15.jpg")
bg = pygame.transform.scale(bg, (900, 600))

star_img = pygame.image.load("sticker1.webp").convert_alpha()
star_img = pygame.transform.scale(star_img, (60, 60))

tree_img = pygame.transform.scale(pygame.image.load("tree.png").convert_alpha(), (120, 120))
bush_img = pygame.transform.scale(pygame.image.load("sticker5.webp").convert_alpha(), (40, 40))
rock_img = pygame.transform.scale(pygame.image.load("box.png").convert_alpha(), (40, 40))
barrel_img = pygame.transform.scale(pygame.image.load("box.png").convert_alpha(), (50, 50))

key_img = pygame.transform.scale(pygame.image.load("key.png").convert_alpha(), (70, 70))

pause_icon = pygame.transform.scale(pygame.image.load("sticke77r.webp").convert_alpha(), (40, 40))
home_icon = pygame.transform.scale(pygame.image.load("stick88er.webp").convert_alpha(), (40, 40))
exit_icon = pygame.transform.scale(pygame.image.load("sticke99r.webp").convert_alpha(), (40, 40))

pygame.mixer.init()
alert_sound = pygame.mixer.Sound("suriname-eas-alarm-351634.mp3")
explosion_sound = pygame.mixer.Sound("bomb-2-360875.mp3")
warning_sound = pygame.mixer.Sound("10sec-digital-countdown-sfx-319873.mp3")

camera_img = pygame.image.load("camera.webp").convert_alpha()
camera_img = pygame.transform.scale(camera_img, (30, 30))

bomb_img = pygame.transform.scale(pygame.image.load("bomb.webp").convert_alpha(), (20, 20))

clock = pygame.time.Clock()



class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self, screen):
        pass

    def get_rect(self):
        pass

    def get_mask(self):
        pass


class Police(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.jump_strength = -15
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 8
        self.direction = "idle"
        self.stopped = False
        self.img_idle = police_idle
        self.move_right = move_right
        self.move_left = move_left
        self.current_img = police_idle

    def update(self, keys=None, obstacles_rects=None, obstacles_masks=None, key_rect=None, bomb_triggered=False):
        move_x = 0
  
        if self.y >= 580:
           self.y = 580
           self.velocity_y = 0
           self.is_jumping = False


        if not self.stopped:
            if keys is not None:
                if keys[pygame.K_LEFT]:
                    move_x = -5
                    self.direction = "left"
                elif keys[pygame.K_RIGHT]:
                    move_x = 5
                    self.direction = "right"
                else:
                    self.direction = "idle"
                    self.frame_index = 0

        if not bomb_triggered:
            if keys is not None and keys[pygame.K_BACKSPACE] and not self.is_jumping:
                self.velocity_y = self.jump_strength
                self.is_jumping = True

        if self.is_jumping:
           self.velocity_y += self.gravity
           self.y += self.velocity_y
        if self.y >= 580:
          self.y = 580
          self.velocity_y = 0
          self.is_jumping = False


        if self.direction in ["right", "left"]:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.move_right)
                self.frame_timer = 0
        else:
            self.frame_timer = 0

        if bomb_triggered:
            self.current_img = self.img_idle
        else:
            if self.direction == "right":
                self.current_img = self.move_right[self.frame_index]
            elif self.direction == "left":
                self.current_img = self.move_left[self.frame_index]
            else:
                self.current_img = self.img_idle

        if obstacles_rects is not None and obstacles_masks is not None and key_rect is not None:
            police_mask = pygame.mask.from_surface(self.current_img)
            img_w, img_h = self.current_img.get_size()
            temp_rect = pygame.Rect(self.x, self.y - img_h, img_w, img_h)

            collision = False
            for i, rect in enumerate(obstacles_rects):
                offset = (rect.x - temp_rect.x, rect.y - temp_rect.y)
                if police_mask.overlap(obstacles_masks[i], offset):
                    if key_rect.x > 0 and key_rect.y > 0:
                        collision = True
                        break

            if collision and not self.is_jumping:
                self.stopped = True
            else:
                if not bomb_triggered:
                    self.stopped = False

            if not self.stopped:
                self.x += move_x
            return temp_rect
        else:
          
            self.x += move_x
            return pygame.Rect(self.x, self.y, 50, 50)

    def draw(self, screen):
        img_w, img_h = self.current_img.get_size()
        screen.blit(self.current_img, (self.x, self.y - img_h))

    def get_rect(self):
        img_w, img_h = self.current_img.get_size()
        return pygame.Rect(self.x, self.y - img_h, img_w, img_h)

    def get_mask(self):
        return pygame.mask.from_surface(self.current_img)


class Thief(Character):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 8
        self.images = thief_img
        self.current_img = self.images[0]

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.frame_timer = 0
            self.current_img = self.images[self.frame_index]
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.current_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

    def get_mask(self):
        return pygame.mask.from_surface(self.current_img)




class Key:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 70)
        self.mask = pygame.mask.from_surface(key_img)
        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(key_img, self.rect)


class Bomb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.mask = pygame.mask.from_surface(bomb_img)
        self.visible = False
        self.triggered = False
        self.start_time = None

    def draw(self, screen):
        if self.visible:
            screen.blit(bomb_img, self.rect)

    def trigger(self):
        self.triggered = True
        self.start_time = pygame.time.get_ticks()
        self.visible = False




class Game:
    def __init__(self, speed, background, obstacles, camera_pos, moving_obstacles=False, show_bomb=False, police_pos=(120, 530), thief_pos=(800, 530)):
        self.speed = speed
        self.background = background
        self.obstacles = obstacles
        self.camera_pos = camera_pos
        self.moving_obstacles = moving_obstacles
        self.police = Police(*police_pos)
        self.thief = Thief(*thief_pos, speed)
        self.key = Key(230, 450)
        self.bomb = Bomb(350, 550) if show_bomb else None
        if self.bomb:
            self.bomb.visible = True

        self.alert_played = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        self.paused = False

        self.start_time = time.time()

        self.obstacles_rects = [rect for img, rect in obstacles]
        self.obstacles_masks = [pygame.mask.from_surface(img) for img, rect in obstacles]

        
        self.pause_rect = pygame.Rect(10, 10, 40, 40)
        self.home_rect = pygame.Rect(60, 10, 40, 40)
        self.exit_rect = pygame.Rect(110, 10, 40, 40)



    def flash_effect(self, color):
        for _ in range(4):
            screen.fill(color)
            pygame.display.update()
            pygame.time.delay(150)
            screen.fill(BLACK)
            pygame.display.update()
            pygame.time.delay(150)

    def draw_text(self, text, pos, size=60, color=BLACK):
        f = pygame.font.SysFont(None, size)
        surface = f.render(text, True, color)
        screen.blit(surface, pos)

    def show_result_screen(self, result, time_taken):
        screen.fill(WHITE)
        self.draw_stars()
        if result == "win":
            self.draw_text("You win!", (300, 150), 70, (0, 128, 0))
        else:
            self.draw_text("You lost!", (300, 150), 70, (200, 0, 0))
        self.draw_text(f"Time taken: {round(time_taken, 2)} second", (200, 250), 50, BLACK)

        if result == "win":
            if time_taken < 7:
                stars = 3
            elif time_taken < 12:
                stars = 2
            else:
                stars = 1
            for i in range(stars):
                screen.blit(star_img, (300 + i * 70, 350))

        pygame.display.update()
        pygame.time.delay(3000)
        main_menu()

    def draw_stars(self):
        stars = []
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(-600, 0)
            radius = random.randint(2, 5)
            stars.append([x, y, radius])
        for _ in range(30):
            screen.fill(BLACK)
            for star in stars:
                pygame.draw.circle(screen, GOLD, (star[0], star[1]), star[2])
                star[1] += 10
            pygame.display.update()
            pygame.time.delay(50)

    def run(self):
        global alert_sound, explosion_sound, warning_sound

        while True:
            screen.blit(self.background, (0, 0))
            screen.blit(camera_img, self.camera_pos)

            # رسم الأيقونات
            screen.blit(pause_icon, self.pause_rect)
            screen.blit(home_icon, self.home_rect)
            screen.blit(exit_icon, self.exit_rect)


            if not self.alert_played and (self.camera_pos[0] - 20) < self.thief.x < (self.camera_pos[0] + 20) and self.thief.y > self.camera_pos[1]:
                alert_sound.play()
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                self.alert_played = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    alert_sound.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_rect.collidepoint(event.pos):
                        self.paused = not self.paused
                    elif self.home_rect.collidepoint(event.pos):
                        return
                    elif self.exit_rect.collidepoint(event.pos):
                         pygame.quit()
                         sys.exit()

            if self.paused:
                self.draw_text("Paused", (380, 250), 80, (200, 0, 0))
                pygame.display.update()
                clock.tick(15)
                continue

            keys = pygame.key.get_pressed()

            police_rect = self.police.update(keys, self.obstacles_rects, self.obstacles_masks, self.key.rect, self.bomb.triggered if self.bomb else False)

            if self.key.visible:
                offset_key = (self.key.rect.x - police_rect.x, self.key.rect.y - police_rect.y)
                police_mask = pygame.mask.from_surface(self.police.current_img)
                if police_mask.overlap(self.key.mask, offset_key):
                    self.key.rect.x = -100
                    self.key.rect.y = -100
                    self.obstacles_rects.clear()
                    self.obstacles_masks.clear()
                    self.obstacles.clear()
                    self.key.visible = False

            # تحقق من القنبلة
            if self.bomb and self.bomb.visible and not self.bomb.triggered:
                offset_bomb = (self.bomb.rect.x - police_rect.x, self.bomb.rect.y - police_rect.y)
                police_mask = pygame.mask.from_surface(self.police.current_img)
                if police_mask.overlap(self.bomb.mask, offset_bomb):
                    explosion_sound.play()
                    warning_sound.play()
                    self.bomb.trigger()
                    self.police.stopped = True

        
            if self.bomb and self.bomb.triggered:
                elapsed = pygame.time.get_ticks() - self.bomb.start_time
                if elapsed >= 5000:
                    self.police.stopped = False
                    self.bomb.triggered = False
                    warning_sound.stop()
                    explosion_sound.stop()

            self.thief.update()

            # تحقق من التصادم بين الشرطي واللص (الفوز)
            police_mask = pygame.mask.from_surface(self.police.current_img)
            offset_thief = (self.thief.x - police_rect.x, self.thief.y - police_rect.y)
            if police_mask.overlap(self.thief.get_mask(), offset_thief):
                if not self.police.stopped:
                    time_taken = time.time() - self.start_time
                    self.flash_effect(GREEN_FLASH)
                    self.show_result_screen("win", time_taken)
                    return

            # تحقق من هروب اللص (الخسارة)
            if self.thief.x + 50 < 0:
                time_taken = time.time() - self.start_time
                self.flash_effect(RED_FLASH)
                self.show_result_screen("lose", time_taken)
                return

            # رسم كل العناصر
            self.police.draw(screen)
            self.thief.draw(screen)

            if self.obstacles:
                for img, rect in self.obstacles:
                    if self.moving_obstacles and (self.key.visible) and not self.police.stopped:
                        rect.x -= 1
                    screen.blit(img, rect)

            self.key.draw(screen)
            if self.bomb:
                self.bomb.draw(screen)

            pygame.display.update()
            clock.tick(60)


# دوال  لرسم النص والأزرار

def draw_text(text, pos, size=60, color=BLACK):
    f = pygame.font.SysFont(None, size)
    surface = f.render(text, True, color)
    screen.blit(surface, pos)

def draw_button(rect, text, base_color, hover_color, mouse_pos, text_size=40):
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    font_btn = pygame.font.SysFont(None, text_size)
    text_surf = font_btn.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def main_menu():
    button_easy = pygame.Rect(300, 200, 200, 60)
    button_medium = pygame.Rect(300, 300, 200, 60)
    button_hard = pygame.Rect(300, 400, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))

        draw_button(button_easy, "Easy", (173, 216, 230), (135, 206, 250), mouse_pos)
        draw_button(button_medium, "Medium", (255, 255, 153), (255, 255, 100), mouse_pos)
        draw_button(button_hard, "Hard", (255, 182, 193), (255, 105, 180), mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy.collidepoint(event.pos):
                    obstacles_easy = [
                        (tree_img, pygame.Rect(250, 480, 120, 120)),
                        (tree_img, pygame.Rect(700, 470, 120, 120)),
                    ]
                    game = Game(speed=1, background=background_easy, obstacles=obstacles_easy, camera_pos=(760, 260),police_pos=(100,800),thief_pos=(760, 520))
                    game.run()

                elif button_medium.collidepoint(event.pos):
                    obstacles_medium = [
                        (bush_img, pygame.Rect(250, 540, 60, 60)),
                        (bush_img, pygame.Rect(600, 540, 60, 60)),
                    ]
                    game = Game(speed=2, background=background_medium, obstacles=obstacles_medium, camera_pos=(700, 285),police_pos=(100,800),thief_pos=(720, 520), moving_obstacles=True)
                    game.run()

                elif button_hard.collidepoint(event.pos):
                    obstacles_hard = [
                        (barrel_img, pygame.Rect(450, 530, 60, 60)),
                        (barrel_img, pygame.Rect(650, 530, 60, 60)),
                    ]
                    game = Game(speed=1.5, background=background_hard, obstacles=obstacles_hard, camera_pos=(800, 50),police_pos=(100,800),thief_pos=(800, 520), moving_obstacles="hard_trick", show_bomb=True)
                    game.run()

        pygame.display.update()
        clock.tick(60)

main_menu()
