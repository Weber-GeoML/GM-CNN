# Mathematical Background

## Group Theory Fundamentals

### What is a Group?
A group (G, ×) is a set G with a binary operation × that satisfies four axioms, implemented across the `group_element/` module.

### Dihedral Groups D_n

The dihedral group D_n represents the symmetries of a regular n-gon, fully implemented in `dihedral_group_element.py`:

- **Order**: 2n elements
- **Generators**: rotation (r) and reflection (f)
- **Relations**: Encoded in the `product()` method logic

#### Group Presentation
D_n = ⟨r, f | r^n = f² = e, frf = r⁻¹⟩

#### Element Enumeration
Every element representable by `DihedralElement(r, f, n)` where:
- f ∈ {0, 1} (flip component)
- r ∈ {0, 1, ..., n-1} (rotation component)

## Group Actions on Data

### Definition
Mathematical concept underlying the equivariance properties that will be implemented in the `layers/` module.

### Examples in Computer Vision
Applications that the `models/` module will target:
- **Rotations**: Image rotation by multiples of 2π/n
- **Reflections**: Image flipping operations
- **Combined**: Compositions via `DihedralElement.product()`

## Equivariant Functions

### Definition
Functions satisfying f(g · x) = g · f(x), the core property that neural network layers in `layers/` will implement.

### Importance in Deep Learning
Benefits realized through the complete GMCNN architecture:
- **Translation Equivariance**: Standard CNN property
- **Rotation Equivariance**: Extended via `group_element/` implementations
- **Data Efficiency**: Achieved through weight sharing in group convolutions
- **Generalization**: Improved performance on transformed inputs

## G-Convolution

### Mathematical Foundation
The theoretical basis for convolution operations that will be implemented in the `layers/` module.

### Standard vs Group Convolution
- **Standard**: Traditional CNN convolution
- **Group**: Extended convolution using `DihedralElement` operations

### Discrete Implementation
For finite groups like those in `dihedral_group_element.py`: discrete summation over group elements.

## Representation Theory

### Group Representations
Mathematical framework underlying the tensor operations in neural network layers.

### Regular Representation
The specific representation type used in G-CNN implementations, utilizing the group structure from `group_element/`.

## Steerable Filters

### Concept
Filter design principle for layers in `layers/` module that transform predictably under group actions.

### Benefits
- **Guaranteed equivariance**: Through mathematical construction
- **Efficient implementation**: Via group element operations
- **Theoretical foundation**: Based on representation theory

## Applications

### Computer Vision
Target applications for models in `models/` module:
- **Object Recognition**: Rotation-invariant classification
- **Medical Imaging**: Orientation-independent analysis
- **Satellite Imagery**: Multi-angle object detection

### Scientific Computing
Extended applications:
- **Physics Simulations**: Respecting physical symmetries
- **Crystallography**: Crystal structure analysis
- **Molecular Modeling**: Conformational analysis

## Implementation Connections

### File Relationships
- `group_element.py`: Provides abstract interface for mathematical operations
- `dihedral_group_element.py`: Implements specific group mathematics
- `layers/`: Will use group operations for equivariant convolutions
- `models/`: Will combine layers into complete architectures
- `utils/`: Will provide supporting functions for group operations

## Further Reading

1. **Group Theory**: Dummit & Foote - "Abstract Algebra"
2. **G-CNNs**: Cohen & Welling - "Group Equivariant Convolutional Networks"
3. **Steerable CNNs**: Cohen & Welling - "Steerable CNNs"
4. **Applications**: Weiler & Cesa - "General E(2)-Equivariant Steerable CNNs"