import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(
    ["ja", "en"],
    gpu=False
)

def read_text(image):

    image = np.array(image)

    results = reader.readtext(
        image,
        detail=0
    )

    return "\n".join(results)