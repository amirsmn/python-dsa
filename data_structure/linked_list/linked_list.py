

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f"Node(value={repr(self.value)})"

    def __str__(self):
        return f"{self.value}"


class LinkedList:
    def __init__(self):
        self.head = None
        self.__len = 0

    def append(self, value):
        if not self.head:
            self.head = Node(value)
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = Node(value)

        self.__len += 1

    def appendleft(self, value):
        new_head = Node(value)
        new_head.next = self.head
        self.head = new_head
        self.__len += 1

    def insert(self, value, position):
        if position < 0:
            position += self.__len

        if position <= 0:
            self.appendleft(value)
        elif position >= self.__len:
            self.append(value)
        else:
            pre_node = self.head
            for _ in range(position - 1):
                pre_node = pre_node.next

            new_node = Node(value)
            new_node.next = pre_node.next
            pre_node.next = new_node
            self.__len += 1

    def insert_after(self, target, new_value):
        current_node = self.head
        while current_node:
            if current_node.value == target:
                new_node = Node(new_value)
                new_node.next = current_node.next
                current_node.next = new_node
                self.__len += 1
                return
            current_node = current_node.next

    def insert_before(self, target, new_value):
        current_node = self.head
        pre_node = None
        while current_node:
            if current_node.value == target:
                if pre_node is None:
                    self.appendleft(new_value)
                else:
                    new_node = Node(new_value)
                    pre_node.next = new_node
                    new_node.next = current_node
                    self.__len += 1
                return

            pre_node = current_node
            current_node = current_node.next

    def pop(self):
        if not self.head:
            raise IndexError("pop from an empty linked list")
        elif not self.head.next:
            popped_value = self.head.value
            self.head = None
        else:
            current_node = self.head
            while current_node.next.next:
                current_node = current_node.next
            popped_value = current_node.next.value
            current_node.next = None

        self.__len -= 1
        return popped_value

    def popleft(self):
        if not self.head:
            raise IndexError("pop from an empty linked list")

        popped_value = self.head.value
        self.head = self.head.next
        self.__len -= 1
        return popped_value

    def remove(self, value):
        if not self.head:
            pass
        elif self.head.value == value:
            self.head = self.head.next
            self.__len -= 1
            return
        else:
            current_node = self.head
            while current_node and current_node.next:
                if current_node.next.value == value:
                    current_node.next = current_node.next.next
                    self.__len -= 1
                    return
                current_node = current_node.next

        raise ValueError(f"{value} is not in linked list")

    def __repr__(self):
        nodes = []
        node = self.head
        while node:
            nodes.append(repr(node))
            node = node.next

        return f"LinkedList([{', '.join(nodes)}])"

    def __str__(self):
        node_values = []
        node = self.head
        while node:
            node_values.append(str(node))
            node = node.next
        if not node_values:
            return "[]"
        return f"[{" -> ".join(node_values)}]"

    def __len__(self):
        return self.__len

