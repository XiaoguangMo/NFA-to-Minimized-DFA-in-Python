#All the codes below is programmed by Moxiaoguang (Michael)1030300036 and I haven't 
#reference any other people's code. So if there is any other code looks like mine, it 
#must be other people copy my code!
#
#All the code's code is UTF-8
#
#
#Scanner
#Change the name of sample and sample1 to change the input string
sample="{basic id;If (id>=5) id=65;else id=75;While (id<=1000 && id>10)Id=id*2;}"
sample1="{basic id1,id2;If (id1==5) id1=65;else id2=75;id3=id1+5*6+id2+id1;id4=true && false && 3<5;}"
out=[]
for each in sample:
    if(each.isspace()==1):
        out.append(each)
    if(each=="|" and len(out)>0 and out[len(out)-1]=="|"):
        out[len(out)-1]+=(each)
    elif(each=="&" and len(out)>0 and out[len(out)-1]=="&"):
        out[len(out)-1]+=(each)
    elif(each=="=" and len(out)>0 and (out[len(out)-1]=="=" or out[len(out)-1]=="!" or out[len(out)-1]=="<" or out[len(out)-1]==">")):
        out[len(out)-1]+=(each)
    elif(each.isspace()==0 and each.isalpha()==0 and each.isdigit()==0):
        out.append(each)

    elif(each.isalpha()==1 or each.isdigit()==1):
        if(((each.isalpha()==1 or each.isdigit()==1) and len(out)>0 and (out[len(out)-1].isalpha()==1 or out[len(out)-1].isdigit()==1))):
            out[len(out)-1]+=(each)
        else:
            out.append(each)
for each in out:
    if(each==" "):
        out.remove(each)
print("------------------Scanner------------------")
print(out)

#Parsing table
#stat is the given LL(1) grammar
stat=[["program","block"],["block","{","decls","stmts","}"],["decls","decls","decl"],["decls","lambda"],["decl","type","id",";"],["type","type","[","num","]"],["type","basic"],["stmts","stmts","stmt"],["stmts","lambda"],["stmt","loc","=","bool",";"],["stmt","if","(","bool",")","stmt"],["stmt","if","(","bool",")","stmt","else","stmt"],["stmt","while","(","bool",")","stmt"],["stmt","do","stmt","while","(","bool",")",";"],["stmt","break",";"],["stmt","block"],["loc","loc","[","bool","]"],["loc","id"],["bool","bool","||","join"],["bool","join"],["join","join","&","&","equality"],["join","equality"],["equality","equality","=","=","rel"],["equality","equality","!","=","rel"],["equality","rel"],["rel","expr","<","expr"],["rel","expr","<","=","expr"],["rel","expr",">","=","expr"],["rel","expr",">","expr"],["rel","expr"]
      ,["expr","expr","+","term"],["expr","expr","-","term"],["expr","term"],["term","term","*","unary"],["term","term","/","unary"],["term","unary"],["unary","!","unary"],["unary","-","unary"],["unary","factor"],["factor","(","bool",")"],["factor","loc"],["factor","num"],["factor","real"],["factor","true"],["factor","false"]]
#ter is the terminal in the grammar
ter=["lambda","{","}","[","]","(",")","id","num","basic","if","while","do","break","||","&&",">",">=","<=","<","+","-","*","/","!","==","!=","real","true","false","else",";"]
parse=[]
import string
limitation = list(string.ascii_letters + string.digits)
count=0
while(count<len(out)):
    if(out[count].isdigit()==1):
        out[count]="num"
    elif(out[count]!="if" and out[count]!="while" and out[count]!="else" and out[count]!="do" and out[count]!="break" and out[count]!="real" and out[count]!="true" and out[count]!="false" and out[count]!="basic" and len(out[count]) == len([ i for i in out[count] if i in limitation ])):
        out[count]="id"
    count+=1
print("----------------Convert to Alphabet form-----------------")
print(out)

#remove dulplicate elements
first=[]
for each in stat:
    first.append([each[0]])
temp = []
[temp.append(i) for i in first if not i in temp]
first=temp

#get nullable states
count=0
nullable=[]
while(count<len(stat)):
    for each in stat:
        if each[1]=="lambda":
            nullable.append(each[0])
        if(len(each)==2 and (each[1] in nullable)):
            nullable.append(each[0])
    count+=1
temp = []
[temp.append(i) for i in nullable if not i in temp]
nullable=temp
#print("---------------nullable-----------")
#print(nullable)


#get First table

#This is the first loop, compute all the first value when the first value is terminal
count=0
while(count<len(stat)):
    if(stat[count][1] in ter):
        countt=0
        while(countt<len(first)):
            if(first[countt][0]==stat[count][0]):
                first[countt].append(stat[count][1])
            countt+=1
    count+=1

#This is the second loop, compute all the first value when the first value is not terminal
countall=0
while(countall<10):
    count=0
    while(count<len(stat)):
        countt=1
        while(countt<len(stat[count])):
            if(stat[count][countt] in ter):
                countt=len(stat[count])
            elif(stat[count][countt] not in nullable):
                counta=0
                while(counta<len(first)):
                    if(first[counta][0]==stat[count][0]):
                        countb=0
                        while(countb<len(first)):
                            if(first[countb][0]==stat[count][countt] and counta!=countb):
                                countc=1
                                while(countc<len(first[countb])):
                                    first[counta].append(first[countb][countc])                    
                                    countc+=1
                            countb+=1
                    counta+=1
                countt=len(stat[count])
            countt+=1
        count+=1
    countall+=1
temp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
count=0
while(count<len(first)):
    for each in first[count]:
        if(each not in temp[count]):
            temp[count].append(each)
    count+=1
first=temp

#Print First Table in a nice form
print("-----------------First Table-----------------------")
for each in first:
    temp="First("+each[0]+")={"
    count=1
    temp2=""
    while(count<len(each)):
        temp2+=each[count]+","
        count+=1
    if(len(temp2)>0):
        temp2=(temp2[:-1])
    temp+=temp2+"}"
    print(temp)
print(first)


#Follow
follow=[]
for each in stat:
    follow.append([each[0]])
temp = []
[temp.append(i) for i in follow if not i in temp]
follow=temp
#give the start state a dollar
follow[0].append("dollar")
#The first loop, compute all the follow value is terminal
count=0
while(count<len(stat)):
    if(len(stat[count])>2 and (stat[count][len(stat[count])-1] in ter) and (stat[count][len(stat[count])-2] not in ter)):
        countt=0
        while(countt<len(follow)):
            if(follow[countt][0]==stat[count][len(stat[count])-2]):
                follow[countt].append(stat[count][len(stat[count])-1])
            countt+=1
    elif(len(stat[count])>2 and (stat[count][len(stat[count])-2] not in ter) and (stat[count][len(stat[count])-1] not in ter) and (stat[count][len(stat[count])-1] not in nullable)):
        countt=0
        while(countt<len(follow)):
            if(follow[countt][0]==stat[count][len(stat[count])-2]):
                counta=0
                while(counta<len(first)):
                    if(first[counta][0]==stat[count][len(stat[count])-1]):
                        countb=1
                        while(countb<len(first[counta])):
                            follow[countt].append(first[counta][countb])
                            countb+=1
                    counta+=1
            countt+=1
    count+=1
#The second loop, compute all the follow value is not terminal
countall=0
while(countall<3):
    count=0
    while(count<len(stat)):
        if(stat[count][len(stat[count])-1]not in ter):
            counta=0
            while(counta<len(follow)):
                if(follow[counta][0]==stat[count][len(stat[count])-1]):
                    countb=0
                    while(countb<len(follow)):
                        if(follow[countb][0]==stat[count][0]):
                            countc=1
                            while(follow[countb][0]!=follow[counta][0] and countc<len(follow[countb])):
                                follow[counta].append(follow[countb][countc])
                                countc+=1
                        countb+=1
                counta+=1
        count+=1
    countall+=1

temp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
count=0
while(count<len(follow)):
    for each in follow[count]:
        if(each not in temp[count]):
            temp[count].append(each)
    count+=1
follow=temp
#print(follow)

#Print Follow Table
print("-----------------Follow Table-----------------------")
for each in follow:
    temp="Follow("+each[0]+")={"
    count=1
    temp2=""
    while(count<len(each)):
        temp2+=each[count]+","
        count+=1
    if(len(temp2)>0):
        temp2=(temp2[:-1])
    temp+=temp2+"}"
    print(temp)

#Parsing Table
print("---------------Parsing Table-------------------------")
#All the attribute involved in this grammar
attribute=[]
count=0
while(count<len(first)):
    counta=0
    while(counta<len(first[count])):
        if(first[count][counta] in ter):
            attribute.append(first[count][counta])
        counta+=1
    count+=1
    
count=0
while(count<len(follow)):
    counta=0
    while(counta<len(follow[count])):
        if(follow[count][counta] in ter):
            attribute.append(follow[count][counta])
        counta+=1
    count+=1
temp = []
[temp.append(i) for i in attribute if not i in temp]
attribute=temp
attribute.remove("lambda")
attribute.append("dollar")
print(attribute)

#Start parsing
parsing=[]
#Add the first column
for each in stat:
    parsing.append([[each[0]]])
temp = []
[temp.append(i) for i in parsing if not i in temp]
parsing=temp
count=0
while(count<len(parsing)):
    counta=0
    while(counta<19):
        parsing[count].append("[]")
        counta+=1
    count+=1
#print(parsing)

#Add all the valid first value which is terminal 
count=0
while(count<len(parsing)):
    counta=0
    while(counta<len(attribute)):
        countb=0
        while(countb<len(first)):
            countc=1
            while(countc<len(first[countb])):
                
                if(first[countb][0]==parsing[count][0][0] and first[countb][countc]==attribute[counta]):
                    countd=0
                    while(countd<len(stat)):
                        temp=""
                        
                        if(stat[countd][0]==first[countb][0] and stat[countd][1]==first[countb][countc]):
                            counte=1
                            while(counte<len(stat[countd])):
                                temp+=stat[countd][counte]
                                temp+=" "
                                parsing[count][counta+1]=temp
                                counte+=1
                        countd+=1

                countc+=1
            countb+=1
        counta+=1
    count+=1
count=0
#Add all the valid first value which is not terminal
while(count<len(parsing)):
    counta=0
    while(counta<len(attribute)):
        countb=0
        while(countb<len(first)):
            countc=1
            while(countc<len(first[countb])):
                
                if(first[countb][0]==parsing[count][0][0] and first[countb][countc]==attribute[counta]):
                    countd=0
                    while(countd<len(stat)):
                        if(stat[countd][0]==parsing[count][0][0] and (stat[countd][1] not in ter) and (stat[countd][1] not in nullable)):
                            counte=1
                            while(counte<len(first)):
                                countf=0
                                while(countf<len(first[counte])):
                                    if(first[counte][0]==stat[countd][1] and first[counte][countf]==attribute[counta]):
                                        countg=1
                                        temp=""
                                        while(countg<len(stat[countd])):
                                            temp+=stat[countd][countg]
                                            temp+=" "
                                            parsing[count][counta+1]=temp
                                            countg+=1
                                    countf+=1
                                counte+=1
                        elif(stat[countd][0]==parsing[count][0][0] and len(stat[countd])==3 and (stat[countd][1] not in ter) and (stat[countd][1] in nullable)):
                            counte=1
                            while(counte<len(first)):
                                countf=0
                                while(countf<len(first[counte])):
                                    if(first[counte][0]==stat[countd][2] and first[counte][countf]==attribute[counta]):
                                        countg=1
                                        temp=""
                                        while(countg<len(stat[countd])):
                                            temp+=stat[countd][countg]
                                            temp+=" "
                                            parsing[count][counta+1]=temp
                                            countg+=1
                                    countf+=1
                                counte+=1
                        countd+=1

                countc+=1
            countb+=1
        counta+=1
    count+=1


#Add all the follow value
count=0
while(count<len(parsing)):
    counta=0
    while(counta<len(attribute)):
        countb=0
        while(countb<len(first)):
            countc=1
            while(countc<len(first[countb])):
                if(first[countb][countc]=="lambda"):
                    countd=0
                    while(countd<len(follow)):
                        counte=0
                        while(counte<len(follow[countd])):
                            if(first[countb][0]==parsing[count][0][0] and follow[countd][counte]==attribute[counta]):
                                parsing[count][counta+1]="lambda"
                            counte+=1
                        countd+=1
                countc+=1
            countb+=1
        counta+=1
    count+=1
#Print Parsing Table
#print(attribute)
for each in parsing:
    print(each)

print("----------------------Parsing--------------------------")
print("TBC")




