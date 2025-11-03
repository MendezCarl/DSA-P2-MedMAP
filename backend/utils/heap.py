from collections import defaultdict
import sys

class minHeap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.position = [] #index is the vertex, value is the position in the heap array

    #location is a tuple of (lat, lon)
    def newMinHeapNode(self, location, dist):
        node = [location, dist]
        return node

    def swapMinHeapNode(self, a, b):
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp

    def minHeapify(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if (left < self.size and self.array[left][1] < self.array[smallest][1]):
            smallest = left
        if (right < self.size and self.array[right][1] < self.array[smallest][1]):
            smallest = right
        
        if (smallest != index):
            self.position[self.array[smallest][0]] = index
            self.position[self.array[index][0]] = smallest

            self.swapMinHeapNode(smallest, index)

            self.minHeapify(smallest) #recursive call
    
    def extractMin(self):
        if (self.size) == 0:
            return None

        root = self.array[0]
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        self.position[lastNode[0]] = 0
        del self.position[root[0]]

        self.size -= 1
        self.minHeapify(0) # heapify from root

        return root
    
    def decreaseKey(self, node, dist):
        index = self.position[node]
        self.array[index][1] = dist #updating distance value

        while (index > 0 and self.array[index][1] < self.array[(index-1)//2][1]): #log n implementation
            self.position[self.array[index][0]] = (index-1)//2 #swaps position
            self.position[self.array[(index-1)//2][0]] = index
            self.swapMinHeapNode(index, (index-1)//2)

            index = (index-1)//2

    def isInMinHeap(self, node):
        if (self.position[node] < self.size):
            return True
        return False


        