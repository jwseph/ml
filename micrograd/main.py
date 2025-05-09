import numpy as np

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    # def __pow__(self, other):
    #     # self ** other == e ** (other * ln(self))
    #     return (other * self.log()).exp()
    
    # def __rpow__(self, other):
    #     # other ** self == e ** (self * ln(other))
    #     other = other if isinstance(other, Value) else Value(other)
    #     return (self * other.log()).exp()
    
    def exp(self):
        out = Value(np.exp(self.data), (self,), 'exp')

        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward

        return out
    
    def log(self):
        out = Value(np.log(self.data), (self,), 'log')

        def _backward():
            self.grad += 1 / self.data * out.grad
        out._backward = _backward

        return out
    
    def cos(self):
        out = Value(np.cos(self.data), (self,), 'cos')

        def _backward():
            self.grad += -np.sin(self.data) * out.grad
        out._backward = _backward

        return out

    def arctan(self):
        out = Value(np.arctan(self.data), (self,), 'arctan')

        def _backward():
            self.grad += 1 / (1 + self.data**2) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out

    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self): # -self
        return self * -1

    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"



'''



1   3   1
0   5   1
0   0  



'''

if __name__ == "__main__":
    import sympy

    X = np.array([[1, 4, 2], [-4, -11, -7], [0, 10, -2]])

    # Display reduced row echelon form as a 3 x 4 matrix
    print(sympy.Matrix(X).rref())
    print(f'Rank: {sympy.Matrix(X).rank()}')