from ot import Ins, Del, tii, tid, tdi, tdd, transform
from uuid import UUID

def assert_op(op, p, v):
  assert(op.pos==p)
  assert(op.value==v)

def test_tdd():
  o1 = Del(pos=1, value=3)
  o2 = Del(pos=1, value=3)
  to = tdd(o1, o2)
  assert_op(to, 1, 3)

  o1 = Del(pos=0, value=3)
  o2 = Del(pos=2, value=6)
  to = tdd(o2, o1)
  assert_op(to, 0, 5)

  o1 = Del(pos=0, value=3)
  o2 = Del(pos=10, value=6)
  to = tdd(o2, o1)
  assert_op(to, 7, 6)

def test_tid():
  oi_val = "hahaha"
  o1 = Ins(pos=1, value=oi_val)
  o2 = Del(pos=1, value=3)
  to = tid(o1, o2)
  assert_op(to, 1, oi_val)

  o1 = Ins(pos=10, value=oi_val)
  o2 = Del(pos=1, value=3)
  to = tid(o1, o2)
  assert_op(to, 7, oi_val)

  o1 = Ins(pos=1, value=oi_val)
  o2 = Del(pos=10, value=3)
  to = tid(o1, o2)
  assert_op(to, 1, oi_val)
  
def test_tdi():
  oi_val = "hahaha"
  
  o1 = Del(pos=1, value=3)
  o2 = Ins(pos=1, value=oi_val)
  to = tdi(o1, o2)
  assert_op(to, 1+len(oi_val), 3)

  o1 = Del(pos=1, value=3)
  o2 = Ins(pos=10, value=oi_val)
  to = tdi(o1, o2)
  assert_op(to, 1, 3)

  o1 = Del(pos=10, value=30)
  o2 = Ins(pos=1, value=oi_val)
  to = tdi(o1, o2)
  assert_op(to, 10 + len(oi_val) , 30)

def test_tii():
  oi1_val = "abcd"
  oi2_val = "1234567"

  o1 = Ins(pos=1, value=oi1_val)
  o1.id= "1"
  o2 = Ins(pos=1, value=oi2_val)
  o2.id= "2"
  to = tii(o1, o2)
  assert_op(to, 1+len(oi2_val), oi1_val)
  to = tii(o2, o1)
  assert_op(to, 1, oi2_val)

  o1 = Ins(pos=1, value=oi1_val)
  o1.id = "2"
  o2 = Ins(pos=1, value=oi2_val)
  o2.id= "1"
  to = tii(o1, o2)
  assert_op(to, 1, oi1_val)

  o1 = Ins(pos=1, value=oi1_val)
  o2 = Ins(pos=10, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 1, oi1_val)

  o1 = Ins(pos=10, value=oi1_val)
  o2 = Ins(pos=1, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 10 + len(oi2_val) , oi1_val)

def test_uuid_case():
  o1 = Ins(0, "hello")
  o1.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d055')
  o2 = Ins(5, "123")
  o3 = Ins(0, "abcd")
  o3.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d054')
  o4 = Ins(0, "test")
  o4.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d056')

  to = transform(o3,o1)
  assert_op(to, len(o1.value), o3.value)
  to = transform(o3,o2)
  assert_op(to, 0, o3.value)

  to = transform(o4,o1)
  assert_op(to, 0, o4.value)
  to = transform(o4,o2)
  assert_op(to, 0, o4.value)
  to = transform(o4,o2)
  assert_op(to, 0, o4.value)



def test_transform():
  oi_val = "hahaha"
  o1 = Ins(pos=1, value=oi_val)
  o2 = Ins(pos=1, value=oi_val)
  o3 = Del(pos=1, value=3)
  assert(tii(o1, o2) == transform(o1, o2))
  assert(tid(o1, o3) == transform(o1, o3))
  assert(tdi(o3, o2) == transform(o3, o2))
  assert(tdd(o3, o3) == transform(o3, o3))