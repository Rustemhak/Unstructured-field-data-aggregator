# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class Matrix:
    
    def __init__(self) -> None:
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e0_ = 0
        self.f = 0
        self.init()
    
    def set0_(self, a_ : float, b_ : float, c_ : float, d_ : float, e0__ : float, f_ : float) -> None:
        self.a = a_
        self.b = b_
        self.c = c_
        self.d = d_
        self.e0_ = e0__
        self.f = f_
    
    def __str__(self) -> str:
        return "[{0} {1} {2} {3} {4} {5}]".format(self.a, self.b, self.c, self.d, self.e0_, self.f)
    
    def init(self) -> None:
        self.a = (1)
        self.b = (0)
        self.c = (0)
        self.d = (1)
        self.e0_ = (0)
        self.f = (0)
    
    def copy_from(self, m : 'Matrix') -> None:
        self.a = m.a
        self.b = m.b
        self.c = m.c
        self.d = m.d
        self.e0_ = m.e0_
        self.f = m.f
    
    def multiply(self, m : 'Matrix') -> None:
        a_ = (self.a * m.a) + (self.b * m.c)
        b_ = (self.a * m.b) + (self.b * m.d)
        c_ = (self.c * m.a) + (self.d * m.c)
        d_ = (self.c * m.b) + (self.d * m.d)
        e0__ = (self.e0_ * m.a) + (self.f * m.c) + m.e0_
        f_ = (self.e0_ * m.b) + (self.f * m.d) + m.f
        self.set0_(a_, b_, c_, d_, e0__, f_)
    
    def translate(self, e0__ : float, f_ : float) -> None:
        self.e0_ = ((self.a * e0__) + (self.c * f_) + self.e0_)
        self.f = ((self.b * e0__) + (self.d * f_) + self.f)