import bpy
import math
import bpy_extras

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
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
                               text = MYADDON_OT_create_ico_sphere.bl_label)
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


class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}

    #メニューを実行したときに呼ばれる関数
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        return {'FINISHED'}


class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をエクスポートします"

    #出力するファイルの拡張子
    filename_ext = ".scene"

    #自動的に改行させるメソッド
    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')


    def execute(self,context):
        print("シーン情報をエクスポートします")
       
        #ファイルに出力
        self.export()

        print("シーン情報をエクスポートしました")
        self.report({'INFO'},"Exported This Scene")
        
        return {'FINISHED'}
    
    #ファイルに書き出す処理
    def export(self):
        """ファイルに出力"""
        print("シーン情報出力中... %r" % self.filepath)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズ
        with open(self.filepath, "wt")as file:

            #ファイルに文字列を書き込む
            self.write_and_print(file, "SCENE")

             #シーン内全オブジェクトについて
            for object in bpy.context.scene.objects:
               # file.write(object.type + " - " + object.name)

               #親オブジェクトがあるものはスキップ（親が呼び出すため）
               if(object.parent):
                   continue
               #シーン直下のオブジェクトをルートノード（０）とし再帰関数で走査
               self.parse_scene_recursive(file,object,0)
               #self.write_and_print(file, f"  Type: {object.type}")
               #self.write_and_print(file, f"Object: {object.name}")
                
               #ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
               #型は Vector,Quaternion, Vector
               trans, rot, scale =object.matrix_local.decompose()
               #回転を Quaternion から Euler (三軸での回転角)に変換
               rot = rot.to_euler()
               #ラジアンから度数法に変換
               rot.x = math.degrees(rot.x)
               rot.y = math.degrees(rot.y)
               rot.z = math.degrees(rot.z)

               

    #オブジェクトの１個分の出力処理
    def parse_scene_recursive(self,file,object,level):
        """シーン解析用再帰関数"""

        #深さ分インデントする
        indent = ''
        for i in range(level):
            indent += "\t"

        #オブジェクト名書き込み
        self.write_and_print(file,indent + object.type)
        #オブジェクト名書き込み - オブジェクト名の表示あり
        #self.write_and_print(file, indent + object.type + " - " + object.name)
        trans,rot,scale = object.matrix_local.decompose()
        #回転を Quaternion から Euler （３軸での回転角）に変換
        rot = rot.to_euler()
        #ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        #トランスフォーム情報を表示
        self.write_and_print(file, indent + f"  Translate: ({trans.x:.3f}, {trans.y:.3f}, {trans.z:.3f})")
        self.write_and_print(file, indent + f"  Rotation:  ({rot.x:.3f}, {rot.y:.3f}, {rot.z:.3f})")
        self.write_and_print(file, indent + f"  Scale:     ({scale.x:.3f}, {scale.y:.3f}, {scale.z:.3f})")
        #カスタムプロパティ'file_name'
        if "file_name" in object:
            self.write_and_print(file, indent + f"  N %s" % object["file_name"])
        self.write_and_print(file,indent + 'END')
        self.write_and_print(file,"")

        #子ノードへ進む（深さが１上がる）
        for child in object.children:
            self.parse_scene_recursive(file,child,level + 1)


#パネルファイル名
class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトファイルのネームパネル"""
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニューの描画
    def draw(self,context):

        #パネルに項目を追加
        if "file_name" in context.object:
            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["file_name"]',text=self.bl_label)
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)


#オペレーター　カスタムプロパティ['file_name']追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileNmae 追加"
    bl_description = "['file_name']カスタムプロパティを追加します"
    bl_options = {"REGISTER","UNDO"}

    def execute(self,context):

        #['file_name']カスタムプロパティを追加
        context.object["file_name"] = ""

        return {"FINISHED"}


    



#blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    OBJECT_PT_file_name,
    MYADDON_OT_add_filename,
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




        