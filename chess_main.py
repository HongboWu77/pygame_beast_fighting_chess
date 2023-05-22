import pygame.sprite
import chess_sprites
from chess_sprites import *


class BeastGame(object):
    """斗兽棋主游戏"""

    # 游戏初始化：创建游戏窗口、定义游戏标题、创建游戏初始界面
    def __init__(self):
        print("游戏初始化...")
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_RECT.size)
        pygame.display.set_caption("10组的斗兽棋")
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        self.__update_sprites()
        self.__status_deliver()
        pygame.display.update()
        # 设置定时器时间，玩家1与玩家2每轮有60s的思考时间，若未选择，则自动选择一枚棋子向前移动
        # pygame.time.set_timer(TURN_ANOTHER_PLAYER, 5000)

    # 游戏进程：事件监测=>（游戏开始）动物竞争=>胜负判定=>更新游戏元素=>更新状态提示=>刷新屏幕
    def game_line(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # self.cat_game_status()
            self.__event_handler()
            if chess_sprites.start_game_flag == 1:
                self.__struggle_animals()
                self.__game_win()
            self.__update_sprites()
            self.__status_deliver()
            pygame.display.update()

    # 创建对应精灵和精灵组(胜败图标、游戏按钮、背景、动物等)
    def __create_sprites(self):
        # 胜败图标
        self.win_1 = GameSprite("./beast_images/true.png", (player1_win_rect[0]*BOX_ROW_LEN, player1_win_rect[1]*BOX_LINE_LEN))
        self.false_1 = GameSprite("./beast_images/false.png", (player1_win_rect[0]*BOX_ROW_LEN, player1_win_rect[1]*BOX_LINE_LEN))
        self.win_2 = GameSprite("./beast_images/true.png", (player2_win_rect[0]*BOX_ROW_LEN, player2_win_rect[1]*BOX_LINE_LEN))
        self.false_2 = GameSprite("./beast_images/false.png", (player2_win_rect[0]*BOX_ROW_LEN, player2_win_rect[1]*BOX_LINE_LEN))
        self.player1_win = pygame.sprite.Group(self.win_1, self.false_2)
        self.player2_win = pygame.sprite.Group(self.win_2, self.false_1)
        # 游戏按钮
        self.button_start = GameSprite("./beast_images/start_game_button.png", (start_button_rect[0]*BOX_ROW_LEN, start_button_rect[1]*BOX_LINE_LEN))
        self.button_quit = GameSprite("./beast_images/quit_game_button.png", (quit_button_rect[0]*BOX_ROW_LEN, quit_button_rect[1]*BOX_LINE_LEN))
        self.button_restart = GameSprite("./beast_images/restart_game_button.png", (restart_button_rect[0]*BOX_ROW_LEN, restart_button_rect[1]*BOX_LINE_LEN))
        self.button_group = pygame.sprite.Group(self.button_start, self.button_quit, self.button_restart)
        # 创建背景精灵
        self.back_1 = BackSprite("./beast_images/back.png", (0, 0))
        self.back_2 = BackSprite("./beast_images/右边背景图.jpg", (648, 0))
        # 将背景精灵加入背景精灵组
        self.back_group = pygame.sprite.Group(self.back_1, self.back_2)
        # 创建玩家一的动物精灵
        self.mouse_1 = AnimalSprite("./beast_images/mouse_1.png", 1, player_1[0])
        self.cat_1 = AnimalSprite("./beast_images/cat_1.png", 2, player_1[1])
        self.dog_1 = AnimalSprite("./beast_images/dog_1.png", 3, player_1[2])
        self.wolf_1 = AnimalSprite("./beast_images/wolf_1.png", 4, player_1[3])
        self.leopard_1 = AnimalSprite("./beast_images/leopard_1.png", 5, player_1[4])
        self.tigger_1 = AnimalSprite("./beast_images/tigger_1.png", 6, player_1[5])
        self.lion_1 = AnimalSprite("./beast_images/lion_1.png", 7, player_1[6])
        self.elephant_1 = AnimalSprite("./beast_images/elephant_1.png", 8, player_1[7])
        # 创建玩家二的动物精灵
        self.mouse_2 = AnimalSprite("./beast_images/mouse_2.png", 1, player_2[0])
        self.cat_2 = AnimalSprite("./beast_images/cat_2.png", 2, player_2[1])
        self.dog_2 = AnimalSprite("./beast_images/dog_2.png", 3, player_2[2])
        self.wolf_2 = AnimalSprite("./beast_images/wolf_2.png", 4, player_2[3])
        self.leopard_2 = AnimalSprite("./beast_images/leopard_2.png", 5, player_2[4])
        self.tigger_2 = AnimalSprite("./beast_images/tigger_2.png", 6, player_2[5])
        self.lion_2 = AnimalSprite("./beast_images/lion_2.png", 7, player_2[6])
        self.elephant_2 = AnimalSprite("./beast_images/elephant_2.png", 8, player_2[7])
        # 将动物精灵加入动物精灵组
        self.animal_1 = pygame.sprite.Group(self.mouse_1, self.cat_1, self.dog_1, self.wolf_1, self.leopard_1, self.tigger_1, self.lion_1, self.elephant_1)
        self.animal_2 = pygame.sprite.Group(self.mouse_2, self.cat_2, self.dog_2, self.wolf_2, self.leopard_2, self.tigger_2, self.lion_2, self.elephant_2)

    # 更新游戏元素，并对游戏元素进行绘制
    def __update_sprites(self):
        # 背景图的绘制
        self.back_group.draw(self.screen)
        # 游戏按钮的绘制
        self.button_group.draw(self.screen)
        # 玩家一动物的位置更新
        self.mouse_1.update(chess_sprites.player_1[0])
        self.cat_1.update(chess_sprites.player_1[1])
        self.dog_1.update(chess_sprites.player_1[2])
        self.wolf_1.update(chess_sprites.player_1[3])
        self.leopard_1.update(chess_sprites.player_1[4])
        self.tigger_1.update(chess_sprites.player_1[5])
        self.lion_1.update(chess_sprites.player_1[6])
        self.elephant_1.update(chess_sprites.player_1[7])
        # 玩家一动物的绘制
        self.animal_1.draw(self.screen)
        # 玩家二动物的位置更新
        self.mouse_2.update(chess_sprites.player_2[0])
        self.cat_2.update(chess_sprites.player_2[1])
        self.dog_2.update(chess_sprites.player_2[2])
        self.wolf_2.update(chess_sprites.player_2[3])
        self.leopard_2.update(chess_sprites.player_2[4])
        self.tigger_2.update(chess_sprites.player_2[5])
        self.lion_2.update(chess_sprites.player_2[6])
        self.elephant_2.update(chess_sprites.player_2[7])
        # 玩家二动物的绘制
        self.animal_2.draw(self.screen)
        # 胜败图标的绘制
        if chess_sprites.res_game_flag == 1:
            self.player1_win.draw(self.screen)
        elif chess_sprites.res_game_flag == 2:
            self.player2_win.draw(self.screen)

    # 更新并绘制状态提示(欢迎语、游戏进行状态、下棋提示、胜负状态等)
    def __status_deliver(self):
        # 欢迎
        welcome_font = pygame.font.SysFont("lisu", 36)
        welcome_font_image = welcome_font.render("欢迎来到斗兽棋!!!", True, (0, 0, 255))
        # 状态提示
        status_font = pygame.font.SysFont("lisu", 36)
        status_font_image_1 = status_font.render("等待玩家1出棋", True, (255, 0, 0))
        status_font_image_2 = status_font.render("等待玩家2出棋", True, (255, 0, 0))
        status_font_image_wait = status_font.render("游戏未开始", True, (255, 0, 0))
        status_font_image_exit = status_font.render("游戏已结束", True, (255, 0, 0))
        # 结局提示
        win_font = pygame.font.SysFont("lisu", 36)
        win_font_image_1 = win_font.render("胜利玩家：玩家1", True, (255, 0, 0))
        win_font_image_2 = win_font.render("胜利玩家：玩家2", True, (255, 0, 0))
        win_font_image_temp = win_font.render("胜利玩家：待定", True, (0, 0, 255))
        # 渲染欢迎语
        self.screen.blit(welcome_font_image,
                         (chess_sprites.welcome_font_rect[0] * BOX_ROW_LEN, chess_sprites.welcome_font_rect[1] * BOX_LINE_LEN))
        # 渲染状态提示
        if chess_sprites.start_game_flag == 0:
            if chess_sprites.res_game_flag == 0:
                self.screen.blit(status_font_image_wait,(chess_sprites.status_font_rect[0] * BOX_ROW_LEN, chess_sprites.status_font_rect[1] * BOX_LINE_LEN))
                self.screen.blit(win_font_image_temp,(chess_sprites.win_font_rect[0]*BOX_ROW_LEN, chess_sprites.win_font_rect[1]*BOX_LINE_LEN))
            elif chess_sprites.res_game_flag == 1:
                self.screen.blit(status_font_image_exit, (chess_sprites.status_font_rect[0] * BOX_ROW_LEN, chess_sprites.status_font_rect[1] * BOX_LINE_LEN))
                self.screen.blit(win_font_image_1, (chess_sprites.win_font_rect[0] * BOX_ROW_LEN, chess_sprites.win_font_rect[1] * BOX_LINE_LEN))
            elif chess_sprites.res_game_flag == 2:
                self.screen.blit(status_font_image_exit, (chess_sprites.status_font_rect[0] * BOX_ROW_LEN, chess_sprites.status_font_rect[1] * BOX_LINE_LEN))
                self.screen.blit(win_font_image_2, (chess_sprites.win_font_rect[0] * BOX_ROW_LEN, chess_sprites.win_font_rect[1] * BOX_LINE_LEN))
        elif chess_sprites.start_game_flag == 1:
            if chess_sprites.TAG == 0:
                self.screen.blit(status_font_image_1, (chess_sprites.status_font_rect[0] * BOX_ROW_LEN,chess_sprites.status_font_rect[1] * BOX_LINE_LEN))
                self.screen.blit(win_font_image_temp, (chess_sprites.win_font_rect[0] * BOX_ROW_LEN, chess_sprites.win_font_rect[1] * BOX_LINE_LEN))
            elif chess_sprites.TAG == 1:
                self.screen.blit(status_font_image_2, (chess_sprites.status_font_rect[0] * BOX_ROW_LEN,chess_sprites.status_font_rect[1] * BOX_LINE_LEN))
                self.screen.blit(win_font_image_temp, (chess_sprites.win_font_rect[0] * BOX_ROW_LEN, chess_sprites.win_font_rect[1] * BOX_LINE_LEN))

    # 游戏状态以及变量的初始化
    def __init_game(self):
        chess_sprites.player_1 = [(padding, 2*BOX_LINE_LEN+padding), (5*BOX_ROW_LEN+padding, BOX_LINE_LEN+padding),
            (BOX_ROW_LEN+padding, BOX_LINE_LEN+padding),(4*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding),
            (2*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding), (6*BOX_ROW_LEN+padding, padding),
            (padding, padding), (6*BOX_ROW_LEN+padding, 2*BOX_LINE_LEN+padding)]
        chess_sprites.player_2 = [(6*BOX_LINE_LEN+padding, 6*BOX_LINE_LEN+padding), (BOX_ROW_LEN+padding, 7*BOX_LINE_LEN+padding),
            (5*BOX_ROW_LEN+padding, 7*BOX_LINE_LEN+padding), (2*BOX_ROW_LEN+padding, 6*BOX_LINE_LEN+padding),
            (4*BOX_ROW_LEN+padding, 6*BOX_LINE_LEN+padding), (padding, 8*BOX_LINE_LEN+padding),
            (6*BOX_ROW_LEN+padding, 8*BOX_LINE_LEN+padding), (padding, 6*BOX_LINE_LEN+padding)]
        chess_sprites.FLAG = 0
        chess_sprites.TAG = 0
        chess_sprites.mx = 0
        chess_sprites.my = 0
        self.animal_1.empty()
        self.animal_2.empty()
        self.animal_1.add(self.mouse_1, self.cat_1, self.dog_1, self.wolf_1, self.leopard_1, self.tigger_1, self.lion_1, self.elephant_1)
        self.animal_2.add(self.mouse_2, self.cat_2, self.dog_2, self.wolf_2, self.leopard_2, self.tigger_2, self.lion_2, self.elephant_2)
        
    # 棋盘移动限制的定义(例如只有老鼠可以过河、老虎和狮子可以跨河、其他动物只能走路)
    def __limit_move(self, event):
        if chess_sprites.my > chess_sprites.pre_my:
            chess_sprites.my = chess_sprites.pre_my + 1
            chess_sprites.mx = chess_sprites.pre_mx
        elif chess_sprites.my == chess_sprites.pre_my:
            if chess_sprites.mx > chess_sprites.pre_mx:
                chess_sprites.my = chess_sprites.pre_my
                chess_sprites.mx = chess_sprites.pre_mx + 1
            elif chess_sprites.mx < chess_sprites.pre_mx:
                chess_sprites.my = chess_sprites.pre_my
                chess_sprites.mx = chess_sprites.pre_mx - 1
            elif chess_sprites.mx == chess_sprites.pre_mx:
                if chess_sprites.TAG == 0:
                    chess_sprites.my = chess_sprites.pre_my + 1
                elif chess_sprites.TAG == 1:
                    chess_sprites.my = chess_sprites.pre_my - 1
                chess_sprites.mx = chess_sprites.pre_mx
        elif chess_sprites.my < chess_sprites.pre_my:
            chess_sprites.my = chess_sprites.pre_my - 1
            chess_sprites.mx = chess_sprites.pre_mx
        if chess_sprites.FLAG in [0]:
            print("0")
            pass
        elif chess_sprites.FLAG in [5, 6]:
            print("5、6")
            if (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_top_rect:
                if chess_sprites.my == chess_sprites.pre_my + 1:
                    chess_sprites.my = chess_sprites.pre_my + 4
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_bottom_rect:
                if chess_sprites.my == chess_sprites.pre_my - 1:
                    chess_sprites.my = chess_sprites.pre_my - 4
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_left_rect:
                if chess_sprites.mx == chess_sprites.pre_mx + 1:
                    chess_sprites.mx = chess_sprites.pre_mx + 3
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_right_rect:
                if chess_sprites.mx == chess_sprites.pre_mx - 1:
                    chess_sprites.mx = chess_sprites.pre_mx - 3
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_middle_rect:
                if chess_sprites.mx == chess_sprites.pre_mx + 1:
                    chess_sprites.mx = chess_sprites.pre_mx + 3
                elif chess_sprites.mx == chess_sprites.pre_mx - 1:
                    chess_sprites.mx = chess_sprites.pre_mx - 3
        elif chess_sprites.FLAG in [1, 2, 3, 4, 7]:
            print("1、2、3、4、7")
            if (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_top_rect:
                if chess_sprites.my == chess_sprites.pre_my + 1:
                    if event.pos[0] // BOX_ROW_LEN > chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx + 1
                    elif event.pos[0] // BOX_ROW_LEN < chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx - 1
                    elif event.pos[0] // BOX_ROW_LEN == chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx + 1
                    chess_sprites.my = chess_sprites.pre_my
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_bottom_rect:
                if chess_sprites.my == chess_sprites.pre_my - 1:
                    if event.pos[0] // BOX_ROW_LEN > chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx + 1
                    elif event.pos[0] // BOX_ROW_LEN < chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx - 1
                    elif event.pos[0] // BOX_ROW_LEN == chess_sprites.pre_mx:
                        chess_sprites.mx = chess_sprites.pre_mx - 1
                    chess_sprites.my = chess_sprites.pre_my
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_left_rect:
                if chess_sprites.mx == chess_sprites.pre_mx + 1:
                    if chess_sprites.TAG == 0:
                        chess_sprites.my = chess_sprites.pre_my + 1
                    elif chess_sprites.TAG == 1:
                        chess_sprites.my = chess_sprites.pre_my - 1
                    chess_sprites.mx = chess_sprites.pre_mx
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_right_rect:
                if chess_sprites.mx == chess_sprites.pre_mx - 1:
                    if chess_sprites.TAG == 0:
                        chess_sprites.my = chess_sprites.pre_my + 1
                    elif chess_sprites.TAG == 1:
                        chess_sprites.my = chess_sprites.pre_my - 1
                    chess_sprites.mx = chess_sprites.pre_mx
            elif (chess_sprites.pre_mx, chess_sprites.pre_my) in chess_sprites.river_border_middle_rect:
                if chess_sprites.mx == chess_sprites.pre_mx + 1:
                    if chess_sprites.TAG == 0:
                        chess_sprites.my = chess_sprites.pre_my + 1
                    elif chess_sprites.TAG == 1:
                        chess_sprites.my = chess_sprites.pre_my - 1
                    chess_sprites.mx = chess_sprites.pre_mx
                elif chess_sprites.mx == chess_sprites.pre_mx - 1:
                    if chess_sprites.TAG == 0:
                        chess_sprites.my = chess_sprites.pre_my + 1
                    elif chess_sprites.TAG == 1:
                        chess_sprites.my = chess_sprites.pre_my - 1
                    chess_sprites.mx = chess_sprites.pre_mx

    # 事件监测处理（开始游戏、退出游戏、重新开始游戏、棋子移动等）
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (event.pos[0] // chess_sprites.BOX_ROW_LEN,
                                          event.pos[1] // chess_sprites.BOX_LINE_LEN) == chess_sprites.start_button_rect:
                    if chess_sprites.start_game_flag == 1:
                        print("游戏已开始")
                    elif chess_sprites.start_game_flag == 0:
                        print("游戏开始...")
                        self.__init_game()
                        chess_sprites.res_game_flag = 0
                        chess_sprites.start_game_flag = 1
                        # 不理解这里为什么要刷新
                        self.__update_sprites()
                        pygame.display.update()
                elif event.button == 1 and (event.pos[0] // chess_sprites.BOX_ROW_LEN,
                                            event.pos[1] // chess_sprites.BOX_LINE_LEN) == chess_sprites.quit_button_rect:
                    self.__game_over()
                elif event.button == 1 and (event.pos[0] // chess_sprites.BOX_ROW_LEN,
                                            event.pos[1] // chess_sprites.BOX_LINE_LEN) == chess_sprites.restart_button_rect:
                    print("游戏重新开始...")
                    chess_sprites.start_game_flag = 0
                    self.__init_game()
                    chess_sprites.res_game_flag = 0
                    chess_sprites.start_game_flag = 1
                    # 不理解这里为什么要刷新
                    self.__update_sprites()
                    pygame.display.update()

            if event.type == pygame.QUIT:
                BeastGame.__game_over()

            if chess_sprites.start_game_flag == 1:
                if chess_sprites.TAG == 0:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("玩家", chess_sprites.TAG + 1, "出棋中...")
                        if event.button == 1:
                            # print('鼠标按下左键', event.pos)
                            chess_sprites.mx, chess_sprites.my = event.pos
                            chess_sprites.mx = chess_sprites.mx // BOX_ROW_LEN
                            chess_sprites.my = chess_sprites.my // BOX_LINE_LEN
                            # print('鼠标按下左键', chess_sprites.mx, chess_sprites.my)
                            pygame.draw.circle(self.screen, (255, 0, 0), (chess_sprites.mx+9, chess_sprites.my+9), 9)
                            pygame.display.update()
                            for temp in chess_sprites.player_1:
                                if (temp[0]//BOX_ROW_LEN, temp[1]//BOX_LINE_LEN) == (chess_sprites.mx, chess_sprites.my):
                                    break
                                else:
                                    pass
                                chess_sprites.FLAG += 1
                            if chess_sprites.FLAG > 7:
                                chess_sprites.FLAG = 0
                        if event.button == 3:
                            # print('鼠标按下右键', event.pos)
                            chess_sprites.mx, chess_sprites.my = event.pos
                            chess_sprites.mx = chess_sprites.mx // BOX_ROW_LEN
                            chess_sprites.my = chess_sprites.my // BOX_LINE_LEN
                            chess_sprites.pre_mx = chess_sprites.player_1[chess_sprites.FLAG][0]//BOX_ROW_LEN
                            chess_sprites.pre_my = chess_sprites.player_1[chess_sprites.FLAG][1]//BOX_LINE_LEN
                            self.__limit_move(event)
                            print('鼠标按下右键', chess_sprites.mx, chess_sprites.my)
                            chess_sprites.player_1[chess_sprites.FLAG] = (chess_sprites.mx*BOX_ROW_LEN+padding, chess_sprites.my*BOX_LINE_LEN+padding)
                            chess_sprites.FLAG = 0
                            print("玩家", chess_sprites.TAG + 1, "出棋完成...")
                            chess_sprites.TAG = (chess_sprites.TAG + 1) % 2
                elif chess_sprites.TAG == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("玩家", chess_sprites.TAG + 1, "出棋中...")
                        if event.button == 1:
                            # print('鼠标按下左键', event.pos)
                            chess_sprites.mx, chess_sprites.my = event.pos
                            chess_sprites.mx = chess_sprites.mx // BOX_ROW_LEN
                            chess_sprites.my = chess_sprites.my // BOX_LINE_LEN
                            # print('鼠标按下左键', chess_sprites.mx, chess_sprites.my)
                            pygame.draw.circle(self.screen, (255, 0, 0), (chess_sprites.mx + 9, chess_sprites.my + 9), 9)
                            pygame.display.update()
                            for temp in chess_sprites.player_2:
                                if (temp[0] // BOX_ROW_LEN, temp[1] // BOX_LINE_LEN) == (chess_sprites.mx, chess_sprites.my):
                                    break
                                else:
                                    pass
                                chess_sprites.FLAG += 1
                            if chess_sprites.FLAG > 7:
                                chess_sprites.FLAG = 0
                        if event.button == 3:
                            # print('鼠标按下右键', event.pos)
                            chess_sprites.mx, chess_sprites.my = event.pos
                            chess_sprites.mx = chess_sprites.mx // BOX_ROW_LEN
                            chess_sprites.my = chess_sprites.my // BOX_LINE_LEN
                            chess_sprites.pre_mx = chess_sprites.player_2[chess_sprites.FLAG][0] // BOX_ROW_LEN
                            chess_sprites.pre_my = chess_sprites.player_2[chess_sprites.FLAG][1] // BOX_LINE_LEN
                            self.__limit_move(event)
                            print('鼠标按下右键', chess_sprites.mx, chess_sprites.my)
                            chess_sprites.player_2[chess_sprites.FLAG] = (chess_sprites.mx*BOX_ROW_LEN+padding, chess_sprites.my*BOX_LINE_LEN+padding)
                            chess_sprites.FLAG = 0
                            print("玩家", chess_sprites.TAG + 1, "出棋完成...")
                            chess_sprites.TAG = (chess_sprites.TAG + 1) % 2

    # 棋子相撞判定
    def __struggle_animals(self):
        dicts = pygame.sprite.groupcollide(self.animal_1, self.animal_2, False, False)
        for key, value in dicts.items():
            for temp in chess_sprites.x_rect:
                if (chess_sprites.mx, chess_sprites.my) == (temp[0], temp[1]):
                    if chess_sprites.TAG == 0:
                        self.animal_1.remove(key)
                    elif chess_sprites.TAG == 1:
                        self.animal_2.remove(value[0])
                    return
            if key.animal > value[0].animal:
                if key.animal == 8 and value[0].animal == 1:
                    self.animal_1.remove(key)
                else:
                    self.animal_2.remove(value[0])
            elif key.animal < value[0].animal:
                if key.animal == 1 and value[0].animal == 8:
                    self.animal_2.remove(value[0])
                else:
                    self.animal_1.remove(key)
            elif key.animal == value[0].animal:
                if chess_sprites.TAG == 0:
                    self.animal_1.remove(key)
                elif chess_sprites.TAG == 1:
                    self.animal_2.remove(value[0])

    # 游戏胜负判定
    @staticmethod
    def __game_win():
        if chess_sprites.TAG == 0:
            for temp in chess_sprites.player_2:
                if (temp[0] // BOX_ROW_LEN, temp[1] // BOX_LINE_LEN) == (chess_sprites.player_1_loss_x, chess_sprites.player_1_loss_y):
                    print("玩家2取得胜利...")
                    chess_sprites.res_game_flag = 2
                    chess_sprites.start_game_flag = 0
        elif chess_sprites.TAG == 1:
            for temp in chess_sprites.player_1:
                if (temp[0] // BOX_ROW_LEN, temp[1] // BOX_LINE_LEN) == (chess_sprites.player_2_loss_x, chess_sprites.player_2_loss_y):
                    print("玩家1取得胜利...")
                    chess_sprites.res_game_flag = 1
                    chess_sprites.start_game_flag = 0

    # 游戏结束
    @staticmethod
    def __game_over():
        print("游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = BeastGame()
    # 启动游戏
    game.game_line()
