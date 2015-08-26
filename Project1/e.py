def fst(p):
    return p[0]

def snd(p):
    return p[1]

def fn_dom(F):
    return {k for k in F.keys()}

def fn_range(F):
    return {v for v in F.values()}

def mk_dfa(Q, Sigma, Delta, q0, F):
    assert(Sigma != {})

    assert("" not in Sigma)
    dom = fn_dom(Delta)
    states_dom = set(map(fst,dom))
    input_dom = set(map(snd,dom))
    state_targ = set(fn_range(Delta))
    assert(states_dom == Q)
    assert(input_dom == Sigma)
    assert(len(Delta)==len(Q)*len(Sigma))
    assert((state_targ <= Q)&(state_targ != {}))
    assert(q0 in Q)

    assert(set(F) <= Q)
    return({"Q":Q, "Sigma":Sigma, "Delta":Delta, "q0":q0, "F":F})

def mkp_dfa(Q, Sigma, Delta, q0, F):
    assert(Sigma != {})
    assert(q0 in Q)

    assert(set(F) <= Q)
    return({"Q":Q, "Sigma":Sigma, "Delta":Delta, "q0":q0, "F":F})


Q1 = {'S0','S1'}
Sigma1 = {'a','b'}
Delta1 = {('S0', 'a'): 'S0', ('S1', 'a'): 'S0', ('S1', 'b'): 'S1', ('S0', 'b'): 'S1'}
q01 = 'S0'
F1 = {'S1'}
DFA1 = mk_dfa(Q1,Sigma1,Delta1,q01,F1)

assert(DFA1 == {'Q': {'S1', 'S0'}, 'q0': 'S0', 'F': {'S1'}, 'Sigma': {'a', 'b'}, 'Delta': {('S0', 'a'): 'S0', ('S1', 'a'): 'S0', ('S1', 'b'): 'S1', ('S0', 'b'): 'S1'}})

def mktot(D):
    """ Given a partially specified DFA, make it total by transitioning to state BH wherever undefined.
    """
    add_delta = { (q,c) : "BH" for q in D["Q"] for c in D["Sigma"] if (q,c) not in D["Delta"] }

    bh_moves =  { ("BH", c): "BH" for c in D["Sigma"] }
    
    add_delta.update(bh_moves)

    add_delta.update(D["Delta"])
    
    return {"Q": D["Q"] | { "BH" }, "Sigma": D["Sigma"], "q0": D["q0"], "F": D["F"], "Delta": add_delta}

assert(mktot(DFA1) == {'Q': {'S1', 'S0', 'BH'}, 'q0': 'S0', 'Delta': {('S0', 'a'): 'S0', ('BH', 'a'): 'BH', ('S1', 'a'): 'S0', ('S1', 'b'): 'S1', ('S0', 'b'): 'S1', ('BH', 'b'): 'BH'}, 'Sigma': {'a', 'b'}, 'F': {'S1'}})
             
assert(mktot(mktot(DFA1)) == mktot(DFA1))


def prdfa(D):
        """Prints the DFA neatly.
        """
        Dt = mktot(D)
        print("")
        print("Q:", Dt["Q"])
        print("Sigma:", Dt["Sigma"])
        print("q0:", Dt["q0"])
        print("F:", Dt["F"])
        print("Delta:")
        print("\t".join(map(str,Dt["Q"])))
        print("----------------------------------------------------------------------------------------")
        for c in (Dt["Sigma"]):
            nxt_qs = [Dt["Delta"][(q, c)] for q in Dt["Q"]]
            print("\t".join(map(str, nxt_qs)) + "\t" + c)
            print("")

def step_dfa(D, q, c):
    """Run DFA D from state q on character c. Return the next state.
    """
    assert(c in D["Sigma"])
    assert(q in D["Q"])
    return D["Delta"][(q,c)]

def run_dfa(D, q, s):
    """Run DFA D from state q on string S. Return the next state. We run DFAs to run on "" also (empty).
    """
    # Don't run DFAs on empty strings
    return q if s=="" else run_dfa(D, step_dfa(D, q, s[0]), s[1:])

def accepts(D, q, s):
    """ Checks for DFA acceptance.
    """
    return run_dfa(D, q, s) in D["F"]

def in_arrows(D, q):
    """ Given a DFA D and a state q, return the set of states feeding into q,
        along with the symbol labeling the move, as a dict. Does not include q.
    """
    return dict([(a1,q1) for a1 in D["Sigma"] for q1 in D["Q"] if ((q1 != q) & (q==step_dfa(D, q1, a1))) ])

def out_arrows(D, q):
    """ Given a DFA D and a state q, return the set of states feeding out of q,
        along with the symbol labeling the move, as a dict. Does not include q.
    """
    return dict([(a1,q1) for a1 in D["Sigma"] for q1 in D["Q"] if ((q1 != q) & (q1==step_dfa(D, q, a1))) ])

def self_arrows(D, q):
    """ in_arrows for the case that the move is from q.
    """
    return dict([(a1,q) for a1 in D["Sigma"] if q == step_dfa(D, q, a1)])

assert(in_arrows(DFA1,'S0') == {'a': 'S1'})

assert(out_arrows(DFA1, 'S0') == {'b': 'S1'})

assert(self_arrows(mktot(DFA1), 'BH') == {'a': 'BH', 'b': 'BH'})

def map_eps_to_visible(L):
    return list(map(lambda x: 'EPS' if x=='' else x, L))

def mush_self_loops(arrows):

    labels = { re for re in arrows.keys() }
    if (labels == set()):  
        return ""
    else:
        labels_vis = map_eps_to_visible(list(labels))
        return "(" + (" + ".join(labels_vis)) + ")" + "* "

def combine_alt(Existing, New):
    return ( 'EPS' + " + " + New  ) if Existing == '' else (  Existing + " + " + New  )
    
def comb_if_exists(key, New, Existing):
    return combine_alt(Existing[key], New[key]) if key in Existing else New[key]

def form_path_re(a1, self_re, a2):
    """Any one of the args could be empty. If non-empty a1/a2, bracket. Then concatenate.
    """
    if ((a1=="") & (a2=="")):
        return self_re
    elif (a1==""):
        return self_re + " ("+a2+") "
    elif (a2==""):
        return " ("+a1+") " + self_re
    else:
        return " ("+a1+") " + self_re + " ("+a2+") "
    
def new_edges_after_elim(D, q):
    self_a = self_arrows(D, q)
    self_re = mush_self_loops(self_a)
    Just_the_new_edges = { (q1,q2) :  form_path_re(a1, self_re, a2)
                           for a1, q1 in in_arrows(D,q).items() for a2, q2 in out_arrows(D,q).items()
                           if (q1 != 'BH') & (q2 != 'BH') }
    Just_the_new_edges_from_to = list(Just_the_new_edges.keys())

    Existing_par_edges = { (q1, q2) : x for ((q1, x), q2) in D["Delta"].items() if (q1,q2) in Just_the_new_edges_from_to }
    return dict(map(lambda x:
                        ((x[0], comb_if_exists(x, Just_the_new_edges, Existing_par_edges)), x[1]),
                    Just_the_new_edges.keys())
                )
    
    
def mk_gnfa(D):
    GNFA_delta = { ("Real_I","") : D["q0"] }

    GNFA_delta.update({ (f, "") :"Real_F" for f in D["F"] })
    GNFA_delta.update(D["Delta"])
    return { "Q" : (D["Q"] | {"Real_I"} | {"Real_F"}),
             "Sigma" : D["Sigma"] | {""},
             "Delta" : GNFA_delta,
             "q0" : "Real_I",
             "F" : {"Real_F"} }

GNFA1 = mk_gnfa(DFA1)


def del_state_from_gnfa(D, q):
    print("**** Eliminating state ****")
    
    Delta_increment = new_edges_after_elim(D, q)
    Delta_increment_from_to = { (frm, to) for ((frm, x), to) in set(Delta_increment.items()) }
    
    
    Sigma_increment = { x for ((frm, x), to) in Delta_increment.items()
                        if (frm != "BH") & (frm != q) & (to != "BH")  & (to != q)  }
    
    Old_Sigma_survivors = { x for ((frm, x), to) in D["Delta"].items()
                            if (frm != "BH") & (frm != q) & (to != "BH")  & (to != q)  }
    new_Sigma = Old_Sigma_survivors | Sigma_increment
    
    new_Q = D["Q"] - {q}

    Old_Delta_survivors = { (frm, c) : to for ((frm, c), to) in D["Delta"].items()
                            if ( ((frm, to) not in Delta_increment_from_to)
                                 & (frm in new_Q) & (frm != q)
                                 & (to in new_Q)  & (to != q)
                                 & (c in new_Sigma) ) }

    Old_Delta_survivors.update(Delta_increment)
    
    print(mkp_dfa(new_Q, new_Sigma, Old_Delta_survivors, D["q0"], D["F"]))
    return mkp_dfa(new_Q, new_Sigma, Old_Delta_survivors, D["q0"], D["F"])

def mk_testDtoR2():
    Q = {'S0','S1', 'S2', 'S3'}
    Sigma = {'a','b', 'c', 'd', 'e', 'f', 'g'}
    Delta = {('S0', 'a'): 'S1',
             ('S1', 'b'): 'S1',
             ('S1', 'c'): 'S3',
             ('S3', 'd'): 'S1',
             ('S1', 'e'): 'S2',
             ('S2', 'f'): 'S3',
             ('S0', 'g'): 'S2'}
    q0 = 'S0'
    F = {'S2', 'S3'}
    return mkp_dfa(Q, Sigma, Delta, q0, F)

Dt2 = mktot(mk_gnfa(mk_testDtoR2()))
dd2 = del_state_from_gnfa(Dt2, 'S3')
dd3 = del_state_from_gnfa(mktot(dd2), 'S1')
dd4 = del_state_from_gnfa(mktot(dd3), 'S0')
dd5 = del_state_from_gnfa(mktot(dd4), 'S2')
prdfa(dd5)
