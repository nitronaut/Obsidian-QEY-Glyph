"""
QEY Core Library - The Symbolic Language of the Darkbrane

This library implements the QEY (Quantum Entity Yield) Glyph Language,
a visual cryptographic language for representing identity, authority, 
access permissions and contractual relationships within the Darkbrane.

The QEY system consists of:
- 7 primitive visual elements
- 7 structural layers
- 5 grammatical concepts
- Multiple identity classes
- Static and Living glyph forms
- Compositional language capabilities
"""

import math
import random
import hashlib
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Tuple, Optional, Union
import numpy as np


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class PrimitiveElement(Enum):
    """The seven primitive visual elements of QEY."""
    POINT = auto()      # Dot, node or small disc - Identity, origin or reference
    LINE = auto()       # Straight or curved stroke - Relationship, connection or instruction
    ARC = auto()        # Partial circle - Authority, boundary or scope
    RING = auto()       # Complete circle - Integrity, containment or continuity
    FRACTURE = auto()   # Broken line or interrupted ring - Separation, restriction or delegation
    JUNCTION = auto()   # Intersecting lines - Agreement, association or shared authority
    PULSE = auto()      # Repeated marks or animated segments - Active state, challenge or temporal condition


class LayerType(Enum):
    """The seven structural layers of a QEY glyph."""
    ORIGIN = auto()           # Layer 1: The innermost point or central structure
    IDENTITY_LATTICE = auto() # Layer 2: Pattern of intersecting lines and geometric relationships
    AUTHORITY_RING = auto()   # Layer 3: Circular or segmented boundary
    CAPABILITY_ARRAY = auto() # Layer 4: Radial extensions
    WITNESS_MARK = auto()     # Layer 5: Distinctive marks for cryptographic attestations
    TEMPORAL_RING = auto()    # Layer 6: Outer ring with time-dependent information
    QUANTUM_SEAL = auto()     # Layer 7: Outermost structure, interface to quantum-secure auth


class GrammarElement(Enum):
    """The five fundamental grammatical concepts of QEY."""
    ORIGIN = auto()      # Who or what is acting?
    RELATION = auto()    # What is the relationship?
    AUTHORITY = auto()   # What permission or obligation exists?
    CONDITION = auto()   # Under what circumstances?
    EXECUTION = auto()   # What action is authorised?


class QEYClass(Enum):
    """Different classes of QEY identities."""
    HUMAN = auto()
    SUPERAGENT = auto()
    MACHINE = auto()
    NODE = auto()
    BLOODLINE = auto()
    SOVEREIGN = auto()
    GHOST = auto()
    NULL = auto()
    COLLECTIVE = auto()


class AuthorityType(Enum):
    """Types of authority that can be represented."""
    PERSONAL = auto()
    INHERITED = auto()
    CONTRACTUAL = auto()
    INSTITUTIONAL = auto()
    SOVEREIGN = auto()
    DELEGATED = auto()


class Capability(Enum):
    """Capabilities that can be authorised."""
    ACCESS_INFORMATION = auto()
    EXECUTE_CONTRACTS = auto()
    OPERATE_MACHINERY = auto()
    CONTROL_SERVOBOT = auto()
    ACCESS_SUPERAGENT = auto()
    ENTER_OMNIVERSE = auto()
    ADMINISTER_NODE = auto()


class GlyphForm(Enum):
    """Form of the glyph."""
    STATIC = auto()
    LIVING = auto()


# Visual constants
DEFAULT_SIZE = 512
CENTER = 256
MAX_LAYERS = 7
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Primitive:
    """A single primitive element with visual properties."""
    element_type: PrimitiveElement
    x: float = 0.0
    y: float = 0.0
    radius: float = 1.0
    angle: float = 0.0  # in radians
    length: float = 1.0
    width: float = 1.0
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)  # RGBA
    filled: bool = True
    animated: bool = False
    animation_phase: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'element_type': self.element_type.name,
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'angle': self.angle,
            'length': self.length,
            'width': self.width,
            'color': self.color,
            'filled': self.filled,
            'animated': self.animated,
            'animation_phase': self.animation_phase
        }


@dataclass
class Layer:
    """A single layer in the QEY glyph structure."""
    layer_type: LayerType
    primitives: List[Primitive] = field(default_factory=list)
    radius: float = 1.0
    rotation: float = 0.0
    visibility: float = 1.0  # 0-1 for fade effects
    active: bool = True
    
    def add_primitive(self, primitive: Primitive):
        self.primitives.append(primitive)
        return self
    
    def to_dict(self) -> Dict:
        return {
            'layer_type': self.layer_type.name,
            'radius': self.radius,
            'rotation': self.rotation,
            'visibility': self.visibility,
            'active': self.active,
            'primitives': [p.to_dict() for p in self.primitives]
        }


@dataclass
class QEYGlyph:
    """A complete QEY glyph with all layers and metadata."""
    identity_hash: str = ""  # Cryptographic hash of the identity
    qey_class: QEYClass = QEYClass.HUMAN
    form: GlyphForm = GlyphForm.STATIC
    layers: Dict[LayerType, Layer] = field(default_factory=dict)
    size: int = DEFAULT_SIZE
    background_color: Tuple[int, int, int, int] = (0, 0, 0, 0)  # Transparent
    
    # Authentication state for Living QEY
    is_authenticated: bool = False
    authentication_phase: float = 0.0  # 0-1
    
    # Temporal properties
    validity_start: Optional[float] = None
    validity_end: Optional[float] = None
    
    # Authority properties
    authority_type: AuthorityType = AuthorityType.PERSONAL
    capabilities: List[Capability] = field(default_factory=list)
    
    # Composition
    composed_glyphs: List['QEYGlyph'] = field(default_factory=list)
    composition_operator: Optional[str] = None  # e.g., "INHERITANCE", "CONTRACT", "DELEGATION"
    
    def __post_init__(self):
        # Initialize all layers
        for layer_type in LayerType:
            if layer_type not in self.layers:
                self.layers[layer_type] = Layer(layer_type=layer_type)
    
    def get_layer(self, layer_type: LayerType) -> Layer:
        """Get a specific layer, creating it if it doesn't exist."""
        if layer_type not in self.layers:
            self.layers[layer_type] = Layer(layer_type=layer_type)
        return self.layers[layer_type]
    
    def add_capability(self, capability: Capability):
        """Add a capability to the glyph."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
        return self
    
    def compose(self, other: 'QEYGlyph', operator: str = "CONTRACT"):
        """Compose this glyph with another."""
        self.composed_glyphs.append(other)
        self.composition_operator = operator
        return self
    
    def to_dict(self) -> Dict:
        """Serialize the glyph to a dictionary."""
        return {
            'identity_hash': self.identity_hash,
            'qey_class': self.qey_class.name,
            'form': self.form.name,
            'size': self.size,
            'background_color': self.background_color,
            'is_authenticated': self.is_authenticated,
            'authentication_phase': self.authentication_phase,
            'authority_type': self.authority_type.name,
            'capabilities': [c.name for c in self.capabilities],
            'layers': {k.name: v.to_dict() for k, v in self.layers.items()},
            'composed_glyphs': [g.to_dict() for g in self.composed_glyphs],
            'composition_operator': self.composition_operator
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'QEYGlyph':
        """Deserialize a glyph from a dictionary."""
        glyph = cls(
            identity_hash=data.get('identity_hash', ''),
            qey_class=QEYClass[data.get('qey_class', 'HUMAN')],
            form=GlyphForm[data.get('form', 'STATIC')],
            size=data.get('size', DEFAULT_SIZE),
            background_color=tuple(data.get('background_color', (0, 0, 0, 0))),
            is_authenticated=data.get('is_authenticated', False),
            authentication_phase=data.get('authentication_phase', 0.0),
            authority_type=AuthorityType[data.get('authority_type', 'PERSONAL')],
            capabilities=[Capability[c] for c in data.get('capabilities', [])],
            composition_operator=data.get('composition_operator')
        )
        
        # Reconstruct layers
        for layer_name, layer_data in data.get('layers', {}).items():
            layer_type = LayerType[layer_name]
            layer = Layer(
                layer_type=layer_type,
                radius=layer_data.get('radius', 1.0),
                rotation=layer_data.get('rotation', 0.0),
                visibility=layer_data.get('visibility', 1.0),
                active=layer_data.get('active', True)
            )
            for prim_data in layer_data.get('primitives', []):
                primitive = Primitive(
                    element_type=PrimitiveElement[prim_data['element_type']],
                    x=prim_data.get('x', 0.0),
                    y=prim_data.get('y', 0.0),
                    radius=prim_data.get('radius', 1.0),
                    angle=prim_data.get('angle', 0.0),
                    length=prim_data.get('length', 1.0),
                    width=prim_data.get('width', 1.0),
                    color=tuple(prim_data.get('color', (255, 255, 255, 255))),
                    filled=prim_data.get('filled', True),
                    animated=prim_data.get('animated', False),
                    animation_phase=prim_data.get('animation_phase', 0.0)
                )
                layer.add_primitive(primitive)
            glyph.layers[layer_type] = layer
        
        # Reconstruct composed glyphs (simplified - just references)
        # For full reconstruction, we'd need recursive from_dict
        
        return glyph


@dataclass
class QEYExpression:
    """A compositional expression in QEY language."""
    origin: QEYGlyph
    relation: Optional[QEYGlyph] = None
    authority: Optional[QEYGlyph] = None
    condition: Optional[QEYGlyph] = None
    execution: Optional[QEYGlyph] = None
    
    def to_dict(self) -> Dict:
        return {
            'origin': self.origin.to_dict() if self.origin else None,
            'relation': self.relation.to_dict() if self.relation else None,
            'authority': self.authority.to_dict() if self.authority else None,
            'condition': self.condition.to_dict() if self.condition else None,
            'execution': self.execution.to_dict() if self.execution else None
        }


# =============================================================================
# GLYPH GENERATORS
# =============================================================================

class QEYGenerator:
    """Generates QEY glyphs based on identity and authority parameters."""
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Color palettes for different classes
        self.class_colors = {
            QEYClass.HUMAN: [(200, 100, 50, 255), (255, 200, 150, 255), (150, 80, 40, 255)],
            QEYClass.SUPERAGENT: [(100, 200, 255, 255), (150, 220, 255, 255), (50, 120, 200, 255)],
            QEYClass.MACHINE: [(200, 200, 200, 255), (150, 150, 150, 255), (100, 100, 100, 255)],
            QEYClass.NODE: [(0, 200, 100, 255), (0, 255, 150, 255), (0, 150, 80, 255)],
            QEYClass.BLOODLINE: [(150, 50, 200, 255), (200, 100, 255, 255), (100, 30, 150, 255)],
            QEYClass.SOVEREIGN: [(255, 215, 0, 255), (255, 180, 0, 255), (200, 140, 0, 255)],
            QEYClass.GHOST: [(80, 80, 80, 180), (120, 120, 120, 200), (60, 60, 60, 150)],
            QEYClass.NULL: [(50, 50, 50, 100), (30, 30, 30, 80), (20, 20, 20, 60)],
            QEYClass.COLLECTIVE: [(100, 150, 200, 255), (150, 180, 220, 255), (80, 120, 180, 255)]
        }
        
        # Authority ring patterns
        self.authority_patterns = {
            AuthorityType.PERSONAL: self._generate_personal_authority,
            AuthorityType.INHERITED: self._generate_inherited_authority,
            AuthorityType.CONTRACTUAL: self._generate_contractual_authority,
            AuthorityType.INSTITUTIONAL: self._generate_institutional_authority,
            AuthorityType.SOVEREIGN: self._generate_sovereign_authority,
            AuthorityType.DELEGATED: self._generate_delegated_authority
        }
    
    def generate_identity_hash(self, identity_data: str) -> str:
        """Generate a cryptographic hash for an identity."""
        return hashlib.sha256(identity_data.encode()).hexdigest()[:16]
    
    def generate_glyph(
        self,
        identity_data: str,
        qey_class: QEYClass = QEYClass.HUMAN,
        authority_type: AuthorityType = AuthorityType.PERSONAL,
        capabilities: List[Capability] = None,
        form: GlyphForm = GlyphForm.STATIC,
        size: int = DEFAULT_SIZE
    ) -> QEYGlyph:
        """Generate a complete QEY glyph."""
        if capabilities is None:
            capabilities = []
        
        glyph = QEYGlyph(
            identity_hash=self.generate_identity_hash(identity_data),
            qey_class=qey_class,
            form=form,
            size=size,
            authority_type=authority_type,
            capabilities=capabilities
        )
        
        # Generate each layer
        self._generate_origin_layer(glyph)
        self._generate_identity_lattice_layer(glyph)
        self._generate_authority_ring_layer(glyph)
        self._generate_capability_array_layer(glyph)
        self._generate_witness_mark_layer(glyph)
        self._generate_temporal_ring_layer(glyph)
        self._generate_quantum_seal_layer(glyph)
        
        return glyph
    
    def _generate_origin_layer(self, glyph: QEYGlyph):
        """Generate Layer 1: The Origin."""
        layer = glyph.get_layer(LayerType.ORIGIN)
        layer.radius = 0.1  # Relative to glyph size
        
        # Create central point
        point = Primitive(
            element_type=PrimitiveElement.POINT,
            x=0.0,
            y=0.0,
            radius=0.05,
            color=self._get_class_color(glyph.qey_class, 0)
        )
        layer.add_primitive(point)
        
        # Add class-specific origin elements
        if glyph.qey_class == QEYClass.SUPERAGENT:
            # Superagents have a more complex origin
            for i in range(3):
                angle = i * (2 * math.pi / 3)
                small_point = Primitive(
                    element_type=PrimitiveElement.POINT,
                    x=math.cos(angle) * 0.08,
                    y=math.sin(angle) * 0.08,
                    radius=0.02,
                    color=self._get_class_color(glyph.qey_class, 1)
                )
                layer.add_primitive(small_point)
        elif glyph.qey_class == QEYClass.COLLECTIVE:
            # Collective has multiple origin points
            for i in range(4):
                angle = i * (2 * math.pi / 4) + random.uniform(-0.1, 0.1)
                small_point = Primitive(
                    element_type=PrimitiveElement.POINT,
                    x=math.cos(angle) * 0.06,
                    y=math.sin(angle) * 0.06,
                    radius=0.015,
                    color=self._get_class_color(glyph.qey_class, i % 3)
                )
                layer.add_primitive(small_point)
    
    def _generate_identity_lattice_layer(self, glyph: QEYGlyph):
        """Generate Layer 2: The Identity Lattice."""
        layer = glyph.get_layer(LayerType.IDENTITY_LATTICE)
        layer.radius = 0.25
        
        # Generate lattice based on identity hash
        hash_val = int(glyph.identity_hash[:8], 16)
        
        # Create intersecting lines
        num_lines = 6 + (hash_val % 5)
        for i in range(num_lines):
            angle = i * (2 * math.pi / num_lines) + random.uniform(-0.2, 0.2)
            length = 0.25 * random.uniform(0.8, 1.2)
            
            line = Primitive(
                element_type=PrimitiveElement.LINE,
                x=0.0,
                y=0.0,
                angle=angle,
                length=length,
                width=0.005,
                color=self._get_class_color(glyph.qey_class, 1)
            )
            layer.add_primitive(line)
        
        # Add junctions where lines intersect
        for i in range(num_lines):
            for j in range(i + 1, num_lines):
                if random.random() < 0.3:  # 30% chance of junction
                    angle1 = i * (2 * math.pi / num_lines)
                    angle2 = j * (2 * math.pi / num_lines)
                    
                    # Calculate intersection point (simplified)
                    x = 0.15 * math.cos((angle1 + angle2) / 2)
                    y = 0.15 * math.sin((angle1 + angle2) / 2)
                    
                    junction = Primitive(
                        element_type=PrimitiveElement.JUNCTION,
                        x=x,
                        y=y,
                        radius=0.01,
                        color=self._get_class_color(glyph.qey_class, 2)
                    )
                    layer.add_primitive(junction)
    
    def _generate_authority_ring_layer(self, glyph: QEYGlyph):
        """Generate Layer 3: The Authority Ring."""
        layer = glyph.get_layer(LayerType.AUTHORITY_RING)
        layer.radius = 0.4
        
        # Use authority-specific pattern
        pattern_func = self.authority_patterns.get(
            glyph.authority_type,
            self._generate_personal_authority
        )
        pattern_func(glyph, layer)
    
    def _generate_personal_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate a personal authority ring (complete)."""
        ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.01,
            color=self._get_class_color(glyph.qey_class, 0)
        )
        layer.add_primitive(ring)
    
    def _generate_inherited_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate an inherited authority ring (with lineage markers)."""
        # Main ring
        ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.01,
            color=self._get_class_color(glyph.qey_class, 0)
        )
        layer.add_primitive(ring)
        
        # Add inheritance markers (small arcs)
        for i in range(4):
            angle = i * (2 * math.pi / 4)
            arc = Primitive(
                element_type=PrimitiveElement.ARC,
                x=math.cos(angle) * layer.radius,
                y=math.sin(angle) * layer.radius,
                radius=0.03,
                angle=angle,
                length=math.pi / 2,
                width=0.005,
                color=self._get_class_color(glyph.qey_class, 1)
            )
            layer.add_primitive(arc)
    
    def _generate_contractual_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate a contractual authority ring (segmented)."""
        # Create segmented ring
        num_segments = 8
        for i in range(num_segments):
            angle = i * (2 * math.pi / num_segments)
            segment_length = 2 * math.pi / num_segments * 0.8  # 80% of full segment
            
            arc = Primitive(
                element_type=PrimitiveElement.ARC,
                x=0.0,
                y=0.0,
                radius=layer.radius,
                angle=angle,
                length=segment_length,
                width=0.01,
                color=self._get_class_color(glyph.qey_class, i % 2)
            )
            layer.add_primitive(arc)
    
    def _generate_institutional_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate an institutional authority ring (double ring)."""
        # Outer ring
        outer_ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.01,
            color=self._get_class_color(glyph.qey_class, 0)
        )
        layer.add_primitive(outer_ring)
        
        # Inner ring
        inner_ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius * 0.9,
            width=0.008,
            color=self._get_class_color(glyph.qey_class, 1)
        )
        layer.add_primitive(inner_ring)
    
    def _generate_sovereign_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate a sovereign authority ring (with crown-like projections)."""
        # Main ring
        ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.015,
            color=self._get_class_color(glyph.qey_class, 0)
        )
        layer.add_primitive(ring)
        
        # Add crown projections
        for i in range(6):
            angle = i * (2 * math.pi / 6)
            x = math.cos(angle) * layer.radius
            y = math.sin(angle) * layer.radius
            
            line = Primitive(
                element_type=PrimitiveElement.LINE,
                x=x,
                y=y,
                angle=angle,
                length=0.05,
                width=0.008,
                color=self._get_class_color(glyph.qey_class, 1)
            )
            layer.add_primitive(line)
    
    def _generate_delegated_authority(self, glyph: QEYGlyph, layer: Layer):
        """Generate a delegated authority ring (with fractures)."""
        # Create ring with fractures
        num_segments = 6
        for i in range(num_segments):
            angle = i * (2 * math.pi / num_segments)
            segment_length = 2 * math.pi / num_segments * 0.7  # 70% of full segment
            
            # Every other segment is a fracture
            if i % 2 == 0:
                fracture = Primitive(
                    element_type=PrimitiveElement.FRACTURE,
                    x=0.0,
                    y=0.0,
                    radius=layer.radius,
                    angle=angle,
                    length=segment_length,
                    width=0.01,
                    color=self._get_class_color(glyph.qey_class, 0)
                )
                layer.add_primitive(fracture)
            else:
                arc = Primitive(
                    element_type=PrimitiveElement.ARC,
                    x=0.0,
                    y=0.0,
                    radius=layer.radius,
                    angle=angle,
                    length=segment_length,
                    width=0.01,
                    color=self._get_class_color(glyph.qey_class, 1)
                )
                layer.add_primitive(arc)
    
    def _generate_capability_array_layer(self, glyph: QEYGlyph):
        """Generate Layer 4: The Capability Array."""
        layer = glyph.get_layer(LayerType.CAPABILITY_ARRAY)
        layer.radius = 0.6
        
        # If no capabilities, add a minimal structure
        if not glyph.capabilities:
            # Add a few default radial lines
            for i in range(4):
                angle = i * (2 * math.pi / 4)
                line = Primitive(
                    element_type=PrimitiveElement.LINE,
                    x=0.0,
                    y=0.0,
                    angle=angle,
                    length=layer.radius,
                    width=0.005,
                    color=self._get_class_color(glyph.qey_class, 0)
                )
                layer.add_primitive(line)
        else:
            # Distribute capabilities radially
            num_capabilities = len(glyph.capabilities)
            for i, capability in enumerate(glyph.capabilities):
                angle = i * (2 * math.pi / num_capabilities)
                
                # Different visual representation for each capability
                if capability in [Capability.ACCESS_INFORMATION, Capability.ACCESS_SUPERAGENT]:
                    # Access capabilities: lines
                    line = Primitive(
                        element_type=PrimitiveElement.LINE,
                        x=0.0,
                        y=0.0,
                        angle=angle,
                        length=layer.radius * 0.9,
                        width=0.01,
                        color=(100, 200, 100, 255)
                    )
                    layer.add_primitive(line)
                elif capability in [Capability.EXECUTE_CONTRACTS, Capability.ADMINISTER_NODE]:
                    # Execution capabilities: arcs
                    arc = Primitive(
                        element_type=PrimitiveElement.ARC,
                        x=math.cos(angle) * layer.radius * 0.5,
                        y=math.sin(angle) * layer.radius * 0.5,
                        radius=0.1,
                        angle=angle,
                        length=math.pi,
                        width=0.01,
                        color=(200, 100, 200, 255)
                    )
                    layer.add_primitive(arc)
                elif capability in [Capability.OPERATE_MACHINERY, Capability.CONTROL_SERVOBOT]:
                    # Control capabilities: junctions
                    junction = Primitive(
                        element_type=PrimitiveElement.JUNCTION,
                        x=math.cos(angle) * layer.radius * 0.7,
                        y=math.sin(angle) * layer.radius * 0.7,
                        radius=0.02,
                        color=(200, 200, 100, 255)
                    )
                    layer.add_primitive(junction)
                elif capability == Capability.ENTER_OMNIVERSE:
                    # Special capability: ring
                    ring = Primitive(
                        element_type=PrimitiveElement.RING,
                        x=math.cos(angle) * layer.radius * 0.6,
                        y=math.sin(angle) * layer.radius * 0.6,
                        radius=0.05,
                        width=0.008,
                        color=(100, 100, 200, 255)
                    )
                    layer.add_primitive(ring)
    
    def _generate_witness_mark_layer(self, glyph: QEYGlyph):
        """Generate Layer 5: The Witness Mark."""
        layer = glyph.get_layer(LayerType.WITNESS_MARK)
        layer.radius = 0.75
        
        # Generate witness marks based on identity hash
        hash_val = int(glyph.identity_hash[8:16], 16)
        
        # Number of witness marks based on hash
        num_marks = 3 + (hash_val % 5)
        
        for i in range(num_marks):
            angle = random.uniform(0, 2 * math.pi)
            distance = 0.7 + random.uniform(-0.05, 0.05)
            
            # Different mark types
            mark_type = hash_val % 3
            if mark_type == 0:
                # Point mark
                point = Primitive(
                    element_type=PrimitiveElement.POINT,
                    x=math.cos(angle) * distance,
                    y=math.sin(angle) * distance,
                    radius=0.015,
                    color=(255, 255, 255, 255)
                )
                layer.add_primitive(point)
            elif mark_type == 1:
                # Small line mark
                line = Primitive(
                    element_type=PrimitiveElement.LINE,
                    x=math.cos(angle) * distance,
                    y=math.sin(angle) * distance,
                    angle=angle + math.pi / 2,
                    length=0.03,
                    width=0.005,
                    color=(255, 255, 255, 255)
                )
                layer.add_primitive(line)
            else:
                # Small arc mark
                arc = Primitive(
                    element_type=PrimitiveElement.ARC,
                    x=math.cos(angle) * distance,
                    y=math.sin(angle) * distance,
                    radius=0.02,
                    angle=0,
                    length=math.pi,
                    width=0.005,
                    color=(255, 255, 255, 255)
                )
                layer.add_primitive(arc)
    
    def _generate_temporal_ring_layer(self, glyph: QEYGlyph):
        """Generate Layer 6: The Temporal Ring."""
        layer = glyph.get_layer(LayerType.TEMPORAL_RING)
        layer.radius = 0.85
        
        # Main temporal ring
        ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.008,
            color=(200, 200, 200, 255),
            animated=glyph.form == GlyphForm.LIVING
        )
        layer.add_primitive(ring)
        
        # Add temporal markers
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            marker = Primitive(
                element_type=PrimitiveElement.POINT,
                x=math.cos(angle) * layer.radius,
                y=math.sin(angle) * layer.radius,
                radius=0.005,
                color=(200, 200, 200, 255),
                animated=glyph.form == GlyphForm.LIVING
            )
            layer.add_primitive(marker)
    
    def _generate_quantum_seal_layer(self, glyph: QEYGlyph):
        """Generate Layer 7: The Quantum Seal."""
        layer = glyph.get_layer(LayerType.QUANTUM_SEAL)
        layer.radius = 0.95
        
        # Main seal ring
        seal_ring = Primitive(
            element_type=PrimitiveElement.RING,
            x=0.0,
            y=0.0,
            radius=layer.radius,
            width=0.012,
            color=self._get_class_color(glyph.qey_class, 2),
            animated=glyph.form == GlyphForm.LIVING
        )
        layer.add_primitive(seal_ring)
        
        # Add quantum seal elements
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            
            # Create pulse-like elements
            pulse = Primitive(
                element_type=PrimitiveElement.PULSE,
                x=math.cos(angle) * layer.radius,
                y=math.sin(angle) * layer.radius,
                radius=0.01,
                angle=angle,
                length=0.03,
                width=0.005,
                color=self._get_class_color(glyph.qey_class, 0),
                animated=glyph.form == GlyphForm.LIVING
            )
            layer.add_primitive(pulse)
        
        # Add authentication indicator
        if glyph.form == GlyphForm.LIVING:
            auth_indicator = Primitive(
                element_type=PrimitiveElement.POINT,
                x=0.0,
                y=layer.radius + 0.02,
                radius=0.015,
                color=(0, 255, 0, 255) if glyph.is_authenticated else (255, 0, 0, 255),
                animated=True
            )
            layer.add_primitive(auth_indicator)
    
    def _get_class_color(self, qey_class: QEYClass, index: int) -> Tuple[int, int, int, int]:
        """Get a color from the class palette."""
        colors = self.class_colors.get(qey_class, [(255, 255, 255, 255)])
        return colors[index % len(colors)]
    
    def generate_composite_glyph(
        self,
        glyphs: List[QEYGlyph],
        operator: str = "CONTRACT"
    ) -> QEYGlyph:
        """Generate a composite glyph from multiple glyphs."""
        if not glyphs:
            raise ValueError("At least one glyph is required")
        
        # Use the first glyph as the base
        base_glyph = glyphs[0]
        
        # Create a new glyph that composes the others
        composite = QEYGlyph(
            identity_hash=self.generate_identity_hash(operator + "_" + "_".join(g.identity_hash for g in glyphs)),
            qey_class=QEYClass.COLLECTIVE,
            form=GlyphForm.STATIC,
            size=base_glyph.size,
            composition_operator=operator
        )
        
        # Copy layers from base glyph
        for layer_type, layer in base_glyph.layers.items():
            new_layer = Layer(
                layer_type=layer.layer_type,
                radius=layer.radius,
                rotation=layer.rotation,
                visibility=layer.visibility,
                active=layer.active
            )
            for prim in layer.primitives:
                new_prim = Primitive(
                    element_type=prim.element_type,
                    x=prim.x,
                    y=prim.y,
                    radius=prim.radius,
                    angle=prim.angle,
                    length=prim.length,
                    width=prim.width,
                    color=prim.color,
                    filled=prim.filled,
                    animated=prim.animated,
                    animation_phase=prim.animation_phase
                )
                new_layer.add_primitive(new_prim)
            composite.layers[layer_type] = new_layer
        
        # Add composed glyphs
        composite.composed_glyphs = glyphs[1:]
        
        # Modify the authority ring to show composition
        layer = composite.get_layer(LayerType.AUTHORITY_RING)
        # Add connection lines between glyphs
        for i, glyph in enumerate(glyphs[1:]):
            angle = i * (2 * math.pi / len(glyphs))
            line = Primitive(
                element_type=PrimitiveElement.LINE,
                x=0.0,
                y=0.0,
                angle=angle,
                length=0.5,
                width=0.008,
                color=(200, 200, 0, 255)
            )
            layer.add_primitive(line)
        
        return composite


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_sample_glyphs() -> List[QEYGlyph]:
    """Generate a set of sample glyphs for demonstration."""
    generator = QEYGenerator(seed=42)
    
    glyphs = []
    
    # Human glyph
    human = generator.generate_glyph(
        identity_data="mateus_fiel_human_001",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.PERSONAL,
        capabilities=[
            Capability.ACCESS_INFORMATION,
            Capability.ACCESS_SUPERAGENT
        ],
        form=GlyphForm.STATIC
    )
    glyphs.append(human)
    
    # Superagent glyph
    superagent = generator.generate_glyph(
        identity_data="lycos_superagent_001",
        qey_class=QEYClass.SUPERAGENT,
        authority_type=AuthorityType.INSTITUTIONAL,
        capabilities=[
            Capability.EXECUTE_CONTRACTS,
            Capability.OPERATE_MACHINERY,
            Capability.ACCESS_INFORMATION
        ],
        form=GlyphForm.STATIC
    )
    glyphs.append(superagent)
    
    # Machine glyph
    machine = generator.generate_glyph(
        identity_data="loopdrive_machine_001",
        qey_class=QEYClass.MACHINE,
        authority_type=AuthorityType.DELEGATED,
        capabilities=[
            Capability.OPERATE_MACHINERY,
            Capability.ADMINISTER_NODE
        ],
        form=GlyphForm.STATIC
    )
    glyphs.append(machine)
    
    # Bloodline glyph
    bloodline = generator.generate_glyph(
        identity_data="fiel_bloodline_001",
        qey_class=QEYClass.BLOODLINE,
        authority_type=AuthorityType.INHERITED,
        capabilities=[
            Capability.ACCESS_SUPERAGENT,
            Capability.ENTER_OMNIVERSE
        ],
        form=GlyphForm.STATIC
    )
    glyphs.append(bloodline)
    
    # Ghost glyph
    ghost = generator.generate_glyph(
        identity_data="ghost_identity_001",
        qey_class=QEYClass.GHOST,
        authority_type=AuthorityType.PERSONAL,
        capabilities=[],
        form=GlyphForm.STATIC
    )
    glyphs.append(ghost)
    
    # Living glyph (authenticated)
    living = generator.generate_glyph(
        identity_data="mateus_authenticated",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.CONTRACTUAL,
        capabilities=[
            Capability.ACCESS_INFORMATION,
            Capability.EXECUTE_CONTRACTS
        ],
        form=GlyphForm.LIVING
    )
    living.is_authenticated = True
    living.authentication_phase = 1.0
    glyphs.append(living)
    
    return glyphs


if __name__ == "__main__":
    # Test the core library
    print("Testing QEY Core Library...")
    generator = QEYGenerator(seed=42)
    
    # Generate a sample glyph
    glyph = generator.generate_glyph(
        identity_data="test_identity_001",
        qey_class=QEYClass.HUMAN,
        authority_type=AuthorityType.PERSONAL,
        capabilities=[Capability.ACCESS_INFORMATION]
    )
    
    print(f"Generated glyph: {glyph.identity_hash}")
    print(f"Class: {glyph.qey_class.name}")
    print(f"Authority: {glyph.authority_type.name}")
    print(f"Capabilities: {[c.name for c in glyph.capabilities]}")
    print(f"Layers: {list(glyph.layers.keys())}")
    
    # Test serialization
    glyph_dict = glyph.to_dict()
    restored_glyph = QEYGlyph.from_dict(glyph_dict)
    print(f"Serialization test passed: {restored_glyph.identity_hash == glyph.identity_hash}")
    
    # Generate sample glyphs
    sample_glyphs = generate_sample_glyphs()
    print(f"Generated {len(sample_glyphs)} sample glyphs")
    
    print("QEY Core Library test complete!")
