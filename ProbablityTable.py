import random


class ProbabilityTable:
    def __init__(self):
        self.table = {}
        self.total_weight = 0.0

    def add_item(self, item, weight):
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.table[item] = weight
        self.total_weight += weight

    def update_weight(self, item, new_weight):
        if new_weight < 0:
            raise ValueError("Weight cannot be negative.")
        if item not in self.table:
            raise ValueError("Item not found in the probability table.")
        self.total_weight -= self.table[item]
        self.total_weight += new_weight
        self.table[item] = new_weight

    def calculate_probability(self, item):
        if item not in self.table:
            raise ValueError("Item not found in the probability table.")
        weight = self.table[item]
        probability = weight / self.total_weight
        return probability

    def sample_item(self):
        if not self.table:
            raise ValueError("Probability table is empty.")
        random_num = random.uniform(0, self.total_weight)
        cumulative_weight = 0.0
        for item, weight in self.table.items():
            cumulative_weight += weight
            if random_num <= cumulative_weight:
                return item
