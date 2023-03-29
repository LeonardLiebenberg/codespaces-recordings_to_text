import os
import paramiko
import random

class FilePathManager:
    def __init__(self, root_path: str) -> None:
        self.root_path = root_path

    def navigate(self, directory_path: str) -> str:
        """Joins paths relative to the root path."""
        return os.path.abspath(os.path.join(self.root_path,"{}".format(directory_path)))
    
    def make_directory(self, *args: str) -> str:
        """Creates a new directory relative to the root path."""
        path = self.join_paths(*args)
        os.makedirs(path, exist_ok=True)
        return path

    def remove_files(self,file_list: list, directory: str) -> None:
        """Deletes all files in the specified directory."""
        for file in file_list:
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file}")
                else:
                    print(f"File {file} does not exist in {directory}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")


    def list_files(self, directory_path: str) -> list[str]:
        """Lists all files in a directory relative to the root path."""
        path = self.navigate(directory_path)
        if os.path.isdir(path):
            return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return []

    def list_directories(self, *args: str) -> list[str]:
        """Lists all directories in a directory relative to the root path."""
        path = self.join_paths(*args)
        if os.path.isdir(path):
            return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return []


class SFTPFileManager:
    def __init__(self,sftp_connection: paramiko.SFTPClient,sftp_root: str) -> None:
        self.sftp = sftp_connection
        self.root_path = sftp_root #"/"
        
    
    def close(self):
        if self.sftp is not None:
            self.sftp.close()
    
    def list_dir(self):
        if self.sftp is None:
            self.connect() 
        files = []
        self.sftp.chdir(self.root_path)
        for file in self.sftp.listdir():
            files.append(file)
        
        return files
  
    def newest_dir(self) -> str:
        folder_list = self.list_dir()
        folder_list.sort(key=lambda x: self.sftp.stat(x).st_mtime, reverse=True)
        latest_folder = folder_list[0]
        return self.root_path + latest_folder
    
    def download_recordings(self,remote_path: str,target:str) -> None:
        self.sftp.chdir(remote_path)
        ogg_files = [filename for filename in self.sftp.listdir() if filename.endswith('.ogg')]
        large_ogg_files = [filename for filename in ogg_files if self.sftp.stat(filename).st_size > 5 * 10240]
        random_ogg_files = random.sample(large_ogg_files, min(len(large_ogg_files), 5000))

        for file in large_ogg_files:
            self.sftp.get(remote_path + '/' + file, target + '/' + file)        
         
        self.sftp.close()

    

        