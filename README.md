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

## 功能特点

- 支持模拟场景和真实场景的UCB策略计算
- 可自定义臂的数量（最多26个）【在demo文件夹中有支持10000个臂的程序】
- 模拟场景下可随机生成或手动设置臂的均值
- 真实场景下可手动输入每个臂的奖励值
- 详细的每轮选择和奖励输出
- 灵活的参数设置，包括轮数、奖励生成范围等

## 文件说明

1. `UCB_模拟场景计算`: 用于模拟场景的UCB策略计算
2. `UCB_真实场景计算`: 用于真实场景的UCB策略计算

## 使用说明

本项目使用Python 3编写。确保您的系统已安装Python 3。

windows可以直接下载exe文件夹中的可执行文件。


程序中**C值**的会影响算法的行为：

**较大**的C值会增加探索，可能会更多地尝试不同的臂。
**较小**的C值会减少探索，更倾向于利用当前认为最好的臂。

-**C值设为默认值为1**是UCB算法的一个经典设置，通常被称为"UCB1"算法。
-在Python的源码中你可以修改UCB公式中的C值，默认为1。
-在exe可执行文件中不可修改C值，默认值为1。

```
【这个位置不正确，需要修改代码后再确定，只是临时位置】
def ucb_value(avg_reward, total_choices, count, C=1):
```

### UCB公式
$$
UCB_i(t) = \overline{X}_i(t) + C \sqrt{\frac{2 \ln(t)}{N_i(t)}}
$$

其中：

- $UCB_i(t)$ 是在时间 $t$ 时臂 $i$ 的【UCB值】
- $\overline{X}_i(t)$ 是臂 $i$ 到时间 $t$ 为止的【平均奖励】
- $C$ 是控制探索程度的参数（在标准UCB1算法中通常设为1）
- $t$ 是总的选择次数
- $N_i(t)$ 是到时间 $t$ 为止臂 $i$ 被选择的次数

## 使用方法

### 模拟场景计算

按照提示输入参数，包括臂的数量、是否手动设置均值、随机生成范围、轮数等。

### 真实场景计算

按照提示输入臂的数量和每个臂的预定义奖励值。

## 贡献

我们欢迎您提出问题和建议！如果您想为这个项目做出贡献，请提交pull request。

## 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源许可证。

---

感谢您使用UCB多臂老虎机策略模拟器！希望这个工具能够帮助您在决策和探索中找到平衡。
