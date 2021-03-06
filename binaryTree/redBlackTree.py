"""redBlackTree.py

This module implements Left-Leaning Red-Black Tree (LLRB)

insertion & deletion takes only O(h) time 

height of the RBT(N nodes) is not bigger than 2logN
- if there are no RED nodes in the tree, h = logN
- if it has the maximum RED nodes, h <= 2logN
"""

import bst_utils


"""constant"""
RED = True
BLACK = False


class Node():
    def __init__(self, key, value, color):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None
    
    def __repr__(self):
        color = 'RED'
        if self.color == BLACK:
            color = 'BLACK'
        return  'Node({},{},{})'.format(self.key, repr(self.value), color)
		

class RedBlackTree():
    def __init__(self):
        self.root = None
    
    def is_empty(self):
        return self.root is None
    
    def is_red(self, node):
        if node is None:
            return False
        return node.color == RED
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        searched, parent = self._search_node(node, key)
        if searched is None:
            return None
        else:
            return searched.value

    def _search_node(self, node, key, parent=None):
        if node is None:
            return None, None
        if key < node.key:
            return self._search_node(node.left, key, parent=node)
        elif key > node.key:
            return self._search_node(node.right, key, parent=node)
        else:
            return node, parent

    def search_less_near(self, key):
        return self._search_less_near(self.root, key)

    def _search_less_near(self, node, key, largest=None):
        """
        search for the node that has smaller and nearest key (not equal)
        """
        if node is None:
            return largest
        elif key < node.key:
            return self._search_less_near(node.left, key, largest=largest)
        elif key > node.key:
            if largest is None or largest.key < node.key:
                largest = node
            return self._search_less_near(node.right, key, largest=largest)
        else:
            return self._search_less_near(node.left, key, largest=largest)

    def search_greater_near(self, key):
        return self._search_greater_near(self.root, key)

    def _search_greater_near(self, node, key, smallest=None):
        """
        search for the node that has greater and nearest key (not equal)
        """
        if node is None:
            return smallest
        elif key < node.key:
            if smallest is None or smallest.key > node.key:
                smallest = node
            return self._search_greater_near(node.left, key, smallest=smallest)
        elif key > node.key:
            return self._search_greater_near(node.right, key, smallest=smallest)
        else:
            return self._search_greater_near(node.right, key, smallest=smallest)

    def rotate_left(self, node):
        """
        move the right red link of a node to the left
        initial status: node is BLACK, node.right is RED 
        this method used to rotate these two nodes counter-clockwise, and make the left child RED (right->BLACK)
        -> node.right move to node's original position, and the node will be the left child of node.right
        """
        t = node.right
        node.right = t.left
        t.left = node
        t.color = node.color
        node.color = RED
        return t 

    def rotate_right(self, node):
        """
        move the left red link of a node to the right
        opposite case of rotate_left(node)
        """
        t = node.left
        node.left = t.right
        t.right = node
        t.color = node.color
        node.color = RED
        return t

    def flip_colors(self, node):
        """
        if two links' color are the same, change both to the other color, 
        and make the parent's color reversed also
        """
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
        self.root.color = BLACK

    def _insert(self, node, key, value):
        """
        insert a new node(RED)
        case 0: right child is RED, left child is BLACK -> rotate_left
        case 1: left child is RED, left child's child is also RED -> rotate_right
        case 2: both two children are RED -> flip_colors
        """
        if node is None:
            return Node(key, value, RED)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        
        if (not self.is_red(node.left)) and self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        return node

    def move_red_left(self, node):
        """
        make the red color node on the left side for deleting a node 
        case 0: node.left & node.left.left are all BLACK, node.right.left is also BLACK -> flip_colors
        case 1: node.left & node.left.left are all BLACK, and node.right.left is RED -> move RED to the left
        """
        self.flip_colors(node)
        if self.is_red(node.right.left):
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)
            self.flip_colors(node)
        return node

    def move_red_right(self, node):
        """
        make the red color node on the right side for deleting a node 
        """
        self.flip_colors(node)
        if self.is_red(node.left.left):
            node = self.rotate_right(node)
            self.flip_colors(node)
        return node

    def minimum_node(self, node):
        """get the minimum key node from the subtree"""
        if node.left is None:
            return node
        else:
            return self.minimum_node(node.left)

    def delete_min(self):
        """delete a node which has the min key"""
        self.root = self._delete_min(self.root)
        self.root.color = BLACK

    def _delete_min(self, node):
        if node.left is None:
            return None
        if (not self.is_red(node.left)) and (not self.is_red(node.left.left)):
            node = self.move_red_left(node)
        node.left = self._delete_min(node.left)
        return self.fix_up(node)
    
    def fix_up(self, node):
        """fix the structure of RBT after deleting a node"""
        if self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)
        return node
    
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if key < node.key:
            if node.left is None:
                raise KeyError(key)
            if not (self.is_red(node.left)) and (not self.is_red(node.left.left)):
                node = self.move_red_left(node)
            node.left = self._delete(node.left, key)
            return node
        else:
            if self.is_red(node.left):
                node = self.rotate_right(node)
            if key == node.key and node.right is None:
                return node.left
            elif node.right is None:
                raise KeyError(key)
            elif (not self.is_red(node.right)) and (not self.is_red(node.right.left)):
                node = self.move_red_right(node)
            
            if key == node.key: # and node.right is not None:
                # remove root
                min_node = self.minimum_node(node.right)
                node.key = min_node.key
                node.value = min_node.value
                node.right = self._delete_min(node.right)
            else:
                node.right = self._delete(node.right, key)
            return self.fix_up(node)
        

if __name__ == '__main__':
    """test"""
    rbt = RedBlackTree()
    rbt.insert(12, 'A')
    rbt.insert(9, 'B')
    rbt.insert(15, 'C')
    rbt.insert(16, 'D')
    rbt.insert(18, 'E')
    
    print(rbt._search_less_near(rbt.root, 12))

    print('after insertion')
    #bst_utils.pre_order(rbt.root)
    bst_utils.print_tree(rbt.root)

    print('delete min')
    rbt.delete_min()

    print('after deletion')
    #bst_utils.pre_order(rbt.root)
    bst_utils.print_tree(rbt.root)

    print('delete 15')
    rbt._delete(rbt.root, 15)

    print('after deletion')
    #bst_utils.pre_order(rbt.root)
    bst_utils.print_tree(rbt.root)

    print('abc', rbt.root.left.right)
