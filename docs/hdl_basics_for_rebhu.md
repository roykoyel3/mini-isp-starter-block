# HDL Basics

## Introduction

Verilog is a Hardware Description Language (HDL) used to describe digital circuits at the Register-Transfer Level (RTL) for designing and implementing Field Programmable Gate Arrays (FPGAs) and Application Specific Integrated Circuits (ASICs).

In this project, Verilog is used to implement a streaming **3×3 convolution accelerator** on the Microchip PolarFire SoC FPGA. This document introduces the HDL concepts required to understand the RTL implementation of the line buffer, sliding window generator, convolution core, top-level module, and testbench.

---

## Verilog Module Structure

A Verilog design is organized into **modules**, where each module represents an independent hardware block. Larger digital systems are built by connecting multiple modules together.

A typical Verilog module is shown below:

```verilog
module module_name (
    input  wire clk,
    input  wire rst,
    input  wire [7:0] pixel_in,
    output wire [7:0] pixel_out
);

// Internal signal declarations

// Combinational logic

// Sequential logic

endmodule
```

A Verilog module typically contains:

- **Module Declaration** – Defines the module name.
- **Port List** – Declares input and output ports.
- **Internal Signals** – Declares signals such as `wire` and `reg`.
- **Logic Description** – Implements the required functionality.
- **Module Termination** – Ends the module using the `endmodule` keyword.

Verilog supports three modeling styles:

- **Gate-Level Modeling** – Uses basic logic gates.
- **Dataflow Modeling** – Describes hardware using continuous assignments and Boolean expressions.
- **Behavioral Modeling** – Describes hardware functionality using procedural blocks.

This project primarily uses **Behavioral** and **Dataflow** modeling to implement synthesizable RTL.

---

## Data Types

Verilog provides different data types to model hardware signals and storage elements.

### `wire`

A `wire` represents a physical connection between hardware blocks and is driven using continuous assignments.

```verilog
wire valid;
assign valid = enable & ready;
```

### `reg`

A `reg` stores values assigned inside procedural blocks such as `always`.

```verilog
reg [7:0] pixel_out;

always @(posedge clk)
    pixel_out <= pixel_in;
```

### `logic`

`logic` is a SystemVerilog data type that combines many use cases of `wire` and `reg`. Since this project is written in Verilog HDL, `wire` and `reg` are primarily used.

---

## Combinational Logic

Combinational logic produces outputs that depend only on the current input values. It does not require a clock and is commonly implemented using `assign` statements or `always @(*)` blocks.

### Continuous Assignment (`assign`)

```verilog
wire y;

assign y = a & b;
```

### `always @(*)`

```verilog
reg y;

always @(*) begin
    if (sel)
        y = a;
    else
        y = b;
end
```

In this project, combinational logic is used for arithmetic operations, kernel multiplication, addition, and clipping within the convolution datapath.

---

## Sequential Logic

Sequential logic produces outputs based on both the current inputs and the previous state of the circuit. Unlike combinational logic, it requires a clock signal to update stored values.

A clocked `always` block is commonly used to implement registers and flip-flops.

```verilog
reg [7:0] pixel_out;

always @(posedge clk) begin
    pixel_out <= pixel_in;
end
```

### Blocking vs Non-Blocking Assignments

Verilog provides two assignment operators inside procedural blocks.

| Blocking (`=`) | Non-Blocking (`<=`) |
|----------------|---------------------|
| Executes statements sequentially | Updates all registers simultaneously at the end of the clock cycle |
| Commonly used in combinational logic | Commonly used in sequential logic |

For sequential RTL, **non-blocking (`<=`) assignments** are recommended because they correctly model hardware registers.

### Project Relevance

The line buffer, pipeline registers, and output registers of the convolution accelerator are implemented using clocked `always` blocks with non-blocking assignments.

---

## Clock and Reset

A **clock** is a periodic signal that synchronizes the operation of sequential circuits. Registers update their stored values only on the active edge of the clock, ensuring predictable and synchronous hardware behavior.

A **reset** initializes the circuit to a known state during startup or recovery from an error. Resets can be **synchronous** (applied with the clock) or **asynchronous** (applied immediately). Most FPGA designs prefer synchronous resets for better timing and portability.

```verilog
reg [7:0] pixel_out;

always @(posedge clk) begin
    if (rst)
        pixel_out <= 8'd0;
    else
        pixel_out <= pixel_in;
end
```

### Project Relevance

The streaming convolution accelerator uses a clock to synchronize pixel processing and a reset signal to initialize registers and line buffers before processing a new image stream.

---

## Valid/Ready Streaming

Streaming interfaces transfer one data item per clock cycle using handshake signals. The two most common signals are:

- **valid** – Indicates that the sender is providing valid data.
- **ready** – Indicates that the receiver is ready to accept data.

A data transfer occurs only when both `valid` and `ready` are asserted during the same clock cycle.

```verilog
always @(posedge clk) begin
    if (valid && ready)
        pixel_out <= pixel_in;
end
```

This handshake mechanism prevents data loss when one module produces data faster than the next module can process it.

### Project Relevance

The convolution accelerator processes one pixel at a time as a continuous stream. The `valid` and `ready` signals ensure that pixels are transferred correctly between the line buffer, sliding window generator, and convolution core.

---

## Signed Arithmetic, Bit Widths and Fixed-Point Scaling

Digital hardware uses a fixed number of bits to represent data. The selected **bit width** determines the range of values that can be represented and directly affects hardware resource usage.

For image processing, pixel values are typically represented as **8-bit unsigned** numbers (`0–255`). Kernel coefficients, however, may contain **negative values**, requiring **signed arithmetic**.

```verilog
wire signed [7:0] kernel;
wire [7:0] pixel;
wire signed [15:0] product;

assign product = kernel * pixel;
```

Some image-processing algorithms use **fixed-point representation**, where a fixed number of bits represent the fractional part of a value. Fixed-point arithmetic provides a hardware-efficient alternative to floating-point operations.

### Project Relevance

The convolution accelerator processes 8-bit grayscale pixels and multiplies them with signed kernel coefficients. Proper bit-width selection prevents overflow, while fixed-point arithmetic enables efficient hardware implementation without using floating-point units.

---

## Parameters

Parameters allow constant values to be defined once and reused throughout a module. They improve code readability and make the design configurable without modifying the RTL implementation.

```verilog
module line_buffer #(
    parameter IMAGE_WIDTH = 320
)(
    input wire clk,
    input wire rst
);
```

Changing the parameter value automatically updates the module configuration during compilation.

### Project Relevance

Parameters are useful for defining configurable values such as image width, kernel size, and pixel bit width, allowing the convolution accelerator to support different image resolutions with minimal code changes.

---

## Module Instantiation

Large digital systems are built by connecting multiple modules together. This process is known as **module instantiation**, where one module is used as a component inside another module.

```verilog
line_buffer u_line_buffer (
    .clk(clk),
    .rst(rst),
    .pixel_in(pixel_in),
    .pixel_out(pixel_out)
);
```

The instance name (`u_line_buffer`) uniquely identifies the module instance, while the ports connect signals between the parent and child modules.

### Project Relevance

The streaming convolution accelerator is implemented using a hierarchical design. Individual modules such as the line buffer, sliding window generator, convolution core, and top-level module are connected through module instantiation to form the complete image-processing pipeline.

---

## Coding Guidelines for This Project

The following coding practices will be followed throughout this project:

- Use meaningful and consistent module and signal names.
- Keep each module focused on a single functionality.
- Use `wire` for combinational connections and `reg` for sequential logic.
- Use `assign` or `always @(*)` for combinational logic.
- Use `always @(posedge clk)` with non-blocking (`<=`) assignments for sequential logic.
- Parameterize configurable values such as image width and kernel size.
- Use proper indentation and comments to improve code readability.
- Write synthesizable RTL and avoid unnecessary hardware complexity.
- Verify each module independently before integrating it into the complete design.

Following these guidelines improves readability, maintainability, and simplifies debugging and verification during FPGA development.

---

## Summary

This document introduced the fundamental Verilog HDL concepts required for developing the Mini-ISP Starter Block. Topics such as module structure, data types, combinational and sequential logic, clock and reset, streaming interfaces, signed arithmetic, fixed-point representation, parameters, and module instantiation provide the foundation for implementing synthesizable RTL.

The concepts discussed here will be applied throughout the project to design, simulate, verify, and synthesize a streaming **3×3 convolution accelerator** for image filtering on the Microchip PolarFire SoC FPGA.
