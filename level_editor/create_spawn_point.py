import bpy
from bpy.props import StringProperty
from .load_spawn_point import import_spawn_symbol_object
from .load_spawn_point import SpawnNames



class MY_ADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "level_editor.spawn_create_symbol"
    bl_label = "出現ポイントのシンボルを作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    __annotations__ = {
        "type": StringProperty(
            name="Type",
            default="PlayerSpawn"
        )
    }

    object_name = "PlayerSpawn"

    def execute(self, context):
        # 読み込み済みのコピー元オブジェクトを検索
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        # 存在しない場合は読み込みオペレータを実行して再取得
        if spawn_object is None:
            spawn_object = import_spawn_symbol_object(self.type)
            if spawn_object is None:
                self.report({'ERROR'}, "出現ポイントのシンボルの取得に失敗しました")
                return {'CANCELLED'}


        print("出現ポイントのシンボルを作成します")

        # Blenderでの選択を解除
        bpy.ops.object.select_all(action='DESELECT')

        # 複製元の非表示オブジェクトを複製する
        object = spawn_object.copy()

        # 複製したオブジェクトを現在のシーンにリンク
        bpy.context.collection.objects.link(object)

        # オブジェクト名を変更
        object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        return {'FINISHED'}

# 自キャラ専用出現ポイントシンボル作成オペレータ
class MY_ADDON_OT_SPAWN_CREATE_PLAYER_SYMBOL(bpy.types.Operator):
    """出現ポイントのシンボルを作成・配置する"""
    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントのシンボルを作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.level_editor.spawn_create_symbol(type="PlayerSpawn")

        return {'FINISHED'}
    

# エネミー専用出現ポイントシンボル作成オペレータ
class MY_ADDON_OT_SPAWN_CREATE_ENEMY_SYMBOL(bpy.types.Operator):
    """出現ポイントのシンボルを作成・配置する"""
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "エネミー出現ポイントのシンボルを作成"
    bl_description = "エネミー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.level_editor.spawn_create_symbol(type="EnemySpawn")

        return {'FINISHED'}