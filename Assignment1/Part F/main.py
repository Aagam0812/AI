"""
This module calculates the area of a circle given its radius.
"""

from math import pi

def calculate_circle_area(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.
    
    Args:
        radius (float): The radius of the circle.
    
    Returns:
        float: The area of the circle.
    """
    return pi * radius ** 2

def main() -> None:
    radius: float = 5.0
    area = calculate_circle_area(radius)
    print(f"The area of a circle with radius {radius} is {area:.2f}")

if __name__ == "__main__":
    main()