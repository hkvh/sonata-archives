#!/usr/bin/env python
"""
The core module for all composer classes.

Keep this as the only data file in the root directory to ensure it is upserted first since it is a precondition
for all the other files since they link to the composers with FKs
"""
import logging
from typing import Dict, Any

from datetime import date

from database_design.sonata_data_classes import ComposerDataClass
from database_design.sonata_table_specs import Composer
from general_utils.sql_utils import Field


class Beethoven(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:          "beethoven",
            Composer.SURNAME:     "Beethoven",
            Composer.FULL_NAME:   "Ludwig van Beethoven",
            Composer.BIRTH_DATE:  date(1770, 12, 17),
            Composer.DEATH_DATE:  date(1827, 3, 26),
            Composer.NATIONALITY: "German",
        }


class Mahler(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:          "mahler",
            Composer.SURNAME:     "Mahler",
            Composer.FULL_NAME:   "Gustav Mahler",
            Composer.BIRTH_DATE:  date(1860, 7, 7),
            Composer.DEATH_DATE:  date(1911, 5, 18),
            Composer.NATIONALITY: "Austrian",
        }


class Tchaikovsky(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:          "tchaikovsky",
            Composer.SURNAME:     "Tchaikovsky",
            Composer.FULL_NAME:   "Pyotr Ilyich Tchaikovsky",
            Composer.BIRTH_DATE:  date(1840, 5, 7),
            Composer.DEATH_DATE:  date(1893, 11, 6),
            Composer.NATIONALITY: "Russian",
        }


# Make sure to update this list with all composers
composer_list = [
    Beethoven,
    Mahler,
    Tchaikovsky,
]


# Core upsert method that all data modules must have
def upsert_all():
    for x in composer_list:
        x.upsert_data()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')
    upsert_all()
