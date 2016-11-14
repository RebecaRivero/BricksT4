# -*- coding: utf-8 -*-
import sys, pygame
from pygame.locals import *
try:
    import android
except ImportError:
    android = None 

ANCHO = 550
ALTO = 900

 
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("img/pelota.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO - 40
        self.speed = [0.2, -0.2]
 
    def actualizar(self, time, base, impacto_bloques, pantalla):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
            
        if self.rect.bottom > ALTO:
            finJuego(pantalla)

 
        if pygame.sprite.collide_rect(self, base):
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

        if impacto_bloques:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time 
 
    
            
 
class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("img/base1.png")
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO / 2
        self.rect.y = ALTO - 30
               
            

        

class Ladrillo(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = cargar_imagen("img/rojo.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
  
 
def cargar_imagen(filename, transparent = False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image


def finJuego(pantalla):
    finjuego = True
    img = cargar_imagen("img/fin.png")
    pantalla.blit(img, (ANCHO / 2, ALTO / 2))
    pygame.display.flip()
    while finjuego:
        evento = pygame.event.wait()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()

def ganarJuego(pantalla):
    ganarjuego = True
    img = cargar_imagen("img/gana.png")
    pantalla.fill((0, 0, 0))
    pantalla.blit(img, (ANCHO / 2, ALTO / 2))
    pygame.display.flip()
    while ganarjuego:
        evento = pygame.event.wait()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
 

 
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("BricksT 4")
 
    if android:
        android.init()

    pelota = Pelota()
    base = Base()
    ladrillos = pygame.sprite.Group()


    t = 0
    for i in range(90/10):
        e = 0
        for s in range(ANCHO / 25):
            ladrillo = Ladrillo(e, t)
            ladrillos.add(ladrillo)
            e += 50
        t += 23

    reloj = pygame.time.Clock()
    puntuacion = 0

    salir = False
    
    while salir != True:
        time = reloj.tick(60)


        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                salir = True
                sys.exit()



        pantalla.fill((0, 0, 0))
        lista_impacto_ladrillos = pygame.sprite.spritecollide(pelota, ladrillos, True) 
        pelota.actualizar(time, base, lista_impacto_ladrillos, pantalla)

        
        ladrillos.draw(pantalla)
        pantalla.blit(pelota.image, pelota.rect)
        
        pantalla.blit(base.image, (base.rect.x, base.rect.y))

        base.rect.x, ejey = pygame.mouse.get_pos() 

        pygame.display.flip()
        for bloque in lista_impacto_ladrillos:
            puntuacion += 1
            if puntuacion == 99:
                ganarJuego(pantalla)


        


        
    return 0
 
if __name__ == '__main__':
    
    main()