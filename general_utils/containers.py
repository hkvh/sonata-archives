#!/usr/bin/env python
import collections
from collections import Counter, defaultdict
from typing import Tuple


class CounterDict(Counter):
    """
    Subclasses collection's Counter dict "Counter" to add functionality that I feel it should have (like quickly
    deleting all 0 element counts)
    """

    @classmethod
    def fromkeys(cls, iterable, v=None):
        return super().fromkeys(cls, iterable)

    def delete_zero_counts(self):
        """
        The default counter will add things with 0 counts to the dict and have it display when printing most_common
        This method deletes all of those with 0 counts, so that we don't need to worry about adding things with a
        count of 0
        """
        for el in [el for el, count in self.items() if count == 0]:
            del self[el]

    def most_common(self, n=None):
        """
        Overrides most_common to delete zero_counts first
        """
        self.delete_zero_counts()
        return super().most_common()

    def total_count(self):
        """
        A useful method that computes the total_count of all elements in the counter
        :return: the total count of items in the dict
        """
        return sum([count for count in self.values()])


class Multimap(collections.Mapping):
    """
    This Multimap is a wrapper of the defaultdict(set) to be a bit more convenient:

    1. It properly does not consider any sets of length 0 as being not in the dict  (see __contains__ for details)

    2. It contains an as_list_of_tuples method that converts it from the multimap format into a list of tuples
    for ease of inserting into a database

    This class is leveraged heavily be the user hierarchy and is extended to the two classes
    UserEmailToUserIdsMultimap and UserConciseHierarchyDirectedGraph

    It is an extension of mapping, not mutable mapping, because it is designed to be created as blank and added to
    with its add method.
    """

    def __init__(self):
        """
        Construct an empty multimap as a default dict with a set
        """
        self.mmap = defaultdict(set)

    def __len__(self):
        """Overrided to use contains to not include null"""
        return len([x for x in self])

    def __getitem__(self, key):
        """Just returns the set at a given key... If key missing, will return the empty set, as desired"""
        return self.mmap[key]

    def __contains__(self, m):
        """Overwrite contains to return false if our map's set is empty"""
        return len(self.mmap[m]) != 0
        # this is otherwise a quirk with defaultdict:
        # if 'a' is not in dict d, then `'a' in d` would return False unless you at some point queried d['a'] at which
        # point it would return True forever. We don't want that, so this makes it always return False if its set
        # is empty.

    def __repr__(self):
        """Return a printout of the dict"""
        string = "\n"
        for key in self.keys():
            string = string + "{:50}\t{}\n".format("'" + key + "':", self[key])
        return string

    def __iter__(self):
        """Iterates over the underlying dict mmap but uses our new contains to ignore keys referring to 0 length sets"""
        for key in set(self.mmap.keys()):
            if key in self:  # use new __contains__ method that ignores 0-length sets that mmap would include by default
                yield key
        # Note that the set around self.mmap.keys is very necessary so that you won't get a
        # it will give you a Runtime error for changing the size of it while iterating,
        #
        # You may think you'd want this error because you shouldn't be changing the size of something while iterating
        # but bizarrely because of the default dict implementation, simply checking for something not in the dict
        # actually is changing its size (adding an empty set which we then ignore). So it's better to freeze the keys
        # of the dict and iterate through those frozen keys

    def add_key_value_pair(self, key_value_pair: Tuple) -> None:
        """
        The main add method, takes a key_value pair and adds to the multimap.

        :param key_value_pair: a (key, value) tuple where we will add the value to the key's set
        """
        key, value = key_value_pair
        self.mmap[key].add(value)

    def as_list_of_tuples(self):
        """
        Converts our multimap into a list of tuple pairs (i.e. for inserting into sql) by converting the n values
        mapped to each key as n tuples of (key1, val1), (key1, val2) ... (key1, valn), etc.

        :return: our dict as a list of tuples
        """
        return [(key, value) for key in self for value in self[key]]


if __name__ == '__main__':
    a = Counter(a=1, b=20, c=3, d=0)
    print(a.most_common())
    a = CounterDict(a=1, b=20, c=3.2, d=0)
    print(a.most_common())
    print(a.total_count())
    print("\n\n")
    b = Multimap()
    b.add_key_value_pair(('bob', 'b'))
    b.add_key_value_pair(('bob', 'c'))
    b.add_key_value_pair(('jim', 'j'))
    print('bob' in b)
    print(len(b.mmap))
    print(len(b))
    print(b.mmap)
    print(b)

    print('a' in b)  # When using a key not in the mmap
    print(len(b.mmap))
    print(len(b))
    print(b.mmap)
    print(b)  # notice how 'a' is not in b but it is in b.mmap

    print(b.as_list_of_tuples())
