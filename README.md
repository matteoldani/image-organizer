# Photo library organizer

Simple tool to give structure to my unorganized picture library. It extracts EXIF and renames and divide the photos based on year and month.

Note: The images will be moved and not copied between the source path and the destination one. 

## Final Structure

```bash
|-- 2002
|   |-- 01
|   |   |-- IMG-20020101-0001.png
|   |-- 02
|   |-- 03
|   |-- 04
|-- 2003
|   |-- 01
|   |-- 02
|   |   |-- IMG-20030201-0001.png
|   |   |-- IMG-20030201-0002.png
|   |-- 03
|   |-- 05
|   |-- 07
|   |-- 08
```

## Disclaimer

This tool did not go under extensive testing. Moreover, the EXIF extraction does not cover all the edge cases and just adopts one fallback method.