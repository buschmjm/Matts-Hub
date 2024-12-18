from ._anvil_designer import flipCardTemplate
from anvil import *
import anvil.server
import anvil.users
import time

class flipCard(flipCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.faces = []
    self.current_index = 0
    self.rotation = 0
    
    # Initialize container styles
    self.faces_container.add_event_handler('show', self.setup_styles)
    
  def setup_styles(self, **event_args):
    """Set up the 3D transformation styles"""
    self.faces_container.style.perspective = '1000px'
    self.faces_container.style.transform_style = 'preserve-3d'
    
  def add_face(self, component):
    """Add a new face to the cube"""
    face = Container()
    face.add_component(component)
    face.style.backface_visibility = 'hidden'
    face.style.position = 'absolute'
    face.style.width = '100%'
    face.style.height = '100%'
    
    # Position faces in 3D space
    angle = len(self.faces) * 90
    face.style.transform = f'rotateY({angle}deg) translateZ(150px)'
    
    self.faces.append(face)
    self.faces_container.add_component(face)
    self.update_nav()
    
  def rotate_to_face(self, index):
    """Rotate the cube to show the specified face"""
    if 0 <= index < len(self.faces):
      self.current_index = index
      self.rotation = -index * 90
      
      # Apply rotation animation
      self.faces_container.style.transition = 'transform 0.6s ease'
      self.faces_container.style.transform = f'rotateY({self.rotation}deg)'
      self.update_nav()
      
  def update_nav(self):
    """Update navigation controls"""
    total = len(self.faces)
    self.page_indicator.text = f"{self.current_index + 1}/{total}" if total > 0 else "0/0"
    self.prev_button.enabled = total > 1 and self.current_index > 0
    self.next_button.enabled = total > 1 and self.current_index < total - 1
    
  def prev_button_click(self, **event_args):
    if self.current_index > 0:
      self.rotate_to_face(self.current_index - 1)
      
  def next_button_click(self, **event_args):
    if self.current_index < len(self.faces) - 1:
      self.rotate_to_face(self.current_index + 1)
