# Application execution

> Without needing to use the command line below (which is intended for technical users)

## Windows

Download the aw client in **[exe](https://github.com/earos-ai/aw-client/tree/master/dist)**.

# Command line run

## 1.Install Git

> To install git-lfs as an additional tool, check out (https://git-lfs.com/)

### Windows

Go to the Git official website(https://git-scm.com/downloads/win) to download the specified version of Git for installation.

### Mac

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git git-lfs
```
### Linux

#### Debian/Ubuntu

For the latest stable version for your release of Debian/Ubuntu

```
# apt-get install git git-lfs
```

For Ubuntu, this PPA provides the latest stable upstream Git version

```
# add-apt-repository ppa:git-core/ppa
# apt update; apt install git git-lfs
```

#### Fedora

`# yum install git git-lfs` (up to Fedora 21)
`# dnf install git git-lfs` (Fedora 22 and later)

#### Gentoo

```
# emerge --ask --verbose dev-vcs/git
```

#### Arch Linux

```
# pacman -S git
```

#### openSUSE

```
# zypper install git
```

#### Mageia

```
# urpmi git
```

#### Nix/NixOS

```
# nix-env -i git
```

#### FreeBSD

```
# pkg install git
```

#### Solaris 9/10/11 ([OpenCSW](https://www.opencsw.org/))

```
# pkgutil -i git
```

#### Solaris 11 Express, OpenIndiana

```
# pkg install developer/versioning/git
```

#### OpenBSD

```
# pkg_add git
```

#### Alpine

```
$ apk add git git-lfs
```

#### Red Hat Enterprise Linux, Oracle Linux, CentOS, Scientific Linux, et al.

RHEL and derivatives typically ship older versions of git. You can [download a tarball](https://www.kernel.org/pub/software/scm/git/) and build from source, or use a 3rd-party repository such as [the IUS Community Project](https://ius.io/) to obtain a more recent version of git.

#### Slitaz

```
$ tazpkg get-install git
```

## 2.Build virtual environment

### Windows
#### Step 1: Download and Install Python 3.9
Navigate to the Python Downloads Page :
Open your web browser and go to the official Python website: python.org/downloads
#### Step 2: Install virtualenv
```
pip install virtualenv
```
#### Step 3: Create a Virtual Environment
```
\your\python3.9version\path\python -m venv venv
```
#### Step 4: Activate the Virtual Environment
```
venv\Scripts\activate
```

### Mac

#### Apple Silicon

```shell
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

#### Intel

```shell
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

### Linux

#### Linux x86

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

#### AWS Graviton2/ARM64

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

#### IBMZ/LinuxOne/s390x

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-s390x.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

## 3.Start running the node 

### Windows
```
venv\Scripts\activate
git clone xxx \your\project\path\aw-node
cd \your\project\path\aw-node
pip install -r requirements.txt
python aw.py
```


### Mac or Linux

```shell
source ~/miniconda3/bin/activate
conda create -y -n aw-node python==3.10
conda activate aw-node
git clone xxx /root/aw-node
cd /root/aw-node
pip install -r requirements.txt
python aw.py
```
