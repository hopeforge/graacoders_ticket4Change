from PIL import Image
from pyzbar.pyzbar import decode


class ImageDecoder:

    def decode_qr_code(self, image_file):
        return decode(Image.open(image_file))

    def get_decoded_value(self, decoded_image):
        qr_code_value = {}
        for decoded in decoded_image:
            if decoded.type == 'QRCODE':
                decoded_ascii = decoded.data.decode('ascii').split('|')
                qr_code_value['chaveConsulta'] = decoded_ascii[0]
                qr_code_value['timeStamp'] = decoded_ascii[1]
                qr_code_value['valorTotal'] = decoded_ascii[2]
                qr_code_value['CPFCNPJValue'] = decoded_ascii[3]
                qr_code_value['assinaturaQRCODE'] = decoded_ascii[4]
                qr_code_value['QRCODEPolygon'] = decoded.polygon
                qr_code_value['QRCODERectangle'] = decoded.rect
        return qr_code_value
