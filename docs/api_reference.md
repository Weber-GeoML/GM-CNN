# API Reference

## group_element Module

### group_element.py

#### GroupElement (Abstract Base Class)
Abstract base class defining the interface for all group elements.

**Methods:**
- `product(other: GroupElement) -> GroupElement`: Abstract method for group multiplication
- `inverse() -> GroupElement`: Abstract method for computing group inverse  
- `__str__() -> str`: String representation of the group element

### dihedral_group_element.py

#### DihedralElement
Concrete implementation of dihedral group elements D_n.

**Constructor:**
- `__init__(r: int, f: int, n: int)`: Initialize dihedral group element
  - `r`: Rotation component (0 to n-1)
  - `f`: Flip component (0 or 1)
  - `n`: Order of the dihedral group

**Attributes:**
- `r: int`: Rotation component
- `f: int`: Flip component
- `n: int`: Group order

**Methods:**
- `product(other: DihedralElement) -> DihedralElement`: Group multiplication following dihedral group rules
- `inverse() -> DihedralElement`: Compute group inverse
- `__str__() -> str`: String representation (e.g., "r^1", "f^1 * r^2")

**Mathematical Properties:**
- Implements dihedral group D_n with 2n elements
- Satisfies group axioms: closure, associativity, identity, inverse
- Handles composition of rotations and reflections

## Usage Examples

### Basic Group Operations
Working with `DihedralElement` from `dihedral_group_element.py`:
- Create elements with different r, f, n values
- Use `product()` method for group multiplication
- Use `inverse()` method for inverse computation
- Use `__str__()` for readable output

### Group Property Verification
The implementation in `dihedral_group_element.py` ensures:
- All products remain within the group (closure)
- Associative property holds for all elements
- Identity element behaves correctly
- Every element has a proper inverse

## File Dependencies

### Import Structure
- `dihedral_group_element.py` imports from `group_element.py`
- Future modules in `layers/` will import `DihedralElement`
