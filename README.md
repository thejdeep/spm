# spm
A tiny package manager. More info <a href="http://localhost:4000/blog/2015/07/02/building-a-package-manager/" target="_blank">here</a>

## Install
```
$ git clone https://github.com/thejdeep/spm.git
$ cd spm/
$ sudo cp spm /bin/
$ sudo chmod +x /bin/spm
$ sudo cp install.py ~/.
```
Sorry for this lame way of installation. Will surely package this when I find time.

## Usage

### To install a package
```
$ spm install <pkg_name>
```
### To remove a package
```
$ spm remove <pkg_name>
```
### To check if package is installed
```
$ spm check <pkg_name>
```
### To list all installed packages
```
$ spm list
```

