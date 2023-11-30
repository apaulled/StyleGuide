class ColorBucket:

    def __init__(self):
        self.red = 0
        self.orange = 0
        self.yellow = 0
        self.green = 0
        self.aqua = 0
        self.blue = 0
        self.purple = 0
        self.pink = 0
        self.brown = 0
        self.black = 0
        self.white = 0
        self.gray = 0

    def __str__(self):
        yuh = ""
        for key, value in self.__dict__.items():
            yuh += key + " " + str(value) + "\n"
        return yuh

    def get_key_colors(self):
        colors = self.__dict__
        primary = max(colors, key=lambda key: colors[key])
        colors[primary] = 0
        secondary = max(colors, key=lambda key: colors[key])
        return primary.upper(), secondary.upper()

    def get_primary(self):
        colors = self.__dict__
        return max(colors, key=lambda key: colors[key]).upper()

    def get_least(self):
        colors = self.__dict__
        colors['gray'] = 1026
        return min(colors, key=lambda key: colors[key]).upper()

    def add_pixel(self, color):
        match color:
            case 'RED':
                self.red += 1
            case 'ORANGE':
                self.orange += 1
            case 'YELLOW':
                self.yellow += 1
            case 'GREEN':
                self.green += 1
            case 'AQUA':
                self.aqua += 1
            case 'BLUE':
                self.blue += 1
            case 'PURPLE':
                self.purple += 1
            case 'PINK':
                self.pink += 1
            case 'BROWN':
                self.brown += 1
            case 'BLACK':
                self.black += 1
            case 'WHITE':
                self.white += 1
            case 'GRAY':
                self.gray += 1
