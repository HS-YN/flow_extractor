Extracting dense flow field given a video.

#### Depencies:
- LibZip: 
to install on ubuntu ```apt-get install libzip-dev``` on mac ```brew install libzip```
- Python 3.x

### Install
```
git clone --recursive http://github.com/hs-yn/flow_extractor
cd flow_extractor
sh setup.sh
```

Note that it will take quite a long time to build opencv (depending on your configuration)

### Usage
```
python flow_extractor.py <flag>
```

