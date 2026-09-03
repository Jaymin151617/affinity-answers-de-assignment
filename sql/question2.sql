-- Which type of wheat has the longest DNA sequence?
-- Hint: Use the rfamseq and taxonomy tables.

SELECT t.species, r.length
FROM taxonomy t
INNER JOIN rfamseq r
    ON t.ncbi_id = r.ncbi_id
WHERE t.species LIKE '%wheat%'
ORDER BY r.length DESC
LIMIT 1;

-- Answer: Triticum durum (durum wheat) has the longest DNA sequence among
-- the matching wheat entries, with a length of 836,514,780.