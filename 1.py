import sys

class Node:
	def __init__(self, val = None, left = None, right = None, parent = None, number = None, balance = None):
		self.val = val
		self.left = left
		self.right = right
		self.height = 1
		self.number = number
		self.parent = parent
		self.balance = balance

n = int(sys.stdin.readline())
if n == 0:
	print(0)
	sys.exit(0)
sys.setrecursionlimit(900000000)

# arr = [Node() for i in range(n)]

# -------- функции баланса дерева -------
def height(node):
	if node:
		return node.height
	else:
		return 0

def b_factor(node):
    if not node:
        return

    return height(node.right) - height(node.left)

def fix_height(node):
    if not node:
        return

    node.height = max(height(node.left), height(node.right)) + 1
    return node

# ------- первая вставка в дерево ------
head = None

# ------ вставка в дерево ---------
def insert(node, val):
	if not node:
		return Node(val)

	if val < node.val:
		node.left = insert(node.left, val)

	if val > node.val:
		node.right = insert(node.right, val)

	return balance(node)


def left_turn(node):
    tmp = node.right
    node.right = tmp.left

    tmp.left = node
    node = fix_height(node)
    tmp = fix_height(tmp)
    return tmp

def right_turn(node):
    tmp = node.left
    node.left = tmp.right

    tmp.right = node
    node = fix_height(node)
    tmp = fix_height(tmp)
    return tmp

def balance(node):
    if not node:
        return

    node = fix_height(node)

    if b_factor(node) > 1:
        if b_factor(node.right) < 0:
            node.right = right_turn(node.right)
            return left_turn(node)
        else:
            return left_turn(node)
    elif b_factor(node) < -1:
        if b_factor(node.left) > 0:
            node.left = left_turn(node.left)
            return right_turn(node)
        else:
            return right_turn(node)
            
    return node

#------- функция поиска по дереву ------
def exist(node, val):
	if not node:
		return 'N'

	if val < node.val:
		return exist(node.left, val)

	elif val > node.val:
		return exist(node.right, val)

	else:
		return 'Y'

def find(node, val):
	if not node:
		return

	sys.stdout.write(f'{exist(head, val)}' + '\n')
	
	
# ------- функция удаления --------
def delete(node, val):
	if not node:
		return head 

	if val < node.val:
		node.left = delete(node.left, val)
		return balance(node)

	if val > node.val:
		node.right =delete(node.right, val)
		return balance(node)

	if val == node.val:
		left = node.left
		right = node.right
		del(node)
		if not left:
			return right
		# if not node.left and node.right:
		# 	tmp = node.right
		# 	node = None
		# 	return tmp
		# if not node.right and node.left:
		# 	tmp = node.left
		# 	node = None
		# 	return tmp
		# if not node.left and not node.right:
		# 	node = None
		# 	return node

		tmp = get_max(left)
		# right = node.right
		tmp.left = delete_max(left)
		tmp.right = right
		return balance(tmp)

	else:
		return balance(node)


def get_max(node):
    current = node

    while current.right:
        current = current.right
    
    return current

def delete_max(node):
	if not node.right:
		return node.left

	node.right = delete_max(node.right)
	return balance(node)

for i in range(n):
	operation, val = sys.stdin.readline().split()
	if operation == 'A':
		head = insert(head, int(val))
		if head:
			res = b_factor(head)
			sys.stdout.write(str(res) + '\n')
		else:
			sys.stdout.write(str(0) + '\n')
	if operation == 'D':
		head = delete(head, int(val))
		if head:
			res = b_factor(head)
			sys.stdout.write(str(res) + '\n')
		else:
			sys.stdout.write(str(0) + '\n')
		
	if operation == 'C':
		if head:
			find(head, int(val))
		else:
			sys.stdout.write('N')
		