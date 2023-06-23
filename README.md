# ProbabilityTable

**崔世博	北京航空航天大学	email:20373740@buaa.edu.cn**

##内容列表
- [阶段一](#阶段一)
- [阶段二](#阶段二)
- [阶段三](#阶段三)

##阶段一

###实现思路
定义一个类`ProbabilityTable`用于实现概率表，类中一个字典`table`存储物品名称`item`和对应的权重`weight`，物品名称作为键，权重作为值。类中还维护总权重`total_weight`，用于辅助进行计算概率和采样物品。

计算某个物品的概率等于$weight/total\_weight$。

按照概率采样一个物品，使用`random_uniform`在`[0,total_weight]`内随机采样一个实数`random_num`。定义累计概率`cumulative_weight`（初值为0），遍历`table`中的物品，将其权重加到`cumulative_weight`上，在`cumulative_weight`首次超过`random_num`时采样该物品，结束采样。

对采样过程正确性的证明：假设有$n$个物品，分别编号$1$~$n$，它们的权重相应为$w_1$~$w_n$。把`[0,total_weight]`想象成线段，`random_num`是其上一个随机采样的点，使用几何概型得到采样到物品$k(1\le k\le n)$的概率为：

$$
P(\sum_{i=1}^{k}w_{i}\ge random\_num>\sum_{i=1}^{k-1}w_{i})=\frac{w_k}{total\_weight}
$$
即采样到物品的概率就是物品的概率。

需要考虑以下情形异常处理以保证API的正确性：

- 物品权重为负时报错
- 在计算某个物品概率时，物品名称输错时报错
- 在采样物品时，物品表为空时报错

###API接口

```python
class ProbabilityTable:
    def __init__(self):
        """
        创建一个新的概率表对象。
        """
    def add_item(self, item, weight):
        """
        向概率表中添加一个物品及其权重。

        参数:
        - item: str，物品名称。
        - weight: float，物品权重。不能是负数。

        异常:
        - ValueError: 如果权重为负数，则引发异常。
        """

    def calculate_probability(self, item):
        """
        计算给定物品的概率。

        参数:
        - item: str，要计算概率的物品名称。

        返回值:
        - float，给定物品的概率。

        异常:
        - ValueError: 如果物品不在概率表中，则引发异常。
        """

    def sample_item(self):
        """
        根据物品的概率进行采样，返回一个随机选取的物品。

        返回值:
        - str，采样得到的物品名称。

        异常:
        - ValueError: 如果概率表为空，则引发异常。
        """`
```

###使用示例

```python
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
```

运行`./example1.py`即可看到以上用例的结果。

## 阶段二

### 实现思路

只需要增加一个`update_weight`方法，输入参数为需要更新权重物品的名称`item`以及更新后的权重，将`table`中对应值修改即可。需要注意的是需要维护`total_weight`的值。

需要注意以下情形的异常处理：

- 更新后的权重不能是负数
- 物品名称需要在table中

### API接口

仅在类`ProbabilityTable`中增加了`update_weight`，其他部分不变。

```python
def update_weight(self, item, new_weight):
    """
    更新给定物品的权重。
    
    参数:
    - item: str，要更新权重的物品名称。
    - new_weight: float，新的物品权重。必须是非负数。
    
    异常:
    - ValueError: 如果物品不在概率表中，则引发异常。
    """
```

### 使用示例

```python
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
```

运行`.\example2.py`即可看到以上用例的结果。

## 阶段三

### 实现思路

根据Markov概率模型，某个64位无符号整数$x$出现的概率为：
$$
Pr(x)=Pr(x_0|*)Pr(x_1|*x_0)\cdots Pr(x_n|x_0\cdots x_{n-1})\\\cdots Pr(x_{63}|x_{63-n}\cdots x_{62})
$$
根据上式，$x$的某一位是0或者是1只与前面（至多）$n$位有关。因此可以逐位采样生成整数输出。（直接计算所有可能的64位整数的概率并采样是不现实的）

条件概率的计算公式如下：
$$
Pr(x_{i}|x_{i-n}\cdots x_{i-1})=\frac{Count(x_{i-n}\cdots x_{i})}{Count(x_{i-n}\cdots x_{i-1})}
$$
在`MarkovModel`类中，我们维护一个`counts`，它的键是不超过`n`位的字符串`context`，它的值是一个`table`，形如{'0':1, '1':1}，记录了在上文是`context`的前提下，下一位是`0`或`1`的次数。`MarkovModel`类中存在一个采样器`pt`，它就是前面实现的概率表。

因此，
$$
Pr(x_{i}|x_{i-n}\cdots x_{i-1})=\frac{counts[context][x_{i}]}{counts[context][0]+counts[context][1]}
$$
训练时，遍历所有训练数据，使用滑动窗口维护`counts`即可（用空间换时间的思路）。

计算某个整数的概率，只需按照给定公式顺序计算。

采样时，初始上文`context`为空，根据`counts`导出的条件概率采样下一位，补充到`context`尾部（如果`context`长度达到`n`位，则需要去掉首位，保持`n`位长），更新`pt`中的`0`和`1`的权重，继续完成下一位的采样，直到64位。

### API接口

该API提供了使用Markov模型进行训练、生成和计算概率的功能。Markov模型是一种基于上下文的概率模型，用于生成二进制数据序列。

```python
from ProbabilityTable import ProbabilityTable

class MarkovModel:
    def __init__(self, order):
        """
        初始化马尔可夫模型对象。

        参数:
        - order: int，模型的阶数。
        """

    def train(self, data):
        """
        使用给定的数据训练马尔可夫模型。

        参数:
        - data: Iterable[int]，训练数据，包含一系列整数。
        """

    def generate(self, length):
        """
        采样指定长度的二进制数。

        参数:
        - length: int，要生成的二进制数的长度。

        返回值:
        - str，采样得到的二进制数的字符串表示。
        """

    def probability(self, number):
        """
        计算给定数字（当成64位2进制串）在马尔可夫模型下的概率。

        参数:
        - number: int，要计算概率的数字。

        返回值:
        - float，给定数字的概率。
        """
     
    def random_choice(self, choices):
        """
        根据给定权重，随机选择0或1。

        参数:
        - choices: Dict[str, int]，0和1的权重。

        返回值:
        - str，随机选择的选项。
        """
    
    @staticmethod
    def to_binary_string(number):
        """
        将给定数字转换为64位的二进制字符串表示。

        参数:
        - number: int，要转换的数字。

        返回值:
        - str，二进制字符串表示。
        """

```

### 使用示例

```python
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
print(f"Probability of 0: {probability_of_0}")

# 采样10个整数
samples = [model.generate(64) for _ in range(10)]
print("10 Generated samples (in binary):")
for sample in samples:
    print(sample)
```

运行`.\example3.py`即可看到以上用例的结果。

![image-20230623112014835](C:\Users\Jadeite\AppData\Roaming\Typora\typora-user-images\image-20230623112014835.png)