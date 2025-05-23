import bpy
import math
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

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]

    #サブメニューの描画
    def draw(self,context):
        #トップバーの「エディターメニュー」に項目を追加（オペレーターを追加）
        self.layout.operator("wm.url_open_preset",text= " Manual",icon = 'HELP')
        #区切り線
        self.layout.separator()
        self.layout.operator("wm.url_open_preset",text= " Manual",icon = 'HELP')
        #区切り線
        self.layout.separator()
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
                             text = MYADDON_OT_stretch_vertex.bl_label)
        #区切り線
        self.layout.separator()
        self.layout.operator(MYAADDON_OT_create_ico_sphere.bl_idname,
                               text = MYAADDON_OT_create_ico_sphere.bl_label)
         #区切り線
        self.layout.separator()
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
                             text = MYADDON_OT_export_scene.bl_label)
        


    #既存のメニューにサブメニューを追加
    def submenu(self, context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #リドゥ　アンドゥ可能オプション
    bl_options = {'REGISTER','UNDO'}

    #メニューを実行したときに呼ばれるコースバック関数
    def execute(self,context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")

        #オペレーターの命令終了通知
        return {'FINISHED'}


class MYAADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}

    #メニューを実行したときに呼ばれる関数
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        return {'FINISHED'}


class MYADDON_OT_export_scene(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をエクスポートします"

    def execute(self,context):
        print("シーン情報をエクスポートします")
       
        #シーン内全オブジェクトについて
        for object in bpy.context.scene.objects:
            print(object.type + " - " + object.name)
            #ローカルトランスフォーム行列kら平行移動、回転、スケーリングを抽出
            #型は Vector,Quaternion, Vector
            trans, rot, scale =object.matrix_local.decompose()
            #回転を Quaternion から Euler (三軸での回転角)に変換
            rot = rot.to_euler()
            #ラジアンから度数法に変換
            rot.x = math.degrees(rot.x)
            rot.y = math.degrees(rot.y)
            rot.z = math.degrees(rot.z)

            #トランスフォーム情報を表示
            print("Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z))
            print("Rot(%f,%f,%f)" % (rot.x, rot.y, rot.z))
            print("Scale(%f,%f,%f)" % (scale.x, scale.y,scale.z))

            #親オブジェクトの名前
            if object.parent:
                print("Parent:" + object.parent.name)
            print()

        print("シーン情報をエクスポートしました")
        self.report({'INFO'},"Exported This Scene")
        
        return {'FINISHED'}


#blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
    MYADDON_OT_stretch_vertex,
    MYAADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
)

#Add On Startup callback
def register():
    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化")
    
#Add On Disable callback
def unregister():
    #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    #Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化")




    
# #Test Run 
# if __name__== "__main__":
#     register()    


#メニュー項目描画
def draw_menu_manual(self,context):
    #self : 呼び出し元のクラスインスタンス。thisポインタのような扱い
    #context : カーソルを合わせたときのポップアップのカスタマイズに使用する
    #トップバーの[エディターメニュー]に項目(オペレーター)を追加
    self.layout.operator("wm.url_open_preset",text="Manual",icon='HELP')




        