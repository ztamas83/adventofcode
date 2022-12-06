from aocd import get_data as aocd_gd
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_data(day:int, year:int, remote:bool = False) -> list[str]:
    """Return daily puzzle input"""
    if remote:
        return aocd_gd(day=day, year=year).splitlines()
    
    with open(os.path.join(__location__, f'input_{year}_{day}.txt'), 'r') as f:
        lines = f.readlines()
        if "\n" in lines:
            return lines.splitlines()
        return lines
