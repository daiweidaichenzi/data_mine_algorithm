from collections import Counter

import numpy as np


def load_data():
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


def get_neighbor_labels(train_labels, distance_dic, k):
    sorted_distances = sorted(distance_dic.items(), key=lambda x: x[1])
    neighbor_labels = []

    for i in range(k):
        # sorted_distances[i][0] 是训练集中的索引
        train_index = sorted_distances[i][0]
        neighbor_labels.append(train_labels[train_index])

    return neighbor_labels


def cal_distance(dataset, pre_data_list):
    #计算距离的函数可以改变，可以用欧氏距离，曼哈顿距离等，因为我这里的数据集都是字符串，所以我简单的直接比较样本间字符串的相似个数来计算距离（相似度）
    distance_dic = {}
    index=0
    for data in dataset:
        distance=len(data)
        for i in range(len(data)):
            if pre_data_list[i]==data[i]:
                distance-=1
        distance_dic[index]=distance
        index+=1
    return distance_dic


def pre_label(labels_list):
    count_result=Counter(labels_list)
    # print(type(count_result))
    return count_result.most_common(1)[0][0]

def KNN(dataset,labels,k,pre_data_list):
    #计算离数据集中每个样本的距离
    pre_data_y=[]
    for pre_data in pre_data_list:
        distance_dic=cal_distance(dataset,pre_data)
        neighbor_labels = get_neighbor_labels(labels, distance_dic, k)
        pre_y=pre_label(neighbor_labels)
        pre_data_y.append(pre_y)
    return pre_data_y
if __name__ == '__main__':
    dataset, labels_col = load_data()
    dataset = np.array(dataset)
    dataset_feature=dataset[:,:-1]
    labels=dataset[:,-1]
    # print(labels.shape)

    col=KNN(dataset_feature,labels,3,[['Sunny', 'Hot', 'High', 'Weak'],['Sunny', 'Hot', 'High', 'Strong']])
    # pre_label=[]

    for i in range(len(col)):
        print(col[i])

