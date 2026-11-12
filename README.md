# QEY Glyph Generator - Darkbrane Protocol

## Overview

The **QEY Glyph Generator** is a graphical implementation of the **QEY (Quantum Entity Yield) Glyph Language**, a visual cryptographic language designed for the **Darkbrane Protocol** and the **Dead Drop Society** universe.

QEY is not just a barcode or QR code alternative. It is a **compositional symbolic language** that represents:
- **Identity** - Who or what is acting
- **Authority** - What permissions or obligations exist
- **Authentication** - Visual interface to cryptographic verification
- **Contractual Relationships** - Complex executable agreements

## Features

### Core System
- **7 Primitive Elements**: Point, Line, Arc, Ring, Fracture, Junction, Pulse
- **7 Structural Layers**: Origin, Identity Lattice, Authority Ring, Capability Array, Witness Mark, Temporal Ring, Quantum Seal
- **5 Grammatical Concepts**: Origin, Relation, Authority, Condition, Execution
- **9 Identity Classes**: Human, Superagent, Machine, Node, Bloodline, Sovereign, Ghost, Null, Collective

### Visual Design
- Radial and symmetrical structures with intentional asymmetry
- Ancient symbolic script aesthetics combined with futuristic cryptographic machinery
- Distinctive visual identity for each QEY class
- Static and Living (animated) glyph forms

### Capabilities
- Generate unique QEY glyphs for any identity
- Configure authority types and capabilities
- Create composite glyphs representing complex relationships
- Export static PNG images
- Export animated GIFs for Living QEY
- Export/import glyph definitions as JSON
- Interactive GUI for glyph creation and exploration

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Required Packages
```bash
pip install pillow numpy
```

### Optional Packages
- For GUI: tkinter (usually included with Python)

### Quick Install
```bash
# Clone or download this repository
cd qey_glyph_generator

# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install pillow numpy
```

## Usage

### Command Line

#### Generate a single glyph
```python
from qey_core import QEYGenerator, QEYClass, AuthorityType, Capability
from qey_renderer import QEYRenderer

# Create generator
generator = QEYGenerator(seed=42)

# Generate a human glyph
glyph = generator.generate_glyph(
    identity_data="mateus_fiel",
    qey_class=QEYClass.HUMAN,
    authority_type=AuthorityType.INHERITED,
    capabilities=[Capability.ACCESS_SUPERAGENT, Capability.EXECUTE_CONTRACTS]
)

# Render to file
renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 255))
renderer.render_to_file(glyph, "mateus_qey.png")
```

#### Generate sample glyphs
```python
from qey_renderer import render_all_sample_glyphs

# Generates all sample glyphs to the 'output' directory
render_all_sample_glyphs('output')
```

#### Create animations
```python
from qey_core import QEYGenerator, QEYClass, GlyphForm
from qey_renderer import QEYAnimator

generator = QEYGenerator(seed=42)
glyph = generator.generate_glyph(
    identity_data="test",
    qey_class=QEYClass.HUMAN,
    form=GlyphForm.LIVING
)

animator = QEYAnimator(size=512, fps=30)
animator.create_authentication_animation(glyph, "auth_animation.gif")
```

### Graphical Interface

Run the interactive GUI application:
```bash
python qey_app.py
```

The GUI provides:
- Identity configuration (class, form, seed)
- Authority configuration (type, authentication state)
- Capability selection
- Real-time glyph preview
- Export to PNG and JSON
- Animation generation
- Sample glyphs browser

## Architecture

### Core Modules

1. **qey_core.py** - Core QEY language implementation
   - Primitive elements and layers
   - Glyph generation and composition
   - Serialization/deserialization
   - Sample glyph generation

2. **qey_renderer.py** - Visual rendering engine
   - Static glyph rendering to PIL Images
   - Animated GIF generation
   - Post-processing effects
   - Multiple output formats

3. **qey_app.py** - Interactive GUI application
   - Tkinter-based interface
   - Real-time preview
   - Export functionality
   - History management

### Data Structures

#### Primitive
Represents a single visual element with properties:
- Type (Point, Line, Arc, Ring, Fracture, Junction, Pulse)
- Position (x, y)
- Dimensions (radius, length, width)
- Orientation (angle)
- Color (RGBA)
- Animation properties

#### Layer
Contains multiple primitives for a specific structural layer:
- Layer type (Origin, Identity Lattice, etc.)
- Radius (distance from center)
- Rotation
- Visibility
- Active state

#### QEYGlyph
Complete glyph with all layers and metadata:
- Identity hash
- QEY class
- Form (Static/Living)
- Authority type
- Capabilities
- Temporal properties
- Authentication state
- Composed glyphs

## The QEY Language

### Primitive Elements

| Element | Visual Form | Meaning |
|---------|-------------|---------|
| Point | Dot, node, small disc | Identity, origin, reference |
| Line | Straight or curved stroke | Relationship, connection, instruction |
| Arc | Partial circle | Authority, boundary, scope |
| Ring | Complete circle | Integrity, containment, continuity |
| Fracture | Broken line or interrupted ring | Separation, restriction, delegation |
| Junction | Intersecting lines | Agreement, association, shared authority |
| Pulse | Repeated marks or animated segments | Active state, challenge, temporal condition |

### Structural Layers

1. **Origin** - Innermost point identifying the originating identity
2. **Identity Lattice** - Pattern of intersecting lines representing public cryptographic reference
3. **Authority Ring** - Circular or segmented boundary indicating scope of authority
4. **Capability Array** - Radial extensions indicating authorised activities
5. **Witness Mark** - Distinctive marks for cryptographic attestations
6. **Temporal Ring** - Outer ring with time-dependent information
7. **Quantum Seal** - Outermost structure, interface to quantum-secure authentication

### Identity Classes

- **Human** - Personal identity, biometric association, inherited credentials
- **Superagent** - Autonomous identity, processing authority, contractual obligations
- **Machine** - Hardware identity, operating permissions, ownership
- **Node** - Network identity, routing privileges, validator status
- **Bloodline** - Inherited identity, contractual succession
- **Sovereign** - Exceptional authority over a defined domain
- **Ghost** - Identity operating outside recognised registries
- **Null** - Revoked, erased, or deliberately unresolvable identity
- **Collective** - Shared identity representing multiple participants

### Authority Types

- **Personal** - Individual authority
- **Inherited** - Authority passed down through lineage
- **Contractual** - Authority granted by agreement
- **Institutional** - Authority from an organization
- **Sovereign** - Supreme authority over a domain
- **Delegated** - Authority granted to another entity

### Capabilities

- Access Information
- Execute Contracts
- Operate Machinery
- Control Servobot
- Access Superagent
- Enter Omniverse Environment
- Administer Network Node

## Design Philosophy

### Visual Aesthetics

QEY glyphs are designed to look like a cross between:
- **Ancient symbolic scripts** - Evoking the mystery and tradition of historical writing systems
- **Mathematical notation** - Precise, structured, and meaningful
- **Futuristic cryptographic machinery** - Complex, technological, and secure

### Key Design Principles

1. **Radial Symmetry** - Most glyphs are radially symmetric, but with intentional asymmetry to convey specific meanings
2. **Layered Structure** - Seven distinct layers provide depth and complexity
3. **Compositional** - Individual glyphs can be combined to form larger expressions
4. **Dynamic** - Living QEY glyphs can animate and change based on authentication state
5. **Distinctive** - Each QEY class has unique visual characteristics

### Color Schemes

Each QEY class has its own color palette:
- **Human**: Warm earth tones (reds, oranges, browns)
- **Superagent**: Cool blues and cyans
- **Machine**: Metallic grays and silvers
- **Node**: Greens representing network connectivity
- **Bloodline**: Purples representing heritage
- **Sovereign**: Golds representing authority
- **Ghost**: Transparent grays (barely visible)
- **Null**: Very dark, almost invisible
- **Collective**: Mixed blues representing cooperation

## Examples

### Simple Human Glyph
```python
from qey_core import QEYGenerator, QEYClass, AuthorityType
from qey_renderer import QEYRenderer

generator = QEYGenerator(seed=42)
glyph = generator.generate_glyph(
    identity_data="john_doe",
    qey_class=QEYClass.HUMAN,
    authority_type=AuthorityType.PERSONAL
)

renderer = QEYRenderer(size=512)
renderer.render_to_file(glyph, "human_glyph.png")
```

### Composite Glyph (Inheritance)
```python
from qey_core import QEYGenerator, QEYClass, AuthorityType, Capability

generator = QEYGenerator(seed=42)

# Create parent glyph
parent = generator.generate_glyph(
    identity_data="fiel_ancestor",
    qey_class=QEYClass.HUMAN,
    authority_type=AuthorityType.BLOODLINE
)

# Create child glyph
child = generator.generate_glyph(
    identity_data="mateus_fiel",
    qey_class=QEYClass.HUMAN,
    authority_type=AuthorityType.INHERITED,
    capabilities=[Capability.ACCESS_SUPERAGENT]
)

# Create composite
composite = generator.generate_composite_glyph(
    [parent, child],
    operator="INHERITANCE"
)

renderer = QEYRenderer(size=768)
renderer.render_to_file(composite, "inheritance_glyph.png")
```

### Living QEY with Animation
```python
from qey_core import QEYGenerator, QEYClass, GlyphForm
from qey_renderer import QEYAnimator

generator = QEYGenerator(seed=42)
glyph = generator.generate_glyph(
    identity_data="authenticated_user",
    qey_class=QEYClass.HUMAN,
    form=GlyphForm.LIVING
)

animator = QEYAnimator(size=512, fps=30)
animator.create_authentication_animation(
    glyph,
    "authentication.gif",
    num_frames=90
)
```

## Integration with Darkbrane

### QKD Integration

QEY glyphs are designed to work with **Quantum Key Distribution (QKD)** systems:

1. **Glyph Presentation** - User presents QEY to a Loopdrive or authentication terminal
2. **Identity Resolution** - Darkbrane resolves the glyph against its identity registry
3. **Challenge Generation** - Terminal generates a fresh authentication challenge
4. **Credential Verification** - User proves possession of private credentials
5. **Quantum-Secure Session** - QKD establishes shared secret key where available
6. **Contract Verification** - Darkbrane evaluates authority and permissions
7. **Glyph Activation** - Living QEY displays authentication and permission state

### Authentication Flow

For **Static QEY**:
- Provides identity reference
- Cannot independently prove authorization
- Requires external verification

For **Living QEY**:
- Dynamically renders based on authentication state
- Rings, junctions, and marks change during authentication
- Visual feedback for trust, authority, and access
- Complete pattern = successful authentication
- Fractured pattern = authentication failure

## File Formats

### PNG Export
- Static image of the glyph
- Transparent or colored background
- Configurable size
- High-quality rendering

### JSON Export
```json
{
  "identity_hash": "abc123...",
  "qey_class": "HUMAN",
  "form": "STATIC",
  "size": 512,
  "background_color": [0, 0, 0, 0],
  "is_authenticated": false,
  "authentication_phase": 0.0,
  "authority_type": "PERSONAL",
  "capabilities": ["ACCESS_INFORMATION"],
  "layers": {
    "ORIGIN": {...},
    "IDENTITY_LATTICE": {...},
    ...
  }
}
```

### GIF Export
- Animated glyph for Living QEY
- Configurable frame rate and duration
- Shows authentication process or pulsing effects

## Advanced Usage

### Custom Glyph Generation

Create custom glyphs with specific patterns:
```python
from qey_core import QEYGlyph, QEYClass, LayerType, PrimitiveElement, Primitive, Layer

# Create a custom glyph
glyph = QEYGlyph(
    identity_hash="custom_001",
    qey_class=QEYClass.HUMAN
)

# Add custom origin
origin_layer = glyph.get_layer(LayerType.ORIGIN)
origin_layer.add_primitive(Primitive(
    element_type=PrimitiveElement.POINT,
    x=0, y=0,
    radius=0.1,
    color=(255, 0, 0, 255)
))

# Add custom lattice
lattice_layer = glyph.get_layer(LayerType.IDENTITY_LATTICE)
for i in range(8):
    angle = i * (2 * math.pi / 8)
    lattice_layer.add_primitive(Primitive(
        element_type=PrimitiveElement.LINE,
        x=0, y=0,
        angle=angle,
        length=0.3,
        width=0.01,
        color=(255, 255, 255, 255)
    ))

# Render it
renderer = QEYRenderer()
renderer.render_to_file(glyph, "custom_glyph.png")
```

### Batch Generation

Generate multiple glyphs for a population:
```python
from qey_core import QEYGenerator, QEYClass, AuthorityType
from qey_renderer import QEYRenderer

generator = QEYGenerator()
renderer = QEYRenderer(size=256)

# Generate 100 human glyphs
for i in range(100):
    glyph = generator.generate_glyph(
        identity_data=f"person_{i:03d}",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.PERSONAL
    )
    renderer.render_to_file(glyph, f"population/person_{i:03d}.png")
```

## Performance

### Rendering Speed
- Simple glyphs: ~10-50ms per render
- Complex glyphs with many primitives: ~50-200ms per render
- Animations: ~1-5 seconds for 60-frame GIF

### Memory Usage
- Each glyph: ~1-10KB in memory
- Rendered image (512x512): ~1MB as PNG
- Animation (60 frames): ~10-50MB as GIF

### Scalability
- Can generate thousands of unique glyphs
- Each glyph has unique visual characteristics based on identity hash
- Deterministic generation (same seed = same glyph)

## Contributing

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd qey_glyph_generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install for development
pip install -e .
```

### Running Tests
```bash
# Run core tests
python -m unittest tests.test_core

# Run renderer tests
python -m unittest tests.test_renderer

# Run all tests
python -m unittest discover tests
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Keep functions focused and single-purpose
- Use descriptive variable names

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

## Acknowledgments

- Inspired by the **Darkbrane Protocol** and **Dead Drop Society** universe
- Designed to evoke the aesthetic of **ancient symbolic scripts** and **futuristic cryptographic systems**
- Built with **Python**, **Pillow**, and **NumPy**

## Contact

For questions, issues, or contributions, please refer to the project's issue tracker or documentation.

---

**QEY Glyph Generator** - Making the Darkbrane visually distinctive, one glyph at a time.
