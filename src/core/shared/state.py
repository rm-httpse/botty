from dataclasses import dataclass
from PIL import Image
from src.utils.converter import image_to_base64

@dataclass
class BotState:
  screen: Image.Image | None
  task: dict
  status: str
  
  def to_dict(self):
    return {
      "screen": image_to_base64(self.screen) if self.screen else None,
      "task": self.task,
      "status": self.status
    }