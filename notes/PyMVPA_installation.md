# PyMVPA installation

Had trouble installing PyMVPA with Python3 on OSX 10.12.6.

Instead had to do the following steps:

### Download & install Anaconda distro of Python2.7
https://anaconda.org/

### Install dependencies
http://www.ccnlab.net/python/ 

```
conda install matplotlib numpy scipy ipython statsmodels networkx 
```

```
pip install -U scikit-learn nipy nibabel
```


### Install PyMVPA
```
cd ~
git clone git://github.com/PyMVPA/PyMVPA.git
cd PyMVPA
make 3rd
python setup.py build_ext
python setup.py install
```

### Misc...

The anaconda python distribution may change your default 'jupyter' install. 

>which jupyter

may now yield:

>/anaconda2/bin/jupyter

And while there seems to be the option of running a Python3 kernel from this new Jupyter, not sure if it is pointing to a anaconda python3 or the one you've already set up. 

If you've previously set up jupyter for Python3 using *pip3*, you can create an alias to explicity point to this version of jupyter. 

```
cd ~
emacs .bash_profile
```

and type

> alias jupyter3="/usr/local/bin/jupyter"


