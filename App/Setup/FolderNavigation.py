from os import listdir, getcwd
from os.path import join, isdir, basename

class DuplicatedFoldername(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class FolderNavigation:
    def __init__(self):
        self.cwd = getcwd()
        self.folders: dict[str, str] = dict()
        self.files: dict[str, list] = dict()
        self.file_folder_lookup()

    def get_files(self, foldername: str) -> list[str]:
        return self.files[foldername]

    def get_folderpath(self, foldername: str) -> str:
        return self.folders[foldername]

    def get_filepath(self, foldername: str, filename: str) -> str | None:
        if not self.file_exists(foldername, filename):
            raise FileExistsError(f"{filename} not found in {foldername}")
        return join(self.cwd, self.folders[foldername], filename)

    def file_exists(self, foldername: str, filename: str) -> bool:
        return True if filename in self.files[foldername] else False

    def file_folder_lookup(self, relative_path: str="App") -> None:
        absolute_path = join(self.cwd, relative_path)
        basedir = basename(absolute_path)

        if basedir in self.folders.keys():
            raise DuplicatedFoldername("Two folders have the same name! Not cool!")

        self.folders[basedir] = relative_path
        self.files[basedir] = list()

        files = listdir(absolute_path)
        if files.count("__pycache__"):
            files.remove("__pycache__")
        for file in files:
            file_abs_path = join(absolute_path, file)
            file_rel_path = join(relative_path, file)
            if isdir(file_abs_path):
                self.file_folder_lookup(relative_path=file_rel_path)
            else:
                self.files[basedir].append(file)
