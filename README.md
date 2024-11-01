## Install Prerequisites
```
python3 -m venv venv/pkiaas-docs
source venv/pkiaas-docs/bin/activate
pip3 install mkdocs-material
#deactivate when done
#deactivate
```

## Create Documentation
```
mkdocs new .
```

## Test
```
mkdocs serve -a 0.0.0.0:8000
```

## Deploy
```
mkdocs gh-deploy
```