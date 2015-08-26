sets = {}

def make(x):
        global sets
        sets[x] = set([x])

def find_(sets,x):
        for id,s in sets.items():
                if x in s:
                        return id

def find(x):
        """wrapper for find_"""
        global sets
        return find_(sets,x)

def union(p,q):
        """combines a and b"""
        global sets

        a,b = normalise(find(p),find(q))
        if a != b:
                sets[a] |= sets[b]
                del sets[b]

neq   = set()
equiv = set()
path  = set()
dfa   = {}

# (idm L1.1)
def normalise(p,q):
        return (p,q) if p<q else (q,p)

def set_make():
        return set()

def set_insert(v,s):
        s.add(v)

def set_remove(v,s):
        s.remove(v)

def set_search(v,s):
        return v in s

def set_elements(s):
        return s

def equiv_p(p,q):
        """tests equivalence of p and q"""
        global neq, equiv, path, dfa, verbose
        d = dfa

        if (p,q) in neq:
                return False

        if set_search((p,q),path):
                return True

        set_insert((p,q),path)

        for a in d['Sigma']:

                (p_,q_) = normalise(find(d['delta'](p,a)),find(d['delta'](q,a)))

                if p_ != q_ and not set_search((p_,q_),equiv):
                        set_insert((p_,q_),equiv)

                        if not equiv_p(p_,q_):
                                return False
                        else:
                                set_remove((p_,q_),path)

        set_insert((p,q),equiv)

        return True

def joinstates(d,classes):
        """returns new dfa based on equivalence classes"""

        Q = set(classes.keys())
        Sigma = d['Sigma']
        delta = lambda p,a: find_(classes,d['delta'](p,a))
        q0 = find_(classes,d['q0'])
        F = set(map(lambda x: find_(classes,x),list(d['F'])))

        return {'Q':Q,'Sigma':Sigma,'delta':delta,'q0':q0,'F':F}


def min_incr(d):
        global neq, equiv, path, dfa
        dfa = d

        for q in d['Q']:
                make(q)

        neq = set([normalise(p,q) for p in d['F'] for q in d['Q'] - d['F']])

        for p in d['Q']:
                for q in [x for x in d['Q'] if x > p]:
                        if (p,q) in neq:
                                continue

                        if find(p) == find(q):
                                continue

                        equiv = set_make()
                        path  = set_make()

                        if equiv_p(p,q):
                                for (p_,q_) in set_elements(equiv):
                                        union(p_,q_)
                        else:
                                neq |= path

        classes = {}
        for p in d['Q']:
                lider = find(p)
                classes[lider] = classes[lider] | set([p]) if lider in classes else set([p])


        return joinstates(d,classes)

def printdfa(name,d):
        print(name)
        print('Q    : {0}\nSigma: {1}\ndelta:'.format(d['Q'],d['Sigma']))
        for q,a in [(q,a) for q in d['Q'] for a in d['Sigma']]:
                print(q,a,d['delta'](q,a))
        print('q0   : {0}\nF    : {1}\n'.format(d['q0'],d['F']))


def dfa_01_d(p,a):
        tab = {
                0:{'a':1,'b':2},
                1:{'a':4,'b':2},
                2:{'a':3,'b':2},
                3:{'a':4,'b':0},
                4:{'a':4,'b':4}}

        return tab[p][a]

dfa_01 = {'Q':set([0,1,2,3,4]),'Sigma':set(['a','b']),'delta':dfa_01_d,'q0':0,'F':set([4])}

if __name__ == '__main__':
        printdfa('Input',dfa_01)
        dfa_01_min = min_incr(dfa_01)
        printdfa('Output',dfa_01_min)
