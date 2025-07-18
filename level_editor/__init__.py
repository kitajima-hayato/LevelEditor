import bpy

import copy
import mathutils



bl_info = {
    "name": "LevelEditor",
    "author": "Hayato Kitajima",
    "version": (1,0),
    "blender": (4,4),
    "location": "",
    "description": "LevelEditor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}

# モジュールのインポート
from .my_menu import TOPBAR_MT_my_menu
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .export_scene import MYADDON_OT_export_scene
from .file_name import OBJECT_PT_file_name, MYADDON_OT_add_filename
from .add_collider import MYADDON_OT_add_collider, OBJECT_PT_collider
from .draw_collider import DrawCollider


#blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    OBJECT_PT_file_name,
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
)

#Add On Startup callback
def register():
    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(
        DrawCollider.draw_collider,(),"WINDOW","POST_VIEW")
    print("レベルエディタが有効化")
    
#Add On Disable callback
def unregister():
    # メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    #3dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle,"WINDOW")

    # クラス登録解除
    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化")



#メニュー項目描画
def draw_menu_manual(self,context):
    #self : 呼び出し元のクラスインスタンス。thisポインタのような扱い
    #context : カーソルを合わせたときのポップアップのカスタマイズに使用する
    #トップバーの[エディターメニュー]に項目(オペレーター)を追加
    self.layout.operator("wm.url_open_preset",text="Manual",icon='HELP')




        