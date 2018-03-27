class AnimationMiddleware:
    def __init__(self, parent=None, left=None, right=None):
        self.animation = []
        self.parent = parent
        self.left = left
        self.right = right

    def process(self, data):
        if self.parent is None:
            self.left = 0
            self.right = len(data)
            self.animation.append(data[:])
        else:
            parent_data = self.parent.last_data()
            # extend data with parent data
            res = parent_data[self.parent.left:self.left] + data + parent_data[self.right:self.parent.right]
            self.parent.process(res)
        return self

    def last_data(self):
        return self.parent.last_data() if self.parent else self.animation[-1]

    def dive(self, left, right):
        return AnimationMiddleware(self, self.left + left, self.left + right)


class GroupOfMiddlewares:
    def __init__(self, group=[]):
        if isinstance(group, list):
            self.group = group
        else:
            self.group = [group]

    def __getattr__(self, item):
        return ExecuteGroup(self.group, item)


class ExecuteGroup:
    def __init__(self, group, method_name):
        self.group = group
        self.method_name = method_name

    def __call__(self, *arg, **kwarg):
        res = []
        for middleware in self.group:
            m = getattr(middleware, self.method_name)
            res.append(m(*arg, **kwarg))
        return GroupOfMiddlewares(res)


# testing

a1 = AnimationMiddleware()
a2 = AnimationMiddleware()

g = GroupOfMiddlewares([a1, a2])

g.process('hello world')
assert a1.animation == ['hello world'], a1.animation
assert a2.animation == ['hello world'], a2.animation

g.dive(0, 5).process('*****').dive(1, 4).process('---')
g.dive(6, 11).process('*****')
assert a1.animation == ['hello world', '***** world', '*---* world', '*---* *****'], a1.animation
assert a2.animation == ['hello world', '***** world', '*---* world', '*---* *****'], a2.animation

__all__ = [
    AnimationMiddleware,
    GroupOfMiddlewares,
]
