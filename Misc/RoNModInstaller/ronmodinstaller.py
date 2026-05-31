import zipfile
import rarfile
import py7zr
import os
Disk = "D"
mods_folder = r"C:\Users\ayomi\Desktop\Files\RoNModInstaller\Mods"
paks_folder = Disk+":\SteamLibrary\steamapps\common\Ready Or Not\ReadyOrNot\Content\Paks"

zips = os.listdir(mods_folder)

for file in zips:
    print(f"Extracting: {file}")
    if file.endswith(".zip"):
        with zipfile.ZipFile(os.path.join(mods_folder, file), 'r') as zip_ref:
            all_files = zip_ref.namelist()
            files_to_extract = [file for file in all_files if file.endswith(".pak")]
            num = len(files_to_extract)
            for file in files_to_extract:
                zip_ref.extract(file, paks_folder)
            print(f"Extracted: {num} pak(s)")
            os.unlink(file)
    elif file.endswith(".rar"):
        with rarfile.RarFile(os.path.join(mods_folder, file), 'r') as rar_ref:
            all_files = rar_ref.namelist()
            files_to_extract = [file for file in all_files if file.endswith(".pak")]
            num = len(files_to_extract)
            for file in files_to_extract:
                rar_ref.extract(file, paks_folder)
            print(f"Extracted: {num} pak(s)")
            os.unlink(file)
    elif file.endswith(".7z"):
        with py7zr.SevenZipFile(os.path.join(mods_folder, file), 'r') as z_ref:
            all_files = z_ref.getnames()
            files_to_extract = [file for file in all_files if file.endswith(".pak")]
            num = len(files_to_extract)
            for file in files_to_extract:
                z_ref.extract(file, paks_folder)
            print(f"Extracted: {num} pak(s)")
            os.unlink(file)