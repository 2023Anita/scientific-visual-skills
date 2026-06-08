# Example Prompts

## `scientific-infographic`

```text
$scientific-infographic
请生成一张科研信息图：主题是“肿瘤微环境中的免疫逃逸机制”。
内容包括：T 细胞耗竭、PD-1/PD-L1 轴、Treg 细胞、肿瘤相关巨噬细胞、缺氧微环境、免疫治疗干预点。
中文，4:5，中等说明，Nature 系克制学术配色，适合综述图和公众号。
```

## `scientific-cover-visual`

```text
$scientific-cover-visual
请生成一张科研封面主视觉：主题是“纳米药物穿越血脑屏障”。
核心视觉概念：纳米颗粒像微型探针一样穿过半透明屏障，进入神经网络微环境。
英文短标题，3:4，强主视觉，浅色高级医学封面，不要真实期刊 logo。
```

## `scientific-paper-figure`

```text
$scientific-paper-figure
请生成一张 Graphical Abstract：主题是“工程化外泌体递送 siRNA 抑制肿瘤生长”。
输入端：工程化外泌体。
过程机制：靶向肿瘤细胞、内吞、释放 siRNA、沉默致癌基因。
输出结果：肿瘤细胞增殖下降。
英文少量标签，16:9，Science 系理性机制配色。
```

## Multi-skill Case: Anesthesia Mechanisms

这个案例适合同时调用三套 Skill：先做封面主视觉，再做总览信息图，最后拆成论文机制图。

```text
$scientific-cover-visual
$scientific-infographic
$scientific-paper-figure
请围绕“麻醉药的机制”生成 6-8 张专业医学科研图。
核心问题：
1. 麻醉药如何让人进入麻醉性无意识状态。
2. 麻醉药如何产生镇痛。
3. 肌松药如何产生骨骼肌松弛。

图像组合：
- 一张科研封面主视觉，突出 balanced anesthesia 的三联目标。
- 一张总览信息图，分为 hypnosis、analgesia、muscle relaxation 三栏。
- 三张论文机制图，分别解释催眠、镇痛、肌松。
- 一张平衡麻醉控制回路教学图。
- 一张分子靶点到临床终点的 Graphical Abstract。

要求：
- 英文短标签，避免大段文字。
- 16:9 为主，封面可用 4:5。
- 不写药物剂量，不给临床处置建议。
- 不使用真实期刊 logo、医院标识或品牌名。
```
