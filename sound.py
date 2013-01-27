import pygame, sys

pygame.mixer.init()
machineGunSound = pygame.mixer.Sound('assets/machine-gun.ogg')
#This is a machine gun, doofus
failSplatSound = pygame.mixer.Sound('assets/fail-splat.ogg')
#PC dies
nastySquishSound = pygame.mixer.Sound('assets/nasty-squish.ogg')
#Heart Jump Part 1
wetSplatSound = pygame.mixer.Sound('assets/wet-splat.ogg')
#Heartland
boneSquuchSound = pygame.mixer.Sound('assets/bone-squuch.ogg')
#Heart Jump Part 2
bodyThumpSound = pygame.mixer.Sound('assets/pause-thump.ogg')
#Errybody die, falling
