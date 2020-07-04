# Breadth First Order

class Node:
	def __init__(self,data):
		  self.left = None
		  self.right = None
		  self.data = data
  
def level_order(queue):
    travel = []
    if len(arr) == 0:
      return

    node = arr[0]
    arr.pop(0)

    # Caching parent Nodes
    if node.left:
      arr.append(node.left)
    if node.right:
      arr.append(node.right)
    print (node.data, end = '  ')
    travel.append(node.data)
    level_order(arr)


if __name__ == '__main__':
	arr = list()
	root = Node(1)
	arr.append(root)

	# Creating Node
	root.right = Node(2)
	root.right.right = Node(5)
	root.right.right.left = Node(3)
	root.right.right.right = Node(6)
	root.right.right.left.right = Node(4)
	(level_order(arr))



                    
               