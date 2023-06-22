# ProbabilityTable
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

$$P(\sum_{i=1}^{k}w_{i}\ge random\_num>\sum_{i=1}^{k-1}w_{i})=\frac{w_k}{total\_weight}$$

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
# 创建一个新的概率表对象
pt = ProbabilityTable()

# 向概率表中添加物品及其权重
pt.add_item("apple", 0.4)
pt.add_item("banana", 0.5)
pt.add_item("orange", 0.2)

# 计算物品的概率
probability_of_B = pt.calculate_probability("apple")
print("Probability of item 'apple':", '%.5f' % (pt.calculate_probability("apple")))


# 根据概率采样一个物品
sampled_item = pt.sample_item()
print("Sampled item:", sampled_item)
```

运行`./ProbabilityTable.py`即可看到以上用例的结果。

