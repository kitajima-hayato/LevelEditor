import bpy
import os
import bpy.ops


# オペレータ 出現ポイントのシンボルを読み込む　
class MY_ADDON_OT_spawn_import_symbol(bpy.types.Operator):
    """出現ポイントのシンボルを読み込む"""
    bl_idname = "level_editor.spawn_import_symbol"
    bl_label = "出現ポイントのシンボルを読み込む"
    bl_description = "出現ポイントのシンボルを読み込みます"

    prototype_object_name = "PrototypePlayerSpawn"
    object_name = "PlayerSpawn"




class load_spawn_point(bpy.types.Operator):
    """Load Spawn Point"""
    bl_idname = "level_editor.load_spawn_point"
    bl_label = "出現ポイントシンボル"
    bl_description = "出現ポイントのシンボルをインポートします"

    def load_obj(self, type):
        print("出現ポイントのシンボルをインポートします")

        # 重複ロード防止
        spawn_object = bpy.data.objects.get(SpawnNames.names[type][SpawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {'CANCELLED'}

        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory = os.path.dirname(__file__)
        #ディレクトリからのモデルファイルの相対パス記述
        #relative_path = "player/Player.obj"
        relative_path = SpawnNames.names[type][SpawnNames.FILENAME]
        # 合成してモデルファイルのフルパスを得る
        full_path = os.path.join(addon_directory,relative_path)

        # オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',
                              filePath = full_path,
                              display_type = 'THUMBNAIL',
                              forward_axis = 'Z',up_axis = 'Y',)
        # 回転を適用
        bpy.ops.object.transform_apply(location=False,
                                       rotation=True,
                                       scale=False,
                                       properties=False,
                                       isolate_users=False,)
        
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name = SpawnNames.names[type][SpawnNames.PROTOTYPE]

        # オブジェクトの種類を設定
        #object["type"] = MY_ADDON_OT_spawn_import_symbol.object_name
        object["type"] = SpawnNames.names[type][SpawnNames.INSTANCE]
        # メモリ上においておくかシーンから外す
        # bpy.context.collection.objects.unlink(object)

        return {'FINISHED'}
    
    
    def execute(self, context):
        # エネミーオブジェクト読み込み
        self.load_obj("EnemySpawn")
        # プレイヤーオブジェクト読み込み
        self.load_obj("PlayerSpawn")

        return {'FINISHED'}
        




def import_spawn_symbol_object(type):
    prototype_name = SpawnNames.names[type][SpawnNames.PROTOTYPE]
    object_name = SpawnNames.names[type][SpawnNames.INSTANCE]
    relative_path = SpawnNames.names[type][SpawnNames.FILENAME]

    if bpy.data.objects.get(prototype_name):
        return bpy.data.objects.get(prototype_name)

    addon_directory = os.path.dirname(__file__)
    # relative_path = "player/Player.obj"
    full_path = os.path.join(addon_directory, relative_path)

    bpy.ops.wm.obj_import('EXEC_DEFAULT',
                          filepath=full_path,
                          display_type='THUMBNAIL',
                          forward_axis='Z', up_axis='Y')

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    obj = bpy.context.active_object
    if obj:

        obj.name = prototype_name
        obj["type"] = object_name
    
        bpy.context.collection.objects.unlink(obj)
        return obj

class SpawnNames():

    # インデックス
    PROTOTYPE = 0
    INSTANCE = 1
    FILENAME = 2

    names = {}

    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["EnemySpawn"] = ("PrototypeEnemySpawn","EnemySpawn", "enemy/enemy.obj")
    names["PlayerSpawn"] = ("PrototypePlayerSpawn", "PlayerSpawn", "player/Player.obj")