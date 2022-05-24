from PIL import Image, ImageDraw, ImageFilter, ImageFont
import colorsys
import random
import uuid
from app_dict import genName

def getBomzhPicClean(gen, name=None):
    t_r = random.randint(1,12)
    i_r = random.randint(1,4)
    n_r = random.randint(1,4)
    v_r = random.randint(1,16)
    br_r = random.randint(1,16)


    bp = Image.open("pic/b.png")
    tp = Image.open("pic/t/{}.png".format(t_r))
    vp = Image.open("pic/v/{}.png".format(v_r))
    brp = Image.open("pic/br/{}.png".format(br_r))
    ip = Image.open("pic/i/{}.png".format(i_r))
    np = Image.open("pic/n/{}.png".format(n_r))

    bp.paste(tp, (0, 0), tp)
    bp.paste(vp, (0, 0), vp)
    bp.paste(brp, (0, 0), brp)
    bp.paste(ip, (0, 0), ip)
    bp.paste(np, (0, 0), np)
    file_dir = "data/pic/clean/{}.png".format(str(uuid.uuid4()))

    bp.save(file_dir)
    bp.close()
    tp.close()
    vp.close()
    brp.close()
    ip.close()
    np.close()
    return file_dir

def getBomzhPic(gen, name=None):
    clean_pic_url = getBomzhPicClean(gen, name)

    fg = Image.open("pic/fg.png")
    bp = Image.open(clean_pic_url)

    fg.paste(bp, (0, 0), bp)

    if name != None:
        width, height = fg.size
        title_font = ImageFont.truetype('src/fonts/TippytoesRegular.ttf', 72)
        image_editable = ImageDraw.Draw(fg)
        image_editable.text((width//2,45), name, (237, 230, 211), font=title_font, anchor='mm')


    file_dir = "data/pic/full/{}.png".format(str(uuid.uuid4()))

    fg.save(file_dir)
    bp.close()
    fg.close()
    return [clean_pic_url, file_dir]

def getBandaPic(user_id,bomzhs):
    fg = Image.open("pic/fg_big.png")

    bomzhs_pic = []
    for b in bomzhs:
        bomzhs_pic.append(b.pic_clean_url)

    i = 1
    for pic in bomzhs_pic:
        tmp_pic = Image.open(pic)
        fg.paste(tmp_pic, (-400 + 333*i, 0), tmp_pic)
        i+=1
    fg.thumbnail((1000,400), Image.ANTIALIAS)
    fg.save('data/pic/team/{}.png'.format(user_id))

    return 'data/pic/team/{}.png'.format(user_id)