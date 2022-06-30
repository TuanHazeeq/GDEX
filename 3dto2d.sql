ALTER TABLE test_areas
  ALTER COLUMN polygon TYPE geometry
    USING ST_SETSRID(ST_Force2D(Polygon),4326);