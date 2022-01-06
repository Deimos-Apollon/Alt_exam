from source.config import SQL_USER, SQL_PASS
from mysql.connector import connect, Error, ProgrammingError


class SqlReader:
    def __init__(self, connection):
        self.connection = connection

    def check_if_DOI_exists(self, doi):
        check_query = fr'''
               SELECT DOI FROM work WHERE DOI = '{doi}'
               '''
        with self.connection.cursor() as cursor:
            cursor.execute(check_query)
            do_exists = cursor.fetchall()
        return do_exists

    def get_author_id(self, given, family):
        get_query = fr'''
                        SELECT ID FROM author where given_name = ("{given}") and family_name = ("{family}")
                    '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            id = cursor.fetchall()
        return id[0][0] if id else None

    def count_author_works(self, ID):
        get_query = fr'''
               SELECT COUNT(*) FROM author_has_work WHERE author_id=({ID})
           '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            ans = cursor.fetchall()
        return ans[0][0]

    def get_authors_of_work(self, doi):
        get_query = fr'''
                          SELECT author_ID FROM author_has_work WHERE work_DOI = '{doi}'
                          '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            authors = cursor.fetchall()
        return authors

    def get_references_dois_of_work(self, work_doi):
        get_query = fr'''
                          SELECT Src_DOI FROM work_cites_work WHERE Work_DOI = "{work_doi}"
                    '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            refs_doi = cursor.fetchall()
        return refs_doi

    def get_work_is_referenced_count(self, work_doi):
        get_query = fr'''
                          SELECT Is_referenced_count FROM work WHERE DOI = "{work_doi}"
                    '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            number_of_refs = cursor.fetchall()
        return number_of_refs[0][0]

    def get_author_works(self, author_id):
        get_query = fr'''
                      SELECT Work_DOI FROM author_has_work WHERE Author_ID = {author_id}
                      '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            works = cursor.fetchall()
        return works

    def get_all_authors(self):
        get_query = fr'''
                          SELECT ID FROM author
                       '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            authors = cursor.fetchall()
        return tuple(elem[0] for elem in authors)

    def get_all_citations(self):
        get_query = fr'''
                            SELECT * FROM author_cites_author
                   '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            authors_cites_authors = cursor.fetchall()
        return authors_cites_authors

    def get_number_citations(self):
        get_query = fr'''
                            SELECT ID FROM author_cites_author ORDER BY ID DESC Limit 1
                   '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            num_entries = cursor.fetchall()
        return num_entries[0][0]


    def get_citation_id_from_graph(self, entry_ID):
        get_query = fr'''
                            SELECT author_Citates_author_ID from graph where ID = {entry_ID}
                   '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry[0][0] if entry else None

    def get_authors_from_citations_via_id(self, entry_ID):
        get_query = fr'''
                        SELECT author_ID, Src_ID FROM author_cites_author WHERE ID = {entry_ID}
                   '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry[0] if entry else None

    def get_citation_from_citations_via_authors(self, author_ID, Src_ID):
        get_query = fr'''
                           SELECT ID FROM author_cites_author WHERE author_ID = {author_ID} and Src_ID = {Src_ID}
                      '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry[0][0] if entry else None

    def get_all_citation_from_citations_via_author_id(self, author_ID):
        get_query = fr'''
                          SELECT ID FROM author_cites_author WHERE author_ID = {author_ID}
                     '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry if entry else None

    def get_all_citation_from_citations_via_src_id(self, Src_ID):
        get_query = fr'''
                          SELECT ID FROM author_cites_author WHERE Src_ID = {Src_ID}
                     '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry if entry else None

    def get_authors_with_short_names(self):
        get_query = fr'''
                            SELECT ID FROM author WHERE CHAR_LENGTH(given_name) < 5
                      '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry if entry else None

    def get_src_authors(self, author_id):
        get_query = fr'''
                            SELECT src_id FROM author_cites_author WHERE author_ID = {author_id}
                      '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry if entry else None

    def get_author_name(self, author_id):
        get_query = fr'''
                        SELECT given_name, family_name FROM author WHERE ID = {author_id}
                    '''
        with self.connection.cursor() as cursor:
            cursor.execute(get_query)
            entry = cursor.fetchall()
        return entry[0] if entry else None

    def execute_get_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            entry = cursor.fetchall()
        return entry if entry else None
