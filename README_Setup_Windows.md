## Setup Instructions for Windows 10

## TODO Fill this out

The following in an instructional guide for PostgreSQL, Python 3 Conda Environments and Lilypond that is confirmed to work on Mac OS 10.13, but should work on most non-ancient versions of Mac OS X.

## I. PostgreSQL 9.6 Localhost Database

This codebase is designed to use PostgreSQL, which you can install at the link [here](https://www.postgresql.org/download/).

I am using version 9.6, but version 10 should also work. Do not install any version prior to 9 as it will likely NOT work.

Once you have postgres installed and running locally, you should be able to connect to it in any database IDE (I recommend [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) with the following default connection settings:

* Host: 127.0.0.1
* Port: 5432
* Username: postgres
* Password: postgres
* Database: postgres

These are the connection settings that are configured in credentials.py – if you configure it differently, you can just update that file.

## II. Python 3.6 Development Virtual Environment

This codebase requires using python 3.6+ with some dependencies, and to prevent this from installing these dependencies globally and affecting your default version of python (probably v2.7.X), I highly recommend that you use a virtual environment to manage this project. 

I found using virtualenv and virtualenvwrapper difficult, and I recommend using conda as I found it to be simpler and a bit nicer.

However, I will maintain both a requirements.txt and an environment.yml, which will enable you to still use whatever virtual environment method you please.

If you have experience using some other virtualenvironment, feel free to set that up, and you can skip the rest of this section and install all dependencies in the usual way running:

`$ pip install -r requirements.txt`

But if you do choose to use conda as I recommend, here is the guide:

#### 1. Download and Install the latest Anaconda3 for Python 3

Install Anaconda3 for Python 3.6+ at the link [here](https://www.continuum.io/downloads).

You can obviously choose the command line or graphical installer, but I'd recommend the command line installer because it's faster.

You may also see something about miniconda which I have played around with and tried, but I had errors using it, so I'd recommend that you install the full anaconda.

If you've already installed conda ages ago, run `$ conda update --prefix /Users/<YourName>/anaconda3 anaconda` and it will ask you if you want to update everything.

#### 2. Confirm that your `python` command now runs Conda's installation of python

Before installing anaconda, executing `$ which python` should produce `/usr/bin/python` and running `$ python` would likely start a session of python 2.7.X.

If the anaconda3 installer worked successfully, executing `$ which python` should now point to `/Users/<YourName>/anaconda3/bin/python`, and running `$ python` should start a session of python 3.6.X.

If this didn't work, perhaps your `.bash_profile` is a mess due to earlier installations of things like virtualenv and virtualenvwrapper.

Open your `.bash_profile` and delete or comment out anything relating to those and make sure you have a line like this:

```
# added by Anaconda3 4.4.0 installer
export PATH="/Users/<YourName>/anaconda3/bin:$PATH"
```
Once you've fixed your `.bash_profile`, close out your terminal and open a new one and now `$ which python` point to the right place.

#### 3. Create the sonata-archives virtual environment

There are two ways to create the sonata-archives virtual environment:

1. Create a new empty environment with `$ conda create --name sonata-archives python=3`. Choose yes to create the environment with a few default conda packages.

	Activate the environment with `$ source activate sonata-archives ` and you should see `(sonata-archives) ~$` before your shell.
	
	You can confirm that it is empty of pip-installed python packages by running `(sonata-archives) $ pip freeze` which should return nothing, but conda added a few aforementioned conda-installed default packages (including openssl, wheel and pip), so `(sonata-archives) $ conda list` will not be empty.

	Now that you are in your conda environment, you are able to use pip to install all the requirements: simply run:

	`(sonata-archives) $ pip install -r requirements.txt`
	
	This will install all the python requirements with pip which beautifully integrates into your conda environment.

2. Create the sonata-archives conda environment directly from the `environment.yml` configuration by running:

	`$ conda env create environment.yml`

	This should create an environment named `sonata-archives` with all necessary conda and pip packages that you can activate via `$ source activate sonata-archives`.
	
*Note*: If you messed this up and need to remove your environment to start from scratch, first deactivate it with `source deactivate` and then you can remove it with `conda remove --name sonata-archives --all`. 

(You can see a list of all your envs with `conda info --envs`)

*Additional Note*: If you chose not to use conda for your environment, the first method above can be easily adapted to pyenv/virtualenv where you setup a `sonata-archives` empty env and then run `$ pip install -r requirements.txt`

### 4. Adding new dependencies / Installing new packages

In general, you can view your pip-installed packages in any python environment (conda or not) with the simple command `$ pip freeze`.

But in a conda environment you can also run: `$ conda list`, a more robust command that will show you both the conda-installed packages and the pip-installed packages.

Although conda can be used to install new packages, I want to support all kinds of envs by keeping a normal python requirements.txt, so **DO NOT USE CONDA TO INSTALL ANY PYTHON PACKAGES - ALWAYS USE PIP**. If you have to install some package that only conda can do and not pip, then that is a different issue and might motivate forcing everyone to use conda envs.

But since almost everything is available via pip and pip integrates seamlessly with your conda env (once you have activated it with `$ source activate sonata-archives`), all you need to do is use pip to install a package in the usual way:

`(sonata-archives) $ pip install somepackage`

When you have installed everything that you need (and have confirmed this with `$ pip freeze` / `$ conda list` that things are working, **run the bash script update_dependencies.sh**:

`(sonata-archives) $ bash update_dependencies.sh`

This bash script will update both the pip requirements.txt and the conda environment.yml files (and will allow both methods of section 3 to work for collaborators). This is why it is so important to install packages with only pip, because a pip-installed package enteres the requirements.txt and the environment.yml file, while a conda-installed package would only enter the environment.yml.

*Note*: My simple bash script is a wrapper to both `$ pip freeze` and `$ conda env export` where I grep out the "prefix" stored in the latter command so that our local anaconda path is not in the file designed to be shared with others)

*Additional Note*: if you messed something up by installing a package in your virtual environment that clashes with something and want to uninstall everything to get a fresh start, you can do this nifty command:

`pip freeze | xargs pip uninstall -y`

And then you can fix things in the requirements.txt and run `pip install -r requriements.txt`. Of course, never only change something only in requirements.txt and not environment.yml - be sure to run the bash script `update_dependencies.sh` to make both the two files match.

### 5. Optional: Configuring the PyCharm IDE to use your virtual environment

Although you are free to use whatever text editor or IDE you want to work on this project, I prefer [JetBrains PyCharm](https://www.jetbrains.com/pycharm/).

When you open sonata-archives, by default the Project will be configured to use your default version of Python, which is not what we want.

At least in version 2017.2, to change this, go to:

PyCharm--> Preferences --> Project: sonata-archives --> Project Interpreter --> <Click on the gear> --> Add Local

Then navigate to the python executable in your virtualenv folder which for the conda files should be at: 

`~/anaconda3/envs/sonata-archives/bin/python3.6`

Make sure that you choose the python executable in the bin folder, which should be around ~10 KB, not an alias (which will only be a few bytes)


## III. Lilypond 2.18

GNU Lilypond is the software that this repository uses to convert a markup text into musical images.

First install Lilypond 2.18 following the instructions [here](http://lilypond.org/macos-x.html).

After it's installed, configure it so that you can execute it from the command line.

In most cases, this should mean adding the following line to your `~/.bash_profile`:

`export PATH="$PATH:/Applications/LilyPond.app/Contents/Resources/bin/"`

Finally, to confirm that lilypond is set-up properly, open up a new terminal (must close an existing one if you had it open)
and run:

`$ lilypond --version`

If this doesn't work, make sure that your path is actually pointing at the proper bin folder inside the package contents of the Lilypond.app