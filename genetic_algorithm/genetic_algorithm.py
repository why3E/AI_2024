import random

# 설정값
random.seed('ai_test')
POP_SIZE = 5
MUT_RATE = 0.2
CHROM_SIZE = 6
actual_solution = []


def create_solution():
    global actual_solution
    actual_solution = random.sample(range(10), CHROM_SIZE)


def init_population(size):
    return [random.sample(range(10), CHROM_SIZE) for _ in range(size)]


def fitness(chrom):
    return sum(
        5 if chrom[i] == actual_solution[i] else 1 if chrom[i] in actual_solution else 0 for i in range(CHROM_SIZE))


def select(pop):
    total_fit = sum(fitness(ch) for ch in pop)
    pick = random.uniform(0, total_fit)
    current = 0
    for ch in pop:
        current += fitness(ch)
        if current > pick:
            return ch


def crossover(p1, p2):
    point = random.randint(1, CHROM_SIZE - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def mutate(ch):
    for i in range(CHROM_SIZE):
        if random.random() < MUT_RATE:
            ch[i] = random.choice([g for g in range(10) if g not in ch])


if __name__ == "__main__":
    size = POP_SIZE
    for a in range(8):
        create_solution()
        best_fit, iterations = -1, 0
        pop = init_population(size)

        while best_fit < CHROM_SIZE * 5:
            best = max(pop, key=fitness)
            best_fit = fitness(best)
            next_gen = []
            for _ in range(size // 2):
                c1, c2 = crossover(select(pop), select(pop))
                next_gen.extend([c1, c2])
            pop = next_gen
            for ch in pop:
                mutate(ch)
            iterations += 1

        print(f"Experiment {a + 1}:")
        print(f"- Population Size: {size}")
        print(f"- Iterations to Solution: {iterations}")
        print(f"- Actual Solution: {actual_solution}")
        print(f"- Best Found Solution: {best}")
        print("-" * 60)

        size *= 2


"""
Experiment 1:
- Population Size: 5
- Iterations to Solution: 4304
- Actual Solution: [1, 0, 4, 9, 7, 5]
- Best Found Solution: [1, 0, 4, 9, 7, 5]
------------------------------------------------------------
Experiment 2:
- Population Size: 10
- Iterations to Solution: 351
- Actual Solution: [1, 6, 9, 4, 5, 8]
- Best Found Solution: [1, 6, 9, 4, 5, 8]
------------------------------------------------------------
Experiment 3:
- Population Size: 20
- Iterations to Solution: 53
- Actual Solution: [9, 2, 6, 0, 7, 4]
- Best Found Solution: [9, 2, 6, 0, 7, 4]
------------------------------------------------------------
Experiment 4:
- Population Size: 40
- Iterations to Solution: 14
- Actual Solution: [1, 2, 6, 7, 0, 4]
- Best Found Solution: [1, 2, 6, 7, 0, 4]
------------------------------------------------------------
Experiment 5:
- Population Size: 80
- Iterations to Solution: 5
- Actual Solution: [4, 8, 3, 6, 2, 9]
- Best Found Solution: [4, 8, 3, 6, 2, 9]
------------------------------------------------------------
Experiment 6:
- Population Size: 160
- Iterations to Solution: 10
- Actual Solution: [6, 1, 0, 2, 5, 7]
- Best Found Solution: [6, 1, 0, 2, 5, 7]
------------------------------------------------------------
Experiment 7:
- Population Size: 320
- Iterations to Solution: 6
- Actual Solution: [1, 4, 6, 8, 9, 2]
- Best Found Solution: [1, 4, 6, 8, 9, 2]
------------------------------------------------------------
Experiment 8:
- Population Size: 640
- Iterations to Solution: 9
- Actual Solution: [4, 3, 6, 0, 1, 9]
- Best Found Solution: [4, 3, 6, 0, 1, 9]
------------------------------------------------------------
"""