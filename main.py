import os
from pathlib import Path

import pygame


WINDOW_SIZE = (1920,1080)
WINDOW_TITLE = "SPBP"
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# 矩形的四个数字分别是左上角的 x、y 坐标，以及宽、高。
START_BUTTON = pygame.Rect(370, 245, 220, 52)
EXIT_BUTTON = pygame.Rect(370, 317, 220, 52)
BACK_BUTTON = pygame.Rect(370, 317, 220, 52)


def draw_text(screen, font, label, center):
    """把文字画在指定中心点，改文字长度时仍能保持居中。"""
    surface = font.render(label, True, TEXT_COLOR)
    screen.blit(surface, surface.get_rect(center=center))


def draw_button(screen, font, label, rect):
    pygame.draw.rect(screen, TEXT_COLOR, rect, width=1)
    draw_text(screen, font, label, rect.center)


def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        clock = pygame.time.Clock()

        # 直接查看 Windows 字体目录，避开 Pygame 的字体注册表扫描。
        # 没有可用中文字体时，用 Pygame 自带字体显示英文。
        fonts_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        font_path = next(
            (str(fonts_dir / name) for name in ("msyh.ttc", "simhei.ttf", "simsun.ttc")
             if (fonts_dir / name).is_file()),
            None,
        )
        title_font = pygame.font.Font(font_path, 48)
        button_font = pygame.font.Font(font_path, 28)
        if font_path:
            title, start, exit_label, setup, back = (
                WINDOW_TITLE, "开始", "退出", "准备游戏", "返回"
            )
        else:
            title, start, exit_label, setup, back = (
                "Selling Pounds by the Pound", "Start", "Exit", "Game Setup", "Back"
            )

        page = "menu"
        while True:
            # 先处理输入。用事件记录的坐标判断点击是否落在按钮内。
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if page == "menu":
                        if START_BUTTON.collidepoint(event.pos):
                            page = "setup"
                        elif EXIT_BUTTON.collidepoint(event.pos):
                            return
                    elif BACK_BUTTON.collidepoint(event.pos):
                        page = "menu"

            # 每帧先用黑色清掉上一帧，再画当前页面并刷新窗口。
            screen.fill(BACKGROUND_COLOR)
            if page == "menu":
                draw_text(screen, title_font, title, (480, 160))
                draw_button(screen, button_font, start, START_BUTTON)
                draw_button(screen, button_font, exit_label, EXIT_BUTTON)
            else:
                draw_text(screen, title_font, setup, (480, 160))
                draw_button(screen, button_font, back, BACK_BUTTON)
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
