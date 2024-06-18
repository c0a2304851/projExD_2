import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (5,0),
}
KOUKATON = pg.image.load("projExD/ex2/fig/3.png")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    x_axis,y_axis = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        x_axis = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        y_axis = False
    return x_axis,y_axis

def draw_gameover(screen):
    bg_img = pg.image.load("fig/pg_bg.jpg")
    black_out = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black_out,(0,0,0),(0,0,WIDTH,HEIGHT),0)
    black_out.set_alpha(50)
    kk_img_go = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_rct_l = kk_img_go.get_rect()
    kk_rct_l.center = int(WIDTH/3),int(HEIGHT/2)
    kk_rct_r = kk_img_go.get_rect()
    kk_rct_r.center = int(WIDTH/3*2),int(HEIGHT/2)  
    font = pg.font.Font(None, 80)
    txt = font.render("gameover", True,(255,255,255))
    screen.blit(bg_img, [0, 0])
    screen.blit(black_out, [0,0])
    screen.blit(kk_img_go, kk_rct_l)
    screen.blit(kk_img_go, kk_rct_r)
    screen.blit(txt, [int(WIDTH/2),int(HEIGHT/2)])
    pg.display.update()
    clock = pg.time.Clock()
    clock.tick(0.2)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))  # 20*20の空Surface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  # 空Surfaceに赤い円を描く
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rct.colliderect(bb_rct):
                draw_gameover(screen)
                return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for k,v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        kk_img = return_dict()[tuple(sum_mv)]
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_accs,bb_imgs = return_bbap()
        avx = vx*bb_accs[min(tmr//500,9)]
        avy = vy*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]
        bb_rct.move_ip(avx,avy)
        xis, yis = check_bound(bb_rct)
        if not xis:
            vx *= -1
        if not yis:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

def return_bbap():  #bombのaccelとpowerを返す
    bb_accel = [i for i in range(1,11)]
    bb_power = []
    for r in bb_accel:
        bb_img = pg.Surface((20*r,20*r))  # 20*20の空Surface
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)  # 空Surfaceに赤い円を描く
        bb_img.set_colorkey((0,0,0))
        bb_power.append(bb_img)
    return tuple(bb_accel),tuple(bb_power)

def return_dict():
    return {  # こうかとんの回転辞書 .loadのところ定数にした方が良い
        (0,-5): pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False), 90, 2.0),
        (+5,-5): pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False), 45, 2.0),
        (+5,0): pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False), 0, 2.0),
        (+5,+5): pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False), 315, 2.0),
        (0,+5): pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False), 270, 2.0),
        (-5,+5): pg.transform.rotozoom(KOUKATON, 45, 2.0),
        (-5,0): pg.transform.rotozoom(KOUKATON, 0, 2.0),
        (-5,-5): pg.transform.rotozoom(KOUKATON, 315, 2.0),
        (0,0): pg.transform.rotozoom(KOUKATON, 0, 2.0),
    }

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
