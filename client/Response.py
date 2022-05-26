class Response:
  def __init__(self, toDeliver: bool, body: str):
    self.toDeliver = toDeliver
    self.body = body