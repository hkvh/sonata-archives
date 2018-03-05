#!/usr/bin/env python

from flask import Flask, render_template
from psycopg2 import sql

from database_design.sonata_data_classes import PieceDataClass
from database_design.sonata_table_specs import Composer, Piece
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


@app.route('/composer/<composer_id>')
def composer(composer_id: str):
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
        surname = comp_info_dict.pop(Composer.SURNAME.string)

    with LocalhostCursor() as cur:
        select_comp_pieces_query = sql.SQL("""
                  SELECT {id}, {name}, {cat_id}, {nickname}
                  FROM {piece_st}
                  WHERE {comp_id} = {composer_id};
        """).format(id=Piece.ID,
                    name=Piece.NAME,
                    cat_id=Piece.CATALOGUE_ID,
                    nickname=Piece.NICKNAME,
                    comp_id=Piece.COMPOSER_ID,
                    composer_id=sql.Literal(composer_id),
                    piece_st=Piece.schema_table())

        cur.execute(select_comp_pieces_query)
        piece_data = cur.fetchall()

        piece_tuples = [(x[0], PieceDataClass.create_piece_full_name(name=x[1], catalogue_id=x[2], nickname=x[3]))
                        for x in piece_data]

    return render_template('composer.html',
                           composer_surname=surname,
                           composer_info_dict=comp_info_dict,
                           piece_id_name_tuples=piece_tuples)


if __name__ == '__main__':
    app.run(debug=True)
