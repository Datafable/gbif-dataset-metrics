import json


class DatasetDescriptor(object):
    def __init__(self):
        self.data = {'NUMBER_OF_RECORDS': 0,
                     'ARCHIVE_GENERATED_AT': None,
                     'BASISOFRECORDS': {},
                     'TAXON_MATCHES': {},
                     'TAXONOMY': {},
                     'COORDINATE_QUALITY_CATEGORIES': {},

                     'MEDIA': {'media_url_invalid': 0,
                               'media_not_provided': 0,
                               'media_valid': 0,
                               'movingimage': {},
                               'audio': {},
                               'stillimage': {},
                               'no_type': {},
                               }
                     }

    def increment_number_records(self):
        self.data['NUMBER_OF_RECORDS'] = self.data['NUMBER_OF_RECORDS'] + 1

    # Expect a simple string
    def set_archive_generated_at(self, date):
        self.data['ARCHIVE_GENERATED_AT'] = date

    def _store_or_increment_counter(self, value, dict_name):
        if value in self.data[dict_name]:
            self.data[dict_name][value] = self.data[dict_name][value] + 1
        else:
            self.data[dict_name][value] = 1

    def store_or_increment_bor(self, value):
        self._store_or_increment_counter(value, 'BASISOFRECORDS')

    def store_or_increment_taxonomy(self, value):
        self._store_or_increment_counter(value, 'TAXONOMY')

    def store_or_increment_taxonmatch(self, value):
        self._store_or_increment_counter(value, 'TAXON_MATCHES')

    def store_or_increment_coordinatecategory(self, value):
        self._store_or_increment_counter(value, 'COORDINATE_QUALITY_CATEGORIES')

    def mul_increment_invalid_url_count(self):
        self.data['MEDIA']['media_url_invalid'] = self.data['MEDIA']['media_url_invalid'] + 1

    def mul_increment_not_provided_count(self):
        self.data['MEDIA']['media_not_provided'] = self.data['MEDIA']['media_not_provided'] + 1

    def mul_increment_valid_count(self):
        self.data['MEDIA']['media_valid'] = self.data['MEDIA']['media_valid'] + 1

    def _mul_add_occurrence(self, container, occurrence_id, reference):
        if occurrence_id not in container:
            container[occurrence_id] = [reference]
        else:
            container[occurrence_id].append(reference)

    def mul_add_image(self, occurrence_id, reference):
        self._mul_add_occurrence(self.data['MEDIA']['stillimage'], occurrence_id, reference)

    def mul_add_video(self, occurrence_id, reference):
        self._mul_add_occurrence(self.data['MEDIA']['movingimage'], occurrence_id, reference)

    def mul_add_audio(self, occurrence_id, reference):
        self._mul_add_occurrence(self.data['MEDIA']['audio'], occurrence_id, reference)

    def mul_add_notype(self, occurrence_id, reference):
        self._mul_add_occurrence(self.data['MEDIA']['no_type'], occurrence_id, reference)


class DatasetDescriptorAwareEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DatasetDescriptor):
            return obj.data

        return json.JSONEncoder.default(self, obj)
