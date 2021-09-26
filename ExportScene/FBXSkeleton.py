from ExportScene import FBXUnit
from ExportScene.FBXNode import FBXNode


class FBXSkeleton(FBXNode):
    def __init__(self,pNode,partner,map):
        FBXNode.__init__(self,partner,map)
        self.instandeId(FBXUnit.GetInstanceID())
        self.setType("Sprite3D")
        self.analysisNodeContent(pNode)
        pass