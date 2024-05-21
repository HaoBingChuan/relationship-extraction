from pprint import pprint

from py2neo import *
from py2neo import Node, Relationship
from py2neo.matching import *
from infra.neo4j.neoClient import *
"""
参考文档:
https://py2neo.org/2021.1/index.html#
"""


def relation_t():
    graph = graph_conn()
    rela_match = RelationshipMatcher(graph)
    rela = rela_match.match(r_type='IS_OWNER').limit(5)
    print(rela.all())


def post_nego(sub: str, obj: str, event: str,graph):
    # g = graph_conn()
    try:
        tx = graph.begin()
        a = Node("TEST", name=sub)  # Node(label, name)
        b = Node("TEST", name=obj)
        ab = Relationship(a, event, b)
        tx.create(ab)  # 创建节点和关系
        graph.commit(tx)
    except BaseException as ex:
        print(ex)
        if tx:
            graph.rollback(tx)


def test(graph: Graph):
    node_1 = Node('英雄', name='张无忌')
    node_2 = Node('英雄', name='杨逍', 武力值='100')
    node_3 = Node('派别', name='明教')

    graph.create(node_1)
    graph.create(node_2)
    graph.create(node_1)

    node_1_to_node_2 = Relationship(node_1, '教主', node_2)
    node_3_to_node_1 = Relationship(node_1, '统领', node_3)
    node_2_to_node_2 = Relationship(node_2, '师出', node_3)

    graph.create(node_1_to_node_2)
    graph.create(node_3_to_node_1)
    graph.create(node_2_to_node_2)

    node_7 = Node('英雄', name='张翠山')
    node_8 = Node('英雄', name='殷素素')
    node_9 = Node('英雄', name='狮王')

    relationship7 = Relationship(node_1, '生父', node_7)
    relationship8 = Relationship(node_1, '生母', node_8)
    relationship9 = Relationship(node_1, '义父', node_9)

    subgraph_1 = Subgraph(nodes=[node_7, node_8, node_9], relationships=[relationship7, relationship8, relationship9])
    graph.create(subgraph_1)

    # 创建一个新node
    node_10 = Node('武当', name='张三丰')
    graph.create(node_10)
    # 创建两个关系：张无忌→（师公）→张三丰   张翠山→（妻子）→殷素素
    relationship_10 = Relationship(node_1, '师公', node_10)
    relationship_11 = Relationship(node_7, '妻子', node_8)

    graph.create(relationship_10)
    graph.create(relationship_11)

    node_x = Node('英雄', name='韦一笑')
    graph.create(node_x)

    node_100 = Node('巾帼', name='赵敏')
    re_100 = Relationship(node_1, 'Love', node_100)

    node_101 = Node('巾帼', name='周芷若')
    re_101 = Relationship(node_1, 'knows', node_101)
    re_101_ = Relationship(node_101, 'hate', node_100)

    node_102 = Node('巾帼', name='小昭')
    re_102 = Relationship(node_1, 'konws', node_102)

    node_103 = Node('巾帼', name='蛛儿')
    re_103 = Relationship(node_103, 'Love', node_1)

    graph.create(node_100)
    graph.create(re_100)
    graph.create(node_101)
    graph.create(re_101)
    graph.create(re_101_)
    graph.create(node_102)
    graph.create(re_102)
    graph.create(node_103)
    graph.create(re_103)

    node_1 = Node('反派', **{'name': '鹤笔翁', 'age': 54})
    node_2 = Node('反派', **{'name': '鹿笔翁', 'age': 55})
    re_103 = Relationship(node_1, '组合', node_2, **{'name': '玄冥二老'})
    graph.create(node_1)
    graph.create(node_2)
    graph.create(re_103)


if __name__ == '__main__':
    # relation_t()
    graph = graph_conn()
    # test(graph)
    # graph.delete_all()
    try:
        nodes = NodeMatcher(graph)
        print(nodes.get(3))

        s_node = nodes.match("英雄", name="曾涛").first()

        t_node = nodes.match("派别", name="明教").first()

        p = {'position': '中护法'}
        ab = Relationship(s_node, '护法', t_node, **p)
        graph.create(ab)  # 创建节点和关系

        # a = Node("TEST", name="zengtao")  # Node(label, name)
        # b = Node("TEST", name="xiaohui")
        # ab = Relationship(a, "friend", b)
        # graph.create(ab)  # 创建节点和关系
    except BaseException as e:
        print(e)
    finally:
        print('is OK...')
