-- 7-day rolling average per city (window function practice)
SELECT
    city,
    date,
    avg_temp_c,
    ROUND(AVG(avg_temp_c) OVER (
        PARTITION BY city
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS rolling_7d_avg
FROM daily_weather_summary
ORDER BY city, date;

-- Which city had the most rain this month?
SELECT
    city,
    SUM(rainy_hours)     AS total_rainy_hours,
    SUM(total_precip_mm) AS total_precipitation,
    RANK() OVER (ORDER BY SUM(rainy_hours) DESC) AS rain_rank
FROM daily_weather_summary
WHERE date >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY city;

-- Find heatwave days (above city's average by more than 5°C)
WITH city_avg AS (
    SELECT city, AVG(avg_temp_c) AS baseline
    FROM daily_weather_summary
    GROUP BY city
)
SELECT d.city, d.date, d.avg_temp_c,
       ROUND((d.avg_temp_c - a.baseline)::numeric, 1) AS above_avg
FROM daily_weather_summary d
JOIN city_avg a ON d.city = a.city
WHERE d.avg_temp_c > a.baseline + 5
ORDER BY above_avg DESC;