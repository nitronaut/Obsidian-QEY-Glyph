"""
QEY Renderer - Visual rendering of QEY glyphs

This module provides rendering capabilities for QEY glyphs using Pillow (PIL).
It can generate static PNG images of glyphs and animated GIFs for Living QEY.
"""

import math
import os
from typing import List, Tuple, Optional, Union
from PIL import Image, ImageDraw, ImageFilter, ImageSequence
import numpy as np

from qey_core import (
    QEYGlyph, QEYClass, PrimitiveElement, LayerType, GlyphForm,
    Primitive, Layer, generate_sample_glyphs
)


# =============================================================================
# RENDERER CLASSES
# =============================================================================

class QEYRenderer:
    """Renders QEY glyphs to images."""
    
    def __init__(
        self,
        size: int = 512,
        background_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
        anti_aliasing: bool = True,
        high_quality: bool = True
    ):
        """
        Initialize the renderer.
        
        Args:
            size: Size of the output image in pixels
            background_color: Background color as RGBA tuple
            anti_aliasing: Whether to use anti-aliasing (slower but smoother)
            high_quality: Whether to use high-quality rendering
        """
        self.size = size
        self.center = size // 2
        self.background_color = background_color
        self.anti_aliasing = anti_aliasing
        self.high_quality = high_quality
        
        # Create a blank image
        self._create_blank_image()
    
    def _create_blank_image(self):
        """Create a blank image with the specified background."""
        if self.background_color[3] == 0:  # Transparent
            self.image = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        else:
            bg = self.background_color[:3] + (255,) if len(self.background_color) == 3 else self.background_color
            self.image = Image.new('RGBA', (self.size, self.size), bg)
        
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
    
    def render_glyph(
        self,
        glyph: QEYGlyph,
        scale: float = 1.0,
        rotation: float = 0.0
    ) -> Image.Image:
        """
        Render a QEY glyph to an image.
        
        Args:
            glyph: The QEY glyph to render
            scale: Scaling factor for the glyph
            rotation: Rotation angle in radians
            
        Returns:
            PIL Image with the rendered glyph
        """
        self.size = glyph.size
        self.center = self.size // 2
        self._create_blank_image()
        
        # Sort layers by their type (render from innermost to outermost)
        layer_order = [
            LayerType.ORIGIN,
            LayerType.IDENTITY_LATTICE,
            LayerType.AUTHORITY_RING,
            LayerType.CAPABILITY_ARRAY,
            LayerType.WITNESS_MARK,
            LayerType.TEMPORAL_RING,
            LayerType.QUANTUM_SEAL
        ]
        
        for layer_type in layer_order:
            if layer_type in glyph.layers:
                layer = glyph.layers[layer_type]
                if layer.active:
                    self._render_layer(layer, glyph, scale, rotation)
        
        # Render composed glyphs if present
        if glyph.composed_glyphs:
            self._render_composed_glyphs(glyph, scale, rotation)
        
        # Apply post-processing if high quality
        if self.high_quality:
            self.image = self._apply_post_processing(self.image)
        
        return self.image
    
    def _render_layer(
        self,
        layer: Layer,
        glyph: QEYGlyph,
        scale: float,
        rotation: float
    ):
        """Render a single layer."""
        for primitive in layer.primitives:
            self._render_primitive(primitive, layer, glyph, scale, rotation)
    
    def _render_primitive(
        self,
        primitive: Primitive,
        layer: Layer,
        glyph: QEYGlyph,
        scale: float,
        rotation: float
    ):
        """Render a single primitive element."""
        # Calculate position and size with scale
        x = primitive.x * self.center * scale
        y = primitive.y * self.center * scale
        
        # Apply layer rotation
        layer_rotation = layer.rotation + rotation
        
        # Apply rotation to position
        if layer_rotation != 0:
            cos_r = math.cos(layer_rotation)
            sin_r = math.sin(layer_rotation)
            x, y = x * cos_r - y * sin_r, x * sin_r + y * cos_r
        
        # Center the coordinates
        x += self.center
        y += self.center
        
        # Get color with alpha based on visibility
        color = self._apply_visibility(primitive.color, layer.visibility)
        
        # Render based on primitive type
        if primitive.element_type == PrimitiveElement.POINT:
            self._render_point(x, y, primitive.radius * self.center * scale, color, primitive.filled)
        elif primitive.element_type == PrimitiveElement.LINE:
            self._render_line(x, y, primitive.angle + layer_rotation, primitive.length * self.center * scale, primitive.width * self.center * scale, color)
        elif primitive.element_type == PrimitiveElement.ARC:
            self._render_arc(x, y, primitive.radius * self.center * scale, primitive.angle + layer_rotation, primitive.length, primitive.width * self.center * scale, color)
        elif primitive.element_type == PrimitiveElement.RING:
            self._render_ring(x, y, primitive.radius * self.center * scale, primitive.width * self.center * scale, color)
        elif primitive.element_type == PrimitiveElement.FRACTURE:
            self._render_fracture(x, y, primitive.radius * self.center * scale, primitive.angle + layer_rotation, primitive.length, primitive.width * self.center * scale, color)
        elif primitive.element_type == PrimitiveElement.JUNCTION:
            self._render_junction(x, y, primitive.radius * self.center * scale, color)
        elif primitive.element_type == PrimitiveElement.PULSE:
            self._render_pulse(x, y, primitive.radius * self.center * scale, primitive.angle + layer_rotation, primitive.length * self.center * scale, primitive.width * self.center * scale, color, glyph)
    
    def _apply_visibility(self, color: Tuple[int, int, int, int], visibility: float) -> Tuple[int, int, int, int]:
        """Apply visibility to color alpha channel."""
        if len(color) == 4:
            r, g, b, a = color
            new_a = int(a * visibility)
            return (r, g, b, new_a)
        else:
            r, g, b = color
            new_a = int(255 * visibility)
            return (r, g, b, new_a)
    
    def _render_point(self, x: float, y: float, radius: float, color: Tuple[int, int, int, int], filled: bool):
        """Render a point (circle)."""
        if radius <= 0:
            return
        
        bbox = [x - radius, y - radius, x + radius, y + radius]
        if filled:
            self.draw.ellipse(bbox, fill=color)
        else:
            self.draw.ellipse(bbox, outline=color)
    
    def _render_line(self, x: float, y: float, angle: float, length: float, width: float, color: Tuple[int, int, int, int]):
        """Render a line."""
        if length <= 0 or width <= 0:
            return
        
        x2 = x + math.cos(angle) * length
        y2 = y + math.sin(angle) * length
        
        self.draw.line([(x, y), (x2, y2)], fill=color, width=int(width))
    
    def _render_arc(self, x: float, y: float, radius: float, start_angle: float, end_angle: float, width: float, color: Tuple[int, int, int, int]):
        """Render an arc."""
        if radius <= 0 or width <= 0:
            return
        
        # Convert angles to degrees for PIL
        start_deg = math.degrees(start_angle)
        end_deg = math.degrees(start_angle + end_angle)
        
        bbox = [x - radius, y - radius, x + radius, y + radius]
        self.draw.arc(bbox, start_deg, end_deg, fill=color, width=int(width))
    
    def _render_ring(self, x: float, y: float, radius: float, width: float, color: Tuple[int, int, int, int]):
        """Render a ring (circle)."""
        if radius <= 0 or width <= 0:
            return
        
        inner_radius = radius - width / 2
        outer_radius = radius + width / 2
        
        inner_bbox = [x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius]
        outer_bbox = [x - outer_radius, y - outer_radius, x + outer_radius, y + outer_radius]
        
        # Draw outer circle
        self.draw.ellipse(outer_bbox, outline=color, width=int(width))
        
        # For filled rings, we need to draw both circles
        # But PIL doesn't support filled rings directly, so we use outline
    
    def _render_fracture(self, x: float, y: float, radius: float, angle: float, length: float, width: float, color: Tuple[int, int, int, int]):
        """Render a fracture (broken line or interrupted ring)."""
        if radius <= 0 or width <= 0:
            return
        
        # Render as a partial arc with a gap
        start_deg = math.degrees(angle)
        end_deg = math.degrees(angle + length * 0.8)  # Only 80% of the length
        
        bbox = [x - radius, y - radius, x + radius, y + radius]
        self.draw.arc(bbox, start_deg, end_deg, fill=color, width=int(width))
    
    def _render_junction(self, x: float, y: float, radius: float, color: Tuple[int, int, int, int]):
        """Render a junction (intersection point)."""
        if radius <= 0:
            return
        
        # Draw as a small cross
        self.draw.line([(x - radius, y), (x + radius, y)], fill=color, width=int(radius / 2))
        self.draw.line([(x, y - radius), (x, y + radius)], fill=color, width=int(radius / 2))
        
        # Also draw a small circle in the center
        self.draw.ellipse([x - radius/2, y - radius/2, x + radius/2, y + radius/2], fill=color)
    
    def _render_pulse(self, x: float, y: float, radius: float, angle: float, length: float, width: float, color: Tuple[int, int, int, int], glyph: QEYGlyph):
        """Render a pulse (repeated marks or animated segments)."""
        if radius <= 0 or width <= 0:
            return
        
        # For static glyphs, render as small lines
        if glyph.form == GlyphForm.STATIC:
            # Render 3 small lines in a radial pattern
            for i in range(3):
                pulse_angle = angle + i * (2 * math.pi / 3)
                x1 = x + math.cos(pulse_angle) * radius
                y1 = y + math.sin(pulse_angle) * radius
                x2 = x + math.cos(pulse_angle) * (radius + length)
                y2 = y + math.sin(pulse_angle) * (radius + length)
                self.draw.line([(x1, y1), (x2, y2)], fill=color, width=int(width))
        else:
            # For living glyphs, render based on authentication phase
            phase = glyph.authentication_phase
            num_pulses = 4
            for i in range(num_pulses):
                pulse_angle = angle + i * (2 * math.pi / num_pulses)
                # Animate the pulse based on phase
                pulse_length = length * (0.5 + 0.5 * math.sin(phase * 2 * math.pi + i * math.pi / 2))
                
                x1 = x + math.cos(pulse_angle) * radius
                y1 = y + math.sin(pulse_angle) * radius
                x2 = x + math.cos(pulse_angle) * (radius + pulse_length)
                y2 = y + math.sin(pulse_angle) * (radius + pulse_length)
                
                alpha = color[3] if len(color) > 3 else 255
                animated_color = (color[0], color[1], color[2], int(alpha * (0.5 + 0.5 * phase)))
                self.draw.line([(x1, y1), (x2, y2)], fill=animated_color, width=int(width))
    
    def _render_composed_glyphs(self, glyph: QEYGlyph, scale: float, rotation: float):
        """Render composed glyphs around the main glyph."""
        if not glyph.composed_glyphs:
            return
        
        num_composed = len(glyph.composed_glyphs)
        for i, composed_glyph in enumerate(glyph.composed_glyphs):
            angle = i * (2 * math.pi / num_composed)
            
            # Create a temporary renderer for the composed glyph
            temp_renderer = QEYRenderer(
                size=int(glyph.size * 0.4),
                background_color=(0, 0, 0, 0)
            )
            
            # Render the composed glyph
            composed_image = temp_renderer.render_glyph(composed_glyph, scale=0.8)
            
            # Calculate position
            distance = glyph.size * 0.45 * scale
            x = self.center + math.cos(angle) * distance - composed_image.width // 2
            y = self.center + math.sin(angle) * distance - composed_image.height // 2
            
            # Paste the composed glyph
            self.image.paste(composed_image, (int(x), int(y)), composed_image)
            
            # Draw a connection line
            center_x = self.center
            center_y = self.center
            line_x = self.center + math.cos(angle) * distance * 0.7
            line_y = self.center + math.sin(angle) * distance * 0.7
            
            self.draw.line([(center_x, center_y), (line_x, line_y)], fill=(200, 200, 0, 255), width=2)
    
    def _apply_post_processing(self, image: Image.Image) -> Image.Image:
        """Apply post-processing effects for better visual quality."""
        # Apply slight blur for anti-aliasing effect
        if self.anti_aliasing:
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Apply slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def render_to_file(
        self,
        glyph: QEYGlyph,
        filename: str,
        format: str = 'PNG',
        scale: float = 1.0,
        rotation: float = 0.0,
        quality: int = 95
    ):
        """
        Render a glyph to a file.
        
        Args:
            glyph: The QEY glyph to render
            filename: Output filename
            format: Image format (PNG, JPEG, etc.)
            scale: Scaling factor
            rotation: Rotation angle in radians
            quality: Quality for JPEG (1-100)
        """
        image = self.render_glyph(glyph, scale, rotation)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        if format.upper() == 'JPEG':
            # Convert to RGB for JPEG
            rgb_image = image.convert('RGB')
            rgb_image.save(filename, format='JPEG', quality=quality)
        else:
            image.save(filename, format=format, quality=quality)
        
        return image


class QEYAnimator:
    """Creates animated GIFs of Living QEY glyphs."""
    
    def __init__(
        self,
        size: int = 512,
        fps: int = 30,
        duration: float = 3.0,
        background_color: Tuple[int, int, int, int] = (0, 0, 0, 0)
    ):
        """
        Initialize the animator.
        
        Args:
            size: Size of the animation in pixels
            fps: Frames per second
            duration: Duration of the animation in seconds
            background_color: Background color as RGBA tuple
        """
        self.size = size
        self.fps = fps
        self.duration = duration
        self.background_color = background_color
        self.frames = []
    
    def create_authentication_animation(
        self,
        glyph: QEYGlyph,
        filename: str,
        num_frames: int = 60
    ):
        """
        Create an animation of a glyph going through authentication.
        
        Args:
            glyph: The QEY glyph to animate
            filename: Output filename for the GIF
            num_frames: Number of frames in the animation
        """
        # Make sure it's a living glyph
        glyph.form = GlyphForm.LIVING
        
        frames = []
        
        for frame_idx in range(num_frames):
            # Calculate phase (0 to 1)
            phase = frame_idx / (num_frames - 1)
            
            # Update glyph state
            glyph.authentication_phase = phase
            glyph.is_authenticated = phase > 0.7
            
            # Create renderer
            renderer = QEYRenderer(
                size=self.size,
                background_color=self.background_color
            )
            
            # Render frame
            frame = renderer.render_glyph(glyph, scale=1.0, rotation=phase * 2 * math.pi)
            frames.append(frame)
        
        # Save as GIF
        self._save_gif(frames, filename)
        
        return frames
    
    def create_pulse_animation(
        self,
        glyph: QEYGlyph,
        filename: str,
        num_frames: int = 60
    ):
        """
        Create an animation with pulsing effects.
        
        Args:
            glyph: The QEY glyph to animate
            filename: Output filename for the GIF
            num_frames: Number of frames in the animation
        """
        glyph.form = GlyphForm.LIVING
        
        frames = []
        
        for frame_idx in range(num_frames):
            phase = frame_idx / (num_frames - 1)
            
            # Create a copy of the glyph to modify
            import copy
            frame_glyph = copy.deepcopy(glyph)
            frame_glyph.authentication_phase = phase
            
            # Animate the temporal ring rotation
            frame_glyph.get_layer(LayerType.TEMPORAL_RING).rotation = phase * 2 * math.pi
            
            # Animate the quantum seal
            frame_glyph.get_layer(LayerType.QUANTUM_SEAL).rotation = -phase * math.pi
            
            # Render frame
            renderer = QEYRenderer(
                size=self.size,
                background_color=self.background_color
            )
            frame = renderer.render_glyph(frame_glyph, scale=1.0)
            frames.append(frame)
        
        self._save_gif(frames, filename)
        
        return frames
    
    def _save_gif(self, frames: List[Image.Image], filename: str):
        """Save frames as an animated GIF."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        # Save the first frame
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // self.fps,  # Duration per frame in milliseconds
            loop=0  # Loop forever
        )


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def render_all_sample_glyphs(output_dir: str = 'output'):
    """Render all sample glyphs to files."""
    os.makedirs(output_dir, exist_ok=True)
    
    generator = QEYGenerator(seed=42)
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    
    # Generate sample glyphs
    glyphs = generate_sample_glyphs()
    
    class_names = {
        QEYClass.HUMAN: 'Human',
        QEYClass.SUPERAGENT: 'Superagent',
        QEYClass.MACHINE: 'Machine',
        QEYClass.NODE: 'Node',
        QEYClass.BLOODLINE: 'Bloodline',
        QEYClass.SOVEREIGN: 'Sovereign',
        QEYClass.GHOST: 'Ghost',
        QEYClass.NULL: 'Null',
        QEYClass.COLLECTIVE: 'Collective'
    }
    
    for i, glyph in enumerate(glyphs):
        class_name = class_names.get(glyph.qey_class, glyph.qey_class.name)
        form_name = 'Living' if glyph.form == GlyphForm.LIVING else 'Static'
        
        filename = os.path.join(output_dir, f'qey_{class_name}_{form_name}.png')
        renderer.render_to_file(glyph, filename, format='PNG')
        print(f"Rendered: {filename}")
    
    # Create a composite glyph
    human = glyphs[0]
    superagent = glyphs[1]
    composite = generator.generate_composite_glyph(
        [human, superagent],
        operator="INHERITANCE"
    )
    
    filename = os.path.join(output_dir, 'qey_composite_inheritance.png')
    renderer.render_to_file(composite, filename, format='PNG')
    print(f"Rendered: {filename}")
    
    # Create an authentication animation
    animator = QEYAnimator(size=512, fps=30, duration=3.0)
    auth_glyph = generator.generate_glyph(
        identity_data="auth_test",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.CONTRACTUAL,
        form=GlyphForm.LIVING
    )
    
    filename = os.path.join(output_dir, 'qey_authentication_animation.gif')
    animator.create_authentication_animation(auth_glyph, filename, num_frames=60)
    print(f"Rendered: {filename}")
    
    # Create a pulse animation
    filename = os.path.join(output_dir, 'qey_pulse_animation.gif')
    animator.create_pulse_animation(auth_glyph, filename, num_frames=60)
    print(f"Rendered: {filename}")


if __name__ == "__main__":
    print("Testing QEY Renderer...")
    
    # Create a simple glyph
    generator = QEYGenerator(seed=42)
    glyph = generator.generate_glyph(
        identity_data="test_identity",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.PERSONAL
    )
    
    # Render it
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    image = renderer.render_glyph(glyph)
    
    print(f"Rendered glyph to image: {image.size}")
    
    # Save to file
    renderer.render_to_file(glyph, 'test_qey.png', format='PNG')
    print("Saved to test_qey.png")
    
    # Render all sample glyphs
    render_all_sample_glyphs()
    print("All sample glyphs rendered!")
