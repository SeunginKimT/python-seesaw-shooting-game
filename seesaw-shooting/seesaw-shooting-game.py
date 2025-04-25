import pygame
import sys
import random

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 화면 설정
WIDTH = 800
HEIGHT = 600
FPS = 60

# 시소 설정
SEESAW_WIDTH = 140
SEESAW_HEIGHT = 20
SEESAW_SPEED = 8

# 캐릭터 설정
CHAR_WIDTH = 40
CHAR_HEIGHT = 80

# 레벨2 설정
CLOUD_SIZE = 50
RAINDROP_SIZE = 10
MOLE_SIZE = 40
BULLET_SIZE = 5


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Two Stage Game")
        self.clock = pygame.time.Clock()

        # 이미지 로드
        self.load_images()

        self.reset_game()

    def load_images(self):
        # 캐릭터 이미지 로드
        self.char1_img = pygame.image.load("images/performer1.png")  # 파란색 캐릭터
        self.char2_img = pygame.image.load("images/performer2.png")  # 빨간색 캐릭터

        # 이미지 크기 조정
        self.char1_img = pygame.transform.scale(self.char1_img, (CHAR_WIDTH, CHAR_HEIGHT))
        self.char2_img = pygame.transform.scale(self.char2_img, (CHAR_WIDTH, CHAR_HEIGHT))

        # 시소 이미지 로드
        self.seesaw_normal = pygame.image.load("images/seesaw2.png")  # 초기 상태
        self.seesaw_tilted = pygame.image.load("images/seesaw1.png")  # 기울어진 상태

        # 시소 이미지 크기 조정
        self.seesaw_normal = pygame.transform.scale(self.seesaw_normal, (SEESAW_WIDTH, SEESAW_HEIGHT))
        self.seesaw_tilted = pygame.transform.scale(self.seesaw_tilted, (SEESAW_WIDTH, SEESAW_HEIGHT))

        # 시소 상태 변수 추가
        self.seesaw_state = "normal"  # "normal" 또는 "tilted"

    def reset_game(self):
        self.running = True
        self.current_level = 1
        self.lives = 10

        # 게임 상태
        self.game_started = False
        self.background_y = 0
        self.new_background_y = -HEIGHT
        self.scrolling = False

        # 중력 및 점프 관련 변수
        self.GRAVITY = 0.3  # 중력 감소로 더 부드러운 낙하
        self.JUMP_SPEED = -20

        # 시소 관련 변수
        self.reset_seesaw()

        # 캐릭터 관련 변수
        self.reset_characters()

        # 레벨2 관련 변수
        self.reset_level2_objects()

    def reset_seesaw(self):
        self.seesaw_x = (WIDTH - SEESAW_WIDTH) // 2
        self.seesaw_y = HEIGHT - 100
        self.seesaw_speed = 0
        self.seesaw_angle = 0

    def reset_characters(self):
        # 캐릭터 1 (떨어지는 캐릭터)
        self.char1_x = -CHAR_WIDTH
        self.char1_y = 10  # 더 높은 위치에서 시작
        self.char1_vx = 6  # 수평 속도 약간 증가
        self.char1_vy = 1  # 초기 수직 속도 감소
        self.char1_jumping = False

        # 캐릭터 2 (시소 위의 캐릭터)
        self.char2_x = self.seesaw_x + SEESAW_WIDTH - CHAR_WIDTH
        self.char2_y = self.seesaw_y - CHAR_HEIGHT
        self.char2_vy = 0
        self.char2_jumping = False

    def reset_level2_objects(self):
        self.clouds = []
        self.raindrops = []
        self.moles = []
        self.bullets = []
        self.cloud_timer = 0
        self.rain_timer = 0
        self.mole_timer = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.start_game()
                elif event.key == pygame.K_SPACE and self.current_level == 2:
                    self.fire_bullet()

    def start_game(self):
        self.game_started = True
        self.char1_jumping = True
        self.char1_vy = 2

    def update_level1(self):
        if not self.game_started:
            return

        # 시소 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.seesaw_speed = -8
        elif keys[pygame.K_RIGHT]:
            self.seesaw_speed = 8
        else:
            self.seesaw_speed = 0

        self.seesaw_x += self.seesaw_speed
        self.seesaw_x = max(0, min(self.seesaw_x, WIDTH - SEESAW_WIDTH))

        # 캐릭터2 시소 위치에 고정 (점프 중이 아닐 때)
        if not self.char2_jumping:
            self.char2_x = self.seesaw_x + SEESAW_WIDTH - CHAR_WIDTH
            self.char2_y = self.seesaw_y - CHAR_HEIGHT

        # 캐릭터1 포물선 운동
        if self.char1_jumping:
            self.char1_x += self.char1_vx
            self.char1_vy += self.GRAVITY
            self.char1_y += self.char1_vy

            # 화면 범위 체크 - 바닥에 떨어졌을 때 게임오버 처리
            if self.char1_y > HEIGHT:
                self.game_over()
                return

            # 화면 왼쪽이나 오른쪽으로 벗어났을 때도 게임오버 처리
            if self.char1_x < -CHAR_WIDTH or self.char1_x > WIDTH:
                self.game_over()
                return

        # 캐릭터2 점프 업데이트
        if self.char2_jumping:
            self.char2_vy += self.GRAVITY * 0.5
            self.char2_y += self.char2_vy

            # 배경 스크롤링 (캐릭터2만 위로 올라가도록)
            if not self.scrolling and self.char2_y < HEIGHT / 3:
                self.scrolling = True

            if self.scrolling:
                scroll_speed = 5
                self.char2_y -= scroll_speed  # 캐릭터2만 위로 올라감

                if self.char2_y < -CHAR_HEIGHT:  # 화면을 완전히 벗어나면
                    self.current_level = 2
                    self.setup_level2()
                    return

        # 시소 충돌 체크
        self.check_collisions()

    def check_collisions(self):
        # 캐릭터1과 시소의 충돌 검사
        char1_rect = pygame.Rect(self.char1_x, self.char1_y, CHAR_WIDTH, CHAR_HEIGHT)
        seesaw_left = pygame.Rect(
            self.seesaw_x,
            self.seesaw_y,
            SEESAW_WIDTH // 2,
            SEESAW_HEIGHT
        )

        # 캐릭터1이 시소의 왼쪽에 착지했는지 확인
        if char1_rect.colliderect(seesaw_left) and self.char1_vy > 0:
            if not self.char2_jumping:
                self.char2_jumping = True
                self.char2_vy = self.JUMP_SPEED
                self.char1_jumping = False
                self.seesaw_state = "tilted"  # 시소 상태 변경
    def setup_level2(self):
        # 레벨 2 시작할 때 캐릭터 위치 초기화
        self.char2_x = WIDTH // 2
        self.char2_y = HEIGHT - CHAR_HEIGHT - 20
        self.clouds = []
        self.raindrops = []
        self.moles = []
        self.bullets = []

    def create_cloud(self):
        cloud = {
            'x': random.randint(0, WIDTH - CLOUD_SIZE),
            'y': -CLOUD_SIZE,
            'speed': random.randint(1, 3)
        }
        self.clouds.append(cloud)

    def create_raindrop(self):
        for cloud in self.clouds:
            raindrop = {
                'x': cloud['x'] + CLOUD_SIZE // 2,
                'y': cloud['y'] + CLOUD_SIZE,
                'speed': random.randint(5, 8)
            }
            self.raindrops.append(raindrop)

    def create_mole(self):
        mole = {
            'x': random.randint(0, WIDTH - MOLE_SIZE),
            'y': HEIGHT,
            'speed': random.randint(2, 4)
        }
        self.moles.append(mole)

    def fire_bullet(self):
        bullet = {
            'x': self.char2_x + CHAR_WIDTH // 2,
            'y': self.char2_y,
            'speed': -10
        }
        self.bullets.append(bullet)

    def update_clouds(self):
        for cloud in self.clouds[:]:
            cloud['y'] += cloud['speed']
            if cloud['y'] > HEIGHT:
                self.clouds.remove(cloud)

    def update_raindrops(self):
        for drop in self.raindrops[:]:
            drop['y'] += drop['speed']
            if drop['y'] > HEIGHT:
                self.raindrops.remove(drop)

    def update_moles(self):
        for mole in self.moles[:]:
            mole['y'] -= mole['speed']
            if mole['y'] < HEIGHT - 200:  # 일정 높이까지만 올라감
                self.moles.remove(mole)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['y'] += bullet['speed']
            if bullet['y'] < 0:
                self.bullets.remove(bullet)

    def update_level2(self):
        # 캐릭터 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.char2_x = max(0, self.char2_x - 5)
        if keys[pygame.K_RIGHT]:
            self.char2_x = min(WIDTH - CHAR_WIDTH, self.char2_x + 5)

        # 구름 생성
        self.cloud_timer += 1
        if self.cloud_timer >= 60:
            self.create_cloud()
            self.cloud_timer = 0

        # 빗방울 생성
        self.rain_timer += 1
        if self.rain_timer >= 300:
            self.create_raindrop()
            self.rain_timer = 0

        # 두더지 생성
        self.mole_timer += 1
        if self.mole_timer >= 180:
            self.create_mole()
            self.mole_timer = 0

        # 오브젝트 업데이트
        self.update_clouds()
        self.update_raindrops()
        self.update_moles()
        self.update_bullets()

        # 충돌 체크
        self.check_level2_collisions()

    def check_level2_collisions(self):
        char_rect = pygame.Rect(self.char2_x, self.char2_y, CHAR_WIDTH, CHAR_HEIGHT)

        # 빗방울과 충돌
        for drop in self.raindrops[:]:
            drop_rect = pygame.Rect(drop['x'], drop['y'], RAINDROP_SIZE, RAINDROP_SIZE)
            if char_rect.colliderect(drop_rect):
                self.lives -= 1
                self.raindrops.remove(drop)
                if self.lives <= 0:
                    self.game_over()

        # 총알과 구름 충돌
        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE)
            for cloud in self.clouds[:]:
                cloud_rect = pygame.Rect(cloud['x'], cloud['y'], CLOUD_SIZE, CLOUD_SIZE)
                if bullet_rect.colliderect(cloud_rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if cloud in self.clouds:
                        self.clouds.remove(cloud)

    def game_over(self):
        # 게임 오버 화면 표시
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render('GAME OVER', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        # 2초 대기
        pygame.time.wait(2000)

        # 게임 리셋
        self.reset_game()
    def draw(self):
        self.screen.fill(BLACK)

        if self.current_level == 1:
            # 배경 그리기
            pygame.draw.rect(self.screen, (20, 20, 20), (0, self.background_y, WIDTH, HEIGHT))
            if self.scrolling:
                pygame.draw.rect(self.screen, (40, 40, 40), (0, self.new_background_y, WIDTH, HEIGHT))


            if not self.game_started:
                font = pygame.font.Font(None, 74)
                text = font.render('PRESS SPACE TO START', True, WHITE)
                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                self.screen.blit(text, text_rect)


            if self.seesaw_state == "normal":
                self.screen.blit(self.seesaw_normal, (self.seesaw_x, self.seesaw_y))
            else:
                self.screen.blit(self.seesaw_tilted, (self.seesaw_x, self.seesaw_y))


            if self.game_started:
                self.screen.blit(self.char1_img, (self.char1_x, self.char1_y))  # 파란색 캐릭터
                self.screen.blit(self.char2_img, (self.char2_x, self.char2_y))  # 빨간색 캐릭터

        elif self.current_level == 2:

            self.screen.fill((40, 40, 40))


            font = pygame.font.Font(None, 74)
            text = font.render('LEVEL 2', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, 50))
            self.screen.blit(text, text_rect)


            lives_font = pygame.font.Font(None, 36)
            lives_text = lives_font.render(f'Lives: {self.lives}', True, WHITE)
            self.screen.blit(lives_text, (10, 10))


            for cloud in self.clouds:
                pygame.draw.rect(self.screen, WHITE,
                               (cloud['x'], cloud['y'], CLOUD_SIZE, CLOUD_SIZE))


            for drop in self.raindrops:
                pygame.draw.rect(self.screen, (0, 191, 255),
                               (drop['x'], drop['y'], RAINDROP_SIZE, RAINDROP_SIZE))


            for mole in self.moles:
                pygame.draw.rect(self.screen, (139, 69, 19),
                               (mole['x'], mole['y'], MOLE_SIZE, MOLE_SIZE))


            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255, 255, 0),
                               (bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE))


            self.screen.blit(self.char2_img, (self.char2_x, self.char2_y))

        pygame.display.flip()


    def run(self):
        while self.running:
            self.handle_input()

            if self.current_level == 1:
                self.update_level1()
            elif self.current_level == 2:
                self.update_level2()

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()