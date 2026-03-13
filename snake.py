import os
import sys
import time
import random
import msvcrt  # 仅适用于 Windows

# --- 配置 ---
WIDTH = 40   # 游戏区域宽度
HEIGHT = 20  # 游戏区域高度
SPEED = 0.1  # 刷新速度 (秒)，越小越快

# --- 符号定义 ---
HEAD = '🐍'  # 蛇头
BODY = '🟩'  # 蛇身
FOOD = '🍎'  # 食物
EMPTY = ' '  # 空白

# 如果终端不支持 Emoji，可以取消下面注释使用普通字符
# HEAD = '@'
# BODY = 'O'
# FOOD = '*'

def clear_screen():
    """清屏并移动光标到左上角，减少闪烁"""
    # 使用 ANSI 转义序列清屏 (PowerShell 和现代终端支持)
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def get_key():
    """获取键盘输入，处理方向键"""
    if msvcrt.kbhit():
        key = msvcrt.getch()
        # 方向键在 Windows 下通常由两个字节组成，第一个是 0 或 224 (0xe0)
        if key == b'\xe0' or key == b'\x00':
            key = msvcrt.getch()
            if key == b'H': return 'UP'      # ↑
            if key == b'P': return 'DOWN'    # ↓
            if key == b'K': return 'LEFT'    # ←
            if key == b'M': return 'RIGHT'   # →
        else:
            key = key.decode('utf-8', errors='ignore').lower()
            if key == 'w': return 'UP'
            if key == 's': return 'DOWN'
            if key == 'a': return 'LEFT'
            if key == 'd': return 'RIGHT'
            if key == 'q': return 'QUIT'
    return None

def main():
    # 初始化蛇 (居中)
    snake = [(HEIGHT // 2, WIDTH // 2), (HEIGHT // 2, WIDTH // 2 - 1), (HEIGHT // 2, WIDTH // 2 - 2)]
    direction = 'RIGHT'
    food = None
    score = 0
    game_over = False

    # 生成第一个食物
    def spawn_food():
        while True:
            f = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
            if f not in snake:
                return f
    
    food = spawn_food()

    print("正在启动贪吃蛇... 使用方向键或 W/A/S/D 控制，Q 退出。")
    time.sleep(1)

    while not game_over:
        start_time = time.time()
        
        # 1. 处理输入
        key = get_key()
        if key == 'QUIT':
            break
        
        if key:
            # 防止直接反向移动 (例如向右时不能直接向左)
            if key == 'UP' and direction != 'DOWN':
                direction = 'UP'
            elif key == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            elif key == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            elif key == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

        # 2. 计算新头部位置
        head_y, head_x = snake[0]
        if direction == 'UP':
            head_y -= 1
        elif direction == 'DOWN':
            head_y += 1
        elif direction == 'LEFT':
            head_x -= 1
        elif direction == 'RIGHT':
            head_x += 1

        # 3. 碰撞检测 (墙壁或自身)
        if (head_y < 0 or head_y >= HEIGHT or 
            head_x < 0 or head_x >= WIDTH or 
            (head_y, head_x) in snake):
            game_over = True
            break

        # 移动蛇：插入新头部
        snake.insert(0, (head_y, head_x))

        # 4. 吃食物检测
        if (head_y, head_x) == food:
            score += 1
            food = spawn_food()
            # 吃到食物不删除尾部，蛇变长
        else:
            # 没吃到食物，删除尾部，保持长度不变
            snake.pop()

        # 5. 渲染画面
        clear_screen()
        
        # 构建画面缓冲区
        buffer = []
        buffer.append(f"分数: {score} | 速度: {SPEED}s | 控制: 方向键/WASD (Q退出)\n")
        buffer.append("+" + "-" * WIDTH + "+\n")

        for y in range(HEIGHT):
            line = "|"
            for x in range(WIDTH):
                if (y, x) == snake[0]:
                    line += HEAD
                elif (y, x) in snake:
                    line += BODY
                elif (y, x) == food:
                    line += FOOD
                else:
                    line += EMPTY
            line += "|\n"
            buffer.append(line)
        
        buffer.append("+" + "-" * WIDTH + "+\n")
        
        sys.stdout.write("".join(buffer))
        sys.stdout.flush()

        # 6. 控制帧率
        elapsed = time.time() - start_time
        sleep_time = max(0, SPEED - elapsed)
        time.sleep(sleep_time)

    # 游戏结束
    clear_screen()
    print("=" * 30)
    print("游戏结束!")
    print(f"最终得分: {score}")
    print("=" * 30)
    print("按任意键退出...")
    msvcrt.getch()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n游戏被强制中断。")
    except Exception as e:
        print(f"\n发生错误: {e}")
        print("请确保在 Windows PowerShell 中运行此脚本。")