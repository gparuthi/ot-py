from dataclasses import dataclass
from typing import List
from ot import Ins, Del, Operation, transform

@dataclass
class Message:
  version: int
  op: Operation


class Server:
  def __init__(self) -> None:
    self.versions: List[str] = [""]
    self.messages: List[Message] = []
    self.clients: List[Client] = []

  @property
  def version(self):
    return len(self.versions)-1

  @property
  def latest_version(self):
    return self.versions[self.version]

  def apply(self, op: Operation):
    latest = self.latest_version
    if type(op) == Ins:
      latest = f"{latest[:op.pos]}{op.value}{latest[op.pos:]}"
    if type(op) == Del:
      latest = latest[:op.pos] + latest[op.pos+op.value:]

    self.versions.append(latest)
    self.messages.append(Message(version=self.version-1, op=op))

  def process_message(self, new: Message):
    # find messages to tranform with
    against = [m for m in self.messages if m.version>=new.version]

    fin = new.op
    for m in against:
      fin = transform(fin, m.op)  

    fin.id = new.op.id
    self.apply(fin)

  def __repr__(self) -> str:
      return f"Server v({self.version})={self.latest_version}"

server = Server()

class Client:
  def __init__(self, name: str, server: Server) -> None:
    self.name = name
    self.text = server.latest_version
    self.buffer: List[Operation] = []
    self.awaited_op: Operation = None
    self.server: Server = server
    self.version = self.server.version

  def apply(self, op: Operation):
    latest = self.text
    if type(op) == Ins:
      self.text = f"{latest[:op.pos]}{op.value}{latest[op.pos:]}"
    if type(op) == Del:
      self.text = latest[:op.pos] + latest[op.pos+op.value:]

  def add(self, op: Operation):
    self.buffer.append(op)
  
  def send(self):
    op = self.buffer.pop()
    self.server.process_message(
      Message(version=self.version, op=op)
      )
    self.awaited_op = op
  
  def receive_from_server(self):
    def transform_both_ways(o1, o2):
      f1, f2 = transform(o1, o2), transform(o2, o1)
      f1.id = o1.id
      f2.id = o2.id
      return f1, f2

    cur_ver = self.version
    server_messages = self.server.messages[cur_ver:]
    for m in server_messages:
      # ack the awaiting message
      if self.awaited_op and self.awaited_op.id == m.op.id:
        self.awaited_op = None
      else:
        fin, self.awaited_op = transform_both_ways(m.op, self.awaited_op)
        self.apply(fin)
        # OT the message with whats in awaited and the buffer
        for bo in self.buffer:
          bo2 = transform(bo, m.op)
          bo.pos = bo2.pos
      self.version = m.version + 1


    