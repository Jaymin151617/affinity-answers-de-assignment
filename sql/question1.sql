-- How many types of Acacia plants can be found in the taxonomy table?

SELECT COUNT(DISTINCT species)
FROM taxonomy
WHERE species LIKE '%acacia%';

-- Answer: The taxonomy table contains *389* distinct types of Acacia plants.