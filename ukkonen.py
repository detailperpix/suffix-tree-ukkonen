"""
ukkonen.py

Name: Wirmantono

Linear-time Suffix tree creation based on Ukkonen's algorithm
Implementation are based on algorithm in the lecture slides provided by the
Unit Coordinator for the Algorithms unit on my institution.
Details were omitted to prevent academic integrity breach.
"""

CHAR_RANGE = ord('~') - ord('$') + 1


class Node:
    """
    Base class for Node, to be extended to Root, InnerNode or LeafNode
    Node class has an array to store references to other nodes
    the attribute start and end will be used by InnerNode and LeafNode
    as the edge that represent the suffix range.
    """
    def __init__(self, start, end):
        self.links = [None] * CHAR_RANGE
        self.start = start
        self.end = end

    def get_end(self):
        return self.end

    def get_start(self):
        return self.start


class Root(Node):
    """
    Represents the Root node of the suffix tree,
    has its a suffix link to itself
    """
    def __init__(self):
        super().__init__(-1, 0)
        self.suffix_link = self


class InnerNode(Node):
    """
    Represents the Inner Node in the tree, linking between an inner node /
    root node towards a leaf node / inner node
    """
    def __init__(self, start=-1, end=0, active_node=None, suffix_link=None):
        super().__init__(start, end)
        self.suffix_link = suffix_link
        self.active_node = active_node


class LeafNode(Node):
    """
    LeafNode represents the end of each branch in the suffix tree
    """
    def __init__(self, start=-1, end=-1, active_node=None):
        super().__init__(start, end)
        self.links = None
        self.active_node = active_node

    def get_end(self):
        return self.end[0]


class SuffixTree:
    def __init__(self, text):
        self.root = None
        self.text = text
        self.global_end = [-1]
        self.construct_tree()

    def get_char_id(self, char_pos):
        """
        Function for getting the index for traversing the links
        :param char_pos: position of the character in the text
        """
        return ord(self.text[char_pos]) - ord('$')

    def construct_tree(self):

        def start_tree(start):
            """
            Prepare traversal from root, traverse if branch exists,
            otherwise create a LeafNode and traverse into it
            :param start: the first index of current suffix
            """
            node = self.root
            curr_char = self.get_char_id(start)
            if node.links[curr_char] is None:
                """    
                Rule 2:
                Create new leaf node and assign a link to the root node
                Assign range for the new LeafNode
                """
                node.links[curr_char] = LeafNode(start, self.global_end)
                node = node.links[curr_char]
                node.active_node = self.root
                start = i + 1
            else:
                """
                If leaf exists, go to the node
                """
                node = node.links[curr_char]
            return node, start

        def create_inner_node():
            """
            Create a new inner node from an edge, also resolve the links
            from previous nodes and assigning suffix link if applicable
            """
            def add_suffix_link():
                link_to_root = dest_link_to_root
                if link_to_root:
                    node.suffix_link = node_link
                    link_to_root = False
                else:
                    if node_pos == j - 1:
                        node_link.suffix_link = node
                link = node
                link_pos = j
                return link_to_root, link, link_pos
            node = current
            dest_link_to_root = link_incoming_to_root
            node_link = suffix_link_node
            node_pos = suffix_link_text_pos
            start, end = node.get_start(), node.get_end()

            if node.links is None:
                """
                Case where current Node is a LeafNode:
                - Create new leaf node
                - convert current node into intermediate
                - create another leaf node for new character
                """
                curr_char = self.get_char_id(start)
                node.active_node.links[curr_char] = InnerNode(start,
                                                              start + max(i_ptr - 1, 0),
                                                              node.active_node)
                node = node.active_node.links[curr_char]
                dest_link_to_root, node_link, node_pos = add_suffix_link()
                # Create branch for existing range
                curr_char = self.get_char_id(start + i_ptr)
                node.links[curr_char] = LeafNode(start + i_ptr,
                                                 self.global_end,
                                                 node)
            elif start + i_ptr <= end_pos:
                """
                Case for creating inner node in between another inner node
                - Create an inner node
                - change the active node pointer towards the inner node
                - modify the range of the previous inner node
                """
                curr_char = self.get_char_id(start)
                active_node = node.active_node
                active_node.links[curr_char] = InnerNode(start,
                                                         start + max(i_ptr - 1, 0),
                                                         active_node)

                temp_ptr = node
                node = node.active_node.links[curr_char]
                curr_char = self.get_char_id(start + i_ptr)
                node.links[curr_char] = temp_ptr
                temp_ptr.start = start + i_ptr
                temp_ptr.end = end

                # add suffix link if applicable
                dest_link_to_root, node_link, node_pos = add_suffix_link()
            return node, dest_link_to_root, node_link, node_pos

        def traverse_node():
            """
            traverse_node invoked when the current edge range has been exhausted
            and will change the node into the next node based on matching
            the pattern
            """
            node = current
            start = node.get_start()
            iptr = i_ptr
            if node.links is not None:
                offset = max(pos, start + iptr)

                next_char = self.get_char_id(offset + 1)

                """
                move to edge if it exists
                otherwise create a new LeafNode
                """
                if node.links[next_char] is not None:
                    node = node.links[next_char]
                else:
                    node.links[next_char] = LeafNode(pos + 1,
                                                     self.global_end,
                                                     node)
                    temp_ptr = node
                    node = node.links[next_char]
                    node.active_node = temp_ptr
                    node.end = self.global_end
                    if suffix_link_node is not None \
                            and suffix_link_text_pos == j - 1 \
                            and not link_incoming_to_root:
                        suffix_link_node.suffix_link = node.active_node
                iptr = -1
            return node, iptr

        def skip_count():
            """
            Perform skip count optimization by skipping comparison
            that can be performed, once it is not possible to skip
            return to comparison in the main loop
            """
            node = current
            new_pos = pos
            skip_value = skipped_value
            skip = False
            end = node.get_end()
            start = node.start
            if skip_count_range > 0:
                skip_value += (end - start + 1)
                # if possible to skip go to next edge
                if skip_count_range > skip_value:
                    # check if there is an edge leading to the next node
                    next_char = self.get_char_id(min(n - 1,
                                                     pos
                                                     + max(skip_value - 1,
                                                           1)))
                    if node.links is not None \
                            and node.links[next_char] is not None:
                        new_pos = pos + max((skip_value - 1), 1)
                        node = node.links[next_char]
                        skip = True
                    else:
                        """
                        Once we cannot jump any further because of leafnode
                        progress through the comparison
                        """
                        new_pos = min(n - 1, pos)
            return node, new_pos, skip_value, skip

        def traverse_suffix_link():
            """
            traverse the suffix link and handles the creation of LeafNode
            if the node does not have branch leading to the node after traversal
            """
            curr = current
            if curr.active_node is self.root:
                offset = 1
            else:
                offset = 0
            j_ptr = j + 1
            iptr = 0
            start = curr.get_start()
            if curr.active_node is self.root:
                curr_pos = j_ptr + iptr - 1
            else:
                curr_pos = start - 1
            skip_range = 0
            skip_value = 0
            curr_char = self.get_char_id(curr_pos + 1)
            temp_ptr = curr
            curr = curr.active_node.suffix_link
            if curr.links[curr_char] is not None:
                curr = curr.links[curr_char]
                iptr = -1
                """
                Calculate the skippable comparison
                """
                skip_range = temp_ptr.get_end() - temp_ptr.start - offset + 1
            else:
                curr.links[curr_char] = LeafNode(curr_pos + offset,
                                                 self.global_end,
                                                 curr)
                curr = curr.links[curr_char]
                iptr += 1
                curr_pos += 1
            return curr, iptr, j_ptr, curr_pos, skip_range, skip_value

        text = self.text
        n = len(text)
        self.root = Root()
        i = 0
        last_j = -1

        # boolean to check if there is incoming suffix link for root
        link_incoming_to_root = True
        suffix_link_text_pos = -1
        while i < n:
            # begin phase i + 1
            j = last_j + 1
            suffix_link_node = None
            self.global_end[0] += 1
            while j < (i + 1):

                current, pos = start_tree(j)
                """
                Add pointer for assigning suffix link towards root
                if no inner node has been created yet
                """
                if link_incoming_to_root:
                    suffix_link_node = self.root
                    suffix_link_text_pos = j

                i_ptr = 0
                skip_count_range = 0
                skipped_value = 0
                while pos < i + 1:
                    """
                    Current point should be at either LeafNode or Inner Node
                    If at LeafNode, links should be None
                    then extends the range (Rule 2)
                    If at intermediate Node, links shouldn't be None
                    Check range first, if range exceeds then move to next node
                    If mismatch, prepare to create a new node 
                    """
                    # extract node range
                    start_pos, end_pos = current.get_start(), current.get_end()

                    """
                    Perform skip count optimisation, if applicable
                    """
                    current, pos, skipped_value, skipped = skip_count()
                    if skipped:
                        continue
                    else:
                        skip_count_range = 0
                        skipped_value = 0

                    """
                    Compare text in the range
                    if equal continue comparison until j / pos runs out of range
                    if j runs out of range: apply rule 3 (no changes required)
                    if pos runs out of range: apply rule 2 (extends the range)
                    """
                    if text[pos] != text[start_pos + i_ptr]:
                        """
                        Mismatch occurs, create new LeafNode and current Node
                        is converted into intermediate node
                        """
                        current, link_incoming_to_root, \
                        suffix_link_node, suffix_link_text_pos = \
                            create_inner_node()

                        # Create new branch by adding LeafNode
                        current_char = self.get_char_id(pos)
                        current.links[current_char] = LeafNode(pos,
                                                               self.global_end,
                                                               current)
                        # current.links[current_char].active_node = current

                        # modify current node's range
                        # current.start = start_pos + i_ptr
                        # current.end = end_pos #  + max(i_ptr - 1, 0)

                        current = current.links[current_char]

                        # update last_j
                        last_j += 1
                        i_ptr = 0
                    else:
                        """
                        Check if range exceeded the end for current substring
                        """
                        if pos > i - 1 and pos > end_pos:
                            """
                            Prepare to traverse the suffix link if it exists
                            """
                            if current.active_node.suffix_link is not None \
                                    and current.links is None:
                                """
                                Based on the rule that if the active node suffix 
                                link is pointing to the root node and the active 
                                node is the root node, we must remove the first 
                                character from the remainder before traversing
                                """
                                current, i_ptr, j, pos, skip_count_range, \
                                skipped_value = traverse_suffix_link()
                        elif start_pos + i_ptr + 1 > end_pos:
                            # move to next node
                            current, i_ptr = traverse_node()
                        elif pos == i:
                            """
                            Rule 3 require a little more than nothing
                            inc. Showstopper Rule
                            """
                            if suffix_link_node is not None \
                                    and suffix_link_text_pos == j - 1 \
                                    and not link_incoming_to_root:
                                link_ptr = current.active_node
                                suffix_link_node.suffix_link = link_ptr
                            j = i

                    i_ptr += 1
                    pos += 1
                if suffix_link_text_pos != j:
                    suffix_link_node = None
                    suffix_link_text_pos = -1
                j += 1
            # reset suffix_link_node
            i += 1
