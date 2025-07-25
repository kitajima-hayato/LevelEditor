import bpy

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

