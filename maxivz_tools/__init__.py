bl_info = {
    "name" : "MaxivzsTools",
    "author" : "Maxi Vazquez",
    "description" : "Collection of context sensitive and time saving tools",
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . pannels import MaxivzTools_PT_Panel
from . mvztools import SuperSmartCreate
from . mvztools import CSBevel
from . mvztools import SmartDelete
from . mvztools import SmartSelectLoop
from . mvztools import SetCylindricalObjSides
from . mvztools import QuickSelectionVert
from . mvztools import QuickSelectionEdge
from . mvztools import QuickSelectionFace
from . mvztools import ContextSensitiveSlide
from . mvztools import SmartSelectRing
from . mvztools import QuickPivot
from . mvztools import SimpleEditPivot
from . mvztools import QuickModifierToggle
from . mvztools import QuickWireToggle
from . mvztools import WireShadedToggle
from . mvztools import TargetWeldToggle
from . mvztools import SmartExtrude
from . mvztools import QuickRadialSymmetry
from . mvztools import QuickRotateUv90Pos
from . mvztools import QuickRotateUv90Neg
from . mvztools import QuickFFD
from . mvztools import SmartTranslate


classes = (MaxivzTools_PT_Panel, SuperSmartCreate, CSBevel, SmartDelete, SmartSelectLoop, SetCylindricalObjSides, QuickSelectionVert, QuickSelectionEdge, QuickSelectionFace, SmartSelectRing, ContextSensitiveSlide, QuickPivot ,QuickModifierToggle, QuickWireToggle, WireShadedToggle, TargetWeldToggle, SmartExtrude, QuickRadialSymmetry, QuickRotateUv90Pos, QuickRotateUv90Neg, QuickFFD, SimpleEditPivot, SmartTranslate)

register,unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()