WITH tempTable AS(
SELECT vehicle_no,
MAX(odometer)-MIN(odometer) as mileage
FROM vtracker_trackerfeed
WHERE time_stamp >= '2022-04-01' AND time_stamp < '2022-04-30'
GROUP BY vehicle_no
),
temp AS(
SELECT vehicle_no,
MAX(odometer)-MIN(odometer) as mileage
FROM vtracker_trackerfeed
WHERE time_stamp >= '2022-04-01' AND time_stamp < '2022-04-30'
	AND id IN (SELECT id FROM vtracker_trackerfeed
        WHERE ST_WITHIN(coordinate::geometry,(SELECT polygon FROM areas WHERE id=14)))
	GROUP BY vehicle_no
)
SELECT a.vehicle_no, a.mileage, a.mileage/NULLIF(b.mileage,0)*100 as percentage
FROM temp a JOIN tempTable b ON a.vehicle_no = b.vehicle_no