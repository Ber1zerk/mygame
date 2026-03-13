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
# 如果终端不支持 Emoji，请取消下方注释并注释掉 Emoji 部分
HEAD = '🐍'  
BODY = '🟩'  
FOOD = '🍎'  
EMPTY = ' '  

# 备用普通字符方案 (如果上面乱码，请切换到这里)
# HEAD = '@'
# BODY = 'O'
# FOOD = '*'
# EMPTY = ' '

def clear_screen():
    """清屏并移动光标到左上角"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def get_key():
    """获取键盘输入，处理方向键"""
    if msvcrt.kbhit():
        key = msvcrt.getch()
        # 方向键在 Windows 下通常由两个字节组成
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
    death_reason = "" # 用于存储死亡原因

    # 生成食物函数
    def spawn_food():
        while True:
            f = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
            if f not in snake:
                return f
    
    food = spawn_food()

    print("正在启动贪吃蛇...")
    print("控制: 方向键 或 W/A/S/D")
    print("目标: 吃 🍎 变长，不要撞墙或咬自己！")
    time.sleep(1.5)

    while not game_over:
        start_time = time.time()
        
        # 1. 处理输入
        key = get_key()
        if key == 'QUIT':
            death_reason = "玩家主动退出 (Q键)"
            game_over = True
            break
        
        if key:
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

        # 3. 碰撞检测 (区分撞墙和咬自己)
        # 检查是否撞墙
        hit_wall = (head_y < 0 or head_y >= HEIGHT or head_x < 0 or head_x >= WIDTH)
        # 检查是否咬到自己 (注意：此时新头还没加入snake列表，所以直接检查是否在旧蛇身中)
        hit_self = (head_y, head_x) in snake

        if hit_wall:
            game_over = True
            death_reason = "💥 撞到了墙壁！"
            break
        
        if hit_self:
            game_over = True
            death_reason = "🤕 咬到了自己！"
            break

        # 移动蛇：插入新头部
        snake.insert(0, (head_y, head_x))

        # 4. 吃食物检测
        if (head_y, head_x) == food:
            score += 1
            food = spawn_food()
            # 吃到食物不删除尾部，蛇变长
        else:
            # 没吃到食物，删除尾部
            snake.pop()

        # 5. 渲染画面
        clear_screen()
        
        buffer = []
        buffer.append(f"分数: {score} | 控制: 方向键/WASD (Q退出)\n")
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

    # --- 游戏结束画面 ---
    clear_screen()
    print("\n" + "=" * 40)
    print("       🎮 游 戏 结 束 🎮")
    print("=" * 40)
    
    # 显示具体的死亡原因
    if death_reason:
        print(f"\n❌ 失败原因：{death_reason}\n")
    else:
        print("\n❌ 未知错误导致游戏结束\n")

    print(f"🏆 最终得分：{score}")
    print("=" * 40)
    print("\n按任意键退出...")
    
    # 等待用户按键
    try:
        msvcrt.getch()
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n游戏被强制中断 (Ctrl+C)。")
    except Exception as e:
        print(f"\n发生未预期的错误: {e}")
        print("请确保在 Windows PowerShell 中运行。")
        input("按回车退出...")