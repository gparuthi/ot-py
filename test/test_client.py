from system import Client, Message, Server
from ot import Del, Ins, Operation
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
  assert(bob.awaited_op == o2)
  assert(s.version == 3)
  assert(bob.awaited_op == o2)
  assert(bob.version == 1)
  assert(bob.awaited_op.id == s.messages[-1].op.id)
  assert(bob.awaited_op.id != s.messages[1].op.id) 
  bob.receive_from_server()
  assert(bob.version == 3)
  assert(bob.text == s.latest_version)

  alice.receive_from_server()
  assert(alice.version == s.version)
  assert(alice.text == s.latest_version)
  
  
def test_del_scenario():
  def _apply_and_add(cl: Client, op: Operation):
    cl.apply(op)
    cl.add(op)

  s = Server()
  o0 = Ins(0, "aaaa")
  s.apply(o0)
  alice = Client("alice", s)
  bob = Client("bob", s)

  o = Ins(0, "bbbb")
  _apply_and_add(alice, o)
  assert(alice.text == "bbbbaaaa")
  o = Del(3, 3)
  _apply_and_add(alice, o)
  assert(alice.text == "bbbaa")
  o = Ins(0, "cccc")
  _apply_and_add(alice, o)
  assert(alice.text == "ccccbbbaa")
  alice.send()
  alice.receive_from_server()
  assert(alice.text == "ccccbbbaa")
  alice.send()
  alice.receive_from_server()
  assert(alice.text == "ccccbbbaa")
  alice.send()
  alice.receive_from_server()
  assert(alice.text == "ccccbbbaa")
  assert(alice.text == s.latest_version)

  o = Ins(0, "1234")
  _apply_and_add(bob, o)
  assert(bob.text == "1234aaaa")
  bob.receive_from_server()
  bob.send()
  assert(s.latest_version == "1234ccccbbbaa")
  alice.receive_from_server() 
  bob.receive_from_server()
  assert(bob.text == s.latest_version)
  assert(bob.text == alice.text)
  
  

  
  








