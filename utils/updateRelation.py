from app.models import *

def updateRelation(t1_Name, t2_Name):
    obj1 = Wlibrary.objects.filter(name=t1_Name).first()
    obj2 = Wlibrary.objects.filter(name=t2_Name).first()
    t1_mcdc1 = obj1.mcdc_1
    t1_mcdc2 = obj1.mcdc_2
    t2_mcdc1 = obj2.mcdc_1
    t2_mcdc2 = obj2.mcdc_2
    print(t1_mcdc1,t1_mcdc2, t2_mcdc1,t2_mcdc2)
    newt1_mcdc2 = getMin(t1_mcdc2, t2_mcdc2)
    newt2_mcdc1 = getMax(t1_mcdc1, t2_mcdc1)
    print(2)
    print(newt1_mcdc2, newt2_mcdc1)
    Wlibrary.objects.filter(name=t1_Name).update(mcdc_2 = newt1_mcdc2)
    Wlibrary.objects.filter(name=t2_Name).update(mcdc_1 = newt2_mcdc1)
    print(3)
    greaterTheorems = Relation2.objects.filter(t11=obj2.id, operator1='default', t12=0,relationship_id=1,
                                    operator2='default', t22=0).all()
    print(greaterTheorems)
    for theorem in greaterTheorems:
        print(4)
        obj3 = Wlibrary.objects.filter(id= theorem.t21)
        updateRelation(t2_Name, obj3.name)
        print(5)

def getMin(t1_mcdc2, t2_mcdc2):
    mcdc_tpye = ['omega', 'infinity']
    if t1_mcdc2.isnumeric() and t2_mcdc2.isnumeric():
        res = t2_mcdc2 if int(t1_mcdc2) > int(t2_mcdc2) else t1_mcdc2

    elif t1_mcdc2 in mcdc_tpye and t2_mcdc2.isnumeric() :
        res = t2_mcdc2

    elif t1_mcdc2.isnumeric() and t2_mcdc2 in mcdc_tpye:
        res = t1_mcdc2

    elif t1_mcdc2 in mcdc_tpye and t2_mcdc2 in mcdc_tpye:
        if t2_mcdc2 == t2_mcdc2:
            res = t2_mcdc2
        else:
            res = 'omega'
    return res

def getMax(t1_mcdc1, t2_mcdc1):
    mcdc_tpye = ['omega', 'infinity']
    if t1_mcdc1.isnumeric() and t2_mcdc1.isnumeric():
        res = t1_mcdc1 if int(t1_mcdc1) > int(t2_mcdc1) else t2_mcdc1

    elif t1_mcdc1 in mcdc_tpye and t2_mcdc1.isnumeric():
        res = t1_mcdc1

    elif t1_mcdc1.isnumeric() and t2_mcdc1 in mcdc_tpye:
        res = t2_mcdc1

    elif t1_mcdc1 in mcdc_tpye and t2_mcdc1 in mcdc_tpye:
        if t1_mcdc1 == t1_mcdc1:
            res = t2_mcdc1
        else:
            res = 'infinity'
    return res