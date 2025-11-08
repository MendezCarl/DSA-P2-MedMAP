from collections import defaultdict
from heap import minHeap

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    #fromNode is a tuple (lat, lon)
    #toNode is a tuple (lat, lon)
    #weight is the distance between the two nodes
    def addEdge(self, fromNode, toNode, dist):
        newNode = (toNode, dist)
        self.graph[fromNode].append(newNode)

    def getAdjNodes(self, index):
        return self.graph[index]

    def getWeight(self, fromNode, toNode):
        for adjNode, dist in self.graph[fromNode]:
            if adjNode == toNode:
                return dist
        return float("inf")

    def sumEdge(self, fromNode, toNode):
        total = 0
        for adjNode, dist in self.graph[fromNode]:
            total += dist
        return total

    def printGraph(self):
        for node in self.graph:
            print(f"Node {node}:", end="")
            for adjNode, dist in self.graph[node]:
                print(f" -> {adjNode} (weight {dist})", end="")
            print()

    # dist[v] = dist[u] + weight[u][v]
    def dijkstraRoute(self, fromNode, toNode):
        heap = minHeap()
        distances = {} # dictionary holding distances between nodes
        traversed = {} # key: adjNode, value: currentNode

        for node in self.graph:
            distances[node] = float('inf') #leaves each node equal to infinity

        distances[fromNode] = 0
        
        for node in self.graph:
            heap.newMinHeapNode(node, distances[node])
        # heap.size = len(heap.array)

        while heap.size > 0:
            minNode = heap.extractMin()
            if(minNode == None):
                return "no node to extract"
            currentNode = minNode[0]

            if currentNode == toNode:
                path = []
                pathNode = currentNode               
                while pathNode in traversed:
                    path.append(pathNode)
                    pathNode = traversed[pathNode]
                path.append(fromNode)
                return path[::-1]

            for adjNode, distance in self.graph[currentNode]:
                if heap.isInMinHeap(adjNode):
                    newDistance = distances[currentNode] + distance
                    if newDistance < distances[adjNode]:
                        distances[adjNode] = newDistance
                        traversed[adjNode] = currentNode
                        heap.decreaseKey(adjNode, newDistance)
        return "No path found Dijkstras"
                
    # f(n) = g(n) + h(n)
    # g(n) is the cost of the path
    # h(n) is the heuristic cost of the path from current node n to goal node

    # will be using h(n): manhattan distance
    def aStarRoute(self, fromNode, toNode):
        heap = minHeap()
        fScore = {}
        gScore = {}
        traversed = {}

        for node in self.graph:
            gScore[node] = float('inf')
            fScore[node] = float('inf')
        gScore[fromNode] = 0
        fScore[fromNode] = 0
        
        for node in self.graph:
            heap.newMinHeapNode(node, fScore[node])

        while heap.size > 0:
            minNode = heap.extractMin()
            if (minNode == None):
                return "no node to extract"
            currentNode = minNode[0]

            if currentNode == toNode:
                path = []
                pathNode = currentNode
                while pathNode in traversed:
                    path.append(pathNode)
                    pathNode = traversed[pathNode]
                path.append(fromNode)
                return path[::-1]
            
            for adjNode, g in self.graph[currentNode]:
                if heap.isInMinHeap(adjNode):
                    newG = gScore[currentNode] + g
                    if newG < gScore[adjNode]:
                        hScore = abs(adjNode[0] - toNode[0]) + abs(adjNode[1] - toNode[1]) #heuristic score of the adjNode
                        gScore[adjNode] = newG
                        fScore[adjNode] = gScore[adjNode] + hScore
                        traversed[adjNode] = currentNode
                        heap.decreaseKey(adjNode, fScore[adjNode])
        return "No path found with A*"

