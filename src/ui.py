from tkinter import ON
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (loadPrcFileData, BitMask32, Vec3, CollisionTraverser,
    CollisionNode, LColor, CollisionHandlerQueue, CollisionRay, OrthographicLens,
    MouseWatcher, KeyboardButton)
from direct.gui import DirectGui, OnscreenText, DirectFrame, DirectWaitBar, DirectGuiGlobals
import time