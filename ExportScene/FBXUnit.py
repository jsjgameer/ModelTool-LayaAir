import os

from fbx import FbxLayerElement

global VERTEX_FACTOR
global OUT_PATH
global INSTANCEID


def ResetInstanID():
    global INSTANCEID
    INSTANCEID = 0


def GetInstanceID():
    global INSTANCEID
    INSTANCEID += 1
    return INSTANCEID - 1
    pass


def SetGlobalFactio(value):
    global VERTEX_FACTOR
    VERTEX_FACTOR = value


def GetGlobalFactio():
    global VERTEX_FACTOR
    return VERTEX_FACTOR


def checkFileName(fileName):
    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in fileName:
        if char in sets:
            fileName = fileName.replace(char, '_')
    return fileName
    pass


def SetOutPath(value):
    global OUT_PATH
    OUT_PATH = value
    pass


def makeDir(dir):
    filepath, tmpfilename = os.path.split(dir)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    pass


def GetOutPath(value):
    global OUT_PATH
    return OUT_PATH + "/" + value
    pass


def BoolToString(pHeader, pValue):
    if pValue:
        return "true"
    else:
        return "false"


def IntToString(pHeader, pValue):
    return str(pValue)


def DoubleToString(pHeader, pValue):
    return str(pValue);


def ColorToArray(pValue):
    return [pValue.mRed, pValue.mGreen, pValue.mBlue];


def ListContainCount(boneindex, subsubboneindexs):
    containcount = [];
    for i in range(len(boneindex)):
        if boneindex[i] not in subsubboneindexs:
            containcount.append(boneindex[i])
            pass
        pass
    return containcount


# 获取顶点
def GetVertex(p_ControlPoints, p_orginPolygonIndex):
    return p_ControlPoints[p_orginPolygonIndex]
    pass


# 获取数据
def GetDataByPolygonIndexOrVertexIndex(p_ElementDatas, p_orginPolygonIndex, p_VertexIndex):
    if (p_ElementDatas.GetMappingMode() == FbxLayerElement.eByControlPoint):  # 逐顶点
        if p_ElementDatas.GetReferenceMode() == FbxLayerElement.eDirect:
            return p_ElementDatas.GetDirectArray().GetAt(p_orginPolygonIndex)
        if p_ElementDatas.GetReferenceMode() == FbxLayerElement.eIndexToDirect:
            id = p_ElementDatas.GetIndexArray().GetAt(p_orginPolygonIndex)
            return p_ElementDatas.GetDirectArray().GetAt(id)
    if (p_ElementDatas.GetMappingMode() == FbxLayerElement.eByPolygonVertex):  # 逐面片
        if p_ElementDatas.GetReferenceMode() == FbxLayerElement.eDirect:
            return p_ElementDatas.GetDirectArray().GetAt(p_VertexIndex)
        if p_ElementDatas.GetReferenceMode() == FbxLayerElement.eIndexToDirect:
            id = p_ElementDatas.GetIndexArray().GetAt(p_VertexIndex)
            return p_ElementDatas.GetDirectArray().GetAt(id)
    pass  # end
