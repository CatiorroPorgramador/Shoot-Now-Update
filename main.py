# git remote add origin https://github.com/CatiorroPorgramador/Shoot-Now-Update.git
# git commit -m "v(version)"
# git branch -M main
# git push -u origin main
# v0.0.3

'''
add ui
add new zombies
add new guns
add sounds
add menu game
add items
add death menu
'''

import pygame

from random import randint

from scripts.player import player_class
from scripts.zombie import zombie_class
from scripts.item import item_class

pygame.init()

WINDOW_NAME = 'Shoot Now 0.2'
FONT = pygame.font.Font('data/font.ttf', 26)

display = pygame.display.set_mode([850, 600])

def _exi() -> None:
    pygame.quit()
    exit(0)

def menu() -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exi()

def gameplay() -> None:
    pygame.display.set_caption(WINDOW_NAME)

    # Groups
    player_group = pygame.sprite.Group()
    player_shot_group = pygame.sprite.Group()
    zombie_shot_group = pygame.sprite.Group()
    zombie_group = pygame.sprite.Group()

    item_group = pygame.sprite.Group()

    # Objects
    clock = pygame.time.Clock()

    player:player_class = player_class(player_group)

    # Others...
    zom_spw_idx:int = 0 # Zombie Spawner Index
    itm_spw_idx:int = 0 # Item Spawner Index

    ani_inf_idx:int = 0 # Animation Interface Index

    frame_gun:pygame.Surface = pygame.image.load('data/ui/frame.png').convert_alpha()
    frame_gun = pygame.transform.scale(frame_gun, (64, 64))

    # Init

    # Loop
    while True:
        clock.tick(60)
        pygame.display.set_caption(f'{WINDOW_NAME} - {round(clock.get_fps())} fps')

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exi()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.set_id_gun(0)
                    player.update_gun()
                
                elif event.key == pygame.K_2:
                    player.set_id_gun(1)
                    player.update_gun()

        # Draw
        display.fill([100, 100, 100])

        player_group.draw(display)
        display.blit(player.get_gun_sprite().convert_alpha(), (player.rect.x-65, player.rect.y + 12))

        player_shot_group.draw(display)
        zombie_shot_group.draw(display)
        if player.can_shoot:
            player.shoot(player_shot_group)

        zombie_group.draw(display)

        item_group.draw(display)

        # Interface
        for gun in player.pgun:
            sprite = pygame.transform.scale(player.gun_spritesheet.sprite_at(pygame.Rect(28*gun['frame'], 0, 28, 16)), (76, 52))
            
            display.blit(sprite, [ani_inf_idx*60-10, 20])
            ani_inf_idx += 1
        ani_inf_idx = 0

        display.blit(frame_gun, (10, 10))
        display.blit(frame_gun, (74, 10))

        display.blit(FONT.render(f'Life: {player.life}', False, (255, 255, 255)), (150, 10))
        display.blit(FONT.render(f'Kills: {player.kills}', False, (255, 255, 255)), (150, 40))
        display.blit(FONT.render(f'Coins: {player.coins}', False, (255, 255, 255)), (280, 10))

        # Update
        player_group.update()
        player_shot_group.update()
        zombie_shot_group.update()
        zombie_group.update()
        item_group.update()
        
        # Spawn
        zom_spw_idx += 1
        itm_spw_idx += 1

        if zom_spw_idx > 40:
            if randint(0, 1) == 0:
                new_zom = zombie_class(zombie_group)
                new_zom.shot_group = zombie_shot_group
            
            zom_spw_idx = 0
        
        if itm_spw_idx > 40:
            if randint(0, 2) == 1:
                item_class(item_group)
            itm_spw_idx = 0

        # Collisions
        zom_sht_col = pygame.sprite.groupcollide(zombie_group, player_shot_group, False, True, pygame.sprite.collide_rect)
        zom_ply_col = pygame.sprite.groupcollide(zombie_group, player_group, False, False, pygame.sprite.collide_rect)

        ply_sht_col = pygame.sprite.groupcollide(player_group, zombie_shot_group, False, True, pygame.sprite.collide_mask)
        
        itm_ply_col = pygame.sprite.groupcollide(item_group, player_group, True, False, pygame.sprite.collide_rect)

        if zom_ply_col:
            for zom in zom_ply_col:
                player.life -= zom.damage
                zom.vec[0] += -20
        
        if zom_sht_col:
            for zom in zom_sht_col:
                if zom.life-player.pgun[player.id_gun]['damage'] <= 0:
                    player.kills += 1
                zom.life -= player.pgun[player.id_gun]['damage']
        
        if ply_sht_col:
            player.life -= 20
        
        if itm_ply_col:
            for item in itm_ply_col:
                player.coins += item._add[0]
                player.life += item._add[1]

        pygame.display.update()

if __name__ == '__main__':
    gameplay()