import heapq
import math


class Interval():
    def __init__(self, left_endpoint, right_endpoint, l_closed, r_closed):
        self.left_endpoint = left_endpoint
        self.right_endpoint = right_endpoint
        self.left_closed = l_closed
        self.right_closed = r_closed

    def __repr__(self):
        s = "{}, {}".format(self.left_endpoint, self.right_endpoint)
        if self.left_closed:
            left_bracket = '['
        else:
            left_bracket = '('

        if self.right_closed:
            right_bracket = ']'
        else:
            right_bracket = ')'
        interval_string = left_bracket + s + right_bracket
        return 'Interval({})'.format(interval_string)

    def contains(self, interval1):
        interval2 = self
        if interval1.left_endpoint < interval2.left_endpoint:
            return False
        if interval1.left_endpoint == interval2.left_endpoint:
            if not interval2.left_closed:
                return False
        if interval1.right_endpoint > interval2.right_endpoint:
            return False
        if interval1.right_endpoint == interval2.right_endpoint:
            if not interval2.right_closed:
                return False
        return True

    def intersects(self, interval):
        if self.left_endpoint == interval.right_endpoint:
            if self.left_closed and interval.right_closed:
                return True
            else:
                return False

        if self.right_endpoint == interval.left_endpoint:
            if self.right_closed and interval.left_closed:
                return True
            else:
                return False

        left_point = interval.left_endpoint
        point_interval = Interval(left_point, left_point, True, True)
        if self.contains(point_interval):
            return True

        right_point = interval.right_endpoint
        point_interval = Interval(right_point, right_point, True, True)
        if self.contains(point_interval):
            return True
        else:
            return False


class TreeNode():
    def __init__(self, left_endpoint, right_endpoint, l_closed, r_closed):
        self.left = None
        self.right = None
        intv = Interval(left_endpoint, right_endpoint, l_closed, r_closed)
        self.interval = intv
        self.left_endpoint = left_endpoint
        self.right_endpoint = right_endpoint
        self.left_closed = l_closed
        self.right_closed = r_closed
        self.subset = []

    def __repr__(self):
        s = "{}, {}".format(self.left_endpoint, self.right_endpoint)
        if self.left_closed:
            left_bracket = '['
        else:
            left_bracket = '('

        if self.right_closed:
            right_bracket = ']'
        else:
            right_bracket = ')'
        interval_string = left_bracket + s + right_bracket
        return 'TreeNode({})'.format(interval_string)

    def query(self, point):
        point_interval = Interval(point, point, True, True)
        found = []
        for intv in self.subset:
            if intv.contains(point_interval):
                found.append(intv)
        if not self.interval.contains(point_interval):
            return []
        if self.left is not None:
            for intv in self.left.query(point):
                found.append(intv)
        if self.right is not None:
            for intv in self.right.query(point):
                found.append(intv)
        return found


class SegmentTree():
    def __init__(self, intervals):
        self.intervals = intervals
        self.root = None
        self.build_tree()

    def query(self, point):
        if self.root is None:
            raise Exception('tree must be built first')
        return self.root.query(point)

    def build_tree(self):
        intervals = self.intervals
        endpoints = []
        for interval in intervals:
            endpoints.append(interval.left_endpoint)
            endpoints.append(interval.right_endpoint)
        endpoints.append(float('inf'))
        endpoints.append(float('-inf'))

        heapq.heapify(endpoints)
        result = []
        while endpoints:
            ep = heapq.heappop(endpoints)
            if result and result[-1] == ep:
                pass
                # remove duplicate
            else:
                result.append(ep)

        endpoints = result
        elements = []
        for i, ep in enumerate(endpoints):
            if i == 0:
                prev = ep
                continue
            elif i < len(endpoints) - 1:
                elements.append((prev, ep, False, False))
                elements.append((ep, ep, True, True))
                prev = ep
            else:  # i == len(endpoints)-1
                elements.append((prev, ep, False, False))

        num_leaves = len(elements)

        max_depth = int(math.log(num_leaves) / math.log(2)) + 1
        num_last_leaves = 2 * (num_leaves - 2**(max_depth - 1))

        # build tree from bottom to up
        q = []
        for i, elem in enumerate(elements):
            if i < num_last_leaves:
                if i % 2 == 0:
                    prev = elem
                else:
                    left_node = TreeNode(*prev)
                    right_node = TreeNode(*elem)
                    node = TreeNode(prev[0], elem[1], prev[2], elem[3])
                    node.left = left_node
                    node.right = right_node
                    q.append(node)
            else:
                node = TreeNode(*elem)
                q.append(node)

        while len(q) > 1:
            tmp_q = []
            for i, node in enumerate(q):
                if i % 2 == 0:
                    prev = node
                else:
                    left_ep = prev.left_endpoint
                    right_ep = node.right_endpoint
                    l_closed = prev.left_closed
                    r_closed = node.right_closed
                    new_node = TreeNode(left_ep, right_ep, l_closed, r_closed)
                    new_node.left = prev
                    new_node.right = node
                    tmp_q.append(new_node)
            q = tmp_q

        self.root = q[0]

        for interval in intervals:
            self.append_subset(self.root, interval)

        return self.root

    def append_subset(self, node, interval):
        if not node.interval.intersects(interval):
            return None
        elif node.interval.contains(interval):
            node.subset.append(interval)
            return None
        if node.left is not None:
            self.append_subset(node.left, interval)
        if node.right is not None:
            self.append_subset(node.right, interval)


if __name__ == '__main__':
    import random
    intervals = []
    for _ in range(10):
        choice = random.choices(list(range(100)), k=2)
        closed1 = bool(random.choice([0, 1]))
        closed2 = bool(random.choice([0, 1]))
        intv = Interval(min(choice), max(choice), closed1, closed2)
        intervals.append(intv)
        print(intv)

    seg_tree = SegmentTree(intervals)
    print(seg_tree.query(34))
