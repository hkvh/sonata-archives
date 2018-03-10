#!/usr/bin/env python

from flask import Flask, render_template
from psycopg2 import sql

from database_design.sonata_data_classes import PieceDataClass
from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda
from general_utils.postgres_utils import LocalhostCursor
from flask_bootstrap import Bootstrap

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

    return render_template('composers.html', composer_id_name_tuples=comp_tuples)


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
    # 4. piece_tuples: List[Tuple[str, str]]
    # a list of tuples of (piece_id, piece_name) for all pieces for this composer

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

        # TODO Have display names for all fields
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
        piece_tuples = cur.fetchall()

    return render_template('composer.html',
                           composer_id=composer_id,
                           composer_surname=composer_surname,
                           composer_info_dict=comp_info_dict,
                           piece_id_name_tuples=piece_tuples)


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
    # a dict that maps sonata names to dicts of sonata-level attributes and values
    #
    # 6. sonatas_blocks_info_dict: Dict[str, Dict[str, Dict[str, Any]]]
    # nested dicts that map sonata_name --> block name --> block-level dict of attributes and values
    #
    # If sonata name = 'Itself' then this means the piece is a single-movement work that is the sonata

    # Use a dict cursor to have each record return a dict instead of a tuple
    with LocalhostCursor(dict_cursor=True) as cur:

        # #### Piece Info Dict and Piece Name ####
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

        if composer_id != composer_id_of_piece:
            raise Exception("Bad composer id \"{}\" in URL! Piece with id \"{}\" should have composer id \"{}\""
                            "".format(composer_id, piece_id, composer_id_of_piece))

        # #### Composer Surname ####
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

        # ### Sonatas Info Dict
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

        for result in cur:
            sonata_info_dict = dict(result)

            # Remove information that we don't want to display (grab various ids and info we need while popping)
            sonata_info_dict.pop(Sonata.PIECE_ID.string)
            sonata_info_dict.pop(Sonata.ID.string)

            movement_num = sonata_info_dict.pop(Sonata.MOVEMENT_NUM.string)
            intro_id = sonata_info_dict.pop(Sonata.INTRODUCTION_ID.string)
            expo_id = sonata_info_dict.pop(Sonata.EXPOSITION_ID.string)
            dev_id = sonata_info_dict.pop(Sonata.DEVELOPMENT_ID.string)
            recap_id = sonata_info_dict.pop(Sonata.RECAPITULATION_ID.string)
            coda_id = sonata_info_dict.pop(Sonata.CODA_ID.string)

            # Movement Number 0 means the piece is itself a sonata
            if movement_num == 0:
                sonata_name = 'Itself'
            else:
                sonata_name = 'Movement {}'.format(movement_num)

            sonatas_info_dict[sonata_name] = sonata_info_dict
            sonatas_blocks_info_dict[sonata_name] = {}

            block_ids = [intro_id, expo_id, dev_id, recap_id, coda_id]
            block_table_specs = [Introduction, Exposition, Development, Recapitulation, Coda]

            # #### Sonatas Blocks Info Dict ####
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

                        sonatas_blocks_info_dict[sonata_name][block_name] = sonata_block_info_dict

        return render_template('piece.html',
                               composer_id=composer_id,
                               composer_surname=composer_surname,
                               piece_name=piece_name,
                               piece_info_dict=piece_info_dict,
                               sonatas_info_dict=sonatas_info_dict,
                               sonatas_blocks_info_dict=sonatas_blocks_info_dict)


if __name__ == '__main__':
    app.run(debug=True)
