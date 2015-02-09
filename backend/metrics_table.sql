ALTER TABLE gbif_dataset_metrics
ADD COLUMN occurrences integer,
ADD COLUMN bor_preserved_specimen integer,
ADD COLUMN bor_fossil_specimen integer,
ADD COLUMN bor_living_specimen integer,
ADD COLUMN bor_material_sample integer,
ADD COLUMN bor_observation integer,
ADD COLUMN bor_human_observation integer,
ADD COLUMN bor_machine_observation integer,
ADD COLUMN bor_literature integer,
ADD COLUMN bor_unknown integer,
ADD COLUMN coordinates_not_provided integer,
ADD COLUMN coordinates_major_issues integer,
ADD COLUMN coordinates_minor_issues integer,
ADD COLUMN coordinates_valid integer,
ADD COLUMN taxon_not_provided integer,
ADD COLUMN taxon_match_none integer,
ADD COLUMN taxon_match_higherrank integer,
ADD COLUMN taxon_match_fuzzy integer,
ADD COLUMN taxon_match_complete integer,
ADD COLUMN media_not_provided integer,
ADD COLUMN media_url_invalid integer,
ADD COLUMN media_audio integer,
ADD COLUMN media_video integer,
ADD COLUMN media_image integer,
ADD COLUMN taxonomy text;
