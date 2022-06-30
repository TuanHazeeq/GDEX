WITH temp AS
(
	SELECT vehicle_no, a.name,
	(odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp DESC)) as mileage
	FROM vtracker_trackerfeed b LEFT JOIN areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
	WHERE time_stamp >= '2022-04-01 0:0:0' AND time_stamp < '2022-04-30 0:0:0'
	GROUP BY vehicle_no, a.name, odometer, time_stamp
	ORDER BY vehicle_no
)
SELECT vehicle_no, COALESCE(name, 'OTHER'), COALESCE(sum(mileage),0) as mileage FROM temp
GROUP BY vehicle_no, name