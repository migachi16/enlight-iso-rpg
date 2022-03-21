from direct.showbase.ShowBase import ShowBase
from panda3d.core import (loadPrcFileData, BitMask32, Vec3, CollisionTraverser,
    CollisionNode, LColor, CollisionHandlerQueue, CollisionRay)

config_vars = '''
                win-size 1280 720
                show-frame-rate-meter 1
                window-title Enlight
              '''

#    Panda3d initializaton settings
loadPrcFileData('', config_vars)

#   Global variables
WHITE = (1, 1, 1, 1)
SELECTED = (0.3, 0.9, 0, 1)

###
# Main Map Class
###
class GameMap(ShowBase):

    def __init__(self):

        # Initialize background and set up the camera, 
        super().__init__()
        self.cam.setPos(0, -10, 0)
        self.cam.setR(45)   # Roll
        self.cam.setP(self.cam, 60)     # Pitch
        self.cam.setPos(self.cam, self.cam.getPos() + Vec3(0, 0, -4))
        self.set_background_color(0, 0, 0, 1)

        #   Load basic tile texture
        self.plane = self.loader.loadModel('../eggs/plane.egg')
        self.texture1 = self.loader.loadTexture('../tiles/grass02.png')
        self.plane.setTexture(self.texture1)

        #   Initialize the map grid
        self.map = self.render.attachNewNode('map-root')
        self.grid_gen(100, 100)

        #   Allow for mouse selection on the grid
        self.trav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.hit = False

        point = CollisionNode('point')
        point.setFromCollideMask(BitMask32.bit(1))

        point_nodepath = self.cam.attachNewNode(point)
        self.point_ray = CollisionRay()
        
        point.addSolid(self.point_ray)
        self.trav.addCollider(point_nodepath, self.queue)
        self.taskMgr.add(self.mouse_action, 'mouse-action')

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

    #   Handle mouse interactions
    def mouse_action(self, action):

        if self.hit is not False:
            self.map.getChild(self.hit).setColor(WHITE)
            self.hit = False

        #   If the mouse is in the window
        if self.mouseWatcherNode.hasMouse():
            coord = self.mouseWatcherNode.getMouse()
            self.point_ray.setFromLens(self.camNode, coord.getX(), coord.getY())
            self.trav.traverse(self.map)

            if self.queue.getNumEntries() > 0:
                self.queue.sortEntries()
                tile = self.queue.getEntry(0).getIntoNodePath().getNode(2)
                tile_number = int(tile.getName().split('-')[-1])
                self.map.getChild(tile_number).setColor(SELECTED)
                self.hit = tile_number


        return action.cont



map = GameMap()
map.run()



