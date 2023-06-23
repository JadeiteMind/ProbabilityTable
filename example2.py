from ProbablityTable import ProbabilityTable
# 阶段二示例用法
# 创建一个新的概率表对象
pt = ProbabilityTable()

# 向概率表中添加物品及其权重
pt.add_item("apple", 5)
pt.add_item("banana", 5)

# 计算apple的概率
probability_of_apple = pt.calculate_probability("apple")
print("Probability of item 'apple':", '%.5f' % (probability_of_apple))

# 根据概率采样一个物品
sampled_item = pt.sample_item()
print("Sampled item:", sampled_item)

# 更新apple的权重(5->20)
pt.update_weight("apple", 20)

# 重新计算apple的概率
probability_of_apple = pt.calculate_probability("apple")
print("After updating weight, Probability of item 'apple':", '%.5f' % (probability_of_apple))

# 重新采样物品
sampled_item = pt.sample_item()
print("After updating weight, Sampled item:", sampled_item)