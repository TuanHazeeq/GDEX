WITH temp AS (
	SELECT vehicle_no, a.name as area_name, a.polygon, odometer, time_stamp, coordinate
	FROM vtracker_trackerfeed b LEFT JOIN areas a 
	ON ST_DWITHIN(ST_TRANSFORM(b.coordinate::geometry,3380), ST_TRANSFORM(a.polygon,3380),50)
	WHERE DATE(time_stamp) >= '2022-04-05'
	AND ignition = 'true'
	AND vehicle_no = 'BHG9856'
	ORDER BY vehicle_no, time_stamp
)
SELECT vehicle_no, area_name, odometer, MAX(time_stamp) - MIN(time_stamp) AS duration,
ST_MAKELINE(coordinate::geometry)
FROM temp
GROUP BY vehicle_no, odometer, area_name
HAVING MAX(time_stamp) - MIN(time_stamp) > '10 minute'::interval
ORDER BY vehicle_no