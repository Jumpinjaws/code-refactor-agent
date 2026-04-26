import os,sys
def calculate(x,y,op):
    if op=='add':
        return x+y
    elif op=='sub':
        return x-y
    elif op=='mul':
        return x*y
    elif op=='div':
        if y==0:
            return None
        return x/y
    else:
        return None

def process_list(lst):
    result=[]
    for i in range(len(lst)):
        if lst[i]>0:
            result.append(lst[i]*2)
    return result

class datamanager:
    def __init__(self):
        self.data={}
    def add(self,k,v):
        self.data[k]=v
    def get(self,k):
        return self.data.get(k,None)
