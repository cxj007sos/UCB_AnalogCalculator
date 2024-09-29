import math
import random
import datetime

def now():
    """返回当前日期和时间，格式为：YYYY-MM-DD HH:MM:SS"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_valid_num_arms():
    """获取有效的臂数量输入"""
    while True:
        try:
            num_arms = int(input("请输入臂的数量（最多10000个臂）: "))
            if 1 <= num_arms <= 10000:
                return num_arms
            else:
                print("输入不正确，请输入1到10000之间的整数。")
                print()
        except ValueError:
            print("输入不正确，请输入一个整数。")
            print()

def get_arm_means(num_arms):
    """获取用户输入的臂均值"""
    while True:
        means_input = input(f"请输入{num_arms}个臂的均值（用逗号分隔）: ")
        means = means_input.split(',')
        if len(means) != num_arms:
            print(f"输入的均值数量不正确，应为{num_arms}个。请重新输入。")
            continue
        try:
            means = [float(mean.strip()) for mean in means]
            return means
        except ValueError:
            print("输入包含无效的数值。请确保所有输入都是有效的数字（整数或小数）。")

def get_random_generation_params(arm_means=None):
    """获取随机生成参数，考虑手动设置的均值"""
    while True:
        if arm_means:
            min_mean = min(arm_means)
            max_mean = max(arm_means)
            print(f"\n注意：生成范围应该覆盖所有设置的均值 ({min_mean} 到 {max_mean})")
            
        start = input(f"生成范围起始值（不输入默认为{min_mean if arm_means else 0}）: ")
        start = float(start) if start else (min_mean if arm_means else 0)
        
        end = input(f"生成范围最大值（不输入默认为{max(100, max_mean) if arm_means else 100}）: ")
        end = float(end) if end else (max(100, max_mean) if arm_means else 100)
        
        if arm_means and (start > min_mean or end < max_mean):
            print("错误：生成范围不能覆盖所有设置的均值。请重新输入。")
            continue
        
        if start >= end:
            print("错误：起始值必须小于最大值。请重新输入。")
            continue
        
        break

    generate_decimals = get_yes_no_input("是否需要随机生成小数？(Y/N)")
    decimal_places = 0
    if generate_decimals:
        while True:
            try:
                decimal_places = int(input("随机生成小数点后几位(默认是1位,如:0.1): ") or "1")
                if decimal_places >= 0:
                    break
                else:
                    print("请输入非负整数。")
            except ValueError:
                print("请输入有效的整数。")

    return start, end, generate_decimals, decimal_places

def generate_random_means(num_arms, start, end, generate_decimals, decimal_places):
    """生成随机均值"""
    if generate_decimals:
        return [round(random.uniform(start, end), decimal_places) for _ in range(num_arms)]
    else:
        return [round(random.uniform(start, end)) for _ in range(num_arms)]

def generate_rewards(arm_means, num_rewards, generate_decimals, decimal_places, start, end):
    """为每个臂生成奖励数组"""
    rewards = {}
    for i, mean in enumerate(arm_means):
        arm = f"{i+1:05d}"
        if generate_decimals:
            rewards[arm] = [round(random.uniform(start, end), decimal_places) for _ in range(num_rewards)]
        else:
            rewards[arm] = [round(random.uniform(start, end)) for _ in range(num_rewards)]
    return rewards

def initialize_arms(num_arms):
    """初始化每个臂的数据结构"""
    return {f"{i+1:05d}": {'count': 0, 'value': 0, 'rewards': []} for i in range(num_arms)}

def ucb_value(avg_reward, total_choices, count):
    """计算UCB值"""
    C = math.sqrt(2)
    if count > 0:
        return avg_reward + C * math.sqrt(math.log(total_choices) / count)
    else:
        return float('inf')

def update_values(arms, chosen_arm, reward):
    """更新选中臂的值"""
    arms[chosen_arm]['count'] += 1
    arms[chosen_arm]['value'] = ((arms[chosen_arm]['value'] * (arms[chosen_arm]['count'] - 1)) + reward) / arms[chosen_arm]['count']

def run_ucb_simulation(arms, rewards, num_rounds):
    """运行UCB模拟"""
    total_choices = 0
    rewards_history = []

    # 初始化阶段
    print("\n第 0 轮（初始化）:")
    for arm in arms:
        initial_reward = rewards[arm][0]
        arms[arm]['rewards'] = rewards[arm][1:]  # 存储剩余的奖励
        update_values(arms, arm, initial_reward)
        print(f"臂 {arm} 的初始奖励值: {initial_reward:.2f}")

    total_choices = len(arms)
    first_arm = max(arms, key=lambda arm: arms[arm]['value'])
    print()
    print(f"初始化后选择的臂: {first_arm}")

    # UCB模拟
    for round_num in range(1, num_rounds + 1):
        ucb_values = {arm: ucb_value(arms[arm]['value'], total_choices, arms[arm]['count']) for arm in arms}
        chosen_arm = max(ucb_values, key=ucb_values.get)

        if arms[chosen_arm]['rewards']:
            reward = arms[chosen_arm]['rewards'].pop(0)
        else:
            print(f"臂 {chosen_arm} 的预定义奖励已用完，将随机生成新的奖励。")
            reward = round(random.gauss(sum(rewards[chosen_arm]) / len(rewards[chosen_arm]), 10), 2)

        update_values(arms, chosen_arm, reward)
        total_choices += 1
        rewards_history.append(reward)

        print(f"\n第 {round_num} 轮:")
        print(f"选择了臂 {chosen_arm}，奖励值为 {reward:.2f}")
        print("更新后的平均值: " + ", ".join(f"{arm}: {arms[arm]['value']:.2f}" for arm in arms))
        print("更新后的选择次数: " + ", ".join(f"{arm}: {arms[arm]['count']}" for arm in arms))

    return rewards_history, chosen_arm

def get_yes_no_input(prompt):
    """获取Yes/No输入,默认为No"""
    while True:
        choice = input(f"{prompt}【默认为N】: ").strip().lower()
        if choice == '':
            return False
        if choice in ['y', 'n']:
            return choice == 'y'
        print("输入不正确,请输入 Y 或 N。")

def main():
    while True:
        print("欢迎使用大羽牌UCB多臂老虎机策略_ver240928_模拟场景计算")
        print("——————————————————————————————")

        num_arms = get_valid_num_arms()
        print(f"共有 {num_arms} 个臂")

        set_means = get_yes_no_input("\n是否要设定每个臂的均值？(Y/N)")
        if set_means:
            arm_means = get_arm_means(num_arms)
            start, end, generate_decimals, decimal_places = get_random_generation_params(arm_means)
        else:
            start, end, generate_decimals, decimal_places = get_random_generation_params()
            arm_means = generate_random_means(num_arms, start, end, generate_decimals, decimal_places)

        print("\n每个臂的均值:")
        for i, mean in enumerate(arm_means):
            print(f"臂 {i+1:05d}: {mean}")

        print("\n设置摘要:")
        print(f"现在有臂数量:   {num_arms}")
        print(f"手动设定均值:   {'是' if set_means else '否'}")
        print(f"随机生成范围:   {start:.1f} 到 {end:.1f}")
        print(f"是否生成小数:   {'是' if generate_decimals else '否'}")
        if generate_decimals:
            print(f"小数点后位数:   {decimal_places}")

        print("\n奖励生成设置:")
        while True:
            try:
                num_rewards = int(input("每臂需随机生成几次数值（输入正整数）："))
                if num_rewards > 0:
                    break
                else:
                    print("请输入正整数。")
            except ValueError:
                print("输入无效，请输入正整数。")

        rewards = generate_rewards(arm_means, num_rewards, generate_decimals, decimal_places, start, end)

        print("\n生成的奖励值:")
        for arm, arm_rewards in rewards.items():
            print(f"臂 {arm}: {arm_rewards}")

        print("\nUCB模拟设置:")
        while True:
            try:
                rounds = int(input("请输入要运行的额外轮数（除去初始轮）: "))
                if rounds >= 0:
                    break
                else:
                    print("请输入一个非负整数。")
            except ValueError:
                print("输入不正确，请输入一个整数。")

        arms = initialize_arms(num_arms)
        rewards_history, final_arm = run_ucb_simulation(arms, rewards, rounds)
        
        print("\n最终结果:")
        for arm in arms:
            print(f"臂 {arm}: 平均奖励 = {arms[arm]['value']:.2f}, 被选择次数 = {arms[arm]['count']}")

        print(f"\n在第 {rounds} 轮选择了臂 {final_arm}")

        print()
        while True:
            choice = input("是否开始新一轮UCB计算？(Y/N): ").strip().lower()
            if choice in ['y', 'n']:
                break
            else:
                print("输入不正确，请输入 Y 或 N。")

        if choice != 'y':
            break
        print("————————————————————————————————————————————————————————")
        print(now())
        print("\n" * 3)

    print("\n程序结束，谢谢使用！")
    input('请按任意键退出...')

if __name__ == "__main__":
    main()