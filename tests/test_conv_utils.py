import pytest
import sys
import os

# Add explicit imports
from gmcnn.gm_convolution.conv_utils import generate_neighborhood
from gmcnn.group_element.cyclic_group_element import CyclicGroupElement


def test_cyclic_group_n2_t1():
    """
    Test neighborhood generation for cyclic group of order 2 with t=1.
    This should generate elements: [-1, 0, 1] which map to [1, 0, 1] in Z_2
    """
    # Arrange
    group = "cyclic"
    n = 2  # Order of the group
    t = 1  # Range around zero

    # Act
    neighborhood = generate_neighborhood(group, n, t)

    # Assert
    expected = [
        CyclicGroupElement(-1, 2).__str__(),  # Maps to 1 in Z_2
        CyclicGroupElement(0, 2).__str__(),  # Maps to 0 in Z_2
        CyclicGroupElement(1, 2).__str__(),  # Maps to 1 in Z_2
    ]
    assert neighborhood == expected
    assert len(neighborhood) == 3


def test_cyclic_group_n4_t1():
    """
    Test neighborhood generation for cyclic group of order 4 with t=1.
    This should generate elements: [-1, 0, 1] which map to [3, 0, 1] in Z_4
    """
    # Arrange
    group = "cyclic"
    n = 4
    t = 1

    # Act
    neighborhood = generate_neighborhood(group, n, t)

    # Assert
    expected = [
        CyclicGroupElement(-1, 4).__str__(),  # Maps to 3 in Z_4
        CyclicGroupElement(0, 4).__str__(),  # Maps to 0 in Z_4
        CyclicGroupElement(1, 4).__str__(),  # Maps to 1 in Z_4
    ]
    assert neighborhood == expected
    assert len(neighborhood) == 3


def test_cyclic_group_t0():
    """
    Test neighborhood generation with t=0, which should only return the identity element.
    """
    # Arrange
    group = "cyclic"
    n = 4
    t = 0

    # Act
    neighborhood = generate_neighborhood(group, n, t)

    # Assert
    expected = [CyclicGroupElement(0, 4).__str__()]
    assert neighborhood == expected
    assert len(neighborhood) == 1
