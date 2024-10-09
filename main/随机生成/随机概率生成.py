import random

def generate_results(probability, trials):
    return [1 if random.random() < probability else 0 for _ in range(trials)]

# 设置生成次数
trials = 200

# 设置概率
probabilities = {
    "A": 0.49,
    "B": 0.50,
    "C": 0.51,
    "D": 0.52,
    "E": 0.53
}

# 生成结果
results = {key: generate_results(prob, trials) for key, prob in probabilities.items()}

# 打印输出，去掉方括号
for key, result in results.items():
    result_str = ','.join(map(str, result))  # 将结果转换为用逗号分隔的字符串
    print(f"{key}: {result_str}")
    input()