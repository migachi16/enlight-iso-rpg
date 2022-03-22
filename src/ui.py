from tkinter import ON
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (loadPrcFileData, BitMask32, Vec3, CollisionTraverser,
    CollisionNode, LColor, CollisionHandlerQueue, CollisionRay, OrthographicLens,
    MouseWatcher, KeyboardButton)
from direct.gui import DirectGui, OnscreenText, DirectFrame, DirectWaitBar, DirectGuiGlobals
import time

class Bar(NodePath): 

    '''Resource bar class '''
    
    def __init__(self, scale=1, value=1, r=1, g=0, b=0): 
            NodePath.__init__(self, 'healthbar') 
            self.scale = scale
            cmfg = CardMaker('fg') 
            cmfg.setFrame(- scale,  scale, -0.1 * scale, 0.1 * scale) 
            self.fg = self.attachNewNode(cmfg.generate()) 
            cmbg = CardMaker('bg') 
            cmbg.setFrame(- scale, scale, -0.1 * scale, 0.1 * scale) 
            self.bg = self.attachNewNode(cmbg.generate()) 
            self.fg.setColor(r, g, b, 1) 
            self.bg.setColor(0.2, 0.2, 0.2, 1) 
            self.setValue(value) 

    def setValue(self, value):
            value = min(max(0, value), 1)
            self.fg.setScale(value * self.scale, 0, self.scale) 
            self.bg.setScale(self.scale * (1.0 - value), 0, self.scale)
            self.fg.setX((value - 1) * self.scale * self.scale)
            self.bg.setX(value * self.scale * self.scale)