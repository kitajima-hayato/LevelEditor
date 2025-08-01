import bpy

class Disabled_Flag(bpy.types.Operator):
    """カスタムプロパティの定義"""
    bl_idname = "disabled.disabled_flag"
    bl_label = "非出力フラグ"
    bl_description = "このオブジェクトを出力しないようにします"

    def execute(self, context):
        #カスタムプロパティを追加
        context.object["disabled_flag"] = True
        return {"FINISHED"}
    


class Disabled_Flag_PT_Panel(bpy.types.Panel):
    """非出力フラグのパネル"""
    bl_idname = "Disabled_Flag_PT_Panel"
    bl_label = "Disabled Flag"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        #パネルに項目を追加
        if "disabled_flag" in context.object:
            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["disabled_flag"]',text=self.bl_label)
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(Disabled_Flag.bl_idname)