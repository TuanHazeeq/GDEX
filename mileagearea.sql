SELECT vehicle_no, a.name, MAX(odometer)-MIN(odometer) as mileage
FROM vtracker_trackerfeed b JOIN areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
GROUP BY vehicle_no, a.name
ORDER BY vehicle_no