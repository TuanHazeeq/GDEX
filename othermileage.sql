WITH temp AS(
SELECT vehicle_no, MAX(odometer) - MIN(odometer) AS mileage
FROM vtracker_trackerfeed
WHERE id IN (SELECT a.id FROM vtracker_trackerfeed a, areas
			 WHERE ST_WITHIN(coordinate::geometry, polygon))
GROUP BY vehicle_no),
tempTable AS(
SELECT vehicle_no, MAX(odometer) - MIN(odometer) AS mileage
FROM vtracker_trackerfeed
GROUP BY vehicle_no
)
SELECT a.vehicle_no, 'Other' as name, b.mileage - a.mileage AS mileage
FROM temp A JOIN tempTable b ON a.vehicle_no = b.vehicle_no