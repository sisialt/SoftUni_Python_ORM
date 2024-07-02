import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character

# Create queries within functions


def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )

    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune',
# True))


def show_all_locations():
    result = []

    for location in Location.objects.all().order_by('-id'):
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    capitals = Location.objects.all().filter(is_capital=True)
    result = capitals.values('name')
    return result


def delete_first_location():
    Location.objects.first().delete()


# Location.objects.create(
#     name='Sofia',
#     region='Sofia Region',
#     population=1329000,
#     description='The capital of Bulgaria and the largest city in the country',
# )
#
# Location.objects.create(
#     name='Plovdiv',
#     region='Plovdiv Region',
#     population=346942,
#     description='The second-largest city in Bulgaria with a rich historical heritage',
# )
#
# location = Location(
#     name='Varna',
#     region='Varna Region',
#     population=330486,
#     description='A city known for its sea breeze and beautiful beaches on the Black Sea',
# )
# location.save()

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount():
    for car in Car.objects.all():
        discount_percentage = sum(int(num) for num in str(car.year))
        car.price_with_discount = car.price - car.price * discount_percentage / 100
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.all().filter(year__gt=2020).values('model', 'price_with_discount')
    return recent_cars


def delete_last_car():
    Car.objects.last().delete()


# Car.objects.create(
#     model='Mercedes C63 AMG',
#     year=2019,
#     color='white',
#     price=120000.00
# )
#
# Car.objects.create(
#     model='Audi Q7 S line',
#     year=2023,
#     color='black',
#     price=183900.00
# )
#
# Car.objects.create(
#     model='Chevrolet Corvette',
#     year='2021',
#     color='dark grey',
#     price=199999.00
# )

# apply_discount()
# print(get_recent_cars())


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.all().filter(is_finished=False)

    return '\n'.join(str(t) for t in unfinished_tasks)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    new_description = []
    for ch in text:
        new_description.append(chr(ord(ch) - 3))

    new_description = ''.join(new_description)

    for task in Task.objects.filter(title=task_title):
        task.description = new_description
        task.save()
    # Task.objects.filter(title=task_title).update(description=new_description)


# Task.objects.create(
#     title='Simple Task',
#     description='This is a sample task description',
#     due_date='2023-10-31',
#     is_finished=False,
# )
#
# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


def get_deluxe_rooms():
    result = []

    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')

    for room in deluxe_rooms:
        if room.id % 2 == 0:
            result.append(str(room))

    return '\n'.join(result)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by("id")

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

        room.save()

    # not working
    # all_rooms = HotelRoom.objects.all().order_by('id')
    #
    # for i in range(len(all_rooms)):
    #     if not all_rooms[i].is_reserved:
    #         continue
    #
    #     if all_rooms[0] == HotelRoom.objects.first():
    #         all_rooms[0].capacity += all_rooms[0].id
    #         all_rooms[0].save()
    #         continue
    #
    #     all_rooms[i].capacity += all_rooms[i - 1].capacity
    #     all_rooms[i].save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved:
        last_room.delete()


# HotelRoom.objects.create(
#     room_number=101,
#     room_type='Standard',
#     capacity=2,
#     amenities='Tv',
#     price_per_night=100.00,
# )
#
# HotelRoom.objects.create(
#     room_number=201,
#     room_type='Deluxe',
#     capacity=3,
#     amenities='Wi-Fi',
#     price_per_night=200.00,
# )
#
# HotelRoom.objects.create(
#     room_number=501,
#     room_type='Deluxe',
#     capacity=6,
#     amenities='Jacuzzi',
#     price_per_night=400.00,
# )

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=101).is_reserved)
# increase_room_capacity()
# print(HotelRoom.objects.all().values('capacity'))


def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty",
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_name = first_character.name + " " + second_character.name
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_class = "Fusion"
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ["Mage", "Scout"]:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=fusion_name,
        class_name=fusion_class,
        level=fusion_level,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory,
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()


