from app.models import *
import networkx as nx
from matplotlib import pylab as plt

def draw_gragh(node_wlibnames, file_name):
    """
    :param node_models:
    :return:
    """
    g = nx.DiGraph()
    g.add_nodes_from(node_wlibnames)
    edge_list_s = []
    edge_list_d = []
    res = []
    user = User.objects.get(id=1)
    operator1 = ('*', '◇','~')
    operator2 = ('∪', '∩', '✱', 'ㄨ')
    # ==================  for each wlibnames , check relation ============================
    for ind_1, t1 in enumerate(node_wlibnames):
        for ind_2, t2 in enumerate(node_wlibnames[ind_1 + 1:]):
            try:
                nexus = Nexus.objects.get(r_name='<=')
            except:
                nexus = Nexus.objects.create(r_name='<=')
            #A <= A∪B
            #A∩B <= A
            #A✱B <= A
            #AㄨB <= A
            if any([x in t1 for x in operator2]):
                if any([x in t2 for x in operator2]):
                    edge_list_d.append((t1, t2))
                else:
                    thisoper = ''
                    for oper in operator2:
                        if oper in t1:
                            thisoper = oper
                    t11 = t1.split(thisoper)[0]
                    t12 = t1.split(thisoper)[1]
                    obj_1 = Wlibrary.objects.filter(name=t11).values('id', 'name').first()
                    obj_2 = Wlibrary.objects.filter(name=t2).values('id', 'name').first()
                    obj_3 = Wlibrary.objects.filter(name=t12).values('id', 'name').first()
                    if thisoper == '∪':
                        if t2 == t11 or t2 == t12:
                            r = Relation2.objects.filter(t11= obj_2['id'], operator1='default',t12=0,
                                                            t21=obj_1['id'],operator2=thisoper,t22=obj_3['id']).values('id').first()
                            if r:
                                rid = r['id']
                            else:
                                exp = t2 + '<=' + t1
                                r = Relation2.objects.create(t11= obj_2['id'], operator1='default',t12=0,
                                                            t21=obj_1['id'],operator2=thisoper,t22=obj_3['id'], user=user,
                                                            relationship=nexus,exp=exp)
                                rid = r.id
                            edge_list_s.append((t2, t1))
                            res.append((t2,t1, '<=', rid))
                        else:
                            edge_list_d.append((t1, t2))
                    else:
                        if t2 == t11 or t2 == t12:
                            r = Relation2.objects.filter(t11= obj_1['id'], operator1=thisoper,t12=obj_3['id'],
                                                            t21=obj_2['id'],operator2='default',t22=0).values('id').first()
                            if r:
                                rid = r['id']
                            else:
                                exp = t1 + '<=' + t2
                                r = Relation2.objects.create(t11= obj_1['id'], operator1=thisoper,t12=obj_3['id'],
                                                            t21=obj_2['id'],operator2='default',t22=0, user=user,
                                                            relationship=nexus,exp=exp)
                                rid = r.id
                            edge_list_s.append((t1, t2))
                            res.append((t1,t2, '<=', rid))
                        else:
                            edge_list_d.append((t1, t2))
            elif any([x in t2 for x in operator2]):
                thisoper = ''
                for oper in operator2:
                    if oper in t2:
                        thisoper = oper
                t21 = t2.split(thisoper)[0]
                t22 = t2.split(thisoper)[1]
                obj_1 = Wlibrary.objects.filter(name=t1).values('id', 'name').first()
                obj_2 = Wlibrary.objects.filter(name=t21).values('id', 'name').first()
                obj_3 = Wlibrary.objects.filter(name=t22).values('id', 'name').first()
                if thisoper == '∪':
                    if t1 == t21 or t1 == t22:
                        r = Relation2.objects.filter(t11= obj_1['id'], operator1='default',t12=0,
                                                        t21=obj_2['id'],operator2=thisoper,t22=obj_3['id']).values('id').first()
                        if r:
                            rid = r['id']
                        else:
                            exp = t1 + '<=' + t2
                            r = Relation2.objects.create(t11= obj_2['id'], operator1='default',t12=0,
                                                        t21=obj_1['id'],operator2=thisoper,t22=obj_3['id'], user=user,
                                                        relationship=nexus,exp=exp)
                            rid = r.id
                        edge_list_s.append((t1, t2))
                        res.append((t1,t2, '<=', rid))
                    else:
                        edge_list_d.append((t1, t2))
                else:
                    if t1 == t21 or t1 == t22:
                        r = Relation2.objects.filter(t11= obj_2['id'], operator1=thisoper,t12=obj_3['id'],
                                                        t21=obj_1['id'],operator2='default',t22=0).values('id').first()
                        if r:
                            rid = r['id']
                        else:
                            exp = t2 + '<=' + t1
                            r = Relation2.objects.create(t11= obj_2['id'], operator1=thisoper,t12=obj_3['id'],
                                                        t21=obj_1['id'],operator2='default',t22=0, user=user,
                                                        relationship=nexus,exp=exp)
                            rid = r.id
                        edge_list_s.append((t2, t1))
                        res.append((t2,t1, '<=', rid))
                    else:
                        edge_list_d.append((t1, t2))
            else:
                #A <= A* <= A◇  A <= A︿
                if t1.endswith(operator1) and not t2.endswith(operator1):
                    oper = t1[-1]
                    t11 = t1.replace(oper, '')
                    obj_1 = Wlibrary.objects.filter(name=t11).values('id', 'name').first()
                    obj_2 = Wlibrary.objects.filter(name=t2).values('id', 'name').first()
                    if t11 == t2:
                        r = Relation2.objects.filter(t11= obj_2['id'], operator1='default',t12=0,
                                                     t21=obj_1['id'],operator2=oper,t22=0).values('id').first()
                        if r:
                            rid = r['id']
                        else:
                            exp = t2 + '<=' + t1
                            r = Relation2.objects.create(t11= obj_2['id'], operator1='default',t12=0,
                                                     t21=obj_1['id'],operator2=oper,t22=0, user=user,
                                                     relationship=nexus,exp=exp)
                            rid = r.id
                        edge_list_s.append((t2, t1))
                        res.append((t2,t1, '<=', rid))
                    else:
                        edge_list_d.append((t1, t2))

                elif not t1.endswith(operator1) and t2.endswith(operator1):
                    oper = t2[-1]
                    t21 = t2.replace(oper, '')
                    obj_1 = Wlibrary.objects.filter(name=t1).values('id', 'name').first()
                    obj_2 = Wlibrary.objects.filter(name=t21).values('id', 'name').first()
                    if t1 == t21:
                        r = Relation2.objects.filter(t11=obj_1['id'], operator1='default', t12=0,
                                                     t21=obj_2['id'], operator2=oper, t22=0).values('id').first()
                        if r:
                            rid = r['id']
                        else:
                            exp = t1 + '<=' + t2
                            r = Relation2.objects.create(t11=obj_1['id'], operator1='default', t12=0,
                                                         t21=obj_2['id'], operator2=oper, t22=0, user=user,
                                                         relationship=nexus, exp=exp)
                            rid = r.id
                        edge_list_s.append((t1, t2))
                        res.append((t1, t2, '<=', rid))
                    else:
                        edge_list_d.append((t1, t2))

                elif  t1.endswith(operator1) and t2.endswith(operator1):
                    oper1 = t1[-1]
                    oper2 = t2[-1]
                    t11 = t1.replace(oper1, '')
                    t21 = t2.replace(oper2, '')
                    obj_1 = Wlibrary.objects.filter(name=t11).values('id', 'name').first()
                    obj_2 = Wlibrary.objects.filter(name=t21).values('id', 'name').first()
                    if t11 == t21:
                        if oper1 == '*' and oper2 == '◇':
                            r = Relation2.objects.filter(t11=obj_1['id'], operator1=oper1, t12=0,
                                                         t21=obj_2['id'], operator2=oper2, t22=0).values('id').first()
                            if r:
                                rid = r['id']
                            else:
                                exp = t1 + '<=' + t2
                                r = Relation2.objects.create(t11=obj_1['id'], operator1=oper1, t12=0,
                                                             t21=obj_2['id'], operator2=oper2, t22=0, user=user,
                                                             relationship=nexus, exp=exp)
                                rid = r.id
                            edge_list_s.append((t1, t2))
                            res.append((t1,t2, '<=', rid))
                        elif oper1 == '◇' and oper2 == '*':
                            r = Relation2.objects.filter(t11=obj_2['id'], operator1=oper2, t12=0,
                                                         t21=obj_1['id'], operator2=oper1, t22=0).values('id').first()
                            if r:
                                rid = r['id']
                            else:
                                exp = t2 + '<=' + t1
                                r = Relation2.objects.create(t11=obj_2['id'], operator1=oper2, t12=0,
                                                             t21=obj_1['id'], operator2=oper1, t22=0, user=user,
                                                             relationship=nexus, exp=exp)
                                rid = r.id
                            edge_list_s.append((t2, t1))
                            res.append((t2,t1, '<=', 1))
                        else:
                            edge_list_d.append((t1, t2))
                    else:
                        edge_list_d.append((t1, t2))

                else:
                    obj_1 = Wlibrary.objects.get(name=t1)
                    obj_2 = Wlibrary.objects.get(name=t2)
                    r1 = Relation2.objects.filter(t11=obj_1.id, operator1='default', t12=0,
                                                         t21=obj_2.id, operator2='default', t22=0).values('id','relationship').first()
                    r2 = Relation2.objects.filter(t11=obj_2.id, operator1='default', t12=0,
                                                         t21=obj_1.id, operator2='default', t22=0).values('id','relationship').first()
                    if r1 != None:
                        # relation exists
                        if r1['relationship'] == 1:
                            edge_list_s.append((t1, t2))
                            res.append((t1, t2, '<=', r1['id']))
                    elif r2 != None:
                        # relation exists
                        if r2['relationship'] == 1:
                            edge_list_s.append((t2, t1))
                            res.append((t2, t1, '<=', r2['id']))
                    else:
                        # relation not exists
                        step = 0
                        if obj_1.mcdc_1.isnumeric() and obj_2.mcdc_2.isnumeric():
                            if int(obj_1.mcdc_1) > int(obj_2.mcdc_2):
                                step = 1
                            if int(obj_1.mcdc_1) < int(obj_2.mcdc_2):
                                step = 2


                        elif obj_1.mcdc_1 == 'omega' and obj_2.mcdc_2.isnumeric():
                            step = 1
                        elif obj_1.mcdc_1.isnumeric() and obj_2.mcdc_2 == 'omega':
                            step = 2
                        elif obj_1.mcdc_1 == 'infinity':
                            if obj_2.mcdc_2 == 'omega' or obj_2.mcdc_2.isnumeric():
                                step = 1
                        elif obj_2.mcdc_2 == 'infinity':
                            if obj_1.mcdc_1 == 'omega' or obj_1.mcdc_1.isnumeric():
                                step = 2
                        else:
                            step = 0
                        print(step)
                        if step == 1:
                            # check mcdc
                            exp =t1  + '!<' + t2
                            r = Relation2.objects.create(t11=obj_1.id, operator1='default', t12=0,
                                                            t21=obj_2.id, operator2='default', t22=0, user=user,
                                                            relationship=nexus, exp=exp)
                            edge_list_s.append((t1, t2))
                            res.append((t1, t2, "!<", r.id))
                        elif step == 2:
                            exp = t2 + '!<' + t1
                            r = Relation2.objects.create(t11=obj_2.id, operator1='default', t12=0,
                                                            t21=obj_1.id, operator2='default', t22=0, user=user,
                                                            relationship=nexus, exp=exp)
                            #edge_list_d.append((t2, t1))
                            res.append((t2, t1, "!<", r.id))
                        # default
                        else:
                            edge_list_d.append((t1, t2))
    # ==========  draw image   ===================
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_size=700, label=True)
    nx.draw_networkx_edges(g, pos, edgelist=edge_list_s, edge_color='k', style='solid',
                           width=3, label=True)
    nx.draw_networkx_edges(g, pos, edgelist=edge_list_d, width=3, edge_color='b', style='dashed')
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edge_labels(g, pos)
    plt.axis('off')
    plt.savefig(file_name + ".png")  # save as png
    plt.close()
    return res
