
class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self.rgba = [r, g, b, a]

    def set(self, other):
        self.rgba = other.rgba[:]
        
    def set_color(self, r, g, b, a=1.0):
        self.rgba = [r, g, b, a]

    def cap(self):
        m = max(self.rgba)
        if m > 1:
            self.dim(1/m)
            
    def dim(self, factor):
        self.rgba[0] *= factor
        self.rgba[1] *= factor
        self.rgba[2] *= factor

    def mult(self, other):
        self.rgba = [
            self.rgba[i] * other.rgba[i] for i in range(4)
        ]

    def add(self, other):
        self.rgba[0] += other.rgba[0]
        self.rgba[1] += other.rgba[1]
        self.rgba[2] += other.rgba[2]

    def add_mix(self, other, t):
        self.rgba[0] += (other.rgba[0] - self.rgba[0]) * t
        self.rgba[1] += (other.rgba[1] - self.rgba[1]) * t
        self.rgba[2] += (other.rgba[2] - self.rgba[2]) * t

    def __repr__(self):
        return f"Color({self.rgba[0]:.3f}, {self.rgba[1]:.3f}, {self.rgba[2]:.3f})"
