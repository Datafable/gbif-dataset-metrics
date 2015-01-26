ALTER TABLE gbif_dataset_metrics
ADD COLUMN dataset_key text,
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
ADD COLUMN coordinates_valid integer;
