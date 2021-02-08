from ot import _OperationBase, Ins, Del, tii, tid, tdi, tdd

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

  o1 = Ins(id="2", pos=1, value=oi1_val)
  o2 = Ins(id="1", pos=1, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 1, oi1_val)

  o1 = Ins(id="1", pos=1, value=oi1_val)
  o2 = Ins(id="2", pos=1, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 1+len(oi2_val), oi1_val)

  o1 = Ins(pos=1, value=oi1_val)
  o2 = Ins(pos=10, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 1, oi1_val)

  o1 = Ins(pos=10, value=oi1_val)
  o2 = Ins(pos=1, value=oi2_val)
  to = tii(o1, o2)
  assert_op(to, 10 + len(oi2_val) , oi1_val)
