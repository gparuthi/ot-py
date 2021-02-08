# Tii(Ins[p1,c1], Ins[p2, c2]) {
#       if p1 < p2  or (p1 = p2 and u1 > u2) // breaking insert-tie using user identifiers (u1, u2)
#             return Ins[p1, c1];  // e.g. Tii(Ins[3, “a”], Ins[4, “b”]) = Ins[3, “a”]
#       else return Ins[p1+1, c1]; } // Tii(Ins[3, “a”], Ins[1, “b”]) = Ins[4, “a”]
 
# Tid(Ins[p1,c1], Del[p2]) {          
#       if p1 <= p2 return Ins[p1, c1]; // e.g. Tid(Ins[3, “a”], Del[4]) = Ins[3, “a”]
#      else return Ins[p1-1, c1]; } // Tid(Ins[3, “a”], Del[1] ) = Ins[2, “a”]
 
# Tdi(Del[p1], Ins[p2, c2]) {
#       if p1 < p2 return Del[p1];  // e.g.  Tdi(Del[3], Ins[4, “b”]) = Del[3]
#       else return Del[p1+1]; } // Tdi(Del[3], Ins[1, “b”]) = Del[4]
 
# Tdd(Del[p1], Del[p2]) {
#       if p1 < p2 return Del[p1]; // e.g.   Tdd(Del[3], Del[4]) = Del[3]
#       else if p1 > p2 return Del[p1-1]; // Tdd(Del[3], Del[1]) = Del[2]
#       else return I; } // breaking delete-tie using I (identity op)  Tdd(Del[3]. Del[3]) = I

from typing import Union
from uuid import uuid1 as uuid

class _OperationBase: 
  pos: int
  value: Union[int, str]
  id: int = uuid()

  def __init__(self, pos, value) -> None:
      self.pos = pos
      self.value = value

  def clone(self):
    return self.__class__(pos=self.pos, value=self.value)

  def __repr__(self) -> str:
      return f"{self.__class__.__name__}(p={self.pos}, v={self.value})"

class Ins(_OperationBase):
  value: str

class Del(_OperationBase):
  value: int

Operation = Union[Ins, Del]

def tii(oi1: Ins, oi2: Ins):
  if oi1.pos > oi2.pos or (oi1.pos == oi2.pos and oi1.id < oi2.id):
    oi1.pos += len(oi2.value)
  return oi1

def tid(oi: Ins, od: Del):
  if oi.pos > od.pos: 
    oi.pos -= od.value
  return oi

def tdi(od: Del, oi: Ins):
  if od.pos >= oi.pos:
    od.pos += len(oi.value)
  return od

def tdd(od1: Del, od2: Del):
  if od1.pos > od2.pos:
    # if od1 pos is within the range of od2's impact
    od2_end = od2.pos + od2.value
    if od1.pos < od2_end:
      overlap = max(0, (od2_end-od1.pos))
      if overlap:
        od1.pos = od2.pos
        od1.value = od1.value - overlap
    else:
      od1.pos -= od2.value
  return od1


def transform(o1: Operation, o2: Operation):
  first = o1.op
  sec = o2.op

  if type(first) == Ins and sec == Del:
    return tid(o1, o2)
  if type(first) == Ins and sec == Ins:
    return tii(o1, o2)
  if type(first) == Del and sec == Del:
    return tdd(o1, o2)
  if type(first) == Del and sec == Ins:
    return tdi(o1, o2)