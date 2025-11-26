import math
import pandas as pd

def load_data():
    # 示例数据：[天气, 温度, 湿度, 有风, 是否打球]
    dataset = [
        ['Sunny', 'Hot', 'High', 'Weak', 'No'],
        ['Sunny', 'Hot', 'High', 'Strong', 'No'],
        ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
        ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
        ['Sunny', 'Mild', 'High', 'Weak', 'No'],
        ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
        ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
        ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
        ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Strong', 'No']
    ]
    labels = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'Play']
    return dataset, labels

def cal_entroy(labels):

    label_dict={}
    for lable in labels:
        if(lable not in label_dict):
            label_dict[lable]=0
        label_dict[lable]+=1
    entroy=0
    for lable in label_dict.keys():
        p=label_dict[lable]/len(labels)
        entroy-=p*math.log(p,2)
    return entroy
def choose_root(dataset):
    entroy=cal_entroy(dataset.iloc[:,-1])
    features=dataset.iloc[:,:-1]
    features_columns=features.columns
    entroy_dict={}
    for feature in features_columns:
        entroy_label=0
        for label in features[feature].unique():
            feature_data=dataset[label==dataset[feature]].iloc[:,-1]
            prob=len(feature_data)/len(features[feature])

            entroy_label+=prob*cal_entroy(feature_data)
        entroy_dict[feature]=(entroy-entroy_label)/splitInfo(dataset[feature])

    max_key=max(entroy_dict.keys(),key=entroy_dict.get)
    return max_key
def splitInfo(dataset):
    split_Info=0
    dict={}
    for data in  dataset:
        dict[data]=dict.get(data,0)+1
    for key in dict.keys():
        p=dict[key]/len(dataset)
        split_Info-=p*math.log(p,2)
    return split_Info

def create_tree(dataset, labels):
    if len(dataset) == 0:
        return None
    if len(labels) == 0:
        return None
    if cal_entroy(dataset.iloc[:,-1]) == 0:
        return dataset.iloc[:,-1].iloc[0]
    root = choose_root(dataset)
    tree = {root: {}}
    for feature in dataset[root].unique():
        tree[root][feature] = create_tree(dataset[dataset[root]==feature].drop(columns=[root]), labels)
    return tree

if __name__ == '__main__':
    dataset, labels = load_data()
    dataset=pd.DataFrame(dataset)
    dataset.columns=labels
    dataset.info()
    tree=create_tree(dataset,labels)
    print(tree)
