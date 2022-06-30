WITH tempTable AS(
SELECT vehicle_no, time_stamp as start_time,
LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) AS end_time,
(LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) - time_stamp) AS duration,
odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) AS end_odo,
(LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC)-odometer) as mileage,
ST_MAKELINE(coordinate::geometry, LAG(coordinate, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC)::geometry)
FROM vtracker_trackerfeed, areas a
WHERE time_stamp >= '2022-04-07' AND time_stamp < '2022-04-09'
ORDER BY vehicle_no, time_stamp DESC
	LIMIT 100000
)
SELECT sum(a.duration) as totduration, sum(a.mileage) as totmileage, ST_MAKELINE(a.st_makeline), ST_MAKELINE(b.st_makeline) as route FROM tempTable a, tempTable b
WHERE ST_WITHIN(a.st_makeline, (SELECT polygon FROM areas where id=14)::geometry)
AND ST_WITHIN(b.st_makeline, (SELECT polygon FROM areas where id=4)::geometry)