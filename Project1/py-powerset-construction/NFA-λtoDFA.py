#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    NFA-λtoDFA.py: Convert NFA-λ to DFA using powerset construction.
    Copyright (C) 2012  Jeremy W. Murphy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
    This program is dedicated to my excellent Computing Theory lecturer of
    2012, Dr Sebastian Sardina.

    It implements algorithms from Languages and Machines, 3rd ed., 2006,
    Thomas Sudkamp.
"""

import sys
from Queue import *

try:
    from pydot import *
except ImportError:
    print '(IMPORT ERROR) Required module missing: pydot.'
    sys.exit(1)
try:
    import networkx as nx
except ImportError:
    print '(IMPORT ERROR) Required module missing: NetworkX.'
    sys.exit(1)



VERSION = "1.0.0 beta 2"

lambda_symbol = 'λ'
separator = ', '
# If you don't have Computer Modern Unicode, you are missing out!
# Look for it as cm-unicode in your package directory.
FONTNAME_NODE = 'CMU Serif bold'
FONTNAME_EDGE = 'CMU Serif italic'
CHARSET = 'UTF8'
RANKDIR = 'LR'



# Calculate the transitive closure of node N in graph G, for edges containing symbol.
def transitive_closure(G, N, symbol, closure):
    closure.add(N)
    for node in G[N]:
        if node not in closure:
            # print(N, node)
            for edge in G[N][node]:
                if symbol in G[N][node][edge]['label']:
                    transitive_closure(G, node, symbol, closure)
                    break


# Return λ-closure(N).
# input = G : NetworkX graph, N : NetworkX node, LAMBDA : optionally specify the lambda symbol.
# output = set()
def lambda_closure(G, N, LAMBDA='λ'):
    if N not in G:
        raise RuntimeError('Node {} is not in graph {}!'.format(N, G))
    closure = set()
    transitive_closure(G, N, LAMBDA, closure)
    return frozenset(closure)


def decorate_start(Node):
    Node['fillcolor'] = 'black'
    Node['style'] = 'filled'
    Node['fontcolor'] = 'white'


def decorate_final(Node):
    Node['peripheries'] = 2


# Format the set S as a name.
def name(S):
    result = '{' + ', '.join(str(e) for e in sorted(S)) + '}'
    # print 'DEBUG: name("{}"): "{}"'.format(S, result)
    return result


# Input transition function t creates the DFA transition table from an NFA-λ
def input_transition(G, Sigma, LAMBDA='λ'):
    if len(G.nodes()) == 0:
        raise RuntimeError('input_transition({}, {}): Graph is empty!'.format(G, Sigma))

    t = dict()
    for node in G.nodes():
        t[node] = dict()
        closure = lambda_closure(G, node, LAMBDA)
        for symbol in Sigma:
            t[node][symbol] = set()
            for node2 in closure:
                for target_node in G[node2]:
                    if target_node not in t[node][symbol]:
                        for edge in G[node2][target_node]: # In case the input digraph is not strict.
                            if symbol in G[node2][target_node][edge]['label']:
                                t[node][symbol] |= lambda_closure(G, target_node)
            # Finally, make it a frozen set to enforce semantics and be hashable.
            t[node][symbol] = frozenset(t[node][symbol])
            # print('t(): {}[{}]: {}'.format(node, symbol, t[node][symbol]))
    return t


# It's no heap sort...
def insert_sorted(s, c):
    result = separator.join(str(i) for i in sorted(s.split(separator) + [c]))
    # print 'DEBUG: insert_sorted("{}", {}): "{}"'.format(s, c, result)
    return result


# powerset_construction() creates the DFA from the transition table t
# Nodes are given a 'data' field with their pretty name for later use.
def powerset_construction(t, q0_closure, Sigma):
    if len(t) == 0:
        raise RuntimeError('powerset_construction(): transition table empty!')
    if len(q0_closure) == 0:
        raise RuntimeError('powerset_construction(): start closure empty!')

    Qprime = nx.DiGraph()
    Qprime.add_node(q0_closure, data=name(q0_closure))
    frontier = Queue()
    frontier.put(q0_closure)

    while not frontier.empty():
        X = frontier.get(False)
        # print 'X: {}'.format(name(X))
        for a in Sigma:
            Y = set()
            for N in X:
                Y |= t[N][a]
            Y = frozenset(Y)
            # print '{} -{}-> {}'.format(name(X), a, name(Y))
            if Y not in Qprime.nodes():
                frontier.put(Y)
                Qprime.add_node(Y, data=name(Y))
            if X in Qprime and Y in Qprime[X]:
                Qprime[X][Y]['label'] = insert_sorted(Qprime[X][Y]['label'], a)
            else:
                Qprime.add_edge(X, Y, label=a)

    return Qprime


def rebuild_pretty(Qprime, q0_closure, F):
    # Qprime.node[q0_closure]['start'] = 1

    for N in Qprime.nodes():
        # if N & F:
            # Qprime.node[N]['final'] = 1
        if len(N) == 0:
            Qprime.node[N]['data'] = '∅'

    # Rebuild the graph with pretty names for the nodes.
    # TODO: I expect there is a better (faster) way to do this integrated with the main loop, but I need better Python skills to do it.
    G = nx.DiGraph()
    G.graph['node'] = dict()
    G.graph['node']['fontname'] = FONTNAME_NODE
    G.graph['edge'] = dict()
    G.graph['edge']['fontname'] = FONTNAME_EDGE
    G.graph['rankdir'] = RANKDIR
    # Add in the nodes, adding graphviz formatting for start and final states.
    for N in Qprime.nodes(data=True):
        pretty_name = N[1]['data']
        G.add_node(pretty_name)
        if N[0] & F:
            decorate_final(G.node[pretty_name])
        if N[0] == q0_closure:
            decorate_start(G.node[pretty_name])
    # Add in the edges.
    for E in Qprime.edges(data=True):
        G.add_edge(Qprime.node[E[0]]['data'], Qprime.node[E[1]]['data'], label=E[2]['label'])

    return G


# DOT files often have everything in quotes, which just get in the way.
def remove_quotes(G, quotes='\'"'):
    for n,nbrs in G.adjacency_iter():
        for nbr,eattr in nbrs.items():
            for edge in eattr:
                label = eattr[edge]['label']
                if label[0] == label[-1] and label[0] in quotes:
                    new_label = label[1:-1]
                    # print 'DEBUG:'. label, '=>', new_label
                    G[n][nbr][edge]['label'] = new_label


# NFA_parameters() returns a tuple containing Σ, q0 and F.
# Σ is constructed by adding every encountered edge symbol and discarding λ at the end.
# q0 requires a node with the 'start' attribute.
# F is constructed by adding every node with the 'final' attribute.
def NFA_parameters(NFA):
    if len(NFA.nodes()) == 0:
        raise RuntimeError('ERROR: NFA_parameters({}): Empty graph!'.format(NFA))
    Sigma = set()
    F = set()
    q0 = None

    for N in NFA.nodes():
        if 'final' in NFA.node[N]:
            F.add(N)
        if 'start' in NFA.node[N]:
            q0 = N
        for N2 in NFA[N]:
            for edge in NFA[N][N2]:
                Sigma |= frozenset(NFA[N][N2][edge]['label'].split(separator))

    Sigma.discard(lambda_symbol)

    if len(Sigma) == 0:
        print('WARNING: Automaton has no input alphabet!  This is theoretically possible but probably an error.')

    if q0 == None:
        raise RuntimeError('ERROR: Automaton does not have a start state!')

    if len(F) == 0:
        raise RuntimeError('ERROR: Automaton has no final states!')

    # print 'NFA_parameters:', Sigma, q0, F
    return frozenset(Sigma), q0, frozenset(F)


def main(*args):
    if len(args) != 3:
        print 'Usage: {} <input file> <output file>'.format(args[0])
        return 2

    try:
        NFA = nx.read_dot(args[1])
    except IOError:
        print '{}: file does not exist or is not readable.  Terminating.'.format(args[1])
        return 3

    remove_quotes(NFA)

    Sigma, q0, F = NFA_parameters(NFA)

    # for node in NFA.nodes(data=True):
        # print('{}'.format(node))
    # for edge in NFA.edges(data=True):
        # print edge
    t = input_transition(NFA, Sigma)
    # print '*** input_transition() result ***'
    # for node in sorted(t):
        # print('{} {}'.format(node, t[node]))
    q0_closure = lambda_closure(NFA, q0)
    DFA = powerset_construction(t, q0_closure, Sigma)
    DFA = rebuild_pretty(DFA, q0_closure, F)
    # print '=== powerset_construction() results ==='
    # for node in DFA.nodes(data=True):
        # print('{}'.format(node))
    # for edge in DFA.edges(data=True):
        # print edge

    DFAdot = nx.to_pydot(DFA)
    DFAdot.set_rankdir(RANKDIR)
    DFAdot.set_charset(CHARSET)
    try:
        DFAdot.write(args[2])
    except IOError:
        print '{}: IO error writing file.  Terminating.'.format(args[2])
        return 3

    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
