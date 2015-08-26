#All code programmed by Michael Mo
#NFA is the input set
#DFA is the output set
#3 stands for lambda
#In the set of NFA and DFA, the first element is the set of all transition fuctions
#The second set is the start state
#The third set is the final state
#The forth set is the sigma
#The fifth set is the states

DFA = [[],[],[],[],[]]
def methodTwo(list):
    tempList = []
    for i in list:
        if not i in tempList:
            tempList.append(i)
    return tempList
def starteclosure(a,b):
        #print a[0]
        for element in a[0]:
                if (element[0][0]==b and element[1][0]=='3'):
                        DFA[1].insert(0,element[2][0])
                        DFA[1].insert(0,b)
                        starteclosure(a,element[2][0])
                        DFA[1] = methodTwo(DFA[1])
        #print a

NFA = [[[['q0'],'0',['q1']],
                [['q0'],'3',['q3']],
                [['q1'],'1',['q4']],
                [['q1'],'3',['q5']],
                [['q2'],'3',['q0']],
                [['q2'],'0',['q4']],
                [['q3'],'0',['q5']],
                [['q3'],'0',['q2']],
                [['q3'],'3',['q5']],
                [['q4'],'3',['q5']]],['q0'],['q5'],['0','1'],['q0','q1','q2','q3','q4','q5']]

starteclosure(NFA,NFA[1][0])
sigma = NFA[3]
DFA[0]=[[DFA[1]]]
DFA[0].insert(1,DFA[0][0])
print DFA
DFA[0][0].insert(1,'0')
DFA[0][0].insert(2,[])
#DFA[0][1].insert(1,'1')
#DFA[0][1].insert(2,[])
for a in sigma:
        for b in DFA[1]:
                for c in NFA[0]:
                        if (c[0][0]==b and c[1]==a):
                                DFA[0][0][2].insert(2,c[2][0])
                                

#for a in NFA[0]:
           # if(a[0][0]=='q0'and a[1]=='3'):
#                
#                DFA[1]=a[0]+a[2]
  #              DFA[0].insert(0,DFA[1])
#                for b in DFA[0][0]:
#                    #print b
#                    for c in NFA[0]:
#                        #print c[0][0]
#                        if (c[1]!='3' and (b==c[0][0])):
#                            print "end"
#                    #if (b==)
                    #print b
                #print (DFA[1])
                #print (DFA)
            #print(a[2])
print DFA
#MDFA = [[[['q0','q3'],'0',['q1','q2','q4']],
#         [['q0','q3'],'1',['q0','q1','q2','q5']],
#         [['q1','q2','q3','q4'],'0',['q0','q1','q4','q5']],
#         [['q1','q2','q3','q4'],'1',['q1','q5']]],
#        ['q0','q3'],
#        [['q0','q1','q2','q5'],['q0','q1','q4','q5'],['q1','q5']],
#        ['1','2','3'],
#        [['q0','q1','q2','q5'],['q0','q1','q4','q5'],['q1','q5'],['q1','q2','q3','q4'],['q0','q3'],['q1','q2','q4']]]
