import time, os, glob
from main import db, Bomzh, Location, User, send_msg
from datetime import datetime, date, timedelta

def memory_clean():
    t_start = time.time()
    pic_c = 0
    pic_for_d = 0

    full_pic_list = glob.glob("data/pic/full/*")
    pic_c += len(full_pic_list)
    f_full_pic_list = []
    for pic in full_pic_list:
        new_p = pic.replace('\\', '/')
        f_full_pic_list.append(new_p)

    clean_pic_list = glob.glob("data/pic/clean/*.png")
    pic_c += len(clean_pic_list)
    f_clean_pic_list = []
    for pic in clean_pic_list:
        new_p = pic.replace('\\', '/')
        f_clean_pic_list.append(new_p)

    usefull_pic = []
    miss_pic = 0

    bomzhs_obj = Bomzh.query.all()

    for bomzh in bomzhs_obj:
        if bomzh.pic_url in f_full_pic_list:
            usefull_pic.append(bomzh.pic_url)
        else:
            miss_pic += 1
        if bomzh.pic_clean_url in f_clean_pic_list:
            usefull_pic.append(bomzh.pic_clean_url)
        else:
            miss_pic += 1

    for full_pic in f_full_pic_list:
        if full_pic in usefull_pic:
            pass
        else:
            os.remove(full_pic)
            pic_for_d += 1

    for clean_pic in f_clean_pic_list:
        if clean_pic in usefull_pic:
            pass
        else:
            os.remove(clean_pic)
            pic_for_d += 1
    t_end = time.time()
    t_run = t_end - t_start

    return t_run, pic_c, pic_for_d, miss_pic



def update_work():
    t_start = time.time()
    bomzh_obj_list = Bomzh.query.all()

    bomzhs_obj_c = len(bomzh_obj_list)
    bomzhs_obj_on_work = 0
    bomzhs_obj_finish_work = 0

    for bomzh in bomzh_obj_list:
        if bomzh.state == 2: 
            bomzhs_obj_on_work += 1  

            location = Location.query.filter_by(id=bomzh.work_location).first()

            last_work = bomzh.last_work
            final_t = last_work + timedelta(minutes=location.work_time)

            if final_t <= datetime.now():
                bomzhs_obj_finish_work += 1

                bomzh.is_work = False
                bomzh.state = 5

                db.session.commit()
                user = User.query.filter_by(id=bomzh.user_id).first()

                send_msg(
                    chat_id = user.chat_id, 
                    text = "Бомж {}[#{}] закончил работу".format(bomzh.name, bomzh.id),
                    buttons=[
                        [["Посмотреть добычу","/endwork " + str(bomzh.id)]]
                    ]           
                )
    t_end = time.time()
    t_run = t_end - t_start
    return t_run, bomzhs_obj_c, bomzhs_obj_on_work, bomzhs_obj_finish_work


os.system("title " + "BOMZH RPG --- DATA UPDATER ---")
while True:
    t_start = time.time()
    os.system('cls')
    print('='*32 + ' UPDATE [ {} ] '.format(datetime.now()) + '='*32 )
    
    print('\n' + '.'*8 + ' WORK UPDATE ' + '.'*8 )
    delta, obj_c, obj_on_work, obj_finish_work = update_work()
    print(" -- delta:[ {} ] -- objs:[ {} ] -- objs on work:[ {} ] -- obj finish work:[ {} ]".format(delta, obj_c, obj_on_work, obj_finish_work))
    
    print('\n' + '.'*8 + ' MEMR CLEAN ' + '.'*8 )
    delta, pic, pic_d, pic_m = memory_clean()
    print(" -- delta:[ {} ] -- pic:[ {} ] -- pic_d:[ {} ] -- pic_m:[ {} ]".format( delta, pic, pic_d, pic_m))


    t_end = time.time()
    t_run = t_end - t_start
    print("\n\nFINAL DELTA [{}]".format(t_run))
    time.sleep(10)