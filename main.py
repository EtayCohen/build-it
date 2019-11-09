import pygame, random

pygame.init()
pygame.font.init()
pygame.display.set_caption('BUILD-IT!')
font = pygame.font.Font(None, 50)

HEIGHT = 640
WIDTH = 480
BLOCK_SIZE = 50


class Game:
    def __init__(self):
        self.height, self.width = HEIGHT, WIDTH
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        self.blocks = [Block()]
        self.factor = 1
        self.lost = False

    def draw(self):
        self.screen.fill((255, 255, 255))
        for block in self.blocks:
            block.draw(self.screen)

    def add(self):
        self.blocks[-1].velocity = 0
        if self.blocks[-1].y <= BLOCK_SIZE:
            self.scroll()
        if len(self.blocks) > 1:
            if (self.blocks[-1].x > self.blocks[-2].x + self.blocks[-1].width or
                    self.blocks[-1].x + self.blocks[-1].width < self.blocks[-2].x):
                self.lost = True
            if self.blocks[-1].x < self.blocks[-2].x:
                self.blocks[-1].width = (self.blocks[-1].x + self.blocks[-1].width) - self.blocks[-2].x
                self.blocks[-1].x = self.blocks[-2].x
            elif self.blocks[-1].x + self.blocks[-1].width > self.blocks[-2].x + self.blocks[-1].width:
                self.blocks[-1].width = (self.blocks[-2].x + self.blocks[-2].width) - self.blocks[-1].x
        self.blocks.append(Block(y=self.blocks[-1].y,
                                 velocity=2 * random.choice([1, -1]),
                                 factor=self.factor,
                                 width=self.blocks[-1].width))
        self.factor *= 1.1

    def update(self):
        self.blocks[-1].offscreen()
        for block in self.blocks:
            block.update()

    def restart(self):
        pass

    def stop(self):
        for block in self.blocks:
            block.velocity = 0

    def scroll(self):
        for block in self.blocks:
            block.y += BLOCK_SIZE * 3
        del self.blocks[:3]


class Block:
    def __init__(self, factor=1.0, velocity=0, y=HEIGHT, width=BLOCK_SIZE * 3):
        self.y = y - BLOCK_SIZE
        self.velocity = velocity * factor
        self.height, self.width = BLOCK_SIZE, width
        self.x = (WIDTH - self.width) / 2 if factor == 1 else random.randint(0, int(WIDTH - self.width))

    def update(self):
        self.x += self.velocity

    def draw(self, screen):
        r_add, g_add = (self.width % 155), (self.width % 200)
        pygame.draw.rect(screen, (100 + r_add, 55 + g_add, 255), (self.x, self.y, self.width, self.height))

    def offscreen(self):
        if self.x + self.width > WIDTH or self.x < 0:
            self.velocity *= -1


def main():
    clock = pygame.time.Clock()
    game = Game()
    game.add()
    while not game.lost:
        game.update()
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.add()
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
