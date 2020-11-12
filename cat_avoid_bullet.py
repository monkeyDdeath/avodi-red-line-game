

import pygame, sys, random, time
from pygame.locals import *

#定义猫类
class Cat:
    #控制猫的初始化位置和默认非移动状态
    def __init__(self, WIDTH, HEIGHT, DOWN, UP, LEFT, RIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.catx = 10
        self.caty = self.height/2 - 39.5
        self.down = DOWN
        self.up = UP
        self.left = LEFT
        self.right = RIGHT
        self.cat = pygame.image.load('cat.png')
        self.speed = 10
        self.dead = False
    #更新猫的位置    
    def updateCat(self):
        if self.down and self.catRect.bottom<self.height:
            self.caty += self.speed
        elif self.up and self.catRect.top>0:
            self.caty -= self.speed
        elif self.right and self.catRect.right<WIDTH:
            self.catx += self.speed
        elif self.left and self.catRect.left>0:
            self.catx -= self.speed
        #在这里实时记录图片矩形的位置
        self.catRect = pygame.Rect(self.catx, self.caty, 125, 79)

#定义第一阶段子弹，一次一颗子弹，速度、厚度随机
class Bullet:
    def __init__(self, red, width, height):
        self.red = red
        self.width = width
        self.height = height
        self.long = random.randint(30, 40)
        self.speed = random.randint(10, 15)
        self.bullet_width = random.randint(8, 16)
        self.startx = width
        self.starty = random.randint(0,self.height)
        self.startPos = (self.startx, self.starty)
        self.endPos = (self.startx+self.long, self.starty)
        self.status = True
    #绘制子弹
    def updateBullet(self):
        if self.status:
            (x1, y1) = self.startPos
            (x2, y2) = self.endPos
            self.startPos = (x1-self.speed, y1)
            self.endPos = (x2-self.speed, y2)
            self.line = pygame.draw.line(screen, self.red, self.startPos, 
                                         self.endPos, self.bullet_width)
            #更新子弹
            if self.line.right <= 0:
                self.__init__(self.red, self.width, self.height)

#定义第二阶段子弹
class Bullet2:
    def __init__(self, red, width, height):
        self.red = red
        self.width = width
        self.height = height
        self.long = random.randint(30, 40)
        self.speed = random.randint(8, 13)
        self.bullet_width = random.randint(8, 16)
        self.startx = random.randint(0, self.width)
        self.starty = 0
        self.startPos = (self.startx, self.starty)
        self.endPos = (self.startx, self.starty-self.long)
        self.status = True
        
    def updateBullet(self):
        if self.status:
            (x1, y1) = self.startPos
            (x2, y2) = self.endPos
            self.startPos = (x1, y1+self.speed)
            self.endPos = (x2, y2+self.speed)
            self.line = pygame.draw.line(screen, self.red, self.startPos, 
                                         self.endPos, self.bullet_width)
            #更新子弹
            if self.line.top >= self.height:
                self.__init__(self.red, self.width, self.height)

class Bullet3:
    #第三阶段的子弹，可以随便设计好玩的来增加游戏变态程度
    def __init__(self, red, width, height):
        self.red = red
        self.width = width
        self.height = height
        
        #状态锁
        self.mutex = [True, True, True]

        #线的纵坐标
        self.liney_all = []
        for i in range(3):
            ran_y = random.randint(1, self.height)
            self.liney_all.append(ran_y)
        self.liney_all.sort()

        #线的横坐标
        self.linex_all = []
        for i in range(3):
            ran_x = random.randint(1, self.width)
            self.linex_all.append(ran_x)
        self.linex_all.sort()

        #线的长度
        self.long_all = [30, 35, 40, 45, 50]
        self.long = random.choice(self.long_all)

        #所有线的集合
        self.line_ass = []
        for i in range(3):
            posStart = (self.linex_all[i], self.liney_all[i])
            posEnd = (self.linex_all[i]+self.long, self.liney_all[i])
            self.line_ass.append([posStart, posEnd])
        
    def updateBullet(self):
        self.line_all = []
        for i in range(3):
            (x1, y1) = self.line_ass[i][0]
            (x2, y2) = self.line_ass[i][1]
            if self.mutex[i]:
                self.line_ass[i][0] = (x1-10, y1)
                self.line_ass[i][1] = (x2-10, y2)
                self.line = pygame.draw.line(screen, self.red, 
                                                self.line_ass[i][0], 
                                                self.line_ass[i][1], 4)
                self.line_all.append(self.line)
                if self.line.left <= 0:
                    self.mutex[i] = False
                    
            elif not self.mutex[i]:
                self.line_ass[i][0] = (x1+10, y1)
                self.line_ass[i][1] = (x2+10, y2)
                self.line = pygame.draw.line(screen, self.red, 
                                                self.line_ass[i][0], 
                                                self.line_ass[i][1], 4)
                self.line_all.append(self.line)
                if self.line.right >= self.width:
                    self.mutex[i] = True

#定义背景图片
class Direction:
    def __init__(self):
        self.direcx = 250
        self.direcy = 200
        self.image = pygame.image.load('direct.png')
        self.moveright = False
        self.moveleft = False
        self.startmove = False
    
    def updateDirection(self):
        if self.moveright:
            self.direcx -= 20
            if self.direcx <= -199:
                self.direcx = 799
                
        elif self.moveleft:
            #猫贴左边界才更新，表示猫在后退
            if self.startmove:
                self.direcx += 20
                if self.direcx >= 799:
                    self.direcx = -199

#核心代码，更新界面
class CreatMap:
    def __init__(self, cat, bullet, bullet2, bullet3, direction, width, height):
        self.width = width
        self.height = height
        self.cat = cat
        self.bullet = bullet
        self.bullet2 = bullet2
        self.bullet3 = bullet3
        self.direction = direction
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.begin = False
        self.restart = False
        self.phaseTwo = False#检测是否发射从上至下的子弹
        self.phaseThree = False
        self.score = 0
    
    def updateMap(self):
        #没开始画面
        if not self.begin:
            screen.fill(self.white)
            text = '按Y键开始游戏'
            text2 = '按方向键操控猫咪'
            text3 = '通过躲避红线得分'
            font = pygame.font.SysFont('kaiti', 30)
            text_surf = font.render(text, 1, (0, 0, 255))
            text2_surf = font.render(text2, 1, (0, 0, 255))
            text3_surf = font.render(text3, 1, (0, 0, 255))
            screen.blit(text_surf, [self.width/2-105, self.height/2-75])
            screen.blit(text2_surf, [self.width/2-120, self.height/2-45])
            screen.blit(text3_surf, [self.width/2-120, self.height/2-15])
            pygame.display.flip()
        
        else:
            screen.fill(self.white)
            self.cat.updateCat()

            self.checkLeftCollide()
            self.direction.updateDirection()
            screen.blit(self.direction.image, 
                        (self.direction.direcx, self.direction.direcy))
            self.bullet.updateBullet()
            
            #当分数达到一定程度，发射下一阶段子弹
            if self.score > 5:
                self.phaseTwo = True
                self.bullet2.updateBullet()
            
            if self.score > 20:
                self.phaseThree = True
                self.bullet3.updateBullet()
            
            self.checkDead()
            if not self.cat.dead:
                screen.blit(self.cat.cat, (self.cat.catx, self.cat.caty))#在这里传递，猫死了就消失
                self.blitScore()
                pygame.display.update()
            else:
                self.result()
                if self.restart:
                    '''
                    这里重新开始游戏，把所有实例重新初始化，
                    但因为实例是在游戏循环更新之前就被创建好的，然后才作为初始数据
                    放到了CreatMap类里，所以存在代码冗余问题，
                    Cat、Direction、Bullet它们的位置数据在游戏过程中
                    是被改动了的，所以就需要手动把它们被改动的数据给重新调整，
                    比如这里的猫的生死状态、背景图的移动变化、新子弹的初始位置
                    '''
                    self.__init__(self.cat, self.bullet, self.bullet2,
                                  self.bullet3, self.direction,
                                  self.width, self.height)
                    
                    self.cat.dead = False
                    self.cat.catx = 10
                    self.cat.caty = self.height/2 - 39.5
                    
                    self.direction.direcx = 250
                    self.direction.direcy = 200
                    
                    self.bullet.startx = self.width
                    self.bullet.starty = random.randint(0,self.height)
                    self.bullet.startPos = (self.bullet.startx, 
                                            self.bullet.starty)
                    self.bullet.endPos = (self.bullet.startx+self.bullet.long, 
                                          self.bullet.starty)
                    
                    self.bullet2.startx = random.randint(0, self.width)
                    self.bullet2.starty = 0
                    self.bullet2.startPos = (self.bullet2.startx, 
                                             self.bullet2.starty)
                    self.bullet2.endPos = (self.bullet2.startx, 
                                           self.bullet2.starty-self.bullet2.long)
                    
                    self.bullet3.line_all = []
                    
                    '''
                    子弹3的位置没有初始化
                    '''

        
    def checkLeftCollide(self):
        '''
        当猫的图片达到最左边，背景图响应键盘左键一直右移
        注意，这个最左边的值和猫图片大小、移动速度和屏幕宽度有关，这里恰好等于0罢了
        '''
        if self.cat.catRect.left <= 0:
            self.direction.startmove = True
        else:
            self.direction.startmove = False
    
    #检查猫是否被子弹碰到
    def checkDead(self):
        if self.bullet.line.colliderect(self.cat.catRect):
            self.cat.dead = True
        
        if self.phaseTwo:
            if self.bullet2.line.colliderect(self.cat.catRect):
                self.cat.dead = True
                
        if self.phaseThree:
            for i in range(3):
                if self.bullet3.line_all[i].colliderect(self.cat.catRect):
                    self.cat.dead = True
    
    #失败结果
    def result(self):
        text = '你好菜哦，就得了%s分' % str(self.score)
        text2 = '按R键重新开始吧'
        font = pygame.font.SysFont('kaiti', 30)
        text_surf = font.render(text, 1, (255, 128, 0))
        text2_surf = font.render(text2, 2, (255, 128, 0))
        screen.blit(text_surf, [self.width/2 - 150, 0])
        screen.blit(text2_surf,[self.width/2 - 120, 30])
        pygame.display.flip()
    
    #分数
    def blitScore(self):
        font = pygame.font.SysFont('kaiti', 20)
        if self.bullet.line.right <= 0:
            self.score += 1
        if self.phaseTwo and self.bullet2.line.top >= self.height:
            self.score += 5
        if self.phaseThree:
            self.score += 1
        score_surf = font.render(str(self.score), 1, (191, 0, 191))
        text = '得分'
        text_surf = font.render(text, 1, (191, 0, 191))
        screen.blit(score_surf, [self.width//2 - 10, 0])
        screen.blit(text_surf, [self.width//2 - 50, 0])
        pygame.display.flip()
    
    '''
    这里是定义最终结局，我想的就是达到达到一定分数，在界面最右边放盆猫粮，猫迟到就算赢了
    当然可以设计更好玩的赢法，随意
    '''
    def checkWin(self):
        pass    

#主程序，主要用来响应键盘事件
def main(FPS):
    #类、函数之间共用的变量要声明全局变量
    global screen, background
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('别碰红线')
    fps = pygame.time.Clock()

    while True:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    Cat.down = True
                elif event.key == K_UP:
                    Cat.up = True
                elif event.key == K_LEFT:
                    Cat.left = True
                    Direction.moveleft = True
                elif event.key == K_RIGHT:
                    Cat.right = True
                    Direction.moveright = True
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                elif event.key == K_y:
                    CreatMap.begin = True
                
                elif event.key == K_r:
                    CreatMap.restart = True
                    
            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    Cat.down = False
                elif event.key == K_UP:
                    Cat.up = False
                elif event.key == K_LEFT:
                    Cat.left = False
                    Direction.moveleft = False
                elif event.key == K_RIGHT:
                    Cat.right = False
                    Direction.moveright = False

        CreatMap.updateMap()
        
if __name__ == '__main__':
    #界面数据
    SIZE = WIDTH, HEIGHT = 800, 600
    FPS = 70
    RED = (255, 0, 0)
    DOWN = False
    UP = False
    RIGHT = False
    LEFT = False
    #实例化猫、子弹、背景图、地图
    Cat = Cat(WIDTH, HEIGHT, DOWN, UP, LEFT, RIGHT)
    Bullet = Bullet(RED, WIDTH, HEIGHT)
    Bullet2 = Bullet2(RED, WIDTH, HEIGHT)
    Bullet3 = Bullet3(RED, WIDTH, HEIGHT)
    Direction = Direction()
    CreatMap = CreatMap(Cat, Bullet, Bullet2, Bullet3, Direction, WIDTH, HEIGHT)
    
    main(FPS)
