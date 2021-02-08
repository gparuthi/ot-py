from dataclasses import dataclass
from typing import List, Union
from ot import Ins, Del, Operation, transform

@dataclass
class Message:
  version: int
  op: Operation

class Server:
  versions: List[str] = [""]
  messages: List[Message] = []

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
  name: str
  buffer: List[Operation]
  awaited_op: Operation = None
  server = Server

  def add(self, op: Operation):
    self.buffer.append(op)
  
  # def send(self):
    # self.awaited_op = 