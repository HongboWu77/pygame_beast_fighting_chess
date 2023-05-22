import pygame

"""常量"""
# 窗口大小的常量
WINDOW_RECT = pygame.Rect(0, 0, 1000, 830)
# 棋盘大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 647, 830)
# 屏幕刷新的帧率
FRAME_PER_SEC = 30

# 绘制棋盘与棋子的基础常量
BOARD_HEIGHT = 830
BOARD_WIDTH = 647
BOX_ROW = 7
BOX_LINE = 9
BOX_ROW_LEN = BOARD_WIDTH/BOX_ROW
BOX_LINE_LEN = BOARD_HEIGHT/BOX_LINE
padding = 6

# 玩家1的兽穴坐标
player_1_loss_x = 3
player_1_loss_y = 0
# 玩家2的兽穴坐标
player_2_loss_x = 3
player_2_loss_y = 8

# 棋盘的陷阱坐标
x_rect = [(2, 0), (4, 0), (3, 1), (2, 8), (3, 7), (4, 8)]

# 棋盘的河流位置
river_rect = [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
# 棋盘河流周边位置
river_border_top_rect = [(1, 2), (2, 2), (4, 2), (5, 2)]
river_border_bottom_rect = [(1, 6), (2, 6), (4, 6), (5, 6)]
river_border_left_rect = [(0, 3), (0, 4), (0, 5)]
river_border_middle_rect = [(3, 3), (3, 4), (3, 5)]
river_border_right_rect = [(6, 3), (6, 4), (6, 5)]

# 棋子名称的常量数组
animals = ["mouse", "cat", "dog", "wolf", "leopard", "tiger", "lion", "elephant"]

# 游戏按钮的位置
start_button_rect = (8, 0)
quit_button_rect = (8, 1)
restart_button_rect = (8, 2)

# 状态文字显示位置
welcome_font_rect = (7.3, 3.3)
status_font_rect = (7.3, 4.3)
win_font_rect = (7.3, 5.3)
rules_title_rect = (7.3, 6.3)
rules_content1_rect = (7.3, 7.3)
rules_content2_rect = (7.3, 7.9)
rules_content3_rect = (7.3, 8.5)

# 胜败图标的位置
player1_win_rect = (2, 0)
player2_win_rect = (2, 6)

"""变量"""
# 棋子的坐标
# 鼠(1) 猫(2) 狗(3) 狼(4) 豹(5) 虎(6) 狮(7) 象(8)
player_1 = [(padding, 2*BOX_LINE_LEN+padding), (5*BOX_ROW_LEN+padding, BOX_LINE_LEN+padding),
            (BOX_ROW_LEN+padding, BOX_LINE_LEN+padding), (4*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding),
            (2*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding), (6*BOX_ROW_LEN+padding, padding),
            (padding, padding), (6*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding)]
player_2 = [(6*BOX_LINE_LEN+padding, 6*BOX_LINE_LEN+padding), (BOX_ROW_LEN+padding, 7*BOX_LINE_LEN+padding),
            (5*BOX_ROW_LEN+padding, 7*BOX_LINE_LEN+padding), (2*BOX_ROW_LEN+padding, 6*BOX_LINE_LEN+padding),
            (4*BOX_ROW_LEN+padding, 6*BOX_LINE_LEN+padding), (padding, 8*BOX_LINE_LEN+padding),
            (6*BOX_ROW_LEN+padding, 8*BOX_LINE_LEN+padding), (padding, 6*BOX_LINE_LEN+padding)]

# 切换玩家的定时事件（未使用）
TURN_ANOTHER_PLAYER = pygame.USEREVENT

# 玩家1与玩家2的标志
TAG = 0
# 选中动物的标志
FLAG = 0
# 最新的移动位置
mx = 0
my = 0
# 最新的选中位置
pre_mx = 0
pre_my = 0
# 游戏是否开始的信号(默认0表示未开启)
start_game_flag = 0
# 游戏是否有结果的信号（默认0为无信号）
res_game_flag = 0


class GameSprite(pygame.sprite.Sprite):
    """斗兽棋游戏精灵"""

    def __init__(self, image_name, position):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]


class BackSprite(GameSprite):
    """背景精灵"""

    def __init__(self, image_name, position):
        super().__init__(image_name, position)

    def update(self, position):
        super().update(position)


class AnimalSprite(GameSprite):
    """动物精灵"""

    # 8  7  6  5  4  3  2  1
    # 象(8) 狮(7) 虎(6) 豹(5) 狼(4) 狗(3) 猫(2) 鼠(1) 象(8)
    # 特例：1与8比较，鼠（1）赢
    # 落入陷阱，置为0
    def __init__(self, image_name, animal, position):
        super().__init__(image_name, position)
        self.animal = animal

    def update(self, position):
        super().update(position)

    def __del__(self):
        pass
