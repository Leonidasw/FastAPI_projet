#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.

import RPi.GPIO as GPIO
import time

# Configuration de la GPIO
GPIO.setmode(GPIO.BCM)  # Utilisation du mode BCM pour référencer les broches
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche 2 (GPIO A2) en entrée avec résistance de pull-up
lst=[0]
i=9
def modif(liste):
    lst[0]+=1
def bouton_appuye(channel):
    modif(lst)
    print(i)
    print("Le bouton a été appuyé !")

# Détection de l'appui sur le bouton
GPIO.add_event_detect(5, GPIO.FALLING, callback=bouton_appuye, bouncetime=300)


import math
import sys
import time
from grove.adc import ADC

__all__ = ['GroveThumbJoystick']

class GroveThumbJoystick(object):
    '''
    Grove Thumb Joystick class

    Args:
        channel(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channelX = channel
        self.channelY = channel + 1
        self.adc = ADC()

    @property
    def value(self):
        '''
        Get the water strength value

        Returns:
            (pair): x-ratio, y-ratio, all are 0(0.0%) - 1000(100.0%)
        '''
        return self.adc.read(self.channelX), self.adc.read(self.channelY)

Grove = GroveThumbJoystick

matrice = [[0 for i in range(10)] for j in range(10)]

position = [0, 0]

def deplacement(position, vecteur, taille, vitesse_x, vitesse_y,x_pred,y_pred):
    """
    Met à jour la position dans la matrice en fonction du vecteur de déplacement.
    - `position` : Coordonnées actuelles [ligne, colonne].
    - `vecteur` : Vecteur de déplacement (x, y) compris entre -100 et 100.
    - `taille` : Taille de la matrice (taille x taille).
    """
    if x_pred == 0 and y_pred == 0:
        dx = 1 if vecteur[0] > 33 else -1 if vecteur[0] < -33 else 0
        dy = 1 if vecteur[1] > 33 else -1 if vecteur[1] < -33 else 0
    else:
        dx = 0.25 if vecteur[0] > 33 else -0.25 if vecteur[0] < -33 else 0
        dy = 0.25 if vecteur[1] > 33 else -0.25 if vecteur[1] < -33 else 0

    nouvelle_position = [
        position[0] + dx*vitesse_x,  
        position[1] + dy*vitesse_y   
    ]

    nouvelle_position[0] = nouvelle_position[0]%taille
    nouvelle_position[1] = nouvelle_position[1]%taille
    
    return nouvelle_position, (dx != 0 or dy != 0)  

def calculer_vitesse(nb):
    """
    Détermine la vitesse en fonction de l'inclinaison du joystick.
    - Vitesse normale (1 case/sec) : Inclinaison modérée (\( -50 \leq x, y \leq 50 \)).
    - Vitesse rapide (1 case/0.5 sec) : Inclinaison forte (\( x > 50 \) ou \( x < -50 \), \( y > 50 \) ou \( y < -50 \)).
    """
    if abs(nb) > 66 :
        return 1 
    return 0.5  

def affichage_matrice(matrice,position,press):
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if i == int(position[0]) and j == int(position[1]):
                if press:
                    print("X", end=" ") 
                else:
                    print("0", end=" ") 
            else:
                print(".", end=" ")  
        print()

def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = 0

    sensor = GroveThumbJoystick(pin)
    matrice = [[0 for i in range(10)] for j in range(10)]
    position = [0, 0]
    press=True
    affichage_matrice(matrice,position,press)
            
            
    x_pred=0
    y_pred=0
    while True:
        x, y = sensor.value
        if x > 900:
            if press:
                press=False
            else:
                press=True
            x=500
            time.sleep(0.1)
        x,y=(x//10 -50)*4, (y//10 -50)*4
        vitesse_x = calculer_vitesse(x)
        vitesse_y = calculer_vitesse(y)
		
        nouvelle_position, deplacement_possible = deplacement(position, [x, y], len(matrice),vitesse_x,vitesse_y,x_pred,y_pred)
		
        if deplacement_possible:
            position = nouvelle_position
		
        x_pred,y_pred=x,y
        int_position=[int(position[0]),int(position[1])]
        print("\nPosition actuelle : ", int_position)
        affichage_matrice(matrice,position,press)
        time.sleep(0.05)
if __name__ == '__main__':
    main()

