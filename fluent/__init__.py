'''
Copyright (C) 2019
rudy.michau@gmail.com

Created by RUDY MICHAU

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import gpu
from gpu_extras.batch import batch_for_shader


import blf
import bgl
import bmesh
import bpy
from bpy.app.handlers import persistent
from bpy_extras.view3d_utils import region_2d_to_location_3d
from bpy_extras import view3d_utils
from bpy.types import Menu
import bpy.utils.previews
from collections import Counter
import math
import mathutils
from mathutils import Matrix, Vector
from os.path import join, dirname
import time
import urllib
import webbrowser

bl_info = {
    "name": "Fluent",
    "description": "hard surface modeling addon",
    "author": "Rudy MICHAU",
<<<<<<< HEAD
    "version": (1, 1, 2),
=======
    "version": (1, 1, 5),
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Object" }

tool_called = 'CUT'
init_pref = True
<<<<<<< HEAD
=======
polydraw_run = False
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

translate = {
    "ENGLISH" : {
        "cutCall":"Cut/Add",
        "sliceCall":"Slice",
        "createCall":"Creation",
        "addLatestBevel": "Add latest bevel",
        "symetrizePlan":"Symetrize a Plan",
        "autoComplete" : "Auto-Complete",
        "booleanDisplay":"Show/Hide boolean object",
        "wireframe":"Show/Hide wireframe",
        "latestBevelWidth" : "Latest bevel width",
        "angleLimit" : "Angle Limit",
        "defaultDepth" : "Default depth",
        "corner" : "Default bevel width",
        "bevelResolution" : "Bevel resolution",
        "circleResolution" : "Default circle resolution",
        "autoMirror" : "Auto-mirror",
        "otherAdjustment" : "Other adjustments",
        "moveObj" : "Move object along plane : G, Shift+Z+Z",
        "moveObjZ" : "Up/Down object along normal of plane : G, Z, Z",
        "finish" : "Finish : Right Click",
        "showBoolObj" : "Show / Hide boolean object : H",
        "cancel" : "Cancel : Esc",
        "finishCurrentAdjustement" : "Finish current adjustment : Left Click",
        "horizontalMouseMove": "Horizontal mouse move",
        "fastSlow":"Fast/Slow",
        "thicknessOffset" : "Thickness / Offset toggle",
        "crossModel" : "Cross the model",
        "useFlyMenu" : "Use fly menu : hold left click, go to wanted tool, relase left click",
        "roundStraight" : "Round/Straight",
        "remove" : "Remove",
        "steps" : "Steps",
        "smoothCircle" : "High resolution",
        "pressAxis" : "Press an axis to show it, press it again to hide it",
        "axisSelection" : "Axis activation",
        "offset" : "Offset",
        "count" : "Count",
        'radius' : 'Radius',
        'number' : "Number of elements",
        'rotation90' : '90° rotation',
        'solidify' : 'Solidify',
        'firstBevel' : 'First Bevel',
        'secondbevel' : 'Second Bevel',
        'mirror' : 'mirror',
        'array' : 'Array',
        'circularArray' : 'Circular Array',
        'adjustment' : 'adjustment',
        'latestBevelSegments' : 'Latest bevel segments',
        'validateDrawing' : 'Validate polygon',
        'validatePath' : 'Validate path',
        'fakeSlice':'Fake slice',
        'duplicate':'Duplicate',
        'synchBool':'Synchronize boolean objects',
        'makePreset':'Make/Clear preset',
        'cutAgain':'Cut again',
<<<<<<< HEAD
        'cleanBooleanApplication':'Boolean supports'
=======
        'cleanBooleanApplication':'Boolean supports',
        'editCall':'Edit',
        'technicalDisplay':'Technical Display',
        'displayGrid' : 'Display grid : Right Click on a face',
        'drawOutside':'Draw outside : Shift + Left Click on face before to draw',
        'snap':'Snap : Hold Ctrl',
        'drawFromCenter':'Draw from center : Hold Shift',
        'drawSquare':'Draw square : Hold Ctrl',
        'drawOrtho':'Draw in ortho direction',
        'undo':'Undo',
        'gridResolution' : 'Grid resolution',
        'gridRotation' : 'Grid rotation',
        'alignmentHelper':'Alignment helper',
        'revolveMode':'Revolver Mode',
        'revolve':'Revolve'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    },
    "CHINESE" : {
        "cutCall":"切割/添加",
        "sliceCall":"切片",
        "createCall":"创建",
        "addLatestBevel":"给当前对象添加倒角",
        "symetrizePlan":"使对称",
        "autoComplete" : "自动完成",
        "booleanDisplay":"显示/隐藏布尔对象",
        "wireframe":"线框",
        "latestBevelWidth" : "当前倒角宽度",
        "angleLimit" : "角度限制",
        "defaultDepth" : "默认深度",
        "corner" : "默认倒角宽度",
        "bevelResolution" : "倒角分辨率",
        "circleResolution" : "默认棱分段数",
        "autoMirror" : "自动镜像",
        "otherAdjustment" : "其他调整",
        "moveObj" : "沿平面移动 : G, Shift+Z+Z",
        "moveObjZ" : "沿平面法线上/下移动对象 : G, Z, Z",
        "finish" : "完成 : 点击右键",
        "showBoolObj" : "显示/隐藏 布尔对象 : H",
        "cancel" : "取消 : Esc",
        "finishCurrentAdjustement" : "完成当前调整: 点击左键",
        "horizontalMouseMove": "水平移动鼠标",
        "fastSlow":"快速/慢速",
        "thicknessOffset" : "厚度/偏移模式切换",
        "crossModel" : "贯穿模型",
        "useFlyMenu" : "使用浮动菜单 : 按住左键, 把鼠标指针移动到你想使用的工具上去, 然后松开左键",
        "roundStraight" : "圆角/直角",
        "remove" : "移除",
        "steps" : "分辨率",
        "smoothCircle" : "高分辨",
        "pressAxis" : "按下一个轴显示，再按一次隐藏",
        "axisSelection" : "激活轴",
        "offset" : "偏移",
        "count" : "计数",
        'radius' : '半径',
        'number' : "元素数量",
        'rotation90' : '90° 旋转',
        'solidify' : '固化',
        'firstBevel' : '倒角（一）',
        'secondbevel' : '倒角（二）',
        'mirror' : '镜像',
        'array' : '阵列',
        'circularArray' : '圆形阵列',
        'adjustment' : '调整',
        'latestBevelSegments' : 'Latest bevel segments',
        'validateDrawing' : 'Validate polygon',
        'validatePath' : 'Validate path',
        'fakeSlice':'Fake slice',
        'duplicate':'复制',
        'synchBool':'Synchronize boolean objects',
        'makePreset':'Make/Clear preset',
        'cutAgain':'Cut again',
<<<<<<< HEAD
        'cleanBooleanApplication':'Boolean supports'
=======
        'cleanBooleanApplication':'Boolean supports',
        'editCall':'Edit',
        'technicalDisplay':'Technical Display',
        'displayGrid' : 'Display grid : Right Click on a face',
        'drawOutside':'Draw outside : Shift + Left Click on face before to draw',
        'snap':'Snap : Hold Ctrl',
        'drawFromCenter':'Draw from center : Hold Shift',
        'drawSquare':'Draw square : Hold Ctrl',
        'drawOrtho':'Draw in ortho direction',
        'undo':'Undo',
        'gridResolution' : 'Grid resolution',
        'gridRotation' : 'Grid rotation',
        'alignmentHelper':'Alignment helper',
        'revolveMode':'Revolver Mode',
        'revolve':'Revolve'
    },
    "TRAD_CHINESE" : {
        "cutCall":"切/增加",
        "sliceCall":"切片",
        "createCall":"創造",
        "addLatestBevel": "新增最後斜角",
        "symetrizePlan":"對稱平面",
        "autoComplete" : "自動完成",
        "booleanDisplay":"顯示/隱藏布林物件",
        "wireframe":"顯示/隱藏線架構",
        "latestBevelWidth" : "最後斜角寬度",
        "angleLimit" : "角度極限",
        "defaultDepth" : "預設深度",
        "corner" : "預設斜角寬度",
        "bevelResolution" : "斜角解析度",
        "circleResolution" : "預設圓解析度",
        "autoMirror" : "自動鏡射",
        "otherAdjustment" : "其他調整",
        "moveObj" : "沿平面移動物件 : G, Shift+Z+Z",
        "moveObjZ" : "沿平面法向移動物件 : G, Z, Z",
        "finish" : "完成 : 右鍵",
        "showBoolObj" : "顯示/隱藏布林物件 : H",
        "cancel" : "取消 : Esc",
        "finishCurrentAdjustement" : "完成目前調整 : 左鍵",
        "horizontalMouseMove": "滑鼠水平移動",
        "fastSlow":"快/慢",
        "thicknessOffset" : "厚度/偏移切換",
        "crossModel" : "模型剖面",
        "useFlyMenu" : "使用懸空面板 : 按住左鍵, 游標移到欲選工具, 放開左鍵",
        "roundStraight" : "圓/直",
        "remove" : "移除",
        "steps" : "階數",
        "smoothCircle" : "高解析度",
        "pressAxis" : "在軸上按一次顯示, 再按一次隱藏",
        "axisSelection" : "啟動軸",
        "offset" : "偏移",
        "count" : "數量",
        'radius' : '半徑',
        'number' : "元素數量",
        'rotation90' : '90度旋轉',
        'solidify' : '實體化',
        'firstBevel' : '第一斜角',
        'secondbevel' : '第二斜角',
        'mirror' : '鏡射',
        'array' : '陣列',
        'circularArray' : '圓形陣列',
        'adjustment' : '調整',
        'latestBevelSegments' : '最後斜角段數',
        'validateDrawing' : '驗證多邊形',
        'validatePath' : '驗證路徑',
        'fakeSlice':'假切片',
        'duplicate':'複製',
        'synchBool':'同步布林物件',
        'makePreset':'建立/清空預設',
        'cutAgain':'再切',
        'cleanBooleanApplication':'布林優化',
        'editCall':'編輯',
        'technicalDisplay':'技術顯示',
        'displayGrid' : '顯示格線：在面上按右鍵',
        'drawOutside':'從外面畫：畫之前在面上按Shift +左鍵',
        'snap':'Snap : 鎖點：按住Ctrl鍵',
        'drawFromCenter':'從中心畫：按住Shift鍵',
        'drawSquare':'畫方形：按住Ctrl鍵',
        'drawOrtho':'沿平行向畫',
        'undo':'復原',
        'gridResolution' : '格線解析度',
        'gridRotation' : '格線角度',
        'alignmentHelper':'對齊輔助器',
        'revolveMode':'輪盤模式',
        'revolve':'迴轉'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    },
    "JAPANESE":{
        "cutCall":"カット/追加",
        "sliceCall":"スライス",
        "createCall":"生成",
        "addLatestBevel": "最終ベベルの追加",
        "symetrizePlan":"対称化する",
        "autoComplete" : "オートコンプリート",
        "booleanDisplay":"ブーリアンオブジェクト表示/非表示",
        "wireframe":"ワイヤーフレーム表示/非表示",
        "latestBevelWidth" : "最新ベベルの幅",
        "angleLimit" : "アングル制限",
        "defaultDepth" : "デフォルトの深さ",
        "corner" : "デフォルトのベベル幅",
        "bevelResolution" : "ベベル解像度",
        "circleResolution" : "デフォルトの円解像度",
        "autoMirror" : "オートミラー",
        "otherAdjustment" : "その他の調整",
        "moveObj" : "平面に沿ったオブジェクトの移動 : G, Shift+Z+Z",
        "moveObjZ" : "平面の法線に沿ったオブジェクトの上下移動 : G, Z, Z",
        "finish" : "終了 : 右クリック",
        "showBoolObj" : "ブーリアンオブジェクト表示/非表示 : H",
        "cancel" : "キャンセル : Esc",
        "finishCurrentAdjustement" : "現在の調整を終了する : 左クリック",
        "horizontalMouseMove": "マウスの水平移動",
        "fastSlow":"速い/遅い",
        "thicknessOffset" : "厚み/オフセット 切り替え",
        "crossModel" : "モデルの交差",
        "useFlyMenu" : "フライメニューを使用 : 左クリックを押したままツールを選び、左クリックを解除します。",
        "roundStraight" : "丸型/ストレート型",
        "remove" : "削除",
        "steps" : "解像度",
        "smoothCircle" : "高解像度",
        "pressAxis" : "軸を押すと表示され、もう一度押すと非表示になります",
        "axisSelection" : "軸をアクティブ",
        "offset" : "オフセット",
        "count" : "数",
        'radius' : '半径',
        'number' : "要素数",
        'rotation90' : '90°回転',
        'solidify' : '固める',
        'firstBevel' : '1st ベベル',
        'secondbevel' : '2nd ベベル',
        'mirror' : '対称',
        'array' : '配列',
        'circularArray' : '円形配列',
        'adjustment' : '調整',
        'latestBevelSegments' : '最新ベベルのセグメント',
<<<<<<< HEAD
        'validateDrawing' : 'Validate polygon',
        'validatePath' : 'Validate path',
        'fakeSlice':'Fake slice',
        'duplicate':'複製',
        'synchBool':'ブーリアンオブジェクトの同期',
        'makePreset':'Make/Clear preset',
        'cutAgain':'Cut again',
        'cleanBooleanApplication':'Boolean supports'
=======
        'validateDrawing' : 'ポリゴンをアクセプト',
        'validatePath' : 'パスをアクセプト',
        'fakeSlice':'偽のスライス',
        'duplicate':'複製',
        'synchBool':'ブーリアンオブジェクトの同期',
        'makePreset':'プリセットを作成/空にする',
        'cutAgain':'もう一度切る',
        'cleanBooleanApplication':'ブーリアン最適化',
        'editCall':'編集',
        'technicalDisplay':'テクニカルディスプレイ',
        'displayGrid' : 'グリッド線を表示：面を右クリック',
        'drawOutside':'外側から描く：ペイントする前に顔の上でShift +左ボタンを描く',
        'snap':'Snap : スナップ：Ctrlキーを押しながら',
        'drawFromCenter':'中心から描く：Shiftキーを押しながら',
        'drawSquare':'正方形を描く：Ctrlキーを押しながら',
        'drawOrtho':'正射影',
        'undo':'元に戻す',
        'gridResolution' : 'グリッドの解像度',
        'gridRotation' : 'グリッド回転',
        'alignmentHelper':'アライメント補助',
        'revolveMode':'回るモード',
        'revolve':'回る'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    },
    "FRANCAIS" : {
        "cutCall":"Creuser/Ajouter",
        "sliceCall":"Découper",
        "createCall":"Nouvel objet",
        "addLatestBevel":"Ajouter un chamfrein",
        "symetrizePlan":"Symétrie axiale d'un plan",
        "autoComplete" : "Finalisation",
        "booleanDisplay":"Montrer/Cacher les booléens",
        "wireframe":"Afficher/Cacher le maillage",
        "latestBevelWidth" : "Taille du chamfrein",
        "angleLimit" : "Angle limite",
        "defaultDepth" : "Profondeur par défaut",
        "corner" : "Largeur du premier bevel",
        "bevelResolution" : "Résolution des chamfreins",
        "circleResolution" : "Résolution par défaut des cercles",
        "autoMirror" : "Miroir automatique",
        "otherAdjustment" : "Autres options",
        "moveObj" : "Déplacer l'objet dans le plan : G, Shift+Z+Z",
        "moveObjZ" : "Monter/Descendre l'objet : G, Z, Z",
        "finish" : "Terminer : Right Click",
        "showBoolObj" : "Montrer/Cacher les objets booléens : H",
        "cancel" : "Annuler : Esc",
        "finishCurrentAdjustement" : "Quitter l'ajustement en cours : Left Click",
        "horizontalMouseMove": "Bouger la souris horizontalement",
        "fastSlow":"Rapide / Lent",
        "thicknessOffset" : "Épaisseur / Décalage, basculer avec",
        "crossModel" : "Traverser le modèle",
        "useFlyMenu" : "Menu vollant : maintenir click gauche et relacher sur l'icône shouaité",
        "roundStraight" : "Arrondi/Droit",
        "remove" : "Supprimer",
        "steps" : "Résolution",
        "smoothCircle" : "Haute résolution",
        "pressAxis" : "Appuyer un axe pour l'activer, ré-appuyer pour le désactiver",
        "axisSelection" : "Activation des axes",
        "offset" : "Décalage",
        "count" : "Nombre",
        'radius' : 'Rayon',
        'number' : "Nombre d'éléments",
        'rotation90' : 'Rotation à 90°',
        'solidify' : 'Extrusion',
        'firstBevel' : 'Premier Chamfrein',
        'secondbevel' : 'Second Chamfrein',
        'mirror' : 'Miroir',
        'array' : 'Répétition',
        'circularArray' : 'Répétition Circulaire',
        'adjustment' : 'Ajustement',
        'latestBevelSegments' : 'Résolution du dernier chamfrein',
        'validateDrawing' : 'Validate polygon',
        'validatePath' : 'Validate path',
        'fakeSlice':'Fausse découpe',
        'duplicate':'Dupliquer',
        'synchBool':'Synchroniser les booléens',
        'makePreset':'Créer/Supprimer préconfiguration',
        'cutAgain':'Nouvelle coupe',
<<<<<<< HEAD
        'cleanBooleanApplication':'Création de support'
=======
        'cleanBooleanApplication':'Création de support',
        'editCall':'Éditer',
        'technicalDisplay':'Vue Technique',
        'displayGrid' : 'Afficher la grille : Click droit sur une face',
        'drawOutside':'Dessin à l\'extérieur : Shift + clique gauche sur une face avant de dessiner',
        'snap':'Snap : Maintenir Ctrl',
        'drawFromCenter':'Dessin à partir du centre : Maintenir Shift',
        'drawSquare':'Dessiner un carré : Maintenir Ctrl',
        'drawOrtho':'Dessiner dans les directions X/Y/Z',
        'undo':'Retour',
        'gridResolution' : 'Résolution de la grille',
        'gridRotation' : 'Rotation de la grille',
        'alignmentHelper':'Aide à l\'alignement',
        'revolveMode':'Tracer un profil de révolution',
        'revolve':'Révolution'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    }
}

def get_addon_preferences():
    addon_key = __package__.split(".")[0]
    addon_prefs = bpy.context.preferences.addons[addon_key].preferences

    return addon_prefs

def check_update():
    adresse = 'http://cgthoughts.com/fluent_current_version/index.html'
    response = urllib.request.urlopen(adresse)
    html = str(response.read())
    last_version = html[2:11]
    current_version = str(bl_info['version'])
    if last_version != current_version:
        return True, last_version
    else:
        return False, False

def active_obj(obj):
    bpy.context.view_layer.objects.active = obj

fluent_icons_collection = {}
fluent_icons_loaded = False

# Chargement des icones

def load_icons():
    global fluent_icons_collection
    global fluent_icons_loaded

    if fluent_icons_loaded: return fluent_icons_collection["main"]

    custom_icons = bpy.utils.previews.new()

    icons_dir = join(dirname(__file__))

    custom_icons.load("autocomplete_one", join(icons_dir, "autocomplete_one.png"), 'IMAGE')
    custom_icons.load("sym", join(icons_dir, "sym.png"), 'IMAGE')
    custom_icons.load("latest_bevel", join(icons_dir, "latest_bevel.png"), 'IMAGE')
    custom_icons.load("show_bool", join(icons_dir, "show_bool.png"), 'IMAGE')
    custom_icons.load("cut", join(icons_dir, "cut.png"), 'IMAGE')
    custom_icons.load("slice", join(icons_dir, "slice.png"), 'IMAGE')
    custom_icons.load("creation", join(icons_dir, "creation.png"), 'IMAGE')
    custom_icons.load("wireframe", join(icons_dir, "wireframe.png"), 'IMAGE')
    custom_icons.load("duplicate", join(icons_dir, "duplicate.png"), 'IMAGE')
    custom_icons.load("gumroad", join(icons_dir, "gumroad.png"), 'IMAGE')
    custom_icons.load("bm", join(icons_dir, "bm.png"), 'IMAGE')
    custom_icons.load("warning", join(icons_dir, "warning.png"), 'IMAGE')
    custom_icons.load("preset", join(icons_dir, "preset.png"), 'IMAGE')
<<<<<<< HEAD
=======
    custom_icons.load("edit", join(icons_dir, "edit.png"), 'IMAGE')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

    fluent_icons_collection["main"] = custom_icons
    fluent_icons_loaded = True

    return fluent_icons_collection["main"]

def clear_icons():
    global fluent_icons_loaded
    for icon in fluent_icons_collection.values():
        bpy.utils.previews.remove(icon)
    fluent_icons_collection.clear()
    fluent_icons_loaded = False

# dessin à l'écran ***************************************************************************************************
<<<<<<< HEAD
HIGHTLIGHT = (0.0, 0.643, 1, 1)
=======
# HIGHTLIGHT = (0.0, 0.643, 1, 1)
# HIGHTLIGHT = get_addon_preferences().hightlight
HIGHTLIGHT = (0, 0.8, 1, 1)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
WHITE = (1, 1, 1, 1)
CR = "Carriage Return"
menu_offset = [16, 0]
ico_size = 24
<<<<<<< HEAD
ico_size_factor = 1
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
ico_marge = 8

def draw_line(coords):
    # coords = [(1, 1, 1), (-2, 0, 0), (-2, -1, 3), (0, 1, 1)]
    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    shader.bind()
<<<<<<< HEAD
    shader.uniform_float("color", (1, 0.349, 0, 1))
=======
    shader.uniform_float("color", (1, 1, 1, 1))
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def draw_square_large(x, y, color, delta = 0):
    vertices = (
        (0, 0), (0, 8), (8, 8),(8, 0)
        )
    indices = (
        (0, 1, 2),(0, 2, 3)
        )
    vertices = repositionning_3d(vertices, x, y)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def repositionning_3d(vertices, x, y):
    # replace le dessin
    vertices_list = list(vertices)
    i = 0
    for v in vertices_list:
        coord = list(v)
        coord[0] = coord[0] + x
        coord[1] = coord[1] + y
        vertices_list[i] = tuple(coord)
        i = i+1
    vertices = tuple(vertices_list)
    return vertices

def draw_square(x, y, color, delta = 0):
    vertices = (
        (0, 0), (0, 4), (4, 4),(4, 0)
        )
    indices = (
        (0, 1, 2),(0, 2, 3)
        )
    vertices = repositionning_3d(vertices, x, y)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

<<<<<<< HEAD
=======
def draw_all_square(coord_list, color):
    vertices = []
    indices = []
    i = 0
    for c in coord_list:
        vertices.append([0+c[0], 0+c[1]])
        vertices.append([0+c[0], 4+c[1]])
        vertices.append([4+c[0], 4+c[1]])
        vertices.append([4+c[0], 0+c[1]])
        indices.append([0 + 4 *i, 1 + 4 *i, 2 + 4 *i])
        indices.append([0 + 4 *i, 2 + 4 *i, 3 + 4 *i])
        i+=1

    vertices = tuple(vertices)
    indices = tuple(indices)

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
def draw_cross(x, y, color, delta = 0):
    # vertices = (
    #     (0, 13), (0, 11), (24, 11),(24, 13),
    #     (11, 24),(11, 0), (13, 0), (14, 24)
    #     )
    # indices = (
    #     (0, 1, 2),(0, 2, 3),
    #     (4, 5, 6),(4, 6, 7)
    #     )
    # vertices = repositionning_3d(vertices, x, y)
    # shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    # batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    # shader.bind()
    # shader.uniform_float("color", color)
    # batch.draw(shader)

    coords=((0, 12), (24, 12), (12, 24), (12, 0))
    coords = repositionning_3d(coords, x, y)

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def draw_tris_batch(vertices, indices, color):
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_snap_grid(self, context):
    if self.snap_display != 'NOTHING':
        if self.snap_display == 'SPECIAL_POINTS':
            region = context.region
            rv3d = context.region_data
            if self.snap_refresh:
                self.snap_vert_coord_list=[]
                self.snap_calculated_coord_list=[]
                m = [0, 0, 0]

                # determine l'equation du plan
                if self.snap_support == 'OBJECT':
                    equation_du_plan = plan_equation(self.normal, self.cast['face_center_position'])
                    self.snap_vert_coord_list = self.cast['vertices']
                    if self.snap_extend:
                        self.snap_vert_coord_list = self.cast['vertices_coplanar']
                    else:
                        self.snap_vert_coord_list = self.cast['vertices']
                else:
                    matrix = self.drawing_tool_plan_obj.matrix_world.copy()
                    equation_du_plan = plan_equation(self.drawing_tool_plan_obj.data.polygons[0].normal, self.drawing_tool_plan_obj.data.polygons[0].center)
                    for v in self.drawing_tool_plan_obj.data.vertices:
                        self.snap_vert_coord_list.append(v.co)
                # trouve les coordonnees extremes
                if self.snap_support == 'OBJECT':
                    first_loop = True
                    for v in self.snap_vert_coord_list:
                        if first_loop:
                            x_max = v.x
                            y_max = v.y
                            z_max = v.z
                            x_min = v.x
                            y_min = v.y
                            z_min = v.z
                            first_loop = False
                        if v.x > x_max:
                            x_max = v.x
                        if v.y > y_max:
                            y_max = v.y
                        if v.z > z_max:
                            z_max = v.z
                        if v.x < x_min:
                            x_min = v.x
                        if v.y < y_min:
                            y_min = v.y
                        if v.z < z_min:
                            z_min = v.z
                elif self.snap_support == 'PLANE':
                    x_max = self.snap_zoom
                    y_max = self.snap_zoom
                    z_max = 0
                    x_min = -self.snap_zoom
                    y_min = -self.snap_zoom
                    z_min = 0
                else:
                    x_max = 2
                    y_max = 2
                    z_max = 0
                    x_min = -2
                    y_min = -2
                    z_min = 0

<<<<<<< HEAD
=======
                if 'x_max' not in vars():
                    x_max = 2
                    y_max = 2
                    z_max = 0
                    x_min = -2
                    y_min = -2
                    z_min = 0

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                # grille
                delta_x = (x_max - x_min)
                delta_y = (y_max - y_min)
                delta_z = (z_max - z_min)

                if self.snap_mode != 'DEFAULT':
                    delta_x = max([delta_x, delta_y, delta_z])
                    delta_y = max([delta_x, delta_y, delta_z])
                    delta_z = max([delta_x, delta_y, delta_z])

                out_of_grid = self.out_of_grid

                for x in range(self.snap_resolution + out_of_grid):
                    for y in range(self.snap_resolution +out_of_grid):
                        for z in range(self.snap_resolution +out_of_grid):
                # if snap plane close to XY YZ XZ plane, don't append to list
                            if round(delta_x,3) == 0:
                               xlen = 1
                            else:
                               xlen = self.snap_resolution + out_of_grid
                            if round (delta_y,3) == 0:
                               ylen = 1
                            else:
                               ylen = self.snap_resolution + out_of_grid
                            if round(delta_z,3) == 0:
                               zlen = 1
                            else:
                               zlen = self.snap_resolution + out_of_grid

                for x in range(xlen):
                    for y in range(ylen):
                        for z in range(zlen):
                            gx = delta_x/(self.snap_resolution-1) * (x) + (x_min - out_of_grid / 2 *delta_x/(self.snap_resolution-1))
                            gy = delta_y/(self.snap_resolution-1) * (y) + (y_min - out_of_grid / 2 *delta_y/(self.snap_resolution-1))
                            gz = delta_z/(self.snap_resolution-1) * (z) + (z_min - out_of_grid / 2 *delta_z/(self.snap_resolution-1))
                            grid_point = mathutils.Vector( (gx, gy, gz) )
                            if plan_equation(self.normal, grid_point, 'CHECK', equation_du_plan):
                                self.snap_calculated_coord_list.append(grid_point)
                self.snap_refresh = False

            vertices_WHITE = []
            indices_WHITE = []
<<<<<<< HEAD
=======
            black_dots = []
            blue_dot_list = []
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            for s in self.snap_calculated_coord_list:
                if self.snap_support == 'OBJECT':
                    co_3d = self.bool_target.matrix_world @ s
                else:
                    co_3d = self.drawing_tool_plan_obj.matrix_world @ s
                co_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d)
                try:
<<<<<<< HEAD
                    if math.fabs(self.mouse_x - co_2d.x) < 16 and math.fabs(self.mouse_y - co_2d.y) < 16:
                        draw_square_large(co_2d.x-4, co_2d.y-4, HIGHTLIGHT)
                        self.mouse_x = co_2d.x
                        self.mouse_y = co_2d.y
                    else:
                        draw_square(co_2d.x-2, co_2d.y-2, (0, 0, 0, 1))
                except:
                    pass

=======
                    black_dots.append([co_2d.x-2, co_2d.y-2])
                except:pass

                try:
                    if math.fabs(self.mouse_x - co_2d.x) < 16 and math.fabs(self.mouse_y - co_2d.y) < 16:
                        blue_dot_list.append([co_2d.x, co_2d.y])
                except:
                    pass

            draw_all_square(black_dots, (0, 0, 0, 1))
            try:
                limit = 32
                for d in blue_dot_list:
                    distance = math.sqrt(math.pow(d[0]-self.mouse_x, 2) + math.pow(d[1]-self.mouse_y, 2))
                    if distance <= limit:
                        limit = distance
                        blue_dot = [d[0], d[1]]

                draw_square_large(blue_dot[0]-4, blue_dot[1]-4, HIGHTLIGHT)
                self.mouse_x = blue_dot[0]
                self.mouse_y = blue_dot[1]
            except:pass

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if self.bool_target:
                try:
                    mwi = self.drawing_tool_plan_obj.matrix_world.inverted()
                    normal = self.drawing_tool_plan_obj.matrix_world.to_3x3() @ self.drawing_tool_plan_obj.data.polygons[0].normal
                    normal_x = normal.x/10000
                    normal_y = normal.y/10000
                    normal_z = normal.z/10000
                except:
                    pass
                # liste des snaps d'alignement possible
                snap_candidate = []
                if self.snap_support == 'OBJECT':
                    for s in self.snap_vert_coord_list:
                        co_3d = self.bool_target.matrix_world @ s
                        co_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d)
                        try:
                            if math.fabs(self.mouse_x - co_2d.x) < 16 and math.fabs(self.mouse_y - co_2d.y) < 16:
                                draw_square_large(co_2d.x-4, co_2d.y-4, HIGHTLIGHT)
                                self.mouse_x = co_2d.x
                                self.mouse_y = co_2d.y
                            else:
                                # draw_square(co_2d.x-2, co_2d.y-2, (1, 1, 1, 1))
                                _dx = co_2d.x-2
                                _dy = co_2d.y-2
                                l = len(vertices_WHITE)
                                vertices_WHITE += ((0+_dx, 0+_dy), (0+_dx, 4+_dy), (4+_dx, 4+_dy),(4+_dx, 0+_dy))
                                indices_WHITE += [(0+l, 1+l, 2+l),(0+l, 2+l, 3+l)]
                        except: pass

                        if self.snap_align :
                            # co_3d = self.bool_target.matrix_world @ s
                            local_pos = mwi @ co_3d
                            local_pos = mathutils.Vector((local_pos.x, local_pos.y, 0))
                            # coordonnees locales snapées
                            cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, 'LOCAL')
                            co_2d_local_x_snaped = mathutils.Vector((local_pos.x, cast['hit'].y, 0))
                            co_2d_local_y_snaped = mathutils.Vector((cast['hit'].x, local_pos.y, 0))
                            # coordonnees globales snapées
                            co_3d_x_snaped = self.drawing_tool_plan_obj.matrix_world @ co_2d_local_x_snaped
                            co_3d_y_snaped = self.drawing_tool_plan_obj.matrix_world @ co_2d_local_y_snaped
                            # projection à l'écran du point snapé
                            co_2d_screen_x_snaped = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d_x_snaped)
                            co_2d_screen_y_snaped = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d_y_snaped)

                            try:
                                if co_2d_screen_x_snaped.x - 8 <= self.mouse_x <= co_2d_screen_x_snaped.x + 8:
                                    snap_candidate.append([math.fabs(self.mouse_x - co_2d_screen_x_snaped.x) , co_3d, co_3d_x_snaped, co_2d_screen_x_snaped.x, 'X'])
                                elif co_2d_screen_y_snaped.y - 8 <= self.mouse_y <= co_2d_screen_y_snaped.y + 8:
                                    snap_candidate.append([math.fabs(self.mouse_y - co_2d_screen_y_snaped.y), co_3d, co_3d_y_snaped, co_2d_screen_y_snaped.y, 'Y'])
                            except:
                                pass
                            if len(snap_candidate):
                                d_min = [35]
                                for sc in snap_candidate:
                                    if sc[0] < d_min[0]:
                                        d_min = sc
                                # if d_min[4] == 'X':
                                #     self.mouse_x = d_min[3]
                                # else:
                                #     self.mouse_y = d_min[3]
                                draw_line([(d_min[1].x+normal_x, d_min[1].y+normal_y, d_min[1].z+normal_z), (d_min[2].x+normal_x, d_min[2].y+normal_y, d_min[2].z+normal_z)])


            # BLACK and HILIGHT points may cause process slow down, too
            # However, the most important thing to do is to lighten the drawing of WHITE points that can easily increase in number
            draw_tris_batch(tuple(vertices_WHITE), tuple(indices_WHITE), (1, 1, 1, 1))

            # dessin du plan
            try:
                normal = self.drawing_tool_plan_obj.matrix_world.to_3x3() @ self.drawing_tool_plan_obj.data.polygons[0].normal
                normal_x = normal.x/1000
                normal_y = normal.y/1000
                normal_z = normal.z/1000
                out_of_grid = self.out_of_grid
                a = self.snap_resolution + out_of_grid - 1
                alist = self.snap_calculated_coord_list
                if self.snap_support == 'OBJECT':
                    v_0 = self.bool_target.matrix_world @ alist[0]
                    v_1 = self.bool_target.matrix_world @ alist[a]
                    v_2 = self.bool_target.matrix_world @ alist[a*(a+2)]
                    v_3 = self.bool_target.matrix_world @ alist[a*(a+1)]
                else:
                    v_0 = self.drawing_tool_plan_obj.matrix_world @ alist[0]
                    v_1 = self.drawing_tool_plan_obj.matrix_world @ alist[a]
                    v_2 = self.drawing_tool_plan_obj.matrix_world @ alist[a*(a+2)]
                    v_3 = self.drawing_tool_plan_obj.matrix_world @ alist[a*(a+1)]

                coords = [(v_0.x, v_0.y, v_0.z),
                (v_1.x+normal_x, v_1.y+normal_y, v_1.z+normal_z),
                (v_2.x+normal_x, v_2.y+normal_y, v_2.z+normal_z),
                (v_3.x+normal_x, v_3.y+normal_y, v_3.z+normal_z)]

                indices = [(0, 1, 2), (0, 2, 3)]
                shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
                batch = batch_for_shader(shader, 'TRIS', {"pos": coords}, indices = indices)
                shader.bind()
                shader.uniform_float("color", (0.0, 0.643, 1, 0.25))
                bgl.glEnable(bgl.GL_BLEND)
                batch.draw(shader)
                bgl.glDisable(bgl.GL_BLEND)



            except:
                pass

            try:
                # marquage du centre du plan
                co_3d = self.drawing_tool_plan_obj.location
                co_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, co_3d)
                # draw_cross(co_2d.x-12, co_2d.y-12, (1, 0.349, 0, 1), delta = 0)
                draw_cross(co_2d.x-12, co_2d.y-12, (1, 1, 1, 1), delta = 0)
            except:
                pass

def draw_frist_bevel_icon(x, y, color):
    vertices = (
        (8, 24), (5, 21), (5, 4), (8, 0), (16, 0), (19, 4), (19, 21), (16, 24)
        )
    indices = (
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 6), (0, 6, 7)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_second_bevel_icon(x, y, color):
    vertices = (
        (0, 14), (0, 12), (5, 6), (19, 6), (24, 12), (24, 14), (19, 19), (5, 19),
        (1, 13), (6, 8), (18, 8), (23, 13), (18, 17), (6, 17),
        (3, 13), (7, 9), (17, 9), (21, 13), (17, 16), (7, 16)
        )
    indices = (
        (0, 1, 8), (1, 2, 9), (1, 9, 8), (2, 3, 10), (2, 10, 9), (3, 4, 11), (3, 11, 10), (4, 5, 11), (11, 5, 6), (11, 6, 12), (12, 6, 7), (12, 7, 13), (13, 7, 0), (13, 0, 8),
        (14, 15, 19), (19, 15, 16), (19, 16, 18), (18, 16, 17)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_first_solidify_icon(x, y, color):
    vertices = (
        (5, 8), (12, 0), (19, 8),
        (5, 16), (19, 16), (12, 24),
        (10, 8), (10, 16), (14, 16), (14, 8)
        )
    indices = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (6, 8, 9)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_second_solidify_icon(x, y, color):
    vertices = (
        (0, 24), (0, 0), (24, 0), (24, 24),
        (1, 23), (1, 1), (23, 1), (23, 23),
        (19, 19), (5, 19), (5, 5), (19, 5)
        )
    indices = (
        (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
        (8, 9, 10), (8, 10, 11)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_mirror_icon(x, y, color):
    vertices = (
        (13,24), (13, 0), (19, 0), (24, 6), (24, 18), (19, 24),
        (11, 24), (5, 24), (0, 18), (0, 6), (5, 0), (11, 0), (10, 23), (5, 23), (1, 18), (1, 6), (5, 1), (10, 1)
        )
    indices = (
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5),
        (6, 7, 13), (6, 13, 12), (7, 8, 14), (7, 14, 13), (8, 9, 15), (8, 15, 14), (9, 10, 16), (9, 16, 15), (10, 11, 17), (10, 17, 16), (11, 6, 12), (11, 12, 17)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_array_icon(x, y, color):
    vertices = (
        (5, 24), (0, 19), (0, 0), (5, 5),
        (11, 24), (6, 19), (6, 0), (11, 5),
        (17, 24), (12, 19), (12, 0), (17, 5),
        (23, 24), (18, 19), (18, 0), (23, 5)
        )
    indices = (
        (0, 1, 2),(0, 2, 3),
        (4, 5, 6), (4, 6, 7),
        (8, 9, 10), (8, 10, 11),
        (12, 13, 14), (12, 14, 15)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

<<<<<<< HEAD
def draw_circular_array_icon(x, y, color):
=======
def draw_Circular_Array_icon(x, y, color):
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    vertices = (
        (3, 14), (3, 10), (5, 10), (5, 14), (2, 13), (2, 11), (6, 11), (6, 13),
        (5, 8), (5, 4), (7, 4), (7, 8), (4, 7), (4, 5), (8, 5), (8, 7),
        (11, 6), (11, 2), (13, 2), (13, 6), (10, 5), (10, 3), (14, 3), (14, 5),
        (17, 8), (17,4), (19, 4), (19, 8), (16, 7), (16, 5), (20, 5), (20, 7),
        (19, 14), (19, 10), (21, 10), (21, 14), (18, 13), (18, 11), (22, 11), (22, 13),
        (17, 20), (17, 16), (19, 16), (19, 20), (16, 19), (16, 17), (20, 17), (20, 19),
        (11, 22), (11, 18), (13, 18), (13, 22), (10, 21), (10, 19), (14, 19), (14, 21),
        (5, 20), (5, 16), (7, 16), (7, 20), (4, 19), (4, 17), (8, 17), (8, 19)
        )
    indices = (
        (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
        (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15),
        (16, 17, 18), (16, 18, 19), (20, 21, 22), (20, 22, 23),
        (24, 25, 26), (24, 26, 27), (28, 29, 30), (28, 30, 31),
        (32, 33, 34), (32, 34, 35), (36, 37, 38), (36, 38, 39),
        (40, 41, 42), (40, 42, 43), (44, 45, 46), (44, 46, 47),
        (48, 49, 50), (48, 50, 51), (52, 53, 54), (52, 54, 55),
        (56, 57, 58), (56, 58, 59), (60, 61, 62), (60, 62, 63)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_symetrize_icon(x, y, color):
    vertices = (
        (10, 8), (0, 8), (0, 13), (3, 16), (10, 16), (13, 8), (13, 16), (20, 16), (23, 13), (23, 8), (12, 7), (12, 17), (11, 17), (11, 7)
        )
    indices = (
        (0, 1, 2), (0, 2, 3), (0, 3, 4),
        (5, 6, 7), (5, 7, 8), (5, 8, 9),
        (10, 11, 12), (10, 12, 13)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_radius_icon(x, y, color):
    vertices = (
        (0, 12), (8, 4), (8, 20),
        (16, 20), (16, 4), (24, 12),
        (8, 11), (8, 14), (16, 14), (16, 11)
        )
    indices = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (6, 9, 8)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_smooth_icon(x, y, color):
    vertices = (
        (0, 12), (3, 8),
        (3, 8), (5, 7),
        (5, 7), (7, 7),
        (7, 7), (9, 8),
        (9, 8), (15, 16),
        (15, 16), (17, 17),
        (17, 17), (19, 17),
        (19, 17), (21, 16),
        (21, 16), (24, 12)
        )
    vertices = repositionning(vertices, x, y)
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": vertices})
    shader.bind()
    shader.uniform_float("color", color)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def draw_resolution_icon(x, y, color):
    vertices = (
        (2, 18), (2, 6), (12, 0), (22, 6), (22, 18), (12, 24)
        )
    indices = (
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5)
        )
    vertices = repositionning(vertices, x, y)
    drawing_tris(vertices, indices, color)

def draw_item_hover(x, y, width, height):
    l = x + width
    h = y - height
    vertices = ((x, y), (l, y), (l, h), (x, h))
    indices = ((0, 1, 2),(0, 2, 3))
<<<<<<< HEAD
    color = ((1, 1, 1, 0.25), (1, 1, 1, 0) , (1, 1, 1,0 ), (1, 1, 1, 0.25))
=======
    color = ((0.4, 0.4, 0.4, 1), (0.4, 0.4, 0.4, 1) , (0.4, 0.4, 0.4, 1), (0.4, 0.4, 0.4, 1))
    # color = ((1, 1, 1, 0.25), (1, 1, 1, 0) , (1, 1, 1,0 ), (1, 1, 1, 0.25))
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    shader = gpu.shader.from_builtin('2D_SMOOTH_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices, "color": color}, indices=indices)
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def draw_block(x, y, width, height, color):
    l = x + width
    h = y - height
    vertices = ((x, y), (l, y), (l, h), (x, h))
    indices = ((0, 1, 2),(0, 2, 3))
    drawing_tris(vertices, indices, color)

def repositionning(vertices, x, y):
    # replace le dessin
    vertices_list = list(vertices)
    i = 0
    for v in vertices_list:
        coord = list(v)
        coord[0] = x + coord[0]
        coord[1] = y - coord[1]
        vertices_list[i] = tuple(coord)
        i += 1
    vertices = tuple(vertices_list)
    return vertices

def drawing_tris(vertices, indices, color):
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def draw_callback_px(self, context):
<<<<<<< HEAD
    text_x_origin = 5
    text_y_origin = 500
=======
    global HIGHTLIGHT
    HIGHTLIGHT = get_addon_preferences().hightlight
    text_x_origin = get_addon_preferences().text_x_origin
    text_y_origin = get_addon_preferences().text_y_origin
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    try:
        packed_strings = self.screen_text
    except:
        packed_strings = ''
<<<<<<< HEAD
    font_id = 0
    blf.size(font_id, 18, 72)
=======

    font_id = 0
    blf.size(font_id, get_addon_preferences().text_size, 72)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45)
    shader = None
    batch = None

    def text_dimensions(text):
        text_width, text_height = blf.dimensions(font_id, text)
        return{"width":text_width, "height": text_height}

    # Ecrire le texte ****************************************
<<<<<<< HEAD
=======
    # blf.enable(font_id, 4)
    # blf.shadow(font_id, 0, 0, 0, 0, 1)
    # blf.shadow_offset(font_id, 1, -1)
    max_width = 0
    if packed_strings:
        for command in packed_strings:
            if len(command) == 2:
                pstr, pcol = command
                color = list(pcol)
                blf.color(font_id, color[0], color[1], color[2], color[3])
                text_width, text_height = blf.dimensions(font_id, pstr)
                blf.position(font_id, (text_x_origin + x_offset), (text_y_origin + y_offset), 0)
                # blf.draw(font_id, pstr)
                x_offset += text_width
            else:
                if x_offset > max_width:
                    max_width = x_offset
                x_offset = 0
                y_offset -= line_height
    draw_block(text_x_origin-5, text_y_origin + line_height + 3, max_width +10, (y_offset - line_height) * (-1) + 10, (0, 0, 0, 0.25))
    x_offset = 0
    y_offset = 0
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    if packed_strings:
        for command in packed_strings:
            if len(command) == 2:
                pstr, pcol = command
                color = list(pcol)
                blf.color(font_id, color[0], color[1], color[2], color[3])
                text_width, text_height = blf.dimensions(font_id, pstr)
                blf.position(font_id, (text_x_origin + x_offset), (text_y_origin + y_offset), 0)
                blf.draw(font_id, pstr)
                x_offset += text_width
            else:
                x_offset = 0
                y_offset -= line_height
<<<<<<< HEAD
=======

    draw_snap_grid(self, context)

    try:
        if self.build_step in {0, 0.5, 1, 2}:
            matrix = self.bool_obj.matrix_world.copy()
            # vertices = get_verts(self.bool_obj)
            depth = bpy.context.evaluated_depsgraph_get()
            eobj = self.bool_obj.evaluated_get(depth)
            mesh = bpy.data.meshes.new_from_object(eobj)
            self.meshes_names_to_clean.append(mesh.name)
            vertices = [v.co for v in mesh.vertices]
            edges = mesh.edges
            coords = []
            for e in edges:
                v = vertices[e.vertices[0]]
                vv = vertices[e.vertices[1]]
                global_coord = matrix @ v
                global_coord_ = matrix @ vv
                coords.append((global_coord.x, global_coord.y, global_coord.z))
                coords.append((global_coord_.x, global_coord_.y, global_coord_.z))
            draw_line(coords)
    except:pass

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    # MENU ******************************
    try:
        nb_blocks = len(self.display_menu.get_blocks())
        angle_between_blocks = math.radians(360 / nb_blocks)
        pie_radius = 100
        item_height = 25
        block_width = 175
        padding = 6
        item_width = block_width - 2*padding

        block_count = 0
        self.display_menu.set_menu_hover(False)
        for b in self.display_menu.get_blocks():
            block_height = padding + len(self.display_menu.get_blocks()[b]['items']) * (item_height + padding)
            block_position_x = self.display_menu.get_position()['x']+math.cos(angle_between_blocks*block_count)*pie_radius - block_width/2
            block_position_y = self.display_menu.get_position()['y']+math.sin(angle_between_blocks*block_count)*pie_radius + block_height/2
<<<<<<< HEAD
            draw_block(block_position_x, block_position_y, block_width, block_height, (0, 0, 0, .5))
=======
            draw_block(block_position_x, block_position_y, block_width, block_height, (0, 0, 0, 0))
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            item_count = 0
            for i in self.display_menu.get_blocks()[b]['items']:
                item_position_x = block_position_x + padding
                item_position_y = block_position_y - padding - item_count * (item_height + padding)
                self.display_menu.get_blocks()[b]['items'][item_count]['position_x'] = item_position_x
                self.display_menu.get_blocks()[b]['items'][item_count]['position_y'] = item_position_y
                self.display_menu.get_blocks()[b]['items'][item_count]['width'] = item_width
                self.display_menu.get_blocks()[b]['items'][item_count]['height'] = item_height

                if self.display_menu.get_blocks()[b]['items'][item_count]['hover']:
                    self.display_menu.set_menu_hover(True)
<<<<<<< HEAD
                    draw_item_hover(item_position_x , item_position_y, item_width, item_height)
=======
                    draw_item_hover(item_position_x-5, item_position_y+5, item_width+10, item_height+10)
                else:
                    draw_block(item_position_x-5, item_position_y+5, item_width+10, item_height+10, (0.35, 0.35, 0.35, 1))
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

                if self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'FIRST_BEVEL':
                    if self.bool_obj.modifiers['First_Bevel'].show_render:
                        draw_frist_bevel_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_frist_bevel_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'SECOND_BEVEL':
                    if self.bool_obj.modifiers['Second_Bevel'].show_render:
                        draw_second_bevel_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_second_bevel_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'FIRST_SOLIDIFY':
                    if self.bool_obj.modifiers['First_Solidify'].show_render:
                        draw_first_solidify_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_first_solidify_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'SECOND_SOLIDIFY':
                    if self.bool_obj.modifiers['Second_Solidify'].show_render:
                        draw_second_solidify_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_second_solidify_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'MIRROR':
                    if self.bool_obj.modifiers['Mirror'].show_render:
                        draw_mirror_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_mirror_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'ARRAY':
                    if self.bool_obj.modifiers['ArrayX'].show_render or self.bool_obj.modifiers['ArrayY'].show_render or self.bool_obj.modifiers['ArrayZ'].show_render:
                        draw_array_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_array_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'CIRCULAR_ARRAY':
<<<<<<< HEAD
                    has_circular_array = False
                    for m in self.bool_obj.modifiers:
                        if m.name == 'circular_displace' and m.show_render:
                            has_circular_array = True
                    if has_circular_array:
                        draw_circular_array_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_circular_array_icon(round(item_position_x), round(item_position_y), WHITE)
=======
                    has_Circular_Array = False
                    for m in self.bool_obj.modifiers:
                        if m.name == 'Circular_Displace' and m.show_render:
                            has_Circular_Array = True
                    if has_Circular_Array:
                        draw_Circular_Array_icon(round(item_position_x), round(item_position_y), HIGHTLIGHT)
                    else:
                        draw_Circular_Array_icon(round(item_position_x), round(item_position_y), WHITE)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'SYMETRIZE':
                    draw_symetrize_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'SMOOTH':
                    draw_smooth_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'RADIUS':
                    draw_radius_icon(round(item_position_x), round(item_position_y), WHITE)

                elif self.display_menu.get_blocks()[b]['items'][item_count]['icon'] == 'RESOLUTION':
                    draw_resolution_icon(round(item_position_x), round(item_position_y), WHITE)

                blf.size(font_id, 16, 72)
                blf.color(font_id, 1, 1, 1, 1)
                text_width, text_height = blf.dimensions(font_id, self.display_menu.get_blocks()[b]['items'][item_count]['text'])
                if self.display_menu.get_blocks()[b]['items'][item_count]['icon']:
                    blf.position(font_id, item_position_x + ico_size + 2*padding, item_position_y - math.fabs(item_height - text_height)/2 - text_height, 0)
                else:
                    blf.position(font_id, item_position_x + 2*padding, item_position_y - math.fabs(item_height - text_height)/2 - text_height, 0)
                blf.draw(font_id, self.display_menu.get_blocks()[b]['items'][item_count]['text'])
                item_count+=1
            block_count+=1
    except:pass

<<<<<<< HEAD
    draw_snap_grid(self, context)

=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    context.area.tag_redraw()

def make_oops(msg):
    global CR
    def oops(self, context):
        for m in msg:
            self.layout.label(text=m)
    return oops

def plan_equation(n = 0, v = 0, do = 'CALCUL', eq = [0, 0, 0, 0]):
    # n est le vecteur normal au plan, v un point du plan
    if do == 'CALCUL':
        equation_coef = [0, 0, 0, 0]
        equation_coef[0] = n.x
        equation_coef[1] = n.y
        equation_coef[2] = n.z
        equation_coef[3] = (-1) * n.x * v.x - n.y * v.y - n.z * v.z
        return equation_coef
    elif do == 'CHECK':
        if round(eq[0] * v.x + eq[1] * v.y + eq[2] * v.z + eq[3], 3) == 0:
            return True
        else:
            return False

def has_modifier(obj, type, attr = ''):
    obj_has_modifier = False
    position = None
    for i in range(len(obj.modifiers)):
        if obj.modifiers[i].type == type:
            if attr:
                if getattr(obj.modifiers[i], attr):
                    obj_has_modifier = True
                    position = i
            else:
                obj_has_modifier = True
                position = i

    return obj_has_modifier, position

def active_object(obj = None, action = 'GET'):
    if action == 'SET':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        return obj
    elif action == 'GET':
        return bpy.context.active_object

def weighted_normals_manager(obj, action):
    if obj.hide_viewport:
        obj.hide_viewport = False
        hidden = True
    else:
        hidden = False
    old_active_obj = bpy.context.active_object
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    old_active_obj.select_set(False)
    has_weighted_normals = False


    if action == 'ADD':
        modif = obj.modifiers.new(name='Weighted Normal', type='WEIGHTED_NORMAL')
        modif.show_expanded = False
        bpy.context.object.data.use_auto_smooth = True
    elif action == 'REPLACE':
        for modif in obj.modifiers:
            if modif.type == 'WEIGHTED_NORMAL':
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                break
    elif action == 'REMOVE':
        for modif in obj.modifiers:
            if modif.type == 'WEIGHTED_NORMAL':
                obj.modifiers.remove(modif)
                bpy.ops.object.shade_flat()
                break
    elif action == 'CHECK':
        try:
            for modif in obj.modifiers:
                if modif.type == 'WEIGHTED_NORMAL':
                    has_weighted_normals = True
        except:
            pass

    if hidden:
        obj.hide_viewport = True

    obj.select_set(False)
    old_active_obj.select_set(True)
    bpy.context.view_layer.objects.active = old_active_obj
    return has_weighted_normals

def latest_bevel_manager(obj, action):
    if obj.hide_viewport:
        obj.hide_viewport = False
        hidden = True
    else:
        hidden = False
    has_latest_bevel = False
    old_active_obj = bpy.context.active_object
    if old_active_obj:
        old_active_obj.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    modif = None

    if action == 'REPLACE':
        if len(obj.modifiers) >= 2:
            modif = obj.modifiers[len(obj.modifiers)-2]
            modif_two = obj.modifiers[len(obj.modifiers)-3]
            if modif.type == 'BEVEL' and modif.limit_method == 'ANGLE' and modif.width <= 0.02 + 0.001 and modif.segments > 1:
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
                bpy.ops.object.modifier_move_down(modifier=modif.name)
            elif modif_two.type == 'BEVEL' and modif_two.limit_method == 'ANGLE' and modif_two.width <= 0.02 + 0.001 and modif_two.segments > 1:
                bpy.ops.object.modifier_move_down(modifier=modif_two.name)
                bpy.ops.object.modifier_move_down(modifier=modif_two.name)
                bpy.ops.object.modifier_move_down(modifier=modif_two.name)
                bpy.ops.object.modifier_move_down(modifier=modif_two.name)
    elif action == 'CHECK':
        try:
            if len(obj.modifiers) >= 1:
                modif = obj.modifiers[len(obj.modifiers)-1]
                if modif.type == 'BEVEL' and modif.limit_method == 'ANGLE' and modif.width <= 0.02 + 0.001:
                    has_latest_bevel = True
            if len(obj.modifiers) >= 2:
                modif_two = obj.modifiers[len(obj.modifiers)-2]
                if modif_two.type == 'BEVEL' and modif_two.limit_method == 'ANGLE' and modif_two.width <= 0.02 + 0.001:
                    has_latest_bevel = True
            if len(obj.modifiers) >= 3:
                modif_three = obj.modifiers[len(obj.modifiers)-3]
                if modif_three.type == 'BEVEL' and modif_three.limit_method == 'ANGLE' and modif_three.width <= 0.02 + 0.001:
                    has_latest_bevel = True
        except:
            pass
    elif action == 'REMOVE':
        obj.modifiers.remove(obj.modifiers[len(obj.modifiers)-1])
        bpy.ops.object.shade_flat()
    elif action == 'ADD':
        modif = obj.modifiers.new(name='latestBevel', type='BEVEL')
        modif.limit_method = 'ANGLE'
        modif.angle_limit = 0.523599
<<<<<<< HEAD
        modif.segments = 6
=======
        modif.segments = bpy.context.scene.fluentProp.latest_bevel_segments
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        modif.width = bpy.context.scene.fluentProp.width
        modif.miter_outer = 'MITER_ARC'
        modif.use_clamp_overlap = False
        modif.harden_normals = True
        modif.show_expanded = False
        bpy.ops.object.shade_smooth()
        obj['fluent_object'] = True

    if hidden:
        obj.hide_viewport = True

    obj.select_set(False)
    if old_active_obj:
        old_active_obj.select_set(True)
        bpy.context.view_layer.objects.active = old_active_obj

    return has_latest_bevel

def rotation_cartesian(x, y):
    return [y*1, x*(-1)]

def empty_manager(obj):
    had_empty = None
    for o in bpy.data.objects:
        if o.type == 'EMPTY':
            if obj == None:
                if bpy.context.scene.cursor.location.x - 0.01 <= o.location.x <= bpy.context.scene.cursor.location.x + 0.01 and bpy.context.scene.cursor.location.y - 0.01 <= o.location.y <= bpy.context.scene.cursor.location.y + 0.01 and bpy.context.scene.cursor.location.z - 0.01 <= o.location.z <= bpy.context.scene.cursor.location.z + 0.01:
                    had_empty = True
                    empty = o
            else:
                if obj.location.x - 0.01 <= o.location.x <= obj.location.x + 0.01 and obj.location.y - 0.01 <= o.location.y <= obj.location.y + 0.01 and obj.location.z - 0.01 <= o.location.z <= obj.location.z + 0.01:
                    had_empty = True
                    empty = o
                    break
    if not had_empty:
        bpy.ops.object.add(type='EMPTY')
        empty = bpy.context.active_object
        empty.empty_display_size = 0.1
        # parente l'original avec le bool
        empty.select_set(False)

    return empty

def duplicate_obj(obj, apply = True, location = True, rotation = True, scale = True):
    if weighted_normals_manager(obj, 'CHECK'):
        had_weighted_normals = True
        weighted_normals_manager(obj, 'REMOVE')
    else:
        had_weighted_normals = False
    if latest_bevel_manager(obj, 'CHECK'):
        had_latest_bevel = True
        latest_bevel_manager(obj, 'REMOVE')
    else:
        had_latest_bevel = False

    depth = bpy.context.evaluated_depsgraph_get()
    eobj = obj.evaluated_get(depth)
    mesh = bpy.data.meshes.new_from_object(eobj)
    name = obj.name + "_duplicate"
    copy = bpy.data.objects.new(name, mesh)
    copy.data = mesh
    bpy.context.collection.objects.link(copy)

    copy.location = obj.location
    copy.rotation_euler = obj.rotation_euler
    copy.dimensions = obj.dimensions
    if obj.show_wire == True:
        copy.show_wire = True
        copy.show_all_edges = True
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    obj.select_set(False)
    active_object(copy, 'SET')
    try:
        bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    except:
        pass

    return copy, had_latest_bevel, had_weighted_normals

def obj_ray_cast(context, mouse_x, mouse_y, obj, reference = 'LOCAL', duplicate = False):
    # creer une copie en appliquant les modifiers
    if obj.name != 'drawing_tool_plan_obj':
        if duplicate:
            copy, had_latest_bevel, had_weighted_normals = duplicate_obj(obj)
            working_obj = copy
            if had_latest_bevel:
                latest_bevel_manager(obj, 'ADD')
        else:
            working_obj = obj
    else:
        working_obj = obj

    working_obj_polygons = working_obj.data.polygons

    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = mouse_x, mouse_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + view_vector

    matrix = working_obj.matrix_world.copy()
    # get the ray relative to the object
    matrix_inv = matrix.inverted()
    ray_origin_obj = matrix_inv @ ray_origin
    ray_target_obj = matrix_inv @ ray_target
    ray_direction_obj = ray_target_obj - ray_origin_obj

    # cast the ray
    success, location, normal, face_index = working_obj.ray_cast(ray_origin_obj, ray_direction_obj)

    vert_list = []
    vert_coplanar_list = []
    if success:
        # liste des vertices de la face (on enregistre les coordonnées)
        for v in working_obj_polygons[face_index].vertices:
            vert = working_obj.data.vertices[v]
            if reference == 'WORLD':
                co_world = matrix @ vert.co
                vert_list.append(co_world)
            elif reference == 'LOCAL':
                vert_list.append(vert.co)
        # liste des vertices coplanaires
        normal_world = matrix.to_3x3() @ normal
        equation_du_plan = plan_equation(normal_world, matrix @ working_obj_polygons[face_index].center)
        for v in working_obj.data.vertices:
            if plan_equation(normal_world, v.co, 'CHECK', equation_du_plan):
                if reference == 'WORLD':
                    co_world = matrix @ v.co
                    vert_coplanar_list.append(co_world)
                elif reference == 'LOCAL':
                    vert_coplanar_list.append(v.co)

    try:
        bpy.data.objects.remove(copy, do_unlink=True)
    except:
        pass

    if reference == 'LOCAL':
        return {'success' : success, 'hit' : location, 'normal' : normal, 'face_index' : face_index, 'ray_origin' : ray_origin, 'face_center_position': working_obj_polygons[face_index].center, 'vertices': vert_list, 'vertices_coplanar': vert_coplanar_list}
    elif reference == 'WORLD':
        return {'success' : success, 'hit' : matrix @ location, 'normal' : matrix.to_3x3() @ normal, 'face_index' : face_index, 'ray_origin' : ray_origin, 'face_center_position': matrix @ working_obj_polygons[face_index].center, 'vertices': vert_list, 'vertices_coplanar': vert_coplanar_list}

def click_on(context, mouse_x, mouse_y, ignore = False):
    # cast rays and find the closest object
    best_length_squared = -1.0
    best_obj = None

    for obj in context.visible_objects:
        if obj.type == 'MESH' and not obj.hide_viewport and obj != ignore:
            matrix = obj.matrix_world.copy()
            try:
                result = obj_ray_cast(context, mouse_x, mouse_y, obj)
            except:
                result = {'success' : False}

            if result.get('success'):
                hit_world = matrix @ result.get('hit')
                normal_world = matrix.to_3x3() @ result.get('normal')
                length_squared = (hit_world - result.get('ray_origin')).length_squared
                if best_obj is None or length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj

    # now we have the object under the mouse cursor,
    # we could do lots of stuff but for the example just select.
    if best_obj is not None:
        final_result = obj_ray_cast(context, mouse_x, mouse_y, best_obj)
        final_result['hit'] = hit_world
        final_result['obj'] = best_obj
        final_result['normal'] = normal_world
        return final_result
    else:
        return {'success':False}

def rotate_plane(obj):
    obj.rotation_mode='XYZ'
    save_matrix = obj.matrix_world.copy()
    limite = 37
    out_of_limit = False
    if round(obj.rotation_euler.x,3) != round(obj.rotation_euler.y,3):
        if math.fabs(obj.rotation_euler.x) < math.fabs(obj.rotation_euler.y):
            ################################################################################
            i = 0
            rotate_direction = 1
            while not(math.radians(-10) <= round(obj.rotation_euler.x,5) <= math.radians(10)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.x,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(5 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.x) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-1) <= round(obj.rotation_euler.x,5) <= math.radians(1)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.x,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.5 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.x) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-0.1) <= round(obj.rotation_euler.x,5) <= math.radians(0.1)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.x,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.05 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.x) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-0.01) <= round(obj.rotation_euler.x,5) <= math.radians(0.01)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.x,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.005 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.x) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            if i == limite :
                out_of_limit = True
        else:
            ################################################################################
            i = 0
            rotate_direction = 1
            while not(math.radians(-10) <= round(obj.rotation_euler.y,5) <= math.radians(10)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.y,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(5 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.y) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-1) <= round(obj.rotation_euler.y,5) <= math.radians(1)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.y,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.5 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.y) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-0.1) <= round(obj.rotation_euler.y,5) <= math.radians(0.1)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.y,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.05 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.y) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            ################################################################################
            if i == limite :
                out_of_limit = True
            i = 0
            rotate_direction = 1
            while not(math.radians(-0.01) <= round(obj.rotation_euler.y,5) <= math.radians(0.01)) and i != limite:
                i += 1
                previous_rotation = round(obj.rotation_euler.y,5)
                obj.matrix_world @= Matrix.Rotation(math.radians(0.005 * rotate_direction), 4, 'Z')
                if math.fabs(obj.rotation_euler.y) > math.fabs(previous_rotation) and i==1:
                    rotate_direction *= -1
            if i == limite :
                out_of_limit = True
        if out_of_limit:
            obj.matrix_world = save_matrix

def cycles_visibility(stat):
    bpy.context.object.cycles_visibility.camera = stat
    bpy.context.object.cycles_visibility.glossy = stat
    bpy.context.object.cycles_visibility.scatter = stat
    bpy.context.object.cycles_visibility.shadow = stat
    bpy.context.object.cycles_visibility.transmission = stat
    bpy.context.object.cycles_visibility.diffuse = stat

def local_rotate(obj, axis, angle):
    obj.matrix_world @= Matrix.Rotation(math.radians(angle), 4, axis)

def smooth_manager(obj, action, value = 5):
    old_active = active_object('GET')
    active_object(obj, 'SET')
    if action == 'ADD':
        modif = obj.modifiers.new(name='Triangulate', type='TRIANGULATE')
        modif.min_vertices = 4
        modif.ngon_method = 'BEAUTY'
        modif.quad_method = 'SHORTEST_DIAGONAL'
        modif.show_expanded = False
        # modif.show_in_editmode = False
        for i in range(20):
            bpy.ops.object.modifier_move_up(modifier="Triangulate")
        bpy.ops.object.modifier_move_down(modifier="Triangulate")
        modif = obj.modifiers.new(name='Subdivision', type='SUBSURF')
        modif.quality = 6
        modif.levels = 3
        modif.render_levels = 3
        modif.show_expanded = False
        for i in range(20):
            bpy.ops.object.modifier_move_up(modifier="Subdivision")
        bpy.ops.object.modifier_move_down(modifier="Subdivision")
        bpy.ops.object.modifier_move_down(modifier="Subdivision")
        modif = obj.modifiers.new(name='Decimate', type='DECIMATE')
        modif.decimate_type = 'DISSOLVE'
        modif.angle_limit = 0.00174533
        modif.show_expanded = False
        for i in range(20):
            bpy.ops.object.modifier_move_up(modifier="Decimate")
        bpy.ops.object.modifier_move_down(modifier="Decimate")
        bpy.ops.object.modifier_move_down(modifier="Decimate")
        bpy.ops.object.modifier_move_down(modifier="Decimate")

    elif action == 'REMOVE':
        for m in obj.modifiers:
            if m.type == 'TRIANGULATE' or m.type == 'SUBSURF':
                obj.modifiers.remove(m)
    elif action == 'CHECK':
        for i in range(len(obj.modifiers)):
            if i == 1 and obj.modifiers[i].type == 'TRIANGULATE' and obj.modifiers[i+1].type == 'SUBSURF':
                return True
        return False

    active_object(old_active, 'SET')

def preset_manager(action = 'GET', obj = None):
    if action == 'GET' and obj:
        try:
            bpy.context.scene.fluentProp.depth = obj.modifiers['First_Solidify'].thickness
            bpy.context.scene.fluentProp.solidify_offset = obj.modifiers['First_Solidify'].offset
        except:pass
        try:
            bpy.context.scene.fluentProp.corner = obj.modifiers['First_Bevel'].width
            if obj.modifiers['First_Bevel'].segments == 1:
                bpy.context.scene.fluentProp.straight_bevel = True
            else:
                bpy.context.scene.fluentProp.straight_bevel = False
        except:pass
        try:
            bpy.context.scene.fluentProp.second_bevel_width = obj.modifiers['Second_Bevel'].width
            if obj.modifiers['Second_Bevel'].segments == 1:
                bpy.context.scene.fluentProp.second_bevel_straight = True
            else:
                bpy.context.scene.fluentProp.second_bevel_straight = False
        except:pass
    elif action == 'RESET':
        bpy.context.scene.fluentProp.depth = 0
        bpy.context.scene.fluentProp.solidify_offset = 0
        bpy.context.scene.fluentProp.corner = 0
        bpy.context.scene.fluentProp.second_bevel_width = 0
        bpy.context.scene.fluentProp.straight_bevel = False
        bpy.context.scene.fluentProp.second_bevel_straight = False

<<<<<<< HEAD
=======
def enter_value_validation(value, event):
    if event.value == 'PRESS' and event.type in {'NUMPAD_ENTER', 'RET'}:
        return [True, float(value)]
    else:
        return [False]

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
class F_Menu():

    def __init__(self, mouse_x, mouse_y):
        self.menu = []
        self.blocks = {}
        self.menu_position = {'x':mouse_x, 'y':mouse_y}
        self.visibility = True
        self.menu_hover = False

    def get_position(self):
        return self.menu_position

    def set_position(self, x, y):
        self.menu_position = {'x':x, 'y':y}

    def set_menu_hover(self, a):
        self.menu_hover = a

    def get_menu_hover(self):
        return self.menu_hover

    def get_blocks(self):
        return self.blocks

    def add_block(self, name):
        new_block = {'position': [0, 0], 'items' : []}
        self.menu.append(name)
        self.blocks[name] = new_block

    def add_item(self, target_block, command, text, type, icon = None, hover = False):
        new_item = {'text' : text, 'command':command, 'position_x':0, 'position_y':0, 'width':0, 'height':0, 'hover':hover, 'type': type, 'icon': icon}
        self.blocks[target_block]['items'].append(new_item)

    def hover(self, mouse_x, mouse_y):
        for b in self.blocks:
            bb = self.blocks[b]
            for i in bb['items']:
<<<<<<< HEAD
                if i['type'] in {'BUTTON', 'SLIDER'}:
=======
                if i['type'] in {'BUTTON', 'SLIDER', 'LABEL'}:
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                    if i['position_x'] < mouse_x < i['position_x']+i['width'] and i['position_y'] - i['height']< mouse_y < i['position_y']  :
                        i['hover'] = True
                    else:
                        i['hover'] = False

    def action(self):
        for b in self.blocks:
            bb = self.blocks[b]
            for i in bb['items']:
                if i['hover']:
                    return i['command']
                    break

class PolyDraw(bpy.types.Operator):
    bl_idname = "wm.polydraw"
    bl_label="Drawing Shape"
    bl_options = {'REGISTER', 'UNDO'}

    def snap(self, ox, oy, x, y, only = None):
        if not only:
            delta_x = math.fabs(ox - x)
            delta_y = math.fabs(oy - y)

            if delta_y != 0:
                snap = delta_x / delta_y
            else:
                snap = 2

            if snap < 0.25:
                x = ox
            elif snap > 1.75:
                y = oy
            else:
                a = x - ox + oy
                b = -(x - ox) + oy
                if math.fabs(a-y) < math.fabs(b-y):
                    y = a
                else:
                    y = b
        elif only == '45':
            a = x - ox + oy
            b = -(x - ox) + oy
            if math.fabs(a-y) < math.fabs(b-y):
                y = a
            else:
                y = b


        snap_coord = [x, y]
        return snap_coord

    def snap_grid(self, context, event):
        self.snap_display = 'SPECIAL_POINTS'
        if self.mesh_maker_call and not self.bool_target:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
        else:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
        if self.cast['success']:
            self.snap_refresh = True
        else:
            self.snap_display = 'NOTHING'

    def get_view_orientation_from_matrix(self, view_matrix):
        r = lambda x: round(x, 2)
        view_rot = view_matrix.to_euler()

        orientation_dict = {(0.0, 0.0, 0.0) : 'TOP',
                            (r(math.pi), 0.0, 0.0) : 'BOTTOM',
                            (r(-math.pi/2), 0.0, 0.0) : 'FRONT',
                            (r(math.pi/2), 0.0, r(-math.pi)) : 'BACK',
                            (r(-math.pi/2), r(math.pi/2), 0.0) : 'LEFT',
                            (r(-math.pi/2), r(-math.pi/2), 0.0) : 'RIGHT'}

        return orientation_dict.get(tuple(map(r, view_rot)), 'UNDEFINED')

    def update_display(self):

<<<<<<< HEAD
        self.screen_text = [("Fluent Making Tool", WHITE)]
=======
        def adjustment_value(modifier):
            if self.enter_value == 'None':
                return str(round(modifier, 3))
            else:
                return self.enter_value

        self.screen_text = [("FLUENT TOOLS", WHITE)]
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

        if self.build_step in {1, 2, 0.5}:
            self.screen_text.extend([CR, CR, ('SHAPE', WHITE)])
            if self.draw_type == 'box':
                self.screen_text.extend([CR, ('    Rectangle : R', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Shape : S', WHITE)])
                self.screen_text.extend([CR, ('    Circle : C', WHITE)])
            elif self.draw_type == 'poly':
                self.screen_text.extend([CR, ('    Rectangle : R', WHITE)])
                self.screen_text.extend([CR, ('    Shape : S', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Circle : C', WHITE)])
            elif self.draw_type == 'prism':
                self.screen_text.extend([CR, ('    Rectangle : R', WHITE)])
                self.screen_text.extend([CR, ('    Shape : S', WHITE)])
                self.screen_text.extend([CR, ('    Circle : C', HIGHTLIGHT)])

        if not self.mesh_maker_call and self.build_step in {2, 3} and not self.adjustment:
            self.screen_text.extend([CR, CR, ('BOOLEAN OPERATION', WHITE)])
            if self.bool_operation == 'DIFFERENCE':
                self.screen_text.extend([CR, ('    Difference : S', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Union : D', WHITE)])
                self.screen_text.extend([CR, ('    Intersect : F', WHITE)])
            elif self.bool_operation == 'UNION':
                self.screen_text.extend([CR, ('    Difference : S', WHITE)])
                self.screen_text.extend([CR, ('    Union : D', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Intersect : F', WHITE)])
            elif self.bool_operation == 'INTERSECT':
                self.screen_text.extend([CR, ('    Difference : S', WHITE)])
                self.screen_text.extend([CR, ('    Union : D', WHITE)])
                self.screen_text.extend([CR, ('    Intersect : F', HIGHTLIGHT)])

        if self.adjustment:
            if self.adjustment in {'FIRST_BEVEL','SECOND_BEVEL'}:
<<<<<<< HEAD
                self.screen_text.extend([CR, CR, ('BEVEL ADJUSTEMENT', HIGHTLIGHT)])
=======
                if self.adjustment == 'FIRST_BEVEL':
                    self.screen_text.extend([CR, CR, ('BEVEL ADJUSTMENT ' + adjustment_value(self.bool_obj.modifiers['First_Bevel'].width), HIGHTLIGHT)])
                else:
                    self.screen_text.extend([CR, CR, ('BEVEL ADJUSTMENT ' + str(round(self.bool_obj.modifiers['Second_Bevel'].width, 3)), HIGHTLIGHT)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('roundStraight'))+' : C', WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fastSlow')+' : Ctrl / Shift'), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('remove') + ' : Del'), WHITE)])
            elif self.adjustment == 'FIRST_SOLIDIFY':
<<<<<<< HEAD
                self.screen_text.extend([CR, CR, ('SOLIDIFY ADJUSTEMENT', HIGHTLIGHT)])
                if self.draw_type != 'path':
=======
                if self.draw_type != 'path':
                    self.screen_text.extend([CR, CR, ('SOLIDIFY ADJUSTMENT ' + adjustment_value(self.bool_obj.modifiers['First_Solidify'].thickness), HIGHTLIGHT)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fastSlow')+' : Ctrl / Shift'), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('thicknessOffset')+' : C'), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('crossModel')+' : V'), WHITE)])
                else:
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fastSlow')+' : Ctrl / Shift'), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fakeSlice')+' : C'), WHITE)])
                    self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('crossModel')+' : V'), WHITE)])
            elif self.adjustment == 'SECOND_SOLIDIFY':
<<<<<<< HEAD
                self.screen_text.extend([CR, CR, ('SECOND SOLIDIFY ADJUSTEMENT', HIGHTLIGHT)])
=======
                self.screen_text.extend([CR, CR, ('SECOND SOLIDIFY ADJUSTMENT ' + adjustment_value(self.bool_obj.modifiers['Second_Solidify'].thickness), HIGHTLIGHT)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fastSlow')+' : Ctrl / Shift'), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fakeSlice')+' : C'), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('remove') + ' : Del'), WHITE)])
            elif self.adjustment == 'RESOLUTION':
<<<<<<< HEAD
                self.screen_text.extend([CR, CR, ('RESOLUTION ADJUSTEMENT', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('steps'))+' : ', WHITE), (str(self.bool_obj.modifiers['Screw'].steps), HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Smooth cercle : C', WHITE)])
=======
                self.screen_text.extend([CR, CR, ('RESOLUTION ADJUSTMENT', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('steps'))+' : ', WHITE), (str(self.bool_obj.modifiers['Screw'].steps), HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Smooth cercle : C', WHITE)])
            elif self.adjustment == 'RADIUS':
                self.screen_text.extend([CR, CR, ('RADIUS ADJUSTMENT ' + adjustment_value(self.bool_obj.modifiers['Radius'].strength), HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('horizontalMouseMove')), WHITE)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            elif self.adjustment == 'MIRROR':
                self.screen_text.extend([CR, CR, ('Mirror', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    Mirror 1 : ', WHITE)])
                if self.bool_obj.modifiers['Mirror'].use_axis[0]:
                    self.screen_text.extend([('X', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('X', WHITE)])
                self.screen_text.extend([(' / ', WHITE)])
                if self.bool_obj.modifiers['Mirror'].use_axis[1]:
                    self.screen_text.extend([('Y', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('Y', WHITE)])
                self.screen_text.extend([(' / ', WHITE)])
                if self.bool_obj.modifiers['Mirror'].use_axis[2]:
                    self.screen_text.extend([('Z', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('Z', WHITE)])
                self.screen_text.extend([CR, ('    Mirror 2 (use Shift + axis) : ', WHITE)])
                if self.bool_obj.modifiers['Second_Mirror'].use_axis[0]:
                    self.screen_text.extend([(' X', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('X', WHITE)])
                self.screen_text.extend([(' / ', WHITE)])
                if self.bool_obj.modifiers['Second_Mirror'].use_axis[1]:
                    self.screen_text.extend([('Y', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('Y', WHITE)])
                self.screen_text.extend([(' / ', WHITE)])
                if self.bool_obj.modifiers['Second_Mirror'].use_axis[2]:
                    self.screen_text.extend([('Z', HIGHTLIGHT)])
                else:
                    self.screen_text.extend([('Z', WHITE)])
                self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('pressAxis')), WHITE)])
            elif self.adjustment == 'ARRAY':
                    self.screen_text.extend([CR, CR, ('ARRAY', HIGHTLIGHT)])
                    if self.array_axis == 'X':
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('axisSelection')), WHITE),(' X ', HIGHTLIGHT),('// Y // Z', WHITE)])
                    elif self.array_axis == 'Y':
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('axisSelection')), WHITE),(' X // ', WHITE),('Y ', HIGHTLIGHT),('// Z', WHITE)])
                    elif self.array_axis == 'Z':
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('axisSelection')), WHITE),(' X // Y // ', WHITE),('Z', HIGHTLIGHT)])
                    else:
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('axisSelection'))+' : X // Y // Z', WHITE)])
                    self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('pressAxis')), WHITE)])
                    if self.other_adjustement == 'OFFSET':
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('offset')), HIGHTLIGHT),(' : S', WHITE)])
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('count')), WHITE),(' : D ', WHITE)])
                    else:
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('offset')), WHITE),(' : S', WHITE)])
                        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('count')), HIGHTLIGHT),(' : D ', WHITE)])
                    self.screen_text.extend([CR,('        X : ', WHITE)])
                    if self.bool_obj.modifiers['ArrayX'].show_render:
                        self.screen_text.extend([(str(self.bool_obj.modifiers['ArrayX'].count), HIGHTLIGHT)])
                    else:
                        self.screen_text.extend([('0', WHITE)])
                    self.screen_text.extend([(' / Y : ', WHITE)])
                    if self.bool_obj.modifiers['ArrayY'].show_render:
                        self.screen_text.extend([(str(self.bool_obj.modifiers['ArrayY'].count), HIGHTLIGHT)])
                    else:
                        self.screen_text.extend([('0', WHITE)])
                    self.screen_text.extend([(' / Z : ', WHITE)])
                    if self.bool_obj.modifiers['ArrayZ'].show_render:
                        self.screen_text.extend([(str(self.bool_obj.modifiers['ArrayZ'].count), HIGHTLIGHT)])
                    else:
                        self.screen_text.extend([('0', WHITE)])
                    if not self.other_adjustement:
                        self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('fastSlow')), WHITE)])
            elif self.adjustment == 'CIRCULAR_ARRAY':
                self.screen_text.extend([CR, CR, ('CIRCULAR ARRAY', HIGHTLIGHT)])
                if not self.other_adjustement:
                    self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('radius')), HIGHTLIGHT),(' / '+str(translate.get(get_addon_preferences().language).get('number')) + ' : C', WHITE)])
                else:
                    self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('radius')) + ' / ', WHITE),(str(translate.get(get_addon_preferences().language).get('number')), HIGHTLIGHT), (' : C', WHITE)])
<<<<<<< HEAD
                if any([m for m in self.bool_obj.modifiers if m.name == "circular_array"]):
                    self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('number')) + ' : ', WHITE)])
                    self.screen_text.extend([(str(self.bool_obj.modifiers['circular_array'].count), HIGHTLIGHT)])
=======
                if any([m for m in self.bool_obj.modifiers if m.name == "Circular_Array"]):
                    self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('number')) + ' : ', WHITE)])
                    self.screen_text.extend([(str(self.bool_obj.modifiers['Circular_Array'].count), HIGHTLIGHT)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('axisSelection')) + ' : V / B', WHITE)])
                self.screen_text.extend([CR, ('    '+str(translate.get(get_addon_preferences().language).get('remove') + ' : Del'), WHITE)])

            elif self.adjustment == 'SMOOTH':
                self.screen_text.extend([CR, CR, ('Curve', HIGHTLIGHT)])
                self.screen_text.extend([CR, ('    '+'Subdivisions : ', WHITE)])
                self.screen_text.extend([(str(self.bool_obj.modifiers['Subdivision'].levels), HIGHTLIGHT)])

            elif self.adjustment == 'SYM':
                self.screen_text.extend([CR, CR, ('SYMETRIZE PLAN', HIGHTLIGHT)])

        self.screen_text.extend([CR, CR, ('KEYS', WHITE)])
        if self.draw_type == 'poly' and self.build_step == 0.5 and not self.screw_drawing:
<<<<<<< HEAD
            self.screen_text.extend([CR,('    Revolver Mode : A', WHITE)])
        if self.screw_drawing:
            self.screen_text.extend([CR,('    Revolve : Space', WHITE)])
        if self.build_step == 1:
            self.screen_text.extend([CR,('    Display grid : Right Click on face', WHITE)])
            self.screen_text.extend([CR,('    Draw outside : Shift + Left Click on face before to draw', WHITE)])
        if self.build_step == 2 and self.draw_type == 'poly':
            self.screen_text.extend([CR,('    Snap : Hold Ctrl', WHITE)])
        if self.build_step == 2 and self.draw_type == 'box':
            self.screen_text.extend([CR,('    Draw from center : Hold Shift', WHITE)])
            self.screen_text.extend([CR,('    Draw square : Hold Ctrl', WHITE)])
        if self.build_step == 2:
            self.screen_text.extend([CR,('    Draw in ortho plane : Shift + (X / Y / Z)', WHITE)])
        if self.build_step == 2 and self.draw_type == 'poly' :
            self.screen_text.extend([CR,('    Undo : ', WHITE),('Back space', WHITE)])
=======
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('revolveMode'))+' : A', WHITE)])
        if self.screw_drawing:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('revolve'))+' : Right Click', WHITE)])
        if self.build_step == 1:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('displayGrid')), WHITE)])
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('drawOutside')), WHITE)])
        if self.build_step == 2 and self.draw_type == 'poly':
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('snap')), WHITE)])
        if self.build_step == 2 and self.draw_type == 'box':
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('drawFromCenter')), WHITE)])
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('drawSquare')), WHITE)])
        if self.build_step == 2:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('drawOrtho'))+' : Shift + (X / Y / Z)', WHITE)])
        if self.build_step == 2 and self.draw_type == 'poly' :
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('undo')), WHITE),('Back space', WHITE)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('validateDrawing')), WHITE),(' : Right click', WHITE)])
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('validatePath')), WHITE),(' : Space', WHITE)])
        if self.build_step == 3:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('makePreset')), WHITE),(' : E / Shift + E', WHITE)])
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('cutAgain')), WHITE),(' : Shift + W', WHITE)])
            # self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('moveObj')), WHITE)])
            # self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('moveObjZ')), WHITE)])
<<<<<<< HEAD
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('useFlyMenu')), WHITE)])
=======
            # self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('useFlyMenu')), WHITE)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('finish')), WHITE)])
        if self.build_step == 4:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('finishCurrentAdjustement')), WHITE)])
        if self.build_step in {3,4}:
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('showBoolObj')), WHITE)])

        self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('cancel')), WHITE)])

        if self.snap_display == 'SPECIAL_POINTS':
            self.screen_text.extend([CR,CR,('GRID', WHITE)])
<<<<<<< HEAD
            self.screen_text.extend([CR,('    Grid resolution : ', WHITE), (str(self.snap_resolution - 1), HIGHTLIGHT)])
            self.screen_text.extend([CR,('    Grid rotation : X (', WHITE)])
=======
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('gridResolution')) + ' : ', WHITE), (str(self.snap_resolution - 1), HIGHTLIGHT)])
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('gridRotation'))+' : X', WHITE)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.screen_text.extend([(str(self.drawing_tool_plan_obj['local_X_rotation']), HIGHTLIGHT)])
            self.screen_text.extend([(') Y (', WHITE)])
            self.screen_text.extend([(str(self.drawing_tool_plan_obj['local_Y_rotation']), HIGHTLIGHT)])
            self.screen_text.extend([(') Z (', WHITE)])
            self.screen_text.extend([(str(self.drawing_tool_plan_obj['local_Z_rotation']), HIGHTLIGHT)])
            self.screen_text.extend([(')', WHITE)])
<<<<<<< HEAD
            self.screen_text.extend([CR,('    Alignment helper', WHITE)])
=======
            self.screen_text.extend([CR,('    '+str(translate.get(get_addon_preferences().language).get('alignmentHelper')), WHITE)])
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if self.snap_align:
                self.screen_text.extend([(' : ', WHITE), ('D', HIGHTLIGHT)])
            else:
                self.screen_text.extend([(' : ', WHITE), ('D', WHITE)])
            # self.screen_text.extend([CR,('    Square divisions', WHITE), (' : N', WHITE)])
            # self.screen_text.extend([CR,('    Extend grid : W', WHITE)])
            # self.screen_text.extend([CR,('    Hide grid : X', WHITE)])

    def hover(self, target):
        if self.mouse_x >= target[0] and self.mouse_x <= target[1]:
            if self.mouse_y >= target[2] and self.mouse_y <= target[3]:
                return True
            else:
                return False

    def auto_bevel_segments(self, context, obj, bevel_name):
        angle = math.sqrt(math.asin(min(obj.modifiers[bevel_name].width, 1)))
        segments = int(context.scene.fluentProp.bevel_resolution * (angle + (1 - math.cos(angle))))
        if segments < 4 :
            segments = 4
        return segments

    def make_plan_tool(self, context, event, target):
        self.draw_from_out = False
        self.drawing_tool_plan_verts.append((-self.plane_size, self.plane_size, 0))
        self.drawing_tool_plan_verts.append((self.plane_size, self.plane_size, 0))
        self.drawing_tool_plan_verts.append((self.plane_size, -self.plane_size, 0))
        self.drawing_tool_plan_verts.append((-self.plane_size, -self.plane_size, 0))
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        faces = [(0, 1, 2, 3)]
        mesh_data = bpy.data.meshes.new("drawing_tool_plan_data")
        mesh_data.from_pydata(self.drawing_tool_plan_verts, [], [])
        mesh_data.update()
        drawing_tool_plan_obj = bpy.data.objects.new("drawing_tool_plan_obj", mesh_data)
        self.drawing_tool_plan_obj = drawing_tool_plan_obj
        bpy.context.scene.collection.objects.link(drawing_tool_plan_obj)
        context.view_layer.objects.active = drawing_tool_plan_obj
        if self.bool_target:
            self.bool_target.select_set(False)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()
        drawing_tool_plan_obj.update_from_editmode()
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        self.drawing_tool_plan_obj['local_Y_rotation'] = 0
        self.drawing_tool_plan_obj['local_X_rotation'] = 0
        self.drawing_tool_plan_obj['local_Z_rotation'] = 0

        if self.bool_target:
            drawing_tool_plan_obj.location = self.cast['hit']
            Up=mathutils.Vector((0,0,1))
            norm = self.cast['normal']
            Qrot=norm.rotation_difference(Up)
            drawing_tool_plan_obj.rotation_mode='QUATERNION'
            drawing_tool_plan_obj.rotation_quaternion@=Qrot.inverted()

            target.select_set(False)
            drawing_tool_plan_obj.select_set(True)
            context.view_layer.objects.active = drawing_tool_plan_obj
            bpy.ops.object.hide_view_set(unselected = False)
            rotate_plane(drawing_tool_plan_obj)
        else:
            drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.hide_view_set()

        drawing_tool_plan_obj.select_set(False)

    def build_mesh_quad_plan(self, context, event):
        if self.build_step in {1, 0.5}:
            for i in range(4):
                self.bool_obj_verts.append((0, 0, 0))
            edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
            faces = [(0, 1, 2, 3)]
            mesh_data = bpy.data.meshes.new("bool_obj_data")
            mesh_data.from_pydata(self.bool_obj_verts, [], [])
            mesh_data.update()
            bool_obj = bpy.data.objects.new("bool_obj", mesh_data)
            self.bool_obj = bool_obj
            bpy.context.scene.collection.objects.link(bool_obj)
            bool_obj.select_set(True)
            context.view_layer.objects.active = bool_obj

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bool_obj.update_from_editmode()

            bpy.ops.object.mode_set(mode='OBJECT')
<<<<<<< HEAD
=======
            bool_obj['fluent_type'] = 'box'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            if self.bool_target:

                if self.mesh_maker_call:
                    bool_obj.display_type = 'TEXTURED'
                else:
                    bool_obj.display_type = 'WIRE'
                bool_obj.show_transparent = True
                bool_obj.show_wire = True
                bool_obj.location = self.cast['hit']
                Up=mathutils.Vector((0,0,1))
                norm = self.cast['normal']
                Qrot=norm.rotation_difference(Up)
                bool_obj.rotation_mode='QUATERNION'
                bool_obj.rotation_quaternion@=Qrot.inverted()

                self.bool_target.select_set(False)
                bool_obj.select_set(True)
                context.view_layer.objects.active = bool_obj

                bool_obj.select_set(False)
                bpy.ops.object.hide_view_set(unselected = False)
                rotate_plane(bool_obj)
            else:
                bool_obj.display_type = 'TEXTURED'
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.flip_normals()
                bpy.ops.object.mode_set(mode='OBJECT')

            self.bool_obj.select_set(True)
            if self.build_step == 1:
                self.build_step = 2

        elif self.build_step == 2:
            if self.delta_click:
                if not event.shift:
                    if not event.ctrl:
                        self.bool_obj.data.vertices[0].co.x = self.delta_click.x
                        self.bool_obj.data.vertices[0].co.y = self.delta_click.y
                        self.bool_obj.data.vertices[2].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[2].co.y = self.cast['hit'].y
                        self.bool_obj.data.vertices[1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = self.cast['hit'].y
                    else:
                        snap_result = self.snap(self.bool_obj.data.vertices[0].co.x, self.bool_obj.data.vertices[0].co.y, self.cast['hit'].x, self.cast['hit'].y, '45')
                        self.bool_obj.data.vertices[0].co.x = self.delta_click.x
                        self.bool_obj.data.vertices[0].co.y = self.delta_click.y
                        self.bool_obj.data.vertices[2].co.x = snap_result[0]
                        self.bool_obj.data.vertices[2].co.y = snap_result[1]
                        self.bool_obj.data.vertices[1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = snap_result[1]
                else:
                    if not event.ctrl:
                        self.bool_obj.data.vertices[0].co.x = self.delta_click.x  - (self.cast['hit'].x - self.delta_click.x)
                        self.bool_obj.data.vertices[0].co.y = self.delta_click.y  - (self.cast['hit'].y - self.delta_click.y)
                        self.bool_obj.data.vertices[2].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[2].co.y = self.cast['hit'].y
                        self.bool_obj.data.vertices[1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = self.cast['hit'].y
                    else:
                        snap_result = self.snap(self.delta_click.x, self.delta_click.y, self.cast['hit'].x, self.cast['hit'].y, '45')
                        self.bool_obj.data.vertices[0].co.x = self.delta_click.x  - (snap_result[0] - self.delta_click.x)
                        self.bool_obj.data.vertices[0].co.y = self.delta_click.y  - (snap_result[1] - self.delta_click.y)
                        self.bool_obj.data.vertices[2].co.x = snap_result[0]
                        self.bool_obj.data.vertices[2].co.y = snap_result[1]
                        self.bool_obj.data.vertices[1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = snap_result[1]

            else:
                if not event.shift:
                    if not event.ctrl:
                        self.bool_obj.data.vertices[0].co.x = 0
                        self.bool_obj.data.vertices[0].co.y = 0
                        self.bool_obj.data.vertices[2].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[2].co.y = self.cast['hit'].y
                        self.bool_obj.data.vertices[1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = self.cast['hit'].y
                    else:
                        snap_result = self.snap(self.bool_obj.data.vertices[0].co.x, self.bool_obj.data.vertices[0].co.y, self.cast['hit'].x, self.cast['hit'].y, '45')
                        self.bool_obj.data.vertices[0].co.x = 0
                        self.bool_obj.data.vertices[0].co.y = 0
                        self.bool_obj.data.vertices[2].co.x = snap_result[0]
                        self.bool_obj.data.vertices[2].co.y = snap_result[1]
                        self.bool_obj.data.vertices[1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = snap_result[1]
                else:
                    if not event.ctrl:
                        self.bool_obj.data.vertices[0].co.x = (-1)*self.cast['hit'].x
                        self.bool_obj.data.vertices[0].co.y = (-1)*self.cast['hit'].y
                        self.bool_obj.data.vertices[2].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[2].co.y = self.cast['hit'].y
                        self.bool_obj.data.vertices[1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = self.cast['hit'].y
                    else:
                        snap_result = self.snap(0, 0, self.cast['hit'].x, self.cast['hit'].y, '45')
                        self.bool_obj.data.vertices[0].co.x = (-1) * snap_result[0]
                        self.bool_obj.data.vertices[0].co.y = (-1) * snap_result[1]
                        self.bool_obj.data.vertices[2].co.x = snap_result[0]
                        self.bool_obj.data.vertices[2].co.y = snap_result[1]
                        self.bool_obj.data.vertices[1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[1].co.y = self.bool_obj.data.vertices[0].co.y
                        self.bool_obj.data.vertices[3].co.x = self.bool_obj.data.vertices[0].co.x
                        self.bool_obj.data.vertices[3].co.y = snap_result[1]

    def build_mesh_prism(self, context, event):
        if self.build_step in {1, 0.5}:
            self.bool_obj_verts.append((0, 0, 0))
            self.bool_obj_verts.append((0, 0, 0))
            edges = [(0, 1)]
            mesh_data = bpy.data.meshes.new("bool_obj_data")
            mesh_data.from_pydata(self.bool_obj_verts, edges, [])
            mesh_data.update()
            bool_obj = bpy.data.objects.new("bool_obj", mesh_data)
            self.bool_obj = bool_obj
            bpy.context.scene.collection.objects.link(bool_obj)
            context.view_layer.objects.active = bool_obj

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            self.bool_obj.data.vertices[1].select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            new_vert_group = bpy.ops.object.vertex_group_add()
            bpy.ops.object.vertex_group_assign()
            v_groups = bpy.context.active_object.vertex_groups
            v_groups[0].name = 'radius'
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')


            if self.bool_target:
                if self.mesh_maker_call:
                    bool_obj.display_type = 'TEXTURED'
                else:
                    bool_obj.display_type = 'WIRE'
                bool_obj.show_transparent = True
                bool_obj.show_wire = True
                bool_obj.location = self.cast['hit']
                Up=mathutils.Vector((0,0,1))
                norm=self.cast['normal']
                Qrot=norm.rotation_difference(Up)
                bool_obj.rotation_mode='QUATERNION'
                bool_obj.rotation_quaternion@=Qrot.inverted()

                bool_obj.select_set(False)
                bpy.ops.object.hide_view_set(unselected = False)
                rotate_plane(bool_obj)
            else:
                bool_obj.display_type = 'TEXTURED'
            bool_obj.select_set(True)
            bpy.context.object.data.use_auto_smooth = True

            # creation des modifiers
            bpy.ops.object.mode_set(mode = 'OBJECT')
            modif = bool_obj.modifiers.new(name='Radius', type='DISPLACE')
            modif.show_in_editmode = True
            modif.show_on_cage = True
            modif.direction = 'X'
            modif.vertex_group = 'radius'
            modif.strength = 0
            modif.mid_level = 0

            bpy.ops.object.mode_set(mode = 'OBJECT')
            modif = bool_obj.modifiers.new(name='Screw', type='SCREW')
<<<<<<< HEAD
            modif.steps = bpy.context.scene.fluentProp.prism_segments
            modif.render_steps = bpy.context.scene.fluentProp.prism_segments
            if modif.steps >= 8:
                bool_obj['fluent_cylinder'] = True
            else:
                bool_obj['fluent_cylinder'] = False
            modif.use_merge_vertices = True

            modif = bool_obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
            modif.thickness = bpy.context.scene.fluentProp.depth
=======
            modif.merge_threshold = 0.0001
            modif.steps = bpy.context.scene.fluentProp.prism_segments
            modif.render_steps = bpy.context.scene.fluentProp.prism_segments
            if modif.steps >= 8:
                bool_obj['fluent_type'] = 'prism'
            else:
                bool_obj['fluent_type'] = 'semi-prism'
            modif.use_merge_vertices = True

            modif = bool_obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
            if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                modif.thickness = bpy.context.scene.fluentProp.depth
            else:
                modif.thickness = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            modif_decim = bool_obj.modifiers.new(name='Decimate', type='DECIMATE')
            modif_decim.decimate_type = 'DISSOLVE'
            modif_decim.angle_limit = 0.00174533

            if self.bool_target:
                if self.mesh_maker_call:
                    modif.offset = -1
                else:
                    if self.angle == 0:
                        if bpy.context.scene.fluentProp.solidify_offset:
                            modif.offset = bpy.context.scene.fluentProp.solidify_offset
                        else:
                            modif.offset = -0.99
                    else:
                        modif.offset = 0
            else:
                modif.offset = 0

            if self.build_step == 1:
                self.build_step = 2

        elif self.build_step == 2:
            if self.delta_click:
                self.bool_obj.data.vertices[0].co.x = self.delta_click.x
                self.bool_obj.data.vertices[0].co.y = self.delta_click.y
                self.bool_obj.data.vertices[1].co.x = self.delta_click.x
                self.bool_obj.data.vertices[1].co.y = self.delta_click.y
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                self.delta_hit = self.delta_click
                self.delta_click = None
            if self.delta_hit:
                a = (self.cast['hit'].x - self.delta_hit.x) - self.bool_obj.data.vertices[0].co.x
                b = (self.cast['hit'].y - self.delta_hit.y) - self.bool_obj.data.vertices[0].co.y
                self.bool_obj.modifiers['Radius'].strength  = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
            else:
                a = self.cast['hit'].x - self.bool_obj.data.vertices[0].co.x
                b = self.cast['hit'].y - self.bool_obj.data.vertices[0].co.y
                self.bool_obj.modifiers['Radius'].strength  = math.sqrt(math.pow(a, 2) + math.pow(b, 2))

    def build_mesh_poly(self, context, event):
        if self.build_step in {1, 0.5}:
            for i in range(self.poly_count):
                self.bool_obj_verts.append((0, 0, 0))
            edges = []
            for i in range(self.poly_count - 1):
                edges.append((i, i+1))
            edges.append((23, 0))
            faces = [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)]
            mesh_data = bpy.data.meshes.new("bool_obj_data")
            mesh_data.from_pydata(self.bool_obj_verts, edges, faces)
            mesh_data.update()
            bool_obj = bpy.data.objects.new("bool_obj", mesh_data)
            self.bool_obj = bool_obj
            bpy.context.scene.collection.objects.link(bool_obj)
            context.view_layer.objects.active = bool_obj
            bpy.ops.object.mode_set(mode='OBJECT')
            if self.bool_target:

                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                if self.mesh_maker_call:
                    bool_obj.display_type = 'TEXTURED'
                else:
                    bool_obj.display_type = 'WIRE'
                bool_obj.show_transparent = True
                bool_obj.show_wire = True
                bool_obj.location = self.cast['hit']
                Up = mathutils.Vector((0,0,1))
                norm = self.cast['normal']
                Qrot=norm.rotation_difference(Up)
                bool_obj.rotation_mode='QUATERNION'
                bool_obj.rotation_quaternion@=Qrot.inverted()

                bool_obj.select_set(False)
                bpy.ops.object.hide_view_set(unselected = False)

                bpy.ops.object.mode_set(mode='EDIT')
                bool_obj.update_from_editmode()
                bpy.ops.object.mode_set(mode='OBJECT')
                rotate_plane(bool_obj)
            else:
                bool_obj.display_type = 'TEXTURED'

            bool_obj.select_set(True)
            bpy.context.view_layer.objects.active = self.bool_obj

            if self.build_step == 1:
                self.build_step = 2

        elif self.build_step == 2:
<<<<<<< HEAD

=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if event.type == 'MOUSEMOVE':
                if self.delta_click :
                    if not event.ctrl:
                        self.bool_obj.data.vertices[self.poly_count-1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[self.poly_count-1].co.y = self.cast['hit'].y
                    else:
                        if self.poly_count == self.poly_count_origin :
                            snap_result = self.snap(self.bool_obj.data.vertices[self.poly_count-2].co.x, self.bool_obj.data.vertices[self.poly_count-2].co.y, self.cast['hit'].x, self.cast['hit'].y)
                        else:
                            snap_result = self.snap(self.bool_obj.data.vertices[self.poly_count].co.x, self.bool_obj.data.vertices[self.poly_count].co.y, self.cast['hit'].x, self.cast['hit'].y)
                        self.bool_obj.data.vertices[self.poly_count-1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[self.poly_count-1].co.y = snap_result[1]
                else:
                    if not event.ctrl:
                        self.bool_obj.data.vertices[self.poly_count-1].co.x = self.cast['hit'].x
                        self.bool_obj.data.vertices[self.poly_count-1].co.y = self.cast['hit'].y
                    else:
                        if self.poly_count == self.poly_count_origin :
                            snap_result = self.snap(self.bool_obj.data.vertices[self.poly_count-2].co.x, self.bool_obj.data.vertices[self.poly_count-2].co.y, self.cast['hit'].x, self.cast['hit'].y)
                        else:
                            snap_result = self.snap(self.bool_obj.data.vertices[self.poly_count].co.x, self.bool_obj.data.vertices[self.poly_count].co.y, self.cast['hit'].x, self.cast['hit'].y)
                        self.bool_obj.data.vertices[self.poly_count-1].co.x = snap_result[0]
                        self.bool_obj.data.vertices[self.poly_count-1].co.y = snap_result[1]

            if event.value == 'PRESS' and event.type == 'LEFTMOUSE':
                self.poly_count = self.poly_count - 1

    def fake_obj(self):
        vertex = []
        vertex.append((-10, -10, 0))
        vertex.append((-10, 10, 0))
        vertex.append((10, 10, 0))
        vertex.append((10, -10, 0))
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        faces = [(0, 1, 2, 3)]
        mesh_data = bpy.data.meshes.new("fakeFluentObject_data")
        mesh_data.from_pydata(vertex, edges, faces)
        mesh_data.update()
        self.bool_target = bpy.data.objects.new("fakeFluentObject", mesh_data)
        bpy.context.scene.collection.objects.link(self.bool_target)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        depsgraph.update()
        self.normal = mathutils.Vector((0,0,1))

    def build_path(self, context, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if not self.mesh_maker_call and latest_bevel_manager(self.original_bool_target, True):
            bpy.ops.object.shade_smooth()
        obj['fluent_object'] = True
        # First bevel
        modif = obj.modifiers.new(name='First_Bevel', type='BEVEL')
        modif.limit_method = 'VGROUP'
        modif.vertex_group = 'bevel'
        modif.use_only_vertices = True
        modif.width = bpy.context.scene.fluentProp.corner
        modif.segments = self.auto_bevel_segments(context,obj,'First_Bevel')
        if modif.width == 0:
            modif.show_viewport = False
            modif.show_render = False
        else:
            modif.show_viewport = True
            modif.show_render = True

        modif = obj.modifiers.new(name='Screw', type='SCREW')
        modif.angle = 0
        modif.axis = 'Z'
        modif.steps = 3
        modif.render_steps = 2
        modif.screw_offset = 2
        # Solidify
        modif = obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
        modif.offset = 0
        modif.thickness = bpy.context.scene.fluentProp.depth
        modif.use_even_offset = True

    def make_inset(self):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = []
        i = 0
        for v in active_object('GET').data.vertices:
            if v.select:
                selected_verts.append(i)
            i+=1
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = bpy.context.selected_objects[1]
        obj.select_set(False)
        active_object(self.bool_target, 'SET')
        for v in selected_verts:
            self.bool_target.data.vertices[v].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.dissolve_mode(use_verts=True)
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.bool_target.select_set(False)
        obj = active_object(obj, 'SET')
        self.bool_obj = obj
<<<<<<< HEAD
=======
        self.bool_obj['fluent_type'] = 'box'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        obj.display_type = 'WIRE'
        self.draw_type = 'inset'

    def add_modifiers(self, context, event, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj = active_object(obj, 'SET')
        if not tool_called == 'CREATION':
            cycles_visibility(False)
        if not self.mesh_maker_call and latest_bevel_manager(self.original_bool_target, True):
            bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
        obj['fluent_object'] = True
        if self.draw_type in {'box', 'poly', 'inset'}:
            # flip normal si pas dans le bon sens
            if self.mesh_maker_call:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            else:
                if self.draw_type in {'box', 'poly'}:
                    face_target_world_normal = self.normal
                    face_target_world_normal.normalize()
                    bool_obj_world_normal = self.bool_obj.matrix_world.to_3x3() @ self.bool_obj.data.polygons[0].normal
                    bool_obj_world_normal.normalize()
                    if round(face_target_world_normal.x, 5) != round(bool_obj_world_normal.x, 5) or round(face_target_world_normal.y, 5) != round(bool_obj_world_normal.y, 5) or round(face_target_world_normal.z, 5) != round(bool_obj_world_normal.z, 5):
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.flip_normals()
                        bpy.ops.object.mode_set(mode='OBJECT')
            for v in obj.data.vertices:
                v.select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            new_vert_group = bpy.ops.object.vertex_group_add()
            bpy.ops.object.vertex_group_assign()
            v_groups = bpy.context.active_object.vertex_groups
            v_groups[0].name = 'bevel'
<<<<<<< HEAD
=======

            if self.mesh_maker_call and self.draw_type == 'box':
                bpy.ops.mesh.subdivide()
                bpy.ops.object.mode_set(mode='OBJECT')
                obj.vertex_groups["bevel"].remove([4, 5, 6, 7, 8])
                bpy.ops.object.mode_set(mode='EDIT')

            bpy.ops.mesh.select_mode(type='FACE')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.modifiers.new(name='First_Bevel', type='BEVEL')
            obj.modifiers['First_Bevel'].limit_method = 'VGROUP'
            obj.modifiers['First_Bevel'].vertex_group = 'bevel'
            obj.modifiers['First_Bevel'].use_only_vertices = True
            obj.modifiers['First_Bevel'].width = bpy.context.scene.fluentProp.corner
            if bpy.context.scene.fluentProp.straight_bevel:
                obj.modifiers['First_Bevel'].segments = 1
            else:
                obj.modifiers['First_Bevel'].segments = self.auto_bevel_segments(context,obj,'First_Bevel')
            if obj.modifiers['First_Bevel'].width == 0:
                obj.modifiers['First_Bevel'].show_viewport = False
                obj.modifiers['First_Bevel'].show_render = False
            else:
                obj.modifiers['First_Bevel'].show_viewport = True
                obj.modifiers['First_Bevel'].show_render = True
            # Solidify
            obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
<<<<<<< HEAD
=======
            obj.modifiers['First_Solidify'].show_in_editmode = False
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if self.mesh_maker_call:
                if self.bool_target:
                    obj.modifiers['First_Solidify'].offset = -1
                else:
                    obj.modifiers['First_Solidify'].offset = 0
            else:
                if self.angle == 0:
                    if bpy.context.scene.fluentProp.solidify_offset:
                        obj.modifiers['First_Solidify'].offset = bpy.context.scene.fluentProp.solidify_offset
                    else:
                        obj.modifiers['First_Solidify'].offset = -0.99
                else:
                    obj.modifiers['First_Solidify'].offset = 0
<<<<<<< HEAD
            obj.modifiers['First_Solidify'].thickness = bpy.context.scene.fluentProp.depth
=======
            if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                obj.modifiers['First_Solidify'].thickness = bpy.context.scene.fluentProp.depth
            else:
                if tool_called == 'CREATION':
                    obj.modifiers['First_Solidify'].thickness = 0
                else:
                    obj.modifiers['First_Solidify'].thickness = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        elif self.draw_type == 'prism':
            # flip normal si pas dans le bon sens
            if self.bool_target:
                bpy.ops.object.duplicate()
                the_copy = bpy.context.selected_objects[0]
                self.bool_obj.select_set(False)
                bpy.ops.object.convert(target='MESH')
                face_target_world_normal = self.bool_target.matrix_world.to_3x3().inverted().transposed() @ self.cast['normal']
                face_target_world_normal.normalize()
                bool_obj_world_normal = self.bool_obj.matrix_world.to_3x3().inverted().transposed() @ the_copy.data.polygons[0].normal
                bool_obj_world_normal.normalize()
                bpy.data.objects.remove(the_copy, do_unlink=True)
                self.bool_obj.select_set(True)
                bpy.context.view_layer.objects.active = self.bool_obj
                if round(face_target_world_normal.x, 5) != round(bool_obj_world_normal.x, 5) or round(face_target_world_normal.y, 5) != round(bool_obj_world_normal.y, 5) or round(face_target_world_normal.z, 5) != round(bool_obj_world_normal.z, 5):
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode='OBJECT')
        elif self.draw_type == 'path':
            self.bool_obj_location[0] = obj.location.x
            self.bool_obj_location[1] = obj.location.y
            self.bool_obj_location[2] = obj.location.z
            vec = mathutils.Vector((0.0, 0.0, 0.01))
            inv = obj.matrix_world.copy()
            inv.invert()
            vec_rot = vec @ inv
            obj.location = obj.location + vec_rot

            for v in obj.data.vertices:
                v.select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            new_vert_group = bpy.ops.object.vertex_group_add()
            bpy.ops.object.vertex_group_assign()
            v_groups = bpy.context.active_object.vertex_groups
            v_groups[0].name = 'bevel'
            bpy.ops.object.mode_set(mode='OBJECT')

            if not self.screw_drawing:
                modif = obj.modifiers.new(name='Screw', type='SCREW')
                modif.angle = 0
                modif.axis = 'Z'
                modif.steps = 2
                modif.render_steps = 2
<<<<<<< HEAD
                modif.screw_offset = bpy.context.scene.fluentProp.depth * (-1)
=======
                if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                    modif.screw_offset = bpy.context.scene.fluentProp.depth * (-1)
                else:
                    modif.screw_offset = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414) * (-1)

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                #Decimate
                modif = obj.modifiers.new(name='Decimate', type='DECIMATE')
                modif.decimate_type = 'DISSOLVE'
                # First bevel
                modif = obj.modifiers.new(name='First_Bevel', type='BEVEL')
                modif.limit_method = 'ANGLE'
                modif.use_only_vertices = False
                modif.width = bpy.context.scene.fluentProp.corner
                modif.segments = self.auto_bevel_segments(context,obj,'First_Bevel')
                if modif.width == 0:
                    modif.show_viewport = False
                    modif.show_render = False
                else:
                    modif.show_viewport = True
                    modif.show_render = True
                # Solidify
                modif = obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
                modif.offset = 0
                modif.thickness = .01
                modif.use_even_offset = True
            else:
                modif = obj.modifiers.new(name='Screw', type='SCREW')
                modif.angle = math.radians(360)
                modif.axis = 'Y'
                modif.steps = bpy.context.scene.fluentProp.prism_segments
                modif.render_steps = bpy.context.scene.fluentProp.prism_segments
                if modif.steps >= 8:
<<<<<<< HEAD
                    obj['fluent_cylinder'] = True
                else:
                    obj['fluent_cylinder'] = False
=======
                    obj['fluent_type'] = 'prism'
                else:
                    obj['fluent_type'] = 'semi-prism'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                modif.screw_offset = 0
                bpy.context.object.modifiers["Screw"].use_merge_vertices = True
                #Decimate
                modif = obj.modifiers.new(name='Decimate', type='DECIMATE')
                modif.decimate_type = 'DISSOLVE'
                modif.angle_limit = 0.00174533

            # Solidify
            modif = obj.modifiers.new(name='First_Solidify', type='SOLIDIFY')
            modif.offset = 0
            modif.thickness = 0
            modif.use_even_offset = True
            modif.show_render = False
            modif.show_viewport = False
        # Second bevel
        obj.modifiers.new(name='Second_Bevel', type='BEVEL')
        obj.modifiers['Second_Bevel'].limit_method = 'ANGLE'
        obj.modifiers['Second_Bevel'].angle_limit = 0.523599
        obj.modifiers['Second_Bevel'].width = bpy.context.scene.fluentProp.second_bevel_width
        if bpy.context.scene.fluentProp.second_bevel_straight:
            obj.modifiers['Second_Bevel'].segments = 1
        else:
            obj.modifiers['Second_Bevel'].segments = self.auto_bevel_segments(context,obj,'Second_Bevel')
        obj.modifiers['Second_Bevel'].use_clamp_overlap = False
        obj.modifiers['Second_Bevel'].miter_outer = 'MITER_ARC'
        if bpy.context.scene.fluentProp.second_bevel_width:
            obj.modifiers['Second_Bevel'].show_viewport = True
            obj.modifiers['Second_Bevel'].show_render = True
        else:
            obj.modifiers['Second_Bevel'].show_viewport = False
            obj.modifiers['Second_Bevel'].show_render = False
        # Second Solidify
        obj.modifiers.new(name='Second_Solidify', type='SOLIDIFY')
        obj.modifiers['Second_Solidify'].offset = 0
        obj.modifiers['Second_Solidify'].thickness = -0.01
        obj.modifiers['Second_Solidify'].use_even_offset = True
        obj.modifiers['Second_Solidify'].show_viewport = False
        obj.modifiers['Second_Solidify'].show_render = False

        # Array
        obj.modifiers.new(name='ArrayX', type='ARRAY')
        obj.modifiers['ArrayX'].relative_offset_displace[0] = 1
        obj.modifiers['ArrayX'].relative_offset_displace[1] = 0
        obj.modifiers['ArrayX'].relative_offset_displace[2] = 0
        obj.modifiers['ArrayX'].count = 2
        obj.modifiers['ArrayX'].show_render = False
        obj.modifiers['ArrayX'].show_viewport = False

        obj.modifiers.new(name='ArrayY', type='ARRAY')
        obj.modifiers['ArrayY'].relative_offset_displace[0] = 0
        obj.modifiers['ArrayY'].relative_offset_displace[1] = 1
        obj.modifiers['ArrayY'].relative_offset_displace[2] = 0
        obj.modifiers['ArrayY'].count = 2
        obj.modifiers['ArrayY'].show_render = False
        obj.modifiers['ArrayY'].show_viewport = False

        obj.modifiers.new(name='ArrayZ', type='ARRAY')
        obj.modifiers['ArrayZ'].relative_offset_displace[0] = 0
        obj.modifiers['ArrayZ'].relative_offset_displace[1] = 0
        obj.modifiers['ArrayZ'].relative_offset_displace[2] = 1
        obj.modifiers['ArrayZ'].count = 2
        obj.modifiers['ArrayZ'].show_render = False
        obj.modifiers['ArrayZ'].show_viewport = False

        # Mirror
        obj.modifiers.new(name='Mirror', type='MIRROR')
        obj.modifiers['Mirror'].mirror_object = self.original_bool_target
        obj.modifiers['Mirror'].show_viewport = False
        obj.modifiers['Mirror'].show_render = False
        obj.modifiers['Mirror'].use_axis[0] = False
        obj.modifiers['Mirror'].use_axis[1] = False
        obj.modifiers['Mirror'].use_axis[2] = False

        if bpy.context.scene.fluentProp.auto_mirror_x :
            obj.modifiers['Mirror'].use_axis[0] = True
            obj.modifiers['Mirror'].show_viewport = True
            obj.modifiers['Mirror'].show_render = True
        if bpy.context.scene.fluentProp.auto_mirror_y :
            obj.modifiers['Mirror'].use_axis[1] = True
            obj.modifiers['Mirror'].show_viewport = True
            obj.modifiers['Mirror'].show_render = True
        if bpy.context.scene.fluentProp.auto_mirror_z :
            obj.modifiers['Mirror'].use_axis[2] = True
            obj.modifiers['Mirror'].show_viewport = True
            obj.modifiers['Mirror'].show_render = True

        # Second Mirror
        obj.modifiers.new(name='Second_Mirror', type='MIRROR')
        obj.modifiers['Second_Mirror'].mirror_object = self.original_bool_target
        obj.modifiers['Second_Mirror'].show_viewport = False
        obj.modifiers['Second_Mirror'].show_render = False
        obj.modifiers['Second_Mirror'].use_axis[0] = False
        obj.modifiers['Second_Mirror'].use_axis[1] = False
        obj.modifiers['Second_Mirror'].use_axis[2] = False

        # si pas de rebool ***************************************************************************************
        if self.bool_target and not self.rebool_call and not self.mesh_maker_call:
            new_mod = self.bool_target.modifiers.new(name='Boolean', type="BOOLEAN")
            new_mod.operation = self.bool_operation
            new_mod.object = obj
            new_mod.show_expanded = False
            latest_bevel_manager(self.bool_target, 'REPLACE')
            for modif in obj.modifiers:
                modif.show_expanded = False
            if obj.modifiers['First_Solidify'].thickness > 0 and self.draw_type != 'path':
                self.bool_operation = 'DIFFERENCE'
                self.switch_bool_operation()
            elif obj.modifiers['First_Solidify'].thickness < 0 and self.draw_type != 'path':
                self.bool_operation = 'UNION'
                self.switch_bool_operation()
        # si demande de rebool *************************************************************
        if self.bool_target and self.rebool_call and not self.mesh_maker_call:
            # attention ici on dupplique la copie pour faire le rebool
            obj.select_set(False)
            self.bool_target.select_set(True)
            bpy.ops.object.duplicate()
            the_copy = bpy.context.selected_objects[0]
            the_copy['fluent_object'] = True
            self.rebool_obj = the_copy

            new_mod = self.bool_target.modifiers.new(name='Boolean', type="BOOLEAN")
            new_mod.operation = 'DIFFERENCE'
            new_mod.object = obj
            new_mod.show_expanded = False

            new_mod = the_copy.modifiers.new(name='Boolean', type="BOOLEAN")
            new_mod.operation = 'INTERSECT'
            new_mod.object = obj
            new_mod.show_expanded = False

            the_copy.select_set(False)

            if latest_bevel_manager(self.bool_target, 'CHECK'):
                latest_bevel_manager(the_copy, 'REPLACE')
                latest_bevel_manager(self.bool_target, 'REPLACE')

            for modif in obj.modifiers:
                modif.show_expanded = False

            for modif in the_copy.modifiers:
                modif.show_expanded = False


        bpy.context.view_layer.objects.active = self.bool_obj

    def switch_bool_operation(self):
        i = 0
        latestKey = 0
        if self.bool_target and self.bool_obj:
            for m in range(len(self.bool_target.modifiers)):
                if self.bool_target.modifiers[i].type == 'BOOLEAN':
                    latestKey = i
                i+=1
            if self.bool_operation == 'DIFFERENCE':
                self.bool_target.modifiers[latestKey].operation = 'DIFFERENCE'


            elif self.bool_operation == 'UNION':
                self.bool_target.modifiers[latestKey].operation = 'UNION'
            elif self.bool_operation == 'INTERSECT':
                self.bool_target.modifiers[latestKey].operation = 'INTERSECT'

    def hideModifier(self, obj, mod):
        if obj.modifiers[mod].show_render:
            obj.modifiers[mod].show_render = False
            obj.modifiers[mod].show_viewport = False
        else:
            obj.modifiers[mod].show_render = True
            obj.modifiers[mod].show_viewport = True
        self.end_of_adjustment()

    def end_of_adjustment(self):
        self.adjustment = ''
        self.other_adjustement = False
        self.build_step = 3
        self.array_axis = ''

    def fly_adjustement(self, context, event):
        obj = self.bool_obj
        self.bool_obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
<<<<<<< HEAD
=======

        # saisie des valeurs
        if event.value == 'PRESS' and event.type in {'NUMPAD_0', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 'NUMPAD_5', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_PERIOD', 'PERIOD', 'COMMA'}:
            if self.enter_value == 'None':
                self.enter_value = ''
            if event.type == 'NUMPAD_0':
                self.enter_value += '0'
            elif event.type == 'NUMPAD_1':
                self.enter_value += '1'
            elif event.type == 'NUMPAD_2':
                self.enter_value += '2'
            elif event.type == 'NUMPAD_2':
                self.enter_value += '2'
            elif event.type == 'NUMPAD_3':
                self.enter_value += '3'
            elif event.type == 'NUMPAD_4':
                self.enter_value += '4'
            elif event.type == 'NUMPAD_5':
                self.enter_value += '5'
            elif event.type == 'NUMPAD_6':
                self.enter_value += '6'
            elif event.type == 'NUMPAD_7':
                self.enter_value += '7'
            elif event.type == 'NUMPAD_8':
                self.enter_value += '8'
            elif event.type == 'NUMPAD_9':
                self.enter_value += '9'
            elif event.type in {'NUMPAD_PERIOD', 'PERIOD', 'COMMA'}:
                self.enter_value += '.'

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if self.adjustment == 'FIRST_SOLIDIFY':
            modif_name = 'First_Solidify'
            if event.value == 'PRESS' and event.type == 'C':
                if self.draw_type in {'box', 'poly', 'prism'}:
                    if self.other_adjustement:
                        self.other_adjustement = False
                        self.modifier_previous_value = obj.modifiers[modif_name].thickness
<<<<<<< HEAD
=======
                        self.x_mouse_slider_origin = event.mouse_region_x
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                    else:
                        self.other_adjustement = True
                        self.modifier_previous_value = obj.modifiers[modif_name].offset
                        self.x_mouse_slider_origin = event.mouse_region_x
                elif self.draw_type == 'path':
                    obj.modifiers[modif_name].thickness = 0.001
<<<<<<< HEAD
            if event.value == 'PRESS' and event.type == 'V':
                if self.draw_type in {'box', 'poly', 'prism'}:
                    obj.modifiers[modif_name].thickness = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414)
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            if self.shift_work:
                increment = 3000
            elif self.ctrl_work:
                increment = 30
            else:
                increment = 300
<<<<<<< HEAD
=======

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                if not self.other_adjustement:
                    self.modifier_previous_value = obj.modifiers[modif_name].thickness
                else:
                    self.modifier_previous_value = obj.modifiers[modif_name].offset
<<<<<<< HEAD
            if not self.other_adjustement:
                if event.mouse_region_x != self.x_mouse_slider_origin and event.type == 'MOUSEMOVE':
                    obj.modifiers[modif_name].thickness = self.modifier_previous_value - ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
            else:
                if event.mouse_region_x != self.x_mouse_slider_origin:
                    obj.modifiers[modif_name].offset = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
=======

            if not self.other_adjustement:
                if event.mouse_region_x != self.x_mouse_slider_origin:
                    obj.modifiers[modif_name].thickness = self.modifier_previous_value - ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                if enter_value_validation(self.enter_value, event)[0]:
                    obj.modifiers[modif_name].thickness = enter_value_validation(self.enter_value, event)[1]
                    self.end_of_adjustment()
            else:
                if event.mouse_region_x != self.x_mouse_slider_origin:
                    obj.modifiers[modif_name].offset = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                if enter_value_validation(self.enter_value, event)[0]:
                    obj.modifiers[modif_name].offset = enter_value_validation(self.enter_value, event)[1]
                    self.end_of_adjustment()

            if event.value == 'PRESS' and event.type == 'V':
                if self.draw_type in {'box', 'poly', 'prism'}:
                    obj.modifiers[modif_name].thickness = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414)
                    self.end_of_adjustment()

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if obj.modifiers[modif_name].thickness > 0 and not self.rebool_call and not self.mesh_maker_call and self.bool_operation != 'DIFFERENCE' and self.draw_type != 'path':
                self.bool_operation = 'DIFFERENCE'
                self.switch_bool_operation()
            elif  obj.modifiers[modif_name].thickness < 0 and not self.rebool_call and not self.mesh_maker_call and self.bool_operation != 'UNION' and self.draw_type != 'path':
                self.bool_operation = 'UNION'
                self.switch_bool_operation()
<<<<<<< HEAD
            if obj.modifiers[modif_name].offset < -1 :
                obj.modifiers[modif_name].offset = -1
=======

            if obj.modifiers[modif_name].offset < -1 :
                obj.modifiers[modif_name].offset = -1

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if obj.modifiers[modif_name].offset > 1 :
                obj.modifiers[modif_name].offset = 1

        if self.adjustment == 'SCREW' :
            modif_name = 'Screw'
            if event.value == 'PRESS' and event.type == 'V':
                obj.modifiers[modif_name].screw_offset = max(self.bool_target.dimensions[0] * 1.414, self.bool_target.dimensions[1] * 1.414, self.bool_target.dimensions[2] * 1.414) * (-1)
            if self.shift_work:
                increment = 3000
            elif self.ctrl_work:
                increment = 30
            else:
                increment = 300
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                self.modifier_previous_value = obj.modifiers[modif_name].screw_offset
            if event.mouse_region_x != self.x_mouse_slider_origin and event.type == 'MOUSEMOVE':
                obj.modifiers[modif_name].screw_offset = self.modifier_previous_value - ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
<<<<<<< HEAD
=======
            if enter_value_validation(self.enter_value, event)[0]:
                    obj.modifiers[modif_name].screw_offset = enter_value_validation(self.enter_value, event)[1]
                    self.end_of_adjustment()
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if obj.modifiers[modif_name].screw_offset < 0 and not self.rebool_call and not self.mesh_maker_call and self.bool_operation == 'UNION':
                self.bool_operation = 'DIFFERENCE'
                self.switch_bool_operation()
                obj.location.x = self.bool_obj_location[0]
                obj.location.y = self.bool_obj_location[1]
                obj.location.z = self.bool_obj_location[2]
                vec = mathutils.Vector((0.0, 0.0, 0.01))
                inv = obj.matrix_world.copy()
                inv.invert()
                vec_rot = vec @ inv
                obj.location = obj.location + vec_rot
            elif  obj.modifiers[modif_name].screw_offset > 0 and not self.rebool_call and not self.mesh_maker_call and self.bool_operation == 'DIFFERENCE':
                self.bool_operation = 'UNION'
                self.switch_bool_operation()
                obj.location.x = self.bool_obj_location[0]
                obj.location.y = self.bool_obj_location[1]
                obj.location.z = self.bool_obj_location[2]
                vec = mathutils.Vector((0.0, 0.0, -0.01))
                inv = obj.matrix_world.copy()
                inv.invert()
                vec_rot = vec @ inv
                obj.location = obj.location + vec_rot

        if self.adjustment == 'SECOND_SOLIDIFY':
            if self.shift_work:
                increment = 10000
            elif self.ctrl_work:
                increment = 100
            else:
                increment = 1000
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                self.modifier_previous_value = obj.modifiers['Second_Solidify'].thickness
            if event.mouse_region_x != self.x_mouse_slider_origin:
                obj.modifiers['Second_Solidify'].thickness = self.modifier_previous_value - ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
<<<<<<< HEAD
            if event.value == 'PRESS' and event.type == 'C':
                obj.modifiers['Second_Solidify'].thickness = .001
=======
            if enter_value_validation(self.enter_value, event)[0]:
                obj.modifiers[modif_name].thickness = enter_value_validation(self.enter_value, event)[1]
                self.end_of_adjustment()
            if event.value == 'PRESS' and event.type == 'C':
                obj.modifiers['Second_Solidify'].thickness = .0001
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.end_of_adjustment()

            if event.value == 'PRESS' and event.type == 'DEL':
                self.hideModifier(obj, 'Second_Solidify')

        if self.draw_type != 'prism' and self.adjustment == 'FIRST_BEVEL':
            if self.shift_work:
                increment = 5000
            elif self.ctrl_work:
                increment = 50
            else:
                increment = 500
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                self.modifier_previous_value = obj.modifiers['First_Bevel'].width
            if event.mouse_region_x != self.x_mouse_slider_origin:
                obj.modifiers['First_Bevel'].width = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
<<<<<<< HEAD

=======
            if enter_value_validation(self.enter_value, event)[0]:
                obj.modifiers['First_Bevel'].width = enter_value_validation(self.enter_value, event)[1]
                self.end_of_adjustment()
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if obj.modifiers['First_Bevel'].segments != 1:
                obj.modifiers['First_Bevel'].segments = self.auto_bevel_segments(context,obj,'First_Bevel')
            if obj.modifiers['First_Bevel'].width == 0:
                obj.modifiers['First_Bevel'].show_viewport = False
                obj.modifiers['First_Bevel'].show_render = False
            else:
                obj.modifiers['First_Bevel'].show_viewport = True
                obj.modifiers['First_Bevel'].show_render = True
            if event.value == 'PRESS' and event.type == 'DEL':
                self.hideModifier(obj, 'First_Bevel')

        if self.draw_type != 'prism' and event.value == 'PRESS' and event.type == 'C' and self.adjustment == 'FIRST_BEVEL':
            if obj.modifiers['First_Bevel'].segments == 1:
                obj.modifiers['First_Bevel'].segments = self.auto_bevel_segments(context,obj,'First_Bevel')
            else:
                obj.modifiers['First_Bevel'].segments = 1

        if self.adjustment == 'SECOND_BEVEL':
            if self.shift_work:
                increment = 5000
            elif self.ctrl_work:
                increment = 50
            else:
                increment = 500
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                self.modifier_previous_value = obj.modifiers['Second_Bevel'].width
            if event.mouse_region_x != self.x_mouse_slider_origin:
                obj.modifiers['Second_Bevel'].width = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
<<<<<<< HEAD
=======
            if enter_value_validation(self.enter_value, event)[0]:
                obj.modifiers['Second_Bevel'].width = enter_value_validation(self.enter_value, event)[1]
                self.end_of_adjustment()
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if obj.modifiers['Second_Bevel'].segments != 1:
                obj.modifiers['Second_Bevel'].segments = self.auto_bevel_segments(context,obj,'Second_Bevel')
            if obj.modifiers['Second_Bevel'].width == 0:
                obj.modifiers['Second_Bevel'].show_viewport = False
                obj.modifiers['Second_Bevel'].show_render = False
            else:
                obj.modifiers['Second_Bevel'].show_viewport = True
                obj.modifiers['Second_Bevel'].show_render = True
            if event.value == 'PRESS' and event.type == 'DEL':
                self.hideModifier(obj, 'Second_Bevel')
        if event.value == 'PRESS' and event.type == 'C' and self.adjustment == 'SECOND_BEVEL':
            if obj.modifiers['Second_Bevel'].segments == 1:
                obj.modifiers['Second_Bevel'].segments = self.auto_bevel_segments(context,obj,'Second_Bevel')
            else:
                obj.modifiers['Second_Bevel'].segments = 1

        if self.adjustment == 'MIRROR':
            if event.shift and event.value == 'PRESS' and event.type == 'LEFTMOUSE':
                target = click_on(context, self.mouse_x, self.mouse_y)
                bpy.context.scene.cursor.location = target.get('hit')
                if not self.empty_mirror:
                    self.empty_mirror = empty_manager(None)
                self.empty_mirror.location = target.get('hit')
                obj.modifiers['Mirror'].mirror_object = self.empty_mirror
                obj.modifiers['Second_Mirror'].show_viewport = True
                obj.modifiers['Second_Mirror'].show_render = True
            if event.shift :
                modif_name = 'Second_Mirror'
            else:
                modif_name = 'Mirror'
            if event.value == 'PRESS' and event.type == 'X':
                if obj.modifiers[modif_name].use_axis[0] :
                    obj.modifiers[modif_name].use_axis[0] = False
                    if not obj.modifiers[modif_name].use_axis[0] and not obj.modifiers[modif_name].use_axis[1] and not obj.modifiers[modif_name].use_axis[2]:
                        obj.modifiers[modif_name].show_viewport = False
                        obj.modifiers[modif_name].show_render = False
                else:
                    obj.modifiers[modif_name].use_axis[0] = True
                    obj.modifiers[modif_name].show_viewport = True
                    obj.modifiers[modif_name].show_render = True
            if event.value == 'PRESS' and event.type == 'Y':
                if obj.modifiers[modif_name].use_axis[1] :
                    obj.modifiers[modif_name].use_axis[1] = False
                    if not obj.modifiers[modif_name].use_axis[0] and not obj.modifiers[modif_name].use_axis[1] and not obj.modifiers[modif_name].use_axis[2]:
                        obj.modifiers[modif_name].show_viewport = False
                        obj.modifiers[modif_name].show_render = False
                else:
                    obj.modifiers[modif_name].use_axis[1] = True
                    obj.modifiers[modif_name].show_viewport = True
                    obj.modifiers[modif_name].show_render = True
            if event.value == 'PRESS' and event.type == 'Z':
                if obj.modifiers[modif_name].use_axis[2] :
                    obj.modifiers[modif_name].use_axis[2] = False
                    if not obj.modifiers[modif_name].use_axis[0] and not obj.modifiers[modif_name].use_axis[1] and not obj.modifiers[modif_name].use_axis[2]:
                        obj.modifiers[modif_name].show_viewport = False
                        obj.modifiers[modif_name].show_render = False
                else:
                    obj.modifiers[modif_name].use_axis[2] = True
                    obj.modifiers[modif_name].show_viewport = True
                    obj.modifiers[modif_name].show_render = True

        if self.adjustment == 'ARRAY':
            if event.value == 'PRESS' and event.type == 'X':
                if self.array_axis == 'X':
                    self.array_axis = ''
                    obj.modifiers['ArrayX'].show_viewport = False
                    obj.modifiers['ArrayX'].show_render = False
                else:
                    self.x_mouse_slider_origin = event.mouse_region_x
                    self.modifier_previous_value = obj.modifiers['ArrayX'].relative_offset_displace[0]
                    self.other_adjustement = 'OFFSET'
                    self.array_axis = 'X'
                    obj.modifiers['ArrayX'].show_viewport = True
                    obj.modifiers['ArrayX'].show_render = True

            if event.value == 'PRESS' and event.type == 'Y':
                if self.array_axis == 'Y':
                    self.array_axis = ''
                    obj.modifiers['ArrayY'].show_viewport = False
                    obj.modifiers['ArrayY'].show_render = False
                else:
                    self.x_mouse_slider_origin = event.mouse_region_x
                    self.modifier_previous_value = obj.modifiers['ArrayY'].relative_offset_displace[1]
                    self.other_adjustement = 'OFFSET'
                    self.array_axis = 'Y'
                    obj.modifiers['ArrayY'].show_viewport = True
                    obj.modifiers['ArrayY'].show_render = True


            if event.value == 'PRESS' and event.type == 'Z':
                if self.array_axis == 'Z':
                    self.array_axis = ''
                    obj.modifiers['ArrayZ'].show_viewport = False
                    obj.modifiers['ArrayZ'].show_render = False
                else:
                    self.x_mouse_slider_origin = event.mouse_region_x
                    self.modifier_previous_value = obj.modifiers['ArrayZ'].relative_offset_displace[2]
                    self.other_adjustement = 'OFFSET'
                    self.array_axis = 'Z'
                    obj.modifiers['ArrayZ'].show_viewport = True
                    obj.modifiers['ArrayZ'].show_render = True

            if event.value == 'PRESS' and event.type == 'S':
                self.other_adjustement = 'OFFSET'
                self.x_mouse_slider_origin = event.mouse_region_x
                if self.array_axis == 'X':
                    self.modifier_previous_value = obj.modifiers['ArrayX'].relative_offset_displace[0]
                if self.array_axis == 'Y':
                    self.modifier_previous_value = obj.modifiers['ArrayY'].relative_offset_displace[1]
                if self.array_axis == 'Z':
                        self.modifier_previous_value = obj.modifiers['ArrayZ'].relative_offset_displace[2]
            if event.value == 'PRESS' and event.type == 'D':
                    self.other_adjustement = 'COUNT'
                    self.x_mouse_slider_origin = event.mouse_region_x
                    if self.array_axis == 'X':
                        self.modifier_previous_value = obj.modifiers['ArrayX'].count
                    if self.array_axis == 'Y':
                        self.modifier_previous_value = obj.modifiers['ArrayY'].count
                    if self.array_axis == 'Z':
                        self.modifier_previous_value = obj.modifiers['ArrayZ'].count
            if self.shift_work:
                increment = 1000
            elif self.ctrl_work:
                increment = 10
            else:
                increment = 100
            if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                self.x_mouse_slider_origin = event.mouse_region_x
                if self.array_axis == 'X':
                    self.modifier_previous_value = obj.modifiers['ArrayX'].relative_offset_displace[0]
                elif self.array_axis == 'Y':
                    self.modifier_previous_value = obj.modifiers['ArrayY'].relative_offset_displace[1]
                elif self.array_axis == 'Z':
                    self.modifier_previous_value = obj.modifiers['ArrayZ'].relative_offset_displace[2]
            if event.type == 'MOUSEMOVE' and self.array_axis != '':
                if self.array_axis == 'X':
                    if self.other_adjustement == 'OFFSET':
                        if event.mouse_region_x != self.x_mouse_slider_origin:
                            obj.modifiers['ArrayX'].relative_offset_displace[0] = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                    else:
                        obj.modifiers['ArrayX'].count = self.modifier_previous_value + (event.mouse_region_x - self.x_mouse_slider_origin)/40

                if self.array_axis == 'Y':
                    if self.other_adjustement == 'OFFSET':
                        if event.mouse_region_x != self.x_mouse_slider_origin:
                            obj.modifiers['ArrayY'].relative_offset_displace[1] = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                    else:
                        obj.modifiers['ArrayY'].count = self.modifier_previous_value + (event.mouse_region_x - self.x_mouse_slider_origin)/40

                if self.array_axis == 'Z':
                    if self.other_adjustement == 'OFFSET':
                        if event.mouse_region_x != self.x_mouse_slider_origin:
                            obj.modifiers['ArrayZ'].relative_offset_displace[2] = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                    else:
                        obj.modifiers['ArrayZ'].count = self.modifier_previous_value + (event.mouse_region_x - self.x_mouse_slider_origin)/40

<<<<<<< HEAD
        if self.draw_type == 'prism' and event.type == 'MOUSEMOVE' and self.adjustment == 'RADIUS':
=======
        if self.draw_type == 'prism' and self.adjustment == 'RADIUS':
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            obj = bpy.context.active_object
            if event.mouse_region_x != self.x_mouse_slider_origin and not event.shift:
                obj.modifiers['Radius'].strength = self.modifier_previous_value + ((self.mouse_x - self.x_mouse_slider_origin)/100)
            else:
                obj.modifiers['Radius'].strength = self.modifier_previous_value + ((self.mouse_x - self.x_mouse_slider_origin)/1000)
<<<<<<< HEAD
=======
            if enter_value_validation(self.enter_value, event)[0]:
                obj.modifiers['Radius'].strength = enter_value_validation(self.enter_value, event)[1]
                self.end_of_adjustment()
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

        if self.draw_type in {'prism', 'screw'} and self.adjustment == 'RESOLUTION':
            obj = bpy.context.active_object
            if self.shift_work:
                increment = 100
            else:
                increment = 10
            if self.shift_press or self.shift_release:
                self.modifier_previous_value = obj.modifiers['Screw'].steps
                self.x_mouse_slider_origin = event.mouse_region_x
<<<<<<< HEAD
            if event.type == 'MOUSEMOVE':
                if event.mouse_region_x != self.x_mouse_slider_origin:
                        obj.modifiers['Screw'].steps = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                        obj.modifiers['Screw'].render_steps = obj.modifiers['Screw'].steps
                else:
                    obj.modifiers['Screw'].steps = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                    obj.modifiers['Screw'].render_steps = obj.modifiers['Screw'].steps
                if obj.modifiers['Screw'].steps >= 8:
                    obj['fluent_cylinder'] = True
                else:
                    obj['fluent_cylinder'] = False
=======
            if event.mouse_region_x != self.x_mouse_slider_origin:
                obj.modifiers['Screw'].steps = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                obj.modifiers['Screw'].render_steps = obj.modifiers['Screw'].steps
            if enter_value_validation(self.enter_value, event)[0]:
                obj.modifiers['Screw'].steps = enter_value_validation(self.enter_value, event)[1]
                obj.modifiers['Screw'].render_steps = enter_value_validation(self.enter_value, event)[1]
                self.end_of_adjustment()
            if obj.modifiers['Screw'].steps >= 8:
                obj['fluent_type'] = 'prism'
            else:
                obj['fluent_type'] = 'semi-prism'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

        if self.draw_type == 'prism' and event.value == 'PRESS' and event.type == 'C' and self.adjustment == 'RESOLUTION':
            obj = bpy.context.active_object
            if obj.modifiers['Screw'].steps == context.scene.fluentProp.bevel_resolution *4:
                obj.modifiers['Screw'].steps = context.scene.fluentProp.bevel_resolution
                obj.modifiers['Screw'].render_steps = obj.modifiers['Screw'].steps
            else:
                obj.modifiers['Screw'].steps = context.scene.fluentProp.bevel_resolution * 4
                obj.modifiers['Screw'].render_steps = obj.modifiers['Screw'].steps

        if self.adjustment == 'CIRCULAR_ARRAY':
<<<<<<< HEAD
            has_circular_array = False
            for m in self.bool_obj.modifiers:
                if m.name == 'circular_displace':
                    has_circular_array = True
                    if not m.show_render:
                        m.show_render = True
                        m.show_viewport = True
                if m.name == 'circular_array':
                    if not m.show_render:
                        m.show_render = True
                        m.show_viewport = True
            if not has_circular_array:
=======
            has_Circular_Array = False
            for m in self.bool_obj.modifiers:
                if m.name == 'Circular_Displace':
                    has_Circular_Array = True
                    if not m.show_render:
                        m.show_render = True
                        m.show_viewport = True
                if m.name == 'Circular_Array':
                    if not m.show_render:
                        m.show_render = True
                        m.show_viewport = True
            if not has_Circular_Array:
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.ops.object.add(type='EMPTY')
                self.empty_obj = bpy.context.active_object

                self.empty_obj.matrix_world = self.bool_obj.matrix_world

<<<<<<< HEAD
                self.empty_matrix_save = self.bool_obj.matrix_world

                displace_modif = self.bool_obj.modifiers.new(name='circular_displace', type='DISPLACE')
=======
                self.empty_matrix_save = self.bool_obj.matrix_world.copy()

                displace_modif = self.bool_obj.modifiers.new(name='Circular_Displace', type='DISPLACE')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                displace_modif.direction = 'X'
                displace_modif.show_in_editmode = True
                displace_modif.show_on_cage = True
                displace_modif.strength = 0

<<<<<<< HEAD
                array_modif = self.bool_obj.modifiers.new(name='circular_array', type='ARRAY')
=======
                array_modif = self.bool_obj.modifiers.new(name='Circular_Array', type='ARRAY')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                array_modif.use_relative_offset = False
                array_modif.use_object_offset = True
                array_modif.count = 4
                self.empty_obj.matrix_world @= Matrix.Rotation(math.radians(90), 4, 'Z')
                array_modif.offset_object = self.empty_obj

                # place les modifiers au dessus des array et du mirror
                context.view_layer.objects.active = self.bool_obj
<<<<<<< HEAD
                bpy.ops.object.modifier_move_up(modifier="circular_displace")
                bpy.ops.object.modifier_move_up(modifier="circular_displace")
                bpy.ops.object.modifier_move_up(modifier="circular_displace")
                bpy.ops.object.modifier_move_up(modifier="circular_displace")

                bpy.ops.object.modifier_move_up(modifier="circular_array")
                bpy.ops.object.modifier_move_up(modifier="circular_array")
                bpy.ops.object.modifier_move_up(modifier="circular_array")
                bpy.ops.object.modifier_move_up(modifier="circular_array")
=======
                bpy.ops.object.modifier_move_up(modifier="Circular_Displace")
                bpy.ops.object.modifier_move_up(modifier="Circular_Displace")
                bpy.ops.object.modifier_move_up(modifier="Circular_Displace")
                bpy.ops.object.modifier_move_up(modifier="Circular_Displace")

                bpy.ops.object.modifier_move_up(modifier="Circular_Array")
                bpy.ops.object.modifier_move_up(modifier="Circular_Array")
                bpy.ops.object.modifier_move_up(modifier="Circular_Array")
                bpy.ops.object.modifier_move_up(modifier="Circular_Array")
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

                self.bool_obj.select_set(True)
                self.empty_obj.select_set(True)
                context.view_layer.objects.active = self.bool_obj
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                self.empty_obj.select_set(False)
                self.empty_obj.hide_viewport = True

            else:
                if event.value == 'PRESS' and event.type == 'C':
                    if self.other_adjustement:
                        self.other_adjustement = False
<<<<<<< HEAD
                        self.modifier_previous_value = self.bool_obj.modifiers['circular_displace'].strength
                        self.x_mouse_slider_origin = event.mouse_region_x
                    else:
                        self.other_adjustement = True
                        self.modifier_previous_value = self.bool_obj.modifiers['circular_array'].count
=======
                        self.modifier_previous_value = self.bool_obj.modifiers['Circular_Displace'].strength
                        self.x_mouse_slider_origin = event.mouse_region_x
                    else:
                        self.other_adjustement = True
                        self.modifier_previous_value = self.bool_obj.modifiers['Circular_Array'].count
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                        self.x_mouse_slider_origin = event.mouse_region_x

                if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                    self.x_mouse_slider_origin = event.mouse_region_x
                    if self.other_adjustement:
<<<<<<< HEAD
                        self.modifier_previous_value = self.bool_obj.modifiers['circular_array'].count
                    else:
                        self.modifier_previous_value = self.bool_obj.modifiers['circular_displace'].strength

                if event.type == 'MOUSEMOVE':
=======
                        self.modifier_previous_value = self.bool_obj.modifiers['Circular_Array'].count
                    else:
                        self.modifier_previous_value = self.bool_obj.modifiers['Circular_Displace'].strength

                if event.type == 'MOUSEMOVE' or enter_value_validation(self.enter_value, event):
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                    if not self.other_adjustement:
                        if self.shift_work:
                            increment = 2000
                        elif self.ctrl_work:
                            increment = 20
                        else:
                            increment = 200
                        if self.shift_press or self.shift_release or self.ctrl_press or self.ctrl_release:
                            self.x_mouse_slider_origin = event.mouse_region_x
<<<<<<< HEAD
                            self.modifier_previous_value = self.bool_obj.modifiers['circular_displace'].strength
                        self.bool_obj.modifiers['circular_displace'].strength = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
=======
                            self.modifier_previous_value = self.bool_obj.modifiers['Circular_Displace'].strength
                        self.bool_obj.modifiers['Circular_Displace'].strength = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment)
                        if enter_value_validation(self.enter_value, event)[0]:
                            obj.modifiers['Circular_Displace'].strength = enter_value_validation(self.enter_value, event)[1]
                            self.end_of_adjustment()
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                    else:
                        if self.shift_work:
                            increment = 300
                        elif self.ctrl_work:
                            increment = 20
                        else:
                            increment = 100
<<<<<<< HEAD
                        a = self.bool_obj.modifiers['circular_array'].count
                        self.bool_obj.modifiers['circular_array'].count = int(self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment))
                        b = self.bool_obj.modifiers['circular_array'].count
                        if a != b:
                            self.empty_obj.matrix_world = self.empty_matrix_save
                            angle = 360 / self.bool_obj.modifiers['circular_array'].count
                            self.empty_obj.matrix_world @= Matrix.Rotation(math.radians(angle), 4, 'Z')
                if event.value == 'PRESS' and event.type == 'DEL':
                    self.hideModifier(obj, 'circular_displace')
                    self.hideModifier(obj, 'circular_array')
=======
                        a = self.bool_obj.modifiers['Circular_Array'].count
                        self.bool_obj.modifiers['Circular_Array'].count = int(self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/increment))
                        b = self.bool_obj.modifiers['Circular_Array'].count
                        if a != b:
                            self.empty_obj.matrix_world = self.empty_matrix_save
                            angle = 360 / self.bool_obj.modifiers['Circular_Array'].count
                            self.empty_obj.matrix_world @= Matrix.Rotation(math.radians(angle), 4, 'Z')

                if event.value == 'PRESS' and event.type == 'DEL':
                    self.hideModifier(obj, 'Circular_Displace')
                    self.hideModifier(obj, 'Circular_Array')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                if event.value == 'PRESS' and event.type == 'V' and not self.draw_type in {'prism', 'screw'} :
                    for v in self.bool_obj.data.vertices:
                        rotated_point = rotation_cartesian(v.co.x, v.co.y)
                        v.co.x = rotated_point[0]
                        v.co.y = rotated_point[1]
                if event.value == 'PRESS' and event.type == 'B':
                    if self.draw_type=='prism':
                        if self.bool_obj.modifiers['Radius'].direction == 'X':
                            self.bool_obj.modifiers['Radius'].direction ='Z'
                            self.bool_obj.modifiers['Screw'].axis ='X'
                        else:
                            self.bool_obj.modifiers['Radius'].direction ='X'
                            self.bool_obj.modifiers['Screw'].axis ='Z'
                    elif self.draw_type == 'screw':
                        if self.bool_obj.modifiers['Screw'].axis == 'Z':
                            bpy.ops.view3d.snap_cursor_to_selected()
                            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, False, False))
                            bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
                            bpy.ops.object.editmode_toggle()
                            bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
                            self.bool_obj.modifiers['Screw'].axis = 'X'
                        elif self.bool_obj.modifiers['Screw'].axis == 'X':
                            bpy.ops.view3d.snap_cursor_to_selected()
                            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
                            bpy.ops.transform.rotate(value=-1.5708, orient_axis='Y', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, False, False))
                            bpy.ops.object.editmode_toggle()
                            bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
                            self.bool_obj.modifiers['Screw'].axis = 'Z'

                    else:
                        for v in self.bool_obj.data.vertices:
                            if v.co.z == 0:
                                v.co.z = v.co.x
                                v.co.x = 0
                            else:
                                v.co.x = v.co.z
                                v.co.z = 0

        if self.adjustment == 'SMOOTH':
            if event.value == 'PRESS' and event.type == 'X':
                if smooth_manager(self.bool_obj, 'CHECK'):
                    smooth_manager(self.bool_obj, 'REMOVE')
                else:
                    smooth_manager(self.bool_obj, 'ADD')
            if event.type == 'MOUSEMOVE':
                obj.modifiers['Decimate'].show_viewport = False
                obj.modifiers['Subdivision'].levels = self.modifier_previous_value + ((event.mouse_region_x - self.x_mouse_slider_origin)/200)
                obj.modifiers['Subdivision'].render_levels = obj.modifiers['Subdivision'].levels
            else:
                obj.modifiers['Decimate'].show_viewport = True

<<<<<<< HEAD
=======
        if self.adjustment == 'FLIP':
            if obj.modifiers["Screw"].use_normal_flip:
                obj.modifiers["Screw"].use_normal_flip = False
            else:
                obj.modifiers["Screw"].use_normal_flip = True
            self.end_of_adjustment()

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    def modal(self, context, event):
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y
        # gestion des evenements du shift
        if event.shift and not self.shift_press and not self.shift_work:
            self.shift_press = True
        elif event.shift and self.shift_press:
            self.shift_press = False
            self.shift_work = True
        elif not event.shift and self.shift_work:
            self.shift_release = True
            self.shift_work = False
        elif not event.shift and self.shift_release:
            self.shift_release = False
<<<<<<< HEAD
=======
        else:
            self.shift_press = False
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        # gestion des evenements du ctrl
        if event.ctrl and not self.ctrl_press and not self.ctrl_work:
            self.ctrl_press = True
        elif event.ctrl and self.ctrl_press:
            self.ctrl_press = False
            self.ctrl_work = True
        elif not event.ctrl and self.ctrl_work:
            self.ctrl_release = True
            self.ctrl_work = False
        elif not event.ctrl and self.ctrl_release:
            self.ctrl_release = False
<<<<<<< HEAD
=======
        else:
            self.ctrl_press = False
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

        self.update_display()
        draw_callback_px(self, context)

<<<<<<< HEAD
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_5', 'NUMPAD_7', 'G', 'TAB'} and self.build_step in {0.5,1, 2, 3, 4} or event.type == 'R' and  self.build_step in {3, 4} or event.alt:
            return {'PASS_THROUGH'}

=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if bpy.context.active_object:
            if bpy.context.active_object.mode == 'EDIT' and event.value == 'PRESS' and event.type == 'I' and event.shift and not self.bool_obj:
                self.make_inset()
                self.bool_target.select_set(False)
                self.add_modifiers(context, event, self.bool_obj)
                self.draw_type = 'box'
                self.build_step = 4
                self.adjustment = 'FIRST_SOLIDIFY'
            elif bpy.context.active_object.mode == 'EDIT':
                return {'PASS_THROUGH'}

<<<<<<< HEAD
=======
        if event.type in {'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_5', 'NUMPAD_7'} and self.build_step in {0.5,1, 2, 3, 4} and not event.shift or event.type == 'R' and  self.build_step in {3, 4} or event.alt:
            return {'PASS_THROUGH'}

        # if event.type == get_addon_preferences().fluent_menu_shortcut_key and event:
        #     return {'RUNNING_MODAL'}

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'G', 'TAB'}:
            return {'PASS_THROUGH'}


>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if event.value == 'PRESS' and event.type == 'LEFTMOUSE':
            self.mouse_click = True
        if event.value == 'RELEASE' and event.type == 'LEFTMOUSE':
            self.mouse_click = False

        # Switch affichage boolean obj
        if event.value == 'PRESS' and event.type == 'H':
            if self.bool_obj.hide_viewport:
                self.bool_obj.hide_viewport = False
                self.bool_obj.select_set(True)
                bpy.context.view_layer.objects.active = self.bool_obj
            else:
                self.bool_obj.hide_viewport = True

        # toggle between wireframe/solid view
        if event.value == 'PRESS' and event.type == 'Q':
            if bpy.context.space_data.shading.type == 'SOLID':
                bpy.context.space_data.shading.type = 'WIREFRAME'
            elif bpy.context.space_data.shading.type == 'WIREFRAME':
                bpy.context.space_data.shading.type = 'SOLID'


        # Choix du type de dessin**********************************************************
        if self.build_step in {1,2,0.5} and event.value == 'PRESS' and event.type == 'R':
            self.draw_type = 'box'
            self.reset_draw(context, event, False)

        if  self.build_step in {1,2,0.5} and event.value == 'PRESS' and event.type == 'S':
            self.draw_type = 'poly'
            self.reset_draw(context, event, False)

        if  self.build_step in {1,2,0.5} and event.value == 'PRESS' and event.type == 'C':
            self.draw_type = 'prism'
            self.reset_draw(context, event, False)

        # Choix du type d'opération boolean
        if event.value == 'PRESS' and event.type == 'S' and self.build_step in {3} and not self.adjustment:
            self.bool_operation = 'DIFFERENCE'
            self.switch_bool_operation()

        if event.value == 'PRESS' and event.type == 'D' and self.build_step in {3} and not self.adjustment:
            self.bool_operation = 'UNION'
            self.switch_bool_operation()

        if event.value == 'PRESS' and event.type == 'F' and self.build_step in {3} and not self.adjustment:
            self.bool_operation = 'INTERSECT'
            self.switch_bool_operation()

        # gestion des ajustements*************************************************************
        if self.adjustment:
            self.fly_adjustement(context, event)

        # sauvegardes des ajustements
        if self.build_step == 3 and event.value == 'PRESS' and event.type == 'E':
            preset_manager('GET', self.bool_obj)


<<<<<<< HEAD

=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        # reset de la sauvegarde des ajustements
        if self.build_step == 3 and event.value == 'PRESS' and event.type == 'E' and event.shift:
            preset_manager('RESET')

        if self.mouse_click and self.build_step == 3:
            self.build_step = 4
            if self.draw_type == 'box':
                self.box_menu.set_position(event.mouse_region_x, event.mouse_region_y)
                self.display_menu = self.box_menu
            if self.draw_type == 'poly':
                self.poly_menu.set_position(event.mouse_region_x, event.mouse_region_y)
                self.display_menu = self.poly_menu
            if self.draw_type == 'prism':
                self.prism_menu.set_position(event.mouse_region_x, event.mouse_region_y)
                self.display_menu = self.prism_menu
            if self.draw_type == 'path':
                self.path_menu.set_position(event.mouse_region_x, event.mouse_region_y)
                self.display_menu = self.path_menu
            if self.draw_type == 'screw':
                self.screw_menu.set_position(event.mouse_region_x, event.mouse_region_y)
                self.display_menu = self.screw_menu
        try:
            if not self.mouse_click and self.build_step == 4:
<<<<<<< HEAD
=======
                self.enter_value = 'None'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.adjustment = self.display_menu.action()
                self.x_mouse_slider_origin = event.mouse_region_x
                if self.adjustment == 'ARRAY':
                    bpy.ops.transform.select_orientation(orientation='LOCAL')
                    bpy.ops.wm.tool_set_by_id(name="builtin.move", cycle=False, space_type='VIEW_3D')
                if self.adjustment == 'CIRCULAR_ARRAY':
                    self.x_mouse_slider_origin = event.mouse_region_x
                    for m in self.bool_obj.modifiers:
<<<<<<< HEAD
                        if m.name == 'circular_displace':
                            if self.other_adjustement:
                                self.modifier_previous_value = self.bool_obj.modifiers['circular_array'].count
                            else:
                                self.modifier_previous_value = self.bool_obj.modifiers['circular_displace'].strength
=======
                        if m.name == 'Circular_Displace':
                            if self.other_adjustement:
                                self.modifier_previous_value = self.bool_obj.modifiers['Circular_Array'].count
                            else:
                                self.modifier_previous_value = self.bool_obj.modifiers['Circular_Displace'].strength
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                if self.adjustment == 'SYMETRIZE':
                    bpy.ops.transform.select_orientation(orientation='GLOBAL')
                    bpy.ops.wm.tool_set_by_id(name="builtin.move", cycle=False, space_type='VIEW_3D')
                    bpy.ops.wm.symetrizeaplan('INVOKE_DEFAULT')
                if self.adjustment == 'FIRST_SOLIDIFY':
                    self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
                if self.adjustment == 'SECOND_SOLIDIFY':
                    self.modifier_previous_value = self.bool_obj.modifiers['Second_Solidify'].thickness
                if self.adjustment == 'FIRST_BEVEL':
                    self.modifier_previous_value = self.bool_obj.modifiers['First_Bevel'].width
                if self.adjustment == 'SECOND_BEVEL':
                    self.modifier_previous_value = self.bool_obj.modifiers['Second_Bevel'].width
                if self.adjustment == 'SECOND_SOLIDIFY':
                    self.modifier_previous_value = self.bool_obj.modifiers['Second_Solidify'].thickness
                    self.bool_obj.modifiers['Second_Solidify'].show_viewport = True
                    self.bool_obj.modifiers['Second_Solidify'].show_render = True
                if self.adjustment == 'SMOOTH':
                    if not smooth_manager(self.bool_obj, 'CHECK'):
                        smooth_manager(self.bool_obj, 'ADD')
                        self.modifier_previous_value = self.bool_obj.modifiers['Subdivision'].levels
                if self.adjustment == 'RADIUS':
                    self.modifier_previous_value = self.bool_obj.modifiers['Radius'].strength
                if self.adjustment in {'RESOLUTION', 'SCREW'}:
                    if self.draw_type == 'path':
                        self.modifier_previous_value = self.bool_obj.modifiers['Screw'].screw_offset
                    else:
                        self.modifier_previous_value = self.bool_obj.modifiers['Screw'].steps
                self.display_menu = None
                self.build_step = 3
        except:pass
        if event.value == 'PRESS' and event.type == 'LEFTMOUSE' and self.adjustment:
            bpy.ops.transform.select_orientation(orientation='GLOBAL')
            bpy.ops.wm.tool_set_by_id(name="builtin.select", cycle=False, space_type='VIEW_3D')
            self.adjustment = None
            self.other_adjustement = False
            self.build_step = 3
            self.array_axis = ''
            self.display_menu = None

        # gestion du snap blender **************************************************************************
        if event.value=='PRESS' and event.type == 'F2':
            if bpy.context.scene.tool_settings.use_snap:
                bpy.context.scene.tool_settings.use_snap = False
            else:
                bpy.context.scene.tool_settings.use_snap = True
        if event.value=='PRESS' and event.type == 'F3':
            bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
        if event.value=='PRESS' and event.type == 'F4':
            bpy.context.scene.tool_settings.snap_elements = {'FACE'}
        if event.value=='PRESS' and event.type == 'F5':
            bpy.context.scene.tool_settings.snap_elements = {'INCREMENT'}

        # affichage du snap*******************************************************************
        if  event.value == 'PRESS' and event.type == 'RIGHTMOUSE' and self.build_step in {0.5, 1}:
            self.snap_display = 'NOTHING'
            if self.bool_target:
                self.reset_draw(context,event)
                self.snap_support = 'OBJECT'
                self.build_step = 0.5
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                self.save = self.cast.copy()
                self.normal = self.cast['normal']
                self.make_plan_tool(context, event, self.bool_target)
                self.snap_grid(context, event)
                self.grid_menu.set_position(context.region.width*0.75, context.region.height*0.5)
                self.display_menu = self.grid_menu
                if self.draw_type == 'box':
                    self.build_mesh_quad_plan(context, event)
                if self.draw_type == 'poly':
                    self.build_mesh_poly(context, event)
                if self.draw_type == 'prism':
                    self.build_mesh_prism(context, event)
            else:
                self.fake_obj()
                self.snap_support = 'PLANE'
                self.grid_menu.set_position(context.region.width*0.75, context.region.height*0.5)
                self.display_menu = self.grid_menu
                self.snap_grid(context, event)
                bpy.data.objects.remove(self.bool_target, do_unlink=True)
                self.bool_target = None

        if self.build_step in {3, 4, 5}:
            self.snap_display = 'NOTHING'

        if self.snap_display == 'SPECIAL_POINTS':
            # if event.value=='PRESS' and event.type == 'N':
            #     if self.snap_mode == 'DEFAULT':
            #         self.snap_mode = 'SQUARE'
            #     else:
            #         self.snap_mode = 'DEFAULT'
            #     self.snap_refresh = True
            if event.value == 'PRESS' and event.type == 'D':
                if self.snap_align:
                    self.snap_align = False
                else:
                    self.snap_align = True

        # gestion des menus*****************************************************************
        try:
            self.display_menu.hover(event.mouse_region_x, event.mouse_region_y)
            self.menu_hover = self.display_menu.get_menu_hover()
            if event.value == 'PRESS' and event.type == 'LEFTMOUSE' and self.display_menu:
                self.action = self.display_menu.action()

            if self.action == 'RESOLUTION_UP':
                self.snap_resolution = self.snap_resolution + 1
<<<<<<< HEAD
                if self.snap_resolution >= 22:
                    self.snap_resolution = 21
=======
                if self.snap_resolution >= 42:
                    self.snap_resolution = 41
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                get_addon_preferences().grid_resolution = self.snap_resolution
                self.snap_refresh = True
                self.action = None
            elif self.action == 'RESOLUTION_DOWN':
                self.snap_resolution = self.snap_resolution - 1
                if self.snap_resolution <= 2:
                    self.snap_resolution = 2
                get_addon_preferences().grid_resolution = self.snap_resolution
                self.snap_refresh = True
                self.action = None
            elif self.action == 'ZOOM_IN':
                if event.shift:
                    self.snap_zoom += 0.01
                    self.snap_refresh = True
                else:
                    self.snap_zoom += 0.1
                    self.snap_refresh = True
                get_addon_preferences().grid_size = self.snap_zoom
                self.action = None
            elif self.action == 'ZOOM_OUT':
                if event.shift:
                    self.snap_zoom -= 0.01
                    self.snap_refresh = True
                else:
                    self.snap_zoom -= 0.1
                    self.snap_refresh = True
                if self.snap_zoom <= 0:
                    self.snap_zoom == 0.01
                get_addon_preferences().grid_size = self.snap_zoom
                self.action = None
            elif self.action == 'EXTEND':
                if self.snap_extend:
                    self.snap_extend = False
                else:
                    self.snap_extend = True
                self.snap_refresh = True
                self.action = None
            elif self.action == 'HIDE':
                self.snap_display = 'NOTHING'
                self.reset_draw(context, event)
            elif 'ROTATE' in self.action and not 'WORKING' in self.action:
                self.slider_origine_x = event.mouse_region_x
                self.old_rotation = self.drawing_tool_plan_obj.rotation_euler
                # self.angle = 0
                self.action = str(self.action)+'_WORKING'
            elif 'ROTATE' in self.action and 'WORKING' in self.action and self.mouse_click:
                if self.shift_press:
                    self.slider_origine_x = event.mouse_region_x
                if self.shift_release:
                    self.slider_origine_x = event.mouse_region_x
                if self.shift_work:
                    increment = 10
                else:
                    increment = 45
                angle = round((self.slider_origine_x - event.mouse_region_x) / 100)*increment
                if self.angle != angle:
                    self.snap_support = 'PLANE'
                    if 'X' in self.action:
                        local_rotate(self.drawing_tool_plan_obj, 'X', self.angle * -1)
                        local_rotate(self.bool_obj, 'X', self.angle * -1)
                        self.angle = angle
                        local_rotate(self.drawing_tool_plan_obj, 'X', angle)
                        local_rotate(self.bool_obj, 'X', angle)
                        self.snap_refresh = True
                        self.drawing_tool_plan_obj['local_X_rotation'] = angle
                    elif 'Y' in self.action:
                        local_rotate(self.drawing_tool_plan_obj, 'Y', self.angle * -1)
                        local_rotate(self.bool_obj, 'Y', self.angle * -1)
                        self.angle = angle
                        local_rotate(self.drawing_tool_plan_obj, 'Y', angle)
                        local_rotate(self.bool_obj, 'Y', angle)
                        self.snap_refresh = True
                        self.drawing_tool_plan_obj['local_Y_rotation'] = angle
                    elif 'Z' in self.action:
                        local_rotate(self.drawing_tool_plan_obj, 'Z', self.angle * -1)
                        local_rotate(self.bool_obj, 'Z', self.angle * -1)
                        self.angle = angle
                        local_rotate(self.drawing_tool_plan_obj, 'Z', angle)
                        local_rotate(self.bool_obj, 'Z', angle)
                        self.snap_refresh = True
                        self.drawing_tool_plan_obj['local_Z_rotation'] = angle
            elif 'ROTATE' in self.action and 'WORKING' in self.action and not self.mouse_click:
                self.action = None
        except:pass

<<<<<<< HEAD
=======

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        # rotation du plan de dessin en vue d'un screw *************************************************************************
        if event.value == 'PRESS' and event.type =='A' and self.draw_type == 'poly':
            if self.screw_drawing :
                local_rotate(self.drawing_tool_plan_obj, 'X', -90)
                local_rotate(self.bool_obj, 'X', -90)
                self.screw_drawing = False
                self.snap_support = 'OBJECT'
            else:
                local_rotate(self.drawing_tool_plan_obj, 'X', 90)
                local_rotate(self.bool_obj, 'X', 90)
                self.screw_drawing = True
                self.snap_support = 'PLANE'
            self.snap_refresh = True

        # relance le dessin
        if event.value == 'PRESS' and event.type == 'W' and event.shift:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            context.area.tag_redraw()
            self.end_of_drawing('END')
            bpy.ops.wm.polydraw('INVOKE_DEFAULT')
            return{'FINISHED'}

        # Sortie du modal =======================================================================
        # =========================================================================================
        # =========================================================================================
        if ((event.value == 'PRESS' and event.type in {'RIGHTMOUSE'}) or get_addon_preferences().speedflow_fan) and self.build_step == 3 :
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            context.area.tag_redraw()
            self.end_of_drawing('END')
<<<<<<< HEAD

=======
            global polydraw_run
            polydraw_run = False
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            return {'FINISHED'}

        # Cancel *****************************************************************************
        if event.type == 'ESC':
<<<<<<< HEAD
=======
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            if tool_called == 'EDIT':
                bpy.context.object.display_type = self.old_display_style
                return {'CANCELLED'}
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            if bpy.data.objects.get("drawing_tool_plan_obj"):
                obj = bpy.data.objects.get("drawing_tool_plan_obj")
                bpy.ops.object.hide_view_set()
                objs = bpy.data.objects
                objs.remove(objs["drawing_tool_plan_obj"], do_unlink=True)
            if self.rebool_call and self.rebool_obj:
                objs = bpy.data.objects
                objs.remove(objs[self.rebool_obj.name], do_unlink=True)
            if self.bool_obj:
                objs = bpy.data.objects
                objs.remove(objs[self.bool_obj.name], do_unlink=True)
            bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
            if self.had_latest_bevel:
                latest_bevel_manager(self.original_bool_target, 'ADD')
                weighted_normals_manager(self.original_bool_target, 'ADD')
            # comme on travaillait sur une copie on la supprime et raffiche l'original
            if self.bool_target:
                bpy.data.objects.remove(self.bool_target, do_unlink=True)
                self.original_bool_target.hide_viewport = False
                self.original_bool_target.select_set(True)
                bpy.context.view_layer.objects.active = self.original_bool_target

<<<<<<< HEAD
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            return {'CANCELLED'}

        # Dessin ****************************************************************************************************

        if event.value == 'PRESS' and event.type == 'SPACE' and self.draw_type == 'poly' and self.build_step == 2:
            self.draw_type = 'path'
=======
            # global polydraw_run
            polydraw_run = False
            return {'CANCELLED'}

        # Dessin ****************************************************************************************************
        if event.value == 'PRESS' and event.type == 'RIGHTMOUSE' and self.screw_drawing and self.build_step == 2:
            self.draw_type = 'path'

            for m in self.meshes_names_to_clean:
                bpy.data.meshes.remove(bpy.data.meshes[m])

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete(type='ONLY_FACE')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            self.bool_obj.data.vertices[self.poly_count-1].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete(type='VERT')

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode='OBJECT')
            self.drawing_tool_plan_obj.hide_viewport = False
            bpy.ops.object.select_all(action='DESELECT')
            self.drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.delete()

            bpy.context.view_layer.objects.active = self.bool_obj
            self.bool_obj.select_set(True)

            self.add_modifiers(context, event, self.bool_obj)

            local_rotate(self.bool_obj, 'X', 90)
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
            bpy.ops.object.editmode_toggle()
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, False, False))
            bpy.ops.object.editmode_toggle()
            bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
            self.bool_obj.modifiers['Screw'].axis ='Z'
            self.draw_type = 'screw'
            self.bool_obj['fluent_type'] = 'screw'
            self.build_step = 3

        if event.value == 'PRESS' and event.type == 'SPACE' and self.draw_type == 'poly' and not self.screw_drawing and self.build_step == 2:
            self.draw_type = 'path'
            self.bool_obj['fluent_type'] = 'path'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete(type='ONLY_FACE')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            self.bool_obj.data.vertices[self.poly_count-1].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete(type='VERT')

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode='OBJECT')
            self.drawing_tool_plan_obj.hide_viewport = False
            bpy.ops.object.select_all(action='DESELECT')
            self.drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.delete()

            bpy.context.view_layer.objects.active = self.bool_obj
            self.bool_obj.select_set(True)

            self.add_modifiers(context, event, self.bool_obj)
<<<<<<< HEAD
            if not self.screw_drawing :
                self.item_hover = 1
=======
            self.item_hover = 1
            if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.build_step = 5
                self.x_mouse_slider_origin = event.mouse_region_x
                self.adjustment = 'SCREW'
                obj = bpy.context.active_object
                self.modifier_previous_value = self.bool_obj.modifiers['Screw'].screw_offset
            else:
<<<<<<< HEAD
                local_rotate(self.bool_obj, 'X', -90)
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                bpy.ops.object.editmode_toggle()
                bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, False, False))
                bpy.ops.object.editmode_toggle()
                bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
                self.bool_obj.modifiers['Screw'].axis ='Z'
                self.draw_type = 'screw'
                self.build_step = 3

        if event.value == 'PRESS' and event.type == 'RIGHTMOUSE' and self.draw_type == 'poly' and self.build_step == 2:
=======
                self.build_step = 3

        if event.value == 'PRESS' and event.type == 'RIGHTMOUSE' and self.draw_type == 'poly' and not self.screw_drawing and self.build_step == 2:
            self.bool_obj['fluent_type'] = 'poly'

            for m in self.meshes_names_to_clean:
                bpy.data.meshes.remove(bpy.data.meshes[m])

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            # replace le dernier vertice sur le precedent
            self.bool_obj.data.vertices[self.poly_count-1].co.x = self.bool_obj.data.vertices[self.poly_count].co.x
            self.bool_obj.data.vertices[self.poly_count-1].co.y = self.bool_obj.data.vertices[self.poly_count].co.y

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.mode_set(mode='OBJECT')
            self.drawing_tool_plan_obj.hide_viewport = False
            bpy.ops.object.select_all(action='DESELECT')
            self.drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.delete()

            bpy.context.view_layer.objects.active = self.bool_obj
            self.bool_obj.select_set(True)
            bpy.context.scene.cursor.location = (0, 0, 0)
            if not (self.drawing_tool_plan_obj['local_X_rotation'] or self.drawing_tool_plan_obj['local_Y_rotation'] or self.drawing_tool_plan_obj['local_Z_rotation']):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            self.add_modifiers(context, event, self.bool_obj)
            if bpy.context.scene.fluentProp.depth == 0:
                self.item_hover = 1
<<<<<<< HEAD
                self.build_step = 5

                self.x_mouse_slider_origin = event.mouse_region_x
                self.adjustment = 'FIRST_SOLIDIFY'
                obj = bpy.context.active_object
                self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
=======
                if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                    self.build_step = 5
                    self.x_mouse_slider_origin = event.mouse_region_x
                    self.adjustment = 'FIRST_SOLIDIFY'
                    obj = bpy.context.active_object
                    self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
                else:
                    self.build_step = 3

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            else:
                self.build_step = 3

        if (event.type == 'MOUSEMOVE' or (event.value == 'PRESS' and event.type == 'LEFTMOUSE')) and self.draw_type == 'poly' and self.build_step == 2 and not self.menu_hover:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.build_mesh_poly(context, event)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'poly' and self.build_step == 0.5 and not self.menu_hover:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.delta_click = self.cast['hit']
            for v in self.bool_obj.data.vertices:
                v.co.x = self.delta_click.x
                v.co.y = self.delta_click.y
            self.build_step = 2
            self.build_mesh_poly(context, event)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'poly' and self.build_step in {0, 1} and not self.menu_hover:
            self.snap_refresh = True
            if event.shift:
                self.build_step = 0.5
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                self.normal = self.cast['normal']
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_poly(context, event)
            else:
                self.build_step = 1
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                self.normal = self.cast['normal']
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_poly(context, event)

        if event.value == 'PRESS' and event.type == 'BACK_SPACE' and self.draw_type == 'poly' and self.build_step == 2 and not self.menu_hover:
            if self.poly_count < self.poly_count_origin:
                self.bool_obj.data.vertices[self.poly_count-1].co.x = self.bool_obj.data.vertices[0].co.x
                self.bool_obj.data.vertices[self.poly_count-1].co.y = self.bool_obj.data.vertices[0].co.y
                self.poly_count = self.poly_count + 1
                self.bool_obj.data.vertices[self.poly_count-1].co.x = self.cast['hit'].x
                self.bool_obj.data.vertices[self.poly_count-1].co.y = self.cast['hit'].y

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'box' and self.build_step == 2 and not self.menu_hover:
            self.build_step = 3
<<<<<<< HEAD
=======

            for m in self.meshes_names_to_clean:
                bpy.data.meshes.remove(bpy.data.meshes[m])

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.drawing_tool_plan_obj.hide_viewport = False
            bpy.ops.object.select_all(action='DESELECT')
            self.drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.delete()

            bpy.ops.object.select_all(action='DESELECT')
            if self.bool_target:
                self.bool_target.select_set(False)
            self.bool_obj.select_set(True)
            bpy.context.view_layer.objects.active = self.bool_obj

            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            self.add_modifiers(context, event, self.bool_obj)
            if bpy.context.scene.fluentProp.depth == 0:
<<<<<<< HEAD
                self.adjustment = 'FIRST_SOLIDIFY'
                self.build_step = 5
                self.x_mouse_slider_origin = event.mouse_region_x
                obj = bpy.context.active_object
                self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
=======
                if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                    self.adjustment = 'FIRST_SOLIDIFY'
                    self.build_step = 5
                    self.x_mouse_slider_origin = event.mouse_region_x
                    obj = bpy.context.active_object
                    self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
                else:
                    self.build_step = 3
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            else:
                self.build_step = 3

        if event.type == 'MOUSEMOVE' and self.draw_type == 'box' and self.build_step == 2:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.build_mesh_quad_plan(context, event)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'box' and self.build_step == 0.5 and not self.menu_hover:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.delta_click = self.cast['hit']
            self.build_step = 2

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'box' and self.build_step in {0, 1} and self.bool_target and not self.menu_hover:
            self.snap_refresh = True
            if event.shift:
                self.build_step = 0.5
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                self.normal = self.cast['normal']
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_quad_plan(context, event)
            else:
                self.build_step = 1
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                self.normal = self.cast['normal']
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_quad_plan(context, event)
                bpy.ops.object.select_all(action='DESELECT')
                self.bool_obj.select_set(True)
                bpy.context.view_layer.objects.active = self.bool_obj

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'box' and self.build_step in {0, 1} and not self.bool_target and not self.menu_hover:
            self.build_step = 1
            self.fake_obj()
            if not bpy.data.objects.get("drawing_tool_plan_obj"):
                self.make_plan_tool(context, event, self.bool_target)
            self.build_mesh_quad_plan(context, event)
            bpy.ops.object.select_all(action='DESELECT')
            self.bool_obj.select_set(True)
            bpy.context.view_layer.objects.active = self.bool_obj

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'prism' and self.build_step == 2 and not self.menu_hover:
            self.build_step = 3
<<<<<<< HEAD
=======

            for m in self.meshes_names_to_clean:
                bpy.data.meshes.remove(bpy.data.meshes[m])

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.drawing_tool_plan_obj.hide_viewport = False
            bpy.ops.object.select_all(action='DESELECT')
            self.drawing_tool_plan_obj.select_set(True)
            bpy.ops.object.delete()
            self.add_modifiers(context, event, self.bool_obj)
            if bpy.context.scene.fluentProp.depth == 0:
<<<<<<< HEAD
                self.build_step = 5
                self.x_mouse_slider_origin = event.mouse_region_x
                self.adjustment = 'FIRST_SOLIDIFY'
                obj = bpy.context.active_object
                self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
=======
                if self.get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                    self.build_step = 5
                    self.x_mouse_slider_origin = event.mouse_region_x
                    self.adjustment = 'FIRST_SOLIDIFY'
                    obj = bpy.context.active_object
                    self.modifier_previous_value = self.bool_obj.modifiers['First_Solidify'].thickness
                else:
                    self.build_step = 3
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            else:
                self.build_step = 3

        if event.type == 'MOUSEMOVE' and self.draw_type == 'prism' and self.build_step == 2:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.build_mesh_prism(context, event)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'prism' and self.build_step == 0.5 and not self.menu_hover:
            self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.drawing_tool_plan_obj, reference = 'LOCAL')
            self.delta_click = self.cast['hit']
            self.build_step = 2

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.draw_type == 'prism' and self.build_step in {0, 1} and not self.menu_hover:
            self.snap_refresh = True
            if event.shift:
                self.build_step = 0.5
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_prism(context, event)
            else:
                self.build_step = 1
                self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.bool_target, reference = 'WORLD')
                if not bpy.data.objects.get("drawing_tool_plan_obj"):
                    self.make_plan_tool(context, event, self.bool_target)
                self.build_mesh_prism(context, event)

        if event.value == 'PRESS' and event.type == 'X' and event.shift and self.build_step in {0, 0.5, 1, 2}:
            if bpy.data.objects.get("drawing_tool_plan_obj"):
                drawing_tool_plan_obj = bpy.data.objects.get("drawing_tool_plan_obj")
                drawing_tool_plan_obj.rotation_euler.x = math.radians(90)
                drawing_tool_plan_obj.rotation_euler.y = 0
                drawing_tool_plan_obj.rotation_euler.z = 0
                self.bool_obj.rotation_euler.x = math.radians(90)
                self.bool_obj.rotation_euler.y = 0
                self.bool_obj.rotation_euler.z = 0
                self.snap_refresh = True
                self.snap_display = 'NOTHING'
        if event.value == 'PRESS' and event.type == 'Y' and event.shift and self.build_step in {0, 0.5, 1, 2}:
            if bpy.data.objects.get("drawing_tool_plan_obj"):
                drawing_tool_plan_obj = bpy.data.objects.get("drawing_tool_plan_obj")
                drawing_tool_plan_obj.rotation_euler.x = 0
                drawing_tool_plan_obj.rotation_euler.y = math.radians(90)
                drawing_tool_plan_obj.rotation_euler.z = 0
                self.bool_obj.rotation_euler.x = 0
                self.bool_obj.rotation_euler.y = math.radians(90)
                self.bool_obj.rotation_euler.z = 0
                self.snap_refresh = True
                self.snap_display = 'NOTHING'
        if event.value == 'PRESS' and event.type == 'Z' and event.shift and self.build_step in {0, 0.5, 1, 2}:
            if bpy.data.objects.get("drawing_tool_plan_obj"):
                drawing_tool_plan_obj = bpy.data.objects.get("drawing_tool_plan_obj")
                drawing_tool_plan_obj.rotation_euler.x = 0
                drawing_tool_plan_obj.rotation_euler.y = 0
                drawing_tool_plan_obj.rotation_euler.z = math.radians(90)
                self.bool_obj.rotation_euler.x = 0
                self.bool_obj.rotation_euler.y = 0
                self.bool_obj.rotation_euler.z = math.radians(90)
                self.snap_refresh = True
                self.snap_display = 'NOTHING'

        return {'RUNNING_MODAL'}

    def end_of_drawing(self, action = 'END'):
<<<<<<< HEAD
=======
        if tool_called == 'EDIT':
            bpy.context.object.display_type = self.old_display_style
            global polydraw_run
            polydraw_run = False
            return {'FINISHED'}

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if bpy.data.objects.get("drawing_tool_plan_obj"):
            self.bool_obj['local_X_rotation'] = self.drawing_tool_plan_obj['local_X_rotation']
            self.bool_obj['local_Y_rotation'] = self.drawing_tool_plan_obj['local_Y_rotation']
            self.bool_obj['local_Z_rotation'] = self.drawing_tool_plan_obj['local_Z_rotation']
            objs = bpy.data.objects
            objs.remove(objs["drawing_tool_plan_obj"], do_unlink=True)

        # repercute le boolean sur l'original
        if not self.mesh_maker_call and not self.rebool_call:
            # on travaillait sur la copy donc on répercute sur l'original
            modif = self.original_bool_target.modifiers.new(type='BOOLEAN', name='Boolean')
            modif.operation = self.bool_operation
            modif.object = self.bool_obj
            modif.show_expanded = False

            if action == 'END':
                # detruit la copie
                bpy.data.objects.remove(self.bool_target, do_unlink=True)

            # raffiche et selectionne l'original
            self.original_bool_target.hide_viewport = False
            self.original_bool_target.select_set(True)
            self.original_bool_target.data.use_auto_smooth = True
            bpy.context.view_layer.objects.active = self.original_bool_target

            # parente l'original avec le bool
            self.bool_obj.select_set(True)
            self.original_bool_target.select_set(True)
            if get_addon_preferences().auto_parent:
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        if self.rebool_call:
            # on travaillait sur la copy donc on répercute sur l'original
            modif = self.original_bool_target.modifiers.new(type='BOOLEAN', name='Boolean')
            modif.operation = 'DIFFERENCE'
            modif.object = self.bool_obj
            modif.show_expanded = False
            # set le mirror sur l'original
            self.bool_obj.modifiers['Mirror'].mirror_object = self.original_bool_target

            # detruit la copie
            bpy.data.objects.remove(self.bool_target, do_unlink=True)

            # raffiche et selectionne l'original
            self.original_bool_target.hide_viewport = False
            self.original_bool_target.select_set(True)
            self.original_bool_target.data.use_auto_smooth = True

            # selectionne et copie l'original pour finir le rebool
            bpy.ops.object.select_all(action='DESELECT')
            self.original_bool_target.select_set(True)
            bpy.context.view_layer.objects.active = self.original_bool_target
            bpy.ops.object.duplicate()
            the_copy = bpy.context.active_object
            the_copy.data.use_auto_smooth = True
            the_copy['fluent_sliced'] = True
            the_copy.select_set(False)

            # change le dernier boolean en INTERSECT
            the_copy.modifiers[len(the_copy.modifiers)-1].operation = 'INTERSECT'

            # Supprime le rebool de travail qui est une copie
            bpy.data.objects.remove(self.rebool_obj, do_unlink=True)

            # parente l'original avec le bool
            self.bool_obj.select_set(True)
            self.original_bool_target.select_set(True)
            bpy.context.view_layer.objects.active = self.original_bool_target
            if get_addon_preferences().auto_parent:
<<<<<<< HEAD
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                self.bool_obj.select_set(False)
                the_copy.select_set(False)
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        if not self.mesh_maker_call:
=======
                the_copy.select_set(True)
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                the_copy.select_set(False)

        if not self.mesh_maker_call:
            if self.original_bool_target.data.use_auto_smooth:
                self.bool_obj.data.use_auto_smooth = True
            if self.original_bool_target.data.polygons[0].use_smooth:
                for p in self.bool_obj.data.polygons:
                    p.use_smooth = True

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.bool_obj.hide_render = True
            if get_addon_preferences().auto_hide_bool:
                self.bool_obj.hide_viewport = True
            self.bool_obj.color = (0, 0.649, 1, 0.25)
            # self.bool_obj.color = (0, 0.33, 1, 0.25)
            if not bpy.context.space_data.shading.type in {'MATERIAL', 'RENDERED'}:
                bpy.context.space_data.shading.color_type = 'OBJECT'
            self.bool_obj.display_type = get_addon_preferences().bool_style
            self.bool_obj.show_wire = False
            self.original_bool_target.hide_viewport = False
            if action == 'END':
                if not get_addon_preferences().bool_select_after:
                    self.bool_obj.select_set(False)
                    self.original_bool_target.select_set(True)
                    bpy.context.view_layer.objects.active = self.original_bool_target
                else:
                    self.bool_obj.select_set(True)
                    self.original_bool_target.select_set(False)
                    bpy.context.view_layer.objects.active = self.bool_obj
            # replace le latest bevel à la fin
            if self.had_latest_bevel:
                latest_bevel_manager(self.original_bool_target, 'ADD')
                weighted_normals_manager(self.original_bool_target, 'ADD')
            if self.rebool_call:
                if self.had_latest_bevel:
                    latest_bevel_manager(the_copy, 'ADD')
                    weighted_normals_manager(the_copy, 'ADD')
            bpy.data.collections['Bool_Objects'].objects.link(self.bool_obj)
<<<<<<< HEAD
            bpy.context.scene.collection.objects.unlink(self.bool_obj)
=======
            try:
                bpy.context.scene.collection.objects.unlink(self.bool_obj)
            except:pass
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.bool_obj['fluent_bool_object'] = True
        else:
            self.bool_obj.show_wire = False
            self.bool_obj.select_set(True)
            bpy.context.view_layer.objects.active = self.bool_obj
<<<<<<< HEAD
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            self.bool_obj['fluent_object'] = True
            # creer la collection si non existante
            # if not bpy.data.collections.get('Fluent_Creation'):
            #     coll = bpy.data.collections.new("Fluent_Creation")
            #     bpy.context.scene.collection.children.link(coll)
=======
            # bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            self.bool_obj['fluent_object'] = True
            for m in self.bool_obj.modifiers:
                m.show_expanded = False
            # creer la collection si non existante
            if not bpy.data.collections.get('Fluent_Creations'):
                coll = bpy.data.collections.new("Fluent_Creations")
                bpy.context.scene.collection.children.link(coll)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            bpy.data.collections['Fluent_Creations'].objects.link(self.bool_obj)
            bpy.context.scene.collection.objects.unlink(self.bool_obj)
            if self.bool_target:
                # detruit la copie
                bpy.data.objects.remove(self.bool_target, do_unlink=True)
                # raffiche et selectionne l'original
                self.original_bool_target.hide_viewport = False
                if self.had_latest_bevel:
                    latest_bevel_manager(self.original_bool_target, 'ADD')
                    weighted_normals_manager(self.original_bool_target, 'ADD')

        if get_addon_preferences().remove_unused_modifiers:
            for m in self.bool_obj.modifiers:
                if not m.show_render:
                    self.bool_obj.modifiers.remove(m)

        if self.empty_mirror:
            # parente l'original avec l'empty
            self.empty_mirror.select_set(True)
            self.original_bool_target.select_set(True)
            bpy.context.view_layer.objects.active = self.original_bool_target
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            self.empty_mirror.select_set(False)

        if action == 'RELAUNCH':
            self.original_bool_target.hide_viewport = True

    def reset_draw(self, context, event, save_bool = False):
        if bpy.data.objects.get("drawing_tool_plan_obj"):
            try:
                y_rotation = self.drawing_tool_plan_obj['local_Y_rotation']
                x_rotation = self.drawing_tool_plan_obj['local_X_rotation']
                z_rotation = self.drawing_tool_plan_obj['local_Z_rotation']
            except:
                y_rotation = 0
                x_rotation = 0
            objs = bpy.data.objects
            objs.remove(objs["drawing_tool_plan_obj"], do_unlink=True)
        if self.bool_obj and not save_bool:
            objs = bpy.data.objects
            objs.remove(objs[self.bool_obj.name], do_unlink=True)
        self.normal = None
        self.face_index = 0
        self.delta_click = None
        self.build_step = 1

        # self.snap_display = 'NOTHING'
        # self.snap_vert_coord_list = []
        # self.snap_calculated_coord_list = []
        # self.snap_resolution = 5
        # self.snap_refresh = False

        self.verts = []
        self.draw_from_out = False
        self.bool_obj_verts = []
        self.bool_obj = None
        self.poly_count = 24
        # self.screw_drawing = False

        if self.bool_target:
            self.bool_target.select_set(True)
            context.view_layer.objects.active = self.bool_target
            if self.snap_display != 'NOTHING':
                self.build_step = 0.5
                self.cast = self.save.copy()
                self.normal = self.cast['normal']
                self.make_plan_tool(context, event, self.bool_target)
                if self.draw_type == 'box':
                    self.build_mesh_quad_plan(context, event)
                elif self.draw_type == 'poly':
                    self.build_mesh_poly(context, event)
                elif self.draw_type == 'prism':
                    self.build_mesh_prism(context, event)
                try:
                    local_rotate(self.drawing_tool_plan_obj, 'X', x_rotation)
                    local_rotate(self.bool_obj, 'X', x_rotation)
                    local_rotate(self.drawing_tool_plan_obj, 'Y', y_rotation)
                    local_rotate(self.bool_obj, 'Y', y_rotation)
                    local_rotate(self.drawing_tool_plan_obj, 'Z', z_rotation)
                    local_rotate(self.bool_obj, 'Z', z_rotation)
                    self.drawing_tool_plan_obj['local_Y_rotation'] = y_rotation
                    self.drawing_tool_plan_obj['local_X_rotation'] = x_rotation
                    self.drawing_tool_plan_obj['local_Z_rotation'] = z_rotation
                except:pass

        if self.mesh_maker_call and not self.bool_target:
            self.build_step = 0.5
            self.make_plan_tool(context, event, self.bool_target)
            if self.draw_type == 'box':
                self.build_mesh_quad_plan(context, event)
            elif self.draw_type == 'poly':
                self.build_mesh_poly(context, event)
            elif self.draw_type == 'prism':
                self.build_mesh_prism(context, event)

    def invoke(self, context, event):
        global tool_called
        if context.area.type == 'VIEW_3D':
            x = 60
            y = 100
            HIGHTLIGHT = (0.0, 0.643, 1, 1)
            WHITE = (1, 1, 1, 1)
            CR = "Carriage Return"
            self.screen_text = [("PolyDraw", WHITE), CR]
            args = (self, context)

            self.verts = []
            self.draw_from_out = False
            self.cast = None
            self.normal = None
            self.face_casted_position = None
            self.delta_click = None
            self.bool_obj_verts = []
            self.bool_obj = None
            self.bool_obj_location = [0, 0, 0]
            self.bool_target = None
            self.original_bool_target = None
            self.had_latest_bevel = False
            self.rebool_obj = None
            self.rebool_call = None
            self.mesh_maker_call = False
            self.face_index = 0
            self.drawing_tool_plan_verts = []
            self.drawing_tool_plan_obj = None
            self.plane_size = 10
            self.snap_display = 'NOTHING'
            self.snap_mode = 'DEFAULT'
            self.snap_align = False
            self.snap_vert_coord_list = []
            self.snap_calculated_coord_list = []
            self.snap_resolution = get_addon_preferences().grid_resolution
            self.snap_refresh = False
            self.snap_extend = True
            self.snap_zoom = get_addon_preferences().grid_size
            self.snap_support = 'OBJECT'
            self.angle = 0
            self.old_rotation = 0
            self.out_of_grid = 8
            # 1 : pas commencé; 2 : dessin en cours; 3 : ajustement; 4 : ajustement en cours
            self.build_step = 1
<<<<<<< HEAD
=======
            self.enter_value = 'None'
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            self.bool_operation = 'DIFFERENCE'
            self.draw_type = 'box'
            self.screw_drawing = False
            self.prism_radius = 0
            self.prism_steps = bpy.context.scene.fluentProp.prism_segments
            self.poly_count = 24
            self.poly_count_origin = 24
            self.adjustment = ''
            self.x_mouse_slider_origin = 0
            self.y_mouse_slider_origin = 0
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
            self.mouse_back_position = [0, 0]
            self.mouse_click = False
            self.shift_press = False
            self.shift_release = False
            self.shift_work = False
            self.ctrl_press = False
            self.ctrl_release = False
            self.ctrl_work = False
            self.delta_hit = None
            self.face_normal = None
            self.mouse_move = False
            self.adjustement_menu_lock = [False, [0, 0]]
            self.item_hover = 0
            self.modifier_previous_value = 0
            self.array_axis = ''
            self.other_adjustement = False
            self.empty_obj = None
            self.empty_mirror = None
            self.empty_matrix_save = None
            self.empty_origin = None

<<<<<<< HEAD
=======
            self.meshes_names_to_clean = []

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            self.save = None

            self.display_menu = None
            self.action = None
            self.menu_hover = False

            self.box_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.box_menu.add_block('modifiers')
            self.box_menu.add_item('modifiers', 'FIRST_SOLIDIFY', 'Solidify', 'BUTTON','FIRST_SOLIDIFY')
            self.box_menu.add_item('modifiers', 'FIRST_BEVEL', 'First Bevel', 'BUTTON','FIRST_BEVEL')
            self.box_menu.add_item('modifiers', 'SECOND_BEVEL', 'Second Bevel', 'BUTTON','SECOND_BEVEL')
            self.box_menu.add_item('modifiers', 'MIRROR', 'Mirror', 'BUTTON','MIRROR')
            self.box_menu.add_item('modifiers', 'ARRAY', 'Array', 'BUTTON','ARRAY')
            self.box_menu.add_item('modifiers', 'SYMETRIZE', 'Symetrize', 'BUTTON','SYMETRIZE')
            self.box_menu.add_item('modifiers', 'SECOND_SOLIDIFY', 'Second Solidify', 'BUTTON','SECOND_SOLIDIFY')
            self.box_menu.add_item('modifiers', 'CIRCULAR_ARRAY', 'Circular Array', 'BUTTON','CIRCULAR_ARRAY')

            self.poly_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.poly_menu.add_block('modifiers')
            self.poly_menu.add_item('modifiers', 'FIRST_SOLIDIFY', 'Solidify', 'BUTTON','FIRST_SOLIDIFY')
            self.poly_menu.add_item('modifiers', 'FIRST_BEVEL', 'First Bevel', 'BUTTON','FIRST_BEVEL')
            self.poly_menu.add_item('modifiers', 'SECOND_BEVEL', 'Second Bevel', 'BUTTON','SECOND_BEVEL')
            self.poly_menu.add_item('modifiers', 'MIRROR', 'Mirror', 'BUTTON','MIRROR')
            self.poly_menu.add_item('modifiers', 'ARRAY', 'Array', 'BUTTON','ARRAY')
            self.poly_menu.add_item('modifiers', 'SYMETRIZE', 'Symetrize', 'BUTTON','SYMETRIZE')
            self.poly_menu.add_item('modifiers', 'SECOND_SOLIDIFY', 'Second Solidify', 'BUTTON','SECOND_SOLIDIFY')
            self.poly_menu.add_item('modifiers', 'CIRCULAR_ARRAY', 'Circular Array', 'BUTTON','CIRCULAR_ARRAY')
            self.poly_menu.add_item('modifiers', 'SMOOTH', 'Curve', 'BUTTON','SMOOTH')

            self.prism_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.prism_menu.add_block('modifiers')
            self.prism_menu.add_item('modifiers', 'FIRST_SOLIDIFY', 'Solidify', 'BUTTON','FIRST_SOLIDIFY')
            self.prism_menu.add_item('modifiers', 'RADIUS', 'Radius', 'BUTTON','RADIUS')
            self.prism_menu.add_item('modifiers', 'RESOLUTION', 'Resolution', 'BUTTON','RESOLUTION')
            self.prism_menu.add_item('modifiers', 'SECOND_BEVEL', 'Second Bevel', 'BUTTON','SECOND_BEVEL')
            self.prism_menu.add_item('modifiers', 'MIRROR', 'Mirror', 'BUTTON','MIRROR')
            self.prism_menu.add_item('modifiers', 'ARRAY', 'Array', 'BUTTON','ARRAY')
            self.prism_menu.add_item('modifiers', 'SECOND_SOLIDIFY', 'Second Solidify', 'BUTTON','SECOND_SOLIDIFY')
            self.prism_menu.add_item('modifiers', 'CIRCULAR_ARRAY', 'Circular Array', 'BUTTON','CIRCULAR_ARRAY')

            self.path_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.path_menu.add_block('modifiers')
            self.path_menu.add_item('modifiers', 'SCREW', 'Depth/Height', 'BUTTON','FIRST_SOLIDIFY')
            self.path_menu.add_item('modifiers', 'FIRST_SOLIDIFY', 'Thickness', 'BUTTON','RADIUS')
            self.path_menu.add_item('modifiers', 'FIRST_BEVEL', 'First Bevel', 'BUTTON','FIRST_BEVEL')
            self.path_menu.add_item('modifiers', 'SECOND_BEVEL', 'Second Bevel', 'BUTTON','SECOND_BEVEL')
            self.path_menu.add_item('modifiers', 'MIRROR', 'Mirror', 'BUTTON','MIRROR')
            self.path_menu.add_item('modifiers', 'ARRAY', 'Array', 'BUTTON','ARRAY')
            self.path_menu.add_item('modifiers', 'CIRCULAR_ARRAY', 'Circular Array', 'BUTTON','CIRCULAR_ARRAY')

            self.screw_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.screw_menu.add_block('modifiers')
            self.screw_menu.add_item('modifiers', 'RESOLUTION', 'Resolution', 'BUTTON','RESOLUTION')
            self.screw_menu.add_item('modifiers', 'SECOND_BEVEL', 'Second Bevel', 'BUTTON','SECOND_BEVEL')
            self.screw_menu.add_item('modifiers', 'MIRROR', 'Mirror', 'BUTTON','MIRROR')
            self.screw_menu.add_item('modifiers', 'ARRAY', 'Array', 'BUTTON','ARRAY')
            self.screw_menu.add_item('modifiers', 'SECOND_SOLIDIFY', 'Second Solidify', 'BUTTON','SECOND_SOLIDIFY')
            self.screw_menu.add_item('modifiers', 'CIRCULAR_ARRAY', 'Circular Array', 'BUTTON','CIRCULAR_ARRAY')
<<<<<<< HEAD
=======
            self.screw_menu.add_item('modifiers', 'FLIP', 'Flip normal', 'BUTTON')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            self.grid_menu = F_Menu(event.mouse_region_x, event.mouse_region_y)
            self.grid_menu.add_block('grid')
            self.grid_menu.add_item('grid', '', 'Grid Menu', 'LABEL','')
            self.grid_menu.add_item('grid', 'RESOLUTION_UP', 'Resolution +', 'BUTTON','')
            self.grid_menu.add_item('grid', 'RESOLUTION_DOWN', 'Resolution -', 'BUTTON','')
            self.grid_menu.add_item('grid', 'ZOOM_IN', 'Scale +', 'BUTTON','')
            self.grid_menu.add_item('grid', 'ZOOM_OUT', 'Scale -', 'BUTTON','')
            self.grid_menu.add_item('grid', 'EXTEND', 'Extend grid', 'BUTTON','')
            self.grid_menu.add_item('grid', 'ROTATE_X', 'Rotate X', 'SLIDER','')
            self.grid_menu.add_item('grid', 'ROTATE_Y', 'Rotate Y', 'SLIDER','')
            self.grid_menu.add_item('grid', 'ROTATE_Z', 'Rotate Z', 'SLIDER','')
            self.grid_menu.add_item('grid', 'HIDE', 'Hide', 'BUTTON','')

            if not bpy.data.collections.get('Bool_Objects'):
                coll = bpy.data.collections.new("Bool_Objects")
                bpy.context.scene.collection.children.link(coll)

<<<<<<< HEAD
            if bpy.context.selected_objects:
                self.original_bool_target = bpy.context.active_object
                self.original_bool_target['fluent_object'] = True
                # self.bool_target = bpy.context.active_object
                # sauvegarde l'objet original
                # self.original_bool_target = self.bool_target
                # copie l'objet pour travailler sur la copie
                self.bool_target, self.had_latest_bevel, had_weighted_normals = duplicate_obj(self.original_bool_target)
                # if weighted_normals_manager(self.bool_target, 'CHECK'):
                #     weighted_normals_manager(self.bool_target, 'REMOVE')
                # bpy.ops.object.duplicate()
                # self.bool_target = bpy.context.active_object
                # if latest_bevel_manager(self.bool_target, True):
                #     had_latest_bevel = True
                #     latest_bevel_manager(self.bool_target, False, True)
                for p in self.bool_target.data.polygons:
                    p.use_smooth = False
                    # self.original_bool_target.data.use_auto_smooth = False
                # else:
                #     had_latest_bevel = False
                bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
                # applique les booleens
                # for m in self.bool_target.modifiers:
                #     if m.show_render:
                #         bpy.ops.object.modifier_apply(apply_as='DATA', modifier=m.name)
                #     else:
                #         self.bool_target.modifiers.remove(m)
=======
            if active_object('GET') and tool_called != 'EDIT':
                self.original_bool_target = bpy.context.active_object
                self.original_bool_target['fluent_object'] = True
                self.bool_target, self.had_latest_bevel, had_weighted_normals = duplicate_obj(self.original_bool_target)
                for p in self.bool_target.data.polygons:
                    p.use_smooth = False
                bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                # cache l'original
                self.original_bool_target.select_set(False)
                self.original_bool_target.hide_viewport = True
                self.bool_target.select_set(True)
                bpy.context.view_layer.objects.active = self.bool_target

<<<<<<< HEAD
                # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                if self.bool_target.get('fluent_sliced'):
                    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
                    bpy.ops.view3d.snap_cursor_to_selected()
                else:
                    bpy.context.scene.cursor.location = self.original_bool_target.location
                if tool_called == 'SLICE':
                    self.rebool_call = True
                else:
                    self.rebool_call = False
                if tool_called == 'CREATION':
                    self.mesh_maker_call = True
                else:
                    self.mesh_maker_call = False
<<<<<<< HEAD
            else:
=======
            elif not active_object('GET') and tool_called != 'EDIT':
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                # rien n'est selectionné
                if tool_called == 'CREATION':
                    if not bpy.data.collections.get('Fluent_Creations'):
                        coll = bpy.data.collections.new("Fluent_Creations")
                        bpy.context.scene.collection.children.link(coll)
                    self.mesh_maker_call = True
                    self.build_step = 0.5
                    self.snap_zoom = 1
                    self.make_plan_tool(context, event, None)
                    self.build_mesh_quad_plan(context, event)
                else:
                    bpy.context.window_manager.popup_menu(make_oops(['Select an object before to call a cut function.']), title="How to use ?", icon='ERROR')
                    return{'CANCELLED'}
<<<<<<< HEAD
=======
            elif active_object('GET') and tool_called == 'EDIT':
                if len(bpy.context.selected_objects) > 1:
                    bpy.context.window_manager.popup_menu(make_oops(['Select one boolean object.']), title="How to use ?", icon='ERROR')
                    return {'CANCELLED'}
                elif not active_object('GET').get('fluent_type'):
                    bpy.context.window_manager.popup_menu(make_oops(['Select a Fluent object.']), title="How to use ?", icon='ERROR')
                    return {'CANCELLED'}
                else:
                    self.bool_obj = active_object('GET')
                    for m in self.bool_obj.modifiers:
                        if m.name == 'Circular_Array':
                            self.empty_obj = m.offset_object
                            angle = 360 / self.bool_obj.modifiers['Circular_Array'].count
                            local_rotate(self.empty_obj, 'Z', angle * -1)
                            self.empty_matrix_save = self.empty_obj.matrix_world.copy()
                            local_rotate(self.empty_obj, 'Z', angle)
                    if bpy.context.object.display_type != 'TEXTURED':
                        bpy.context.object.display_type = 'WIRE'
                    self.old_display_style = bpy.context.object.display_type
                    self.build_step = 3
                    if self.bool_obj.get('fluent_type') == 'prism' or self.bool_obj.get('fluent_type') == 'semi-prism':
                        self.draw_type = 'prism'
                    elif self.bool_obj.get('fluent_type') == 'box':
                        self.draw_type = 'box'
                    elif self.bool_obj.get('fluent_type') == 'screw':
                        self.draw_type = 'screw'
                    elif self.bool_obj.get('fluent_type') == 'path':
                        self.draw_type = 'path'
                    elif self.bool_obj.get('fluent_type') == 'poly':
                        self.draw_type = 'poly'
            elif not active_object('GET') and tool_called == 'EDIT':
                bpy.context.window_manager.popup_menu(make_oops(['Select a Fluent object.']), title="How to use ?", icon='ERROR')
                return {'CANCELLED'}
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')
            self._handle_two = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            if self.get_view_orientation_from_matrix(context.space_data.region_3d.view_matrix) == 'UNDEFINED':
                context.region_data.view_perspective = 'PERSP'

            context.window_manager.modal_handler_add(self)
<<<<<<< HEAD
=======
            global polydraw_run
            polydraw_run = True
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

class symetrizeAPlan(bpy.types.Operator):
    """Symetrize a plan, doesn't make a seam"""
    bl_idname = "wm.symetrizeaplan"
    bl_label="Class Symetrize"
    bl_options = {'REGISTER', 'UNDO'}

    def sym(self,context):
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        self.old_normal = obj.data.polygons[0].normal
        old_x = self.old_normal.x
        old_y = self.old_normal.y
        old_z = self.old_normal.z

        bm = bmesh.new()
        bm.from_mesh( bpy.context.object.data )
        bm_save = bmesh.new()
        bm_save.from_mesh( bpy.context.object.data )

        #supp tous les vertex de l'autre coté
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            if self.axis == 'X':
                if self.direction == 'POSITIVE':
                    if vert.co.x < 0:
                        bm.verts.remove( vert )
                else:
                    if vert.co.x > 0:
                        bm.verts.remove( vert )
            if self.axis == 'Y':
                if self.direction == 'POSITIVE':
                    if vert.co.y < 0:
                        bm.verts.remove( vert )
                else:
                    if vert.co.y > 0:
                        bm.verts.remove( vert )
            if self.axis == 'Z':
                if self.direction == 'POSITIVE':
                    if vert.co.z < 0:
                        bm.verts.remove( vert )
                else:
                    if vert.co.z > 0:
                        bm.verts.remove( vert )

        bm.to_mesh( bpy.context.object.data )

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        if self.axis == 'X':
            if self.direction == 'POSITIVE':
                bpy.ops.mesh.symmetrize(direction='POSITIVE_X')
            else:
                bpy.ops.mesh.symmetrize(direction='NEGATIVE_X')

        if self.axis == 'Y':
            if self.direction == 'POSITIVE':
                bpy.ops.mesh.symmetrize(direction='POSITIVE_Y')
            else:
                bpy.ops.mesh.symmetrize(direction='NEGATIVE_Y')

        if self.axis == 'Z':
            if self.direction == 'POSITIVE':
                bpy.ops.mesh.symmetrize(direction='POSITIVE_Z')
            else:
                bpy.ops.mesh.symmetrize(direction='NEGATIVE_Z')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()

        test = obj.update_from_editmode()
        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            self.new_normal = obj.data.polygons[0].normal
            if round(self.new_normal.x,2) != round(old_x,2) or round(self.new_normal.y, 2) != round(old_y, 2) or round(self.new_normal.z, 2) != round(old_z, 2):
                obj.modifiers['First_Solidify'].offset = obj.modifiers['First_Solidify'].offset * (-1)
        except:
            bm_save.to_mesh( bpy.context.object.data )
            bpy.context.window_manager.popup_menu(make_oops(['You did a symetrize along wrong axis.','Exemple : if your drawing is in XZ plane you can\'t symetrize along Y axis but along X or Z axis.']), title="How to use ?", icon='ERROR')


        return{'FINISHED'}

<<<<<<< HEAD


=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        if event.value == 'PRESS' and event.type == 'X':
            self.axis = 'X'

        if event.value == 'PRESS' and event.type == 'Y':
            self.axis = 'Y'

        if event.value == 'PRESS' and event.type == 'Z':
            self.axis = 'Z'

<<<<<<< HEAD



=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and not event.shift:
            x, y = event.mouse_region_x, event.mouse_region_y
            region = context.region
            rv3d = context.space_data.region_3d
            vec = region_2d_to_location_3d(region, rv3d, (x, y), (0, 0, 0))

            if self.axis == 'Y' and vec.y >= 0 or self.axis == 'X' and vec.x >= 0 or self.axis == 'Z' and vec.z >= 0 :
<<<<<<< HEAD

=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.direction = 'POSITIVE'
            else:
                self.direction = 'NEGATIVE'

            self.sym(context)
<<<<<<< HEAD
=======
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
            return{'FINISHED'}


        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.axis = 'X'
        self.direction = 'POSITIVE'
        self.old_normal = None
        self.new_normal = None
        obj = bpy.context.active_object
        if obj:
            obj.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            bpy.context.window_manager.popup_menu(make_oops(['Select an object.']), title="How to use ?", icon='ERROR')
            return{'CANCELLED'}

class FLUENT_MT_subMenu_one(bpy.types.Menu):
    bl_label = "Fluent sub menu one"
    # bl_idname = "wm.fluent_mt_submenu_one"
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.booleansynchronization", text=translate.get(get_addon_preferences().language).get('synchBool'))
        layout.prop(context.scene.fluentProp, 'width', text=translate.get(get_addon_preferences().language).get('latestBevelWidth'))
        layout.prop(context.scene.fluentProp, 'latest_bevel_segments', text=translate.get(get_addon_preferences().language).get('latestBevelSegments'))
        layout.prop(context.scene.fluentProp, 'angle', text=translate.get(get_addon_preferences().language).get('angleLimit'))
        layout.prop(context.scene.fluentProp, 'depth', text=translate.get(get_addon_preferences().language).get('defaultDepth'))
        layout.prop(context.scene.fluentProp, 'corner', text=translate.get(get_addon_preferences().language).get('corner'))
        layout.prop(context.scene.fluentProp, 'bevel_resolution', text=translate.get(get_addon_preferences().language).get('bevelResolution'))
        layout.prop(context.scene.fluentProp, 'prism_segments', text=translate.get(get_addon_preferences().language).get('circleResolution'))

class FLUENT_MT_pie_menu(bpy.types.Menu):
    bl_label = "Fluent"
    # bl_idname = "wm.fluent_pie_menu"

    def __init__(self):
        global init_pref
        if init_pref:
            bpy.context.scene.fluentProp.corner = get_addon_preferences().corner_preference
            bpy.context.scene.fluentProp.bevel_resolution = get_addon_preferences().bevel_resolution_preference
            bpy.context.scene.fluentProp.prism_segments = get_addon_preferences().prism_segments_preference
            bpy.context.scene.fluentProp.width = get_addon_preferences().latest_bevel_width_preference
            init_pref = False

    def draw(self, context):
        global translate
        icons = load_icons()
        autocomplete_one_ico = icons.get("autocomplete_one")
        latest_bevel_ico = icons.get("latest_bevel")
        sym_ico = icons.get("sym")
        show_bool_ico = icons.get("show_bool")
        cut_ico = icons.get("cut")
        slice_ico = icons.get("slice")
        creation_ico = icons.get("creation")
        wireframe_ico = icons.get("wireframe")
        duplicate_ico = icons.get("duplicate")
        warning_ico = icons.get("warning")
        preset_ico = icons.get("preset")
<<<<<<< HEAD
=======
        edit_ico = icons.get("edit")
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

        layout = self.layout
        scn = context.scene

        pie = layout.menu_pie()

        # gauche
        box = pie.split().column()
        box.operator("class.cutcall", text=translate.get(get_addon_preferences().language).get('cutCall'), icon_value=cut_ico.icon_id)
        box.operator("class.slicecall", text=translate.get(get_addon_preferences().language).get('sliceCall'), icon_value=slice_ico.icon_id)
        box.operator("class.creationcall", text=translate.get(get_addon_preferences().language).get('createCall'), icon_value=creation_ico.icon_id)
<<<<<<< HEAD
=======
        if not get_addon_preferences().remove_unused_modifiers:
            box.operator("class.editcall", text=translate.get(get_addon_preferences().language).get('editCall'), icon_value=edit_ico.icon_id)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        box.operator("wm.boolinstance", text=translate.get(get_addon_preferences().language).get('duplicate'), icon_value=duplicate_ico.icon_id)

        # droite
        box = pie.split().column()
        if get_addon_preferences().need_updating:
            box.operator("class.openprefs", text="The new version of Fluent is available.", icon_value=warning_ico.icon_id)
        box.operator("wm.addlatestbevel", text=translate.get(get_addon_preferences().language).get('addLatestBevel'), icon_value=latest_bevel_ico.icon_id)
        box.operator("wm.symetrizeaplan", text=translate.get(get_addon_preferences().language).get('symetrizePlan'), icon_value=sym_ico.icon_id)
        box.operator("class.makepreset", text=translate.get(get_addon_preferences().language).get('makePreset'), icon_value=preset_ico.icon_id)
        box_two = box.box().column()
        row = box_two.row(align=True)
        row.label(text=translate.get(get_addon_preferences().language).get('autoMirror'))
        row.prop(context.scene.fluentProp, 'auto_mirror_x', text="X")
        row.prop(context.scene.fluentProp, 'auto_mirror_y', text="Y")
        row.prop(context.scene.fluentProp, 'auto_mirror_z', text="Z")
        box_two = box.box().column()
        box_two.menu("FLUENT_MT_subMenu_one", text=translate.get(get_addon_preferences().language).get('otherAdjustment'))

        # bas
        box = pie.split().column()
        box.operator("class.autocompleteone", text=translate.get(get_addon_preferences().language).get('autoComplete'), icon_value=autocomplete_one_ico.icon_id)
        box.operator("class.clean_boolean", text=translate.get(get_addon_preferences().language).get('cleanBooleanApplication'))
        # haut
        box = pie.split().column()
<<<<<<< HEAD
        box.operator("class.booleandisplay", text=translate.get(get_addon_preferences().language).get('booleanDisplay'), icon_value=show_bool_ico.icon_id)
        box.operator("class.wireframedisplay", text=translate.get(get_addon_preferences().language).get('wireframe'), icon_value=wireframe_ico.icon_id)

class CutCall(bpy.types.Operator):
=======
        box.operator("wm.technicaldisplay", text=translate.get(get_addon_preferences().language).get('technicalDisplay'))
        box.operator("wm.booleandisplay", text=translate.get(get_addon_preferences().language).get('booleanDisplay'), icon_value=show_bool_ico.icon_id)
        box.operator("wm.wireframedisplay", text=translate.get(get_addon_preferences().language).get('wireframe'), icon_value=wireframe_ico.icon_id)

class FLUENT_OT_CutCall(bpy.types.Operator):
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    "Substract or add matter"
    bl_idname = "class.cutcall"
    bl_label="Drawing Shape Cut/Add ops"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        global tool_called
<<<<<<< HEAD
        tool_called = 'CUT'
        bpy.ops.wm.polydraw('INVOKE_DEFAULT')
        return {'FINISHED'}

class SliceCall(bpy.types.Operator):
=======
        global polydraw_run
        tool_called = 'CUT'
        if not polydraw_run:
            bpy.ops.wm.polydraw('INVOKE_DEFAULT')
        return {'FINISHED'}

class FLUENT_OT_SliceCall(bpy.types.Operator):
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    "Slice your model"
    bl_idname = "class.slicecall"
    bl_label="Drawing Shape Slice ops"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        global tool_called
<<<<<<< HEAD
        tool_called = 'SLICE'
        bpy.ops.wm.polydraw('INVOKE_DEFAULT')
=======
        global polydraw_run
        tool_called = 'SLICE'
        if not polydraw_run:
            bpy.ops.wm.polydraw('INVOKE_DEFAULT')
        return {'FINISHED'}

class FLUENT_OT_EditCall(bpy.types.Operator):
    "Slice your model"
    bl_idname = "class.editcall"
    bl_label="editcall"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        global tool_called
        global polydraw_run
        tool_called = 'EDIT'
        if not polydraw_run:
            bpy.ops.wm.polydraw('INVOKE_DEFAULT')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        return {'FINISHED'}

class CreationCall(bpy.types.Operator):
    "Create a new mesh"
    bl_idname = "class.creationcall"
    bl_label="Drawing Shape Creation ops"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        global tool_called
        tool_called = 'CREATION'
        bpy.ops.wm.polydraw('INVOKE_DEFAULT')
        return {'FINISHED'}

class addLatestBevel(bpy.types.Operator):
    """Click : Add
Shift + Click : Remove"""
    bl_idname = "wm.addlatestbevel"
    bl_label="add latest bevel"
    bl_options={'REGISTER','UNDO'}

    def invoke(self, context, event):
<<<<<<< HEAD
=======
        if bpy.context.active_object.mode == 'EDIT':
            bpy.context.window_manager.popup_menu(make_oops(['This function work only in object mode.']), title="Info", icon='ERROR')
            return {'CANCELLED'}
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        if not event.shift:
            for obj in bpy.context.selected_objects:
                if not obj.type == 'MESH':
                    continue
                if not latest_bevel_manager(obj, 'CHECK'):
                    latest_bevel_manager(obj, 'ADD')
                    weighted_normals_manager(obj, 'ADD')
                    # passe tout les bool objects en shade smooth
                    if len(obj.modifiers):
                        for mod in obj.modifiers:
                            if mod.type == 'BOOLEAN':
                                ob = mod.object
                                for p in ob.data.polygons:
                                    p.use_smooth = True
        else:
            for obj in bpy.context.selected_objects:
                if not obj.type == 'MESH':
                    continue
                weighted_normals_manager(obj, 'REMOVE')
                latest_bevel_manager(obj, 'REMOVE')
                for mod in obj.modifiers:
                    if mod.type == 'BOOLEAN':
                        ob = mod.object
                        for p in ob.data.polygons:
                            p.use_smooth = False

        return{'FINISHED'}

class autoCompleteOne(bpy.types.Operator):
    """Complete your model.
Apply every modifiers except the latest bevel
Shift + Click also apply the latest bevel"""
    bl_idname = "class.autocompleteone"
    bl_label="autocomplete one"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        latest_bevel_obj_list = []
        fluent_object_list = []

        # liste tout les objets fluent parmi la selection
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and obj.get('fluent_object'):
                fluent_object_list.append(obj)

        # liste tout les bool_obj
        fluent_bool_object = []
        for obj in bpy.data.objects:
            if obj.get('fluent_bool_object'):
                fluent_bool_object.append(obj)

        # supp les latestbevel s'il y en a et# selectionne les objets fluent et applique tout les modifiers ajoute l'objet à latest_bevel_obj_list
        if not event.shift:
            for obj in fluent_object_list:
                if latest_bevel_manager(obj, 'CHECK'):
                    latest_bevel_obj_list.append(obj)
                    weighted_normals_manager(obj, 'REMOVE')
                    latest_bevel_manager(obj, 'REMOVE')

        # selectionne les objets fluent et applique tout les modifiers
        for obj in fluent_object_list:
            obj.select_set(True)
        bpy.ops.object.duplicate()
        bpy.ops.object.convert(target='MESH')

        # place les objets dans une collection dédiée
        if not bpy.data.collections.get('Completed'):
            coll = bpy.data.collections.new("Completed")
            bpy.context.scene.collection.children.link(coll)
        for o in bpy.context.selected_objects:
            try:
                bpy.data.collections['Completed'].objects.link(o)
            except:
                pass

        for o in bpy.data.collections['Completed'].objects:
            o.hide_render = False

        # supprime tous les objets qui servaient aux bools
        for obj in bpy.data.objects:
            obj.select_set(False)

        for obj in fluent_object_list:
            bpy.context.view_layer.objects.active = None
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.edges_select_sharp()
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.edges_select_sharp()
            bpy.ops.mesh.mark_sharp()
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)
            bpy.ops.wm.addlatestbevel('INVOKE_DEFAULT')

        for obj in latest_bevel_obj_list:
            latest_bevel_manager(obj, 'ADD')
            weighted_normals_manager(obj, 'ADD')
            bpy.ops.object.shade_smooth()
            obj['fluent_object'] = True

        return{'FINISHED'}

class fluentProp(bpy.types.PropertyGroup):

    def latestBevelUpdate(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                if obj.get('fluent_object') and latest_bevel_manager(obj, 'CHECK'):
                    if bpy.context.scene.fluentProp.width <= 0.02:
                        obj.modifiers[len(obj.modifiers)-2].width = bpy.context.scene.fluentProp.width
                    else:
                        obj.modifiers[len(obj.modifiers)-2].width = 0.02
                    obj.modifiers[len(obj.modifiers)-2].angle_limit = bpy.context.scene.fluentProp.angle * 0.0174532925
                    obj.modifiers[len(obj.modifiers)-2].segments = bpy.context.scene.fluentProp.latest_bevel_segments

    def bevelResolutionUpdate(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.get('fluent_object'):
                if len(obj.modifiers):
                    for mod in obj.modifiers:
                        if mod.type =='BEVEL':
                            if mod.segments > 1:
                                angle = math.sqrt(math.asin(min(mod.width, 1)))
                                segments = int(context.scene.fluentProp.bevel_resolution * (angle + (1 - math.cos(angle))))
<<<<<<< HEAD
                                if segments < 2 :
                                    segments = 2
=======
                                if segments < 4 :
                                    segments = 4
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                                mod.segments = segments

    def prismResolutionUpdate(self, context):
        for obj in bpy.context.scene.objects:
<<<<<<< HEAD
            if obj.type == 'MESH' and obj.get('fluent_cylinder'):
=======
            if obj.type == 'MESH' and obj.get('fluent_type') == 'prism':
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                if len(obj.modifiers):
                    for mod in obj.modifiers:
                        if mod.type =='SCREW':
                            if mod.steps >= 8:
                                mod.steps = context.scene.fluentProp.prism_segments
                                mod.render_steps = mod.steps

    width : bpy.props.FloatProperty(
		description = "Latest Bevel Width",
		name        = "Latest bevel width",
<<<<<<< HEAD
		default     = 0.005,
=======
		default     = 0.002,
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
		min         = 0,
		max         = 0.02,
		step        = 0.01,
		precision   = 4,
		update      = latestBevelUpdate
	)
    corner : bpy.props.FloatProperty(
		description = "Default Bevel Width",
		name        = "Default Bevel Width",
		default     = 0,
		min         = 0,
		max         = 10,
		step        = 0.01,
		precision   = 3
	)
    segments : bpy.props.FloatProperty(
		description = "Segments of latestest bevel",
		name        = "Segments",
		default     = 4,
		min         = 0,
		max         = 10,
		step        = 0.01,
		precision   = 3
	)
    angle : bpy.props.FloatProperty(
		description = "Angle limit of latestest bevel",
		name        = "Angle limit",
		default     = 30,
		min         = 0,
		max         = 180,
		step        = 1,
		precision   = 3,
		update      = latestBevelUpdate
	)
    latest_bevel_segments : bpy.props.IntProperty(
		description = "Latest Bevel Segments",
		name        = "Latest Bevel Segments",
<<<<<<< HEAD
		default     = 6,
=======
		default     = 4,
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
		min         = 0,
		max         = 64,
		step        = 1,
		update      = latestBevelUpdate
	)
    depth : bpy.props.FloatProperty(
		description = "Default Depth",
		name        = "Default Depth",
		default     = 0,
		min         = -100,
		max         = 100,
		step        = 0.01,
		precision   = 3
	)
    solidify_offset : bpy.props.FloatProperty(
		description = "solidify offset",
		name        = "solidify_offset",
		default     = 0,
		min         = -1,
		max         = 1,
		precision   = 4
	)
    prism_segments : bpy.props.IntProperty(
		description = "Default Prism Segment",
		name        = "Default Prism Segment",
		default     = 64,
		min         = 0,
		step        = 1,
		update      = prismResolutionUpdate
	)
    bevel_resolution : bpy.props.IntProperty(
		description = "Bevel Resolution",
		name        = "Bevel resolution",
		default     = 32,
		min         = 0,
		step        = 1,
		update      = bevelResolutionUpdate
	)
    auto_mirror_x : bpy.props.BoolProperty(
		description = "Auto Mirror X",
		name        = "X",
		default     = False
	)
    auto_mirror_y : bpy.props.BoolProperty(
		description = "Auto Mirror Y",
		name        = "Y",
		default     = False
	)
    auto_mirror_z : bpy.props.BoolProperty(
		description = "Auto Mirror Z",
		name        = "Z",
		default     = False
	)
    straight_bevel : bpy.props.BoolProperty(
		description = "straight_bevel",
		name        = "straight_bevel",
		default     = False
	)
    second_bevel_width : bpy.props.FloatProperty(
		description = "second_bevel_width",
		name        = "second_bevel_width",
		default     = 0,
		min         = 0,
		max         = 100
	)
    second_bevel_straight : bpy.props.BoolProperty(
		description = "second_bevel_straight",
		name        = "second_bevel_straight",
		default     = False
	)

class makePreset(bpy.types.Operator):
    """Make/Clear preset
Shift + Click : clear"""
    bl_idname = "class.makepreset"
    bl_label="Make/Clear preset"
    bl_options={'REGISTER','UNDO'}

    def invoke(self, context, event):
        obj = active_object('GET')
        if event.shift:
            preset_manager('RESET')
        else:
            if obj.get('fluent_object'):
                preset_manager('GET', obj)
        return{'FINISHED'}

class booleanDisplay(bpy.types.Operator):
    """Show/Hide boolean objects"""
<<<<<<< HEAD
    bl_idname = "class.booleandisplay"
=======
    bl_idname = "wm.booleandisplay"
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    bl_label="Show/Hide boolean objects"
    bl_options={'REGISTER','UNDO'}

    def execute(self, context):
        if bpy.context.active_object:
            bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
            if not bpy.context.space_data.shading.type in {'MATERIAL', 'RENDERED'}:
                bpy.context.space_data.shading.color_type = 'OBJECT'
            obj = bpy.context.active_object
            obj.select_set(False)
            bool_list = []

            for modif in obj.modifiers:
                if modif.type == 'BOOLEAN':
                    bool_list.append(modif.object)

            if len(bool_list):
                if bool_list[0].hide_viewport:
                    for bool_obj in bool_list:
                        bool_obj.select_set(True)
                        bool_obj.hide_viewport = False
<<<<<<< HEAD
                        # bpy.ops.object.hide_view_set()
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                        bool_obj.select_set(False)
                else:
                    for bool_obj in bool_list:
                        bool_obj.select_set(True)
<<<<<<< HEAD
                        # bpy.ops.object.hide_view_clear()
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                        bool_obj.hide_viewport = True
                        bool_obj.select_set(False)

                obj.select_set(True)

                bpy.context.view_layer.objects.active = obj
            else:
                bpy.context.window_manager.popup_menu(make_oops(['No boolean object detected for this mesh.']), title="Info", icon='ERROR')
        else:
            bpy.context.window_manager.popup_menu(make_oops(['No boolean object detected for this mesh.']), title="Info", icon='ERROR')

        return {'FINISHED'}

class booleanCleaner(bpy.types.Operator):
    """Clean unused boolean modifiers"""
    bl_idname = "wm.booleancleaner"
    bl_label="Boolean Cleaner"
    bl_options={'REGISTER','UNDO'}

    def cleanBoolPls(self, obj):
        for modif in obj.modifiers:
            if modif.type == 'BOOLEAN':
                if not modif.object:
                    if modif.operation == 'INTERSECT':
                        objs = bpy.data.objects
                        objs.remove(obj, do_unlink=True)
                        break
                    else:
                        obj.modifiers.remove(modif)

    def invoke(self, context, event):
        for obj in bpy.data.objects:
            self.cleanBoolPls(obj)
        return{'FINISHED'}

class FLUENT_OT_booleanInstance(bpy.types.Operator):
    """Duplicate boolean object
Shift + Click to extract"""
    bl_idname = "wm.boolinstance"
    bl_label="Boolean Instance"
    bl_options={'REGISTER','UNDO'}

    def extraction(self):
        obj = bpy.context.active_object
        bpy.ops.object.duplicate(linked=False)
        copy = bpy.context.active_object
        obj.select_set(False)
        copy.select_set(True)
        bpy.context.view_layer.objects.active = copy
        copy.color = (1, 1, 1, 1)
        copy.display_type = 'TEXTURED'
        cycles_visibility(True)

    def duplicate(self):
        obj = active_object('GET')
        if obj.get('fluent_id'):
            fluent_id = obj.get('fluent_id')
        else:
            fluent_id = 0
            for o in bpy.data.objects:
                if o.get('fluent_id'):
                    if fluent_id < o.get('fluent_id'):
                        fluent_id = o.get('fluent_id')
            fluent_id += 1
        obj['fluent_id'] = fluent_id
        has_displace, displace_position = has_modifier(obj, 'DISPLACE')
        has_array, array_position = has_modifier(obj, 'ARRAY', 'use_object_offset')
        if has_displace and has_array and displace_position < array_position:
            empty_source = obj.children[0]
            empty_source.hide_viewport = False
            empty_source.select_set(True)
            bpy.ops.object.duplicate(linked=True)
            empty_source.hide_viewport = True
            empty_source.select_set(False)
            for o in bpy.context.selected_objects:
                if o.type == 'EMPTY':
                    o.select_set(False)
                    o.hide_viewport = True
            copy = bpy.context.active_object
            obj.select_set(False)
            copy.select_set(False)
            copy['fluent_id'] = fluent_id
        else:
            bpy.ops.object.duplicate(linked=True)
            copy = bpy.context.active_object
            active_object(copy, 'SET')
            obj.select_set(False)
            copy.select_set(False)
            copy['fluent_id'] = fluent_id

        new_mod = self.parent.modifiers.new(name='Boolean_duplicated', type="BOOLEAN")
        new_mod.operation = self.bool_operation
        new_mod.object = copy
        new_mod.show_expanded = False

        if latest_bevel_manager(self.parent, 'CHECK'):
            latest_bevel_manager(self.parent, 'REPLACE')
        if weighted_normals_manager(self.parent, 'CHECK'):
            weighted_normals_manager(self.parent, 'REPLACE')

        copy.select_set(True)
        bpy.context.view_layer.objects.active = copy
        self.copy = copy

    def modal(self, context, event):
        if event.type == 'ESC':
            bpy.ops.transform.select_orientation(orientation='GLOBAL')
            bpy.ops.wm.tool_set_by_id(name="builtin.select", cycle=False, space_type='VIEW_3D')
            objs = bpy.data.objects
            objs.remove(self.copy, do_unlink=True)
            objs.remove(self.parent_copy, do_unlink=True)
            self.parent.hide_viewport = False
            self.parent.select_set(True)
            bpy.context.view_layer.objects.active = self.parent
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
            return {'CANCELLED'}

        obj = bpy.context.active_object
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y

        self.cast = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.parent_copy, 'WORLD')

        if self.cast['success']:
            self.snap_display = 'SPECIAL_POINTS'
            draw_callback_px(self, context)
            cast_two = obj_ray_cast(context, self.mouse_x, self.mouse_y, self.parent_copy, 'WORLD')
            if cast_two['success']:
                obj.location = cast_two['hit']
            if self.cast['normal'] != self.normal:
                self.snap_refresh = True
                self.normal = self.cast['normal']
                obj.rotation_mode='XYZ'
                obj.rotation_euler.x = 0
                obj.rotation_euler.y = 0
                obj.rotation_euler.z = 0
                Up=mathutils.Vector((0,0,1))
                norm=self.cast['normal']
                Qrot=norm.rotation_difference(Up)
                obj.rotation_mode='QUATERNION'
                obj.rotation_quaternion@=Qrot.inverted()
            else:
                self.snap_refresh = False
        else:
            self.snap_display = 'NOTHING'

        if event.value == 'PRESS' and event.type == 'LEFTMOUSE':
            self.duplicate()
        # rotation
        if event.value == 'PRESS' and event.type == 'Z':
            local_rotate(obj, 'Z', 45)
        if event.value == 'PRESS' and event.type == 'Y':
            local_rotate(obj, 'Y', 45)
        if event.value == 'PRESS' and event.type == 'X':
            local_rotate(obj, 'X', 45)
        # controle de la grille
        if event.value=='PRESS' and event.type == 'B':
            self.snap_resolution = self.snap_resolution + 1
            get_addon_preferences().grid_resolution = self.snap_resolution
            self.snap_refresh = True
        if event.value=='PRESS' and event.type == 'V':
            self.snap_resolution = self.snap_resolution - 1
            get_addon_preferences().grid_resolution = self.snap_resolution
            self.snap_refresh = True
        if event.value=='PRESS' and event.type == 'W':
            if self.snap_extend:
                self.snap_extend = False
            else:
                self.snap_extend = True
            self.snap_refresh = True
        # sortie du modal
        if event.value == 'PRESS' and event.type in {'RIGHTMOUSE'}:
            bpy.ops.transform.select_orientation(orientation='GLOBAL')
            bpy.ops.wm.tool_set_by_id(name="builtin.select", cycle=False, space_type='VIEW_3D')
            objs = bpy.data.objects
            objs.remove(self.copy, do_unlink=True)
            objs.remove(self.parent_copy, do_unlink=True)
            self.parent.hide_viewport = False
            self.parent.select_set(True)
            bpy.context.view_layer.objects.active = self.parent
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_two, 'WINDOW')
            if self.had_latest_bevel:
                latest_bevel_manager(self.parent, 'ADD')
                weighted_normals_manager(self.parent, 'ADD')
            bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
            return {'FINISHED'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_5', 'NUMPAD_7'}:
            return {'PASS_THROUGH'}

        self.screen_text = [("Fluent Dupicate Tool", WHITE)]
        self.screen_text.extend([CR, CR, ("KEYS", WHITE)])
        self.screen_text.extend([CR,('    Duplicate : Left Click', WHITE)])
        self.screen_text.extend([CR,('    Rotate : X / Y / Z', WHITE)])
        self.screen_text.extend([CR,('    Grid resolution (', WHITE), (str(self.snap_resolution - 1), HIGHTLIGHT), (') : V / B', WHITE)])
        # self.screen_text.extend([CR,('    Square divisions', WHITE), (' : N', WHITE)])
        self.screen_text.extend([CR,('    Extend grid : W', WHITE)])
        # self.screen_text.extend([CR,('    Hide grid : X', WHITE)])
        self.screen_text.extend([CR,CR,('    Exit : Right Click', WHITE)])
        self.screen_text.extend([CR,('    Cancel : Esc', WHITE)])

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # try:
        global WHITE
        self.snap_vert_coord_list=[]
        self.snap_calculated_coord_list=[]
        self.screw_drawing = False
        self.snap_refresh = True
        self.out_of_grid = 0
        self.snap_extend = True
        self.snap_resolution = get_addon_preferences().grid_resolution
        self.snap_mode = 'DEFAULT'
        self.snap_support = 'OBJECT'
        self.snap_align = False
        self.snap_display = 'SPECIAL_POINTS'
        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y
        self.shift_work = False
        self.bool_operation = None

        bpy.ops.transform.select_orientation(orientation='LOCAL')
        bpy.ops.wm.tool_set_by_id(name="builtin.rotate", cycle=False, space_type='VIEW_3D')

        obj = active_object('GET')
        self.first = obj
        if event.shift:
            self.extraction()
            return {'FINISHED'}
        else:
            if len(bpy.context.selected_objects) in {0, 1} or len(bpy.context.selected_objects) > 2:
                bpy.context.window_manager.popup_menu(make_oops(['First : select the main object','Second : select the boolean object']), title="Error", icon='ERROR')
                return {'FINISHED'}
            obj.rotation_mode='QUATERNION'
            # determine l'opération
            for o in bpy.data.objects:
                if o != obj:
                    for m in o.modifiers:
                        if m.type == 'BOOLEAN' and m.object == obj:
                            self.bool_operation = m.operation
                            break
            if self.bool_operation:
                parent = bpy.context.selected_objects[1]
<<<<<<< HEAD
=======
                if parent == obj: parent = bpy.context.selected_objects[0]
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
                self.parent = parent
                active_object(parent, 'SET')
                bpy.ops.wm.booleancleaner('INVOKE_DEFAULT')
                self.parent_copy, self.had_latest_bevel, had_weighted_normals = duplicate_obj(parent, True, False, False, True)
                self.bool_target = parent
                obj.select_set(True)
                parent.select_set(False)
                active_object(obj, 'SET')
                parent.hide_viewport = True
                self.cast = obj_ray_cast(context, mouse_x, mouse_y, self.parent_copy, 'WORLD')
                self.normal = self.cast['normal']

                args = (self, context)
                self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')
                self._handle_two = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
                context.window_manager.modal_handler_add(self)

                self.parent_copy.select_set(False)
                self.duplicate()

                return {'RUNNING_MODAL'}
            else:
                bpy.context.window_manager.popup_menu(make_oops(['First : select the main object','Second : select the boolean object']), title="How to use ?", icon='ERROR')
                bpy.ops.transform.select_orientation(orientation='GLOBAL')
                bpy.ops.wm.tool_set_by_id(name="builtin.select", cycle=False, space_type='VIEW_3D')
                return {'CANCELLED'}

class booleanSynchronization(bpy.types.Operator):
    """Synchronize boolean object"""
    bl_idname = "wm.booleansynchronization"
    bl_label="Boolean Synchronization"
    bl_options={'REGISTER','UNDO'}

    def invoke(self, context, event):
        obj = bpy.context.active_object
        if obj.get('fluent_id'):
            fluent_id = obj.get('fluent_id')
            for o in bpy.data.objects:
                if o.get('fluent_id') and o.get('fluent_id') == fluent_id and o != obj:
                    o.modifiers.clear()
                    o.select_set(True)
                    bpy.ops.object.make_links_data(type='MODIFIERS')
                    o.select_set(False)


        return {'FINISHED'}

class FLUENT_OT_autosupport(bpy.types.Operator):
    """Select the boolean object first and the main object after
Click : to make support
Shift + Click : each loose parts supports"""
    bl_idname = "class.clean_boolean"
    bl_label="Boolean support creation"
    bl_options = {'REGISTER', 'UNDO'}

    def cutterObj(self):
        height = .01
        vertices = [(-1, -1, -height), (-1, 1, -height), (1, 1, -height), (1, -1, -height),
                    (-1, -1, height), (-1, 1, height), (1, 1, height), (1, -1, height),
                    (-1, 0, -height), (1, 0, -height),
                    (-1, 0, height), (1, 0, height),
                    (0, -1, -height), (0, 1, -height),
                    (0, -1, height), (0, 1, height),
                    (0, 0, -height), (0, 0, height)]

        faces = [(0, 4, 10, 8), (8, 10, 5, 1), (1, 5, 15, 13), (13, 15, 6, 2), (2, 6, 11, 9), (9, 11, 7, 3), (3, 7, 14, 12), (12, 14, 4, 0),
        (4, 10, 17, 14), (10, 5, 15, 17), (17, 15, 6, 11), (14, 17, 11, 7), (0, 8, 16, 12), (8, 1, 13, 16), (16, 13, 2, 9), (12, 16, 9, 3),
        (8, 10, 17, 16), (16, 17, 11, 9), (12, 14, 17, 16), (16, 17, 15, 13)]

        mesh_data = bpy.data.meshes.new("cutter")
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()
        cutter_obj = bpy.data.objects.new("cutter", mesh_data)
        bpy.context.scene.collection.objects.link(cutter_obj)
        active_object(cutter_obj, 'SET')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        new_vert_group = bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()
        v_groups = bpy.context.active_object.vertex_groups
        v_groups[0].name = 'intersect'
        bpy.ops.object.mode_set(mode='OBJECT')

        return cutter_obj

    def execute(self, context):
        # self.obj = bpy.context.active_object
        bool_list = []
        cutter_list = []
        obj = bpy.context.active_object
        margin = 0.01

        if not obj:
            bpy.context.window_manager.popup_menu(make_oops(['First : select the boolean object', 'Second : select the main object']), title="Info", icon='ERROR')
            return {'CANCELLED'}

        # récupère la largeur du dernier bevel angle
        for m in obj.modifiers:
            if m.type == 'BEVEL' and m.limit_method == 'ANGLE':
                margin = m.width * 2 + 0.01

<<<<<<< HEAD
        print('margin : ' + str(margin))
=======
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        obj.select_set(False)

        for o in bpy.context.selected_objects:
            bool_list.append(o)
            o.select_set(False)

        for b in bool_list:
            multiparts = False
            bpy.ops.object.select_all(action='DESELECT')
            active_object(b, 'SET')
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            copy = active_object('GET')

            for m in copy.modifiers:
                if m.type != 'SOLIDIFY':
                    if m.show_render:
                        if m.type in {'MIRROR', 'ARRAY'} and m.show_render:
                            multiparts = True
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=m.name)
                    else:
                        copy.modifiers.remove(m)

            if multiparts and self.event.shift:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                subparts = bpy.context.selected_objects

                for s in subparts:
                    cutter = self.cutterObj()
                    cutter.select_set(True)
                    context.view_layer.objects.active = cutter
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    cutter.dimensions = s.dimensions
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    cutter.dimensions.x = cutter.dimensions.x + margin
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    cutter.dimensions.y = cutter.dimensions.y + margin
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    cutter.location = s.location
                    cutter.rotation_euler = s.rotation_euler
                    cutter_list.append(cutter)
                    cutter.select_set(False)
                    bpy.data.objects.remove(s, do_unlink=True)

            else:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                # bpy.ops.view3d.snap_cursor_to_selected()
                b.select_set(False)
                cutter = self.cutterObj()
                cutter.select_set(True)
                context.view_layer.objects.active = cutter
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                cutter.dimensions = copy.dimensions
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                cutter.dimensions.x = cutter.dimensions.x + margin
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                cutter.dimensions.y = cutter.dimensions.y + margin
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                cutter.location = copy.location
                cutter.rotation_euler = b.rotation_euler
                cutter_list.append(cutter)
                cutter.select_set(False)
                bpy.data.objects.remove(copy, do_unlink=True)

        for o in cutter_list:
            o.select_set(True)

        active_object(obj, 'SET')
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='intersect')
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.intersect()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group='intersect')
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')

        obj.select_set(False)

        context.view_layer.objects.active = bool_list[0]

        return{'FINISHED'}

    def invoke(self, context, event):
        self.event = event
        self.execute(context)
        return {'FINISHED'}

class wireframeDisplay(bpy.types.Operator):
    """Show/Hide wireframe"""
<<<<<<< HEAD
    bl_idname = "class.wireframedisplay"
=======
    bl_idname = "wm.wireframedisplay"
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    bl_label="Show/Hide wireframe"
    bl_options={'REGISTER','UNDO'}

    def invoke(self, context, event):
        if active_object('GET'):
            if bpy.context.object.show_wire == True:
                bpy.context.object.show_wire = False
                bpy.context.object.show_all_edges = False
            else:
                bpy.context.object.show_wire = True
                bpy.context.object.show_all_edges = True
        return{'FINISHED'}

<<<<<<< HEAD
=======
class FLUENT_OT_TechnicalDisplay(bpy.types.Operator):
    """Show/Hide wireframe + boolean objects"""
    bl_idname = "wm.technicaldisplay"
    bl_label="Show/Hide wireframe + boolean objects"
    bl_options={'REGISTER','UNDO'}
    def execute(self, context):
        bpy.ops.wm.wireframedisplay('INVOKE_DEFAULT')
        bpy.ops.wm.booleandisplay('INVOKE_DEFAULT')
        return {'FINISHED'}

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
class gumroadUpdate(bpy.types.Operator):
    """Link to Gumroad"""
    bl_idname = "class.gumroadupdate"
    bl_label="Link to Gumroad"

    def invoke(self, context, event):
        webbrowser.open('https://gumroad.com')
        return {'FINISHED'}

class bmUpdate(bpy.types.Operator):
    """Link to BlenderMarket"""
    bl_idname = "class.bmupdate"
    bl_label="Link to BlenderMarket"

    def invoke(self, context, event):
        webbrowser.open('https://www.blendermarket.com/')
        return {'FINISHED'}

class openPrefs(bpy.types.Operator):
    """Open preferences"""
    bl_idname = "class.openprefs"
    bl_label="Open preferences"
    def invoke(self, context, event):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.window_manager.addon_search = "fluent"
        return {'FINISHED'}

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    speedflow_fan : bpy.props.BoolProperty(
        name="speedflow_fan",
        default=False,
        description="Launch SpeedFlow after primitive creation"
    )

    corner_preference : bpy.props.FloatProperty(
		description = "Default Bevel Width",
		name        = "Default Bevel Width",
		default     = 0,
		min         = 0,
		max         = 10,
		step        = 0.01,
		precision   = 3
	)

    bevel_resolution_preference : bpy.props.IntProperty(
		description = "Bevel Resolution",
		name        = "Bevel resolution",
		default     = 32,
		min         = 0,
		step        = 1
	)

    latest_bevel_width_preference : bpy.props.FloatProperty(
		description = "Latest Bevel Width",
		name        = "Latest Bevel Width",
		default     = 0.003,
		min         = 0,
		step        = 0.001,
		precision   = 3
	)

    prism_segments_preference : bpy.props.IntProperty(
		description = "Default Prism Segment",
		name        = "Default Prism Segment",
		default     = 64,
		min         = 0,
		step        = 1
	)

<<<<<<< HEAD
    shortcut_key : bpy.props.EnumProperty(
=======
    fluent_menu_shortcut_key : bpy.props.EnumProperty(
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        items=(("A", "A", "A"),
        ("B", "B", "B"),
        ("C", "C", "C"),
        ("D", "D", "D"),
        ("E", "E", "E"),
        ("F", "F", "F"),
        ("G", "G", "G"),
        ("H", "H", "H"),
        ("I", "I", "I"),
        ("J", "J", "J"),
        ("K", "K", "K"),
        ("L", "L", "L"),
        ("M", "M", "M"),
        ("N", "N", "N"),
        ("O", "O", "O"),
        ("P", "P", "P"),
        ("Q", "Q", "Q"),
        ("R", "R", "R"),
        ("S", "S", "S"),
        ("T", "T", "T"),
        ("U", "U", "U"),
        ("V", "V", "V"),
        ("W", "W", "W"),
        ("X", "X", "X"),
        ("Y", "Y", "Y"),
        ("Z", "Z", "Z"),
        ),
<<<<<<< HEAD
        default='X'
    )

    shortcut_alt : bpy.props.BoolProperty(
        description = "Use alt to call Fluent",
        name = "Use alt to call Fluent",
        default = True
    )

    shortcut_ctrl : bpy.props.BoolProperty(
=======
        default='F'
    )

    fluent_menu_shortcut_alt : bpy.props.BoolProperty(
        description = "Use alt to call Fluent",
        name = "Use alt to call Fluent",
        default = False
    )

    fluent_menu_shortcut_ctrl : bpy.props.BoolProperty(
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        description = "Use ctrl to call Fluent",
        name = "Use ctrl to call Fluent",
        default = False
    )

<<<<<<< HEAD
    shortcut_shift : bpy.props.BoolProperty(
=======
    fluent_menu_shortcut_shift : bpy.props.BoolProperty(
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        description = "Use shift to call Fluent",
        name = "Use shift to call Fluent",
        default = False
    )

<<<<<<< HEAD
    bool_style : bpy.props.EnumProperty(
        items=(("WIRE", "WIRE", "WIRE"),
        ("TEXTURED", "TEXTURED", "TEXTURED")
=======
    fluent_cut_shortcut_key : bpy.props.EnumProperty(
        items=(("A", "A", "A"),
        ("B", "B", "B"),
        ("C", "C", "C"),
        ("D", "D", "D"),
        ("E", "E", "E"),
        ("F", "F", "F"),
        ("G", "G", "G"),
        ("H", "H", "H"),
        ("I", "I", "I"),
        ("J", "J", "J"),
        ("K", "K", "K"),
        ("L", "L", "L"),
        ("M", "M", "M"),
        ("N", "N", "N"),
        ("O", "O", "O"),
        ("P", "P", "P"),
        ("Q", "Q", "Q"),
        ("R", "R", "R"),
        ("S", "S", "S"),
        ("T", "T", "T"),
        ("U", "U", "U"),
        ("V", "V", "V"),
        ("W", "W", "W"),
        ("X", "X", "X"),
        ("Y", "Y", "Y"),
        ("Z", "Z", "Z"),
        ),
        default='F'
    )

    fluent_cut_shortcut_alt : bpy.props.BoolProperty(
        description = "Use alt to call Fluent cut",
        name = "fluent_cut_shortcut_alt",
        default = True
    )

    fluent_cut_shortcut_ctrl : bpy.props.BoolProperty(
        description = "Use ctrl to call Fluent cut",
        name = "fluent_cut_shortcut_ctrl",
        default = False
    )

    fluent_cut_shortcut_shift : bpy.props.BoolProperty(
        description = "Use shift to call Fluent cut",
        name = "fluent_cut_shortcut_shift",
        default = False
    )

    fluent_slice_shortcut_key : bpy.props.EnumProperty(
        items=(("A", "A", "A"),
        ("B", "B", "B"),
        ("C", "C", "C"),
        ("D", "D", "D"),
        ("E", "E", "E"),
        ("F", "F", "F"),
        ("G", "G", "G"),
        ("H", "H", "H"),
        ("I", "I", "I"),
        ("J", "J", "J"),
        ("K", "K", "K"),
        ("L", "L", "L"),
        ("M", "M", "M"),
        ("N", "N", "N"),
        ("O", "O", "O"),
        ("P", "P", "P"),
        ("Q", "Q", "Q"),
        ("R", "R", "R"),
        ("S", "S", "S"),
        ("T", "T", "T"),
        ("U", "U", "U"),
        ("V", "V", "V"),
        ("W", "W", "W"),
        ("X", "X", "X"),
        ("Y", "Y", "Y"),
        ("Z", "Z", "Z"),
        ),
        default='F'
    )

    fluent_slice_shortcut_alt : bpy.props.BoolProperty(
        description = "Use alt to call Fluent slice",
        name = "fluent_slice_shortcut_alt",
        default = False
    )

    fluent_slice_shortcut_ctrl : bpy.props.BoolProperty(
        description = "Use ctrl to call Fluent slice",
        name = "fluent_slice_shortcut_ctrl",
        default = True
    )

    fluent_slice_shortcut_shift : bpy.props.BoolProperty(
        description = "Use shift to call Fluent slice",
        name = "fluent_slice_shortcut_shift",
        default = False
    )

    fluent_edit_shortcut_key : bpy.props.EnumProperty(
        items=(("A", "A", "A"),
        ("B", "B", "B"),
        ("C", "C", "C"),
        ("D", "D", "D"),
        ("E", "E", "E"),
        ("F", "F", "F"),
        ("G", "G", "G"),
        ("H", "H", "H"),
        ("I", "I", "I"),
        ("J", "J", "J"),
        ("K", "K", "K"),
        ("L", "L", "L"),
        ("M", "M", "M"),
        ("N", "N", "N"),
        ("O", "O", "O"),
        ("P", "P", "P"),
        ("Q", "Q", "Q"),
        ("R", "R", "R"),
        ("S", "S", "S"),
        ("T", "T", "T"),
        ("U", "U", "U"),
        ("V", "V", "V"),
        ("W", "W", "W"),
        ("X", "X", "X"),
        ("Y", "Y", "Y"),
        ("Z", "Z", "Z"),
        ),
        default='F'
    )

    fluent_edit_shortcut_alt : bpy.props.BoolProperty(
        description = "Use alt to call Fluent edit",
        name = "fluent_edit_shortcut_alt",
        default = False
    )

    fluent_edit_shortcut_ctrl : bpy.props.BoolProperty(
        description = "Use ctrl to call Fluent edit",
        name = "fluent_edit_shortcut_ctrl",
        default = False
    )

    fluent_edit_shortcut_shift : bpy.props.BoolProperty(
        description = "Use shift to call Fluent edit",
        name = "fluent_edit_shortcut_shift",
        default = True
    )

    bool_style : bpy.props.EnumProperty(
        items=(("WIRE", "WIRE", "WIRE"),
        ("TEXTURED", "TEXTURED", "TEXTURED"),
        ('BOUNDS', 'BOUNDS', 'BOUNDS')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        ),
        default='TEXTURED'
    )

    language : bpy.props.EnumProperty(
    items=(
    ("ENGLISH", "English", "ENGLISH"),
    ("FRANCAIS", "Français", "FRANCAIS"),
    ("CHINESE", "Chinese", "CHINESE"),
<<<<<<< HEAD
=======
    ("TRAD_CHINESE", "Traditional Chinese", "TRAD_CHINESE"),
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    ("JAPANESE", "Japanese", "JAPANESE"),
    ),
    default='ENGLISH'
    )

    auto_hide_bool : bpy.props.BoolProperty(
        name="auto_hide_bool",
        default=True,
        description="Hide boolean object after creation"
    )

    bool_select_after : bpy.props.BoolProperty(
        name="auto_hide_bool",
        default=False,
        description="Hide boolean object after creation"
    )

    remove_unused_modifiers : bpy.props.BoolProperty(
<<<<<<< HEAD
        name="remove_unused_modifier",
=======
        name="remove_unused_modifiers",
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        default=False,
        description="Delete unused modifier on boolean object"
    )

    auto_parent : bpy.props.BoolProperty(
        name="auto_parent",
        default=True,
        description="Auto parent between the boolean object and his target"
    )

    need_updating : bpy.props.BoolProperty(
		description = "need updating",
		name        = "need_updating",
		default     = False
	)

    last_version : bpy.props.StringProperty(
		description = "last version",
		name        = "last_version",
		default     = "(1.0.6)"
	)

    grid_size : bpy.props.FloatProperty(
		description = "grid size",
		name        = "Grid Size",
		default     = 1,
		min         = 0,
		step        = 0.01,
		precision   = 2
	)

    grid_resolution : bpy.props.IntProperty(
		description = "grid resolution",
		name        = "Grid Resolution",
		default     = 4,
		min         = 0,
		step        = 1
	)

<<<<<<< HEAD
=======
    text_y_origin : bpy.props.IntProperty(
        description = "text_y_origin",
        name        = "text_y_origin",
        default     = 500,
        step        = 1
    )

    text_x_origin : bpy.props.IntProperty(
        description = "text_y_origin",
        name        = "text_y_origin",
        default     = 5,
        step        = 1
    )

    text_size : bpy.props.IntProperty(
        description = "text_size",
        name        = "text_size",
        default     = 18,
        step        = 1
    )

    hightlight : bpy.props.FloatVectorProperty(name="Hightlight color",
        subtype='COLOR',
        size=4,
        default=(0.0,0.8,1,1)
    )

>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    def draw(self, context):
        icons = load_icons()
        gumroad_ico = icons.get("gumroad")
        bm_ico = icons.get("bm")
        warning_ico = icons.get("warning")
        layout = self.layout
        if get_addon_preferences().need_updating:
            layout.label(text="The version " + get_addon_preferences().last_version + " is available !", icon_value=warning_ico.icon_id)
            # split = layout.split()
            row = layout.row()
            row.operator("class.gumroadupdate", text='GUMROAD', icon_value=gumroad_ico.icon_id)
            row.operator("class.bmupdate", text='BLENDERMARKET', icon_value=bm_ico.icon_id)

        box = layout.box()
        row = box.row()
<<<<<<< HEAD
        row.label(text="Shortcut")
        box.label(text="After change, save your preferences and restart Blender.")
        row.prop(self, "shortcut_key", text="Key ")
        row.prop(self, "shortcut_alt", text="Alt")
        row.prop(self, "shortcut_ctrl", text="Ctrl")
        row.prop(self, "shortcut_shift", text="Shift")
=======
        row.label(text="Menu shortcut")
        row.prop(self, "fluent_menu_shortcut_key", text="Key ")
        row.prop(self, "fluent_menu_shortcut_alt", text="Alt")
        row.prop(self, "fluent_menu_shortcut_ctrl", text="Ctrl")
        row.prop(self, "fluent_menu_shortcut_shift", text="Shift")
        row_2 = box.row()
        row_2.label(text='Cut shortcut')
        row_2.prop(self, "fluent_cut_shortcut_key", text="Key ")
        row_2.prop(self, "fluent_cut_shortcut_alt", text="Alt")
        row_2.prop(self, "fluent_cut_shortcut_ctrl", text="Ctrl")
        row_2.prop(self, "fluent_cut_shortcut_shift", text="Shift")
        row_3 = box.row()
        row_3.label(text='Slice shortcut')
        row_3.prop(self, "fluent_slice_shortcut_key", text="Key ")
        row_3.prop(self, "fluent_slice_shortcut_alt", text="Alt")
        row_3.prop(self, "fluent_slice_shortcut_ctrl", text="Ctrl")
        row_3.prop(self, "fluent_slice_shortcut_shift", text="Shift")
        row_4 = box.row()
        row_4.label(text='Edit shortcut')
        row_4.prop(self, "fluent_edit_shortcut_key", text="Key ")
        row_4.prop(self, "fluent_edit_shortcut_alt", text="Alt")
        row_4.prop(self, "fluent_edit_shortcut_ctrl", text="Ctrl")
        row_4.prop(self, "fluent_edit_shortcut_shift", text="Shift")
        box.label(text="After change, save your preferences and restart Blender.")
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
        layout.prop(self, "corner_preference", text="Default Bevel Width")
        layout.prop(self, "bevel_resolution_preference", text="Default Bevel Resolution")
        layout.prop(self, "prism_segments_preference", text="Default Prism Resolution")
        layout.prop(self, "latest_bevel_width_preference", text="Default latest bevel width")
        split = layout.split()
        col = split.column()
        col.label(text="Boolean object display style :")
        col = split.column(align=True)
        col.prop(self, 'bool_style', expand=True)
        layout.prop(self, "auto_hide_bool", text="Hide boolean object when Fluent is closed ")
        layout.prop(self, "bool_select_after", text="Selection boolean object instead of his target when Fluent is closed ")
        layout.prop(self, "remove_unused_modifiers", text="Remove unused modifiers of boolean object ")
        layout.prop(self, "auto_parent", text="Auto parent between the boolean object and his target ")
        layout.prop(self, "language", text="Language ")
        layout.label(text="Translation is in progress. Whole text isn't translated.")
<<<<<<< HEAD
=======
        layout.prop(self, "hightlight", text='Hightlight color')
        layout.prop(self, "text_size", text='Text size')
        layout.label(text='Text position on the screen')
        layout.prop(self, "text_x_origin", text='X')
        layout.prop(self, "text_y_origin", text='Y')
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

    def invoke(self, context, event):
        adresse = 'http://cgthoughts.com/fluent_current_version/index.html'
        response = urllib.request.urlopen(adresse)
        html = str(response.read())
        version = html[5:10]

classes = (
    PolyDraw,
<<<<<<< HEAD
    CutCall,
    SliceCall,
=======
    FLUENT_OT_CutCall,
    FLUENT_OT_SliceCall,
    FLUENT_OT_EditCall,
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    CreationCall,
    symetrizeAPlan,
    addLatestBevel,
    fluentProp,
    autoCompleteOne,
    booleanDisplay,
    FLUENT_MT_pie_menu,
    FLUENT_MT_subMenu_one,
    booleanCleaner,
    AddonPreferences,
    wireframeDisplay,
<<<<<<< HEAD
=======
    FLUENT_OT_TechnicalDisplay,
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
    FLUENT_OT_booleanInstance,
    booleanSynchronization,
    gumroadUpdate,
    bmUpdate,
    openPrefs,
    makePreset,
    FLUENT_OT_autosupport
)
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
<<<<<<< HEAD
    kmi = km.keymap_items.new("wm.call_menu_pie", get_addon_preferences().shortcut_key, "PRESS", alt=get_addon_preferences().shortcut_alt, shift=get_addon_preferences().shortcut_shift, ctrl=get_addon_preferences().shortcut_ctrl).properties.name="FLUENT_MT_pie_menu"
=======
    kmi = km.keymap_items.new("wm.call_menu_pie", get_addon_preferences().fluent_menu_shortcut_key, "PRESS", alt=get_addon_preferences().fluent_menu_shortcut_alt, shift=get_addon_preferences().fluent_menu_shortcut_shift, ctrl=get_addon_preferences().fluent_menu_shortcut_ctrl).properties.name="FLUENT_MT_pie_menu"
    kmi = km.keymap_items.new(FLUENT_OT_CutCall.bl_idname, get_addon_preferences().fluent_cut_shortcut_key, "PRESS", alt=get_addon_preferences().fluent_cut_shortcut_alt, shift=get_addon_preferences().fluent_cut_shortcut_shift, ctrl=get_addon_preferences().fluent_cut_shortcut_ctrl)
    kmi = km.keymap_items.new(FLUENT_OT_SliceCall.bl_idname, get_addon_preferences().fluent_slice_shortcut_key, "PRESS", alt=get_addon_preferences().fluent_slice_shortcut_alt, shift=get_addon_preferences().fluent_slice_shortcut_shift, ctrl=get_addon_preferences().fluent_slice_shortcut_ctrl)
    kmi = km.keymap_items.new(FLUENT_OT_EditCall.bl_idname, get_addon_preferences().fluent_edit_shortcut_key, "PRESS", alt=get_addon_preferences().fluent_edit_shortcut_alt, shift=get_addon_preferences().fluent_edit_shortcut_shift, ctrl=get_addon_preferences().fluent_edit_shortcut_ctrl)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d

    bpy.types.Scene.fluentProp = bpy.props.PointerProperty( type = fluentProp )

    try:
        check, version = check_update()
        if check:
            print('A new version of Fluent is available.')
            get_addon_preferences().need_updating = True
            get_addon_preferences().last_version = version
    except:
        get_addon_preferences().need_updating = False

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
