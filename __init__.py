from . import nodes

NODE_CLASS_MAPPINGS = {
    "NC_LoadImageGIMP": nodes.LoadImageGIMP,
    "NC_LoadMaskGIMP": nodes.LoadMaskGIMP,
    "NC_SendImageWebSocketGIMP": nodes.SendImageWebSocketGIMP,
    "NC_SendImageDimsWebSocketGIMP": nodes.SendImageDimsWebSocketGIMP
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "NC_LoadImageGIMP": "Load Image (GIMP)",
    "NC_LoadMaskGIMP": "Load Mask (GIMP)",
    "NC_SendImageWebSocketGIMP": "Send Image GIMP (WebSocket)",
    "NC_SendImageDimsWebSocketGIMP": "Send Image with Dimensions GIMP (WebSocket)"
}
