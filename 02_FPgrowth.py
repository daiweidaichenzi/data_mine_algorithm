"""
模拟FPgrowth算法
算法步骤
先计算一项集，然后按照支持度降序排序，将支持度小于min_support的项集删除
将剩余的项集按一项集排序顺序排序，然后构建FP树，
对FP树中的每个项，从根节点开始，将项的路径添加到树中，
如果项已经存在于树中，将项的支持度加1，
否则，创建一个新节点，将项添加到节点中，支持度设为1

从支持度最小的节点从下向上查找，查找从根节点到此节点的路径，找出他的全部前缀路径
计算这些前缀路径中，一项集的支持度，构造新的FP树，
"""
from mimetypes import inited


class FPTreeNode:
    def __init__(self,item_name,count,parent_node):
        self.item_name = item_name
        self.count = count
        self.parent_node = parent_node
        self.children = {}
        self.node_link=None#指向相同项名的节点


def load_data():
    return [
        ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
        ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
        ['b', 'f', 'h', 'j', 'o', 'w'],
        ['b', 'c', 'k', 's', 'p'],
        ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
    ]
def pre_processing(items):
    new_list=[]
    for item in items:
        #item[0]是因为item本身是一个list，从list中取出第一个字符串
        new_list.append(frozenset(item))
    return new_list


def cal_1items(new_list, min_support):
    C_1 = {}
    for item in new_list:
        for data in item:
            C_1[data] = C_1.get(data, 0) + 1
    C_tmp = {}
    for data in C_1.keys():
        if min_support <= C_1[data]:
            C_tmp[data] = C_1[data]

    L_1 = sorted(C_tmp.items(), key=lambda x: (-x[1], x[0]))
    return L_1
def find_prefix_path(node):
    path=[]
    while node.parent_node and node.parent_node.item_name!='null':
        path.append(node.parent_node.item_name)
        node=node.parent_node
        #反转路径
    return path[::-1]

def build_fptree(data, header_table, sorted_frequent_items):
    frequent_item_dict=dict(sorted_frequent_items)

    root=FPTreeNode('null',1,None)

    for transcation in data:
        filtered_sorted_frequent_items=[item for item in transcation if item in frequent_item_dict]
        filtered_sorted_frequent_items.sort(key=lambda item:(frequent_item_dict[item],item),reverse=True)

        current_node=root
        for item in filtered_sorted_frequent_items:
            if item not in current_node.children:
                new_node=FPTreeNode(item,1,current_node)
                current_node.children[item]=new_node

                if item not in header_table:
                    header_table[item]=[frequent_item_dict[item],new_node]
                #找到当前项的最后一个节点
                else:
                    last_node=header_table[item][1]
                    while last_node.node_link is not None:
                        last_node=last_node.node_link
                    last_node.node_link=new_node
                current_node=new_node
            else:
                current_node= current_node.children[item]
                current_node.count+=1
    return root,header_table


def mine_fp_tree(header_table, min_support, pre_pattern, frequent_patterns):
    # 根据支持度从低到高遍历头指针表
    sorted_items = sorted(header_table.keys(), key=lambda x: header_table[x][0])

    for item in sorted_items:

        support = header_table[item][0]
        # 生产新的频繁项集
        new_pattern = frozenset(pre_pattern.union({item}))
        frequent_patterns[new_pattern] = support

        # 构建条件模式基
        conditional_pattern_base = []

        node = header_table[item][1]
        while node is not None:
            prefix_path = find_prefix_path(node)
            if prefix_path:  # 确保路径不为空
                conditional_pattern_base.append([prefix_path, node.count])  # 存入 [path, count]
            node = node.node_link

        # 重新计算条件模式基中项的支持度
        conditional_items_counts = {}
        for path, count in conditional_pattern_base:
            for node_item in path:
                conditional_items_counts[node_item] = conditional_items_counts.get(node_item, 0) + count

        conditional_frequent_items = {}
        for cond_item, cond_count in conditional_items_counts.items():
            if cond_count >= min_support:
                conditional_frequent_items[cond_item] = cond_count

        conditional_sorted_items = sorted(conditional_frequent_items.items(), key=lambda item: (-item[1], item[0]))

        if conditional_sorted_items:
            conditional_dataset = []
            item_dict_for_sorting = dict(conditional_frequent_items)
            for path, count in conditional_pattern_base:
                # 过滤出频繁项
                filtered_path = [i for i in path if i in item_dict_for_sorting]
                # 根据 FP 树构建规则（局部频率），排序并添加
                filtered_path.sort(key=lambda item: (item_dict_for_sorting[item], item), reverse=True)

                if filtered_path:
                    for _ in range(count):
                        conditional_dataset.append(filtered_path)
            if conditional_dataset:  # 确保数据集不为空
                conditional_header_table = {}

                cond_root, cond_header = build_fptree(conditional_dataset, conditional_header_table,
                                                      conditional_sorted_items)
                if cond_root.children:
                    mine_fp_tree(cond_header, min_support, new_pattern, frequent_patterns)

if __name__ == '__main__':
    data=load_data()
    #FPgrowth算法,只考虑最小支持度
    #先进行一项集计算
    new_list=pre_processing(data)
    min_support=3
    L_1=cal_1items(new_list,min_support)


    header_table={}
    root,final_header_table=build_fptree(data,header_table,L_1)
    print('a')
    frequent_patterns={}
    mine_fp_tree(final_header_table,min_support,set(),frequent_patterns)

    # 排序输出结果
    final_results = sorted(frequent_patterns.items(), key=lambda x: x[1], reverse=True)

    for pattern, support in final_results:
        print(f"项集: {set(pattern)} | 支持度: {support}")


