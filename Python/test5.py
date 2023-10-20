class ListNode:
    def __init__(self, x):
        self.val = x     # 节点值
        self.next = None # 后继节点引用

# 实例化节点
n1 = ListNode(4) # 节点 head
n2 = ListNode(5)
n3 = ListNode(1)

# 构建引用指向
n1.next = n2
n2.next = n3
