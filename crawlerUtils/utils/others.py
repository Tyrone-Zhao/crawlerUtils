def index_of_str(s1, s2):
    ''' 索引s2在s1中的位置 '''
    n1=len(s1)
    n2=len(s2)
    for i in range(n1-n2+1):
        if s1[i:i+n2]==s2:
            return i
    else:
            return -1


def index_of_str2(s1, s2):
    ''' 索引s2在s1中的位置 '''
    lt=s1.split(s2,1)
    if len(lt)==1:
        return -1
    return len(lt[0])

