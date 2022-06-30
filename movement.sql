WITH tempTable AS(
	SELECT id, vehicle_no, time_stamp,
	(odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)) as mileage,
	ST_MAKELINE((LAG(coordinate, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)::geometry), coordinate::geometry)
	FROM vtracker_trackerfeed
	WHERE DATE(time_stamp) = '2022-04-03'
	GROUP BY vehicle_no, time_stamp,odometer, coordinate, id
	ORDER BY vehicle_no, time_stamp
)
SELECT DATE(time_stamp), vehicle_no, sum(mileage) as totmileage,
CASE WHEN sum(mileage) ISNULL THEN 'Station'
WHEN sum(mileage) < 0 THEN 'Invalid'
WHEN sum(mileage) < 5 THEN 'Station'
ELSE 'Moved'
END AS movement
FROM tempTable
GROUP BY date, vehicle_no
ORDER BY date, vehicle_no