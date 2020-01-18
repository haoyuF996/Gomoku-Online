import socket               # 导入 socket 模块
import pygame
from pygame.locals import *
from sys import exit
import time
import random
import copy,time


s = socket.socket()         # 创建 socket 对象

host = socket.gethostname() # 获取本地主机名
port = 23333                # 设置端口号
sever = '172.17.133.12'#'192.168.3.12'
s.connect((sever, port))
msg = ''
s.setblocking(0)

def Init():
    '''
    Initialize the borad, the screen and some values
    '''
    global player,Anime,Borad,screen,Borad,loc,SIZE,n,Ssize,OnR,BB
    OnR = False
    n = 5
    loc = []
    Borad = InitialiseBorad(SIZE)
    BB = InitialiseBorad(SIZE)
    screen = pygame.display.set_mode((SIZE[0]*50+50, SIZE[1]*50+150), 0, 32)
    screen.fill((0,0,0))
    player = 0
    Anime = 0
    Ssize = (0,0)
def InitialiseBorad(size):
    '''
    initialise the borad with 0s\n
    borad is a dictionary with coordinates as keys\n
    coordinates starts with 0
    '''
    Borad = {}
    for x in range(size[0]):
        for y in range(size[1]):
            Borad[(x,y)] = 0
    return Borad
def DisplyBorad(Borad):
    '''
    Display the borad\n
    Borad: a dictionary with coordinates as keys\n
    0 for empty, 1 for red, 2 for blue\n
    '''
    global screen
    color = (238,221,130)
    List = [(3,3),(3,11),(11,3),(11,11)]
    size,pos = (SIZE[0]*50+50, SIZE[1]*50+50),(0,100)
    pygame.draw.rect(screen, color, Rect(pos, size))
    for i in range(1,SIZE[0]+1):
        pygame.draw.rect(screen, (0,0,0), Rect((i*50-1,150), (2,SIZE[1]*50-50)))

    for i in range(1,SIZE[1]+1):
        pygame.draw.rect(screen, (0,0,0), Rect((50,i*50-1+100), (SIZE[1]*50-50,2)))
    for i in List:
        p = ((i[0]+1)*50,(i[1]+1)*50+100)
        pygame.draw.circle(screen, (0,0,0), p, 6)
    for point in Borad:
        p = ((point[0]+1)*50,(point[1]+1)*50+100)
        if Borad[point]==0:
            continue
            #c = (0,0,0)
            #pygame.draw.circle(screen, c, p, 4)
        else:
            if Borad[point]==1:
                c = (255,255,224)
            elif Borad[point]==2:
                c = (0,0,0)
            elif Borad[point]==-1:
                c = (255,255,224)
            elif Borad[point]==-2:
                c = (0,0,0)
            pygame.draw.circle(screen, c, p, 20)
    return screen
def ShowWin(winner):
    '''
    Show who wins
    '''
    global screen,player,Won
    font = pygame.font.SysFont('impact',68)
    if winner == 'D':
        surface = font.render('Draw',True,(255,255,224))
    else:
        surface = font.render('WIN',True,winner)
    size = surface.get_width(),surface.get_height()
    pygame.draw.rect(screen, (0,0,0), Rect((SIZE[0]*15,30), Ssize))
    pygame.draw.rect(screen, (0,0,0), Rect((SIZE[0]*15,10), size))
    screen.blit(surface,(SIZE[0]*15,10))
def GetMouse(Borad):
    '''
    return position of mouse on Borad\n
    if not on Borad, return False
    '''
    x, y = pygame.mouse.get_pos()
    #获得鼠标位置
    for pos in Borad:
        distance = (x-(pos[0]+1)*50)**2 + (y-(pos[1]+3)*50)**2
        if distance<=400.0:
            return pos
    return False

pygame.init()
SIZE = (15,15)
Init()
pygame.display.set_caption('GomokuC')
DisplyBorad(Borad)
pygame.display.update()
player=2
Won = False
M=(0,0)
while True:
    CC = False
    tempBorad = copy.deepcopy(Borad)
    if not Won and M and Borad[M]<=0 and player==1:
        Borad[M] = 0
    M = GetMouse(Borad)
    #获得鼠标位置
    if not Won and M and Borad[M]<=0 and player==1:
        Borad[M] = -player
    #在鼠标所在位置展示棋子

    for event in pygame.event.get():
        if event.type == QUIT:
            #接收到退出事件后退出程序
            exit()
        if event.type == MOUSEBUTTONDOWN and M and Borad[M]<=0 and not Won and player==1:
            Borad[M] = player
            CC = True
            s.send(str(M).encode())
            #msg = str((M,player)).encode()
            #c.send(msg)
            player = int(2/player)
            #点击空位后放下棋子
    try:
        msg = s.recv(4096).decode()
    except Exception:
        pass
    try:
        if msg == 'Change':
            print(msg)
        BB = eval(msg)
    except Exception:
        if msg == 'White Win':
            ShowWin((255,165,0))
        elif msg == 'Balck Win':
            ShowWin((72,118,255))
        elif msg == 'Draw':
            ShowWin('D')
        elif msg=='Change':
            player = 1
            print('wow')
            msg=''
    

    if type(BB)==list:
        Borad = InitialiseBorad(SIZE)
        color = 2
        for i in BB:
            Borad[i]=color
            color = int(2/color)
    
    if Borad!=tempBorad and not CC:
        s.send(str(Borad).encode())
    
    Borad = BB
    DisplyBorad(Borad)
        #msg = input()
        #if msg == 'break':
            #break
    pygame.display.update()
    

s.close()
