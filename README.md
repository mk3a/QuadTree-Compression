# QuadTree-Compression
Implements a quadTree based image compression algorithm. The algorithm recursively breaks up an image into quads and then furthere compresses if there is high variance( more detail) in the quads. For example, Quads which are mostly blue are not going to be split further. But a Quad with lots of colors and variances in pixel values will get further split up. This was inspired by Michael Fogleman (https://github.com/fogleman?tab=repositories).

## Samples

### Original Image
