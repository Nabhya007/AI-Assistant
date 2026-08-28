import pygame
import math
import random
import time


class JarvisVisual:

    def __init__(self):

        pygame.init()

        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        self.width = 1536
        self.height = 960

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.NOFRAME
        )

        pygame.display.set_caption("JARVIS")

        self.clock = pygame.time.Clock()

        # -------------------------------------------------
        # STATE
        # -------------------------------------------------

        self.visible = False
        self.running = True

        self.status = "SYSTEM ONLINE"

        self.angle = 0
        self.radar_angle = 0
        self.pulse = 0

        self.start_time = time.time()

        # -------------------------------------------------
        # FONTS
        # -------------------------------------------------

        self.font_title = pygame.font.SysFont(
            "Arial",
            46,
            bold=True
        )

        self.font_big = pygame.font.SysFont(
            "Arial",
            34,
            bold=True
        )

        self.font_medium = pygame.font.SysFont(
            "Arial",
            22
        )

        self.font_small = pygame.font.SysFont(
            "Arial",
            16
        )

        self.font_tiny = pygame.font.SysFont(
            "Arial",
            13
        )

        # -------------------------------------------------
        # PARTICLES
        # -------------------------------------------------

        self.particles = []

        for _ in range(180):

            self.particles.append([
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.uniform(0.2, 1.2),
                random.randint(1, 3)
            ])

        # -------------------------------------------------
        # WAVEFORM
        # -------------------------------------------------

        self.waveform = [
            random.randint(5, 35)
            for _ in range(90)
        ]

        # -------------------------------------------------
        # GRID
        # -------------------------------------------------

        self.grid_offset = 0


    # =====================================================
    # SHOW
    # =====================================================

    def show(self, status="SYSTEM ONLINE"):

        self.visible = True
        self.status = status

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.NOFRAME
        )

        pygame.mouse.set_visible(False)


    # =====================================================
    # HIDE
    # =====================================================

    def hide(self):

        self.visible = False

        pygame.mouse.set_visible(True)

        pygame.display.iconify()


    # =====================================================
    # STATUS
    # =====================================================

    def set_status(self, status):

        self.status = status


    # =====================================================
    # TEXT HELPER
    # =====================================================

    def text(
        self,
        text,
        font,
        x,
        y,
        color=(0, 200, 255),
        center=False
    ):

        surface = font.render(
            text,
            True,
            color
        )

        if center:

            rect = surface.get_rect(
                center=(x, y)
            )

        else:

            rect = surface.get_rect(
                topleft=(x, y)
            )

        self.screen.blit(
            surface,
            rect
        )


    # =====================================================
    # PANEL
    # =====================================================

    def panel(
        self,
        x,
        y,
        width,
        height,
        title
    ):

        # Dark transparent-style panel
        pygame.draw.rect(
            self.screen,
            (3, 12, 22),
            (x, y, width, height)
        )

        # Border
        pygame.draw.rect(
            self.screen,
            (0, 90, 130),
            (x, y, width, height),
            1
        )

        # Top accent
        pygame.draw.line(
            self.screen,
            (0, 190, 255),
            (x + 15, y),
            (x + 130, y),
            2
        )

        # Corner cuts

        pygame.draw.line(
            self.screen,
            (0, 130, 180),
            (x, y + 20),
            (x + 20, y),
            1
        )

        pygame.draw.line(
            self.screen,
            (0, 130, 180),
            (x + width - 20, y + height),
            (x + width, y + height - 20),
            1
        )

        self.text(
            title.upper(),
            self.font_small,
            x + 18,
            y + 12,
            (0, 190, 240)
        )


    # =====================================================
    # PARTICLES
    # =====================================================

    def draw_particles(self):

        for particle in self.particles:

            x, y, speed, size = particle

            y -= speed

            if y < 0:

                y = self.height

                x = random.randint(
                    0,
                    self.width
                )

            particle[0] = x
            particle[1] = y

            pygame.draw.circle(
                self.screen,
                (0, 70, 110),
                (int(x), int(y)),
                size
            )


    # =====================================================
    # GRID
    # =====================================================

    def draw_grid(self):

        self.grid_offset += 0.6

        horizon = 760

        # Horizontal lines

        for i in range(12):

            y = horizon + (
                i * 22
            ) + self.grid_offset % 22

            if y >= self.height:
                continue

            pygame.draw.line(
                self.screen,
                (0, 35, 55),
                (0, y),
                (self.width, y),
                1
            )

        # Vertical perspective lines

        center_x = self.width // 2

        for x in range(
            -self.width,
            self.width * 2,
            90
        ):

            pygame.draw.line(
                self.screen,
                (0, 30, 50),
                (center_x, horizon),
                (x, self.height),
                1
            )


    # =====================================================
    # CENTRAL HUD
    # =====================================================

    def draw_core(self):

        cx = self.width // 2
        cy = 455

        self.angle += 0.8

        self.radar_angle += 2.0

        pulse = (
            math.sin(
                time.time() * 3
            ) * 5
        )

        # -------------------------------------------------
        # Faint glow rings
        # -------------------------------------------------

        for radius in [115, 145, 180, 220, 265]:

            pygame.draw.circle(
                self.screen,
                (0, 45, 75),
                (cx, cy),
                int(radius + pulse),
                1
            )

        # -------------------------------------------------
        # Technical outer ring
        # -------------------------------------------------

        pygame.draw.circle(
            self.screen,
            (0, 130, 190),
            (cx, cy),
            270,
            2
        )

        # -------------------------------------------------
        # Rotating segmented ring
        # -------------------------------------------------

        for i in range(36):

            angle = math.radians(
                self.angle + i * 10
            )

            r1 = 245
            r2 = 265

            x1 = cx + math.cos(angle) * r1
            y1 = cy + math.sin(angle) * r1

            x2 = cx + math.cos(angle) * r2
            y2 = cy + math.sin(angle) * r2

            if i % 3 == 0:

                color = (
                    0,
                    210,
                    255
                )

            else:

                color = (
                    0,
                    80,
                    120
                )

            pygame.draw.line(
                self.screen,
                color,
                (x1, y1),
                (x2, y2),
                2
            )

        # -------------------------------------------------
        # Inner rotating ring
        # -------------------------------------------------

        for i in range(12):

            angle = math.radians(
                -self.angle * 1.5 +
                i * 30
            )

            r1 = 155
            r2 = 185

            x1 = cx + math.cos(angle) * r1
            y1 = cy + math.sin(angle) * r1

            x2 = cx + math.cos(angle) * r2
            y2 = cy + math.sin(angle) * r2

            pygame.draw.line(
                self.screen,
                (0, 180, 255),
                (x1, y1),
                (x2, y2),
                3
            )

        # -------------------------------------------------
        # Radar sweep
        # -------------------------------------------------

        radar = math.radians(
            self.radar_angle
        )

        radar_length = 220

        rx = (
            cx +
            math.cos(radar) *
            radar_length
        )

        ry = (
            cy +
            math.sin(radar) *
            radar_length
        )

        pygame.draw.line(
            self.screen,
            (0, 255, 255),
            (cx, cy),
            (rx, ry),
            2
        )

        # -------------------------------------------------
        # Core
        # -------------------------------------------------

        core_radius = int(
            62 + pulse
        )

        pygame.draw.circle(
            self.screen,
            (0, 80, 130),
            (cx, cy),
            core_radius + 18,
            3
        )

        pygame.draw.circle(
            self.screen,
            (0, 160, 230),
            (cx, cy),
            core_radius,
            2
        )

        pygame.draw.circle(
            self.screen,
            (0, 100, 180),
            (cx, cy),
            42
        )

        pygame.draw.circle(
            self.screen,
            (120, 230, 255),
            (cx, cy),
            6
        )

        # -------------------------------------------------
        # JARVIS
        # -------------------------------------------------

        self.text(
            "JARVIS",
            self.font_big,
            cx,
            cy,
            (180, 245, 255),
            center=True
        )


    # =====================================================
    # WAVEFORM
    # =====================================================

    def draw_waveform(
        self,
        x,
        y,
        width,
        height
    ):

        bar_width = width / len(
            self.waveform
        )

        for i in range(
            len(self.waveform)
        ):

            value = (
                self.waveform[i] +
                random.randint(-5, 5)
            )

            value = max(
                3,
                min(
                    height,
                    value
                )
            )

            pygame.draw.rect(
                self.screen,
                (0, 170, 230),
                (
                    int(
                        x + i * bar_width
                    ),
                    int(
                        y + height - value
                    ),
                    2,
                    int(value)
                )
            )


    # =====================================================
    # STATUS PANEL
    # =====================================================

    def draw_status_panel(self):

        x = 25
        y = 130

        self.panel(
            x,
            y,
            350,
            230,
            "SYSTEM STATUS"
        )

        systems = [
            "POWER CORE",
            "MEMORY",
            "CPU",
            "NETWORK",
            "AUDIO SYSTEM",
            "VISION SYSTEM"
        ]

        for i, system in enumerate(
            systems
        ):

            yy = y + 55 + i * 27

            pygame.draw.circle(
                self.screen,
                (0, 210, 255),
                (x + 25, yy + 5),
                3
            )

            self.text(
                system,
                self.font_tiny,
                x + 38,
                yy,
                (150, 200, 215)
            )

            self.text(
                "ONLINE",
                self.font_tiny,
                x + 275,
                yy,
                (0, 220, 255)
            )


    # =====================================================
    # AUDIO PANEL
    # =====================================================

    def draw_audio_panel(self):

        x = 25
        y = 385

        self.panel(
            x,
            y,
            350,
            170,
            "VOICE RECOGNITION"
        )

        self.draw_waveform(
            x + 20,
            y + 55,
            310,
            65
        )

        self.text(
            "LISTENING...",
            self.font_small,
            x + 220,
            y + 130,
            (0, 220, 255)
        )


    # =====================================================
    # NETWORK PANEL
    # =====================================================

    def draw_network_panel(self):

        x = 25
        y = 570

        self.panel(
            x,
            y,
            350,
            190,
            "NETWORK STATUS"
        )

        # Fake network map

        for i in range(12):

            px = (
                x +
                30 +
                random.randint(
                    0,
                    280
                )
            )

            py = (
                y +
                55 +
                random.randint(
                    0,
                    90
                )
            )

            pygame.draw.circle(
                self.screen,
                (0, 150, 220),
                (px, py),
                2
            )

        self.text(
            "GLOBAL SECURE NETWORK",
            self.font_tiny,
            x + 20,
            y + 145,
            (0, 180, 230)
        )

        self.text(
            "ENCRYPTED",
            self.font_tiny,
            x + 20,
            y + 165,
            (0, 220, 255)
        )


    # =====================================================
    # RIGHT STATUS PANEL
    # =====================================================

    def draw_monitor_panel(self):

        x = 1160
        y = 385

        self.panel(
            x,
            y,
            350,
            230,
            "SYSTEM MONITOR"
        )

        values = [
            ("PROCESSOR", 68),
            ("MEMORY", 72),
            ("STORAGE", 83),
            ("NETWORK", 91),
            ("GPU", 74)
        ]

        for i, (name, value) in enumerate(
            values
        ):

            yy = y + 55 + i * 32

            self.text(
                name,
                self.font_tiny,
                x + 20,
                yy,
                (150, 190, 210)
            )

            pygame.draw.rect(
                self.screen,
                (8, 35, 50),
                (
                    x + 130,
                    yy + 3,
                    150,
                    9
                )
            )

            pygame.draw.rect(
                self.screen,
                (0, 180, 240),
                (
                    x + 130,
                    yy + 3,
                    int(
                        150 *
                        value /
                        100
                    ),
                    9
                )
            )

            self.text(
                f"{value}%",
                self.font_tiny,
                x + 290,
                yy,
                (0, 210, 255)
            )


    # =====================================================
    # PROTOCOL PANEL
    # =====================================================

    def draw_protocol_panel(self):

        x = 1160
        y = 130

        self.panel(
            x,
            y,
            350,
            220,
            "ACTIVE PROTOCOL"
        )

        self.text(
            "JARVIS CORE PROTOCOL",
            self.font_medium,
            x + 20,
            y + 60,
            (0, 210, 255)
        )

        self.text(
            "AI SYSTEMS NOMINAL",
            self.font_small,
            x + 20,
            y + 105,
            (150, 210, 220)
        )

        pygame.draw.rect(
            self.screen,
            (10, 40, 55),
            (
                x + 20,
                y + 140,
                250,
                8
            )
        )

        pygame.draw.rect(
            self.screen,
            (0, 190, 245),
            (
                x + 20,
                y + 140,
                215,
                8
            )
        )


    # =====================================================
    # CLOCK
    # =====================================================

    def draw_clock(self):

        current_time = time.strftime(
            "%H:%M:%S"
        )

        current_date = time.strftime(
            "%A, %d %B %Y"
        )

        self.text(
            current_time,
            self.font_big,
            self.width - 190,
            30,
            (180, 240, 255)
        )

        self.text(
            current_date.upper(),
            self.font_tiny,
            self.width - 190,
            72,
            (0, 170, 220)
        )


    # =====================================================
    # HEADER
    # =====================================================

    def draw_header(self):

        self.text(
            "J A R V I S",
            self.font_title,
            25,
            20,
            (170, 240, 255)
        )

        self.text(
            "JUST A RATHER VERY INTELLIGENT SYSTEM",
            self.font_tiny,
            27,
            72,
            (0, 150, 200)
        )

        # Center status

        self.text(
            "●  SYSTEM ONLINE  ●",
            self.font_small,
            self.width // 2,
            30,
            (0, 220, 255),
            center=True
        )


    # =====================================================
    # BOTTOM STATUS
    # =====================================================

    def draw_bottom(self):

        self.text(
            "JARVIS ONLINE",
            self.font_big,
            self.width // 2,
            820,
            (180, 240, 255),
            center=True
        )

        self.text(
            self.status,
            self.font_medium,
            self.width // 2,
            860,
            (0, 190, 240),
            center=True
        )

        # Bottom interface line

        pygame.draw.line(
            self.screen,
            (0, 100, 150),
            (400, 920),
            (1135, 920),
            1
        )


    # =====================================================
    # DRAW EVERYTHING
    # =====================================================

    def draw(self):

        if not self.visible:
            return

        # Background

        self.screen.fill(
            (1, 5, 10)
        )

        # Layers

        self.draw_particles()

        self.draw_grid()

        self.draw_header()

        self.draw_clock()

        self.draw_core()

        self.draw_status_panel()

        self.draw_audio_panel()

        self.draw_network_panel()

        self.draw_protocol_panel()

        self.draw_monitor_panel()

        self.draw_bottom()

        pygame.display.flip()


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        if not self.visible:
            return

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.hide()

                    return

        self.draw()

        self.clock.tick(60)


    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.running = False

        pygame.mouse.set_visible(True)

        pygame.quit()