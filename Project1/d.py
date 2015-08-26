group = [[0 for col in range(7)] for row in range(7)]
a=[[[0 for col in range(3)] for row in range(7)]for Z in range(7)]
a[1][2][0]=3
a[2][4][0]=1
a[2][3][0]=2
a[3][6][2]=1
a[1][5][2]=1
print a

group[1][1]=1

count=2
groupnumber=1
       
for i in range(row):  
        for j in range(col):
            for q in range(Z):
                 if a[i][q][j]==3:
                     if i==1:
                         group[groupnumber][count]=q
                         count=count + 1

for i in range(row):
        count=1
        groupnumber=groupnumber+2
        for j in range(Z):
            if group[i][j]!=0:                
                #print group[i][j],i,j
                for e in range(col):
                   for f in range(Z):
                       if a[group[i][j]][f][e]==2: 
                          group[groupnumber][count]=q
                          count=count + 1
                       if a[group[i][j]][f][e]==1:
                          group[groupnumber-1][count]=q
                          count=count + 1


group[1][1]=1
group[1][2]=2
group[2][1]=3
group[3][1]=5
group[3][2]=4
group[4][1]=6
#print group

#print 1,2,0,1,"\n"
#print 2,3,2,2,"\n"
#print 2,4,2,2,"\n"                                                                                                       

DFA= [[[0 for col in range(3)] for row in range(5)]for Z in range(5)]
DFA[1][2][0]=1
DFA[2][3][2]=2
DFA[2][4][2]=2


for x in range(5):
   for y in range(5):
     for z in range(3):
      if DFA[x][y][z]!=0:
         if z==0:
                 for x in range(4):
                   for y in range(4):
                     if DFA[x][y][z]!=0: 

                                      break

groupdfa = [[[0 for col in range(6)] for row in range(6)]for Z in range(6)]


count=1
groupnumber=1
accept=1
for x in range(5):
   for y in range(5):
     for z in range(3):
             if DFA[x][y][z]!=0:
                       groupdfa[groupnumber][count][accept]=y
             else:
                   groupnumber=2
                   accept=0
                   groupdfa[groupnumber][count][accept]=y



count=1
groupnumber=2
accept=1
group=0
 
for x in range(5):
   for y in range(5):
     for z in range(3):
             if DFA[x][y][z]!=1:
 #                      groupdfa[groupnumber][count][accept]=y
                       group=1;
             if DFA[x][y][z]!=2:
                   groupnumber=groupnumber+1
                   accept=0
                   #groupdfa[groupnumber-1][count-1][accept-1]=y
                   group=0;

                   



               


                    

                      

                    


