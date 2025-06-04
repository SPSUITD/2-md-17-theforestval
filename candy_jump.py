import math
import arcade
import arcade.gui

# константы
# окно игры и название
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Candy Jump"

# размер тайл-карты
TILE_SCALING = 1
# скорость  персонажа
PLAYER_MOVEMENT_SPEED = 5
# скорость изменения анимации
PLAYER_SPRITE_IMAGE_CHANGE_SPEED = 30
# гравитация
GRAVITY = 1.0
# скорость  прыжка
PLAYER_JUMP_SPEED = 20
# количество уровней
NUMBER_OF_LEVELS = 2

# класс окна выигрыша
class WinView(arcade.View):

    def __init__(self, score, sweetscore, total_time_print, level, NUMBER_OF_LEVELS): 
        super().__init__()
        self.score = score
        self.sweetscore = sweetscore
        self.total_time_print = total_time_print
        self.level = level

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BRINK_PINK) 

    def on_draw(self):
        self.clear()
        arcade.draw_text("VICTORY!", self.window.width / 2, self.window.height / 2 + 80,
                         arcade.color.CAPUT_MORTUUM, font_size=60, bold=True, font_name=("Cooper"), anchor_x="center")
        
        arcade.draw_text("VICTORY!", self.window.width / 2 - 5, self.window.height / 2 + 85,
                         arcade.color.WHITE, font_size=60, bold=True, font_name=("Cooper"), anchor_x="center")

        arcade.draw_text(f"coins: {self.score}", self.window.width / 2, self.window.height / 2 - 30,
                         arcade.color.CAPUT_MORTUUM, font_size=22, font_name=("Arial"), anchor_x="center")

        arcade.draw_text(f"cakes: {self.sweetscore}", self.window.width / 2, self.window.height / 2 - 70,
                         arcade.color.CAPUT_MORTUUM, font_size=22, font_name=("Arial"), anchor_x="center")

        arcade.draw_text(f"time: {self.total_time_print}", self.window.width / 2, self.window.height / 2 - 110,
                         arcade.color.CAPUT_MORTUUM, font_size=22, font_name=("Arial"), anchor_x="center")

        arcade.draw_text("press SPACE to next level", self.window.width / 2, self.window.height / 2 - 170,
                         arcade.color.CORDOVAN, font_size=20, font_name=("Arial"), anchor_x="center")
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.level < NUMBER_OF_LEVELS:
            # переход на следующий уровень
                main_view = MainView()
                main_view.level = self.level + 1  # следующий уровень
                main_view.setup()
                self.window.show_view(main_view)
            else:
            # конец уровней
                menu_view = MenuView(None)
                self.window.show_view(menu_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()

# класс окна проигрыша
class GameOverView(arcade.View):

    def __init__(self, score, sweetscore, total_time_print):
        super().__init__()
        self.score = score
        self.sweetscore = sweetscore
        self.total_time_print = total_time_print 

    def on_show_view(self):
        arcade.set_background_color(arcade.color.CAPUT_MORTUUM)

    def on_draw(self):
        self.clear()
        arcade.draw_text("GAME OVER!", self.window.width / 2, self.window.height / 2 + 80,
                         arcade.color.CAMEL, font_size=60, bold=True, font_name=("Cooper"), anchor_x="center")
        
        arcade.draw_text("GAME OVER!", self.window.width / 2 - 5, self.window.height / 2 + 85,
                         arcade.color.COSMIC_LATTE, font_size=60, bold=True, font_name=("Cooper"), anchor_x="center")
        
        arcade.draw_text("mistake: the cake was assembled on a set table", self.window.width / 2, self.window.height / 2 + 30,
                         arcade.color.COSMIC_LATTE, font_size=22, bold=True, font_name=("Arial"), anchor_x="center")
        
        arcade.draw_text(f"coins: {self.score}", self.window.width / 2, self.window.height / 2 - 30,
                         arcade.color.DEER, font_size=22, font_name=("Arial"), anchor_x="center")
        
        arcade.draw_text(f"cakes: {self.sweetscore}", self.window.width / 2, self.window.height / 2 - 70,
                         arcade.color.DEER, font_size=22, font_name=("Arial"), anchor_x="center")
        
        arcade.draw_text(f"time: {self.total_time_print}", self.window.width / 2, self.window.height / 2 - 110,
                         arcade.color.DEER, font_size=22, font_name=("Arial"), anchor_x="center")

        arcade.draw_text("press SPACE to restart", self.window.width / 2, self.window.height / 2 - 170,
                         arcade.color.CORDOVAN, font_size=20, font_name=("Arial"), anchor_x="center")
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            main_view = MainView()
            main_view.setup()
            self.window.show_view(main_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

# класс игры
class MainView(arcade.View):

    def __init__(self):
        super().__init__()
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite = None
        self.coins_text = 0
        self.cakes_text = 0
        self.time_text = 0
        self.total_time = 0
        self.total_time_print = 0
        self.total_coins_on_map = 0 
        self.total_cakes_on_map = 0 
        self.player_sprite_go = []
        self.manager = arcade.gui.UIManager()

        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BRINK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=15
                ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BAKER_MILLER_PINK,              
                font_color=arcade.color.WHITE,    
                font_size=15
                ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.DARK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=15
                )
        }

        switch_menu_button = arcade.gui.UIFlatButton(text="| |", width=55, height = 55, style=button_style)
        self.end_of_map = 0
        self.level = 1

        # открытие меню по нажатию кнопки
        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        # местоположение кнопки паузы
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="right",
            anchor_y="top",
            child=switch_menu_button,
        )

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.COSMIC_LATTE)
        self.manager.enable()

    def setup(self):

        # камеры
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # загрузка карты с тайлами
        map_name = f"maps/map{self.level}.json" 
        layer_options = {
            "platforms1": {"use_spatial_hash": True},
            "platforms2": {"use_spatial_hash": True},
            "cakes": {"use_spatial_hash": True},
            "fakecakes": {"use_spatial_hash": True},
            "coins": {"use_spatial_hash": True}
        }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # подсчет количества монет на карте
        if "coins" in self.scene:
            self.total_coins_on_map = len(self.scene["coins"])
        else:
            self.total_coins_on_map = 0

        # подсчет количества тортов на карте
        if "cakes" in self.scene:
            self.total_cakes_on_map = len(self.scene["cakes"])
        else:
            self.total_cakes_on_map = 0

        # загрузка персонажки и установка изначальной позиции
        self.player_sprite = arcade.Sprite()
        for i in range(1, 9):
            self.player_sprite_go.append(arcade.load_texture(f"img/go({i}).png"))
        self.player_sprite.texture = self.player_sprite_go[1]
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 256

        # добавление игрока в сцену
        self.scene.add_sprite_list("Player", use_spatial_hash=False)
        self.scene["Player"].append(self.player_sprite)

        # создание списка слоев тайлов
        walls = arcade.SpriteList()
        walls.extend(self.scene["platforms1"])
        walls.extend(self.scene["platforms2"])
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=walls)

        # доп элементы
        self.background_color = arcade.color.COSMIC_LATTE 
        self.score = 0
        self.sweetscore = 0 
        self.coins_text = arcade.Text(f"coins: {self.score}", 15, 15, arcade.color.CAPUT_MORTUUM, 15)
        self.cakes_text = arcade.Text(f"cakes: {self.sweetscore}", 140, 15, arcade.color.CAPUT_MORTUUM, 15)    
        self.time_text = arcade.Text(f"time: {self.total_time_print}", 265, 15, arcade.color.CAPUT_MORTUUM, 15)

    def on_draw(self):

        # чистка экрана
        self.clear()

        # отрисовка игровой сцены
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        self.manager.draw()
    
        # отрисовка доп элементов
        self.coins_text.draw()
        self.cakes_text.draw()
        self.time_text.draw()

    # настройка камеры
    def center_camera_to_player(self):

        # размеры карты в пикселях
        map_width = self.tile_map.width * self.tile_map.tile_width # ширина карты умножается на ширину одного тайла
        map_height = self.tile_map.height * self.tile_map.tile_height  # высота карты умножается на высоту одного тайла

        # центрирование камеры на игроке
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.player_sprite.center_y

        # границы камеры
        min_x = self.camera.viewport_width / 2
        max_x = map_width - self.camera.viewport_width / 2
        min_y = self.camera.viewport_height / 2
        max_y = map_height + self.camera.viewport_height / 2

        # ограничение на выход за край карты
        screen_center_x = max(min_x, min(screen_center_x, max_x))
        screen_center_y = max(min_y, min(screen_center_y, max_y))

        self.camera.position = (screen_center_x, screen_center_y)

    def on_update(self, delta_time):

        # обновление камеры
        self.center_camera_to_player()

        # обновление времени
        self.total_time += delta_time

        # обновление физики
        self.physics_engine.update()

        if "fakecakes" in self.scene: # проверка, что слой существует
            fakecakes_collected = arcade.check_for_collision_with_list(self.player_sprite, self.scene["fakecakes"]) # проверка столкновений персонажа с элементом слоя
            for cake in fakecakes_collected:
                cake.remove_from_sprite_lists()
                game_over_view = GameOverView(self.score, self.sweetscore, self.total_time_print)
                self.window.show_view(game_over_view) 
                return 
            
        if "cakes" in self.scene: # проверка, что слой существует
            cakes_collected = arcade.check_for_collision_with_list(self.player_sprite, self.scene["cakes"]) # проверка столкновений персонажа с элементом слоя
            for cake in cakes_collected:
                cake.remove_from_sprite_lists()
                self.sweetscore += 1
                self.cakes_text.text = f"cakes: {self.sweetscore}" # вывод количества на экран в процессе сбора

        if "coins" in self.scene: # проверка, что слой существует
            coins_collected = arcade.check_for_collision_with_list(self.player_sprite, self.scene["coins"]) # проверка столкновений персонажа с элементом слоя
            for coin in coins_collected:
                coin.remove_from_sprite_lists()
                self.score += 1
                self.coins_text.text = f"coins: {self.score}" # вывод количества на экран в процессе сбора

        # анимация бега
        if self.physics_engine.can_jump(): # проверка персонажа на поверхности
            if self.player_sprite.change_x != 0: # проверка движения по горизонтали
                frame = int(self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 8
                self.player_sprite.texture = self.player_sprite_go[frame] # обычная текстура вправо
    
        # время
        ms, sec = math.modf(self.total_time)
        minutes = int(sec) // 60
        seconds = int(sec) % 60
        msec = int(ms*100)
        self.total_time_print = f"{minutes:02d}:{seconds:02d}:{msec:02d}"
        self.time_text.text = f"time: {self.total_time_print}"

        # проверка условия победы
        if (self.score == self.total_coins_on_map and self.total_coins_on_map > 0) and (self.sweetscore == self.total_cakes_on_map and self.total_cakes_on_map > 0):
            win_view = WinView(self.score, self.sweetscore, self.total_time_print, self.level, NUMBER_OF_LEVELS)
            self.window.show_view(win_view)
            return 

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

# класс меню
class MenuView(arcade.View):

    def __init__(self, main_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BRINK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=20,
                font_name=("Arial"),
                ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BAKER_MILLER_PINK,              
                font_color=arcade.color.WHITE,    
                font_size=20,
                font_name=("Arial"),
                ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.DARK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=20,
                font_name=("Arial"),
                )
        }

        resume_button = arcade.gui.UIFlatButton(text="resume", width=250, style = button_style)
        start_new_game_button = arcade.gui.UIFlatButton(text="start new game", width=250, style=button_style)
        rules_button = arcade.gui.UIFlatButton(text="rules", width=250, style=button_style)
        exit_button = arcade.gui.UIFlatButton(text="exit", width=250, style=button_style)

        # создание сетки для расположения кнопок
        self.grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=20
        )

        # добавление кнопок
        self.grid.add(resume_button, column=0, row=0)
        self.grid.add(start_new_game_button, column=1, row=0)
        self.grid.add(rules_button, column=0, row=1)
        self.grid.add(exit_button, column=1, row=1)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-50,
            child=self.grid,
        )

        self.main_view = main_view

        @resume_button.event("on_click")
        def on_click_resume_button(event):
            self.window.show_view(self.main_view)

        @start_new_game_button.event("on_click")
        def on_click_start_new_game_button(event):
            main_view = MainView()
            main_view.setup()
            self.window.show_view(main_view)

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        @rules_button.event("on_click")
        def on_click_volume_button(event):
            volume_menu = SubMenu(
                "Rules",
                "main task: collect all coins and cakes on the map",
                "notes: avoid cakes on set tables",
            )
            self.manager.add(volume_menu, layer=1)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):

        arcade.set_background_color(arcade.color.NAVAJO_WHITE)
        self.manager.enable()

    def on_draw(self):
        self.clear()

        arcade.draw_text("Candy Jump!", self.window.width / 2, self.window.height / 2 + 80,
                         arcade.color.BRINK_PINK, font_size=70, bold=True, font_name=("Cooper"), anchor_x="center")
        
        arcade.draw_text("Candy Jump!", self.window.width / 2 - 5, self.window.height / 2 + 85,
                         arcade.color.WHITE, font_size=70, bold=True, font_name=("Cooper"), anchor_x="center")
        
        self.manager.draw()

# класс сабменю
class SubMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):

    def __init__(
        self,
        title: str,
        input_text1: str,
        input_text2: str,
    ):
        super().__init__(size_hint=(1, 1))

        # установка дополнительного окна
        frame = self.add(arcade.gui.UIAnchorLayout(width=375, height=450, size_hint=None))
        frame.with_padding(all=5)

        # фон
        frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=10,
                right=10,
                bottom=10,
                top=10,
                texture=arcade.load_texture(
                    "img\фон.png"
                ),
            )
        )

        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BRINK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=20,
                font_name=("Arial"),
                ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.BAKER_MILLER_PINK,              
                font_color=arcade.color.WHITE,    
                font_size=20,
                font_name=("Arial"),
                ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                bg=arcade.color.DARK_PINK,        
                font_color=arcade.color.WHITE,     
                font_size=20,
                font_name=("Arial"),
                )
        }

        # кнопка выхода в основное меню
        back_button = arcade.gui.UIFlatButton(text="back", width=325, height=50, style=button_style)
        back_button.on_click = self.on_click_back_button

        # фото локации которую нужно избегать
        texture = arcade.load_texture("img/правила.png")
        image_widget = arcade.gui.UITextureButton(texture=texture, width=150, height=95)

        # заголовок
        title_label = arcade.gui.UILabel(text=title, font_size=60, font_name=("Cooper"),  text_color=arcade.color.BRINK_PINK, multiline=False)
    
        # основной текст
        input_text1 = arcade.gui.UILabel(text=input_text1, font_size=20, align="left", font_name=("Arial"), text_color=arcade.color.DEER, width=325, multiline=True)
        input_text2 = arcade.gui.UILabel(text=input_text2, font_size=20, align="left", font_name=("Arial"), text_color=arcade.color.DEER, width=325, multiline=True)

        widget_layout = arcade.gui.UIBoxLayout(space_between=15)
        widget_layout.add(title_label)
        widget_layout.add(input_text1)
        widget_layout.add(image_widget)
        widget_layout.add(input_text2)
        widget_layout.add(back_button)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        self.parent.remove(self)

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    main_view = MainView()
    main_view.setup()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    main()

