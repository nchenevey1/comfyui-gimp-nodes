# ComfyUI Nodes for External Tooling Modified for GIMP

* Provides nodes geared towards using GIMP as a frontend for ComfyUI. Modified from https://github.com/Acly/comfyui-tooling-nodes, thank you Acly.
* What changed: Load Image, Load Mask, and Send Image were modified to send, receive, and process base64 encoded RGBA data rather than base64 encoded PNG data.

* <a href="#images">Sending and receiving images</a>
* <a href="#installation">Installation</a>

## <a id="images" href="#toc">Sending and receiving images</a>

### Load Image (GIMP)

Loads an image from an RGBA image embedded into the prompt as base64 string.
* Inputs: base64 encoded binary data of an RGBA image
* Outputs: image (RGB) and mask (alpha) if present

### Load Mask (GIMP)

Loads a mask (single channel) from an RGBA image embedded into the prompt as base64 string.
* Inputs: base64 encoded binary data of an RGBA image
* Outputs: the first channel of the image as mask

### Send Image GIMP (WebSocket)

Sends an output image over the client WebSocket connection as RGBA data.
* Inputs: the image (RGB or RGBA)

This will send one base64 encoded message for the image via WebSocket:
```
12<RGBA-data>
```
That is one 32-bit integer (big endian) with value 12 followed by the base64 encoded RGBA binary data. There is also a JSON message afterwards:
```
{'type': 'executed', 'data': {'node': '<node ID>', 'output': {'images': [{'source': 'websocket', 'content-type': 'image/png', 'type': 'output'}, ...]}, 'prompt_id': '<prompt ID>}}
```
You can see how the data is received in the GIMP plugin at https://github.com/nchenevey1/gimp-comfy-tools

### Send Image with Dimensions GIMP (WebSocket)

Sends an output image over the client WebSocket connection as RGBA data.
* Inputs: the image (RGB or RGBA)

This will send one base64 encoded message for the image via WebSocket:
```
14<RGBA-data>
```
That is one 32-bit integer (big endian) with value 14 followed by the base64 encoded Width (32 bit), Height (32 bit), and RGBA binary data. There is also a JSON message afterwards:
```
{'type': 'executed', 'data': {'node': '<node ID>', 'output': {'images': [{'source': 'websocket', 'content-type': 'image/png', 'type': 'output'}, ...]}, 'prompt_id': '<prompt ID>}}
```
You can see how the data is received in the GIMP plugin at https://github.com/nchenevey1/gimp-comfy-tools

## <a id="installation" href="#toc">Installation</a>

Download the repository and unpack into the `custom_nodes` folder in the ComfyUI installation directory.

Or clone via GIT, starting from ComfyUI installation directory:
```
cd custom_nodes
git clone https://github.com/nchenevey1/comfyui-gimp-nodes.git
```

Restart ComfyUI and the nodes are functional.
