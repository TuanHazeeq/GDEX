WITH tempTable AS(
	SELECT vehicle_no, DATE(time_stamp),odometer
	FROM vtracker_trackerfeed
	WHERE time_stamp >= '2022-04-01 0:0:0' AND time_stamp < '2022-04-02 0:0:0'
	GROUP BY vehicle_no, time_stamp,odometer, coordinate, id
	ORDER BY vehicle_no, time_stamp DESC
)
SELECT date, vehicle_no, MAX(odometer) - MIN(odometer) as total_mileage,
CASE WHEN MAX(odometer) - MIN(odometer) ISNULL THEN 0
WHEN MAX(odometer) - MIN(odometer) < 0 THEN -1
WHEN MAX(odometer) - MIN(odometer) < 5 THEN 0
ELSE 1
END AS movement
FROM tempTable
GROUP BY date, vehicle_no
ORDER BY date, vehicle_no