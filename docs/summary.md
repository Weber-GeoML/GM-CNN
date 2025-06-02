# GMCNN: Group-equivariant Convolutional Neural Networks

## Overview

GMCNN is a Python library implementing Group-equivariant Convolutional Neural Networks (G-CNNs), specifically designed to work with dihedral group symmetries. G-CNNs are neural networks that respect the symmetries of their input data, making them particularly effective for tasks where rotational and reflectional symmetries are important (e.g., image classification, pattern recognition).

## What are G-CNNs?

Group-equivariant Convolutional Neural Networks extend traditional CNNs by incorporating group theory concepts:

- **Equivariance**: If you transform the input (e.g., rotate an image), the network's internal representations transform in a predictable way
- **Group Actions**: Mathematical operations that describe how symmetries act on data
- **Dihedral Groups**: Groups that capture rotations and reflections, denoted as D_n (rotations by 2π/n and reflections)

## Key Benefits

1. **Reduced Parameter Count**: Sharing weights across group transformations
2. **Improved Generalization**: Built-in understanding of symmetries
3. **Data Efficiency**: Less training data needed due to symmetry constraints
4. **Theoretical Guarantees**: Mathematical foundation ensures consistent behavior

## Repository Structure

```
gmcnn/
├── group_element/           # Group theory implementations
│   ├── group_element.py     # Abstract base class for group elements
│   └── dihedral_group_element.py  # Dihedral group element implementation
├── layers/                  # Neural network layer implementations
├── models/                  # Complete model architectures
└── utils/                   # Utility functions and helpers
```

## Quick Start

The core functionality revolves around the `DihedralElement` class in `dihedral_group_element.py`, which provides methods like `product()` and `inverse()` for group operations.

## Documentation Structure

- **[Group Elements](group_elements.md)**: Detailed explanation of group theory implementation
- **[Mathematical Background](mathematical_background.md)**: Theoretical foundations and concepts
- **[Implementation Details](implementation_details.md)**: Code architecture and design decisions
- **[API Reference](api_reference.md)**: Complete function and class documentation

## Mathematical Foundation

The library implements the dihedral group D_n, which has 2n elements:
- n rotations: {r^0, r^1, ..., r^(n-1)} where r is rotation by 2π/n
- n reflections: {f, fr, fr^2, ..., fr^(n-1)} where f is a reflection

Group multiplication follows the relations:
- r^n = e (identity)
- f^2 = e
- frf = r^(-1)