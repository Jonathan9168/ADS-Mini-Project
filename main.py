class STNode:
    def __init__(self, d, l, m, r):
        self.data = d
        self.left = l
        self.right = r
        self.fwd = m
        self.mult = 0

    # prints the node and all its children in a string
    def __str__(self):
        st = "(" + str(self.data) + ", " + str(self.mult) + ") -> ["
        if self.left is not None:
            st += str(self.left)
        else:
            st += "None"
        if self.fwd is not None:
            st += ", " + str(self.fwd)
        else:
            st += ", None"
        if self.right is not None:
            st += ", " + str(self.right)
        else:
            st += ", None"
        return st + "]"


class StringTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.currentStrings = []

    def __str__(self):
        return str(self.root)

    def add(self, st):
        if st == "":
            return None
        if self.root is None:
            self.root = STNode(st[0], None, None, None)
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while True:
                if d == ptr.data:
                    break
                elif d < ptr.data:
                    if ptr.left is None:
                        ptr.left = STNode(d, None, None, None)
                    ptr = ptr.left
                else:
                    if ptr.right is None:
                        ptr.right = STNode(d, None, None, None)
                    ptr = ptr.right
            if i < len(st) - 1 and ptr.fwd is None:
                ptr.fwd = STNode(st[i + 1], None, None, None)
            if i < len(st) - 1:
                ptr = ptr.fwd
        ptr.mult += 1
        self.size += 1

    def addAll(self, A):
        for x in A: self.add(x)

    def printAll(self):
        def printFrom(ptr, s):
            if ptr is None: return
            s0 = s + ptr.data
            for i in range(ptr.mult, 0, -1): print(s0)
            if ptr.left is not None: printFrom(ptr.left, s)
            if ptr.fwd is not None: printFrom(ptr.fwd, s + ptr.data)
            if ptr.right is not None: printFrom(ptr.right, s)

        printFrom(self.root, "")

    def count(self, st):
        if st == "": return None
        charsLeft = len(st)
        ptr = self.root
        for i in range(len(st)):
            while ptr is not None:
                if ptr.data == st[i]:
                    charsLeft -= 1
                    if charsLeft == 0:
                        return ptr.mult
                    if charsLeft > 0 and ptr.fwd is None:
                        return 0
                    ptr = ptr.fwd
                    break
                elif ptr.data < st[i]:
                    ptr = ptr.right
                else:
                    ptr = ptr.left
        return 0

    def min(self):
        if self.root is None: return None
        minStr = ""
        ptr = self.root
        # Check if only one word present if so, simply go forward till end of word
        if self.size == 1:
            while ptr is not None:
                minStr += ptr.data
                ptr = ptr.fwd
            return minStr

        # Go to left most node to find least significant letter lexicographically
        while ptr.left is not None:
            ptr = ptr.left
        minStr += ptr.data

        while ptr is not None:
            # Check if there are any single letter strings
            if ptr.left is None and ptr.mult > 0:
                return minStr

            ptr = ptr.fwd
            while ptr.left is not None:
                ptr = ptr.left

            # If no left node then append letter
            if ptr.left is None:
                minStr += ptr.data
            else:
                # Else go left and check if the string is done
                ptr = ptr.left
                if ptr.mult > 0 and ptr.left is None:
                    minStr += ptr.data
                    return minStr
                minStr += ptr.data

        return minStr

    def append(self, A, v):
        B = [None for _ in range(len(A) + 1)]
        for i in range(len(A)):
            B[i] = A[i]
        B[-1] = v
        return B

    def arrayConcat(self, A, B):
        temp = [None for _ in range(len(A) + len(B))]
        counter = 0
        for i in range(len(A)):
            temp[i] = A[i]
        for i in range(len(A), len(temp)):
            temp[i] = B[counter]
            counter += 1
        return temp

    def nullify(self):
        self.root = None
        self.size = 0
        self.currentStrings = []

    def removeString(self, st):
        A = self.currentStrings
        for i in range(len(A)):
            if A[i] == st:
                self.currentStrings = self.arrayConcat(A[:i], A[i + 1:])

    def remove(self, st):
        if self.root is None or st == "": return None
        self.toArray()
        self.removeString(st)
        new = self.currentStrings
        self.nullify()
        self.addAll(new)

    def toArray(self):
        def printFrom(ptr, s, A):
            if ptr is None: return
            s0 = s + ptr.data
            for i in range(ptr.mult, 0, -1): self.currentStrings = self.append(self.currentStrings, s0)
            if ptr.left is not None: printFrom(ptr.left, s, A)
            if ptr.fwd is not None: printFrom(ptr.fwd, s + ptr.data, A)
            if ptr.right is not None: printFrom(ptr.right, s, A)

        printFrom(self.root, "", [])


def testprint(t, message):
    print("\n" + message, "tree is:", t)
    print("Count 'ca', 'can', 'car', 'cat', 'cats':", t.count("ca"), t.count("can"),
          t.count("car"), t.count("cat"), t.count("cats"))
    print("Size is:", t.size, ", min is:", t.min())
    t.printAll()


t = StringTree()
t.addAll(["car", "can", "cat", "cat", "cat"])
testprint(t, "Initially")
t.add("")
testprint(t, "After adding the empty string")
t.add("ca")
testprint(t, "After adding 'ca'")
t.remove("car")
testprint(t, "After removing 'car'")
t.remove("cat")
t.remove("cat")
testprint(t, "After removing 'cat' twice")
t.remove("ca")
t.add("cats")
testprint(t, "After removing 'ca' and adding 'cats'")
t.remove("can")
t.remove("cats")
t.remove("cat")
print(t, t.size)
