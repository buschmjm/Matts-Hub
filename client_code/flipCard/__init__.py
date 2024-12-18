from ._anvil_designer import flipCardTemplate
from anvil import *
import anvil.server
import anvil.users

class flipCard(flipCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_index = 0
    
    # Initialize after a brief delay to allow components to be added
    anvil.js.call_js('setTimeout', self.setup_faces, 100)
    
  def setup_faces(self):
    """Get all immediate children of card_content as faces"""
    self.faces = [c for c in self.card_content.get_components()]
    
    # Hide all faces except first
    for i, face in enumerate(self.faces):
      face.visible = (i == 0)
    
    # Show/hide navigation based on number of faces
    self.nav_panel.visible = len(self.faces) > 1
    self.update_nav()
    
  def show_face(self, index):
    """Show the specified face with a transition"""
    if 0 <= index < len(self.faces):
      # Hide current face
      if self.current_index < len(self.faces):
        self.faces[self.current_index].visible = False
      
      # Show new face
      self.current_index = index
      self.faces[index].visible = True
      
      # Update navigation
      self.update_nav()
  
  def update_nav(self):
    """Update navigation buttons"""
    self.prev_button.enabled = self.current_index > 0
    self.next_button.enabled = self.current_index < len(self.faces) - 1
  
  def prev_button_click(self, **event_args):
    if self.current_index > 0:
      self.show_face(self.current_index - 1)
      
  def next_button_click(self, **event_args):
    if self.current_index < len(self.faces) - 1:
      self.show_face(self.current_index + 1)
      
  def get_current_face(self):
    """Return the currently visible face"""
    if 0 <= self.current_index < len(self.faces):
      return self.faces[self.current_index]
    return None
