import pytest
import io

from PIL import Image

@pytest.fixture(scope="module")
def annotation():
    annotation = [
        {
                "label" : "Object",
                "label_int" : 0,
                "bounding box" : [0.11212, 0.11, 0.4564, 0.4546]
          },
          {
                "label" : "bla",
                "label_int" : 2,
                "bounding box" : [0.11, 0.11, 0.45, 0.45]
          }
    ]

    return annotation

@pytest.fixture(scope="module")
def binary_annotation():
    annotation = b'[{"label" : "Object","label_int" : 0,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "bla","label_int" : 2,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]'
    return annotation

@pytest.fixture(scope="module")
def binary_annotation_1():
    annotation = b'[{"label" : "bli","label_int" : 4,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "blo","label_int" : 3,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]'
    return annotation

@pytest.fixture(scope="module")
def binary_img():
    img = Image.open("app/tests/sample/img_1.png")
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()
    return imgbyte

@pytest.fixture(scope="module")
def binary_img_1():
    img = Image.open("app/tests/sample/img_2.png")
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()
    return imgbyte

@pytest.fixture(scope="module")
def binary_metadata():
    metadata = b'{"dataset" : [0], "dataset_extraction" : "ARM", "pretreatment" : False, "data_augmentation" : False, "test" : True}'
    return metadata

@pytest.fixture(scope="module")
def item():
    item = {
        "id_code" : "3017620422003",
        "brand" : "Ferero",
        "name" : "Nutella",
        "ingredient" : ["en:sugar","en:added-sugar","en:disaccharide","en:palm-oil","en:oil-and-fat","en:vegetable-oil-and-fat","en:palm-oil-and-fat","en:hazelnut","en:nut","en:tree-nut","en:fat-reduced-cocoa","en:plant","en:cocoa","en:skimmed-milk-powder","en:dairy","en:milk-powder","en:whey-powder","en:whey","en:emulsifier","en:vanillin","en:soya-lecithin","en:e322","en:e322i"],
        "allergen" : ["en:milk","en:nuts","en:soybeans"],
        "nutriment" : '{"carbohydrates":57.5,"carbohydrates_100g":57.5,"carbohydrates_serving":8.62,"carbohydrates_unit":"g","carbohydrates_value":57.5,"carbon-footprint-from-known-ingredients_product":135,"carbon-footprint-from-known-ingredients_serving":5.07,"energy":2252,"energy-kcal":539,"energy-kcal_100g":539,"energy-kcal_serving":80.8,"energy-kcal_unit":"kcal","energy-kcal_value":539,"energy-kcal_value_computed":533.3,"energy-kj":2252,"energy-kj_100g":2252,"energy-kj_serving":338,"energy-kj_unit":"kJ","energy-kj_value":2252,"energy-kj_value_computed":2227.9,"energy_100g":2252,"energy_serving":338,"energy_unit":"kJ","energy_value":2252,"fat":30.9,"fat_100g":30.9,"fat_serving":4.63,"fat_unit":"g","fat_value":30.9,"fiber":0,"fiber_100g":0,"fiber_serving":0,"fiber_unit":"g","fiber_value":0,"fruits-vegetables-legumes-estimate-from-ingredients_100g":0,"fruits-vegetables-legumes-estimate-from-ingredients_serving":0,"fruits-vegetables-nuts-estimate-from-ingredients_100g":13,"fruits-vegetables-nuts-estimate-from-ingredients_serving":13,"nova-group":4,"nova-group_100g":4,"nova-group_serving":4,"nutrition-score-fr":26,"nutrition-score-fr_100g":26,"proteins":6.3,"proteins_100g":6.3,"proteins_serving":0.945,"proteins_unit":"g","proteins_value":6.3,"salt":0.107,"salt_100g":0.107,"salt_serving":0.016,"salt_unit":"g","salt_value":0.107,"saturated-fat":10.6,"saturated-fat_100g":10.6,"saturated-fat_serving":1.59,"saturated-fat_unit":"g","saturated-fat_value":10.6,"sodium":0.0428,"sodium_100g":0.0428,"sodium_serving":0.00642,"sodium_unit":"g","sodium_value":0.0428,"sugars":56.3,"sugars_100g":56.3,"sugars_serving":8.44,"sugars_unit":"g","sugars_value":56.3}',
        "nutriscore" : ["e"],
        "ecoscore" : ["d"],
        "packaging" : ["en:clear-glass","en:non-corrugated-cardboard","en:paper","en:pp-5-polypropylene","xx:82-c-pap"],
        "image" : "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_en.550.400.jpg",
        "url_openfoodfact" : "https://fr.openfoodfacts.org/produit/3017620422003/"
    }

    return item


@pytest.fixture(scope="module")
def item2():
    item = {
        "id_code" : "3017620422003",
        "brand" : "Barilla",
        "name" : "Pesto",
        "ingredient" : ["en:sugar","en:added-sugar","en:disaccharide","en:palm-oil","en:oil-and-fat","en:vegetable-oil-and-fat","en:palm-oil-and-fat","en:hazelnut","en:nut","en:tree-nut","en:fat-reduced-cocoa","en:plant","en:cocoa","en:skimmed-milk-powder","en:dairy","en:milk-powder","en:whey-powder","en:whey","en:emulsifier","en:vanillin","en:soya-lecithin","en:e322","en:e322i"],
        "allergen" : ["en:milk","en:nuts","en:soybeans"],
        "nutriment" : '{"carbohydrates":57.5,"carbohydrates_100g":57.5,"carbohydrates_serving":8.62,"carbohydrates_unit":"g","carbohydrates_value":57.5,"carbon-footprint-from-known-ingredients_product":135,"carbon-footprint-from-known-ingredients_serving":5.07,"energy":2252,"energy-kcal":539,"energy-kcal_100g":539,"energy-kcal_serving":80.8,"energy-kcal_unit":"kcal","energy-kcal_value":539,"energy-kcal_value_computed":533.3,"energy-kj":2252,"energy-kj_100g":2252,"energy-kj_serving":338,"energy-kj_unit":"kJ","energy-kj_value":2252,"energy-kj_value_computed":2227.9,"energy_100g":2252,"energy_serving":338,"energy_unit":"kJ","energy_value":2252,"fat":30.9,"fat_100g":30.9,"fat_serving":4.63,"fat_unit":"g","fat_value":30.9,"fiber":0,"fiber_100g":0,"fiber_serving":0,"fiber_unit":"g","fiber_value":0,"fruits-vegetables-legumes-estimate-from-ingredients_100g":0,"fruits-vegetables-legumes-estimate-from-ingredients_serving":0,"fruits-vegetables-nuts-estimate-from-ingredients_100g":13,"fruits-vegetables-nuts-estimate-from-ingredients_serving":13,"nova-group":4,"nova-group_100g":4,"nova-group_serving":4,"nutrition-score-fr":26,"nutrition-score-fr_100g":26,"proteins":6.3,"proteins_100g":6.3,"proteins_serving":0.945,"proteins_unit":"g","proteins_value":6.3,"salt":0.107,"salt_100g":0.107,"salt_serving":0.016,"salt_unit":"g","salt_value":0.107,"saturated-fat":10.6,"saturated-fat_100g":10.6,"saturated-fat_serving":1.59,"saturated-fat_unit":"g","saturated-fat_value":10.6,"sodium":0.0428,"sodium_100g":0.0428,"sodium_serving":0.00642,"sodium_unit":"g","sodium_value":0.0428,"sugars":56.3,"sugars_100g":56.3,"sugars_serving":8.44,"sugars_unit":"g","sugars_value":56.3}',
        "nutriscore" : ["e"],
        "ecoscore" : ["d"],
        "packaging" : ["en:clear-glass","en:non-corrugated-cardboard","en:paper","en:pp-5-polypropylene","xx:82-c-pap"],
        "image" : "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_en.550.400.jpg",
        "url_openfoodfact" : "https://fr.openfoodfacts.org/produit/3017620422003/"
    }

    return item

@pytest.fixture(scope="module")
def user():
    user = {
        "username" : "raiden",
        "last_name" : "jac",
        "first_name" : "Adrien",
        "age" : 34,
        "gender" : 1}

    return user

@pytest.fixture(scope="module")
def user2():
    user2 = {
        "username" : "juju",
        "last_name" : "jac",
        "first_name" : "Ju",
        "age" : 32,
        "gender" : 2}

    return user2

@pytest.fixture(scope="module")
def place():
    place = {
        "name" : "inter",
        "adresse" : "1 rue A",
        "postcode" : "21000",
        "city" : "Dijon",
        }

    return place

@pytest.fixture(scope="module")
def place2():
    place2 = {
        "name" : "carrefour",
        "adresse" : "2 Rue B",
        "postcode" : "69000",
        "city" : "Lyon",
        }
    return place2

@pytest.fixture(scope="module")
def scan1():
    scan = {
        "id_user" : "1",
        "id_code" : "2",
        "id_place" : "6",
        }
    return scan

@pytest.fixture(scope="module")
def scan2():
    scan = {
        "id_code" : "2",
        "id_place" : "6",
        }
    return scan

@pytest.fixture(scope="module")
def scan3():
    scan = {
        "id_user" : "1",
        "id_place" : "6",
        }
    return scan

@pytest.fixture(scope="module")
def scan4():
    scan = {
        "id_user" : "1",
        "id_code" : "2",
        }
    return scan