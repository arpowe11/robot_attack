import pygame
from explosion import Explosion


class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player) -> None:
        """ Make enemy inherit sprite """
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Set up crate variables
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Crate.png")
        self.image_hurt = pygame.image.load("../assets/Crate_hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/CrateRubble.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurt_timer = 0
        self.just_placed = True


    def update(self, projectiles) -> None:
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False

        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                projectile.explode()
                self.get_hit(projectile.damage)

        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            image_to_draw = self.image_hurt
        else:
            image_to_draw = self.image

        self.screen.blit(image_to_draw, self.rect)

    def get_hit(self, damage) -> None:
        self.health -= damage
        self.hurt_timer = 5

        if self.health <= 0:
            self.health = 99999
            Explosion(self.screen, self.x, self.y, self.explosion_images, 20, 0, False)
            self.kill()


class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player) -> None:
        """ Make enemy inherit sprite """
        Crate.__init__(self, screen, x, y, player)  # NOQA

        # Set up ExplosiveCrate variables
        self.image = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.image_hurt = pygame.image.load("../assets/ExplosiveBarrel_hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion1.png"))
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion2.png"))
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion3.png"))
        self.health = 20

    def get_hit(self, damage) -> None:
        self.health -= damage
        self.hurt_timer = 5

        if self.health <= 0:
            self.health = 99999
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 4, True)
            self.kill()
