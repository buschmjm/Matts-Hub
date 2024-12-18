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
    container = ColumnPanel(spacing_above="none", spacing_below="none")
    container.add_component(component)
    container.visible = False
    
    # Add to our faces list and panel
    self.faces.append(container)
    self.faces_container.add_component(container)
    
    # Show first face and navigation if needed
    if len(self.faces) == 1:
      container.visible = True
    
    self.nav_panel.visible = len(self.faces) > 1
    self.update_nav()
    
  def show_face(self, index):
    """Show the specified face with a transition"""
    if 0 <= index < len(self.faces):
      # Setup transition
      old_face = self.faces[self.current_index]
      new_face = self.faces[index]
      
      # Update navigation state
      self.current_index = index
      self.update_nav()
      
      # Perform transition
      old_face.visible = False
      new_face.visible = True
      
      # Add transition effect
      if index > self.current_index:
        new_face.add_event_handler('show', self.animate_slide_left)
      else:
        new_face.add_event_handler('show', self.animate_slide_right)
        
  def animate_slide_left(self, **event_args):
    """Animate slide from right to left"""
    component = event_args['sender']
    component.opacity = 0
    component.style.transform = 'translateX(100%)'
    
    def animation():
      component.opacity = 1
      component.style.transform = 'translateX(0)'
      component.style.transition = 'all 0.3s ease-out'
    
    # Schedule animation
    anvil.js.call_js('setTimeout', animation, 50)
    
  def animate_slide_right(self, **event_args):
    """Animate slide from left to right"""
    component = event_args['sender']
    component.opacity = 0
    component.style.transform = 'translateX(-100%)'
    
    def animation():
      component.opacity = 1
      component.style.transform = 'translateX(0)'
      component.style.transition = 'all 0.3s ease-out'
    
    # Schedule animation
    anvil.js.call_js('setTimeout', animation, 50)
    
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
