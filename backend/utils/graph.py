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
        return float("Distance not found")

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
    def dijkstraRoute(self, toNode):
        heap = minHeap()
        distances = {} # dictionary holding distances between nodes
        traversed = {} # key: adjNode, value: currentNode

        for node in self.graph:
            distances[node] = float('inf') #leaves each node equal to infinity
        
        for node in self.graph:
            heap.array.append(heap.newMinHeapNode(node, distances[node]))
            heap.position.append(node)
        heap.size = len(heap.array)

        while heap.size > 0:
            minNode = heap.extractMin()
            if(minNode == None):
                return "no node to extract"
            currentNode = minNode[0]

            if currentNode == toNode:
                path = []
                for node in traversed:
                    path.append(node)
                    node = traversed[node]
                return path

            for adjNode, distance in self.graph[currentNode]:
                if heap.isInMinHeap(adjNode):
                    newDistance = distances[adjNode] + distance
                    if newDistance < distances[adjNode]:
                        distances[adjNode] = newDistance
                        traversed[adjNode] = currentNode
                        heap.decreaseKey(adjNode, newDistance)
                
    def aStarRoute(self, toNode):
        pass