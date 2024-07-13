from flask import Flask, jsonify
import random
import json

app = Flask(__name__)

def herbalism_kit(herbalism_kit_result):

    reset_plant_collection = {
        "plant_collection":{
            "common":0,
            "uncommon":0,
            "rare":0,
            "very_rare":0,
            "legendary":0,
            "mythic":0
        }
    }

    if herbalism_kit_result == 123:
        with open("eberron/plant_collection.json","w") as output:
            output.write(json.dumps(reset_plant_collection))
        return reset_plant_collection

    with open("eberron/plant_collection.json") as input:
        plant_collection = json.load(input)

    def die(n):
        result = random.randint(1,n)
        return result
    def plant_potency(x,n):
        all_plants = []
        for i in range(x):
            potency = random.randint(1,n)
            all_plants.append(potency)
        return all_plants


    success_level = int(round(herbalism_kit_result/5,0))

    if success_level == 3:
        num_plants = die(4)
        all_plants = plant_potency(num_plants,1024)    
    elif success_level == 4:
        num_plants = die(6)
        all_plants = plant_potency(num_plants,1024)
    elif success_level == 5:
        num_plants = die(8)
        all_plants = plant_potency(num_plants,1024)
    elif success_level == 6:
        num_plants = die(10)
        all_plants = plant_potency(num_plants,1024)
    elif success_level > 6:
        num_plants = die(12)
        all_plants = plant_potency(num_plants,1024)
    else:
        return {"result":"Roll was too low"}


    for plant in all_plants:
        if plant <= 512:
            check = die(100)
            if herbalism_kit_result >= check:
                plant_collection["plant_collection"]["uncommon"] += 1
            else:
                plant_collection["plant_collection"]["common"] += 1
        elif plant > 512 and plant <= 800:
            check = die(100)
            if herbalism_kit_result >= check:
                plant_collection["plant_collection"]["rare"] += 1
            else:
                plant_collection["plant_collection"]["uncommon"] += 1
        elif plant > 800 and plant <= 950:
            check = die(100)
            if herbalism_kit_result >= check:
                plant_collection["plant_collection"]["very_rare"] += 1
            else:
                plant_collection["plant_collection"]["rare"] += 1
        elif plant > 950 and plant <= 1000:
            check = die(100)
            if herbalism_kit_result >= check:
                plant_collection["plant_collection"]["legendary"] += 1
            else:
                plant_collection["plant_collection"]["very_rare"] += 1
        elif plant > 1000 and plant <= 1024:
            check = die(100)
            if herbalism_kit_result >= check:
                plant_collection["plant_collection"]["mythic"] += 1
            else:
                plant_collection["plant_collection"]["legendary"] += 1



    with open("eberron/plant_collection.json","w") as output:
        output.write(json.dumps(plant_collection))
    
    return plant_collection

@app.route('/api/herbalismkit/<int:integer>', methods=['GET'])
def get_herbalism_kit(integer):
    result = herbalism_kit(integer)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,port=5155,host="0.0.0.0")