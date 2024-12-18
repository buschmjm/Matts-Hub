from ._anvil_designer import flipCardTemplate
from anvil import *
import anvil.server
import anvil.users

class flipCard(flipCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.faces = []
    self.current_index = 0
    
    # Initialize
    self.nav_panel.visible = False
    
  def add_face(self, component):
    """Add a new face to the card"""
    # Create a container for the component
    container = ColumnPanel()
    container.add_component(component)
    container.visible = False
    
    # Add to our faces list and panel
    self.faces.append(container)
    self.face_panel.add_component(container)
    
    # Show first face and navigation if needed
    if len(self.faces) == 1:
      container.visible = True
    
    self.nav_panel.visible = len(self.faces) > 1
    self.update_nav()
    
  def show_face(self, index):
    """Show the specified face with a fade transition"""
    if 0 <= index < len(self.faces):
      # Hide current face
      if self.current_index < len(self.faces):
        current_face = self.faces[self.current_index]
        current_face.visible = False
      
      # Show new face
      self.current_index = index
      new_face = self.faces[index]
      new_face.visible = True
      
      self.update_nav()
      
  def update_nav(self):
    """Update navigation controls"""
    total = len(self.faces)
    self.page_indicator.text = f"{self.current_index + 1}/{total}" if total > 0 else "0/0"
    self.prev_button.enabled = total > 1 and self.current_index > 0
    self.next_button.enabled = total > 1 and self.current_index < total - 1
    
  def prev_button_click(self, **event_args):
    if self.current_index > 0:
      self.show_face(self.current_index - 1)
      
  def next_button_click(self, **event_args):
    if self.current_index < len(self.faces) - 1:
      self.show_face(self.current_index + 1)
