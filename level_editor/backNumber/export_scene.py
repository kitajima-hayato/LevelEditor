import bpy
import bpy_extras
import json
import math

class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をエクスポートします"

    #出力するファイルの拡張子
    filename_ext = ".json"

    #自動的に改行させるメソッド
    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')


    def execute(self,context):
        print("シーン情報をエクスポートします")
       
        #ファイルに出力
        self.export_json()

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

        #カスタムプロパティ'collision'
        if "collider" in object:
            self.write_and_print(file,indent + f"C %s" % object["collider"])
            temp_str = indent + f"  CC %f %f %f"
            temp_str %= (object["collider_center"][0],object["collider_center"][1],object["collider_center"][2])
            self.write_and_print(file,temp_str)
            temp_str = indent + f"  CS %f %f %f"
            temp_str %= (object["collider_size"][0],object["collider_size"][1],object["collider_size"][2])
            self.write_and_print(file,temp_str)
            self.write_and_print(file,indent + 'END')
            self.write_and_print(file,"")
        #子ノードへ進む（深さが１上がる）
        for child in object.children:
            self.parse_scene_recursive(file,child,level + 1)



    def export_json(self):
        """シーン情報をJSON形式で出力"""
        #保存する情報をまとめるdict
        json_object_root = dict()

        #ノード名
        json_object_root["name"]="scene"
        #オブジェクトリストを作成
        json_object_root["objects"]=list()

        #TODO : シーン内全オブジェクトについて
        for object in bpy.context.scene.objects:

            #親オブジェクトがあるものはスキップ（親が呼び出すため）
            if(object.parent):
                continue
            #シーン直下のオブジェクトをルートノード（０）とし再帰関数で走査
            self.parse_scene_recursive_json(json_object_root["objects"],object,0)

        #オブジェクトをJSON文字列にエンコード
        json_text = json.dumps(json_object_root,ensure_ascii=False,cls=json.JSONEncoder,indent=4)
        #コンソールに出力
        print(json_text)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズ
        with open(self.filepath, "w", encoding="utf-8") as file:
            # ファイルに文字列を書き込む
            file.write(json_text)


    def parse_scene_recursive_json(self,data_parent,object,level):
        #シーンのオブジェクト１個分のjsonオブジェクト作成
        json_object = dict()
        #オブジェクトの種類
        json_object["type"] = object.type
        #オブジェクト名
        json_object["name"] = object.name
         # カスタムプロパティ 'file_name'
        if "file_name" in object:
            json_object["file_name"] = object["file_name"]
        else:
            # オブジェクト名をベースに .001 などを除去したファイル名を設定
            json_object["file_name"] = object.name.split('.')[0]

        #オブジェクトのローカルトランスフォームから
        #平行移動、回転、スケーリングを抽出
        trans,rot,scale = object.matrix_local.decompose()
        #回転を Quaternion から Euler （３軸での回転角）に変換
        rot = rot.to_euler()
        #トランスフォーム情報をディクショナリに登録
        transform = dict()
        transform["translation"] = (trans.x,trans.y,trans.z)
        transform["rotation"] = (rot.x,rot.y,rot.z)
        transform["scaling"] = (scale.x,scale.y,scale.z)
        #まとめて１個分のjsonオブジェクトに登録
        json_object["transform"] = transform

        #カスタムプロパティ'collider'
        if "collider" in object:
            collider = dict()
            collider["type"] = object["collider"]
            collider["center"] = object["collider_center"].to_list()
            collider["size"] = object["collider_size"].to_list()
            json_object["collider"] = collider
            

        #１個分のjsonオブジェクトを親オブジェクト登録
        data_parent.append(json_object)

        #子ノードがあれば
        if len(object.children) > 0:
            #子ノードのリストを作成
            json_object["children"] = list()
            #子ノードへ進む（深さが１上がる）
            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"],child,level + 1)


