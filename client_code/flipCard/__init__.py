from ._anvil_designer import flipCardTemplate
from anvil import *
import anvil.server
import anvil.users

class flipCard(flipCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.faces = []
    self.current_index = 0
    self.action_map = {}  # Maps components to next face index
    
    # Initialize navigation
    self.nav_panel.visible = True
    self.setup_faces()
    
  def setup_faces(self):
    """Get all immediate children of content_panel as faces"""
    self.faces = [c for c in self.content_panel.get_components()]
    
    # Hide all faces except first
    for i, face in enumerate(self.faces):
      face.visible = (i == 0)
    
    self.update_nav()
    
  def link_action(self, component, next_face_index):
    """Link a component's click event to show a specific face"""
    self.action_map[component] = next_face_index
    component.set_event_handler('click', self._handle_action_click)
    
  def _handle_action_click(self, sender, **event_args):
    """Handle clicks on linked components"""
    if sender in self.action_map:
      next_index = self.action_map[sender]
      self.show_face(next_index)
      
  def show_face(self, index):
    """Show the specified face with a transition"""
    if 0 <= index < len(self.faces):
      # Hide current face
      self.faces[self.current_index].visible = False
      
      # Show new face
      self.faces[index].visible = True
      self.current_index = index
      
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
