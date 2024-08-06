import json
import os

def FindParent(dict, id, parent):
    step = 0
    while dict[id].get("_parent") and step < 6:
        if dict[id].get("_parent") == parent:
            return True
        id = dict[id].get("_parent")
        step += 1
    return False
weapontype_list = []
weapon_list = []
weaponmod_list = []
mangazine_list = []
with open('items.json','r',encoding="UTF-8") as f:
    items_dict = json.load(f)
    #获取武器类型列表
    for item in items_dict.values():
        if item.get("_parent") == "5422acb9af1c889c16000029":
            weapon_list.append(item.get("_id"))
    #获取武器列表
    for item in items_dict.values():
        if item.get("_parent") in weapon_list:
            weapon_list.append(item.get("_id"))
    #获取武器配件列表
    for item in items_dict.values():
        if FindParent(items_dict,item["_id"],"5448fe124bdc2da5018b4567"):
            weaponmod_list.append(item.get("_id"))
    #获取弹匣列表
    for item in items_dict.values():
        if FindParent(items_dict,item["_id"],"5448bc234bdc2d3c308b4569"):
            mangazine_list.append(item.get("_id"))
    #全兼容
    for item in weapon_list + weaponmod_list:
        if items_dict[item]["_props"].get("Slots"):
            for i in items_dict[item]["_props"]["Slots"]:
                if i["_props"].get("filters"):
                    if i["_name"] != "mod_magazine":
                        for j in i["_props"]["filters"]:
                            j["Filter"] = j["Filter"]+["54009119af1c881c07000029"]
                            j["ExcludedFilter"] = ["5448bc234bdc2d3c308b4569","5485a8684bdc2da71d8b4567"]
                    #弹匣全兼容
                    elif i["_name"] == "mod_magazine":
                        for j in i["_props"]["filters"]:
                            j["Filter"] = j["Filter"]+["5448bc234bdc2d3c308b4569"]
        #弹药全兼容
        if items_dict[item]["_props"].get("Chambers"):
            for i in items_dict[item]["_props"]["Chambers"]:
                if i["_props"].get("filters"):
                    for j in i["_props"]["filters"]:
                            j["Filter"] = j["Filter"]+["5485a8684bdc2da71d8b4567"]
        #取消冲突
        if items_dict[item]["_props"].get("ConflictingItems"):
            items_dict[item]["_props"]["ConflictingItems"] = []
    #弹匣中弹药全兼容
    for item in mangazine_list:
        if items_dict[item]["_props"].get("Cartridges"):
            for i in items_dict[item]["_props"]["Cartridges"]:
                if i["_props"].get("filters"):
                    for j in i["_props"]["filters"]:
                        j["Filter"] = j["Filter"]+["5485a8684bdc2da71d8b4567"]
    #物品栏兼容
    for slot in items_dict["55d7217a4bdc2d86028b456d"]["_props"]["Slots"]:
        if slot["_props"].get("filters"):
            for i in slot["_props"]["filters"]:
                i["Filter"] = i["Filter"]+["54009119af1c881c07000029"]
    #栏位冲突兼容
    for item in items_dict.values():
        if item["_props"].get("BlocksArmorVest"):
            item["_props"]["BlocksArmorVest"] = False
        if item["_props"].get("BlocksEarpiece"):
            item["_props"]["BlocksEarpiece"] = False
        if item["_props"].get("BlocksEyewear"):
            item["_props"]["BlocksEyewear"] = False
        if item["_props"].get("BlocksHeadwear"):
            item["_props"]["BlocksHeadwear"] = False
        if item["_props"].get("BlocksFaceCover"):
            item["_props"]["BlocksFaceCover"] = False
os.mkdir("output")
with open('output/items.json', 'w') as file:
    json.dump(items_dict, file, indent=2)
print("Done")
