# suffix-tree-ukkonen
Python implementation of Ukkonen's linear-time suffix tree creation algorithm.
Ukkonen's algorithm provide a fast suffix tree creation using optimization rules 
to achieve linear-time amortized complexity. The original paper for the algorithm is in
https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf. I have also referred to 
https://stackoverflow.com/a/9513423/414272 and lecture slides provided in the algorithm class 
of my institution.

# Usage instruction
To use this suffix tree, simply import the SuffixTree class and provide string as 
argument when instantiating the SuffixTree.

```
from ukkonen import SuffixTree
tree = SuffixTree("mississippi")
```

## Traversing tree
When traversing the tree, it would begin from the root.
The root will contain a link array which contains references
to the children nodes.
```
# ensure tree has been creaed
current = tree.root
# loop link list
link = current.links
for i in range(len(current.links)):
    if link[i] is not None:
        # do something
```
Once we have gone through the root, the program
needs to iterate through edge. The edge
contains information of the index in the string.
To access this range use:
```
start, end = node.get_start(), node.get_end()
```

# About
The implementation is tested to run on Python 3.8.5