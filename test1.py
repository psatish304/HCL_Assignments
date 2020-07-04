class Node:  
    def __init__(self, data): 
        self.data = data 
        self.left = None
        self.right = None
        
    parents = [] # saving parent paths
    @staticmethod
    def parentAccessing(root, target): 
        if root == None: 
            return False
        if root.data == target: 
            return True
        if (Node.parentAccessing(root.left, target) or
            Node.parentAccessing(root.right, target)): 
            
            # saving nearest parent node
            Node.parents.append(root.data)
            return True
        return False

# Creating Tree
root = Node(2) 
root.left = Node(1) 
root.right = Node(3) 
root.right.left = Node(4) 
root.right.right = Node(5) 
root.right.right.right = Node(6) 
# root.right.right.left = Node(7) 
# root.right.right.right.left = Node(8)
# root.right.right.right.left.right = Node(11)
# root.right.right.right.left.left = Node(10)
# root.right.right.right.right = Node(9)  
if __name__ == '__main__':

    def nearestParents(key1, key2):
       # key1 and key2 are nodes that we want to search in tree
        Node.parentAccessing(root, target = key1) 
        Node.parentAccessing(root, target = key2)
        common = ([x for x in Node.parents if Node.parents.count(x) > 1])
        if len(common) >=2:
        # Considering only nearest two nodes
            print(' and '.join(str(i) for i in set(common[0:2])))
        else:
            print(' and '.join(str(i) for i in set(common)))
        Node.parents = []
    nearestParents(3,6) # 2
    nearestParents(1,5) # 2
    nearestParents(4,6) # 2 and 3