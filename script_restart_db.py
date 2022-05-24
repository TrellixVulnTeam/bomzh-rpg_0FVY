from main import db, Status, Location, Type, SubType, Item
from app_dict import STATUSES, LOCATIONS, TYPES, SUB_TYPES, ITEMS

db.drop_all()
db.create_all()

for s in STATUSES:
    news = Status(line=s)
    db.session.add(news)

for l in LOCATIONS:
    location = Location(
        name=l[0], 
        disc=l[1], 
        lvl_cup=l[2], 
        is_pve=l[3],
        work_time=l[4], 
        energy_lost=l[5],
        chance = l[6],
        chance_max = l[7],
        chance_extra = l[8],
        chance_extra_max = l[9],
        money_drop = l[10],
        gold_drop = l[11],
        exp_drop = l[12],
        joy_drop = l[13],
        joy_lost = l[14],
        hp_lost = l[15],
    )
    db.session.add(location)

for t in TYPES:
    tp = Type(name=t)
    db.session.add(tp)

for st in SUB_TYPES:
    stp = SubType(name=st)
    db.session.add(stp)


for a in ITEMS:
    i = Item(
        name = a[0],
        disc = a[1],
        t = a[2],
        sub_t = a[3],
        tir = a[4],
        # -------
        wep_dmg = a[5],
        wep_ac = a[6],
        wep_crit_s = a[7],
        wep_crit_c = a[8],
        # wep_mod = 

        armor_dmg = a[9],
        # armor_mod = 

        food_eat = a[10],
        food_joi = a[11],

        # -------
        is_seteble = a[12],
        is_useble = a[13],
        is_sell = a[14],
        price = a[15],
    )
    db.session.add(i)



db.session.commit()