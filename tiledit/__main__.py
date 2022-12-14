import pyray as rl
from colors import Colors
from colors import get_color_dict
from raylib import KEY_P, KEY_D, KEY_S, KEY_ENTER, KEY_ESCAPE,KEY_BACKSPACE, KEY_LEFT_CONTROL, KEY_NULL, KEY_SPACE, KEY_UP, KEY_RIGHT_CONTROL, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_LEFT_ALT, KEY_RIGHT_ALT

class ColoredRect():
    def __init__(self, name_str: str, posx: float, posy: float, width: float, height: float, color: rl.Color) -> None:
        self.rect = rl.Rectangle(posx,posy,width,height)
        self.clr = color
        self.name_as_str: str = name_str

    def draw(self):
        rl.draw_rectangle_rec(self.rect, self.clr)

class Selection():
    def __init__(self, pos: rl.Vector2, width:int, thickness:int) -> None:
        self.selection_clr = rl.Color(200,200,200,255)
        self.timer = 0
        self.pos = pos
        self.width = width
        self.thickness = thickness

        self.rect_above = rl.Rectangle(pos.x-thickness, pos.y-thickness,width+(thickness*2), thickness)
        self.rect_below = rl.Rectangle(pos.x-thickness, pos.y+width,width+(thickness*2), thickness)
        self.rect_left = rl.Rectangle(pos.x-thickness, pos.y-thickness, thickness, width+(thickness*2))
        self.rect_right = rl.Rectangle(pos.x+width, pos.y-thickness, thickness,width+(thickness*2))
    
    def draw(self):
        rl.draw_rectangle_rec(self.rect_above, self.selection_clr)
        rl.draw_rectangle_rec(self.rect_below, self.selection_clr)
        rl.draw_rectangle_rec(self.rect_left, self.selection_clr)
        rl.draw_rectangle_rec(self.rect_right, self.selection_clr)
    
    def update(self):
        self.rect_above.x, self.rect_above.y, self.rect_above.width, self.rect_above.height = self.pos.x-self.thickness, self.pos.y-self.thickness, self.width+(self.thickness*2), self.thickness
        self.rect_below.x, self.rect_below.y, self.rect_below.width, self.rect_below.height = self.pos.x-self.thickness, self.pos.y+self.width, self.width+(self.thickness*2), self.thickness
        self.rect_left.x, self.rect_left.y, self.rect_left.width, self.rect_left.height = self.pos.x-self.thickness, self.pos.y-self.thickness, self.thickness, self.width+(self.thickness*2)
        self.rect_right.x, self.rect_right.y, self.rect_right.width, self.rect_right.height = self.pos.x+self.width, self.pos.y-self.thickness, self.thickness, self.width+(self.thickness*2)
        

        self.timer += 1

def draw_checkerboard(base_color: rl.Color, alt_color: rl.Color, begin: int, length: int, tilesize: int):
        is_alt_color: bool = True
        for y in range(begin, begin+(length*tilesize*2), tilesize):
            for x in range(begin, begin+(length*tilesize*2), tilesize):
                if is_alt_color:
                    rl.draw_rectangle(x,y,tilesize,tilesize, alt_color)
                    is_alt_color = not is_alt_color
                else:
                    rl.draw_rectangle(x,y,tilesize,tilesize, base_color)
                    is_alt_color = not is_alt_color
            is_alt_color = not is_alt_color

class File():
    def __init__(self, name: str, filename: str = "Untitled", filepath = "./") -> None:
        self.grid = [[Colors.nothing for _ in range(50)] for _ in range(50)] # initialize grid
        self.name: str = name
        self.filename: str = f"{filename}.pxt"
        self.path_to_file: str = filepath

    def get_grid(self) -> list[list[rl.Color]]:
        return self.grid
    
    def set_grid(self, new_grid: list[list[rl.Color]]):
        self.grid = new_grid
    
    def _get_key_from_val(self, val, dic: dict):
        for k, v in dic.items():
            if v == val:
                return k

    def _encode(self):
        pass
        
    def save(self):
        pass

class Main():
    def __init__(self) -> None:
        self.grid = [[Colors.nothing for _ in range(50)] for _ in range(50)]        
        self.clr_dict = get_color_dict()
        self.modes = ["color picker", "edit", "menu", "selection fill", "erase"]
        self.mode = "color picker"

        rl.init_window(1200,800,"TileEdit")
        rl.set_target_fps(60)
        rl.set_exit_key(KEY_NULL)

        self.paintbrush_color: rl.Color = Colors.black
        self.paint_selection = Selection(rl.Vector2(108,108), 8,1)
        self.paint_selection_index = rl.Vector2(0,0)
        self.window_banner = "[NEW FILE]"
        self.window_title = f"TileEdit -- {self.window_banner}"
        self.selection = Selection(rl.Vector2(660,150),40,5)

        self.hold_delay: int = 0
        self.selection_fill_has_started: bool = False

        self.selection_fill_index = [rl.Vector2(0,0), rl.Vector2(0,0)]

        rl.set_window_title(self.window_title)
        print(len(self.clr_dict))

        self.draw_color_ypos = 0
        self.draw_color_xpos = 660

        self.selection_index = rl.Vector2(0,0)
        self.color_grid = [
            [ColoredRect(key,660+(count*40),150,40,40,value) 
                for count, (key, value) in enumerate(self.clr_dict.items())
                    if count in range(0,11)],
            [ColoredRect(key,180+(count*40),190,40,40,value) 
                for count, (key, value) in enumerate(self.clr_dict.items())
                    if count in range(12,23)],
            [ColoredRect(key,-300+(count*40),230,40,40,value) 
                for count, (key, value) in enumerate(self.clr_dict.items())
                    if count in range(24,35)],
            [ColoredRect(key,-780+(count*40),270,40,40,value) 
                for count, (key, value) in enumerate(self.clr_dict.items())
                    if count in range(36,48) and value != Colors.nothing],
        ]

        while not rl.window_should_close():
            self.update()
            rl.begin_drawing()
            rl.clear_background(Colors.raywhite)
            self.draw()
            rl.end_drawing()
        rl.close_window()

    def draw(self) -> None:
        rl.draw_text(self.window_title, 10, 10, 30, Colors.black)
        rl.draw_rectangle(158,158,415,415,Colors.gray) # border
        draw_checkerboard(rl.Color(235,235,235,255), Colors.raywhite, 166,50,4)
        rl.draw_rectangle(10,650,1180,140,rl.Color(235,235,235,255)) # toolbox btm
        rl.draw_rectangle(650,100,500,525,rl.Color(235,235,235,255)) # toolbox right
        
        rl.draw_text("Colors", 660,110,30,Colors.black)
        rl.draw_text("Info", 20,660,30,Colors.black)
        rl.draw_text(f"Current Mode: {self.mode}", 20, 690, 20, Colors.black)
        rl.draw_text(f"Selected Color: {self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].name_as_str}", 20, 710, 20, Colors.black)

        # color grid
        for column in self.color_grid:
            for clr_rect in column:
                clr_rect.draw()
        # selection
        if self.mode == self.modes[0]:
            self.selection.draw()
        
        for y, column in enumerate(self.grid):
            for x, clr in enumerate(column):
                rl.draw_rectangle(166+(x*8),166+(y*8),8,8,clr)

        if self.mode == self.modes[1]:
            self.paint_selection.draw()

    def update(self) -> None:      
        if self.mode == self.modes[1]:
            self.paint_selection.update()
            
            # clear
            if (rl.is_key_down(KEY_RIGHT_CONTROL) or rl.is_key_down(KEY_LEFT_CONTROL)) and rl.is_key_pressed(KEY_BACKSPACE):
                for y in range(len(self.grid)):
                    for x in range(len(self.grid)):
                        self.grid[y][x] = Colors.nothing

            # erase
            if rl.is_key_down(KEY_BACKSPACE):
                self.grid[int(self.paint_selection_index.y)][int(self.paint_selection_index.x)] = Colors.nothing

            # exit edit mode
            if rl.is_key_pressed(KEY_ESCAPE):
                self.mode = "color picker"

            # fill screen
            if (rl.is_key_down(KEY_LEFT_CONTROL) or rl.is_key_down(KEY_RIGHT_CONTROL)) and rl.is_key_pressed(KEY_SPACE):
                for y in range(len(self.grid)):
                    for x in range(len(self.grid)):
                        self.grid[y][x] = self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].clr
            
            # fill pixel
            if rl.is_key_down(KEY_SPACE):
                self.grid[int(self.paint_selection_index.y)][int(self.paint_selection_index.x)] = self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].clr

            # pixel selection movement
            if rl.is_key_down(KEY_UP):
                self.hold_delay += 1
                if self.hold_delay > 16:
                    if self.paint_selection_index.y - 1 >= 0:
                        self.paint_selection_index.y -= 1
            if rl.is_key_down(KEY_DOWN):
                self.hold_delay += 1
                if self.hold_delay > 16:
                    if self.paint_selection_index.y + 1 < 50:
                        self.paint_selection_index.y += 1

            if rl.is_key_down(KEY_LEFT):
                self.hold_delay += 1
                if self.hold_delay > 16:
                    if self.paint_selection_index.x - 1 >=0:
                        self.paint_selection_index.x -= 1

            if rl.is_key_down(KEY_RIGHT):
                self.hold_delay += 1
                if self.hold_delay > 16:
                    if self.paint_selection_index.x + 1 < 50:
                        self.paint_selection_index.x += 1

            if rl.is_key_pressed(KEY_UP):
                if self.paint_selection_index.y - 1 >= 0: self.paint_selection_index.y -= 1
            if rl.is_key_pressed(KEY_DOWN):
                if self.paint_selection_index.y + 1 < 50: self.paint_selection_index.y += 1
            if rl.is_key_pressed(KEY_LEFT):
                if self.paint_selection_index.x - 1 >= 0: self.paint_selection_index.x -= 1
            if rl.is_key_pressed(KEY_RIGHT):
                if self.paint_selection_index.x + 1 < 50: self.paint_selection_index.x += 1

            if rl.is_key_released(KEY_LEFT) or rl.is_key_released(KEY_RIGHT) or rl.is_key_released(KEY_UP) or rl.is_key_released(KEY_DOWN):
                self.hold_delay = 0
        
            self.paint_selection.pos.x = 166+(8*self.paint_selection_index.x)
            self.paint_selection.pos.y = 166+(8*self.paint_selection_index.y)

            if rl.is_key_pressed(KEY_ESCAPE):
                self.mode = "color picker"

        if rl.is_key_pressed(KEY_S):
            self.mode="selection fill"

        if rl.is_key_pressed(KEY_D):
            self.mode = "edit"
        
        if rl.is_key_pressed(KEY_P):
            self.mode = "color picker"
        
        if self.mode == self.modes[0]:
            self.selection.update()
            self.selection.pos.x, self.selection.pos.y = self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].rect.x, self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].rect.y

            if rl.is_key_pressed(KEY_UP):
                if self.selection_index.y - 1 >= 0:
                    self.selection_index.y -= 1
            if rl.is_key_pressed(KEY_DOWN):
                if self.selection_index.y + 1 < 4:
                    self.selection_index.y += 1

            if rl.is_key_pressed(KEY_LEFT):
                if self.selection_index.x - 1 >=0:
                    self.selection_index.x -= 1
            if rl.is_key_pressed(KEY_RIGHT):
                if self.selection_index.x + 1 < 11:
                    self.selection_index.x += 1

            if rl.is_key_pressed(KEY_SPACE) or rl.is_key_pressed(KEY_ENTER):
                self.paintbrush_color = self.color_grid[int(self.selection_index.y)][int(self.selection_index.x)].clr
                self.mode = "edit"

if __name__ == "__main__":
    Main()
