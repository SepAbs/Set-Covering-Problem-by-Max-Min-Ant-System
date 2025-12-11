from numpy import ones, random, sum, zeros
def fileReader(File):
    print(f"Working on {File}\n")
    Sets = []
    with open(File, "r") as File:
        Contents = File.read().split()
        n, m = int(Contents[0]), int(Contents[1])
        U, Start = {x for x in range(1, n + 1)}, m + 2
        Cost = [int(Contents[Index]) for Index in range (2, Start)]
        Sets += [{"Set": set(), "Cost": -1} for Index in range(0 , m)]
        for i in range(1, n + 1):
            q = int(Contents[Start]) + 1
            for z in range(1, q): 
                Sets[int(Contents[Start + z]) - 1]["Set"].add(i)
            Start += q

        for Index in range(len(Cost)):
            Sets[Index]["Cost"] = t_max
        return U, Sets

class MMAS:
    def __init__(self, numberAnts, numberIterations, Decay, Alpha, Beta):
        self.num_ants, self.num_iterations, self.pheromone_decay, self.alpha, self.beta = numberAnts, numberIterations, Decay, Alpha, Beta
        
    def Solve(self, Problem):
        numberElements, numberSets, bestCost, bestSolution = max([Element for Subset in Problem for Element in Subset]), len(Problem), float("inf"), []
        Pheromone = ones(numberSets)
        for Iteration in range(self.num_iterations):
            Solutions, Costs = [], []
            for Ant in range(self.num_ants):
                uncoveredElements, Solution, totalCost = set(range(1, len(U))), [], 0
                while uncoveredElements:
                    selectedSet = random.choice(range(numberSets), p = self.Probabilities(Problem, Pheromone, Solution, uncoveredElements))
                    Solution.append(selectedSet)
                    uncoveredElements -= Problem[selectedSet]["Set"]
                    totalCost += Problem[selectedSet]["Cost"]

                Solutions.append(Solution)
                Costs.append(totalCost)
                if totalCost < bestCost:
                    bestSolution, bestCost = [Problem[Set]["Set"] for Set in Solution], totalCost
                self.updatePheromone(Pheromone, Solution, Problem)
                #print(bestCost)

            Pheromone *= self.pheromone_decay
        return bestSolution, bestCost

    def Probabilities(self, Problem, Pheromone, Solution, uncoveredElements):
        numberSets = len(Problem)
        Probabilities = zeros(numberSets)
        for Set in range(numberSets):
            if Set not in Solution:
                Probabilities[Set] = (Pheromone[Set] ** self.alpha) * ((len(Problem[Set]["Set"] & uncoveredElements) / len(Problem[Set]["Set"] | uncoveredElements)) ** self.beta)

        return Probabilities / sum(Probabilities)
    
    def updatePheromone(self, Pheromone, Solution, Problem):
        bestDelta, Iteration = min([Problem[Set]["Cost"] for Set in Solution]), 0
        for Set in Solution:
            Pheromone[Set] += 1 / bestDelta
            # All values of phromones must be in interval [t_min, t_max]
            if Pheromone[Set] > t_max:
                Pheromone[Set] = t_max
                
            elif Pheromone[Set] < t_min:
                Pheromone[Set] = t_min

            Iteration += 1

# Files and boundaries for pheromones interval.
Files, t_min, t_max = ["scp41.txt", "scp51.txt", "scp54.txt", "scpa2.txt", "scpb1.txt"], 1, 2

# main()
for File in Files:
    U, Problem = fileReader(File)
    # Low decay causes low evaporation = 0.8
    bestSolution, bestCost = MMAS(numberAnts = 30, numberIterations = 20, Decay = 0.8, Alpha = 3, Beta = 2).Solve(Problem)
    print(f"Best solution: {bestSolution}\n\nBest cost: {bestCost}\n")
print("THE-END")
