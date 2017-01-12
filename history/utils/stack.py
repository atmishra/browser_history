class Stack(object):

    def __init__(self, items=[], current_index=-1):
        self.items = items
        self.current_index = current_index

    def isEmpty(self):
        return self.items == []

    def push(self, item):

        self.pop_multiple()

        self.items.append(item)
        self.current_index += 1

    def pop_multiple(self):
        if len(self.items) > 0 and self.current_index != (len(self.items) - 1):
            for i in range(self.current_index + 1, len(self.items)):

                self.items.pop(self.current_index + 1)

    def peek(self):
        return self.items[self.current_index - 1]

    def back(self):
        if self.current_index > 0:

            self.current_index -= 1

            return self.items[self.current_index]
        else:
            self.current_index = -1
            return -1

    def forward(self):
        if self.current_index >= len(self.items) - 1:
            self.current_index = len(self.items) - 1
            return -1

        else:
            self.current_index += 1

            return self.items[self.current_index]

    def size(self):
        return len(self.items)

    def last_ten(self):
        return self.items[self.current_index::-1][:10]

    def show(self):
        print(self.items)
