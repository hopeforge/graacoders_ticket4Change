import os


class Directory:

    def get_images(self, path):
        file_path_list = []
        for file in os.listdir(path):
            if file.endswith('.jpg') or file.endswith('.jpeg') \
                    or file.endswith('.png'):
                file_path_list.append(os.path.join(path, file))
        return file_path_list
