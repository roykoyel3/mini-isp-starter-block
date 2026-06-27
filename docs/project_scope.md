# Project Scope

## Project Overview

**Project:** FPGA Mini-ISP Starter Block

The objective of this project is to design and verify a reusable streaming **3×3 convolution accelerator** in Verilog HDL for the **Microchip PolarFire SoC (MPFS025T / BeagleV-Fire)** FPGA platform.

The accelerator processes **8-bit grayscale image streams** using configurable 3×3 convolution kernels and is intended to serve as a reusable hardware block for future FPGA-based Image Signal Processing (ISP) pipelines. The project focuses on developing a synthesizable RTL design, validating it against a Python reference model, and documenting the complete development and verification workflow.

---

## Project Objectives

* Design a synthesizable streaming 3×3 convolution accelerator in Verilog HDL.
* Process 8-bit grayscale image streams using a streaming pixel interface.
* Support multiple 3×3 image filtering kernels, including Identity, Blur, Sharpen, Sobel X, and Sobel Y.
* Develop a Python golden model for functional verification.
* Develop the entire RTL code for 3×3 convolution accelerator in Libero SoC.
* Verify the RTL implementation through simulation and comparison with the Python reference model.
* Synthesize the design using Libero SoC and document FPGA resource utilization.

---

## In Scope

The following items are included within the scope of this project:

* Streaming 8-bit grayscale image processing.
* Pixel streaming interface definition.
* Python golden reference model.
* Line buffer implementation.
* 3×3 sliding window generation.
* Streaming convolution engine.
* Image conversion utilities for simulation.
* RTL simulation and functional verification.
* FPGA synthesis using Libero SoC.
* Resource utilization reporting.
* Project documentation and repository maintenance.

---

## Out of Scope

The following items are intentionally excluded from the current project scope:

* CNN acceleration or neural network inference.
* Object detection or image classification.
* Complete Image Signal Processing (ISP) implementation.
* Camera sensor interface development.
* RGB or multi-channel image processing.
* Runtime kernel reconfiguration through external interfaces.

---

## Deliverables

The project is expected to produce the following deliverables:

* Python golden model for 3×3 convolution.
* Image conversion scripts.
* Verilog RTL implementation of the streaming convolution accelerator.
* RTL testbenches and verification environment.
* Regression scripts for automated comparison.
* Sample input and output images.
* FPGA synthesis and resource utilization reports.

