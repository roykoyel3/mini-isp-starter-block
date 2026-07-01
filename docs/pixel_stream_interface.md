# Pixel Stream Interface

## Overview

The 3×3 convolution accelerator processes a continuous stream of 8-bit grayscale pixels using a streaming architecture. Pixels are accepted one clock cycle at a time, buffered using BRAM-based line buffers, assembled into a 3×3 window, filtered using the selected convolution kernel, and streamed out as processed pixels.

The design uses a valid-only streaming interface. A new pixel can be accepted every clock cycle while `valid_in` is asserted.

---

# Top-Level Interface

| Signal | Direction | Width | Description |
|---------|-----------|------:|-------------|
| `clk` | Input | 1 | System clock |
| `rst` | Input | 1 | Active-high synchronous reset |
| `pixel_in` | Input | 8 | Incoming grayscale pixel |
| `valid_in` | Input | 1 | Indicates that `pixel_in` is valid |
| `select_kernel` | Input | 3 | Selects the convolution kernel |
| `pixel_out` | Output | 8 | Filtered output pixel |
| `valid_out` | Output | 1 | Indicates that `pixel_out` is valid |

---

# Parameters

| Parameter | Description |
|-----------|-------------|
| `IMAGE_WIDTH` | Number of pixels per image row |

Example:

```verilog
parameter IMAGE_WIDTH = 1280;
```

---

# Line Buffer Interface

The line buffer stores the previous two image rows using BRAM.

### Inputs

| Signal | Width |
|---------|------:|
| clk | 1 |
| rst | 1 |
| pixel_in | 8 |
| valid_in | 1 |

### Outputs

| Signal | Width | Description |
|---------|------:|-------------|
| current_pixel | 8 | Current input pixel |
| row1_pixel | 8 | Pixel delayed by one image row |
| row2_pixel | 8 | Pixel delayed by two image rows |
| valid_out | 1 | Indicates valid buffered output |

---

# Window Generator Interface

The window generator constructs the 3×3 neighbourhood required for convolution.

### Inputs

| Signal | Width | Description |
|---------|------:|-------------|
| `clk` | 1 | System clock |
| `rst` | 1 | Active-high synchronous reset |
| `valid_in` | 1 | Input data valid signal |
| `current_pixel` | 8 | Current row pixel |
| `row1_pixel` | 8 | Pixel delayed by one image row |
| `row2_pixel` | 8 | Pixel delayed by two image rows |

### Outputs

```
p00 p01 p02
p10 p11 p12
p20 p21 p22
```

Each output represents one pixel of the current 3×3 sliding window.

---

# Convolution Core Interface

The convolution core receives the complete 3×3 window and applies the selected convolution kernel.

### Inputs

```
p00 p01 p02
p10 p11 p12
p20 p21 p22
```
- select_kernel

### Output

| Signal | Width | Description |
|---------|------:|-------------|
| pixel_out | 8 | Filtered output pixel |

---

# Streaming Protocol

The accelerator processes one valid pixel per clock cycle after the pipeline is filled. Data validity is propagated through the processing stages using the `valid_in` and `valid_out` signals, enabling continuous streaming operation.

---

# Data Format

- Pixel format: Unsigned 8-bit grayscale
- Processing: Streaming
- Window size: 3 × 3
- Kernel size: 3 × 3

---

# Supported Kernels

The convolution core supports multiple kernels selected using `select_kernel`.

Examples include:

- Identity
- Blur (Box, Gaussian)
- Sharpen
- Sobel X
- Sobel Y

---

# Design Notes

- Parameterized image width.
- BRAM-based line buffering.
- Streaming pixel-processing architecture
- 3×3 sliding window generation
- Runtime kernel selection
- Modular implementation consisting of separate line buffer, window generator, convolution core, and top-level integration.
