![](https://img.shields.io/badge/language-python-orange) ![](https://img.shields.io/badge/platform-win10--x64%7Cwin11--x64-lightgrey)

[![GitHub issues](https://img.shields.io/github/issues/cxj007sos/rpa_improve)](https://github.com/cxj007sos/rpa_improve/issues) [![GitHub license](https://img.shields.io/github/license/cxj007sos/rpa_improve)](https://github.com/cxj007sos/rpa_improve/blob/master/LICENSE)

[![](https://img.shields.io/badge/bilibili-%E5%A4%A7%E7%BE%BD-ff69b4)](https://space.bilibili.com/3410770?)

# UCB多臂老虎机策略模拟器

## 项目简介

本程序是使用Claude.ai，通过自然语言描述自动生成的Python程序。它基于UCB（Upper Confidence Bound）算法实现了一个多臂老虎机策略模拟器。该项目包含两个主要脚本：一个用于模拟场景计算，另一个用于真实场景计算。

### 缘起

2024-09-08，我在抖音上看到了B站UP主"漫士沉思录"介绍UCB多臂老虎机算法的视频。视频中详细讲解了信心上界算法，该算法在乐观中选择最佳选项，并在交互过程中调整乐观程度，通过历史数据的平均值来评估选择的优劣，从而找到最优解。

UP主启发我们：在人生中应跳出"一锤定音"的固定思维，要勇于尝试，在不断探索中寻找最佳方案。

视频地址：[BV1auHQeLEHc](https://www.bilibili.com/video/BV1auHQeLEHc)

受此启发，我利用Claude.ai开发了这个算法模拟器。

<br>

## 更新日志
- 未来更新日志会写在这里。
<br>

---

## 功能特点

- 支持模拟场景和真实场景的UCB策略计算
- 可自定义臂的数量（最多26个）【在demo文件夹中有支持10000个臂的程序】
- 模拟场景下可随机生成或手动设置臂的均值
- 真实场景下可手动输入每个臂的奖励值
- 详细的每轮选择和奖励输出
- 灵活的参数设置，包括轮数、奖励生成范围等
<br>

## 文件和使用说明

本项目使用Python 3编写。确保您的系统已安装Python 3。
windows可以直接下载exe文件夹中的可执行文件。

1. `UCB_模拟场景计算`: 用于模拟场景的UCB策略计算，计算策略为经典的UCB1。
2. `UCB_真实场景计算`: 用于真实场景的UCB策略计算，计算策略为经典的UCB1。
3. `UCB_真实场景计算_高级版`: 与真实场景不同之处在于C值采取了更复杂的算法。

- **模拟场景计算**

  按照提示输入参数，包括臂的数量、是否手动设置均值、随机生成范围、轮数等。

- **真实场景计算**

  按照提示输入臂的数量和每个臂的预定义奖励值。
  
<br>

## 小数显示说明
**模拟和真实场景计算两者的UCB计算在初始轮和后续每一轮中，选中臂的奖励值和更新后的平均值只显示小数点后两位，但不影响计算精度。**
```python
print(f"臂 {arm} 的初始奖励值: {initial_reward:.2f}") # {initial_reward:.2f} 意为仅打印小数后两位，不影响运算。

print(f"选择了臂 {chosen_arm}，奖励值为 {reward:.2f}") # {reward:.2f} 意为仅打印小数后两位，不影响运算。

print("更新后的平均值: " + ", ".join(f"{arm}: {arms[arm]['value']:.2f}" for arm in arms)) # {arms[arm]['value']:.2f} 意为仅打印小数后两位，不影响运算。
```

<br>

## 程序中会影响算法的行为
### C值
**较大的C值会增加探索**，可能会更多地尝试不同的臂。
**较小的C值会减少探索**，更倾向于利用当前认为最好的臂。

- **C值默认为** $\mathbf{\sqrt{2}}$ 是UCB算法的一个经典设置，通常被称为"UCB1"算法。
- 在Python的源码中【可以修改C值】，在exe可执行文件中【无法修改C值】。

**推荐几个常用的 C 值：**
- C = 1 或 C = $\mathbf{\sqrt{2}}$（标准值）
- C = 0.5（减少探索）
- C = 2 或 3（增加探索）
  
---
### 在代码中你可以修改它

**普通版**
```python
"""普通版中的C值只需要修改这里"""
C =  math.sqrt(2)
```

**高级版**
```python
"""高级版中，C值由多个因素组成，修改以下两行代码的数值可以调整C值"""
# 根据最佳两个选项的差距来决定C值
sigma = 3               # 【标准差的倍数，可根据实际情况调整。sigma = 1 时近似UCB1算法偏保守，减少多次其他臂的尝试】
if top_two_diff > 0.1:  # 【假设0.1为"很大"差距的阈值，需要根据实际情况调整】
```
---

<br>

### UCB公式

$$
UCB_i(t) = \overline{X}_i(t) + C *\sqrt{\frac{\ln t}{N_i(t)}}
$$

<div style="text-align: center;"> 可以简化为 </div>

$$
UCB = \overline{X}+ C *\sqrt{\frac{\ln t}{N}}
$$

**<div style="text-align: center;">UCB值 = 平均奖励 + 探索系数 * 根号下（总选择次数的自然对数 / 该臂被选择的次数）。</div>**

其中：

- $\overline{X}$   ：当前选项的  **平均奖励** 。
- $C$  ：控制**探索程度**的参数，可以根据具体情况进行调整。（在标准UCB1算法中通常设为： $\mathbf{\sqrt{2}}$ ）
- $t$  &nbsp;&nbsp;：当前的  **总选择次数** （轮次）,
- $N$ ：当前选项（臂）被选择的 **次数**

PS:

- $(t)$ 仅表示当前轮次，**$(t)$ 不参与计算。**
- $i$ 仅表示当前被选中的选项（臂），**$i$ 不参与运算。**
- 所以简化公式去除了以上两项。
<br>

## 贡献

我们欢迎您提出问题和建议！如果您想为这个项目做出贡献，请提交pull request。

## 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源许可证。

---

感谢您使用UCB多臂老虎机策略模拟器！希望这个工具能够帮助您在决策和探索中找到平衡。
