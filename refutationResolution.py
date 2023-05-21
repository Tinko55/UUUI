import sys
from queue import LifoQueue
#https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
#https://www.geeksforgeeks.org/stack-in-python/

def loadingClauses(path):

    list=[]

    with open(path, 'r') as clauses:

        for line in clauses:

            if '#' in line:
                continue
            list.append(line.strip().lower())

    goalState= list[len(list)-1]

    list.remove(goalState)

    return set(list), goalState


def loadingClausesCooking(path):
    list = []

    with open(path, 'r') as clauses:

        for line in clauses:

            if '#' in line:
                continue
            list.append(line.strip().lower())

    return set(list)

def loadingInput(path):

    inputs=[]

    with open(path, 'r') as input:

        for line in input:

            if '#' in line:
                continue
            input=tuple()
            command=line.lower().strip().split(' ')
            clause=' '.join(l for l in command[0:len(command)-1])
            input=(clause, command[-1])
            inputs.append(input)


    return inputs

def plResolve(c1, c2):
    resolvents = set()

    if c1 == '~' + c2 or '~' + c1 == c2:

        resolvents.add('NIL')
        return resolvents

    c1 = c1.split()
    c2 = c2.split()
    resolved=''

    removed=False

    for l in c1:

        if l.startswith('~'):

            temp=l.replace('~', '')

            if  temp in c2:

                c2.remove(temp)

                c1.remove(l)
                removed=True
                break
        elif l != 'v':

            temp='~'+l

            if temp in c2:

                c2.remove(temp)

                c1.remove(l)
                removed = True
                break

    for l in c1:
        resolved = resolved + ' ' + l

    for l in c2:
        resolved = resolved + ' ' + l
    if removed:
        resolvents.add(resolved)

    return resolvents


def NILcheck(resolvents, clauses):

    if 'NIL' in resolvents:
        return True

    for l in resolvents:
        for l2 in clauses:
            l2split=l2.split()
            if len(l2.replace('v','').split())==1:
                if len(l.replace('v','').split())==1:
                    for a in l.split():

                        if a.startswith('~') and a != 'v':

                            temp=a.replace('~', '')

                            if temp in l2split:

                                return True
                        elif a !='v':
                            a = '~' + a
                            temp=a
                            if temp in l2split:
                                return True

    return False

def removeSubsumed(cleanClauses):

    readytoremove=set()

    for clause1 in cleanClauses:

            for clause2 in cleanClauses:

                    setclause1=set(clause1.split())
                    setclause2=set(clause2.split())

                    if setclause1 != setclause2 and setclause1.issubset(setclause2):

                        readytoremove.add(clause2)
                    elif setclause1 != setclause2 and setclause2.issubset(setclause1):

                        readytoremove.add(clause1)

    for clause in readytoremove:
        cleanClauses.remove(clause)

    return cleanClauses

def removeUnnecessary(clauses):

    cleanClauses=set()

    for clause in clauses:

        clause=set(clause.split())

        if len(clause) > 1:
            temp = ''
            tautology = True
            for l in clause:

                if l.startswith('~')  and l != 'v':

                    if l.replace('~', '') in clause:
                        tautology=False
                        break

                elif l != 'v':
                    if ('~' + l) in clause:
                        tautology = False
                        break

                temp=temp+   ' ' + l

            if tautology:
                cleanClauses.add(temp)
        else:
            cleanClauses.add(clause.pop())

    fullyclean=removeSubsumed(cleanClauses)


    return fullyclean


def plResolution(F, G):

    clauses= F

    trueG= G
    isTrue=False

    if len(G.split()) > 2 :

        temp=''
        for l in G.split():

            if 'v' in l:
                continue
            elif '~' in l and l!= ' ':
                temp= temp + l.replace('~', '')
            elif '~' not in l and l!= ' ':
                temp= temp + ' ~' + l

            G=temp
    else:
        temp=''
        if "~" in G:

            temp=G.replace('~', '')
            G=temp
        else:

            temp="~"+G
            G=temp

    sos=set(G.split())

    for l in G.split():
        clauses.add(l)

    new= set()

    originalClauses=clauses.copy()

    usedClauses=LifoQueue()

    closed=set()

    while True:

        clauses.update(new)

        newset = removeUnnecessary(clauses)

        clauses.clear()

        clauses=newset.copy()
        newset.clear()

        for c1 in clauses:
            for c2 in clauses:
                if (c1 in sos or c2 in sos) and c1 != c2:

                    check1 = (c1,c2)
                    check2=(c2,c1)
                    if check1 not in closed and check2 not in closed:

                        resolvents = plResolve(c1, c2)
                        closed.add(tuple([c1,c2]))
                        closed.add(tuple([c2,c1]))

                        res=resolvents.copy()

                        if res !=set():
                            used = (res.pop(), c1, c2)
                            usedClauses.put(used)

                        newset1 = removeUnnecessary(resolvents)

                        resolvents.clear()

                        resolvents = newset1.copy()
                        newset1.clear()

                        if resolvents != set():
                            sos.update(resolvents)

                            newset2 = removeUnnecessary(sos)

                            sos.clear()

                            sos = newset2.copy()
                            newset2.clear()

                            new.update(resolvents)

                            newset3 = removeUnnecessary(new)

                            new.clear()

                            new = newset3.copy()
                            newset3.clear()

                            if resolvents != set():
                                isTrue = NILcheck(resolvents, clauses)

                            if isTrue:

                                for c in originalClauses:
                                    print(c)

                                print('===============')
                                first=True
                                parents=set()
                                child=''
                                used=[]

                                while not usedClauses.empty():

                                    child, p1, p2 = usedClauses.get()

                                    p1clean=''

                                    for l in sorted(p1.split()):

                                        if l!='v':
                                            p1clean +=' ' + l

                                    p2clean = ''
                                    for l in sorted(p2.split()):
                                        if l!='v':
                                            p2clean +=' ' + l
                                    childClean=''
                                    for l in sorted(child.split()):
                                        if l!='v':
                                            childClean +=' ' + l

                                    if childClean in parents or first:

                                        parents.add(p1clean)
                                        parents.add(p2clean)
                                        used.append((childClean,p1clean,p2clean))
                                        first=False

                                for c in reversed(used):

                                    child, p1, p2 = c
                                    print('{0}  ({1}, {2})'.format(child, p1, p2))

                                if 'v' in child:
                                    if '~' in child:
                                        print('NIL ({0}, {1})'.format(child.replace('v','').replace('~',''),child.replace('v','')))
                                    else:
                                        print('NIL ({0}, {1})'.format('~'+child.replace('v', ''),child.replace('v', '')))
                                else:
                                    if '~' in child:
                                        print('NIL ({0}, {1})'.format(child.replace('v', '').replace('~', ''),child.replace('v', '')))
                                    else:
                                        print('NIL ({0}, {1})'.format('~' + child.replace('v', ''), child.replace('v', '')))
                                print('===============')

                                print('[CONCLUSION]: {0} is  {1}'.format(trueG, isTrue))
                                return True

                    else:
                        continue

        if new.issubset(clauses):

            print('[CONCLUSION]: {0} is  {1}'.format(trueG, 'unknown'))
            return False




def cooking(clauses, input):

    for i in input:

        clause, command = i

        temp = clauses.copy()

        if command =='?':
            print('\nUser’s command: {0} ?\n'.format(clause))
            plResolution(temp, clause)

        elif command=='+':
            print('\nUser’s command: {0} +'.format(clause))
            print('add {0} \n'.format(clause))

            temp.clear()
            temp=clauses.copy()
            temp.add(clause)
            clauses.clear()
            clauses=temp.copy()
        elif command=='-':

            if clause in clauses:
                print('\nUser’s command: {0} -'.format(clause))
                print('remove {0}\n'.format(clause))
                temp.clear()
                temp = clauses.copy()
                temp.discard(clause)
                clauses.clear()
                clauses = temp.copy()

def main():

    data= []

    data = sys.argv

    if 'resolution' in data:

        index=  data.index('resolution')

        res= data[index+1]

        clauses, goal= loadingClauses(res)

        plResolution(clauses, goal)

    elif 'cooking' in data:

        index = data.index('cooking')

        clausesfile=data[index+1]

        ordersfile = data[index+2]

        clauses =loadingClausesCooking(clausesfile)

        orders =loadingInput(ordersfile)

        cooking(clauses,orders)

if __name__ == '__main__':
    main()