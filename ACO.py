# -*- coding: utf-8 -*-

import numpy as np


class AntforBinPacking(object) : 
    def __init__(self, Data, Nant, Niter, rho, alpha=1, beta=1, Bin_size=150, seed=0):
        self.data  = Data
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.pheromone = np.ones((len(self.data),len(self.data))) / (len(self.data)*2)
        self.local_state = np.random.RandomState(seed)
        self.Bin_size = Bin_size
    
    """
    Main loop.
    """
    def run(self) :

        shortest_path = None
        best_path = ("TBD", np.inf)
        for i in range(self.Niter):
            all_paths = self.constructColonyPaths()
            self.depositPheronomes(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print(i+1, ": ", shortest_path[1])
            if shortest_path[1] < best_path[1]:
                best_path = shortest_path            
            self.pheromone * self.rho  #evaporation
        return best_path

    """
    Pheromones update.
    """
    def depositPheronomes(self, all_paths) :

        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        Nsel = int(self.Nant/20) # Proportion of updated paths
        for path,fit in sorted_paths[:Nsel]:
            prev = path[0]
            for move in path:
                self.pheromone[prev,move] += 1.0 / self.data[move] #dist
                prev = move
        self.pheromone /= self.pheromone.sum()

    """
    Evaluate ant path.
    """
    def eval(self, path) :
        
        res = 1
        bin = 0
        for group in path:
            sizeOfGroup = self.data[group]
            if (bin + sizeOfGroup) <= self.Bin_size :
                bin += sizeOfGroup
            else:
                bin = sizeOfGroup
                res += 1
        return res
        
    """
    Build ant path, path is indexes of groups in self.data.
    """
    def constructSolution(self, start) :
        path = []
        path.append(start)
        visited = np.zeros(len(self.data))
        visited[start] = 1
        prev = start
        for i in range(len(self.data) - 1) :
            move = self.nextMove(self.pheromone[prev], self.data[prev], visited)
            path.append(move)
            prev = move
            visited[move] = 1
        return path
    
    """
    Build colony paths.
    """
    def constructColonyPaths(self) :
        all_paths = []
        for i in range(self.Nant):
            path = self.constructSolution(0)
            #constructing pairs: first is the group selection, second is bin filled.
            all_paths.append((path, self.eval(path))) 
            
        return all_paths
    
    """
    Pick next group index for path.
    """
    def nextMove(self, pheromone, prevGroup, visited) :
        pheromone = np.copy(pheromone)
        pheromone[visited==1] = 0
        row = pheromone ** self.alpha * ((1 / prevGroup) ** self.beta)
        norm_row = row / row.sum()
        move = self.local_state.choice(range(len(self.data)), 1, p=norm_row)[0]
        return move