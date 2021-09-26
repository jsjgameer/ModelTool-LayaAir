from fbx import FbxDeformer, FbxAMatrix

from ExportScene.FBXNode import FBXNode
import ExportScene.FBXUnit as FBXUnit
import ExportScene.FBXConfig as FBXConfig
from ExportScene.ByteUnit import ByteUnit, float_2_byte, uint8_2_byte
from operator import itemgetter
from ImportScene.DisplayCommon import DisplayString, DisplayInt, Display4DVector


class Triangle:
    Count = 0;
    point1 = None
    point2 = None
    point3 = None

    def __init__(self):
        self.count = Triangle.Count
        Triangle.Count = Triangle.Count+1
        pass

    def triangleBoneIndex(self):
        list = []
        if self.point1.boneIndex[0] not in list:
            list.append(self.point1.boneIndex[0])
            pass
        if self.point1.boneIndex[1] not in list:
            list.append(self.point1.boneIndex[1])
            pass
        if self.point1.boneIndex[2] not in list:
            list.append(self.point1.boneIndex[2])
            pass
        if self.point1.boneIndex[3] not in list:
            list.append(self.point1.boneIndex[3])
            pass

        if self.point2.boneIndex[0] not in list:
            list.append(self.point2.boneIndex[0])
            pass
        if self.point2.boneIndex[1] not in list:
            list.append(self.point2.boneIndex[1])
            pass
        if self.point2.boneIndex[2] not in list:
            list.append(self.point2.boneIndex[2])
            pass
        if self.point2.boneIndex[3] not in list:
            list.append(self.point2.boneIndex[3])
            pass

        if self.point3.boneIndex[0] not in list:
            list.append(self.point3.boneIndex[0])
            pass
        if self.point3.boneIndex[1] not in list:
            list.append(self.point3.boneIndex[1])
            pass
        if self.point3.boneIndex[2] not in list:
            list.append(self.point3.boneIndex[2])
            pass
        if self.point3.boneIndex[3] not in list:
            list.append(self.point3.boneIndex[3])
            pass
        return list
        pass



def readVertice(self, data, index):
    self.vertice = [data[index], data[index+1], data[index+2]]
    return index+3


def readNormal(self, data, index):
    self.normal = [data[index], data[index + 1], data[index + 2]]
    return index+3

def readColor(self, data, index):
    self.color = [data[index], data[index + 1], data[index + 2], data[index + 3]]
    return index + 4


def readUV(self, data, index):
    self.uv = [data[index], data[index + 1]]
    return index + 2


def readUV2(self, data, index):
    self.uv2 = [data[index], data[index + 1]]
    return index + 2


def readBoneWeigth(self, data, index):
    self.boneWeight = [data[index], data[index + 1], data[index + 2], data[index + 3]]
    return index + 4


def readBoneIndex(self, data, index):
    self.boneIndex = [data[index], data[index + 1], data[index + 2], data[index + 3]]
    return index + 4

def readTangent(self, data, index):
    self.tangent = [data[index], data[index + 1], data[index + 2], data[index + 3]]
    return index + 4

def hashMap(data):
    return hash(str(data))

readList = [readVertice, readNormal,readColor,readUV,readUV2,readBoneWeigth,readBoneIndex,readTangent]

class VertexData:
    index = 0
    subMeshindex = -1
    subsubMeshindex = -1
    ischange = True
    commonPoint = None
    vertice = None
    normal = None
    color = None
    uv = None
    uv2 = None
    boneWeight = None
    boneIndex = None
    tangent = None

    def __init__(self, index, runList, dataarr):
        self.fmt = ""
        self.index = index
        self.runList = runList
        self.dataarr = dataarr
        coundIndex = 0
        for i in range(len(runList)):
            coundIndex = readList[runList[i]](self, dataarr, coundIndex)
        pass
    def getHash(self):
        data = []
        if self.vertice is not None:
            data.extend(self.vertice)
            pass
        if self.normal is not None:
            data.extend(self.normal)
            pass
        if self.color is not None:
            data.extend(self.color)
            pass
        if self.uv is not None:
            data.extend(self.uv)
            pass
        if self.uv2 is not None:
            data.extend(self.uv2)
            pass
        if self.boneWeight is not None:
            data.extend(self.boneWeight)
            data.extend(self.boneIndex)
            pass
        if self.tangent is not None:
            data.extend(self.tangent)
            pass
        return hash(str(data))
        pass

    def setVertice(self, vertice, scale):
        if self.vertice is None:
            self.vertice = [vertice[0] * scale, vertice[2] * scale, vertice[1] * scale]
        else:
            self.vertice[0] = vertice[0] * scale
            self.vertice[1] = vertice[2] * scale
            self.vertice[2] = vertice[1] * scale
        pass

    def setNormal(self, normal):
        self.normal = [normal[0], normal[2], normal[1]]
        pass

    def setColor(self, color):
        self.color = [color.mRed, color.mGreen, color.mBlue, color.mAlpha]
        pass

    def setUV(self, uv):
        self.uv = [uv[0], uv[1]]
        pass

    def setUV2(self, uv):
        self.uv2 = [uv[0], uv[1]]
        pass

    def setBoneWeigth(self, weigth):
        self.boneWeight = [weigth[0], weigth[1], weigth[2], weigth[3]]
        pass

    def setBoneIndex(self, indexs):
        self.boneIndex = [indexs[0], indexs[1], indexs[2], indexs[3]]
        pass

    def setTangent(self, tangent):
        self.tangent = [tangent[0], tangent[1], tangent[2], tangent[3]]
        pass

    def getByte(self):
        data = bytes()
        if self.vertice is not None:
            data += float_2_byte(self.vertice[0]) + float_2_byte(self.vertice[1]) + float_2_byte(self.vertice[2])
            pass
        if self.normal is not None:
            data += float_2_byte(self.normal[0]) + float_2_byte(self.normal[1]) + float_2_byte(self.normal[2])
            pass
        if self.color is not None:
            data += float_2_byte(self.color[0]) + float_2_byte(self.color[1]) + float_2_byte(
                self.color[2]) + float_2_byte(self.color[3])
            pass
        if self.uv is not None:
            data += float_2_byte(self.uv[0]) + float_2_byte(self.uv[1])
            pass
        if self.uv2 is not None:
            data += float_2_byte(self.uv2[0]) + float_2_byte(self.uv2[1])
            pass
        if self.boneWeight is not None:
            data += float_2_byte(self.boneWeight[0]) + float_2_byte(self.boneWeight[1]) + float_2_byte(
                self.boneWeight[2]) + float_2_byte(self.boneWeight[3])
            data += uint8_2_byte(self.boneIndex[0]) + uint8_2_byte(self.boneIndex[1]) + uint8_2_byte(
                self.boneIndex[2]) + uint8_2_byte(self.boneIndex[3])
            pass
        if self.tangent is not None:
            data += float_2_byte(self.tangent[0]) + float_2_byte(self.tangent[1]) + float_2_byte(
                self.tangent[2]) + float_2_byte(self.tangent[3])
            pass
        return data
        pass

    def clone(self, index):
        vertexData = VertexData(index)
        if self.vertice is not None:
            vertexData.vertice = [self.vertice[0], self.vertice[1], self.vertice[2]]
            pass
        if self.normal is not None:
            vertexData.normal = [self.normal[0], self.normal[1], self.normal[2]]
            pass
        if self.color is not None:
            vertexData.color = [self.color[0], self.color[1], self.color[2], self.color[3]]
            pass
        if self.uv is not None:
            vertexData.uv = [self.uv[0], self.uv[1]]
            pass
        if self.uv2 is not None:
            vertexData.uv2 = [self.uv2[0], self.uv2[1]]
            pass
        if self.boneWeight is not None:
            vertexData.boneWeight = [self.boneWeight[0], self.boneWeight[1], self.boneWeight[2], self.boneWeight[3]]
            vertexData.boneIndex = [self.boneIndex[0], self.boneIndex[1], self.boneIndex[2], self.boneIndex[3]]
            pass
        if self.tangent is not None:
            vertexData.tangent = [self.tangent[0], self.tangent[1], self.tangent[2], self.tangent[3]]
            pass
        return vertexData
        pass


class FBXMesh(FBXNode):
    _vertices = []
    _indices = []
    _dis = []

    def __init__(self, pNode, partner, map):
        FBXNode.__init__(self, partner, map)
        self.analysisNodeContent(pNode)
        self.instandeId(FBXUnit.GetInstanceID())
        self._pMesh = pNode.GetNodeAttribute()
        self._isSkinnerMesh = False
        self._vertices = []
        self.vbDeclaration = ""
        self.everyVBSize = 0
        self._indices = []
        self._subInfo = []
        self._hashMap = {}
        pass

    def analysisMeshConten(self):
        DisplayString("    解析模型", self.nodeName)
        if (self._pMesh.GetControlPointsCount() < 0):  # 没有顶点
            print("没有顶点数据")
            return
            pass
        self.analysisBone()

        nodeName = FBXUnit.checkFileName(self.nodeName)
        meshPath = "Asset/" + nodeName + ".lm"
        self.addProp("meshPath", meshPath)
        alsolePath = self.absolutepath(meshPath)
        FBXUnit.makeDir(alsolePath)
        outfile = ByteUnit(alsolePath)
        if self._isSkinnerMesh:
            self.setType("SkinnedMeshSprite3D")
            self.saveFileSkinnerMesh(outfile, nodeName)
        else:
            self.setType("MeshSprite3D")
            self.saveFileMesh(outfile, nodeName)
            pass
        pass

    def analysisBone(self):
        pGeometry = self._pMesh
        lSkinCount = pGeometry.GetDeformerCount(FbxDeformer.eSkin)
        DisplayInt("蒙皮数量：", lSkinCount)
        for i in range(lSkinCount):
            lClusterCount = pGeometry.GetDeformer(i, FbxDeformer.eSkin).GetClusterCount()
            self.weightTable = {}
            self.bonesName = []
            self.bindPos = []
            for j in range(lClusterCount):
                self._isSkinnerMesh = True
                lCluster = pGeometry.GetDeformer(i, FbxDeformer.eSkin).GetCluster(j)
                self.bonesName.append(lCluster.GetLink().GetName())

                lIndexCount = lCluster.GetControlPointIndicesCount()
                lIndices = lCluster.GetControlPointIndices()
                lWeights = lCluster.GetControlPointWeights()

                for k in range(lIndexCount):
                    controlId = lIndices[k]
                    if controlId not in self.weightTable:
                        self.weightTable[controlId] = []
                        pass
                    list = self.weightTable.get(controlId)
                    list.append({"weight": lWeights[k], "index": j})
        pass

    def saveFileSkinnerMesh(self, outfile, meshName):
        self.analysisMeshData()
        needRun = True
        rootNode = self._map[self.bonesName[0]]
        while needRun:
            if rootNode._partner.nodeName in self._map:
                rootNode = rootNode.getPatner()
            else:
                needRun = False
        self.addProp("rootBone", rootNode.getInstandeId())
        bones = []
        for i in range(len(self.bonesName)):
            boneNode = self._map[self.bonesName[i]]
            bones.append(boneNode.getInstandeId())
            pass
        self.addProp("bones", bones)
        min = [self.minx,self.miny,self.minz]
        max = [self.maxx,self.maxy,self.maxz]
        self.addProp("boundBox",{"min":min,"max":max})
        subMeshCount = len(self._indices)
        boneIndexList = []
        subIBIndex = []
        subsubMeshtriangles = []
        indexBuffer = []
        for i in range(subMeshCount):
            # 存了需要的骨骼数据索引
            subboneIndesList = []
            subboneIndesList.append([])
            boneIndexList.append(subboneIndesList)
            # 存了骨骼数目 24，24，24，10
            subIBIndex.append([])
            # 三角形数组，根据骨骼来划分为好几组划分
            subsubMeshTriangle = []
            subsubMeshtriangles.append(subsubMeshTriangle)
            # 必定有一个三角形组合
            subsubMeshTriangle.append([])
            subAllTriangle = []
            indexs = self._indices[i]
            triangleCount = int(len(indexs) / 3)
            # 开始组织ib,获得所有的三角形
            for index in range(triangleCount):
                triangIndex = index * 3
                triangle = Triangle()
                triangle.point1 = self._vertices[indexs[triangIndex]]
                triangle.point2 = self._vertices[indexs[triangIndex + 1]]
                triangle.point3 = self._vertices[indexs[triangIndex + 2]]
                subAllTriangle.append(triangle)
                pass
            # 将三角形根据骨骼索引分堆
            for triangleIndex in range(len(subAllTriangle)):
                tri = subAllTriangle[triangleIndex]
                tigleboneindexs = tri.triangleBoneIndex()
                isAdd = False
                for m in range(len(subboneIndesList)):
                    lastlist = FBXUnit.ListContainCount(tigleboneindexs, subboneIndesList[m])
                    lastlistCount = len(lastlist)
                    if lastlistCount == 0:
                        subsubMeshTriangle[m].append(tri)
                        isAdd = True
                        break
                        pass
                    elif len(subboneIndesList[m]) + lastlistCount <= FBXConfig.GetMaxBoneCount():
                        for c in range(lastlistCount):
                            subboneIndesList[m].append(lastlist[c])
                            pass
                        subsubMeshTriangle[m].append(tri)
                        isAdd = True
                        break
                        pass
                    pass
                if not isAdd:
                    newboneindexlist = []
                    newTriangleList = []
                    subboneIndesList.append(newboneindexlist)
                    subsubMeshTriangle.append(newTriangleList)
                    for w in range(len(tigleboneindexs)):
                        newboneindexlist.append(tigleboneindexs[w])
                        pass
                    newTriangleList.append(tri)
                    pass
                pass
            # 分堆之后检测增加点并且修改索引
            for q in range(len(subsubMeshTriangle)):
                subsubtriangles = subsubMeshTriangle[q]
                for h in range(len(subsubtriangles)):
                    trianglle = subsubtriangles[h]
                    trianglle.point1 = self.checkPoint(trianglle.point1, i, q)
                    trianglle.point2 = self.checkPoint(trianglle.point2, i, q)
                    trianglle.point3 = self.checkPoint(trianglle.point3, i, q)
                    pass
                pass
            lengths = 0
            for o in range(len(subsubMeshTriangle)):
                lengths += len(subsubMeshTriangle[o]) * 3
                subIBIndex[i].append(lengths)
                pass
            pass

        # 切换缩影且组织index数据
        for ii in range(subMeshCount):
            subsubtriangle = subsubMeshtriangles[ii]
            for tt in range(len(subsubtriangle)):
                boneindexlist = boneIndexList[ii][tt]
                for iii in range(len(subsubtriangle[tt])):
                    trii = subsubtriangle[tt][iii]
                    self.changeBoneIndex(boneindexlist, trii.point3)
                    self.changeBoneIndex(boneindexlist, trii.point2)
                    self.changeBoneIndex(boneindexlist, trii.point1)

                    indexBuffer.append(trii.point1.index)
                    indexBuffer.append(trii.point2.index)
                    indexBuffer.append(trii.point3.index)
                    pass
                pass
            pass

        stringDatas = []
        stringDatas.append("MESH")
        stringDatas.append("SUBMESH")
        # 版本号
        outfile.write_string(FBXConfig.GetMeshHead())
        # 标记数据信息区
        ContentAreaPosition_Start = outfile.pos()  # 预留数据区偏移地址
        outfile.write_uint32(0)  # UInt32 offset
        outfile.write_uint32(0)  # UInt32 blockLength

        # 内容段落信息区
        BlockAreaPosition_Start = outfile.pos()  # 预留段落数量
        blockCount = subMeshCount + 1
        outfile.write_uint16(blockCount)
        for i in range(blockCount):
            outfile.write_uint32(0)  # UInt32 blockStart
            outfile.write_uint32(0)  # UInt32 blockLength

        # 字符区
        StringAreaPosition_Start = outfile.pos()  # 预留字符区
        outfile.write_uint32(0)  # UInt32 offset
        outfile.write_uint16(0)  # count
        # 网格区
        MeshAreaPosition_Start = outfile.pos()
        outfile.write_uint16(stringDatas.index("MESH"))
        stringDatas.append(meshName)
        outfile.write_uint16(stringDatas.index(meshName))

        # vb
        outfile.write_uint16(1)
        VBMeshAreaPostion_Start = outfile.pos()

        for i in range(1):
            outfile.write_uint32(0)  # vbStart
            outfile.write_uint32(0)  # vbLength
            stringDatas.append(self.vbDeclaration)
            outfile.write_uint16(stringDatas.index(self.vbDeclaration))  # vbDeclar
            pass

        # ib
        IBMeshAreaPosition_Start = outfile.pos()
        outfile.write_uint32(0)  # ibStart
        outfile.write_uint32(0)  # ibLength
        self.writeBounds(outfile)

        # uint16 boneCount
        BoneAreaPosition_Start = outfile.pos()
        outfile.write_uint16(len(self.bonesName))  # boneCount
        for i in range(len(self.bonesName)):
            bname = self.bonesName[i]
            stringDatas.append(bname)
            outfile.write_uint16(stringDatas.index(bname))
            pass
        outfile.write_uint32(0)  # inverseGlobalBindPoseStart
        outfile.write_uint32(0)  # inverseGlobalBindPoseLength

        MeshAreaPosition_End = outfile.pos()
        MeshAreaSize = MeshAreaPosition_End - MeshAreaPosition_Start
        subMeshAreaPosition_Start = []
        subMeshAreaPosition_End = []
        subMeshAreaSize = []

        # 子网格
        for i in range(subMeshCount):
            subMeshAreaPosition_Start.append(outfile.pos())
            outfile.write_uint16(stringDatas.index("SUBMESH"))  # 解析函数名字符索引
            outfile.write_uint16(0)  # vbIndex
            outfile.write_uint32(0)  # ibStart
            outfile.write_uint32(0)  # ibLength
            boneIndexListCount = len(boneIndexList[i])
            outfile.write_uint16(boneIndexListCount)  # drawCount
            for j in range(boneIndexListCount):
                outfile.write_uint32(0)  # subIbStart
                outfile.write_uint32(0)  # subIbLength
                outfile.write_uint32(0)  # boneDicStart
                outfile.write_uint32(0)  # boneDicLength

            subMeshAreaPosition_End.append(outfile.pos())
            subMeshAreaSize.append(subMeshAreaPosition_End[i] - subMeshAreaPosition_Start[i])

        # 字符数据区
        StringDatasAreaPosition_Start = outfile.pos()
        for i in range(len(stringDatas)):
            outfile.write_string(stringDatas[i])

        StringDatasAreaPosition_End = outfile.pos()
        StringDatasAreaSize = StringDatasAreaPosition_End - StringDatasAreaPosition_Start

        # 内容数据区
        VBContentDatasAreaPosition_Start = outfile.pos()
        vertexCount = len(self._vertices)
        for i in range(vertexCount):
            outfile.write_byte(self._vertices[i].getByte())

        VBContentDatasAreaPosition_End = outfile.pos()
        VBContentDatasAreaSize = VBContentDatasAreaPosition_End - VBContentDatasAreaPosition_Start
        # indices
        IBContentDatasAreaPosition_Start = outfile.pos()
        if vertexCount > 65535:
            writeFun = outfile.write_uint32
        else:
            writeFun = outfile.write_uint16

        for i in range(len(indexBuffer)):
            writeFun(indexBuffer[i])
            pass
        IBContentDatasAreaPosition_End = outfile.pos()
        IBContentDatasAreaSize = IBContentDatasAreaPosition_End - IBContentDatasAreaPosition_Start

        inverseGlobalBindPosesDatasAreaPosition_Start = 0
        boneDicDatasAreaPosition_Start = 0
        boneDicDatasAreaPosition_End = 0
        lSkinCount = self._pMesh.GetDeformerCount(FbxDeformer.eSkin)
        for i in range(lSkinCount):
            lClusterCount = self._pMesh.GetDeformer(i, FbxDeformer.eSkin).GetClusterCount()
            transformMatrix = FbxAMatrix()
            transformLinkMatrix = FbxAMatrix()
            inverseGlobalBindPosesDatasAreaPosition_Start = outfile.pos()
            globalScale = FBXUnit.GetGlobalFactio()
            for j in range(lClusterCount):
                lCluster = self._pMesh.GetDeformer(i, FbxDeformer.eSkin).GetCluster(j)
                lCluster.GetTransformMatrix(transformMatrix)
                lCluster.GetTransformLinkMatrix(transformLinkMatrix)
                transformMatrix = transformLinkMatrix.Inverse()*transformMatrix
                for kk in range(3):
                    row = transformMatrix.GetRow(kk)
                    outfile.write_float(row[0])
                    outfile.write_float(row[1])
                    outfile.write_float(row[2])
                    outfile.write_float(row[3])
                row = transformMatrix.GetRow(3)
                outfile.write_float(row[0]*globalScale)
                outfile.write_float(row[1]*globalScale)
                outfile.write_float(row[2]*globalScale)
                outfile.write_float(row[3])

                # Display4DVector("0.队列数据", transformMatrix.GetRow(0))
                # Display4DVector("1.队列数据", transformMatrix.GetRow(1))
                # Display4DVector("2.队列数据", transformMatrix.GetRow(2))
                # Display4DVector("3.队列数据", transformMatrix.GetRow(3))
                pass
            boneDicDatasAreaPosition_Start = outfile.pos()
            for i in range(subMeshCount):
                for j in range(len(boneIndexList[i])):
                    boneIndexlist = boneIndexList[i][j]
                    for k in range(len(boneIndexlist)):
                        outfile.write_uint16(boneIndexlist[k])
                        pass
                    pass
                pass
            boneDicDatasAreaPosition_End = outfile.pos()
            pass

        # 倒推子网格区
        ibStart = 0
        ibend = 0
        boneDicStart = boneDicDatasAreaPosition_Start - StringDatasAreaPosition_Start;
        for i in range(subMeshCount):
            outfile.seek(subMeshAreaPosition_Start[i] + 4)
            iblength = len(self._indices[i])
            outfile.write_uint32(ibStart)
            outfile.write_uint32(iblength)
            outfile.seek(outfile.pos() + 2)
            boneIndexListCount = len(boneIndexList[i])
            subIBStart = 0
            for j in range(boneIndexListCount):
                outfile.write_uint32(subIBStart + ibStart)  # subIbStart
                outfile.write_uint32(subIBIndex[i][j] - subIBStart)  # subIbLength
                subIBStart = subIBIndex[i][j]
                outfile.write_uint32(boneDicStart)  # boneDicStart
                outfile.write_uint32(len(boneIndexList[i][j])*2)  # boneDicLength
                boneDicStart += len(boneIndexList[i][j])*2
            ibStart += iblength
            pass
        # 倒推网格区
        outfile.seek(VBMeshAreaPostion_Start)
        outfile.write_uint32(VBContentDatasAreaPosition_Start - StringDatasAreaPosition_Start)
        outfile.write_uint32(vertexCount)

        outfile.seek(IBMeshAreaPosition_Start)
        outfile.write_uint32(IBContentDatasAreaPosition_Start - StringDatasAreaPosition_Start)
        outfile.write_uint32(IBContentDatasAreaSize)

        outfile.seek(BoneAreaPosition_Start + (len(self.bonesName) + 1) * 2)
        outfile.write_uint32(inverseGlobalBindPosesDatasAreaPosition_Start -StringDatasAreaPosition_Start)
        outfile.write_uint32(boneDicDatasAreaPosition_Start - inverseGlobalBindPosesDatasAreaPosition_Start)
        # 倒推字符区
        outfile.seek(StringAreaPosition_Start)
        outfile.write_uint32(0)
        outfile.write_uint16(len(stringDatas))

        # 倒推段落区
        outfile.seek(BlockAreaPosition_Start + 2)
        outfile.write_uint32(MeshAreaPosition_Start)
        outfile.write_uint32(MeshAreaSize)
        for i in range(subMeshCount):
            outfile.write_uint32(subMeshAreaPosition_Start[i])
            outfile.write_uint32(subMeshAreaSize[i])
            pass
        # 倒推标记内容数据信息区
        outfile.seek(ContentAreaPosition_Start)
        outfile.write_uint32(StringDatasAreaPosition_Start)
        outfile.write_uint32(
            StringDatasAreaPosition_Start + StringDatasAreaSize + VBContentDatasAreaSize + IBContentDatasAreaSize +
            subMeshAreaSize[0])

        outfile.close()
        pass

    def changeBoneIndex(self, boneindexlist, vertexdata):
        if vertexdata.ischange:
            for i in range(4):
                vertexdata.boneIndex[i] = boneindexlist.index(vertexdata.boneIndex[i])
            pass
        vertexdata.ischange = False
        pass

    def checkPoint(self, vertexdata, subMeshindex, subsubMeshIndex):
        key = str(subMeshindex) + "," + str(subsubMeshIndex)
        # 第一次循环到这个点
        if vertexdata.subMeshindex == -1 and vertexdata.subsubMeshindex == -1:
            vertexdata.subMeshindex = subMeshindex
            vertexdata.subsubMeshindex = subsubMeshIndex
            return vertexdata
        # 点在与第一次的点相同
        elif vertexdata.subMeshindex == subMeshindex and vertexdata.subsubMeshindex == subsubMeshIndex:
            return vertexdata
        # 第一个重合点
        elif vertexdata.commonPoint is None:
            vertexdata.commonPoint = {}
            newvertexdata = vertexdata.clone(len(self._vertices))
            self._vertices.append(newvertexdata)
            vertexdata.commonPoint.setdefault(key, newvertexdata)
            return newvertexdata
        else:
            if vertexdata.commonPoint.get(key) is not None:
                return vertexdata.commonPoint.get(key)
            else:
                newvertexdata = vertexdata.clone(len(self._vertices))
                self._vertices.append(newvertexdata)
                vertexdata.commonPoint.setdefault(key, newvertexdata)
                return newvertexdata
        pass

    def saveFileMesh(self, outfile, meshName):
        self.analysisMeshData()
        subMeshCount = len(self._indices)
        blockCount = subMeshCount + 1

        stringDatas = []
        stringDatas.append("MESH")
        stringDatas.append("SUBMESH")
        # 版本号
        outfile.write_string(FBXConfig.GetMeshHead())
        # 标记数据信息区
        ContentAreaPosition_Start = outfile.pos()  # 预留数据区偏移地址
        outfile.write_uint32(0)  # UInt32 offset
        outfile.write_uint32(0)  # UInt32 blockLength

        # 内容段落信息区
        BlockAreaPosition_Start = outfile.pos()  # 预留段落数量
        outfile.write_uint16(blockCount)
        for i in range(blockCount):
            outfile.write_uint32(0)  # UInt32 blockStart
            outfile.write_uint32(0)  # UInt32 blockLength

        # 字符区
        StringAreaPosition_Start = outfile.pos()  # 预留字符区
        outfile.write_uint32(0)  # UInt32 offset
        outfile.write_uint16(0)  # count
        # 网格区
        MeshAreaPosition_Start = outfile.pos()
        outfile.write_uint16(stringDatas.index("MESH"))
        stringDatas.append(meshName)
        outfile.write_uint16(stringDatas.index(meshName))

        # vb
        outfile.write_uint16(1)
        VBMeshAreaPostion_Start = outfile.pos()

        for i in range(1):
            outfile.write_uint32(0)
            outfile.write_uint32(0)
            stringDatas.append(self.vbDeclaration)
            outfile.write_uint16(stringDatas.index(self.vbDeclaration))
            pass

        # ib
        IBMeshAreaPosition_Start = outfile.pos()
        outfile.write_uint32(0)  # ibStart
        outfile.write_uint32(0)  # ibLength
        self.writeBounds(outfile)

        # uint16 boneCount
        BoneAreaPosition_Start = outfile.pos()
        outfile.write_uint16(0)  # boneCount
        outfile.write_uint32(0)  # bindPoseStart
        outfile.write_uint32(0)  # bindPoseLength
        outfile.write_uint32(0)  # inverseGlobalBindPoseStart
        outfile.write_uint32(0)  # inverseGlobalBindPoseLength
        MeshAreaPosition_End = outfile.pos()
        MeshAreaSize = MeshAreaPosition_End - MeshAreaPosition_Start
        subMeshAreaPosition_Start = []
        subMeshAreaPosition_End = []
        subMeshAreaSize = []

        # 子网格
        for i in range(subMeshCount):
            subMeshAreaPosition_Start.append(outfile.pos())
            outfile.write_uint16(stringDatas.index("SUBMESH"))  # 解析函数名字符索引
            outfile.write_uint16(0)  # vbIndex
            outfile.write_uint32(0)  # ibStart
            outfile.write_uint32(0)  # ibLength
            outfile.write_uint16(1)  # drawCount

            outfile.write_uint32(0)  # subIbStart
            outfile.write_uint32(0)  # subIbLength
            outfile.write_uint32(0)  # boneDicStart
            outfile.write_uint32(0)  # boneDicLength
            subMeshAreaPosition_End.append(outfile.pos())
            subMeshAreaSize.append(subMeshAreaPosition_End[i] - subMeshAreaPosition_Start[i])

        # 字符数据区
        StringDatasAreaPosition_Start = outfile.pos()
        for i in range(len(stringDatas)):
            outfile.write_string(stringDatas[i])

        StringDatasAreaPosition_End = outfile.pos()
        StringDatasAreaSize = StringDatasAreaPosition_End - StringDatasAreaPosition_Start

        # 内容数据区
        VBContentDatasAreaPosition_Start = outfile.pos()
        vertexCount = len(self._vertices)
        for i in range(vertexCount):
            outfile.write_byte(self._vertices[i].getByte())

        VBContentDatasAreaPosition_End = outfile.pos()
        VBContentDatasAreaSize = VBContentDatasAreaPosition_End - VBContentDatasAreaPosition_Start
        # indices
        IBContentDatasAreaPosition_Start = outfile.pos()
        if vertexCount > 65535:
            writeFun = outfile.write_uint32
        else:
            writeFun = outfile.write_uint16
        for i in range(len(self._indices)):
            indexs = self._indices[i]
            for j in range(len(indexs)):
                writeFun(indexs[j])
            pass

        IBContentDatasAreaPosition_End = outfile.pos()
        IBContentDatasAreaSize = IBContentDatasAreaPosition_End - IBContentDatasAreaPosition_Start

        # 倒推子网格区
        ibStart = 0
        iblength = 0
        for i in range(subMeshCount):
            outfile.seek(subMeshAreaPosition_Start[i] + 4)
            iblength = len(self._indices[i])
            outfile.write_uint32(ibStart)
            outfile.write_uint32(iblength)
            outfile.seek(outfile.pos() + 2)
            outfile.write_uint32(ibStart)
            outfile.write_uint32(iblength)
            ibStart += iblength
            pass
        # 倒推网格区
        outfile.seek(VBMeshAreaPostion_Start)
        outfile.write_uint32(VBContentDatasAreaPosition_Start - StringDatasAreaPosition_Start)
        outfile.write_uint32(vertexCount)

        outfile.seek(IBMeshAreaPosition_Start)
        outfile.write_uint32(IBContentDatasAreaPosition_Start - StringDatasAreaPosition_Start)
        outfile.write_uint32(IBContentDatasAreaSize)
        # 倒推字符区
        outfile.seek(StringAreaPosition_Start)
        outfile.write_uint32(0)
        outfile.write_uint16(len(stringDatas))

        # 倒推段落区
        outfile.seek(BlockAreaPosition_Start + 2)
        outfile.write_uint32(MeshAreaPosition_Start)
        outfile.write_uint32(MeshAreaSize)
        for i in range(subMeshCount):
            outfile.write_uint32(subMeshAreaPosition_Start[i])
            outfile.write_uint32(subMeshAreaSize[i])
            pass
        # 倒推标记内容数据信息区
        outfile.seek(ContentAreaPosition_Start)
        outfile.write_uint32(StringDatasAreaPosition_Start)
        outfile.write_uint32(
            StringDatasAreaPosition_Start + StringDatasAreaSize + VBContentDatasAreaSize + IBContentDatasAreaSize +
            subMeshAreaSize[0])

        outfile.close()
        pass

    def writeBounds(self, outfile):
        outfile.write_float(self.minx)
        outfile.write_float(self.miny)
        outfile.write_float(self.minz)
        outfile.write_float(self.maxx)
        outfile.write_float(self.maxy)
        outfile.write_float(self.maxz)
        pass

    def analysubMesh(self):
        mesh = self._pMesh
        lPolygonCount = mesh.GetPolygonCount()
        groups = []
        lLayerMaterial = mesh.GetLayer(0).GetMaterials()
        for i in range(lPolygonCount):
            lMatId = -1
            if lLayerMaterial is not None:
                lMatId = lLayerMaterial.GetIndexArray().GetAt(i)
                pass
            if lMatId < 0:
                lMatId = 0
            groups.append({"pCount": i, "matid": lMatId})
        groups.sort(key=itemgetter('matid'))
        return groups
        pass

    def analysisMeshData(self):
        mesh = self._pMesh
        runList = []
        # 所有顶点
        controlPoints = mesh.GetControlPoints()
        self.vbDeclaration = "POSITION"
        runList.append(0)
        # 法线
        normals = mesh.GetElementNormal()
        if normals is not None:
            self.vbDeclaration += ",NORMAL"
            runList.append(1)
            pass
        # 颜色
        leVtxc = mesh.GetElementVertexColor(0)
        if leVtxc is not None:
            self.vbDeclaration += ",COLOR"
            runList.append(2)
            pass
        # uv0
        leUV1 = mesh.GetElementUV(0)
        if leUV1 is not None:
            self.vbDeclaration += ",UV"
            runList.append(3)
            pass
        # uv1
        leUV2 = mesh.GetElementUV(1)
        if leUV2 is not None:
            self.vbDeclaration += ",UV1"
            runList.append(4)
            pass
        # 权重法线
        if self._isSkinnerMesh:
            self.vbDeclaration += ",BLENDWEIGHT,BLENDINDICES"
            runList.append(5)
            runList.append(6)
            pass
        # 切线
        leTangent = mesh.GetElementTangent(0)
        if leTangent is not None:
            self.vbDeclaration += ",TANGENT"
            runList.append(7)
            pass
        vertexId = 0

        groups = self.analysubMesh()

        lastmatid = -1
        indexs = []
        self._indices.append(indexs)
        self.maxx = self.maxy = self.maxz = float('-inf')
        self.minx = self.miny = self.minz = float('inf')

        for i in range(mesh.GetPolygonCount()):

            lPolygonSize = mesh.GetPolygonSize(i)
            groupinfo = groups[i]
            if lastmatid >= 0 and lastmatid != groupinfo['matid']:
                indexs = []
                self._indices.append(indexs)
                pass
            lastmatid = groupinfo['matid']
            cPolygonIndex = []
            globalScale = FBXUnit.GetGlobalFactio()
            for j in range(lPolygonSize):
                lControlPointIndex = mesh.GetPolygonVertex(groupinfo['pCount'], j)
                dataarr = []
                # 顶点位置
                vertice = FBXUnit.GetVertex(controlPoints, lControlPointIndex)

                xPoint = vertice[0] * globalScale
                yPoint = vertice[2] * globalScale
                zPoint = vertice[1] * globalScale

                dataarr.append(xPoint)
                dataarr.append(yPoint)
                dataarr.append(zPoint)
                self.minx = min(xPoint, self.minx)
                self.miny = min(yPoint, self.miny)
                self.minz = min(zPoint, self.minz)
                self.maxx = max(xPoint, self.maxx)
                self.maxy = max(yPoint, self.maxy)
                self.maxz = max(zPoint, self.maxz)
                # 法向量
                if normals is not None:
                    normal = FBXUnit.GetDataByPolygonIndexOrVertexIndex(normals, vertexId, vertexId)
                    dataarr.append(normal[0])
                    dataarr.append(normal[2])
                    dataarr.append(normal[1])
                # 顶点颜色
                if leVtxc is not None:
                    color = FBXUnit.GetDataByPolygonIndexOrVertexIndex(leVtxc, vertexId, lControlPointIndex)
                    dataarr.append(color.mRed)
                    dataarr.append(color.mGreen)
                    dataarr.append(color.mBlue)
                    dataarr.append(color.mAlpha)
                    pass
                # uv
                if leUV1 is not None:
                    uv1 = FBXUnit.GetDataByPolygonIndexOrVertexIndex(leUV1, vertexId, lControlPointIndex)
                    dataarr.append(uv1[0])
                    dataarr.append(uv1[1])
                    pass
                # uv1
                if leUV2 is not None:
                    uv2 = FBXUnit.GetDataByPolygonIndexOrVertexIndex(leUV2, vertexId, lControlPointIndex)
                    dataarr.append(uv2[0])
                    dataarr.append(uv2[1])
                    pass
                if self._isSkinnerMesh:
                    boneIndex = [0, 0, 0, 0]
                    boneWeigth = [0, 0, 0, 0]
                    list = self.weightTable[lControlPointIndex]
                    count = min(len(list), 4)
                    for i in range(count):
                        tabData = list[i]
                        boneIndex[i] = tabData["index"]
                        boneWeigth[i] = tabData["weight"]
                    dataarr.append(boneWeigth[0])
                    dataarr.append(boneWeigth[1])
                    dataarr.append(boneWeigth[2])
                    dataarr.append(boneWeigth[3])
                    dataarr.append(boneIndex[0])
                    dataarr.append(boneIndex[1])
                    dataarr.append(boneIndex[2])
                    dataarr.append(boneIndex[3])
                    pass

                if leTangent is not None:
                    tangent = FBXUnit.GetDataByPolygonIndexOrVertexIndex(leTangent, vertexId, lControlPointIndex)
                    dataarr.append(tangent[0])
                    dataarr.append(tangent[2])
                    dataarr.append(tangent[1])
                    dataarr.append(tangent[3])
                    pass
                cPolygonIndex.append(self.getVerData(dataarr,runList))
                vertexId += 1
                pass  # end for
            for j in range(lPolygonSize - 2):
                indexs.append(cPolygonIndex[0])
                indexs.append(cPolygonIndex[j + 1])
                indexs.append(cPolygonIndex[j + 2])
                pass  # end for
            pass
        pass

    def getVerData(self, dataArr, runList):
        hashValue = hashMap(dataArr)
        if self._hashMap.get(hashValue) is not None:
            return self._hashMap.get(hashValue)
        else:
            verData = VertexData(len(self._vertices), runList, dataArr)
            self._vertices.append(verData)
            self._hashMap.setdefault(hashValue, verData.index)
            return verData.index
