# Разработай свою игру в этом файле!
from pygame import *

# Картинки для игры
img_hero = 'ronaldo_hero.png'
img_enemy = 'enemy.png'
img_back = 'football_field_FON.jpg'
img_wall = 'wall.png'
img_bullet = 'ball.png'
img_goal = 'kubok_goal.png'
img_wall_2 = 'wall_2.png.png'


# Шрифты
font.init()
font = font.SysFont('Comic Sans MS', 50) # вид и размер
win = font.render('YOU WIN!!!',True, (237, 0, 8))
lose = font.render('YOU LOSE!!!', True, (237, 0, 8))


# Классы
class GameSprite(sprite.Sprite): # Класс родитель для остальных классов
    def __init__(self, player_image, player_x, player_y, width, height, speed):
        # Вызываем конструктор класса спрайт
        sprite.Sprite.__init__(self)
        # Каждый спрайт должен хранить свойство image(Изображение)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        # Каждый спрайт должен хранить свойство rect - прямоугольник в которые он вписан (хитбокс)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # Метод отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self): # Метод передвижения
        keys = key.get_pressed() # Подключение клавиатуры
        #      маленькая буква кнопка на которую мы назначаем то или иное действие
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 45:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 45:
            self.rect.y += self.speed
    # Метод выстрел (Используя место игрока для создания пули)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 10)
        bullets.add(bullet)
    def fire2(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    side = 'left' # Назначаем любую сторону для движения (скорость 2)
    def update (self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    side = 'left' # Назначаем любую сторону для движения (скорость 2)
    def update (self):
        if self.rect.x <= 100:
            self.side = 'right'
        if self.rect.x >= win_width - 250:
            self.side = 'left'
        if self.side =='left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# Класс стена НЕнаследник Gameprite
class Wall(sprite.Sprite):
    def __init__(self, wall_image, wall_x, wall_y, width, height):
        super().__init__()
        self.w = width
        self.h = height
        # совойство image
        self.image = transform.scale(image.load(wall_image), (width, height))
        # свойство rect (хитбокс)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()


# Окно игры
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))

# Персонажи          картинка,  расположение х,у, ширина, высота, скорость
Ronaldo_hero = Player(img_hero, 5, win_height - 80, 40, 40, 10)
goalkeeper = Enemy(img_enemy, win_width-80, 280, 65, 65, 3)
goal = GameSprite(img_goal, win_width - 120, win_height - 80, 65, 65, 0)
goalkeeper2 = Enemy(img_enemy, win_width - 600, 60, 65, 65, 3)

# Расположение стен
w1 = Wall(img_wall, 100, 20, 250, 45)
w2 = Wall(img_wall, 100, 450, 250, 45)
w3 = Wall(img_wall_2, 100, 60, 45, 320)
w4 = Wall(img_wall_2, 200, 150, 45, 300)
w5 = Wall(img_wall_2, 450, 160, 45, 260)
w7 = Wall(img_wall, 390, 120, 200, 45)
w8 = Wall(img_wall_2, 300, 130, 45, 200)

# Группы для спрайтов
goalkeepers = sprite.Group()
walls = sprite.Group()
bullets = sprite.Group()
# Добавляем в группы спрайты
goalkeepers.add(goalkeeper)
goalkeepers.add(goalkeeper2)

walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w4)
walls.add(w5)
walls.add(w7)
walls.add(w8)

points = 0
# Игровой цикл
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                Ronaldo_hero.fire()
            elif e.key == K_TAB:
                Ronaldo_hero.fire2

    if finish != True:
        window.blit(back,(0,0))
        walls.draw(window)
        goalkeepers.update()
        goalkeepers.draw(window)
        Ronaldo_hero.reset()
        Ronaldo_hero.update()
        goal.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(bullets, goalkeepers, True, True):
            points += 1
        x = font.render(str(points), True, (255,255,255))
        window.blit(x, (20, 20))
        
        if sprite.spritecollide(Ronaldo_hero, walls, False):
            finish = True
            window.blit(lose, (200, 200))
        
        if sprite.spritecollide(Ronaldo_hero, goalkeepers, False):
            finish = True
            window.blit(lose, (200, 200))

        if sprite.collide_rect(Ronaldo_hero, goal):
            finish = True
            window.blit(win, (200, 200))



    display.update()
    clock.tick(FPS)


