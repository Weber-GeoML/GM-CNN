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


## Implementation Connections

### File Relationships
- `group_element.py`: Provides abstract interface for mathematical operations
- `dihedral_group_element.py`: Implements specific group mathematics

## Further Reading

1. **Group Theory**: Dummit & Foote - "Abstract Algebra"
2. **G-CNNs**: Cohen & Welling - "Group Equivariant Convolutional Networks"
3. **Steerable CNNs**: Cohen & Welling - "Steerable CNNs"
4. **Applications**: Weiler & Cesa - "General E(2)-Equivariant Steerable CNNs"
