from pyzbar.pyzbar import decode

def read_barcode(image):

    barcodes = decode(image)

    results = []

    for barcode in barcodes:

        results.append(
            barcode.data.decode("utf-8")
        )

    return results