import itertools
from random import shuffle

def color_vertices(edges):
    '''
    takes a list of edges, and returns a list of sets of vertices which are not adjacent

    This randomizes the set of edges in order to get better results.
    See https://en.wikipedia.org/wiki/Greedy_coloring for more information.

    TODO: find a minimal library that does something better than greedy
    '''
    smallest_coloring = None
    for _ in range(10):
        shuffle(edges)
        res = list(color_vertices_greedy(edges))
        if smallest_coloring is None or len(res) < smallest_coloring:
            smallest_coloring = res
    return smallest_coloring

def color_vertices_greedy(edges):
    done = set()
    vertices = set(itertools.chain(*edges))
    colored_set = set()
    while vertices:
        added = False
        for v in vertices:
            safe = True
            for e in edges:
                e = set(e)
                if v in e and any(existing in e for existing in colored_set):
                    safe = False
            if safe:
                colored_set.add(v)
                vertices.remove(v)
                added = True
                break
        if not added:
            yield colored_set
            colored_set = set()
    if colored_set:
        yield colored_set


if __name__ == '__main__':
    edges = [[1, 2], [2, 6], [6, 14], [14, 11], [11, 3], [3, 8], [8, 13], [13, 9], [9, 15], [15, 4], [4, 16], [16, 7], [7, 5], [5, 12], [12, 10], [10, 1]]
    for vertices in color_vertices(edges):
        print(vertices)

