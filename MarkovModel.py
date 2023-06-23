from ProbablityTable import ProbabilityTable


class MarkovModel:
    def __init__(self, order):
        self.n = order  # 模型的阶数
        self.counts = {}  # 计数器
        self.pt = ProbabilityTable() # 采样器
        self.pt.add_item('0', 1)
        self.pt.add_item('1', 1)

    def train(self, data):
        for number in data:
            binary_string = self.to_binary_string(number)
            for i in range(len(binary_string)):
                if i == 0:
                    context = ''
                elif i < self.n:
                    context = binary_string[0:i]
                else:
                    context = binary_string[i - self.n:i]
                next_char = binary_string[i]
                if context not in self.counts:
                    self.counts[context] = {'0':0, '1':0}
                self.counts[context][next_char] += 1

    def generate(self, length):
        while True:
            current_context = ''
            result = ''
            for _ in range(length):
                if current_context not in self.counts:
                    break
                next_char = self.random_choice(self.counts[current_context])
                result += next_char
                if len(current_context) == self.n:
                    current_context = current_context[1:] + next_char
                else:
                    current_context += next_char
            return result

    def probability(self, number):
        binary_string = self.to_binary_string(number)
        probability = 1.0
        for i in range(len(binary_string)):
            if i == 0:
                context = ''
            elif i < self.n:
                context = binary_string[0:i]
            else:
                context = binary_string[i - self.n:i]
            next_char = binary_string[i]
            if context in self.counts:
                count = self.counts[context][next_char]
                total = sum(self.counts[context].values())
                probability *= count / total
            else:
                probability = 0.0
                break
        return probability

    def random_choice(self, choices):
        self.pt.update_weight('0', choices['0'])
        self.pt.update_weight('1', choices['1'])
        return self.pt.sample_item()

    @staticmethod
    def to_binary_string(number):
        return format(number, '064b')
