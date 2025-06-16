import pytest
from gmcnn.group_element.permutation_group_element import PermutationElement


def test_permutation_initialization() -> None:
    """Test initialization of PermutationElement."""
    # Test valid permutation
    perm = PermutationElement([1, 2, 0])
    assert perm.permutation == [1, 2, 0]

    # Test identity permutation
    identity = PermutationElement([0, 1, 2])
    assert identity.permutation == [0, 1, 2]


def test_permutation_product() -> None:
    """Test the product (composition) of permutations."""
    # Test composition of two permutations
    p1 = PermutationElement([1, 0, 2])
    p2 = PermutationElement([2, 1, 0])
    result = p1.product(p2)
    assert result.permutation == [2, 0, 1]

    # Test composition with identity
    identity = PermutationElement([0, 1, 2])
    p = PermutationElement([1, 2, 0])
    assert p.product(identity).permutation == p.permutation
    assert identity.product(p).permutation == p.permutation


def test_permutation_inverse() -> None:
    """Test the inverse operation of permutations."""
    # Test inverse of a simple permutation
    p = PermutationElement([1, 2, 0])
    p_inv = p.inverse()
    assert p_inv.permutation == [2, 0, 1]

    # Test that p * p^(-1) = identity
    identity = PermutationElement([0, 1, 2])
    assert p.product(p_inv).permutation == identity.permutation
    assert p_inv.product(p).permutation == identity.permutation

    # Test inverse of identity
    assert identity.inverse().permutation == identity.permutation


def test_permutation_string_representation() -> None:
    """Test the string representation of permutations."""
    p = PermutationElement([1, 2, 0])
    assert str(p) == "[1, 2, 0]"
