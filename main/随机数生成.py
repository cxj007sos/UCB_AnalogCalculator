import random
import numpy as np

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("请输入一个正整数。")
        except ValueError:
            print("输入无效，请输入一个正整数。")

def main():
    while True:
        mean = float(input("请输入随机数平均值："))
        
        # 验证起始值必须小于等于平均值
        while True:
            start = int(input("请输入随机数起始值："))
            if start <= mean:
                break
            print("起始值必须小于或等于平均值，请重新输入。")
        
        # 验证结束值必须大于等于平均值
        while True:
            end = int(input("请输入随机数结束值："))
            if end >= mean:
                break
            print("结束值必须大于或等于平均值，请重新输入。")
        
        # 获取正整数生成数目
        num_rewards = get_positive_integer("请随机数生成数目（正整数）：")
        
        rewards = np.random.normal(mean, (end - start) / 6, num_rewards)  # 使用正态分布
        rewards = np.clip(rewards, start, end)  # 将值限制在指定范围内

        # 显示带有 [] 的完整数值结果
        #print(rewards)
        
        # 四舍五入到整数
        rounded_rewards = [round(reward) for reward in rewards]  # 四舍五入到整数
        
        # 显示带有 [] 的四舍五入结果
        #print(f"\n" * 2 + f"{rounded_rewards}")  # 多换行并打印结果

        # 显示不带 [] 的四舍五入结果，方便复制
        print(f"\n" + ', '.join(map(str, rounded_rewards)))  # 输出为逗号分隔的字符串
        print()
        
        # 询问是否继续生成
        choice = input("是否要继续生成随机数？(默认为 y, 输入 n 退出)：").strip().lower()
        print()
        if choice == 'n':
            break

if __name__ == "__main__":
    main()
