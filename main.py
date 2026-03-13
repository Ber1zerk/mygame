import random

# ================= 游戏 1: 人来猜 =================
def human_guess_game():
    print("\n" + "="*30)
    print("🎮 模式 A: 你来猜数字")
    print("="*30)
    
    # 这里我们可以动态选择难度，默认先定 1000
    max_num = 1000
    secret_number = random.randint(1, max_num)
    attempts = 0
    
    print(f"我想好了一个 1 到 {max_num} 之间的数字。")
    
    while True:
        try:
            user_input = input("\n请输入你的猜测 (输入 q 退出): ")
            if user_input.lower() == 'q':
                print("游戏结束！下次再来！👋")
                return
            
            guess = int(user_input)
            attempts += 1
            
            if guess < secret_number:
                print("📉 太小了！")
            elif guess > secret_number:
                print("📈 太大了！")
            else:
                print(f"🎉 恭喜你！猜对了！数字是 {secret_number}。")
                print(f"你用了 {attempts} 次。")
                if attempts <= 7:
                    print("🌟 简直是读心术大师！")
                elif attempts <= 10:
                    print("👍 逻辑清晰，表现优秀！")
                else:
                    print("🐢 下次试试二分法？")
                break
        except ValueError:
            print("❌ 请输入有效的整数！")

# ================= 游戏 2: AI 来猜 =================
def ai_guess_game():
    print("\n" + "="*30)
    print("🤖 模式 B: AI 来猜你的数字")
    print("="*30)
    print("请在心里想一个 1 到 1000 之间的整数。")
    input("想好了吗？按回车键开始...")
    
    low = 1
    high = 1000
    attempts = 0
    
    while low <= high:
        attempts += 1
        guess = (low + high) // 2
        
        print(f"\n第 {attempts} 次猜测：我猜是 {guess}")
        print("  1. 大了 (你想的数比这个小)")
        print("  2. 小了 (你想的数比这个大)")
        print("  3. 猜对了")
        
        response = input("请回答 (1/2/3): ")
        
        if response == '3':
            print(f"\n🎉 哈哈！我赢了！数字就是 {guess}！")
            print(f"我只用了 {attempts} 次。算法无敌！⚡")
            break
        elif response == '1':
            high = guess - 1
        elif response == '2':
            low = guess + 1
        else:
            print("❌ 无效输入，请重新输入。")
            attempts -= 1
            
        if low > high:
            print("\n🚨 等等，数据矛盾了！你是不是中途改数字了？😏")
            break

# ================= 主菜单 =================
def main_menu():
    while True:
        print("\n" + "#"*40)
        print("#       🕹️  Python 游戏中心 🕹️       #")
        print("#"*40)
        print("1. 你来猜数字 (挑战人类直觉)")
        print("2. AI 猜数字 (见证算法力量)")
        print("3. 退出游戏")
        
        choice = input("\n请选择一个选项 (1/2/3): ")
        
        if choice == '1':
            human_guess_game()
        elif choice == '2':
            ai_guess_game()
        elif choice == '3':
            print("👋 感谢游玩，再见！")
            break
        else:
            print("❌ 无效选项，请输入 1、2 或 3。")

if __name__ == "__main__":
    main_menu()