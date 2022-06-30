WITH temp AS
(SELECT vehicle_no, a.name, 
(odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)) as mileage
FROM vtracker_trackerfeed b JOIN areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
GROUP BY vehicle_no, a.name, odometer, time_stamp
ORDER BY vehicle_no)
SELECT vehicle_no, name, sum(mileage) FROM temp
GROUP BY vehicle_no, name