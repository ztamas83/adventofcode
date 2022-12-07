from tools import get_data
from aocd import submit
import re
from collections import OrderedDict as od
from anytree import Node
import sys

indata = get_data(7, 2022)

FS_SIZE = 70000000
REQ_SIZE = 30000000

fs_items: dict[str, tuple[Node, int]] = {}

def is_cmd(line): return line.startswith('$')

def get_full_path(node: Node):

    return '/'.join(map(lambda p: p.name, node.path)).replace('//', '/')


def draw_tree(data) -> dict[str, dict | list]:
    root = Node('/')
    fs_items['/'] = (root, 'dir')
    currentdir : Node = None
    ls_cmd = False
    for line in data:
        line = line.strip()
        if cmd := re.match('\\$ cd (.*)', line):
            if currentdir and not cmd.group(1) in ['..', '/']:
                targetfolder = (get_full_path(currentdir) + '/' + cmd.group(1)).replace('//', '/')
            else:
                targetfolder = cmd.group(1)
            match targetfolder:
                case '..':
                    currentdir = currentdir.parent
                case '/':
                    currentdir = root
                case other:
                    currentdir = fs_items.get(targetfolder)[0]
        elif line == '$ ls':
            ls_cmd = True
        elif ls_cmd:
            if is_cmd(line):
                ls_cmd = False
                pass
            
            (s, name) = tuple(line.split(' '))
            file = Node(name, parent=currentdir)
            fs_items[get_full_path(file)] = (file, s)

def calc_size(node: Node) -> tuple[Node, int]:
    dirsize = 0
    full_path = get_full_path(node)
    if node.is_leaf: #it's a file
        dirsize = int(fs_items.get(full_path)[1])
    else:
        for child in node.children:
            childpath = get_full_path(child)
            if fs_items.get(childpath)[1].isnumeric():
                size = fs_items.get(childpath)[1]
                dirsize += int(size)
                print(f'|_{childpath}: {int(size)} (file)')
            else:
                (_, child_size) = calc_size(child)
                dirsize += child_size
                print(f'|_{childpath}: {child_size} (dir)')
    
    print(f'Fullsize: {get_full_path(node)}: {dirsize}')
    return (node, dirsize)

def total_size(max_size = sys.maxsize):
    total = 0
    for item in fs_items:
        (node, size) = calc_size(fs_items[item][0])
        fs_items[item] = (node, size)
        if size <= max_size:
            total += size

    return total

def dir_size_to_delete() -> int:
    total_size()
    
    space_needed = REQ_SIZE - (FS_SIZE - fs_items['/'][1])
    sort = sorted(fs_items.items(), key=lambda d: d[1][1], reverse=False)
    
    for (path, (node, size)) in sort:
        if size >= space_needed:
            return size
        

# draw_tree(indata)

# assert(total_size(100000) == 95437)

# directories.clear()
# dir_sizes.clear()

indata = get_data(7,2022, True)

draw_tree(indata)

# answer_a = total_size()
answer_b = dir_size_to_delete()
print(answer_b)
#submit(answer_a, part='a', day=7, year=2022)
submit(answer_b, part='b', day=7, year=2022)