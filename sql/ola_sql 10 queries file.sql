CREATE DATABASE ola_ride_insights;

USE ola_ride_insights;

SELECT DATABASE();

USE ola_ride_insights;

SHOW TABLES;

SELECT COUNT(*) AS Total_Bookings
FROM bookings;

DESCRIBE bookings;
SELECT *
FROM bookings
WHERE Booking_Status = 'Success';

SELECT
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Average_Ride_Distance
FROM bookings
GROUP BY Vehicle_Type
ORDER BY Average_Ride_Distance DESC;

SELECT
    COUNT(*) AS Customer_Cancelled_Rides
FROM bookings
WHERE Booking_Status = 'Canceled by Customer';

SELECT
    Customer_ID,
    COUNT(*) AS Total_Rides
FROM bookings
GROUP BY Customer_ID
ORDER BY Total_Rides DESC
LIMIT 5;

SELECT
    Canceled_Rides_by_Driver AS Cancellation_Reason,
    COUNT(*) AS Total_Cancellations
FROM bookings
WHERE Canceled_Rides_by_Driver IS NOT NULL
GROUP BY Canceled_Rides_by_Driver
ORDER BY Total_Cancellations DESC;

SELECT
    MAX(Driver_Ratings) AS Maximum_Rating,
    MIN(Driver_Ratings) AS Minimum_Rating
FROM bookings
WHERE Vehicle_Type = 'Prime Sedan';

SELECT *
FROM bookings
WHERE Payment_Method = 'UPI';

SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Average_Customer_Rating
FROM bookings
GROUP BY Vehicle_Type
ORDER BY Average_Customer_Rating DESC;

SELECT
    ROUND(SUM(Booking_Value), 2) AS Total_Booking_Value
FROM bookings
WHERE Booking_Status = 'Success';

SELECT
    Booking_ID,
    Booking_Status,
    Incomplete_Rides,
    Incomplete_Rides_Reason
FROM bookings
WHERE Incomplete_Rides = 'Yes';