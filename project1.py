import pygame
import random

# 初始化pygame
pygame.init()

# 游戏常量定义
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10  # 游戏网格宽度（列数）
GRID_HEIGHT = 20  # 游戏网格高度（行数）

# 颜色定义（RGB）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# 俄罗斯方块形状和颜色（每个形状用坐标列表表示）
SHAPES = [
    [[1, 1, 1, 1]],  # I型
    [[1, 1], [1, 1]],  # O型
    [[1, 1, 1], [0, 1, 0]],  # T型
    [[1, 1, 1], [1, 0, 0]],  # L型
    [[1, 1, 1], [0, 0, 1]],  # J型
    [[1, 1, 0], [0, 1, 1]],  # Z型
    [[0, 1, 1], [1, 1, 0]]   # S型
]
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, RED, GREEN]

# 游戏窗口设置
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python俄罗斯方块")
clock = pygame.time.Clock()

# 字体设置
font = pygame.font.Font(None, 40)

class TetrisGame:
    def __init__(self):
        # 初始化游戏网格（0表示空，其他数字表示不同颜色的方块）
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_shape = None  # 当前下落的方块
        self.current_color = None  # 当前方块颜色
        self.current_x = 0         # 当前方块x坐标（列）
        self.current_y = 0         # 当前方块y坐标（行）
        self.score = 0             # 分数
        self.game_over = False     # 游戏结束标记
        # 生成第一个方块
        self.new_shape()

    def new_shape(self):
        """生成新的俄罗斯方块"""
        # 随机选择形状和颜色
        shape_idx = random.randint(0, len(SHAPES)-1)
        self.current_shape = SHAPES[shape_idx]
        self.current_color = SHAPE_COLORS[shape_idx]
        # 初始位置（网格中间上方）
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

        # 检查是否游戏结束（新方块刚生成就碰撞）
        if self.check_collision(0, 0):
            self.game_over = True

    def check_collision(self, dx, dy):
        """检查方块移动后是否碰撞（边界或已有方块）"""
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy
                    # 检查是否超出左右边界
                    if new_x < 0 or new_x >= GRID_WIDTH:
                        return True
                    # 检查是否超出下边界
                    if new_y >= GRID_HEIGHT:
                        return True
                    # 检查是否和已有方块重叠（排除上方超出的情况）
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def rotate_shape(self):
        """旋转当前方块"""
        # 旋转逻辑：矩阵转置后反转每行
        original_shape = self.current_shape
        # 转置矩阵
        rotated = list(zip(*original_shape[::-1]))
        # 转换为列表（方便操作）
        self.current_shape = [list(row) for row in rotated]
        
        # 如果旋转后碰撞，恢复原形状
        if self.check_collision(0, 0):
            self.current_shape = original_shape

    def lock_shape(self):
        """将当前方块固定到网格中"""
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_y + y][self.current_x + x] = self.current_color
        # 消除满行
        self.clear_lines()
        # 生成新方块
        self.new_shape()

    def clear_lines(self):
        """消除满行并计分"""
        new_grid = []
        lines_cleared = 0
        # 遍历网格，保留未填满的行
        for row in self.grid:
            if all(cell != 0 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        # 补充空行到网格顶部
        while len(new_grid) < GRID_HEIGHT:
            new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.grid = new_grid
        # 计分（消除行数越多，分数越高）
        self.score += lines_cleared * 100

    def draw_grid(self):
        """绘制游戏网格和方块"""
        # 计算网格绘制的起始位置（居中）
        grid_x = SCREEN_WIDTH // 2 - (GRID_WIDTH * BLOCK_SIZE) // 2
        grid_y = 50

        # 绘制网格背景
        pygame.draw.rect(screen, BLACK, (grid_x-2, grid_y-2, GRID_WIDTH*BLOCK_SIZE+4, GRID_HEIGHT*BLOCK_SIZE+4))
        
        # 绘制固定的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                if color:
                    rect = pygame.Rect(
                        grid_x + x*BLOCK_SIZE,
                        grid_y + y*BLOCK_SIZE,
                        BLOCK_SIZE-1,  # -1 留出间隙
                        BLOCK_SIZE-1
                    )
                    pygame.draw.rect(screen, color, rect)

        # 绘制当前下落的方块
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        grid_x + (self.current_x + x)*BLOCK_SIZE,
                        grid_y + (self.current_y + y)*BLOCK_SIZE,
                        BLOCK_SIZE-1,
                        BLOCK_SIZE-1
                    )
                    pygame.draw.rect(screen, self.current_color, rect)

    def draw_ui(self):
        """绘制UI（分数、游戏结束提示）"""
        # 绘制分数
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (600, 100))

        # 绘制操作提示
        tips = [
            "← →: 左右移动",
            "↓: 加速下落",
            "↑: 旋转方块",
            "空格: 直接落地"
        ]
        for i, tip in enumerate(tips):
            tip_text = font.render(tip, True, WHITE)
            screen.blit(tip_text, (600, 200 + i*40))

        # 游戏结束提示
        if self.game_over:
            game_over_text = font.render("游戏结束！按R重新开始", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

    def handle_input(self):
        """处理键盘输入"""
        keys = pygame.key.get_pressed()
        
        # 左右移动
        if keys[pygame.K_LEFT] and not self.check_collision(-1, 0):
            self.current_x -= 1
        if keys[pygame.K_RIGHT] and not self.check_collision(1, 0):
            self.current_x += 1

        # 加速下落
        if keys[pygame.K_DOWN] and not self.check_collision(0, 1):
            self.current_y += 1

        # 旋转
        if keys[pygame.K_UP]:
            self.rotate_shape()

        # 空格直接落地
        if keys[pygame.K_SPACE]:
            while not self.check_collision(0, 1):
                self.current_y += 1
            self.lock_shape()

    def run(self):
        """游戏主循环"""
        fall_time = 0
        fall_speed = 500  # 方块下落间隔（毫秒）

        while True:
            screen.fill((30, 30, 30))  # 背景色
            current_time = pygame.time.get_ticks()

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # 游戏结束后按R重新开始
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.__init__()  # 重置游戏

            if not self.game_over:
                # 处理输入
                self.handle_input()

                # 自动下落
                if current_time - fall_time > fall_speed:
                    if not self.check_collision(0, 1):
                        self.current_y += 1
                    else:
                        self.lock_shape()
                    fall_time = current_time

            # 绘制所有元素
            self.draw_grid()
            self.draw_ui()

            # 更新屏幕
            pygame.display.update()
            clock.tick(60)

# 启动游戏
if __name__ == "__main__":
    game = TetrisGame()
    game.run()

print("new")