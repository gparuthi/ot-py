from system import Message, Server
from ot import Del, Ins
from uuid import uuid1 as uuid, UUID

def test_apply():
  s = Server()
  o = Ins(0, "hello123")
  s.apply(o)
  assert(s.latest_version == "hello123")
  assert(s.messages[0].op == o)
  assert(s.messages[0].version == 0)

  s.apply(Del(0, 3))
  assert(s.latest_version == "lo123")

def test_process_message():
  s = Server()

  o1 = Ins(0, "hello")
  o1.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d055')
  o2 = Ins(5, "123")
  o3 = Ins(0, "abcd")
  o3.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d054')
  o4 = Ins(0, "test")
  o4.id = UUID('d1ee0884-69bb-11eb-9096-dca90482d056')
  
  s.apply(o1)
  s.apply(o2)
  assert(s.latest_version == "hello123")

  m = Message(0, o3)
  s.process_message(m)
  assert(s.latest_version == "helloabcd123")
  assert(len(s.messages) == 3)
  assert(s.version == 3)
  s.messages[-1].op.id == m.op.id

  m = Message(0, o4)
  s.process_message(m)
  assert(s.latest_version == "testhelloabcd123")
  assert(len(s.messages) == 4)
  assert(s.version == 4)


  