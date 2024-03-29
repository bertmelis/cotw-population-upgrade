import random
import os

import cotw_gameinfo
import deca_tools

def upgrade_population(reserve_name):
    fname = cotw_gameinfo.reserves_population_files[reserve_name]
    backup_fname = fname + "_bak"
    i = 1
    if os.path.isfile(backup_fname):
        while os.path.isfile(backup_fname + str(i)):
           i += 1
        backup_fname += str(i)
    os.rename(fname, backup_fname)
    data_bytes = deca_tools.read_file(backup_fname)
    data_bytes = bytearray(data_bytes)

    # slice data
    header = data_bytes[0:32]
    data_bytes = data_bytes[32:]

    # decode content
    decomed_data_bytes = deca_tools.decompress(data_bytes)
    decomed_data_bytes = bytearray(decomed_data_bytes)

    # slice data
    decomed_header = decomed_data_bytes[0:5]
    decomed_data_bytes = decomed_data_bytes[5:]

    # save adf format data to file
    adf_file = fname + "_sliced"
    deca_tools.save_file(adf_file, decomed_data_bytes)

    parse_obj = deca_tools.parse_adf(adf_file)
    populations = parse_obj.table_instance_full_values[0].value["Populations"].value

    for animal_index, animal_type in cotw_gameinfo.animaltypes_per_reserve[reserve_name].items():

        gender = 0 # run at least once
        while gender != cotw_gameinfo.gender_that_makes_diamond[animal_type]:
            groups_rabbit = populations[animal_index].value["Groups"].value
            random_group = groups_rabbit[random.randint(0, len(groups_rabbit) - 1)].value["Animals"]
            number_animals_in_group = len(random_group.value)
            random_animal = random_group.value[random.randint(0, number_animals_in_group - 1)]
            gender = random_animal.value["Gender"].value
            if gender != cotw_gameinfo.gender_that_makes_diamond[animal_type]:
                continue
            print("This animal will be changed:")
            print("============================")
            print(random_animal)
            print("============================")
            print(f'Old weight: {random_animal.value["Weight"].value}')
            print(f'Old trophy rating: {random_animal.value["Score"].value}')
            if animal_type in cotw_gameinfo.min_go_weight_per_animal.keys():
                new_weight = random.uniform(cotw_gameinfo.min_go_weight_per_animal[animal_type], cotw_gameinfo.max_go_weight_per_animal[animal_type])
                new_tr = random.uniform(cotw_gameinfo.min_go_tr_per_animal[animal_type], cotw_gameinfo.max_go_tr_per_animal[animal_type])
                deca_tools.modify_uint8_data_by_absaddr(decomed_data_bytes, random_animal.value["IsGreatOne"].data_offset, 1)
            else:
                new_weight = random.uniform(cotw_gameinfo.min_diamond_weight_per_animal[animal_type], cotw_gameinfo.max_diamond_weight_per_animal[animal_type])
                new_tr = random.uniform(cotw_gameinfo.min_diamond_tr_per_animal[animal_type], cotw_gameinfo.max_diamond_tr_per_animal[animal_type])
            print(f'New weight: {new_weight}')
            print(f'New trophy rating: {new_tr}')
            deca_tools.modify_f32_data_by_absaddr(decomed_data_bytes,
                                                random_animal.value["Weight"].data_offset,
                                                new_weight)
            deca_tools.modify_f32_data_by_absaddr(decomed_data_bytes,
                                                random_animal.value["Score"].data_offset,
                                                new_tr)

    print(f'Saving updated population file: {fname}')
    decomed_data_bytes = decomed_header + decomed_data_bytes
    comed_data_bytes = header + deca_tools.compress(decomed_data_bytes)
    deca_tools.save_file(fname, comed_data_bytes)


if __name__ == "__main__":
    for reserve in cotw_gameinfo.reserves_population_files:
        if (not os.path.isfile(cotw_gameinfo.reserves_population_files[reserve])):
            continue
        filestats =  os.stat(cotw_gameinfo.reserves_population_files[reserve])
        if (filestats.st_size < 1024):
            continue
        if reserve in cotw_gameinfo.animaltypes_per_reserve:
            print(f'--- {reserve} ---')
            upgrade_population(reserve)
