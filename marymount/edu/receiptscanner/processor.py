from PIL import Image
import pytesseract

from marymount.edu.receiptscanner.encryption import AESCipher
from marymount.edu.receiptscanner.logger import log_event
from marymount.edu.receiptscanner.validation import validate_file

cipher = AESCipher("demo-key")

class ReceiptScanner:

    def parse_image(self, image_path):

        validate_file(image_path)
        log_event("SECURITY", "File validated")

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        log_event("OCR", "Text extracted")

        encrypted = cipher.encrypt(text)

        log_event("ENCRYPTION", "Data encrypted")

        return encrypted