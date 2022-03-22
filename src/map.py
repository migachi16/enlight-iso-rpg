from tkinter import ON
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (loadPrcFileData, BitMask32, Vec3, CollisionTraverser,
    CollisionNode, LColor, CollisionHandlerQueue, CollisionRay, OrthographicLens,
    MouseWatcher, KeyboardButton)
from direct.gui import DirectGui, OnscreenText, DirectFrame, DirectWaitBar, DirectGuiGlobals
import time
import player

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

mainchar = player.Player()

class GameMap(ShowBase):

    '''Main Map class'''

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
        self.model = self.loader.loadModel('models/box')
        self.model.setPos(0, -1, 0)
        self.model.reparentTo(self.render)
        
        #   Accept inputs
        self.accept('w', self.move, ['up'])
        self.accept('a', self.move, ['left'])
        self.accept('s', self.move, ['down'])
        self.accept('d', self.move, ['right'])
        self.accept('w-repeat', self.move, ['up'])
        self.accept('a-repeat', self.move, ['left'])
        self.accept('s-repeat', self.move, ['down'])
        self.accept('d-repeat', self.move, ['right'])

        #   Define inputs
        self.up = KeyboardButton.ascii_key('w')
        self.down = KeyboardButton.ascii_key('s')
        self.left = KeyboardButton.ascii_key('a')
        self.right = KeyboardButton.ascii_key('d')

        #   Font setup, UI, and menus
        mrb = self.loader.loadFont('../eggs/MorrisRoman-Black.ttf')

        hptext = OnscreenText.TextNode('hp')
        hptext.setText('HEALTH')
        hptext.setFont(mrb)
        hppath = self.aspect2d.attachNewNode(hptext)
        hppath.setScale(0.05)
        hppath.setPos(-1.75, 0, 0.95)

        stamtext = OnscreenText.TextNode('stam')
        stamtext.setText('STAMINA')
        stamtext.setFont(mrb)
        stampath = self.aspect2d.attachNewNode(stamtext)
        stampath.setScale(0.05)
        stampath.setPos(-1.75, 0, 0.89)

        srctext = OnscreenText.TextNode('src')
        srctext.setText('SOURCE')
        srctext.setFont(mrb)
        srcpath = self.aspect2d.attachNewNode(srctext)
        srcpath.setScale(0.05)
        srcpath.setPos(-1.75, 0, 0.83)

        #   Resource bars
        
        self.hpbar = DirectGui.DirectWaitBar(text = '', value = mainchar.hp, range = mainchar.hpmax, pos = (-1.15, 0, 0.967),
            barRelief = DirectGuiGlobals.GROOVE, relief = DirectGuiGlobals.GROOVE, barColor = (1, 0.1, 0.1, 1),
            barBorderWidth = (0.05, 0.03), scale = 0.3, frameColor = (0.05, 0.05, 0.05, 0.7))
        
        self.stambar = DirectGui.DirectWaitBar(text = '', value = mainchar.stam, range = mainchar.stammax, pos = (-1.15, 0, 0.907),
            barRelief = DirectGuiGlobals.GROOVE, relief = DirectGuiGlobals.GROOVE, barColor = (0.2, 1, 0.2, 1),
            barBorderWidth = (0.05, 0.03), scale = 0.3, frameColor = (0.05, 0.05, 0.05, 0.7))

        self.srcbar = DirectGui.DirectWaitBar(text = '', value = mainchar.src, range = mainchar.srcmax, pos = (-1.15, 0, 0.847),
            barRelief = DirectGuiGlobals.GROOVE, relief = DirectGuiGlobals.GROOVE, barColor = (0.15, 0.1, 1, 1),
            barBorderWidth = (0.05, 0.03), scale = 0.3, frameColor = (0.05, 0.05, 0.05, 0.7))



        #   UI buttons
        self.settings = DirectGui.DirectButton(pos = (1.72, 0, 0.94), scale = 0.5)
        self.inventory = DirectGui.DirectButton(pos = (1.61, 0, 0.94), scale = 0.5)


        #   Visualization purposes, not in build
        #self.wireframe_on()


    def grid_gen(self, xmax, zmax):

        '''Build the map grid '''    

        i = 0
        for x in range(xmax):
            for z in range(zmax):
                #   Add a node to map and give it an id, then place it 
                tile = self.map.attachNewNode('tile-' + str(i))
                tile.setPos(x, 0, z)
                self.plane.instanceTo(tile)
                tile.find('**/pPlane1').node().setIntoCollideMask(BitMask32.bit(1))
                i += 1


    def mouse_action(self, action):

        '''Handle mouse interactions '''

        #   Cursor touching a tile?
        if self.hit is not False:
            self.map.getChild(self.hit).setColor(WHITE)
            self.hit = False

        #   If the cursor is in the window
        if self.mouseWatcherNode.hasMouse():
            coord = self.mouseWatcherNode.getMouse()
            self.point_ray.setFromLens(self.camNode, coord.getX(), coord.getY())
            self.trav.traverse(self.map)

            if self.queue.getNumEntries() > 0:
                self.queue.sortEntries()
                tile = self.queue.getEntry(0).getIntoNodePath().getNode(2)
                tile_number = int(tile.getName().split('-')[-1])
                self.map.getChild(tile_number).setColor(SELECTED)
                self.hit = tile_number      #   Which tile are we touching?

        return action.cont
    

    def move(self, task):

        '''Move the player model around the map with WASD'''

        initial = self.model.getPos()

        if self.mouseWatcherNode.is_button_down(self.up):
            self.model.setPos(self.model.getPos() + Vec3(1, 0, 1))
 
        if self.mouseWatcherNode.is_button_down(self.left):
            self.model.setPos(self.model.getPos() + Vec3(-1, 0, 1))

        if self.mouseWatcherNode.is_button_down(self.down):
            self.model.setPos(self.model.getPos() + Vec3(-1, 0, -1))

        if self.mouseWatcherNode.is_button_down(self.right):    
            self.model.setPos(self.model.getPos() + Vec3(1, 0, -1))
        
        final = self.model.getPos()

        if initial != final:
            mainchar.stam -= 1
            self.stambar.update(mainchar.stam)
            



map = GameMap()
map.run()



