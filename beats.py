# -*- coding: utf-8 -*-
import pygame
import time
import random
import sys
import os
from pygame.locals import *

# 初始化
pygame.init()

# 帧数
FPS = 60

# 窗口大小
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 700

# 开始窗口大小
MENU_WIDTH = 1024
MENU_HEIGHT = 640

# 颜色值设置
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 155)
YELLOW = (155, 155, 0)

# 下落的箭头的位移值
OFFSET = (0, 3)

# 帧数控制对象
fps_clock = pygame.time.Clock()

# 显示屏幕的SURFACE对象
SCREEN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

# 设置标题
pygame.display.set_caption('Beats')

# 计分
score = 0

# 加载用于显示分数，歌曲名的字体对象
fontObj_60 = pygame.font.Font('Asterix Italic.ttf', 60)

score_text = fontObj_60.render(str(score), True, WHITE)
score_text_rect = score_text.get_rect()
score_text_rect.centerx = 400
score_text_rect.top = 10

# 加载显示菜单的字体对象
fontObj_100 = pygame.font.Font('Asterix Italic.ttf', 100)
fontOBj_70 = pygame.font.Font('freesansbold.ttf', 70)
fontObj_40 = pygame.font.Font('freesansbold.ttf', 40)

# 'PLAY'菜单
play_title_text = fontObj_100.render('PLAY', True, RED)
play_title_text_rect = play_title_text.get_rect()
play_title_text_rect.centerx = 510
play_title_text_rect.centery = 380

# 'DIY'菜单
diy_title_text = fontObj_100.render('DIY', True, WHITE)
diy_title_text_rect = diy_title_text.get_rect()
diy_title_text_rect.centerx = 510
diy_title_text_rect.centery = 460

# 'RECORD'菜单
record_title_text = fontObj_100.render('RECORD', True, WHITE)
record_title_text_rect = record_title_text.get_rect()
record_title_text_rect.centerx = 510
record_title_text_rect.centery = 540

# play（）里调用的，显示结果的字
result_text = fontOBj_70.render('Your Score is:', True, WHITE)
result_text_rect = result_text.get_rect()
result_text_rect.centerx = 260
result_text_rect.centery = 330

# 加载游戏背景
BACKGROUND = pygame.image.load('background.jpg')

# 加载标题
TITLE = pygame.image.load('start.jpg')

# 加载无标题背景
PURE_TITLE = pygame.image.load('pure title.jpg')

# 加载good，great，perfect三个图像
GOOD = pygame.image.load('good.png')
GREAT = pygame.image.load('great.png')
PERFECT = pygame.image.load('perfect.png')
MISS = pygame.image.load('miss.png')

# 加载四种箭头图标
UP_ARROW = pygame.image.load('up_arrow.png')
DOWN_ARROW = pygame.image.load('down_arrow.png')
LEFT_ARROW = pygame.image.load('left_arrow.png')
RIGHT_ARROW = pygame.image.load('right_arrow.png')

# 所有箭头的元组
ARROWS = (UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW)

# 加载判定线
JUDGE_LINE = pygame.image.load('judge_line.png')
judge_line_rect = JUDGE_LINE.get_rect()
judge_line_rect.bottom = 675

# 四色判定线
JUDGE_LINE_PINK = pygame.image.load('judge_line_pink.png')
JUDGE_LINE_BLUE = pygame.image.load('judge_line_blue.png')
JUDGE_LINE_GREEN = pygame.image.load('judge_line_green.png')
JUDGE_LINE_YELLOW = pygame.image.load('judge_line_yellow.png')

# DIY按钮图片加载
BUTTON_BLACK = pygame.image.load('button_black.png')
BUTTON_RED = pygame.image.load('button_red.png')

# 用于选定菜单的变量，在menu()和choose song()里调用
tag = 0

# 记录运行哪一部分的变量，最开始是menu既菜单界面，还有play，song（选歌），diy_song(为DIY模式选歌)，diy(DIY模式)，play（进行游戏），record（查看记录）
part = 'menu'

# 记录打开哪一首歌的变量
filename = 'flower dance.txt'

# 该变量获取所有歌的列表
songs = os.listdir('./beats')

# 在play()里调用，用来记录命中状态
good = False
great = False
perfect = False
miss = False

# 在play()里调用，保存所有产生的箭头
arrows = []

# 记录开始的时间点
time_0 = time.clock()

# 记录DIY模式下玩家敲入的节奏
diy_beats = []

# 记录当前被选择的歌的歌名的变量，在choose song()里调用
song_name = ''

# 在play里调用，保存从文件中获取的节拍
rhythms = []

# 在play()里调用，记录Miss的次数
miss_count = 0

# 这三个都是查询记录时用到的
records = []
record_rects = []
record_texts = []

# DIY模式时的辅助变量，记录按钮变红的时长
red_lasting_time = 0

# 在DIY模式中表示状态，running表示正在录入节拍，'type in filename'表示输入文件名保存
state = 'running'

# 在DIY模式输入文件名时，记录玩家输入的字符的字符串
input_string = ''


# 主循环
def main():
    while True:
        if part == 'menu':
            menu()
        elif part == 'song' or part == 'diy_song':
            choose_song()
        elif part == 'play':
            play()
        elif part == 'diy':
            diy()
        elif part == 'record':
            record()

        pygame.display.update()
        fps_clock.tick(FPS)


'''
思路：
背景直接加载图片绘制。
用一个tag变量来记录哪一个选项被选中，tag有三个值0，1，2.分别对应了图上的PLAY,DIY,RECORD三个选项。在事件处理中，玩家按下UP键怎tag – 1,
按DOWN键则tag+1，表示改变选项，根据tag值，把被选中的选项渲染成红色字体，其他选项渲染成白色字体。最后把渲染好的字体绘制到屏幕上。最后当玩
家按下回车键既做出选择时，根据tag值判断选中哪一个选项，并依次将part变量由‘menu’改为别的部分，比如‘record’，‘song’等，并做出一定的预处
理，比如从文件中读取别的模块将要用到的数据。由于part变量改变，在下一次循环时便会进入游戏的其它模块。
'''


def menu():
    '''获取全局变量'''

    global play_title_text, diy_title_text, record_title_text, tag, part, SCREEN, score, score_text, BACKGROUND, \
        GOOD, GREAT, PERFECT, songs, TITLE, miss, records, record_rects, record_texts

    '''tag用来记录是哪一个选项被选中，值为0表示play, 1表示diy， 2表示record,
       当选项被选中时，fontObj_100.render（用于渲染字体）函数的颜色参数会传入
       红色既RED， 画面中字体会变为红色，其它的没被选中的字体则为白色。'''

    if tag == 0:
        play_title_text = fontObj_100.render('PLAY', True, RED)
        diy_title_text = fontObj_100.render('DIY', True, WHITE)
        record_title_text = fontObj_100.render('RECORD', True, WHITE)
    elif tag == 1:
        play_title_text = fontObj_100.render('PLAY', True, WHITE)
        diy_title_text = fontObj_100.render('DIY', True, RED)
        record_title_text = fontObj_100.render('RECORD', True, WHITE)
    elif tag == 2:
        play_title_text = fontObj_100.render('PLAY', True, WHITE)
        diy_title_text = fontObj_100.render('DIY', True, WHITE)
        record_title_text = fontObj_100.render('RECORD', True, RED)

    '''以下四个SCREEN.blit调用在SCREEN（既代表屏幕的SURFACE对象）上绘图'''

    SCREEN.blit(TITLE, (0, 0))  # 绘制背景
    SCREEN.blit(play_title_text, play_title_text_rect)  # 绘制PLAY选项
    SCREEN.blit(diy_title_text, diy_title_text_rect)  # 绘制DIY选项
    SCREEN.blit(record_title_text, record_title_text_rect)  # 绘制RECORD选项

    '''事件处理的for循环，功能是当关闭窗口时退出游戏，当按下上下键时对tag加1或减1来改变选中的选项
    当按下回车键时（事件为K_RETURN），根据不同的tag来改变part变量，进入不同的部分'''

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                if tag > 0:
                    tag -= 1
            elif event.key == K_SPACE:
                pygame.mixer.music.load('bgm.ogg')
                pygame.mixer.music.play(-1, 0.0)
            elif event.key == K_DOWN:
                if tag < 2:
                    tag += 1
            elif event.key == K_RETURN:
                SCREEN.blit(PURE_TITLE, (0, 0))
                if tag == 0:
                    songs = os.listdir('./beats')  # 这个函数获取对应文件夹下所有的文件名的一个列表，存入到songs变量里，用于在choose song()中显示歌曲列表
                    part = 'song'
                if tag == 1:
                    songs = os.listdir('./beats')
                    part = 'diy_song'
                    tag = 0
                if tag == 2:
                    # 从record.txt中读取得分纪录，并生成对应字体对象，在record()中，只要直接绘制这些字体对象既可
                    with open('record.txt', 'r') as file:
                        records = file.readlines()
                    for i in range(len(records)):
                        record_text = fontObj_60.render(records[i].strip(), True, WHITE)
                        record_texts.append(record_text)
                        record_text_rect = record_text.get_rect()
                        record_text_rect.centerx = 510
                        record_text_rect.centery = 70 + (i * 50)
                        record_rects.append(record_text_rect)
                    print(records)
                    part = 'record'
                    tag = 0


'''
思路：
与menu()的思路是类似的。
'''


def choose_song():
    '''获取全局变量'''

    global songs, filename, tag, part, SCREEN, score, score_text, \
        BACKGROUND, GOOD, GREAT, PERFECT, part, songs, time_0, song_name, rhythms

    '''事件处理的for循环，功能是当关闭窗口时退出游戏，当按下上下键时对tag加1或减1来改变选中的选项
    当按下回车键时（事件为K_RETURN），根据不同的tag来改变part变量，进入不同的部分'''

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                if tag > 0:
                    tag -= 1
            elif event.key == K_DOWN:
                tag += 1
            elif event.key == K_RETURN:
                SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 将窗口大小改为游戏时的大小
                filename = songs[tag]  # 被选择的节奏文件

                '''同一首歌分为歌曲文件（MP3），保存在song文件夹，和节奏文件（txt），
                   保存在beats文件夹，节奏文件就是记录了一堆时间点的文件，song目录里的
                   index.txt文件则记录了歌曲文件和节奏文件的对应关系，根据此文件的内容
                   加载与节奏文件对应的歌曲'''

                with open('./song/index.txt', 'r') as file:
                    temp = file.readlines()
                for name in temp:
                    if name.split(':')[0] == filename:
                        song_name = name.split(':')[1].strip()
                pygame.mixer.music.load('./song/' + song_name)  # 根据选择的歌曲名，加载并播放对应的MP3文件
                pygame.mixer.music.play(1, 0.0)
                time_0 = time.clock()  # 开始计时
                if part == 'song':  # 从节奏文件中获取节拍，存到rhythms数组里
                    rhythms = []
                    with open('./beats/' + filename, 'r') as file:
                        temp = file.readlines()
                    for rhythm in temp:
                        rhythms.append(float(rhythm.strip()))
                    del temp
                    part = 'play'
                if part == 'diy_song':
                    part = 'diy'

    '''这个for循环将歌曲列表的内容绘制到SCREEN上'''

    for i in range(len(songs)):
        if i == tag:
            song_text = fontObj_100.render(songs[i][0:-4], True, RED)
        else:
            song_text = fontObj_100.render(songs[i][0:-4], True, WHITE)
        song_text_rect = song_text.get_rect()
        song_text_rect.centerx = 490
        song_text_rect.centery = 70 + (i * 50)
        SCREEN.blit(song_text, song_text_rect)


'''
思路：
背景和底下的四个判定圈这些固定内容直接绘制到屏幕上。时间节点已经全部存入到rhythms列表里，通过time.clock()获取当前时间并减去起始时间点，
当得到的差与列表里的时间值相同时（误差为0.25），调用generate_arrow()生成一个随机的箭头对象（实际上是一个pygame.Rect对象），并存入到
arrows列表里。同时rhythms里删除此时间点。每一轮都用一个for循环遍历arrows列表，将列表里的箭头都向下偏移一个固定值（定义在OFFSET变量里）
，然后将箭头绘制到屏幕上。事件处理中，当玩家按下上下左右这四个键中的一个时，判断此刻是否有箭头到达判定圈的位置，如果有，再看这个箭头是否
与玩家按下的键对应，如果对应，则得分，得分的多少取决于箭头与判定圈的重合程度。分为miss,good,great,perfect,四档。这四档分别有四个同名的
布尔变量，当其为True时，会在屏幕上绘制相应的图片，以此告诉玩家得分情况。同时玩家的得分也在不断地更新，每一轮都会被重新渲染，最后绘制到屏幕上。
最后，当rhythms里已经没有时间点，或者玩家miss的次数过多，游戏就结束，这时会在屏幕上绘制“you score is”加上得分来表示游戏结果。玩家再按下
回车键时会把结果写入到record.txt中，并把part变量改为’menu’，返回到菜单界面
'''


def play():
    global arrows, good, great, perfect, SCREEN, score, score_text, miss_count, \
        BACKGROUND, GOOD, GREAT, PERFECT, part, songs, time_0, rhythms, miss, result_text

    '''根据rhythms列表里记录的时间点，在对应时间生成一个方向随机的箭头，并加入到
       arrows列表中，每生成一个箭头，rhythms列表就减少一个时间点'''
    if len(rhythms) != 0 and abs((time.clock() - time_0) - (rhythms[0] - 2.8)) <= 0.25:
        arrows.append(generate_arrow(random.choice(ARROWS)))
        rhythms.pop(0)

    '''以下三个SCREEN.blit绘制背景，得分，和判定圈'''
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(score_text, score_text_rect)
    SCREEN.blit(JUDGE_LINE, judge_line_rect)

    hit = False  # 这个变量表示是否命中

    # pygame.draw.line(SCREEN, (255, 255, 255), (0, 635), (511, 635), 1)
    # pygame.draw.line(SCREEN, (255, 255, 255), (0, 610), (511, 610), 1)
    # pygame.draw.line(SCREEN, (255, 255, 255), (0, 595), (511, 595), 1)
    # pygame.draw.line(SCREEN, (255, 255, 255), (0, 580), (511, 580), 1)
    # 上述为用来编写判定函数的辅助线，只在测试时才使用

    '''当rhythms列表为空，或者失误次数超过30次，游戏结束，显示得分
       ，此时按下回车键会把得分纪录写入到record.txt中，并返回菜单界面'''
    if len(rhythms) == 0 or miss_count >= 30:
        SCREEN.blit(result_text, result_text_rect)
        SCREEN.blit(score_text, score_text_rect.move((-145, 340)))
        good = False
        great = False
        perfect = False
        miss = False
        miss_count = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    with open('record.txt', 'a') as file:
                        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(score) + '\n')
                    SCREEN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    part = 'menu'

    '''事件处理，主要是对玩家按下按键时是否得分进行判定，根据按下的时机的
       精确程度的不同，分为good,great,perfect三档以及miss失误，不同档获得不同的分数'''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            for arrow in arrows:
                predicate = (arrow.top + arrow.bottom) / 2
                if (arrow.left == 10 and event.key == pygame.K_LEFT) or (
                                arrow.left == 111 and event.key == pygame.K_UP) or (
                                arrow.left == 220 and event.key == pygame.K_DOWN) or (
                                arrow.left == 360 and event.key == pygame.K_RIGHT):
                    if 595 > predicate > 580:
                        score += 60
                        score_text = fontObj_60.render(str(score), True, WHITE)  # 这里是刷新分数，后面几个同理
                        good = True
                        great = False
                        perfect = False
                        hit = True
                        arrows.remove(arrow)
                    elif 610 > predicate >= 595:
                        score += 80
                        score_text = fontObj_60.render(str(score), True, WHITE)
                        good = False
                        great = True
                        perfect = False
                        hit = True
                        arrows.remove(arrow)
                    elif 635 > predicate >= 610:
                        score += 100
                        score_text = fontObj_60.render(str(score), True, WHITE)
                        good = False
                        great = False
                        perfect = True
                        hit = True
                        arrows.remove(arrow)

            '''如果没有命中，失误数加一，且good,great,perfect置为false，如果命中，则显示一个命中的特效'''
            if not hit:
                good = False
                great = False
                perfect = False
                miss = True
                miss_count += 1
            else:
                if event.key == pygame.K_UP:
                    SCREEN.blit(JUDGE_LINE_GREEN, judge_line_rect)
                elif event.key == pygame.K_LEFT:
                    SCREEN.blit(JUDGE_LINE_PINK, judge_line_rect)
                elif event.key == pygame.K_DOWN:
                    SCREEN.blit(JUDGE_LINE_YELLOW, judge_line_rect)
                elif event.key == pygame.K_RIGHT:
                    SCREEN.blit(JUDGE_LINE_BLUE, judge_line_rect)

    '''该for循环遍历arrows数组，使得箭头向下偏移一个OFFSET，并在SCREEN上绘制箭头'''
    for index in range(len(arrows)):
        if arrows[index].left == 10 and arrows[index].top < 710:
            SCREEN.blit(LEFT_ARROW, arrows[index])
        if arrows[index].left == 111 and arrows[index].top < 710:
            SCREEN.blit(UP_ARROW, arrows[index])
        if arrows[index].left == 220 and arrows[index].top < 710:
            SCREEN.blit(DOWN_ARROW, arrows[index])
        if arrows[index].left == 360 and arrows[index].top < 710:
            SCREEN.blit(RIGHT_ARROW, arrows[index])
        arrows[index] = arrows[index].move(OFFSET)

    '''删除超出屏幕范围的箭头'''
    for arrow in arrows:
        if arrow.top >= 710:
            arrows.remove(arrow)

    '''显示good,great,perfect'''
    if good:
        SCREEN.blit(GOOD, (70, 250))
    elif great:
        SCREEN.blit(GREAT, (70, 250))
    elif perfect:
        SCREEN.blit(PERFECT, (105, 275))
    elif miss:
        SCREEN.blit(MISS, (70, 250))  # 生成箭头位置


# 生成箭头的函数，在play（）里调用
def generate_arrow(arrow):
    rect = LEFT_ARROW.get_rect()
    if arrow == LEFT_ARROW:
        rect.left = 10
        return rect
    if arrow == UP_ARROW:
        rect.left = 111
        return rect
    if arrow == DOWN_ARROW:
        rect.left = 220
        return rect
    if arrow == RIGHT_ARROW:
        rect.left = 360
        return rect


'''
思路：先绘制背景。在中间绘制一个按钮的图片，玩家没有按下空格键时，加载黑色按钮的图片，玩家按下时，则加载红色按钮的图片，达到一个按钮被按下的效果。这其中要注意的是，
如果只是在玩家按下按钮的那一次循环中加载红色按钮，效果会因为红色消失过快而很不明显，需要让红色按钮加载的时间长一些，所以用一个red_lasting_time来记录红色按钮的显示时
间，每次玩家按下空格时，这个值置为10，然后每一轮都会减一直到0为止，当这个值大于0时，就加载红色按钮，否则加载黑色按钮。玩家按下空格键时还会通过time.clock()减去起始时
间点获得当前时间点，并存入到diy_beats列表里。当玩家按下ESC键时，进入保存的流程，需要玩家键入文件名，由于pygame没有提供文本输入框，所以是通过按键事件来获取用户输入的
（使用chr函数，见代码）。当玩家输入完文件名并按下回车键，则根据文件名生成一个新的文件，然后把diy_beats里的时间点写入，保存，更该part变量为menu，回到菜单界面。
'''


def diy():
    global part, time_0, song_name, SCREEN, red_lasting_time, state, input_string
    SCREEN.blit(BACKGROUND, (0, 0))

    '''这部分用于显示按钮，屏幕上的按钮是黑色，当玩家按下空格键记录节奏点时会变成红色一小段时间（按钮被按下的效果）'''
    if red_lasting_time > 0:
        SCREEN.blit(BUTTON_RED, (220, 500))
        red_lasting_time -= 1
    else:
        SCREEN.blit(BUTTON_BLACK, (220, 500))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            '''事件处理，当按下空格键且状态是running时，会把此时的时间点加入到diy_beats列表里'''
            if event.key == K_SPACE and state == 'running':
                t = str(time.clock() - time_0)
                diy_beats.append(t)
                red_lasting_time = 10
                print(t)
            elif event.key == K_ESCAPE:
                '''当按下ESC键时，状态转为type in filename，让玩家输入文件名'''
                if state == 'running':
                    state = 'type in filename'
            elif event.key == K_RETURN:
                if state == 'type in filename':
                    if input_string == '':
                        input_string = 'DIY'
                    with open('./beats/' + input_string + '.txt', 'w') as file:
                        for beat in diy_beats:
                            file.write(beat + '\n')
                    with open('./song/index.txt', 'a') as file:
                        file.write('\n' + input_string + '.txt:' + song_name)
                    SCREEN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    red_lasting_time = 0
                    state = 'running'
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    part = 'menu'
            elif event.key == K_BACKSPACE:  # 这里的操作是当玩家按下BACKSPACE键时，删去字符串的最后一个字符
                input_string = input_string[0:-1]
                '''状态为type in filename时，除了回车以外的输入都通过chr函数转换为字符存储到input_string里。
                pygame里面案件的时间都定义为对应的ASCII码，比如按键0的对应事件为K_0,K_0的值为48，正好是0的ASCII码。
                所以通过chr函数，就可以获得此按键对应的输入'''
            elif state == 'type in filename':
                input_string += chr(event.key)

    '''将用户输入的文件名回显到屏幕上'''
    if state == 'type in filename':
        input_text = fontObj_40.render('Filename:' + input_string, True, WHITE)
        input_text_rect = input_text.get_rect()
        input_text_rect.centerx = 260
        input_text_rect.centery = 350
        SCREEN.blit(input_text, input_text_rect)


'''直接把 record_rects, record_texts里的内容绘制到屏幕上即可，数据在之前已提取'''


def record():
    global part, record_rects, record_texts
    for i in range(len(record_rects)):
        SCREEN.blit(record_texts[i], record_rects[i])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                part = 'menu'


if __name__ == "__main__":
    main()
