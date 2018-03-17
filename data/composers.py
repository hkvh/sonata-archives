#!/usr/bin/env python
"""
The core module for all composer classes.

Keep this as the only data file in the root directory to ensure it is upserted first since it is a precondition
for all the other files since they link to the composers with FKs
"""
from datetime import date
from typing import Dict, Any

from database_design.sonata_data_classes import ComposerDataClass
from database_design.sonata_table_specs import Composer
from general_utils.sql_utils import Field


#################
# Composers
#################

class Beethoven(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "beethoven",
            Composer.SURNAME:           "Beethoven",
            Composer.FULL_NAME:         "Ludwig van Beethoven",
            Composer.BIRTH_DATE:        date(1770, 12, 17),
            Composer.DEATH_DATE:        date(1827, 3, 26),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Bonn, Germany",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Mahler(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "mahler",
            Composer.SURNAME:           "Mahler",
            Composer.FULL_NAME:         "Gustav Mahler",
            Composer.BIRTH_DATE:        date(1860, 7, 7),
            Composer.DEATH_DATE:        date(1911, 5, 18),
            Composer.NATIONALITY:       "Austrian",
            Composer.BIRTHPLACE:        "Kaliště, Czech Republic",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Tchaikovsky(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "tchaikovsky",
            Composer.SURNAME:           "Tchaikovsky",
            Composer.FULL_NAME:         "Pyotr Ilyich Tchaikovsky",
            Composer.BIRTH_DATE:        date(1840, 5, 7),
            Composer.DEATH_DATE:        date(1893, 11, 6),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "Votkinsk, Russia",
            Composer.PRIMARY_RESIDENCE: "Moscow, Russia",
        }


class Rachmaninoff(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "rachmaninoff",
            Composer.SURNAME:           "Rachmaninoff",
            Composer.FULL_NAME:         "Sergei Vasilievich Rachmaninoff",
            Composer.BIRTH_DATE:        date(1873, 4, 1),
            Composer.DEATH_DATE:        date(1943, 3, 28),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "Semyonovo, Russia",
            Composer.PRIMARY_RESIDENCE: "Moscow, Russia",
        }


class Mozart(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "mozart",
            Composer.SURNAME:           "Mozart",
            Composer.FULL_NAME:         "Wolfgang Amadeus Mozart",
            Composer.BIRTH_DATE:        date(1756, 1, 27),
            Composer.DEATH_DATE:        date(1791, 12, 5),
            Composer.NATIONALITY:       "Austrian",
            Composer.BIRTHPLACE:        "Salzburg, Austria",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Haydn(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "haydn",
            Composer.SURNAME:           "Haydn",
            Composer.FULL_NAME:         "Franz Joseph Haydn",
            Composer.BIRTH_DATE:        date(1732, 3, 31),
            Composer.DEATH_DATE:        date(1809, 5, 31),
            Composer.NATIONALITY:       "Austrian",
            Composer.BIRTHPLACE:        "Rohrau, Austria",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Franck(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "franck",
            Composer.SURNAME:           "Franck",
            Composer.FULL_NAME:         "César-Auguste-Jean-Guillaume-Hubert Franck",
            Composer.BIRTH_DATE:        date(1822, 12, 10),
            Composer.DEATH_DATE:        date(1890, 11, 8),
            Composer.NATIONALITY:       "Belgian",
            Composer.BIRTHPLACE:        "Liège, Beligum",
            Composer.PRIMARY_RESIDENCE: "Paris, France",
        }


class Chopin(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "chopin",
            Composer.SURNAME:           "Chopin",
            Composer.FULL_NAME:         "Frédéric François Chopin",
            Composer.BIRTH_DATE:        date(1810, 3, 1),
            Composer.DEATH_DATE:        date(1849, 10, 17),
            Composer.NATIONALITY:       "Polish",
            Composer.BIRTHPLACE:        "Żelazowa Wola, Poland",
            Composer.PRIMARY_RESIDENCE: "Paris, France",
        }


class Grieg(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "grieg",
            Composer.SURNAME:           "Grieg",
            Composer.FULL_NAME:         "Edvard Hagerup Grieg",
            Composer.BIRTH_DATE:        date(1843, 6, 15),
            Composer.DEATH_DATE:        date(1907, 9, 4),
            Composer.NATIONALITY:       "Norwegian",
            Composer.BIRTHPLACE:        "Bergen, Norway",
            Composer.PRIMARY_RESIDENCE: "Bergen, Norway",
        }


class Liszt(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "liszt",
            Composer.SURNAME:           "Liszt",
            Composer.FULL_NAME:         "Franz Liszt",
            Composer.BIRTH_DATE:        date(1811, 10, 22),
            Composer.DEATH_DATE:        date(1886, 7, 31),
            Composer.NATIONALITY:       "Hungarian",
            Composer.BIRTHPLACE:        "Raiding, Austria",
            Composer.PRIMARY_RESIDENCE: "Budapest, Hungary",
        }


class Sibelius(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "sibelius",
            Composer.SURNAME:           "Sibelius",
            Composer.FULL_NAME:         "Jean Sibelius",
            Composer.BIRTH_DATE:        date(1865, 12, 8),
            Composer.DEATH_DATE:        date(1957, 9, 20),
            Composer.NATIONALITY:       "Finnish",
            Composer.BIRTHPLACE:        "Hämeenlinna, Finland",
            Composer.PRIMARY_RESIDENCE: "Helsinki, Finland",
        }


class Dvorak(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "dvorak",
            Composer.SURNAME:           "Dvořák",
            Composer.FULL_NAME:         "Antonin Leopold Dvořák",
            Composer.BIRTH_DATE:        date(1841, 9, 8),
            Composer.DEATH_DATE:        date(1904, 5, 1),
            Composer.NATIONALITY:       "Czech",
            Composer.BIRTHPLACE:        "Nelahozeves, Czech Republic",
            Composer.PRIMARY_RESIDENCE: "Prague, Czech Republic",
        }


class Strauss(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "rstrauss",
            Composer.SURNAME:           "Strauss",
            Composer.FULL_NAME:         "Richard Georg Strauss",
            Composer.BIRTH_DATE:        date(1864, 6, 11),
            Composer.DEATH_DATE:        date(1949, 9, 8),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Munich, Germany",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Brahms(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "brahms",
            Composer.SURNAME:           "Brahms",
            Composer.FULL_NAME:         "Johannes Brahms",
            Composer.BIRTH_DATE:        date(1833, 5, 7),
            Composer.DEATH_DATE:        date(1897, 4, 3),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Hamburg, Germany",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Schumann(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "schumann",
            Composer.SURNAME:           "Schumann",
            Composer.FULL_NAME:         "Robert Schumann",
            Composer.BIRTH_DATE:        date(1810, 6, 8),
            Composer.DEATH_DATE:        date(1856, 7, 29),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Zwickau, Germany",
            Composer.PRIMARY_RESIDENCE: "Düsseldorf, Germany",
        }


class Schubert(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "schubert",
            Composer.SURNAME:           "Schubert",
            Composer.FULL_NAME:         "Franz Peter Schubert",
            Composer.BIRTH_DATE:        date(1797, 1, 31),
            Composer.DEATH_DATE:        date(1828, 11, 19),
            Composer.NATIONALITY:       "Austrian",
            Composer.BIRTHPLACE:        "Vienna, Austria",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Wagner(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "wagner",
            Composer.SURNAME:           "Wagner",
            Composer.FULL_NAME:         "Wilhelm Richard Wagner",
            Composer.BIRTH_DATE:        date(1813, 5, 22),
            Composer.DEATH_DATE:        date(1883, 2, 13),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Leipzig, Germany",
            Composer.PRIMARY_RESIDENCE: "Bayreuth, Germany",
        }


class Mendelssohn(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "mendelssohn",
            Composer.SURNAME:           "Mendelssohn",
            Composer.FULL_NAME:         "Jakob Ludwig Felix Mendelssohn-Bartholdy",
            Composer.BIRTH_DATE:        date(1809, 2, 3),
            Composer.DEATH_DATE:        date(1847, 11, 4),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Hamburg, Germany",
            Composer.PRIMARY_RESIDENCE: "Leipzig, Germany",
        }


class Weber(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "weber",
            Composer.SURNAME:           "Weber",
            Composer.FULL_NAME:         "Carl Maria Freidrich Ernst von Weber",
            Composer.BIRTH_DATE:        date(1786, 11, 19),
            Composer.DEATH_DATE:        date(1826, 6, 5),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Eutin, Germany",
            Composer.PRIMARY_RESIDENCE: "Dresden, Germany",
        }


class Bruch(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "bruch",
            Composer.SURNAME:           "Bruch",
            Composer.FULL_NAME:         "Max Christian Friedrich Bruch",
            Composer.BIRTH_DATE:        date(1838, 1, 6),
            Composer.DEATH_DATE:        date(1920, 10, 2),
            Composer.NATIONALITY:       "German",
            Composer.BIRTHPLACE:        "Cologne, Germany",
            Composer.PRIMARY_RESIDENCE: "Bonn, Germany",
        }


class Prokofiev(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "prokofiev",
            Composer.SURNAME:           "Prokofiev",
            Composer.FULL_NAME:         "Sergei Sergeyevich Prokofiev",
            Composer.BIRTH_DATE:        date(1891, 4, 27),
            Composer.DEATH_DATE:        date(1953, 3, 5),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "Pokrovsk Raion, Ukraine",
            Composer.PRIMARY_RESIDENCE: "Moscow, Russia",
        }


class Shostakovich(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "shostakovich",
            Composer.SURNAME:           "Shostakovich",
            Composer.FULL_NAME:         "Dmitri Dmitriyevich Shostakovich",
            Composer.BIRTH_DATE:        date(1906, 9, 25),
            Composer.DEATH_DATE:        date(1975, 8, 9),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "St. Petersburg, Russia",
            Composer.PRIMARY_RESIDENCE: "St. Petersburg, Russia",
        }


class Scriabin(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "scriabin",
            Composer.SURNAME:           "Scriabin",
            Composer.FULL_NAME:         "Alexander Nikolayevich Scriabin",
            Composer.BIRTH_DATE:        date(1872, 1, 6),
            Composer.DEATH_DATE:        date(1915, 4, 27),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "Moscow, Russia",
            Composer.PRIMARY_RESIDENCE: "Moscow, Russia",
        }


class Gershwin(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "gershwin",
            Composer.SURNAME:           "Gershwin",
            Composer.FULL_NAME:         "George Jacob Gershwin",
            Composer.BIRTH_DATE:        date(1898, 9, 26),
            Composer.DEATH_DATE:        date(1937, 7, 11),
            Composer.NATIONALITY:       "American",
            Composer.BIRTHPLACE:        "New York City, NY, USA",
            Composer.PRIMARY_RESIDENCE: "New York City, NY, USA",
        }


class Copland(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "copland",
            Composer.SURNAME:           "Copland",
            Composer.FULL_NAME:         "Aaron Copland",
            Composer.BIRTH_DATE:        date(1900, 11, 14),
            Composer.DEATH_DATE:        date(1990, 12, 2),
            Composer.NATIONALITY:       "American",
            Composer.BIRTHPLACE:        "New York City, NY, USA",
            Composer.PRIMARY_RESIDENCE: "New York City, NY, USA",
        }


class Faure(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "faure",
            Composer.SURNAME:           "Fauré",
            Composer.FULL_NAME:         "Gabriel Urbain Fauré",
            Composer.BIRTH_DATE:        date(1845, 5, 12),
            Composer.DEATH_DATE:        date(1924, 11, 4),
            Composer.NATIONALITY:       "French",
            Composer.BIRTHPLACE:        "Pamiers, France",
            Composer.PRIMARY_RESIDENCE: "Paris, France",
        }


class Bruckner(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "bruckner",
            Composer.SURNAME:           "Bruckner",
            Composer.FULL_NAME:         "Josef Anton Bruckner",
            Composer.BIRTH_DATE:        date(1824, 9, 4),
            Composer.DEATH_DATE:        date(1896, 10, 11),
            Composer.NATIONALITY:       "Austrian",
            Composer.BIRTHPLACE:        "Ansfelden, Austria",
            Composer.PRIMARY_RESIDENCE: "Vienna, Austria",
        }


class Stravinsky(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "stravinsky",
            Composer.SURNAME:           "Stravinsky",
            Composer.FULL_NAME:         "Igor Fyodorovich Stravinsky",
            Composer.BIRTH_DATE:        date(1882, 6, 17),
            Composer.DEATH_DATE:        date(1971, 4, 6),
            Composer.NATIONALITY:       "Russian",
            Composer.BIRTHPLACE:        "St. Petersburg, Russia",
            Composer.PRIMARY_RESIDENCE: "Los Angeles, CA, USA",
        }


class Ravel(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "ravel",
            Composer.SURNAME:           "Ravel",
            Composer.FULL_NAME:         "Maurice Ravel",
            Composer.BIRTH_DATE:        date(1875, 3, 7),
            Composer.DEATH_DATE:        date(1937, 12, 28),
            Composer.NATIONALITY:       "French",
            Composer.BIRTHPLACE:        "Ciboure, France",
            Composer.PRIMARY_RESIDENCE: "Paris, France",
        }


class Berlioz(ComposerDataClass):
    @classmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Composer.ID:                "berlioz",
            Composer.SURNAME:           "Berlioz",
            Composer.FULL_NAME:         "Louis-Hector Berlioz",
            Composer.BIRTH_DATE:        date(1803, 12, 11),
            Composer.DEATH_DATE:        date(1869, 3, 8),
            Composer.NATIONALITY:       "French",
            Composer.BIRTHPLACE:        "La Côte-Saint-André, France",
            Composer.PRIMARY_RESIDENCE: "Paris, France",
        }