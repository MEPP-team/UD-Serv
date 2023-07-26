A small script that was used in the vegetation project. It is made to convert .ply files to .obj files, keeping the vertex colors.

# Installation

```shell
python3 -m venv venv
. venv/Scripts/activate

(venv)$ pip install -r requirements.txt
```

# Usage

```shell
python convertPLYtoOBJ.py -p [your_path]

# The output will be inside a folder named 'obj' inside of your_path
```
