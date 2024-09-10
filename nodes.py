from __future__ import annotations
from PIL import Image
import numpy as np
import base64
import torch
from server import PromptServer


class LoadImageGIMP:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": (
                    "STRING", {"multiline": False}
            ),
            "width": (
                    "INT",
                    {"default": 512, "min": 0, "max": 8192, "step": 1},
            ),
            "height": (
                "INT",
                {"default": 512, "min": 0, "max": 8192, "step": 1},
            )
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    CATEGORY = "external_tooling"
    FUNCTION = "load_image"

    def load_image(self, image, width, height):
        imgdata = base64.b64decode(image)
        img = Image.frombytes("RGBA", (width, height), imgdata)
        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        img = img.convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]

        return (img, mask)


class LoadMaskGIMP:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "mask": ("STRING", {"multiline": False}),
            "width": (
                    "INT",
                    {"default": 512, "min": 0, "max": 8192, "step": 1},
            ),
            "height": (
                "INT",
                {"default": 512, "min": 0, "max": 8192, "step": 1},
            )
            }
        }

    RETURN_TYPES = ("MASK",)
    CATEGORY = "external_tooling"
    FUNCTION = "load_mask"

    def load_mask(self, mask, width, height):
        imgdata = base64.b64decode(mask)
        img = Image.frombytes("RGBA", (width, height), imgdata)
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)
        if img.dim() == 3:  # RGB(A) input, use red channel
            img = img[:, :, 0]
        return (img.unsqueeze(0),)


class SendImageWebSocketGIMP:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE",)
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "send_images"
    OUTPUT_NODE = True
    CATEGORY = "external_tooling"

    def send_images(self, images):
        results = []
        for tensor in images:
            array = 255.0 * tensor.cpu().numpy() 
            image = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            rgb_data = Image.new("RGBA", image.size, (255, 255, 255, 0))
            rgb_data.paste(image)
            image_bytes = rgb_data.tobytes()
            image_bytes = base64.b64encode(image_bytes)

            server = PromptServer.instance
            server.send_sync(
                12,
                image_bytes,
                server.client_id,
            )

            results.append(
                # Could put some kind of ID here, but for now just match them by index
                {"source": "websocket", "content-type": "image/png", "type": "output"}
            )

        return {"ui": {"images": results}}