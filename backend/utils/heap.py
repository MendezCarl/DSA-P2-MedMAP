from collections import defaultdict

class minHeap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.position = {}

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

            self.minHeapify(smallest)
    
    def extractMin(self):
        if (self.size) == 0:
            return None

        root = self.array[0]
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        self.position[lastNode[0]] = 0
        del self.position[root[0]]

        self.size -= 1
        self.minHeapify(0)

        return root
    
    def decreaseKey(self, node, dist):
        index = self.position[node]
        self.array[index][1] = dist

        while (index > 0 and self.array[index][1] < self.array[(index-1)//2][1]):
            self.position[self.array[index][0]] = (index-1)//2
            self.position[self.array[(index-1)//2][0]] = index
            self.swapMinHeapNode(index, (index-1)//2)

            index = (index-1)//2

    def isInMinHeap(self, node):
        if node in self.position and (self.position[node] < self.size):
            return True
        return False
    

    #location is a tuple of (lat, lon)
    def newMinHeapNode(self, location, dist):
        node = [location, dist]
        self.array.append(node)
        self.position[location] = self.size
        self.size += 1
    
        index = self.size-1
        while index > 0:
            parent = (index-1) // 2
            if self.array[parent][1] > self.array[index][1]:
                self.position[self.array[parent][0]] = index
                self.position[self.array[index][0]] = parent

                self.swapMinHeapNode(parent, index)
                index = parent
            else:
                break
        return node