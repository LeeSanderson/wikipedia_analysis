class ColourPalette(object):
    def __init__(self, *args):
        self.colours = args
        
    def get_colours(self):
        return list(self.colours)

class MaterialLightBlue(ColourPalette):
    def __init__(self):
        super(MaterialLightBlue, self).__init__(
            '#03A9F4', '#0288D1', '#0077C0', '#0065BF', '#0059A8', '#004F95'
        )

class MaterialTeal(ColourPalette):
    def __init__(self):
        super(MaterialTeal, self).__init__(
            '#009688', '#00897B', '#00796B', '#00695C', '#005A51', '#004C45'
        )

class MaterialBrown(ColourPalette):
    def __init__(self):
        super(MaterialBrown, self).__init__(
            '#795548', '#6D4C41', '#5D4037', '#4E342E', '#3E2723', '#2E160F'
        )

class MaterialBlueGrey(ColourPalette):
    def __init__(self):
        super(MaterialBlueGrey, self).__init__(
            '#455A64', '#37474F', '#2E4053', '#23373F', '#1B2D50', '#0F3651'
        )

class MaterialGrey(ColourPalette):
    def __init__(self):
        super(MaterialGrey, self).__init__(
            '#9E9E9E', '#757575', '#616161', '#424242', '#212121', '#000000'
        )

class DefaultColourPalette(ColourPalette):
    def __init__(self):
        super(DefaultColourPalette, self).__init__(
            '#03A9F4', '#0288D1', '#0077C0', '#0065BF', '#0059A8', '#004F95'
        )   

def get_all_colour_palettes():
    return [
        MaterialLightBlue(),
        MaterialTeal(),
        MaterialBrown(),
        MaterialBlueGrey(),
        MaterialGrey(),
        DefaultColourPalette()
    ]
    