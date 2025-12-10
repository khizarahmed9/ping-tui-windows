# Ping TUI

A simple Text User Interface (TUI) for the Windows `ping` command, built using Python and [Textual](https://textual.textualize.io/).

## Screenshot

<img width="3840" height="2088" alt="image" src="https://github.com/user-attachments/assets/bcb14af1-ed2c-4afe-a855-310c0d4f6c51" />

## Overview

This tool provides a visual wrapper around the standard command-line ping tool. It allows you to toggle flags and set parameters using a graphical interface within your terminal, rather than memorizing or typing out complex CLI arguments.

**Note:** This is designed for **Windows** systems, as it uses Windows-specific flags (e.g., `-n` for count, `-t` for infinite).

## About This Project

I created this primarily to learn how to build Text User Interfaces (TUIs). It is a personal learning exercise and I don't really expect anyone to use this over the standard command line, but feel free to look around if you are interested in the code.

## Features

* **Flag Toggles:** Checkboxes for common options like Infinite loop (`-t`), Resolve hostnames (`-a`), and IP version forcing (`-4`/`-6`).
* **Parameter Inputs:** Easy configuration for Packet Size (`-l`), Timeout (`-w`), TTL (`-i`), and Count (`-n`).
* **Command Preview:** See the exact command string generate in real-time as you adjust settings.
* **Log View:** Executes the ping command and displays the output in a scrollable window.

## Installation

1.  Ensure you have Python installed.
2.  Install the required library:

```bash
pip install textual textual-dev
```
