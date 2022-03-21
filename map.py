from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, BitMask32

config_vars = '''
                win-size 1280 720
                show-frame-rate-meter 1
                window-title Enlight
              '''

#    Panda3d initializaton settings
loadPrcFileData('', config_vars)

###
# Main Map Class
###
class GameMap(ShowBase):

    def __init__(self):

        super().__init__()
        self.set_background_color(0, 0, 0, 5)

        #   Load basic tile texture
        self.plane = self.loader.loadModel('eggs/plane.egg')
        self.texture1 = self.loader.loadTexture('tiles/grass02.png')
        self.plane.setTexture(self.texture1)

        #   Initialize the map grid
        self.map = self.render.attachNewNode('map-root')
        self.grid_gen(100, 100)


    #   Build the map grid
    def grid_gen(self, xmax, zmax):
        i = 0
        for x in range(xmax):
            for z in range(zmax):
                #   Add a node to map and give it an id, then place it 
                tile = self.map.attachNewNode('tile-' + str(i))
                tile.setPos(x, 0, z)
                self.plane.instanceTo(tile)
                tile.find('**/pPlane1').node().setIntoCollideMask(BitMask32.bit(1))
                i += 1





map = GameMap()
map.run()



