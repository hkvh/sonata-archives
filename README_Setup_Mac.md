## Setup Instructions for Mac OS X

The following in an instructional guide for PostgreSQL, Python 3.9 Pipenv Environments and Lilypond that is confirmed to work on Mac OS 13.3 Ventura.

## I. PostgreSQL 15 Localhost Database

This codebase is designed to use PostgreSQL, which you can install at the link [here](https://www.postgresql.org/download/).

Alternatively, you can just use the simple app [here](https://postgresapp.com/downloads.html) which will spin up a localhost server without needing the command line.

I am using version 15, but it should likely work on anything after version 11.

Once you have postgres installed and running locally, you should be able to connect to it in any database IDE (I recommend [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) with the following default connection settings:

* Host: 127.0.0.1
* Port: 5432
* Username: postgres
* Password: postgres
* Database: postgres

These are the connection settings that are configured in credentials.py – if you configure it differently, you can just update that file.

## II. Python 3.9 Development Virtual Environment

This codebase requires using python 3.9+ with some dependencies, and to prevent this from installing these dependencies globally and affecting your default version of python I highly recommend that you use a Pipenv virtual environment to manage this project. 


### 1. Install `pyenv` and desired Python version(s)

To install `pyenv` for the first time, run the following terminal command:

```terminal
$ brew install pyenv
```

To confirm that `pyenv` installed correctly, you can run `pyenv versions` and you should get an output as follows:

```console
* system (set by /Users/<username>/.pyenv/version)
```

When first installed, `pyenv` assigns the system default version of Python (whatever version came installed with the MacOS; may default as 2 or 3) as the global version – this is indicated by the above output.

To ensure that any new versions of Python installed via `pyenv` are properly referenced, run the following set of commands depending on the terminal shell you are using:

- For Bash:

  ```bash
  $ echo -e 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
  $ echo -e 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.bash_profile
  $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
  $ source ~/.bash_profile
  ```

- For zsh:

  ```zsh
  $ echo 'Add pyenv to PATH' >> ~/.zprofile
  $ echo '# eval "$(pyenv init --path)"' >> ~/.zprofile
  $ source ~/.zprofile
  ```

---

Note: If `pyenv` has previously been installed, it may be necessary to upgrade it in order to properly install some newer versions of Python. To upgrade an existing install of `pyenv`, run the following terminal command:

```terminal
$ brew upgrade pyenv
```

---

Next, to install a new version of Python to your computer, run the following code segment (replacing `<python_version>` with the required version):

```terminal
$ pyenv install <python_version>
```

`pyenv`-installed versions of Python are saved to the `.pyenv` folder in the root user directory. The current version of Python that I use is **3.9.10**.

At this point, running `pyenv versions` should output something like the following which will list all versions of Python that have been installed on the computer and that are available to assign globally and/or locally (including to a virtual environment):

```console
* system (set by /Users/<username>/.pyenv/version)
  3.9.10
```

Note: If you need to uninstall a `pyenv` version of Python, you can simply execute the following:

```terminal
$ pyenv uninstall <python_version>
```
### 2. Install `pipenv`

There are two options for installing `pipenv`, either via `homebrew` or `pip`. Either way should typically work fine, though using `homebrew` is recommended.

To install `pipenv` via `homebrew`, run the following terminal command:
```terminal
$ brew install pipenv
```

Note: `homebrew` can only install the latest version of `pipenv` while `pip` is able to install older versions of `pipenv` if needed (may be required to be able to install some older versions of Python). If `pip` is used, be sure to use the version compatibile with the Python version that will be installed in the virtual environment (which can be accomplished easily by setting the global or local `pyenv` Python version, discussed in a later section of this document).

### 3. Create sonata-archives virtual environment with pipenv

Note: If using the latest version of PyCharm, you can skip to step 4 as it can do this for you.

To create a new virtual environment with a specific version of Python, simply navigate to the base directory of the sonata-archives on your computer and execute the following:

```terminal
$ pipenv install --python 3.9.10
```


An environment will be created called `sonata-archives-<id>` and can be found within the `~/.local/share/virtualenvs` folder or in `~/.virualenvs` (I'm not sure what controls which one it ends up in) within the root user directory on your computer.

All packages needed for the project are specified within the `Pipfile` and `Pipfile.lock` files located in the root directory of sonata-archives. Those packages will be installed at the same time the environment is created.

If you make a mistake during installation or need to change the Python version assigned to the virtual environment, do so by navigating to the base directory of the repo/folder and removing the virtual environment completely with the following command (and then recreating):

```terminal
$ pipenv --rm
```

### 4. Optional: Configuring the PyCharm IDE to use your virtual environment

Although you are free to use whatever text editor or IDE you want to work on this project, I prefer [JetBrains PyCharm](https://www.jetbrains.com/pycharm/).

When you open sonata-archives, if you are using a current version of PyCharm (after 2022) it should see the Pipfile and ask to create the
Pipenv environment for you automatically.

However, if you have already made it from Step 3 and want to point to it:

Navigate to: PyCharm--> Settings --> Project: sonata-archives --> Project Interpreter --> Add Interpreter --> Add Local Interpreter

Find the path to your previously-created environment which should be as follows:

      ```console
      /Users/<username>/.local/share/virtualenvs/sonata-archives-<id>/bin/python
      ```

Make sure that you choose the python executable in the bin folder, which should be around ~10 KB, not an alias (which will only be a few bytes)


## III. Lilypond 2.24

GNU Lilypond is the software that this repository uses to convert a markup text into musical images.

First install Lilypond 2.24 [here](https://lilypond.org/doc/v2.23/Documentation/web/macos-x).

After it's installed, configure it so that you can execute it from the command line which you can read about on that link; in most cases, this should mean adding the following line to your `~/.zshrc`:

```zsh
export PATH=$PATH:~/lilypond-2.24.1/bin
```

Where in this case I've put the extracted lilypond-2.24.1 archive in the root `~` directory.

Finally, to confirm that lilypond is set-up properly, open up a new terminal (must close an existing one if you had it open)
and run:

`$ lilypond --version`

If this doesn't work, make sure that your path is actually pointing at the proper bin folder.