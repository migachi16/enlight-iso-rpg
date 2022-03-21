from direct.showbase.ShowBase import ShowBase
from panda3d.core import (loadPrcFileData, BitMask32, Vec3, CollisionTraverser,
    CollisionNode, LColor, CollisionHandlerQueue, CollisionRay, OrthographicLens)

config_vars = '''
                win-size 1600 900
                show-frame-rate-meter 1
                window-title Enlight
              '''

#    Panda3d initializaton settings
loadPrcFileData('', config_vars)

#   Global variables
WHITE = (1, 1, 1, 1)
SELECTED = (0.3, 0.9, 0, 1)

###
#   Main Map Class
###
class GameMap(ShowBase):

    def __init__(self):

        #   Initialize background and set up the camera, 
        super().__init__()
        self.cam.setPos(0, -10, 0)
        self.cam.setR(45)   # Roll
        self.cam.setP(self.cam, 60)     # Pitch
        self.cam.setPos(self.cam, self.cam.getPos() + Vec3(0, 0, -2))
        self.set_background_color(0, 0, 0, 1)

        #   Set up for orthographic projection
        camlens = OrthographicLens()
        camlens.setFilmSize(25, 15)
        camlens.setNearFar(-50, 50)
        self.cam.node().setLens(camlens)

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

        #   Initialize the character model
        self.player = self.loader.loadModel('models/box')
        self.player.setPos(0, -1, 0)
        self.player.reparentTo(self.render)

        #   Allow movement
        self.accept('w', self.move, ['up'])
        self.accept('a', self.move, ['left'])
        self.accept('s', self.move, ['down'])
        self.accept('d', self.move, ['right'])
        self.accept('w-repeat', self.move, ['up'])
        self.accept('a-repeat', self.move, ['left'])
        self.accept('s-repeat', self.move, ['down'])
        self.accept('d-repeat', self.move, ['right'])



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
    
    #   Move the player model around the map with WASD
    def move(self, direction):

        match direction:
            case 'up':
                self.player.setPos(self.player.getPos() + Vec3(0, 0, 1))
            case 'left': 
                self.player.setPos(self.player.getPos() + Vec3(-1, 0, 0))
            case 'down':
                self.player.setPos(self.player.getPos() + Vec3(0, 0, -1))
            case 'right':
                self.player.setPos(self.player.getPos() + Vec3(1, 0, 0))



map = GameMap()
map.run()



