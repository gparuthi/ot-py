from system import Client, Message, Server
from ot import Del, Ins
from uuid import uuid1 as uuid, UUID


def test_send():
  s = Server()
  s.apply(Ins(0, "hello"))
  c = Client("A", s)
  assert(c.text=="hello")
  o2 = Ins(5, "123")
  c.add(o2)
  assert(len(c.buffer)==1)
  c.send()
  assert(c.awaited_op.id == o2.id)
  assert(c.awaited_op.id != s.messages[0].op.id)


def test_receive_from_server():
  s = Server()
  o0 = Ins(0, "hello")
  s.apply(o0)

  bob = Client("bob", s)
  bob.receive_from_server()
  assert(bob.version == 1)
  assert(bob.text == s.latest_version)

def test_sync():
  s = Server()
  o0 = Ins(0, "hello")
  s.apply(o0)

  alice = Client("alice", s)
  o1 = Ins(0, "abcd")
  alice.apply(o1)
  alice.add(o1)

  bob = Client("bob", s)
  o2 = Ins(0, "1234")
  bob.apply(o2)
  bob.add(o2)
  assert(bob.text == f"{o2.value}{o0.value}")

  assert(len(s.messages) == 1)
  assert(alice.version == 1)
  alice.send()
  assert(s.version == 2)
  assert(alice.version == 1)
  assert(alice.awaited_op.id == s.messages[-1].op.id)

  assert(bob.version == 1)
  assert(len(bob.buffer) == 1)
  bob.send()
  assert(len(bob.buffer) == 0)
  assert(s.version == 3)
  assert(bob.awaited_op == o2)
  assert(bob.version == 1)
  assert(bob.awaited_op.id == s.messages[-1].op.id)
  assert(bob.awaited_op.id != s.messages[1].op.id) 
  bob.receive_from_server()
  assert(bob.version == 3)
  assert(bob.text == s.latest_version)
  
  











