class Node:
    """ A node in a BST. It may have left and right subtrees """
    def __init__(self, item, left = None, right = None):
        self.item = item
        self.left = left
        self.right = right

class BST:
    """ An implementation of a Binary Search Tree """
    def __init__(self, lst = None):
        self.root = None
        if lst != None:
            for item in lst:
                self.add(item)

    # Non recursive add method, easier to work out the path to the parent        
    def add(self, item):
        """ Add this item to its correct position on the tree """
        # This is a non recursive add method.
        l = []
        if self.root == None: # ... Empty tree ...
            self.root = Node(item, None, None) # ... so, make this the root
        else:
            # Find where to put the item
            child_tree = self.root
            while child_tree != None:
                parent = child_tree
                l.append(parent.item)
                if item < child_tree.item:
                    child_tree = child_tree.left # ... move to the left
                    
                else:
                    
                    child_tree = child_tree.right

            # child_tree should be pointing to the new node, but we've gone too far
            # we need to modify the parent nodes
            if item < parent.item:
                parent.left = Node(item, None, None)
            else:
                parent.right = Node(item, None, None)
        return l[::-1]