# entities/player.py
import pygame
from settings import *
from entities.bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 28          # Чуть меньше TILE_SIZE (32), чтобы легче проезжать в двери
        self.dir = "up"
        self.base_speed = PLAYER_SPEED 
        
        # Экономика и Здоровье
        self.hp = PLAYER_MAX_HP
        self.coins = 0
        self.score = 0
        
        # Таймеры (кулдауны)
        self.cooldown = 0
        self.i_frames = 0
        self.interact_cooldown = 0

        # --- ЗАГРУЗКА СПРАЙТА ТАНКА ИГРОКА ---
        try:
            img = pygame.image.load("танк.png").convert_alpha()
            self.original_image = pygame.transform.scale(img, (self.size, self.size))
        except FileNotFoundError:
            self.original_image = None
            print("ВНИМАНИЕ: Спрайт 'танк.png' не найден. Включена заглушка.")

    def move(self, dx, dy, dungeon, enemies):
        """Плавное движение со скольжением вдоль стен и проверкой столкновений с врагами"""
        if dx != 0:
            new_x = self.x + dx
            if not dungeon.check_collision(new_x, self.y, self.size):
                player_rect = pygame.Rect(new_x, self.y, self.size, self.size)
                can_move = True
                for enemy in enemies:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
                    if player_rect.colliderect(enemy_rect):
                        can_move = False
                        break
                
                if can_move:
                    self.x = new_x
        
        if dy != 0:
            new_y = self.y + dy
            if not dungeon.check_collision(self.x, new_y, self.size):
                player_rect = pygame.Rect(self.x, new_y, self.size, self.size)
                can_move = True
                for enemy in enemies:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
                    if player_rect.colliderect(enemy_rect):
                        can_move = False
                        break
                        
                if can_move:
                    self.y = new_y

    def interact(self, dungeon):
        """Взаимодействие с объектами на карте (Магазин)"""
        if self.interact_cooldown > 0:
            return

        player_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        interaction_zone = player_rect.inflate(20, 20) 

        shop_rects = dungeon.get_shop_rects()
        for shop_rect in shop_rects:
            if interaction_zone.colliderect(shop_rect):
                if self.coins >= HEAL_COST and self.hp < PLAYER_MAX_HP:
                    self.coins -= HEAL_COST
                    self.hp += 1
                    self.interact_cooldown = 30 
                    print("Куплено лечение!") 
                break 

    def update(self, keys, dungeon, bullets, enemies):
        """Основной цикл обновления логики игрока"""
        if self.cooldown > 0: self.cooldown -= 1
        if self.i_frames > 0: self.i_frames -= 1
        if self.interact_cooldown > 0: self.interact_cooldown -= 1

        actual_speed = self.base_speed
        if dungeon.is_in_bush(self.x, self.y, self.size):
            actual_speed *= BUSH_SLOWDOWN_MULTIPLIER 

        dx, dy = 0, 0
        
        # --- ФИКС УПРАВЛЕНИЯ (WASD + ЦФЫВ + СТРЕЛКИ + CapsLock) ---
        # 1094=ц, 1062=Ц | 1099=ы, 1067=Ы | 1092=ф, 1060=Ф | 1074=в, 1042=В
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[1094] or keys[1062]: 
            dy = -actual_speed
            self.dir = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[1099] or keys[1067]: 
            dy = actual_speed
            self.dir = "down"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[1092] or keys[1060]: 
            dx = -actual_speed
            self.dir = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[1074] or keys[1042]: 
            dx = actual_speed
            self.dir = "right"

        if dx != 0 or dy != 0:
            self.move(dx, dy, dungeon, enemies)

        # Стрельба (Пробел работает на любых языках)
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            bx = self.x + self.size // 2
            by = self.y + self.size // 2
            
            offset = self.size // 2 + 4 
            
            if self.dir == "up": by -= offset
            elif self.dir == "down": by += offset
            elif self.dir == "left": bx -= offset
            elif self.dir == "right": bx += offset
            
            bullets.append(Bullet(bx, by, self.dir, is_player=True))
            self.cooldown = PLAYER_SHOOT_COOLDOWN

        # Взаимодействие (E или русская У: 1091=у, 1059=У)
        if keys[pygame.K_e] or keys[1091] or keys[1059]:
            self.interact(dungeon)

    def draw(self, screen):
        """Отрисовка танка"""
        if self.i_frames > 0 and (self.i_frames // 6) % 2 == 0:
            return 

        if self.original_image:
            if self.dir == "down":
                rotated_img = self.original_image
            elif self.dir == "up":
                rotated_img = pygame.transform.rotate(self.original_image, 180)
            elif self.dir == "left":
                rotated_img = pygame.transform.rotate(self.original_image, -90)
            elif self.dir == "right":
                rotated_img = pygame.transform.rotate(self.original_image, 90)
            
            screen.blit(rotated_img, (self.x, self.y))
        else:
            body_color = PLAYER_COLOR
            track_color = (40, 40, 40)
            barrel_color = (20, 20, 20)
            
            if self.dir in ["up", "down"]:
                pygame.draw.rect(screen, track_color, (self.x, self.y, self.size//4, self.size))
                pygame.draw.rect(screen, track_color, (self.x + self.size - self.size//4, self.y, self.size//4, self.size))
                pygame.draw.rect(screen, body_color, (self.x + self.size//4, self.y + self.size//8, self.size//2, self.size - self.size//4))
            else:
                pygame.draw.rect(screen, track_color, (self.x, self.y, self.size, self.size//4))
                pygame.draw.rect(screen, track_color, (self.x, self.y + self.size - self.size//4, self.size, self.size//4))
                pygame.draw.rect(screen, body_color, (self.x + self.size//8, self.y + self.size//4, self.size - self.size//4, self.size//2))

            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            barrel_length = self.size // 2 + 4
            barrel_thickness = 6
            
            if self.dir == "up":
                pygame.draw.rect(screen, barrel_color, (center_x - barrel_thickness//2, self.y - 4, barrel_thickness, barrel_length))
            elif self.dir == "down":
                pygame.draw.rect(screen, barrel_color, (center_x - barrel_thickness//2, center_y, barrel_thickness, barrel_length))
            elif self.dir == "left":
                pygame.draw.rect(screen, barrel_color, (self.x - 4, center_y - barrel_thickness//2, barrel_length, barrel_thickness))
            elif self.dir == "right":
                pygame.draw.rect(screen, barrel_color, (center_x, center_y - barrel_thickness//2, barrel_length, barrel_thickness))