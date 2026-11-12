#!/usr/bin/env python3
"""
QEY Glyph Generator - Main Entry Point

This script provides command-line access to the QEY glyph generation system.
"""

import argparse
import sys
import os
import json
from pathlib import Path

from qey_core import (
    QEYGenerator, QEYClass, AuthorityType, Capability, GlyphForm,
    generate_sample_glyphs
)
from qey_renderer import QEYRenderer, QEYAnimator, render_all_sample_glyphs


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='QEY Glyph Generator - Create visual cryptographic glyphs for the Darkbrane Protocol',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate --identity mateus --qey-class HUMAN --output mateus.png
  %(prog)s generate --identity lycos --qey-class SUPERAGENT --authority SOVEREIGN --output lycos.png
  %(prog)s samples --output-dir output
  %(prog)s animate --identity test --output auth.gif --frames 60
  %(prog)s composite --glyph1 mateus.json --glyph2 lycos.json --operator INHERITANCE --output composite.png
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a QEY glyph')
    generate_parser.add_argument('--identity', type=str, default='default', help='Identity data/name')
    generate_parser.add_argument('--qey-class', type=str, default='HUMAN', 
                                  choices=[c.name for c in QEYClass],
                                  help='QEY class')
    generate_parser.add_argument('--authority', type=str, default='PERSONAL',
                                  choices=[a.name for a in AuthorityType],
                                  help='Authority type')
    generate_parser.add_argument('--form', type=str, default='STATIC',
                                  choices=[f.name for f in GlyphForm],
                                  help='Glyph form (STATIC or LIVING)')
    generate_parser.add_argument('--capability', type=str, action='append',
                                  choices=[c.name for c in Capability],
                                  help='Add a capability (can be specified multiple times)')
    generate_parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    generate_parser.add_argument('--size', type=int, default=512, help='Output image size')
    generate_parser.add_argument('--bg-color', type=str, default='0,0,0,0',
                                  help='Background color as R,G,B,A (comma-separated)')
    generate_parser.add_argument('--output', type=str, default='output.png', help='Output filename')
    
    # Samples command
    samples_parser = subparsers.add_parser('samples', help='Generate sample glyphs')
    samples_parser.add_argument('--output-dir', type=str, default='output',
                                 help='Output directory for samples')
    samples_parser.add_argument('--size', type=int, default=512, help='Output image size')
    
    # Animate command
    animate_parser = subparsers.add_parser('animate', help='Create an animated GIF')
    animate_parser.add_argument('--identity', type=str, default='test', help='Identity data')
    animate_parser.add_argument('--qey-class', type=str, default='HUMAN',
                                 choices=[c.name for c in QEYClass],
                                 help='QEY class')
    animate_parser.add_argument('--type', type=str, default='auth',
                                 choices=['auth', 'pulse'],
                                 help='Animation type (auth or pulse)')
    animate_parser.add_argument('--frames', type=int, default=60, help='Number of frames')
    animate_parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    animate_parser.add_argument('--size', type=int, default=512, help='Output size')
    animate_parser.add_argument('--output', type=str, default='animation.gif', help='Output filename')
    
    # Composite command
    composite_parser = subparsers.add_parser('composite', help='Create a composite glyph')
    composite_parser.add_argument('--glyph1', type=str, required=True, help='First glyph JSON file')
    composite_parser.add_argument('--glyph2', type=str, required=True, help='Second glyph JSON file')
    composite_parser.add_argument('--operator', type=str, default='CONTRACT',
                                   help='Composition operator')
    composite_parser.add_argument('--output', type=str, default='composite.png', help='Output filename')
    composite_parser.add_argument('--size', type=int, default=768, help='Output size')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export a glyph to JSON')
    export_parser.add_argument('--identity', type=str, default='test', help='Identity data')
    export_parser.add_argument('--qey-class', type=str, default='HUMAN',
                                choices=[c.name for c in QEYClass],
                                help='QEY class')
    export_parser.add_argument('--output', type=str, default='glyph.json', help='Output JSON filename')
    export_parser.add_argument('--seed', type=int, default=None, help='Random seed')
    
    # GUI command
    subparsers.add_parser('gui', help='Launch the interactive GUI')
    
    return parser.parse_args()


def parse_color(color_str: str) -> tuple:
    """Parse a color string into RGBA tuple."""
    parts = [int(p.strip()) for p in color_str.split(',')]
    if len(parts) == 3:
        return (parts[0], parts[1], parts[2], 255)
    elif len(parts) == 4:
        return (parts[0], parts[1], parts[2], parts[3])
    else:
        return (0, 0, 0, 0)


def main():
    """Main entry point."""
    args = parse_args()
    
    if args.command is None:
        # Default to GUI
        args.command = 'gui'
    
    try:
        if args.command == 'generate':
            cmd_generate(args)
        elif args.command == 'samples':
            cmd_samples(args)
        elif args.command == 'animate':
            cmd_animate(args)
        elif args.command == 'composite':
            cmd_composite(args)
        elif args.command == 'export':
            cmd_export(args)
        elif args.command == 'gui':
            cmd_gui(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def cmd_generate(args):
    """Handle the generate command."""
    # Parse capabilities
    capabilities = []
    if args.capability:
        for cap_name in args.capability:
            capabilities.append(Capability[cap_name])
    
    # Parse background color
    bg_color = parse_color(args.bg_color)
    
    # Create generator
    generator = QEYGenerator(seed=args.seed)
    
    # Generate glyph
    glyph = generator.generate_glyph(
        identity_data=args.identity,
        qey_class=QEYClass[args.qey_class],
        authority_type=AuthorityType[args.authority],
        capabilities=capabilities,
        form=GlyphForm[args.form],
        size=args.size
    )
    
    # Render and save
    renderer = QEYRenderer(size=args.size, background_color=bg_color)
    renderer.render_to_file(glyph, args.output)
    
    print(f"Generated glyph: {args.output}")
    print(f"  Identity: {args.identity}")
    print(f"  Class: {args.qey_class}")
    print(f"  Authority: {args.authority}")
    print(f"  Form: {args.form}")
    cap_names = [c.name for c in capabilities] if capabilities else ['None']
    print(f"  Capabilities: {', '.join(cap_names)}")


def cmd_samples(args):
    """Handle the samples command."""
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate and render all samples
    render_all_sample_glyphs(args.output_dir)
    
    print(f"Generated sample glyphs in: {args.output_dir}")


def cmd_animate(args):
    """Handle the animate command."""
    # Create generator
    generator = QEYGenerator()
    
    # Generate glyph
    glyph = generator.generate_glyph(
        identity_data=args.identity,
        qey_class=QEYClass[args.qey_class],
        form=GlyphForm.LIVING,
        size=args.size
    )
    
    # Create animator
    animator = QEYAnimator(
        size=args.size,
        fps=args.fps,
        duration=args.frames / args.fps
    )
    
    # Create animation
    if args.type == 'auth':
        animator.create_authentication_animation(glyph, args.output, args.frames)
    else:  # pulse
        animator.create_pulse_animation(glyph, args.output, args.frames)
    
    print(f"Created animation: {args.output}")
    print(f"  Type: {args.type}")
    print(f"  Frames: {args.frames}")
    print(f"  FPS: {args.fps}")


def cmd_composite(args):
    """Handle the composite command."""
    # Load glyphs from JSON
    with open(args.glyph1, 'r') as f:
        glyph1_dict = json.load(f)
    with open(args.glyph2, 'r') as f:
        glyph2_dict = json.load(f)
    
    glyph1 = QEYGlyph.from_dict(glyph1_dict)
    glyph2 = QEYGlyph.from_dict(glyph2_dict)
    
    # Create generator
    generator = QEYGenerator()
    
    # Create composite
    composite = generator.generate_composite_glyph(
        [glyph1, glyph2],
        operator=args.operator
    )
    
    # Render and save
    renderer = QEYRenderer(size=args.size)
    renderer.render_to_file(composite, args.output)
    
    print(f"Created composite glyph: {args.output}")
    print(f"  Operator: {args.operator}")


def cmd_export(args):
    """Handle the export command."""
    # Create generator
    generator = QEYGenerator(seed=args.seed)
    
    # Generate glyph
    glyph = generator.generate_glyph(
        identity_data=args.identity,
        qey_class=QEYClass[args.qey_class]
    )
    
    # Export to JSON
    glyph_dict = glyph.to_dict()
    
    with open(args.output, 'w') as f:
        json.dump(glyph_dict, f, indent=2)
    
    print(f"Exported glyph to: {args.output}")


def cmd_gui(args):
    """Handle the GUI command."""
    # Import here to avoid importing tkinter on headless systems
    try:
        from qey_app import main as gui_main
        print("Launching QEY Glyph Generator GUI...")
        gui_main()
    except ImportError as e:
        print(f"GUI not available: {e}")
        print("Tkinter may not be installed or you may be on a headless system.")
        print("Try using the command-line interface instead.")
        sys.exit(1)


if __name__ == '__main__':
    main()
