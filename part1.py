from pathlib import Path
import sys
import shutil
import os
from multithreading import MyThread

path = Path("C:\Le Croissant\Projects\A messy folder")
reference_path = path


CYRILLIC_SYMBOLS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = ("a", "b", "v", "g", "g", "d", "e", "ye", "j", "z", "y", "i", "yi", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "yu", "ya")
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()






def normalize(name):                       # Нормалізує імена файлів, перекладаючи все на латиницю і позбуваючись спец. символів
    
    name = str(name).translate(TRANS)
    suffix = '.' + name.split('.')[-1]
    name = name.removesuffix(suffix)
    for ch in name:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or '0' <= ch <= '9' or ch == '_':
            continue
        name = name.replace(ch, '_')            
    name = name + suffix
    return name





reference_extentions = {('.jpeg', '.png', '.jpg', '.svg'):                    'images',
                        ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):  'documents',
                        ('.mp3', '.ogg', '.wav', '.amr'):                     'audio',
                        ('.avi', '.mp4', '.mov', '.mkv'):                     'video',
                        ('.zip', '.gz', '.tar'):                              'archives'}

sorted_items =         {'images':         [], #зображення ('JPEG', 'PNG', 'JPG', 'SVG')
                        'documents':      [], #документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
                        'audio':          [], #музика ('MP3', 'OGG', 'WAV', 'AMR')
                        'video':          [], #відео файли ('AVI', 'MP4', 'MOV', 'MKV')
                        'archives':       [], #архіви ('ZIP', 'GZ', 'TAR')
                        'unknown_files':  []} #невідомі розширення

known_extentions = set()
unknown_extentions = set()
folders_to_not_touch = []




def sort_items_by_type(path, reference_path):                                                          # робить огляд файлів і папок, нормалізує імена та складає списки файлів на сортування
    
    for content in path.iterdir():
        if content.is_dir():
            if content.name in sorted_items.keys() and path == reference_path:
                folders_to_not_touch.append(content)
                continue
            elif os.listdir(content) == []:                                                            # якщо папка порожня, вона одразу видаляється
                #print(f'folder {content.name} is empty')
                os.rmdir(content)
            else:
                new_thread = MyThread()                                                                # подальша обробка папки проводиться у окремому потоці
                new_thread.run(sort_items_by_type, content, reference_path)
                # sort_items_by_type(content)
        else:
            new_name = os.path.join(content.parent, normalize(content.name))
            new_file = Path(new_name)
            os.rename(content, new_name)
            is_sorted = False
            for key, value in reference_extentions.items():
                if str(new_file.suffix).lower() in key:
                    sorted_items[value].append(new_file)
                    known_extentions.add(new_file.suffix)
                    is_sorted = True
                    break
            if is_sorted == False:
                sorted_items['unknown_files'].append(new_file)
                unknown_extentions.add(new_file.suffix)      
    #print(sorted_items)

    if known_extentions == set():
        known_extentions.add('No known extentions were met')
    if unknown_extentions == set():
        unknown_extentions.add('No unknown extentions were met')

    
    return sorted_items, known_extentions, unknown_extentions, folders_to_not_touch




def file_operations(sorted_items, folders_to_not_touch):          #  Створює папки для всіх типів файлів та переміщує у них файли, згідно зі списком
    names_of_folders_to_not_touch = []
    for folder in folders_to_not_touch:
        names_of_folders_to_not_touch.append(folder.name)
 

    for key, value in sorted_items.items():
        new_path = os.path.join(path, key)
        if key not in names_of_folders_to_not_touch:
            os.mkdir(new_path)
        for a_file in value:
            try:
                shutil.move(a_file, new_path)
            except:
                os.remove(a_file)
             
    return





def work_with_archives(path):                                      #     Розпаковує архіви у папки                   
    path_to_archives = Path(os.path.join(path, 'archives'))
    for content in path_to_archives.iterdir():
        if content.is_file():
            suffix = '.' + str(content.name).split('.')[-1]
            if suffix in ['.zip', '.gz', '.tar']:
                folder_name = content.name.removesuffix(suffix)
                target_folder = os.path.join(path_to_archives, folder_name)
                os.mkdir(target_folder)
                shutil.unpack_archive(content, target_folder)
                os.remove(content)

    return





def cleanup(path):                                              #   Робить зачистку порожніх папок
    for content in path.iterdir():
        if content.is_dir(): 
            if os.listdir(content) == []:
                os.rmdir(content)
            else:
                cleanup(content)

    return




sorted_list_of_items = sort_items_by_type(path, reference_path)
folders_to_not_touch = sorted_list_of_items[3]
file_operations(sorted_list_of_items[0], folders_to_not_touch)
work_with_archives(path)
cleanup(path)

for key, value in sorted_list_of_items[0].items():   
    print(f'Files: {value} were moved to folder {key}')
print(f'Known extentions found: {sorted_list_of_items[1]}\nUnknown extentions found: {sorted_list_of_items[2]}')
