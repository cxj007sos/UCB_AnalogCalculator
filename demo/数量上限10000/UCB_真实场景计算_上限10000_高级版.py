import math
import datetime

def now():
  """返回当前日期和时间，格式为：YYYY-MM-DD HH:MM:SS"""
  return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def initialize_arms(num_arms):
    """初始化每个臂的数据结构"""
    return {f"{i+1:05d}": {'count': 0, 'value': 0, 'rewards': []} for i in range(num_arms)}

def ucb_value(avg_reward, total_choices, count, rewards, top_two_diff):
    """计算修改后的UCB值"""

    """参数:
    avg_reward: 当前选项的平均回报
    total_choices: 总的选择次数
    count: 当前选项被选择的次数
    rewards: 所有选项的回报列表
    top_two_diff: 最佳两个选项的平均回报差
    """
    if count == 0:
        return float('inf'), None, None, None, None
    
    # 计算当前选项回报的标准差
    std_dev = math.sqrt(sum((r - avg_reward) ** 2 for r in rewards) / len(rewards)) if rewards else 1

    # 根据最佳两个选项的差距来决定C值
    sigma = 3               # 【标准差的倍数，可根据实际情况调整。sigma = 1 时近似UCB1算法偏保守，减少多次其他臂的尝试】
    if top_two_diff > 0.1:  # 【假设0.1为"很大"差距的阈值，需要根据实际情况调整】
        C = sigma * std_dev
    else:
        C = sigma * std_dev * math.log(total_choices)

    ucb = avg_reward + C * math.sqrt(2 * math.log(total_choices) / count)

    return ucb, C, sigma, std_dev, top_two_diff

def update_values(arms, chosen_arm, reward):
    """更新选中臂的值"""
    arms[chosen_arm]['count'] += 1
    arms[chosen_arm]['value'] = ((arms[chosen_arm]['value'] * (arms[chosen_arm]['count'] - 1)) + reward) / arms[chosen_arm]['count']

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

def get_valid_rewards(arm):
    """获取有效的奖励值输入"""
    while True:
        rewards_input = input(f"请输入臂 {arm} 的预定义奖励（用英文逗号分隔，至少输入一个值）: ")
        rewards = []
        try:
            for r in rewards_input.replace('，', ',').split(','):
                rewards.append(float(r.strip()))
            if rewards:
                return rewards
            else:
                print("请至少输入一个有效的奖励值。")
        except ValueError:
            print("输入包含无效的数字，请重新输入所有奖励值。")

def get_top_two_diff(arms):
    """计算最佳两个臂的平均奖励差"""
    values = [arm['value'] for arm in arms.values()]
    top_two = sorted(values, reverse=True)[:2]
    return top_two[0] - top_two[1] if len(top_two) > 1 else 0

def run_ucb_simulation(arms):
    """运行UCB模拟"""
    # 初始化阶段
    print("\n第 0 轮（初始化）:")
    for arm in arms:
        initial_reward = arms[arm]['rewards'].pop(0)
        update_values(arms, arm, initial_reward)
        print(f"臂 {arm} 的初始奖励值: {initial_reward}")

    total_choices = len(arms)
    first_arm = max(arms, key=lambda arm: arms[arm]['value'])
    print()
    print(f"初始化后选择的臂: {first_arm}")

    while True:
        try:
            rounds = int(input("请输入要运行的额外轮数（除去初始轮）: "))
            if rounds >= 0:
                break
            else:
                print("请输入一个非负整数。")
        except ValueError:
            print("输入不正确，请输入一个整数。")

    for round_num in range(1, rounds + 1):
        top_two_diff = get_top_two_diff(arms)
        ucb_values = {}
        ucb_details = {}
        for arm in arms:
            ucb, C, sigma, std_dev, _ = ucb_value(arms[arm]['value'], total_choices, arms[arm]['count'], 
                                                arms[arm]['rewards'], top_two_diff)
            ucb_values[arm] = ucb
            ucb_details[arm] = (C, sigma, std_dev)
        
        chosen_arm = max(ucb_values, key=ucb_values.get)

        if arms[chosen_arm]['rewards']:
            reward = arms[chosen_arm]['rewards'].pop(0)
        else:
            print()
            while True:
                try:
                    reward = float(input(f"请输入臂 {chosen_arm} 的奖励值: "))
                    break
                except ValueError:
                    print("输入不正确，请输入一个有效的数字。")

        update_values(arms, chosen_arm, reward)
        total_choices += 1

        print(f"\n第 {round_num} 轮:")
        print(f"选择了臂 {chosen_arm}，奖励值为 {reward}")
        print("更新后的平均值: " + ", ".join(f"{arm}: {arms[arm]['value']:.2f}" for arm in arms))
        print("更新后的选择次数: " + ", ".join(f"{arm}: {arms[arm]['count']}" for arm in arms))
        # 以下显示变化的数值，只显示小数点后四位，不影响精度。
        print(f"最佳两个选项的平均回报差: {top_two_diff:.4f}")
        print(f"选中臂的 UCB 详情 - C: {ucb_details[chosen_arm][0]:.4f}, sigma: {ucb_details[chosen_arm][1]:.4f}, std_dev: {ucb_details[chosen_arm][2]:.4f}")

    print("\n最终结果:")
    for arm in arms:
        print(f"臂 {arm}: 平均奖励 = {arms[arm]['value']:.2f}, 被选择次数 = {arms[arm]['count']}")
    
    print(f"\n最终第 {rounds} 轮选择了臂 {chosen_arm}")
        

def main():
    while True:
        print("欢迎使用大羽牌UCB多臂老虎机策略_ver240929_高级版")
        print("——————————————————————————————")

        num_arms = get_valid_num_arms()
        arms = initialize_arms(num_arms)

        print(f"已创建 {num_arms} 个臂")

        # 输入每个臂的预定义奖励
        print()
        for arm in arms:
            arms[arm]['rewards'] = get_valid_rewards(arm)

        run_ucb_simulation(arms)

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