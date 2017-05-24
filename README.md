# QuadTree-Compression
Implements a quadTree based image compression algorithm. The algorithm recursively breaks up an image into quads and then further compresses if there is high variance( more detail) in the quads. For example, Quads which are mostly blue are not going to be split further. But a Quad with lots of colors and variances in pixel values will get further split up. This was inspired by Michael Fogleman (https://github.com/fogleman?tab=repositories).

## Samples

#### Original Image
![test2](https://cloud.githubusercontent.com/assets/16367953/26410462/5986da28-4071-11e7-92c3-308c5719dba7.jpg)
#### Low Compression
![lowcompression](https://cloud.githubusercontent.com/assets/16367953/26410427/4436e62c-4071-11e7-9467-f75fbb6f7cb9.png)
#### High Compression
![highcompression](https://cloud.githubusercontent.com/assets/16367953/26410426/443311aa-4071-11e7-97ba-96e56cb01182.png)

