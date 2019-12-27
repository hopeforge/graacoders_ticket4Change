from image_analyzer.directory import Directory
from image_analyzer.exporter import Exporter
from image_analyzer.image_decoder import ImageDecoder


class Main:

    def main():
        directory = Directory()
        path_in = 'D:\\Desktop\\image_analyzer\\data\\input\\'
        path_out = 'D:\\Desktop\\image_analyzer\\data\\output\\'
        image_files = directory.get_images(path_in)

        decoder = ImageDecoder()

        exporter = Exporter()

        for image in image_files:
            decoded_image = decoder.decode_qr_code(image)
            list_to_export = decoder.get_decoded_value(decoded_image)
            if bool(list_to_export):
                exporter.write_csv(path_out, 'cupom_fiscal', list_to_export)

    if __name__ == "__main__":
        main()