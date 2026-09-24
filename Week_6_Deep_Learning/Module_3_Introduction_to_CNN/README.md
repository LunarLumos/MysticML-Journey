# Module 3 – Introduction to Convolutional Neural Networks (CNN)
> Week 6 · Deep Learning   |   ⬅ Previous: [Module 2 – Introduction to ANN](../Module_2_Introduction_to_ANN)  ·  Next ➡: [Module 4 – Introduction to RNN](../Module_4_Introduction_to_RNN)

## 🎯 Learning Objectives
- Explain why dense networks struggle with images and what CNNs do differently.
- Compute a convolution, ReLU, max-pooling and flatten **by hand** in NumPy.
- See how kernels act as feature detectors (edges, blur, sharpen).
- Build, train and inspect a Keras CNN (Conv2D → MaxPooling2D → Flatten → Dense).

## ✅ Syllabus Checklist
- [x] Introduction to CNN
- [x] Working of CNN
- [x] Convolutional Layer | Pooling | Flatten

## 📖 Concepts

### Why CNNs?
A 224×224 colour image has 150,528 inputs. A dense layer with just 100 neurons would need **15 million** weights, and it would ignore the fact that nearby pixels belong together. CNNs fix this with:
- **Local connectivity:** each neuron looks at a small patch (for example 3×3).
- **Weight sharing:** the same small kernel slides over the whole image, so an edge detector works everywhere.
- **Hierarchy:** edges → textures → parts → objects.

### How a CNN works
```
Image ─► [Conv + ReLU] ─► [Pool] ─► [Conv + ReLU] ─► [Pool] ─► Flatten ─► Dense ─► Softmax
          feature maps     smaller    richer features  smaller   1-D vector   classify
```

### Convolutional layer
Slide a kernel $K$ over the image $I$; at each position multiply element-wise and sum:
$$ S(i,j) = \sum_m \sum_n I(i+m,\, j+n)\, K(m,n) $$
Output size: $\left\lfloor \frac{H + 2P - K}{S} \right\rfloor + 1$ (P = padding, S = stride). `padding="same"` keeps the size.

A vertical-edge (Sobel-x) kernel on a dark|bright image produces large values exactly where the edge is:
```
input            kernel          feature map
0 0 0 9 9       -1 0 1           0 36 36
0 0 0 9 9   *   -2 0 2    =      0 36 36
0 0 0 9 9       -1 0 1           0 36 36
...
```
In a CNN the kernel values are **learned** by backprop, not hand-designed. A `Conv2D(16, (3,3))` layer learns 16 such kernels.

### Pooling
**Max pooling** (2×2, stride 2) keeps the largest value in each block. It halves the width and height, cuts computation, and makes the network tolerant to small shifts. Average pooling takes the mean instead.

### Flatten
Turns the final stack of 2-D feature maps (for example 2×2×32) into a 1-D vector (128 numbers) that normal `Dense` layers can classify.

### Our Keras CNN (sklearn digits, 8×8 grayscale)
| Layer | Output shape | Params |
|---|---|---|
| Conv2D(16, 3×3, same) | 8×8×16 | 160 |
| MaxPooling2D(2×2) | 4×4×16 | 0 |
| Conv2D(32, 3×3, same) | 4×4×32 | 4,640 |
| MaxPooling2D(2×2) | 2×2×32 | 0 |
| Flatten | 128 | 0 |
| Dense(64) + Dropout(0.3) | 64 | 8,256 |
| Dense(10, softmax) | 10 | 650 |

We use sklearn's bundled **digits** dataset (1,797 images, 8×8) so it runs **offline** in seconds. The same design scales to 28×28 **MNIST**; see the full project in [`Projects/MNIST_Digit_Recognition`](../../Projects/MNIST_Digit_Recognition), which needs a one-time download of MNIST.

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_convolution_pooling_numpy.py` | Hand-written `conv2d`, `relu`, `max_pool`: a 5×5 pen-and-paper example, then 4 kernels (Sobel-x/y, blur, sharpen) on sklearn's sample photo `china.jpg`, visualised as conv → ReLU → pool |
| `02_keras_cnn_digits.py` | Keras CNN on sklearn digits: training curves, confusion matrix, classification report, and the **feature maps** of the first conv layer |

## ▶️ How to Run
```bash
cd Week_6_Deep_Learning/Module_3_Introduction_to_CNN
python 01_convolution_pooling_numpy.py
python 02_keras_cnn_digits.py               # --epochs 20 (default)
```
Sample result from our run: **0.978 test accuracy** after 20 epochs (about 15 s on a laptop CPU). Plots are saved to `outputs/`.

## 🧠 Key Takeaways
- Convolution = a sliding, learned feature detector with **shared weights**, so it needs far fewer parameters than dense layers.
- ReLU keeps positive responses; pooling shrinks the maps and adds shift tolerance; flatten hands over to dense layers.
- Deeper conv layers see a larger area of the image and learn more abstract features.
- Keras CNNs expect input shaped `(samples, height, width, channels)`, so add a channel axis for grayscale.

## 📝 Practice Exercises
1. Add a diagonal-edge kernel to `KERNELS` in `01_convolution_pooling_numpy.py` and visualise it.
2. Implement **average pooling** and compare its output with max pooling.
3. Use `stride=2` in `conv2d` and check the output size against the formula.
4. Remove the second Conv/Pool block from the Keras CNN. How do accuracy and parameter count change?
5. Replace the CNN with a plain dense network on the flattened 64 pixels and compare accuracy and parameters.
