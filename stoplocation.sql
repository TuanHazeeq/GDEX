SELECT vehicle_no, a.name as area_name, a.polygon, odometer, time_stamp, coordinate
FROM vtracker_trackerfeed b LEFT JOIN areas a 
ON ST_DWITHIN(ST_TRANSFORM(b.coordinate::geometry,3380), ST_TRANSFORM(a.polygon,3380),50)
WHERE DATE(time_stamp) >= '2022-04-04 0:0:0' AND DATE(time_stamp) < '2022-04-05 0:0:0'
AND ignition = 'false'
AND vehicle_no = 'BHG9856'
ORDER BY vehicle_no, time_stamp