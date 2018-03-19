#!/usr/bin/env python
import logging

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from psycopg2 import sql

from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda, ColumnDisplay
from general_utils.postgres_utils import LocalhostCursor

log = logging.getLogger(__name__)

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/composers')
def composers():
    with LocalhostCursor() as cur:
        select_comps_query = sql.SQL("""
                  SELECT {id},{full_name} 
                  FROM {composer_st};
        """).format(id=Composer.ID,
                    full_name=Composer.FULL_NAME,
                    composer_st=Composer.schema_table())

        cur.execute(select_comps_query)
        comp_tuples = cur.fetchall()

        # Create "Surname, Firstname" format by splitting on " "
        comp_tuples = [(comp_id, "{}, {}".format(comp_fn.split(' ')[-1], ' '.join(comp_fn.split(' ')[:-1])))
                       for comp_id, comp_fn in comp_tuples]

        # Sort by the name
        comp_tuples.sort(key=lambda x: x[1])

    return render_template('composers.html', composer_id_name_tuples=comp_tuples)


@app.route('/pieces')
def pieces():
    # The main goal for this method is to render pieces.html with the following:
    #
    # 1. pieces_comp_tuples: List[Tuple[str, str, str]]
    # a list of tuples of (comp_id, piece_id, piece_name_with_composer) for all pieces analyzed
    #
    # 2. pieces_movements_dict: Dict[str, List[int]]
    # a dict mapping piece id --> lists of the analyzed movement nums
    # Use a dict cursor to have fetchone return a dict instead of a tuple

    with LocalhostCursor() as cur:
        select_pieces_query = sql.SQL("""
                  SELECT comp.{comp_id}, piece.{piece_id}, 
                         comp.{comp_surname} || ' ' || piece.{piece_full_name} as cfn
                  FROM {piece_st} AS piece
                  JOIN {comp_st} AS comp
                  ON (piece.{piece_comp_id} = comp.{comp_id})
                  ORDER BY cfn ASC;
        """).format(piece_id=Piece.ID,
                    piece_full_name=Piece.FULL_NAME,
                    piece_comp_id=Piece.COMPOSER_ID,
                    piece_st=Piece.schema_table(),
                    comp_id=Composer.ID,
                    comp_surname=Composer.SURNAME,
                    comp_st=Composer.schema_table())

        cur.execute(select_pieces_query)
        pieces_comp_tuples = cur.fetchall()

        select_pieces_movements_query = sql.SQL("""
                    SELECT {sonata_piece_id}, {sonata_movement_num}
                    FROM {sonata_st}
                    ORDER BY {sonata_movement_num};
        """).format(sonata_piece_id=Sonata.PIECE_ID,
                    sonata_movement_num=Sonata.MOVEMENT_NUM,
                    sonata_st=Sonata.schema_table())

        cur.execute(select_pieces_movements_query)

        pieces_movements_dict = {}
        for piece_id, movement_num in cur:
            movement_list = pieces_movements_dict.setdefault(piece_id, [])
            movement_list.append(movement_num)

    return render_template('pieces.html', pieces_comp_tuples=pieces_comp_tuples,
                           pieces_movements_dict=pieces_movements_dict)


@app.route('/composers/<composer_id>')
def composer(composer_id: str):
    # The main goal for this method is to render composer.html with the following:
    #
    # 1. composer_id: str
    # the provided composer_id based on the url
    #
    # 2. composer_surname: str
    # the last name of the composer
    #
    # 3. comp_info_dict: Dict[str, Any]]
    # a dict that contains all composer-level attributes and values
    #
    # 4. piece_id_name_tuples: List[Tuple[str, str]]
    # a list of tuples of (piece_id, piece_name) for all pieces for this composer
    #
    # 5. pieces_movements_dict: Dict[str, List[int]]
    # a dict mapping piece id --> lists of the analyzed movement nums

    # Use a dict cursor to have fetchone return a dict instead of a tuple
    with LocalhostCursor(dict_cursor=True) as cur:
        select_comp_info_query = sql.SQL("""
                  SELECT *
                  FROM {composer_st}
                  WHERE {id} = {composer_id};
        """).format(id=Composer.ID,
                    composer_id=sql.Literal(composer_id),
                    composer_st=Composer.schema_table())
        cur.execute(select_comp_info_query)

        comp_info_dict = dict(cur.fetchone())

        # Remove information that we don't want to display
        comp_info_dict.pop(Composer.ID.string)

        # Will use surname as separate field so need to keep it
        composer_surname = comp_info_dict.pop(Composer.SURNAME.string)

    with LocalhostCursor() as cur:
        select_comp_pieces_query = sql.SQL("""
                  SELECT {id}, {full_name}
                  FROM {piece_st}
                  WHERE {comp_id} = {composer_id};
        """).format(id=Piece.ID,
                    full_name=Piece.FULL_NAME,
                    comp_id=Piece.COMPOSER_ID,
                    composer_id=sql.Literal(composer_id),
                    piece_st=Piece.schema_table())

        cur.execute(select_comp_pieces_query)
        piece_id_name_tuples = cur.fetchall()

        # Sort by the name
        piece_id_name_tuples.sort(key=lambda x: x[1])

        # Change info dict to have display name keys instead of raw field name keys
        comp_info_dict = ColumnDisplay.create_new_dict_with_display_name_keys(
            cursor=cur,
            table_name=Composer.schema_table().table.string,
            dict_with_column_name_keys=comp_info_dict)

        select_pieces_movements_query = sql.SQL("""
                            SELECT s.{sonata_piece_id}, s.{sonata_movement_num}
                            FROM {sonata_st} AS s
                            JOIN {piece_st} AS p
                            ON s.{sonata_piece_id} = p.{piece_id} 
                            WHERE p.{piece_comp_id} = {composer_id}
                            ORDER BY s.{sonata_movement_num};
                """).format(sonata_piece_id=Sonata.PIECE_ID,
                            sonata_movement_num=Sonata.MOVEMENT_NUM,
                            sonata_comp_id=Sonata.PIECE_ID,
                            piece_id=Piece.ID,
                            piece_comp_id=Piece.COMPOSER_ID,
                            composer_id=sql.Literal(composer_id),
                            piece_st=Piece.schema_table(),
                            sonata_st=Sonata.schema_table())

        cur.execute(select_pieces_movements_query)

        pieces_movements_dict = {}
        for piece_id, movement_num in cur:
            movement_list = pieces_movements_dict.setdefault(piece_id, [])
            movement_list.append(movement_num)

    return render_template('composer.html',
                           composer_id=composer_id,
                           composer_surname=composer_surname,
                           composer_info_dict=comp_info_dict,
                           piece_id_name_tuples=piece_id_name_tuples,
                           pieces_movements_dict=pieces_movements_dict)


@app.route('/composers/<composer_id>/<piece_id>')
def piece(composer_id: str, piece_id: str):
    # The main goal for this method is to render piece.html with the following:
    #
    # 1. composer_id: str
    # the provided composer_id based on the url
    #
    # 2. composer_surname: str
    # the last name of the composer
    #
    # 3. piece_name: str
    # the name of the piece
    #
    # 4. piece_info_dict: Dict[str, Any]
    # a dict of piece-level attribtues and values
    #
    # 5. sonatas_info_dict: Dict[str, Dict[str, Any]]
    # a dict that maps movement_num to dicts of sonata-level attributes and values
    #
    # 6. sonatas_lilypond_image_settings_dict: Dict[str, Dict[str, Any]]
    # a dict that maps movement_num to an image settings dict containing settings for the lilypond file
    # Right now, the only setting it should have is "image_width"
    #
    # 7. sonatas_blocks_info_dict: Dict[str, Dict[str, Dict[str, Any]]]
    # nested dicts that map movement_num --> block name --> block-level dict of attributes and values
    #
    # If sonata name = 'Itself' then this means the piece is a single-movement work that is the sonata

    # Use a dict cursor to have each record return a dict instead of a tuple
    with LocalhostCursor(dict_cursor=True) as cur:

        ###################################
        #  Piece Info Dict and Piece Name #
        ###################################

        select_piece_info_query = sql.SQL("""
            SELECT *
            FROM {piece_st}
            WHERE {id} = {piece_id};
        """).format(id=Piece.ID,
                    piece_id=sql.Literal(piece_id),
                    piece_st=Piece.schema_table())

        cur.execute(select_piece_info_query)
        piece_info_dict = dict(cur.fetchone())

        # Remove information that we don't want to display (grab the full name and composer_id while popping)
        piece_info_dict.pop(Piece.ID.string)
        piece_info_dict.pop(Piece.NAME.string)
        piece_info_dict.pop(Piece.NICKNAME.string)
        piece_info_dict.pop(Piece.CATALOGUE_ID.string)

        piece_name = piece_info_dict.pop(Piece.FULL_NAME.string)
        composer_id_of_piece = piece_info_dict.pop(Piece.COMPOSER_ID.string)

        # Change info dict to have display name keys instead of raw field name keys
        piece_info_dict = ColumnDisplay.create_new_dict_with_display_name_keys(
            cursor=cur,
            table_name=Piece.schema_table().table.string,
            dict_with_column_name_keys=piece_info_dict)

        if composer_id != composer_id_of_piece:
            raise Exception("Bad composer id \"{}\" in URL! Piece with id \"{}\" should have composer id \"{}\""
                            "".format(composer_id, piece_id, composer_id_of_piece))

        ####################
        # Composer Surname #
        ####################
        select_comp_surname_query = sql.SQL("""
                        SELECT {surname}
                        FROM {composer_st}
                        WHERE {id} = {composer_id}
        """).format(surname=Composer.SURNAME,
                    id=Composer.ID,
                    composer_id=sql.Literal(composer_id),
                    composer_st=Composer.schema_table())
        cur.execute(select_comp_surname_query)
        composer_surname = cur.fetchone()[0]

        ######################
        # Sonatas Info Dicts #
        ######################
        select_sonatas_query = sql.SQL("""
                         SELECT *
                         FROM {sonata_st}
                         WHERE {p_id} = {piece_id}
                         ORDER BY {movement_num};
            """).format(p_id=Sonata.PIECE_ID,
                        piece_id=sql.Literal(piece_id),
                        movement_num=Sonata.MOVEMENT_NUM,
                        sonata_st=Sonata.schema_table())
        cur.execute(select_sonatas_query)

        sonatas_info_dict = {}
        sonatas_blocks_info_dict = {}
        sonatas_lilypond_image_settings_dict = {}

        sonatas_data = cur.fetchall()

        for result in sonatas_data:
            sonata_info_dict = dict(result)
            # Remove information that we don't want to display (grab various ids and info we need while popping)
            sonata_info_dict.pop(Sonata.PIECE_ID.string)

            sonata_id = sonata_info_dict.pop(Sonata.ID.string)
            movement_num = sonata_info_dict.pop(Sonata.MOVEMENT_NUM.string)
            intro_id = sonata_info_dict.pop(Sonata.INTRODUCTION_ID.string)
            expo_id = sonata_info_dict.pop(Sonata.EXPOSITION_ID.string)
            dev_id = sonata_info_dict.pop(Sonata.DEVELOPMENT_ID.string)
            recap_id = sonata_info_dict.pop(Sonata.RECAPITULATION_ID.string)
            coda_id = sonata_info_dict.pop(Sonata.CODA_ID.string)
            lilypond_image_settings = sonata_info_dict.pop(Sonata.LILYPOND_IMAGE_SETTINGS.string)

            # Change info dict to have display name keys instead of raw field name keys
            sonata_info_dict = ColumnDisplay.create_new_dict_with_display_name_keys(
                cursor=cur,
                table_name=Sonata.schema_table().table.string,
                dict_with_column_name_keys=sonata_info_dict)

            sonatas_info_dict[movement_num] = sonata_info_dict

            # If settings to the lilypond image were provided for this sonata, we should expect the image to exist
            if lilypond_image_settings is not None:

                # The assumed image path will be in the static folder named after the sonata id
                lilypond_image_settings[Sonata.IMAGE_PATH] = '/static/lilypond/{}.png'.format(sonata_id)

                # Provide a default image width if not provided
                if Sonata.IMAGE_WIDTH not in lilypond_image_settings:
                    lilypond_image_settings[Sonata.IMAGE_WIDTH] = 400

                sonatas_lilypond_image_settings_dict[movement_num] = lilypond_image_settings

            sonatas_blocks_info_dict[movement_num] = {}

            block_ids = [intro_id, expo_id, dev_id, recap_id, coda_id]
            block_table_specs = [Introduction, Exposition, Development, Recapitulation, Coda]

            #############################
            # Sonatas Blocks Info Dicts #
            #############################
            for block_id, block_table_spec in zip(block_ids, block_table_specs):

                # if there is no block id, that means the block is missing, so we can skip
                if block_id is not None:
                    # The name of the block is the same as the table spec class name
                    block_name = block_table_spec.__name__

                    with LocalhostCursor(dict_cursor=True) as cur2:
                        select_sonata_block_info_query = sql.SQL("""
                                                 SELECT *
                                                 FROM {block_st}
                                                 WHERE {id} = {block_id};
                                    """).format(id=block_table_spec.ID,
                                                block_id=sql.Literal(block_id),
                                                block_st=block_table_spec.schema_table())
                        cur2.execute(select_sonata_block_info_query)
                        sonata_block_info_dict = dict(cur2.fetchone())

                        # Remove information that we don't want to display
                        sonata_block_info_dict.pop(block_table_spec.ID.string)

                        # Change info dict to have display name keys instead of raw field name keys
                        sonata_block_info_dict = ColumnDisplay.create_new_dict_with_display_name_keys(
                            cursor=cur,
                            table_name=block_table_spec.schema_table().table.string,
                            dict_with_column_name_keys=sonata_block_info_dict)

                        sonatas_blocks_info_dict[movement_num][block_name] = sonata_block_info_dict

        log.debug('sonatas_lilypond_image_settings_dict: {}'.format(sonatas_lilypond_image_settings_dict))

    return render_template('piece.html',
                           composer_id=composer_id,
                           composer_surname=composer_surname,
                           piece_name=piece_name,
                           piece_info_dict=piece_info_dict,
                           sonatas_info_dict=sonatas_info_dict,
                           sonatas_blocks_info_dict=sonatas_blocks_info_dict,
                           sonatas_lilypond_image_settings_dict=sonatas_lilypond_image_settings_dict,
                           IMAGE_PATH=Sonata.IMAGE_PATH,
                           IMAGE_WIDTH=Sonata.IMAGE_WIDTH)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s')
    app.run(debug=True)
