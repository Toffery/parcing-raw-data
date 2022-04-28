import os
import pandas as pd


# Codes to parse
values = ['30100', '30200', '30300', '40100', '50000']

# Columns for pandas DataFrame
columns = ['ИдДок', 'ДатаДок', 'ДатаОтч', '10100', '20200', '20300', '30100', '30200', '30300', '40100', '50000']

# Structure for data storage
# dict = {
#     иддок: {
#         октмо: {
#             кбк: [0, 0, 0, 0, 0]
#         }
#     }
# }

files = []
for i in os.walk('ИНФОРМ_МАССИВ'):
    files.append(i)
for address, dirs, files in files:
    # Parse every .txt file
    for file in files:
        # Create new dicts for every file
        dict_kbk = {}
        dict_otkmo = {}
        dict_doc_id = {}
        dict_common = {}
        file_address = address + '/' + file
        print(file_address)
        # We need only .txt files, not .xls
        if not file_address.endswith('.xls'):
            # Open file in read-mode
            with open(file_address, 'r', encoding='cp1251') as f:
                # Parse datetime from folder
                DataDok = f'01.{file_address[19:21]}.{file_address[14:18]}'
                print(DataDok)
                # Parse every line of .txt file
                for line in f:
                    # If line startswith @@@, it means that new ИдДок has started
                    if line.startswith('@@@'):
                        # While line not startswith ###, it means that new info block has started
                        while not line.startswith('###'):
                            line = f.readline()
                            # === equal to the end of file
                            if line.startswith('==='):
                                break
                            if line.startswith('ИдДок'):
                                # Parse ИдДок
                                iddok, doc_id = line.strip().split(':')
                            elif line.startswith('ДатаДок'):
                                # Parse ДатаДок
                                datadok, doc_data = line.strip().split(':')
                                # Add ИдДок to ДатаДок for further manipulation
                                doc_id += f',{doc_data}'
                            elif line.startswith('10100:'):
                                # Parse ОКВЭД
                                okved, okved_val = line.strip().split(':')
                                # Take onle first 2 values of ОКВЭД
                                okved_val = okved_val[:2]
                                # Add ОКВЭД to ИдДок for further manipulation
                                doc_id += f',{okved_val}'
                    # If line startswith ###, it means new value block has started
                    if line.startswith('###'):
                        new_line = f.readline()
                        # This value block has ended
                        while not new_line.startswith('###'):
                            # Parse ОТКМО
                            otkmo, otkmo_val = new_line.strip().split(':')
                            new_line = f.readline()
                            # Parse КБК
                            kbk, kbk_val = new_line.strip().split(':')
                            new_line = f.readline()
                            # If in this value block we have only 1 ОТКМО and 1 КБК
                            if new_line.startswith('###'):
                                # For these ИдДок, ОТКМО, КБК set zeros
                                dict_common[doc_id] = {}
                                dict_common[doc_id][otkmo_val] = {}
                                dict_common[doc_id][otkmo_val][kbk_val] = [0, 0, 0, 0, 0]
                                break
                            # If line startswith 20200, it means that new ОТКОМ has started
                            while not new_line.startswith('20200'):
                                # Additional check for having only 1 ОТКМО and 1 КБК
                                if new_line.startswith('###'):
                                    break
                                # Parse codes 30100, 30200, 30300, 40100, 50000
                                val_id, val = new_line.strip().split(':')
                                # If this ИдДок hasn't been parsed already
                                if doc_id not in dict_common.keys():
                                    # Create new dict for this ИдДок
                                    dict_common[doc_id] = {}
                                    # Create new dict for this ОТКМО
                                    dict_common[doc_id][otkmo_val] = {}
                                    # For these ИдДок, ОТКМО, КБК set zeros
                                    dict_common[doc_id][otkmo_val][kbk_val] = [0, 0, 0, 0, 0]
                                    # If code in codes to parse
                                    if val_id in values:
                                        # Take its index from that list
                                        idx = values.index(val_id)
                                        # Add value in this index
                                        dict_common[doc_id][otkmo_val][kbk_val][idx] += float(val)
                                        # Round to 2 signs
                                        dict_common[doc_id][otkmo_val][kbk_val][idx] = \
                                            round(dict_common[doc_id][otkmo_val][kbk_val][idx], 2)
                                # If this ИдДок has been parsed already
                                else:
                                    # If this ОТКМО hasn't been passed already
                                    if otkmo_val not in dict_common[doc_id].keys():
                                        # Create new dict for this ОТКМО
                                        dict_common[doc_id][otkmo_val] = {}
                                        # For these ИдДок, ОТКМО, КБК set zeros
                                        dict_common[doc_id][otkmo_val][kbk_val] = [0, 0, 0, 0, 0]
                                        # Add value
                                        if val_id in values:
                                            idx = values.index(val_id)
                                            dict_common[doc_id][otkmo_val][kbk_val][idx] += float(val)
                                            dict_common[doc_id][otkmo_val][kbk_val][idx] = \
                                                round(dict_common[doc_id][otkmo_val][kbk_val][idx], 2)
                                    # If this ОТКМО has been passed already
                                    else:
                                        # If this КБК hasn't been passed already
                                        if kbk_val not in dict_common[doc_id][otkmo_val].keys():
                                            # For these ИдДок, ОТКМО, КБК set zeros
                                            dict_common[doc_id][otkmo_val][kbk_val] = [0, 0, 0, 0, 0]
                                            # Add values
                                            if val_id in values:
                                                idx = values.index(val_id)
                                                dict_common[doc_id][otkmo_val][kbk_val][idx] += float(val)
                                                dict_common[doc_id][otkmo_val][kbk_val][idx] = \
                                                    round(dict_common[doc_id][otkmo_val][kbk_val][idx], 2)
                                        # If this КБК has been passed already
                                        else:
                                            # Add value
                                            if val_id in values:
                                                idx = values.index(val_id)
                                                dict_common[doc_id][otkmo_val][kbk_val][idx] += float(val)
                                                dict_common[doc_id][otkmo_val][kbk_val][idx] = \
                                                    round(dict_common[doc_id][otkmo_val][kbk_val][idx], 2)
                                # Read new line
                                new_line = f.readline()
        # We are still in one .txt file, we have common dict for every different ИдДок, ОТКМО, КБК
        # Create empty pandas DataFrame
        df = pd.DataFrame(columns=columns)
        # Take every key in common dict, i.e. every ИдДокПроходимся по ключам общего словаря, т.е. по ИдДокам
        for IdDok in dict_common.keys():
            # ИдДок consists ИдДок, ДатаДок and ОКВЭД
            # We need to split them by comma
            info_list = IdDok.split(',')
            # If len == 2, it means that ОКВЭД hasn't been found
            # Если длина списка равна 2, т.е. не было найдено ОКВЭДА
            if len(info_list) == 2:
                # Add 0 instead of empty ОКВЭД
                info_list.append('0')
            # Take every key in dict_common[IdDok], i.e. every different ОТКМО for every ИдДок
            for OTKMO in dict_common[IdDok].keys():
                # Take every key in dict_common[IdDok][OTKMO], i.e every different КБК for every
                # ОТКМО for every ИдДок
                for KBK in dict_common[IdDok][OTKMO].keys():
                    # Fill data for pandas DataFrame
                    data = [
                        info_list[0],  # ИдДок
                        DataDok,  # ДатаДок
                        info_list[1],  # ДатаОтч
                        info_list[2],  # ОКВЭД
                        OTKMO,  # ОТКМО
                        KBK,  # КБК
                        dict_common[IdDok][OTKMO][KBK][0],  # 30100
                        dict_common[IdDok][OTKMO][KBK][1],  # 30200
                        dict_common[IdDok][OTKMO][KBK][2],  # 30300
                        dict_common[IdDok][OTKMO][KBK][3],  # 40100
                        dict_common[IdDok][OTKMO][KBK][4]  # 50000
                    ]
                    # Create DataFrame with this data
                    new_df = pd.DataFrame(data=[data], columns=columns)
                    # Concatenate empty and created DataFrame
                    df = pd.concat([df, new_df], ignore_index=True)
        # Create a path by DataDok
        path_to_save = f'CSV/{DataDok}'

        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        # Save CSV, file[:-4].csv means that we will take exactly the same name as .txt file, but with .csv extension
        df.to_csv(f'{path_to_save}/{file[:-4]}.csv')
        # After printing new .txt file will be parsing
        print('Количество различных ИдДок для файла ', file, len(dict_common))
