-- Table: public.test_areas

-- DROP TABLE IF EXISTS public.test_areas;

CREATE TABLE IF NOT EXISTS public.test_areas
(
    id Serial NOT NULL,
    name character varying(64) COLLATE pg_catalog."default",
    polygon geometry,
	route_type character varying(64) COLLATE pg_catalog."default",
	branch_no character varying(64) COLLATE pg_catalog."default",
    CONSTRAINT test_areas_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.test_areas
    OWNER to postgres;
-- Index: test_areas_polygon_idx

-- DROP INDEX IF EXISTS public.test_areas_polygon_idx;

CREATE INDEX IF NOT EXISTS test_areas_polygon_idx
    ON public.test_areas USING gist
    (polygon)
    TABLESPACE pg_default;