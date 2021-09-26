from ExportScene import FBXUnit
from ExportScene.FBXNode import FBXNode

class FBXLight(FBXNode):

    def __init__(self, pNode):
        FBXNode.__init__(self)
        self.analysisNodeContent(pNode)
        self.instandeId(FBXUnit.GetInstanceID())
        lLight = pNode.GetNodeAttribute()
        lLightTypes = ["PointLight", "DirectionLight", "SpotLight"]
        self.setType(lLightTypes[lLight.LightType.Get()])
        c = lLight.Color.Get()
        self.addProp("color",[c[0], c[1], c[2]]);
        self.addProp("intensity",lLight.Intensity.Get());
