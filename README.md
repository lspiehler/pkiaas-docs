## Install Prerequisites
```
apt install libpango-1.0-0 libpangoft2-1.0-0 libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev
python3 -m venv venv/pkiaas-docs
source venv/pkiaas-docs/bin/activate
pip3 install mkdocs-material mkdocs-with-pdf mkdocs-glightbox mkdocs-material[imaging]
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
##