#Python 3.6
import pygame
import websockets, asyncio
import json
import tensorflow
from game import *


tanklist = []
bot_id = 0
connection = websockets.connect("wss://tanks.ml/ws")

pygame.init()
screen = pygame.display.set_mode((1600, 800))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((50, 50, 50))
screen.blit(background, (0, 0))
pygame.display.flip()

def send_shoot():
    connection.send(json.dumps([0]))

def send_move(direction):
    connection.send(json.dumps([1, direction]))

def send_rotate(direction):
    connection.send(json.dumps([2, direction]))

def set_bot_id(id):
    global bot_id
    bot_id = id

def get_bot_id():
    return bot_id


def redraw():
    n = len(tanklist)
    for i in range(n):
        tanklist[i].draw(screen)
        m = len(tanklist[i].bullets)
        for j in range(m):
            tanklist[i].bullets[j].draw(screen)


def consumer(message):
    header = message[0]
    data = message[1]
    screen.blit(background, (0,0))

    if header == 0:
        n = len(data)
        for i in range(n):

            if(i != n - 1):
                tmpTank = Tank('tank.png', data[i]["x"], data[i]["y"], data[i]["angle"])
            else:
                tmpTank = Tank('myTank.png', data[i]["x"], data[i]["y"], data[i]["angle"])
                set_bot_id(i)

            tanklist.append(tmpTank)
            screen.blit(tmpTank.image, tmpTank.rect)

            m = len(data[i]["bullets"])
            for j in range(m):
                if (i != n - 1):
                    tmpBullet = Bullet('bullet.png', data[i]["bullets"][j]["x"], data[i]["bullets"][j]["y"])
                else:
                    tmpBullet = Bullet('myBullet.png', data[i]["bullets"][j]["x"], data[i]["bullets"][j]["y"])

                tmpTank.bullets.append(tmpBullet)
                screen.blit(tmpBullet.image, tmpBullet.rect)

    elif header == 1:

        tanklist[data[0]].set_position(data[1], data[2])


    elif header == 2:

        tanklist[data[0]].rot_center(data[1])


    elif header == 3:
        if data[0] != get_bot_id():
            tmpBullet = Bullet('bullet.png', data[2], data[3])
        else:
            tmpBullet = Bullet('myBullet.png', data[2], data[3])

        tanklist[data[0]].bullets.append(tmpBullet)
        screen.blit(tmpBullet.image, tmpBullet.rect)

    elif header == 4:
        tanklist[data[0]].bullets[data[1]].set_position(data[2], data[3])

    '''
    elif header == 5:

    elif header == 6:

    elif header == 7:
    '''
    redraw()
    pygame.display.update()

async def tanks():
    async with connection as websocket:
        while 1:
            message = json.loads(await websocket.recv())
            consumer(message)


asyncio.get_event_loop().run_until_complete(tanks())
