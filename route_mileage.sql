WITH temp AS
(
	SELECT vehicle_no, a.name, a.polygon,
	(odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp DESC)) as mileage
	FROM vtracker_trackerfeed b JOIN test_areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
	WHERE time_stamp >= '2022-04-06 0:0:0' AND time_stamp < '2022-04-07 0:0:0'
	AND a.route_type = 'VAN ROUTE COVERAGE'
	GROUP BY vehicle_no, a.name, odometer, time_stamp, a.polygon
	ORDER BY vehicle_no
)
SELECT vehicle_no, name, polygon, COALESCE(sum(mileage),0) as mileage FROM temp
GROUP BY vehicle_no, name, polygon
ORDER BY vehicle_no, COALESCE(sum(mileage),0) DESC