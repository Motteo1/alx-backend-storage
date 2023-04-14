-- List all bands with their main style and ranked by longevity

SELECT band_name, COALESCE(split, 2020) - formed as lifespan
FROM metal_bands
WHERE style like '%Glam rock%';