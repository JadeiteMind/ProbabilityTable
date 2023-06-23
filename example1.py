from ProbablityTable import ProbabilityTable
# 阶段一示例用法
# 创建一个新的概率表对象
pt = ProbabilityTable()

# 向概率表中添加物品及其权重
pt.add_item("apple", 0.4)
pt.add_item("banana", 0.5)
pt.add_item("orange", 0.2)

# 计算物品的概率
probability_of_apple = pt.calculate_probability("apple")
print("Probability of item 'apple':", '%.5f' % (probability_of_apple))


# 根据概率采样一个物品
sampled_item = pt.sample_item()
print("Sampled item:", sampled_item)