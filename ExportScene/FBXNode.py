import json
import fbx

from ImportScene.DisplayCamera import DisplayCamera
from ExportScene import FBXUnit
from ImportScene.DisplayCommon import DisplayString


class FBXNode:
    def __init__(self, partner, map):
        self.__info = {"type": "", "props": {}, "child": []}
        self._children = []
        self._partner = partner
        self._map = map
        pass

    def getPatner(self):
        return self._partner

    def instandeId(self, value):
        self.__info['instanceID'] = value

    def getInstandeId(self):
        return self.__info['instanceID']

    def absolutepath(self, path):
        return FBXUnit.GetOutPath(path)
        pass

    def geometricTransform(self, pNode):
        lTmpVector = pNode.LclTranslation.Get()
        self.addProp("position", [
            lTmpVector[0] * FBXUnit.GetGlobalFactio(),
            lTmpVector[1] * FBXUnit.GetGlobalFactio(),
            lTmpVector[2] * FBXUnit.GetGlobalFactio()
        ])
        lTmpVector = pNode.LclRotation.Get()
        self.addProp("rotationEuler",
                     [lTmpVector[0], lTmpVector[1], lTmpVector[2]])
        lTmpVector = pNode.LclScaling.Get()
        self.addProp("scale", [lTmpVector[0], lTmpVector[1], lTmpVector[2]])
        pass

    def analysisNodeContent(self, pNode):
        self.nodeName = pNode.GetName()
        self.geometricTransform(pNode)
        self.addProp("name", self.nodeName)

        for i in range(pNode.GetChildCount()):
            pchildNode = pNode.GetChild(i)
            if pchildNode.GetNodeAttribute() == None:
                continue
            else:
                lAttributeType = (
                    pchildNode.GetNodeAttribute().GetAttributeType())
                # if lAttributeType == fbx.FbxNodeAttribute.eMarker:
                #    DisplayMarker(pchildNode)
                if lAttributeType == fbx.FbxNodeAttribute.eSkeleton:
                    from ExportScene.FBXSkeleton import FBXSkeleton
                    cnode = FBXSkeleton(pchildNode, self, self._map)
                    self._map[cnode.nodeName] = cnode
                    self.addChildren(cnode)
                elif lAttributeType == fbx.FbxNodeAttribute.eMesh:
                    from ExportScene.FBXMesh import FBXMesh
                    cnode = FBXMesh(pchildNode, self, self._map)
                    self._map[cnode.nodeName] = cnode
                    self.addChildren(cnode)
                # elif lAttributeType == fbx.FbxNodeAttribute.eNurbs:
                #     DisplayNurb(pchildNode)
                # elif lAttributeType == fbx.FbxNodeAttribute.ePatch:
                #     DisplayPatch(pchildNode)
                elif lAttributeType == fbx.FbxNodeAttribute.eCamera:
                    DisplayCamera(pchildNode)
                elif lAttributeType == fbx.FbxNodeAttribute.eLight:
                    from ExportScene.FBXLight import FBXLight
                    self.addChildren(FBXLight(pchildNode))

    def addChildren(self, node):
        self._children.append(node)

    def setType(self, type):
        self.__info['type'] = type

    def setName(self, name):
        self.__info['name'] = name

    def addProp(self, propName, propValue):
        self.__info["props"][propName] = propValue

    def toExportObject(self):
        self.__info['child'] = []
        for i in range(len(self._children)):
            child = self._children[i]
            self.__info['child'].append(child.toExportObject())
            pass
        return self.__info

    def toJson(self):
        return json.dumps(self.toExportObject())
