import os
import sys
import time
import random
import math

# --- 全局配置 ---
# 棋盘位置映射
# 1 | 2 | 3
# --+---+--
# 4 | 5 | 6
# 7 | 8 | 9

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """打印当前棋盘"""
    # 为了美观，如果是空格，显示为点或者保持空格但加边框
    display_board = [x if x != " " else "." for x in board]
    
    print("\n   井 字 棋 大 战   \n")
    print(f" {display_board[0]} | {display_board[1]} | {display_board[2]} ")
    print("---+---+---")
    print(f" {display_board[3]} | {display_board[4]} | {display_board[5]} ")
    print("---+---+---")
    print(f" {display_board[6]} | {display_board[7]} | {display_board[8]} ")
    print("\n")

def print_help_board():
    """打印位置参考图"""
    print("位置编号参考:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")

def check_winner(board, mark):
    """检查是否获胜"""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # 横向
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # 纵向
        (0, 4, 8), (2, 4, 6)             # 斜向
    ]
    for a, b, c in win_conditions:
        if board[a] == mark and board[b] == mark and board[c] == mark:
            return True
    return False

def is_board_full(board):
    """检查棋盘是否满了"""
    return " " not in board

def get_available_moves(board):
    """获取所有空位索引"""
    return [i for i, x in enumerate(board) if x == " "]

# --- AI 逻辑 ---

def ai_move_random(board):
    """简单 AI：随机选择一个空位"""
    moves = get_available_moves(board)
    if moves:
        return random.choice(moves)
    return None

def ai_move_minimax(board, is_maximizing):
    """
    困难 AI：使用 Minimax 算法
    返回最佳移动位置的索引
    """
    # 终止条件
    if check_winner(board, "O"): # AI 是 O
        return 10, None
    if check_winner(board, "X"): # 玩家是 X
        return -10, None
    if is_board_full(board):
        return 0, None

    if is_maximizing:
        best_score = -math.inf
        best_move = None
        for move in get_available_moves(board):
            board[move] = "O"
            score, _ = ai_move_minimax(board, False)
            board[move] = " " # 回溯
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for move in get_available_moves(board):
            board[move] = "X"
            score, _ = ai_move_minimax(board, True)
            board[move] = " " # 回溯
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

def get_ai_move(board, difficulty):
    """根据难度获取 AI 移动"""
    available = get_available_moves(board)
    if not available:
        return None
    
    if difficulty == "easy":
        return ai_move_random(board)
    elif difficulty == "hard":
        # 如果第一步，为了节省计算时间且增加一点变化，可以随机选角或中心，但这里直接上 Minimax 保证无敌
        _, move = ai_move_minimax(board, True)
        return move
    return None

# --- 游戏核心逻辑 ---

def play_round(mode, difficulty=None):
    """执行单局游戏"""
    board = [" "] * 9
    current_symbol = "X" # 玩家总是先手 (X)
    
    # 确定对手名称
    if mode == "pvp":
        p1_name = "玩家 1 (X)"
        p2_name = "玩家 2 (O)"
    else:
        p1_name = "你 (X)"
        diff_text = "简单" if difficulty == "easy" else "困难 (无敌)"
        p2_name = f"电脑 ({diff_text})"

    print(f"\n比赛开始：{p1_name} VS {p2_name}")
    print_help_board()
    time.sleep(1.5)

    game_running = True
    while game_running:
        # 绘制棋盘
        # 清屏前稍微停顿一下，避免闪瞎眼，但在循环中我们通常直接清屏
        clear_screen()
        print(f"当前模式: {'双人对战' if mode == 'pvp' else f'人机对战 ({difficulty})'}")
        print_board(board)

        # 判断当前是谁的回合
        is_player_turn = False
        if mode == "pvp":
            is_player_turn = True # 双人都是人
        else:
            if current_symbol == "X":
                is_player_turn = True # 玩家回合
            else:
                is_player_turn = False # 电脑回合

        if is_player_turn:
            player_name = p1_name if current_symbol == "X" else p2_name
            while True:
                try:
                    move_input = input(f"{player_name}, 请输入位置 (1-9) 或 'q' 退出: ").strip().lower()
                    if move_input == 'q':
                        return "quit"
                    
                    if not move_input.isdigit():
                        print("❌ 请输入数字 1-9。")
                        continue
                    
                    move_idx = int(move_input) - 1
                    if move_idx < 0 or move_idx > 8:
                        print("❌ 数字必须在 1-9 之间。")
                        continue
                    if board[move_idx] != " ":
                        print("❌ 该位置已被占用！")
                        continue
                    
                    # 有效移动
                    board[move_idx] = current_symbol
                    break
                except KeyboardInterrupt:
                    return "quit"
                except Exception:
                    print("❌ 输入错误。")
        else:
            # 电脑回合
            print(f"电脑 ({current_symbol}) 正在思考...")
            time.sleep(0.8) # 模拟思考时间
            move_idx = get_ai_move(board, difficulty)
            if move_idx is not None:
                board[move_idx] = current_symbol
            else:
                # 理论上不会发生，除非棋盘满了
                pass

        # 检查胜负
        if check_winner(board, current_symbol):
            clear_screen()
            print_board(board)
            winner_name = p1_name if current_symbol == "X" else p2_name
            print("=" * 30)
            if mode != "pvp" and current_symbol == "O":
                print(f"🤖 电脑获胜！再接再厉！")
            else:
                print(f"🎉 恭喜 {winner_name} 获胜！ 🎉")
            print("=" * 30)
            game_running = False
            break

        # 检查平局
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("=" * 30)
            print("🤝 平局！棋盘已满。 🤝")
            print("=" * 30)
            game_running = False
            break

        # 切换符号
        current_symbol = "O" if current_symbol == "X" else "X"

    return "finished"

def show_menu():
    """显示主菜单"""
    clear_screen()
    print("=" * 40)
    print("       欢 迎 来 到 井 字 棋       ")
    print("=" * 40)
    print("\n请选择游戏模式:\n")
    
    print("  [1] 双人模式 (PvP)")
    print("      👉 说明：两位玩家在同一台电脑上轮流下棋。")
    print("      👉 适合：朋友聚会，面对面切磋。\n")
    
    print("  [2] 人机模式 - 简单 (PvE Easy)")
    print("      👉 说明：你 vs 电脑。电脑会随机下棋，偶尔会犯错。")
    print("      👉 适合：新手熟悉规则，轻松获胜。\n")
    
    print("  [3] 人机模式 - 困难 (PvE Hard)")
    print("      👉 说明：你 vs 超级电脑。电脑使用最优算法，永不失误。")
    print("      👉 适合：挑战自我，争取平局就是胜利！\n")
    
    print("  [4] 退出游戏")
    print("-" * 40)

def main():
    while True:
        show_menu()
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == '1':
            result = play_round(mode="pvp")
            if result == "quit":
                break
        elif choice == '2':
            result = play_round(mode="pve", difficulty="easy")
            if result == "quit":
                break
        elif choice == '3':
            print("\n⚠️ 警告：此模式下电脑几乎不可能输，你能逼平它吗？")
            time.sleep(2)
            result = play_round(mode="pve", difficulty="hard")
            if result == "quit":
                break
        elif choice == '4':
            print("\n感谢游玩，再见！👋")
            break
        else:
            print("❌ 无效选项，请输入 1 到 4。")
            time.sleep(1)
        
        # 每局结束后，询问是否返回菜单
        if choice in ['1', '2', '3']:
            input("\n按回车键返回主菜单...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n发生错误: {e}")
        input("按回车退出...")