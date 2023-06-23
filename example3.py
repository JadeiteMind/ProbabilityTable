import random
from MarkovModel import MarkovModel

# 阶段三示例用法
# 创建阶数为n的Markov模型，n由终端读入
n = int(input("Please enter the order of the Markov Statiscal Model: "))
model = MarkovModel(n)
print('%d' % model.n, 'Order Markov Statiscal Model:')

# 生成随机训练集，包含10000个64位整数
training_data = [random.randint(0, 2 ** 64 - 1) for _ in range(10000)]
print('Partial random test data:', training_data[:10])

# 训练模型
model.train(training_data)

# 计算整数0的概率
probability_of_0 = model.probability(0)
print("Probability of 0: %f" % probability_of_0)

# 采样10个整数
samples = [model.generate(64) for _ in range(10)]
print("10 Generated samples (in binary):")
for sample in samples:
    print(sample)