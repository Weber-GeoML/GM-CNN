import pytest
import math
from gmcnn.gm_convolution.conv_utils import (
    get_nbrhood_elements,
    get_neighbor_distances,
    get_central_indices,
)


# Tests for get_nbrhood_elements
def test_get_nbrhood_elements_empty():
    """Test direct product with empty neighborhood."""
    assert get_nbrhood_elements([]) == []


def test_get_nbrhood_elements_single():
    """Test direct product with single element."""
    nbrhood = ["a"]
    assert get_nbrhood_elements(nbrhood) == ["aa"]


def test_get_nbrhood_elements_multiple():
    """Test direct product with multiple elements."""
    nbrhood = ["a", "b"]
    expected = ["aa", "ab", "ba", "bb"]
    assert sorted(get_nbrhood_elements(nbrhood)) == sorted(expected)


# Tests for get_neighbor_distances
def test_get_neighbor_distances_cyclic():
    """Test distance computation for cyclic group."""
    group = "cyclic"
    order = 4
    distances = get_neighbor_distances(group, order)

    # Check structure
    assert isinstance(distances, list)
    assert all(isinstance(d, tuple) and len(d) == 2 for d in distances)
    assert all(isinstance(d[0], float) and isinstance(d[1], tuple) for d in distances)

    # Check center point
    center = (order // 2, order // 2)
    assert center == (2, 2)

    # Check if distances are sorted
    assert all(
        distances[i][0] <= distances[i + 1][0] for i in range(len(distances) - 1)
    )


def test_get_neighbor_distances_dihedral():
    """Test distance computation for dihedral group."""
    group = "dihedral"
    order = 4
    distances = get_neighbor_distances(group, order)

    # Check structure
    assert isinstance(distances, list)
    assert len(distances) == (order * 2) * (order * 2)  # Size of dihedral group

    # Check center point
    center = (order, order)
    assert center == (4, 4)

    # Check if distances are sorted
    assert all(
        distances[i][0] <= distances[i + 1][0] for i in range(len(distances) - 1)
    )


def test_get_neighbor_distances_invalid_group():
    """Test with invalid group type."""
    group = "invalid"
    order = 4
    result = get_neighbor_distances(group, order)
    assert result is None


# Tests for get_central_indices
def test_get_central_indices_cyclic():
    """Test central indices for cyclic group."""
    group = "cyclic"
    order = 4
    out_channels = 2

    indices = get_central_indices(group, order, out_channels)

    assert isinstance(indices, list)
    assert len(indices) == out_channels
    assert all(isinstance(idx, str) for idx in indices)
    assert all("mod" in idx for idx in indices)


def test_get_central_indices_dihedral():
    """Test central indices for dihedral group."""
    group = "dihedral"
    order = 4
    out_channels = 2

    indices = get_central_indices(group, order, out_channels)

    assert isinstance(indices, list)
    assert len(indices) == out_channels
    assert all(isinstance(idx, str) for idx in indices)


def test_get_central_indices_out_channels():
    """Test with different numbers of output channels."""
    group = "cyclic"
    order = 4

    # Test with out_channels = 1
    indices_1 = get_central_indices(group, order, 1)
    assert len(indices_1) == 1

    # Test with out_channels = order
    indices_n = get_central_indices(group, order, order)
    assert len(indices_n) == order


@pytest.mark.parametrize(
    "out_channels,order",
    [
        (1, 2),
        (2, 4),
        (4, 8),
    ],
)
def test_get_central_indices_parametrized(out_channels, order):
    """Test with different combinations of out_channels and order."""
    for group in ["cyclic", "dihedral"]:
        indices = get_central_indices(group, order, out_channels)
        assert len(indices) == out_channels


def test_get_central_indices_large():
    """Test with larger group order."""
    group = "cyclic"
    order = 16
    out_channels = 8

    indices = get_central_indices(group, order, out_channels)
    assert len(indices) == out_channels
    # Check that indices are unique
    assert len(set(indices)) == out_channels
