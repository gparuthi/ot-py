from dataclasses import dataclass
from typing import List
from ot import Ins, Del, Operation, transform

@dataclass
class Message:
  version: int
  op: Operation

def apply(text: str, op: Operation):
  if type(op) == Ins:
    text = f"{text[:op.pos]}{op.value}{text[op.pos:]}"
  if type(op) == Del:
    text = text[:op.pos] + text[op.pos+op.value:]
  return text

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
    latest = apply(self.latest_version, op)
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

class Client:
  def __init__(self, name: str, server: Server) -> None:
    self.name = name
    self.text = server.latest_version
    self.buffer: List[Operation] = []
    self.server: Server = server
    self.version = self.server.version
    self.awaited_op = None

  def apply(self, op: Operation):
    latest = self.text
    self.text = apply(latest, op)

  def queue_mesage_to_send(self):
    if not self.awaited_op and len(self.buffer) > 0: 
      self.awaited_op = self.buffer[0]

  def add(self, op: Operation):
    self.buffer.append(op)
    self.queue_mesage_to_send()

  def send(self):
    if self.awaited_op:
      self.server.process_message(
        Message(version=self.version, op=self.awaited_op)
        )
      self.queue_mesage_to_send()
    else:
      print('Nothing to send')
  
  def receive_from_server(self):
    cur_ver = self.version
    # get messages to receive from server
    server_messages = self.server.messages[cur_ver:]
    server_text = self.server.latest_version

    if len(server_messages)>0:
      self.version = server_messages[-1].version + 1

      if len(self.buffer)>0:
        # check for awaited message in server messages
        idx = 0
        while idx < len(server_messages):
          m = server_messages[idx]
          if self.awaited_op.id and self.awaited_op.id == m.op.id:
            # pop and queue next
            self.awaited_op = None
            self.buffer.pop(0)
            server_messages.remove(m)
            self.queue_mesage_to_send()
          idx += 1
            
        # apply transformation to each in the buffer
        for buffer_op in list(self.buffer):
          for m in list(server_messages):
            nbm = transform(buffer_op, m.op)
            buffer_op.pos = nbm.pos
        
        # apply messages
        self.text = server_text
        for buffer_op in self.buffer:
          self.text = apply(self.text, buffer_op)
      else:
        self.text = server_text  
      
      