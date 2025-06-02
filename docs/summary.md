# GMCNN: Group-equivariant Convolutional Neural Networks

## Overview

## Repository Structure

```
gmcnn/
├── group_element/           # Group theory implementations
│   ├── group_element.py     # Abstract base class for group elements
│   └── dihedral_group_element.py  # Dihedral group element implementation
```

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
