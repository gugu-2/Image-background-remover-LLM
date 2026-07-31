# CLI Usage Guide

The `bg-remover` command-line tool allows developers and users to quickly remove backgrounds from images directly from their terminal.

## General Syntax

```bash
bg-remover --input <path_to_input> --output <path_to_output>
```

You can also use the short flags `-i` and `-o`:
```bash
bg-remover -i <path_to_input> -o <path_to_output>
```

## Processing a Single Image

To remove the background from a single image file, provide the path to the image as the input, and the desired destination path as the output.

```bash
bg-remover --input my_photo.jpg --output my_photo_nobg.png
```

> [!TIP]
> The output format should always be `.png` to support transparency (the alpha channel). If you specify a different extension, the background might render as black or white depending on the image viewer.

## Processing a Folder in Batch

If you have a directory full of images and you want to process all of them at once, simply provide the folder paths!

```bash
bg-remover --input ./raw_images/ --output ./clean_images/
```

- The tool will automatically create the output directory if it does not exist.
- It will scan the input directory for supported image formats (`.png`, `.jpg`, `.jpeg`, `.webp`).
- All processed images will be saved in the output directory with `_nobg` appended to their original filenames (e.g., `image1_nobg.png`).

## Help Command

If you ever forget the arguments, run:

```bash
bg-remover --help
```
