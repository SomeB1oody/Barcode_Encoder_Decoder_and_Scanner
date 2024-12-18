import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image
from pylibdmtx.pylibdmtx import encode

def calculate_check_digit(gtin):
    # 计算GTIN-13编码的校验位。
    total = 0
    for i, digit in enumerate(gtin[:12]):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def generate_gtin(gtin_input):
    # 根据12位输入生成带校验位的完整GTIN-13编码。
    if len(gtin_input) == 12 and gtin_input.isdigit():
        return gtin_input + calculate_check_digit(gtin_input)
    return None

def generate_barcode(gtin, barcode_format):
    # 根据选择生成一维条形码并保存为PNG文件。
    barcode_class = barcode.get_barcode_class(barcode_format)
    barcode_obj = barcode_class(gtin, writer=ImageWriter())
    filename = barcode_obj.save(f"{barcode_format}_Barcode_{gtin}")
    print(f"{barcode_format}Barcode saved as {filename}.png")

def generate_qr_code(data):
    # 生成QR码并保存为PNG文件。
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    filename = f"QRCode_{data}.png"
    img.save(filename)
    print(f"QR code saved as{filename}")

def generate_data_matrix(data):
    # 生成Data Matrix码并保存为PNG文件。
    encoded = encode(data.encode('utf-8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    filename = f"DataMatrix_{data}.png"
    img.save(filename)
    print(f"Data Matrix saved as {filename}")

if __name__ == '__main__':
    while True:
        user_input = input("Please enter a 12-digit number to generate (enter 'Exit' to end):")
        if user_input.lower() == 'exit':
            break
        elif len(user_input) == 12 and user_input.isdigit():
            gtin = generate_gtin(user_input)
            print(f"GTIN-13: {gtin}")

            print("Choose a type:")
            print("1. EAN-13")
            print("2. UPC-A")
            print("3. Code128")
            print("4. QR")
            print("5. Data Matrix")

            choice = input("Enter number (1, 2, 3, 4, 5)：")
            if choice == '1':
                generate_barcode(gtin, 'ean13')
            elif choice == '2':
                generate_barcode(gtin[:11], 'upca')  # UPC-A使用11位数字+校验位
            elif choice == '3':
                generate_barcode(gtin, 'code128')
            elif choice == '4':
                generate_qr_code(gtin)  # 使用GTIN生成QR码
            elif choice == '5':
                generate_data_matrix(gtin)  # 使用GTIN生成Data Matrix码
            else:
                print("Invalid type")
        else:
            print("Invalid input, please enter 12 digits")
