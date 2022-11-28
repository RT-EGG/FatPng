# FatPng

# About
Adds extra information to the image file and increases the file size arbitrarily.

---
画像ファイルに余分な情報を追加し、ファイルサイズを任意に増加させます。

# How to use
1. Install python. (Confirmed ver.3.10.x as development.)
1. Install requirements by requiments.txt. If you need, setup venv.
1. Run with arguments. (see the [Sample](#Sample))

---
1. Pythonをインストールします. (開発中はver.3.10.xで確認しました.)
1. requiremts.txtを用いて必要なパッケージをインストールします. (必要に応じ、仮想環境を作ってください)
1. 必要な引数を指定し、実行します. ([Sample](#Sample)を参照ください.)

# Sample

1. Run with new black image.
```
python ./src/main.py --width 256 --height 256 --size 1024
```

2. Run with other image as base.
```
python ./src/main.py --input input.png --size 1024
```

# TODO
~~[ ] Release binary~~

[x] Publish as web service.

-> [link](https://rt-egg.github.io/fat-png-web/)
