# sonata-archives
A repository to build a sonata theory database for all sonatas in the classical common practice period.

## I. Development Environment Setup

To work on this project, you first must properly set up:

* PostgreSQL 9.6
* Python 3.6+ (virtual environment highly recommended)
* Lilypond 2.18

Here are some detailed guides that walk you throught the steps on how to set these up:

* [Mac OS X](README_Setup_Mac.md)
* [Windows 10](README_Setup_Windows.md)

Note that if you haven't worked on it in a while, dependencies may have changed since you last pulled, so it's recommended to first run the following from inside your `sonata-archives` virtual environment / conda environment before running other code:

`(sonata-archives) $ pip install -r requirements.txt`

## II. Building the Sonata Archives Database

To build for the first-time (or rebuild) the sonata-archives database with all composers, pieces and sonatas that live in the `data` directory, simply execute the root-level script:
 
`rebuild_database.py`

This script requires a valid connection to postgres; if you are having connection issues, make sure that your `credentials.py` file matches your setup Postgres credentials.

If you make changes to the attributes of an existing piece or add a new analysis, you should just re-run this script, as it is extremely fast for the database to fully refresh by rebuilding itself.

## III. Rendering Lilypond Score Excerpts

All rendered lilypond images are stored in `app/static/lilypond/`) but the files are not stored in source control (see `.gitignore`). 

Eventually, the files will be stored somewhere like S3, but for now this means that to make all the `.png` files that you will need in order to see the score excerpts, you must first run the following root level script:

`render_all_lilypond.py`

If you are adding additional lilypond files or making changes to existing ones, you can always run the full script and render everything, but because it can take a while, it is advisable to run it with a provided `filename_list` where you list only the specific `.ly` files that need re-rendering.

## IV. Viewing the Sonata Archives Website

### 1. Make sure the database is built

If you haven't already, make sure to follow step II above to build the database as you will need a connection to it in order to have the website display any information.

### 2. Make sure all lilypond images are rendered

If you haven't already, make sure to follow step III above and render all the lilypond files or you will not be able to see most of the image files on the website.

### 3. Start the Flask Web Server

To start the Flask web server in localhost, run the script `app/app.py`

If this works you should see information about `Running on http://127.0.0.1:5000/`

If you get errors, make sure your have installed all dependencies (Flask has many of them) from `requirements.txt`

### 4. View the Website!

Now you can view the website that your webserver is hosting by entering the URL `http://127.0.0.1:5000/` into your browser (Chrome recommended).

## VI. Contributing Analyses to the Sonata Archives

Adding analyses is very easy with the existing framework and does not require detailed knowledge in how the code actually works - simply add or modify files in the `data` directory following the very obvious-to-copy templated formats for the analyses already there!

But to give a bit more details on some nuances:

### 1. Adding a composer

To add a new composer, simply create a new subclass of `ComposerDataClass` and store the class in the `data/composers.py` file. 

You can fill out as much of the `composer_attribute_dict` as you'd like, but make sure to at least give the composer an `ID`, `SURNAME` and `FULL_NAME`.

For the `ID`, usually just choose a concise version of the surname with first initial if necessary.

Examples:

* `mozart` 
* `beethoven`
* `rstrauss`

### 2. Adding a new piece

To add a new piece, first choose a `piece_id` unique identifier for your piece – put the composer's id as the first part of it and include the piece type and number or catalogue number to make it an unambiguous id.

Examples:

* beethoven5
* mozartk330

Then create a new file in `data/<composer_id>/<piece_id>.py` where `composer_id` is the composer of the piece.

In this module, create a new subclass of `PieceDataClass` and fill out as much of the `piece_attribute_dict` as you'd like, but make sure to at least fill out the `ID`, `COMPOSER_ID` and `NAME`.

* `ID` should be a string with same name as the module 
* `COMPOSER_ID` should not be entered as a string; instead import your composer class from `data.composers` and use its `id()` function.
* `NAME` should be just the name of the piece without any nicknames or catalogue ids such as opus numbers. 
	* To add those, fill out `NICKNAME` and/or `CATALOGUE_ID`

Note that if directories start getting cluttered (e.g. there are too many piece modules under `data/beethoven/`), feel free to create as many subfolders under the composer as you would like (e.g. `data/beethoven/symphonies/`, `data/beethoven/piano_sonatas/`). The code that rebuilds the database will recursively dive through all directories until it gets `.py` files and doesn't care about folders!

*Note:* That's not quite true... it does care that `composers.py` is the only root-level module in data so don't add any pieces that aren't in a subfolder of data since the composers must be processed and upserted first.

### 3. Adding a new sonata

To add a new sonata, create a subclass of `SonataDataClass` in the same file as the piece that the sonata is housed in.

You can fill out as much of the `sonata_attribute_dict` as you'd like, but make sure to at least fill out `PIECE_ID`, `MOVEMENT_NUM`, `GLOBAL_KEY`, `INTRODUCTION_PRESENT`, `DEVELOPMENT_PRESENT`, `CODA_PRESENT`.

* `PIECE_ID` should just a be calling `id()` method in your piece's class that should be defined in this file.
* `MOVEMENT_NUM` is an integer representing what movement in the peice the sonata refers to, and it will be used to automatically create an id for the sonata in the format `<piece_id>_<movement_num>`, so it is required. 
	* If the sonata is the piece itself (the piece is a single movement work), use 0 
* `GLOBAL_KEY` is the enum `Key` instance imported from `key_enums.py` that houses the global key of the sonata. It is used to compute relative keys for all additional key fields, so it must be filled out.
* `INTRODUCTION_PRESENT`, `DEVELOPMENT_PRESENT`, `CODA_PRESENT` are booleans that need to be filled out to specify if the optional sonata blocks are present (the Exposition and Recapitulation obviously are always present or you don't have a sonata)

Then fill out the `exposition_attribute_dict` and `recapitulation_attribute_dict` with as many attributes as you want, and also fill out whichever of `introduction_attribute_dict`, `development_attribute_dict`, and `coda_attribute_dict` where you specified `True` for the `PRESENT` parameters above.

#### 4. Adding a new Lilypond file

As of now, each sonata can have at most a single lilypond (`.ly`) file linked to it, which should exist in the `data` directory with a filename that exactly matches the `sonata_id` that it corresponds to. (See above for a discussion on how this will always be `<piece_id>_<movement_num>`)

For example, for Beethoven Symphony No. 5 (`piece_id` =`beethoven5`), the first movement would have a `sonata_id` of `beethoven5_1`, so the corresponding lilypond file should be named `beethoven5_1.ly`.

TODO: More details about how to link the lilypond files to the sonata in the database so that the Flask app knows what images it should try to grab for the website.