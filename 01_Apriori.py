"""
实现Apriori算法
在给定最小支持度（support)和最小置信度(confidence)的前提下
先找到数据中的频繁项集（频繁项集的支持度大于最小支持度）
写出这些频繁项集的非空真子集
计算子集（x）->全集去除子集的剩余部分（y）的置信度（support（y and x）/support（x）
与置信度比较，如果大于最小置信度就是强关联规则
"""
import string
from itertools import combinations


def get_frequent_itemfrozensets(items,new_list,min_support):
    support_list = {}
    for item in items:
        support=0
        for d in new_list:
            if(item.issubset(d)):
                support+=1
        support_list[item]=support
    filter_support={}
    for item,item_support in support_list.items():
        if(item_support>=min_support):
            filter_support[item]=item_support
    return filter_support


def has_infrequent_subset(new_itemset, L_K_1):
    #combinations作用是生产指定长度的所有组合，参一：可迭代对象，参二：组合的长度
    for subset in combinations(new_itemset,len(new_itemset)-1):
        if(frozenset(subset) not in L_K_1):
            return True
    return False

def join(L_K_1,k):
    C_k=set()
    list_L=list(L_K_1)
    for i in range(len(list_L)):
        for j in range(i+1,len(list_L)):
            i_list=sorted(list_L[i])
            j_list=sorted(list_L[j])

            if(i_list[:k-2]==j_list[:k-2]):
                new_itemset=list_L[i].union(list_L[j])
                #剪枝，k项候选项的任何k-1子集都是频繁子集，还有一点
                #任何非频率子集的超集都是非频繁子集
                if  not has_infrequent_subset(new_itemset,L_K_1):
                    C_k.add(new_itemset)
    return C_k

def pre_processing(items):
    new_list=[]
    for item in items:
        #item[0]是因为item本身是一个list，从list中取出第一个字符串
        new_list.append(frozenset(item[0].strip().split(',')))
    return new_list


def find_strong_rules( min_confidence,All_Frequent_Itemfrozensets):
    strong_rules={}
    for item,value in All_Frequent_Itemfrozensets.items():
        if(len(item)<2):
            continue
            #包左不包右
        for i in range(1,len(item)):
            for data in combinations(item,i):
                data_frozenset=frozenset(data)
                if data_frozenset in All_Frequent_Itemfrozensets:
                    confidence=All_Frequent_Itemfrozensets[item]/All_Frequent_Itemfrozensets[data_frozenset]
                    if(confidence>=min_confidence):
                     strong_rules[data_frozenset,item-data_frozenset]=confidence

    return strong_rules


def apriori(data,min_support,min_confidence):
    #将['a,b,c','b,c']->[''a','b','c'',''b','c'']
    new_list=pre_processing(data)

    C_1=set()
    for transaction in new_list:
        for item in transaction:
            # 这里使用frozenset不用set的原因是：
            # frozenset可以作为dict中的key，set作为可变集合，不能作为key
            C_1.add(frozenset([item]))
    L_1=get_frequent_itemfrozensets(C_1,new_list,min_support)
    All_Frequent_Itemfrozensets={}
    All_Frequent_Itemfrozensets.update(L_1)

    L_K_1=L_1.keys()
    k=2

    while L_K_1:
        C_K=join(L_K_1,k)
        L_K=get_frequent_itemfrozensets(C_K,new_list,min_support)

        if(L_K is not None):
            All_Frequent_Itemfrozensets.update(L_K)
            k+=1
            L_K_1=L_K.keys()
        else:
            break



    #计算这些频繁项集的最大项（他不是任何其他频繁项集的真子集）
    strong_rules=find_strong_rules(min_confidence,All_Frequent_Itemfrozensets)
    # for item,value in strong_rules.items():
    #     print(item,value)
    return strong_rules

if __name__ == '__main__':
    list_input=[['1,2,5'],['2,4'],['2,3'],['1,2,3,5'], ['1,2,3']]
    frequent_itemsets=apriori(list_input,3,0.5)
    for item,value in frequent_itemsets.items():
        a,b=item
        a_str=','.join(sorted(list(a)))
        b_str=','.join(sorted(list(b)))

        print(f'{a_str}->{b_str} confidence={value}')
