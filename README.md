# User Study Website for Computer Vision

Flask+React website setup surveys that ask user's preferance of video pairs.

See the [demo client](https://cv-user-study-website-demo.netlify.com/) and [demo server](https://cv-user-study-website.herokuapp.com/show_results)

<kbd> <img src='./doc/screenshot.png' /> </kbd>

## Installation

1. Install miniconda/anaconda, a package for package/environment management
```
wget repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

2. Build conda environment from file
```
conda env create -f environment.yaml
```

3. Activate the environment
```
source activate user_study
```

## How to run
1. Server
```
cd src

# (Please setup the config.py)

# export FLASK_RUN_PORT=5000
# export FLASK_RUN_HOST=0.0.0.0
export FLASK_APP=app.py
flask run
```

2. Client
```
cd client
npm install
export REACT_APP_ENDPOINT=<the path to your server; for example, http://localhost:5000>
# export PORT=3000
npm start
```

## Repository Structure
```
├── .flake8                 Syntax and style settings for Flake8
├── .gitignore              Filenames in this file would be ignored by Git
├── .travis.yml             For Travis CI configuration
├── environment.yaml        For Conda environment
├── README.md
├── LICENSE                 LICENSE file (MIT license here)
├── .github/                For the PR template
├── tests/                  For tests
├── lib/                    For third-party libraries
├── client/                 For React client source code
└── src/                    For Flask server source code

```
## License

MIT 

## Authors

Ya-Liang Chang (Allen) [amjltc295](https://github.com/amjltc295/)


