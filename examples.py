#!/usr/bin/env python3
"""
QEY Glyph Generator - Examples

This script demonstrates various features of the QEY glyph generation system.
Run with: python examples.py
"""

import os
import json
from qey_core import (
    QEYGenerator, QEYClass, AuthorityType, Capability, GlyphForm,
    generate_sample_glyphs, QEYGlyph
)
from qey_renderer import QEYRenderer, QEYAnimator


def setup_output_directory():
    """Create output directory for examples."""
    output_dir = 'examples_output'
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def example_1_simple_glyph():
    """Example 1: Generate a simple human glyph."""
    print("\n" + "="*60)
    print("Example 1: Simple Human Glyph")
    print("="*60)
    
    generator = QEYGenerator(seed=42)
    glyph = generator.generate_glyph(
        identity_data="john_doe",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.PERSONAL
    )
    
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    renderer.render_to_file(glyph, os.path.join(output_dir, "example1_simple_human.png"))
    
    print(f"Generated: {os.path.join(output_dir, 'example1_simple_human.png')}")
    print(f"  Identity Hash: {glyph.identity_hash}")
    print(f"  Class: {glyph.qey_class.name}")
    print(f"  Authority: {glyph.authority_type.name}")


def example_2_superagent_glyph():
    """Example 2: Generate a Superagent glyph with capabilities."""
    print("\n" + "="*60)
    print("Example 2: Superagent Glyph with Capabilities")
    print("="*60)
    
    generator = QEYGenerator(seed=123)
    glyph = generator.generate_glyph(
        identity_data="lycos_superagent",
        qey_class=QEYClass.SUPERAGENT,
        authority_type=AuthorityType.SOVEREIGN,
        capabilities=[
            Capability.EXECUTE_CONTRACTS,
            Capability.OPERATE_MACHINERY,
            Capability.ACCESS_INFORMATION,
            Capability.CONTROL_SERVOBOT
        ]
    )
    
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    renderer.render_to_file(glyph, os.path.join(output_dir, "example2_superagent.png"))
    
    print(f"Generated: {os.path.join(output_dir, 'example2_superagent.png')}")
    print(f"  Capabilities: {', '.join(c.name for c in glyph.capabilities)}")


def example_3_all_classes():
    """Example 3: Generate glyphs for all QEY classes."""
    print("\n" + "="*60)
    print("Example 3: All QEY Classes")
    print("="*60)
    
    generator = QEYGenerator(seed=456)
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    
    for qey_class in QEYClass:
        glyph = generator.generate_glyph(
            identity_data=f"{qey_class.name.lower()}_example",
            qey_class=qey_class,
            authority_type=AuthorityType.PERSONAL
        )
        
        filename = os.path.join(output_dir, f"example3_{qey_class.name.lower()}.png")
        renderer.render_to_file(glyph, filename)
        print(f"  Generated: {filename}")


def example_4_all_authorities():
    """Example 4: Generate glyphs with different authority types."""
    print("\n" + "="*60)
    print("Example 4: Different Authority Types")
    print("="*60)
    
    generator = QEYGenerator(seed=789)
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    
    for authority in AuthorityType:
        glyph = generator.generate_glyph(
            identity_data=f"authority_{authority.name.lower()}",
            qey_class=QEYClass.HUMAN,
            authority_type=authority
        )
        
        filename = os.path.join(output_dir, f"example4_{authority.name.lower()}.png")
        renderer.render_to_file(glyph, filename)
        print(f"  Generated: {filename}")


def example_5_composite_glyph():
    """Example 5: Create a composite glyph (inheritance relationship)."""
    print("\n" + "="*60)
    print("Example 5: Composite Glyph (Inheritance)")
    print("="*60)
    
    generator = QEYGenerator(seed=101112)
    
    # Create parent glyph (Bloodline)
    parent = generator.generate_glyph(
        identity_data="fiel_ancestor",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.INHERITED
    )
    
    # Create child glyph (Inherited)
    child = generator.generate_glyph(
        identity_data="mateus_fiel",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.INHERITED,
        capabilities=[Capability.ACCESS_SUPERAGENT, Capability.EXECUTE_CONTRACTS]
    )
    
    # Create composite glyph
    composite = generator.generate_composite_glyph(
        [parent, child],
        operator="INHERITANCE"
    )
    
    renderer = QEYRenderer(size=768, background_color=(0, 0, 0, 255))
    renderer.render_to_file(composite, os.path.join(output_dir, "example5_inheritance_composite.png"))
    
    print(f"Generated: {os.path.join(output_dir, 'example5_inheritance_composite.png')}")
    print(f"  Composite of: {parent.identity_hash}, {child.identity_hash}")
    print(f"  Operator: INHERITANCE")


def example_6_living_glyph():
    """Example 6: Create a Living QEY glyph."""
    print("\n" + "="*60)
    print("Example 6: Living QEY Glyph")
    print("="*60)
    
    generator = QEYGenerator(seed=131415)
    glyph = generator.generate_glyph(
        identity_data="living_example",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.CONTRACTUAL,
        form=GlyphForm.LIVING
    )
    
    # Set authentication state
    glyph.is_authenticated = True
    glyph.authentication_phase = 1.0
    
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    renderer.render_to_file(glyph, os.path.join(output_dir, "example6_living_glyph.png"))
    
    print(f"Generated: {os.path.join(output_dir, 'example6_living_glyph.png')}")
    print(f"  Form: {glyph.form.name}")
    print(f"  Authenticated: {glyph.is_authenticated}")


def example_7_authentication_animation():
    """Example 7: Create an authentication animation."""
    print("\n" + "="*60)
    print("Example 7: Authentication Animation")
    print("="*60)
    
    generator = QEYGenerator(seed=161718)
    glyph = generator.generate_glyph(
        identity_data="auth_animation",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.CONTRACTUAL,
        form=GlyphForm.LIVING
    )
    
    animator = QEYAnimator(size=512, fps=30, duration=3.0)
    animator.create_authentication_animation(
        glyph,
        os.path.join(output_dir, "example7_authentication_animation.gif"),
        num_frames=60
    )
    
    print(f"Generated: {os.path.join(output_dir, 'example7_authentication_animation.gif')}")
    print(f"  Frames: 60")
    print(f"  FPS: 30")


def example_8_pulse_animation():
    """Example 8: Create a pulse animation."""
    print("\n" + "="*60)
    print("Example 8: Pulse Animation")
    print("="*60)
    
    generator = QEYGenerator(seed=192021)
    glyph = generator.generate_glyph(
        identity_data="pulse_animation",
        qey_class=QEYClass.SUPERAGENT,
        authority_type=AuthorityType.INSTITUTIONAL,
        form=GlyphForm.LIVING,
        capabilities=[Capability.EXECUTE_CONTRACTS, Capability.OPERATE_MACHINERY]
    )
    
    animator = QEYAnimator(size=512, fps=30, duration=3.0)
    animator.create_pulse_animation(
        glyph,
        os.path.join(output_dir, "example8_pulse_animation.gif"),
        num_frames=60
    )
    
    print(f"Generated: {os.path.join(output_dir, 'example8_pulse_animation.gif')}")
    print(f"  Frames: 60")
    print(f"  FPS: 30")


def example_9_json_export_import():
    """Example 9: Export and import glyphs as JSON."""
    print("\n" + "="*60)
    print("Example 9: JSON Export and Import")
    print("="*60)
    
    generator = QEYGenerator(seed=222324)
    
    # Create and export a glyph
    original_glyph = generator.generate_glyph(
        identity_data="json_example",
        qey_class=QEYClass.MACHINE,
        authority_type=AuthorityType.DELEGATED,
        capabilities=[Capability.OPERATE_MACHINERY, Capability.ADMINISTER_NODE]
    )
    
    json_filename = os.path.join(output_dir, "example9_glyph.json")
    with open(json_filename, 'w') as f:
        json.dump(original_glyph.to_dict(), f, indent=2)
    
    print(f"Exported: {json_filename}")
    
    # Import the glyph
    with open(json_filename, 'r') as f:
        glyph_dict = json.load(f)
    
    imported_glyph = QEYGlyph.from_dict(glyph_dict)
    
    # Render the imported glyph
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    renderer.render_to_file(imported_glyph, os.path.join(output_dir, "example9_imported_glyph.png"))
    
    print(f"Imported and rendered: {os.path.join(output_dir, 'example9_imported_glyph.png')}")
    print(f"  Original hash: {original_glyph.identity_hash}")
    print(f"  Imported hash: {imported_glyph.identity_hash}")
    print(f"  Match: {original_glyph.identity_hash == imported_glyph.identity_hash}")


def example_10_ghost_and_null():
    """Example 10: Generate Ghost and Null glyphs."""
    print("\n" + "="*60)
    print("Example 10: Ghost and Null Glyphs")
    print("="*60)
    
    generator = QEYGenerator(seed=252627)
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    
    # Ghost glyph
    ghost = generator.generate_glyph(
        identity_data="ghost_identity",
        qey_class=QEYClass.GHOST,
        authority_type=AuthorityType.PERSONAL
    )
    
    renderer.render_to_file(ghost, os.path.join(output_dir, "example10_ghost.png"))
    print(f"Generated Ghost glyph: {os.path.join(output_dir, 'example10_ghost.png')}")
    
    # Null glyph
    null = generator.generate_glyph(
        identity_data="null_identity",
        qey_class=QEYClass.NULL,
        authority_type=AuthorityType.PERSONAL
    )
    
    renderer.render_to_file(null, os.path.join(output_dir, "example10_null.png"))
    print(f"Generated Null glyph: {os.path.join(output_dir, 'example10_null.png')}")


def example_11_batch_generation():
    """Example 11: Batch generate multiple glyphs."""
    print("\n" + "="*60)
    print("Example 11: Batch Generation")
    print("="*60)
    
    generator = QEYGenerator()
    renderer = QEYRenderer(size=256, background_color=(0, 0, 0, 255))
    
    # Generate 10 human glyphs
    batch_dir = os.path.join(output_dir, "batch")
    os.makedirs(batch_dir, exist_ok=True)
    
    for i in range(10):
        glyph = generator.generate_glyph(
            identity_data=f"person_{i:03d}",
            qey_class=QEYClass.HUMAN,
            authority_type=AuthorityType.PERSONAL
        )
        
        filename = os.path.join(batch_dir, f"person_{i:03d}.png")
        renderer.render_to_file(glyph, filename)
    
    print(f"Generated 10 glyphs in: {batch_dir}")


def example_12_custom_glyph():
    """Example 12: Create a custom glyph manually."""
    print("\n" + "="*60)
    print("Example 12: Custom Glyph Creation")
    print("="*60)
    
    from qey_core import Primitive, Layer, PrimitiveElement, LayerType
    import math
    
    # Create a custom glyph
    glyph = QEYGlyph(
        identity_hash="custom_001",
        qey_class=QEYClass.COLLECTIVE,
        size=512
    )
    
    # Add custom origin (central point)
    origin_layer = glyph.get_layer(LayerType.ORIGIN)
    origin_layer.add_primitive(Primitive(
        element_type=PrimitiveElement.POINT,
        x=0, y=0,
        radius=0.08,
        color=(255, 215, 0, 255)  # Gold
    ))
    
    # Add custom lattice (radial lines)
    lattice_layer = glyph.get_layer(LayerType.IDENTITY_LATTICE)
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        lattice_layer.add_primitive(Primitive(
            element_type=PrimitiveElement.LINE,
            x=0, y=0,
            angle=angle,
            length=0.3,
            width=0.01,
            color=(200, 200, 200, 255)
        ))
    
    # Add custom authority ring (double ring)
    authority_layer = glyph.get_layer(LayerType.AUTHORITY_RING)
    authority_layer.add_primitive(Primitive(
        element_type=PrimitiveElement.RING,
        x=0, y=0,
        radius=0.4,
        width=0.015,
        color=(100, 200, 255, 255)
    ))
    authority_layer.add_primitive(Primitive(
        element_type=PrimitiveElement.RING,
        x=0, y=0,
        radius=0.45,
        width=0.01,
        color=(150, 220, 255, 255)
    ))
    
    # Add custom capability array
    capability_layer = glyph.get_layer(LayerType.CAPABILITY_ARRAY)
    for i in range(4):
        angle = i * (2 * math.pi / 4)
        capability_layer.add_primitive(Primitive(
            element_type=PrimitiveElement.ARC,
            x=math.cos(angle) * 0.6,
            y=math.sin(angle) * 0.6,
            radius=0.08,
            angle=0,
            length=math.pi,
            width=0.01,
            color=(200, 100, 200, 255)
        ))
    
    # Render the custom glyph
    renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
    renderer.render_to_file(glyph, os.path.join(output_dir, "example12_custom_glyph.png"))
    
    print(f"Generated: {os.path.join(output_dir, 'example12_custom_glyph.png')}")
    print(f"  Custom glyph with manual primitive placement")




def main():
    """Run all examples."""
    global output_dir
    
    print("\n" + "="*60)
    print("QEY Glyph Generator - Examples")
    print("="*60)
    print("\nThis script will generate various example glyphs")
    print("in the 'examples_output' directory.\n")
    
    # Setup
    output_dir = setup_output_directory()
    
    # Run examples
    examples = [
        ("Simple Human Glyph", example_1_simple_glyph),
        ("Superagent Glyph", example_2_superagent_glyph),
        ("All QEY Classes", example_3_all_classes),
        ("Authority Types", example_4_all_authorities),
        ("Composite Glyph", example_5_composite_glyph),
        ("Living Glyph", example_6_living_glyph),
        ("Authentication Animation", example_7_authentication_animation),
        ("Pulse Animation", example_8_pulse_animation),
        ("JSON Export/Import", example_9_json_export_import),
        ("Ghost and Null Glyphs", example_10_ghost_and_null),
        ("Batch Generation", example_11_batch_generation),
        ("Custom Glyph", example_12_custom_glyph),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
    print(f"\nOutput directory: {os.path.abspath(output_dir)}")
    print("\nYou can now explore the generated glyphs and animations.")


if __name__ == '__main__':
    main()
