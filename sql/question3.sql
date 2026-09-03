-- We want to paginate a list of families and their longest DNA sequence lengths. The results should:
--      Include only families whose longest DNA sequence is greater than 1,000,000.
--      Be sorted by DNA sequence length in descending order.
--      Return the family accession ID, family name, and maximum sequence length.
--      Return the 9th page, with 15 results per page.
-- Write the SQL query for this.

WITH unique_family_sequences AS (
    SELECT DISTINCT rfam_acc, rfamseq_acc
    FROM full_region
),
long_sequences AS (
    SELECT rfamseq_acc, length
    FROM rfamseq
    WHERE length > 1000000  -- Filter early to reduce the number of rows processed
)
SELECT
    f.rfam_acc AS family_accession_id,
    f.rfam_id AS family_name,
    MAX(r.length) AS max_sequence_length
FROM unique_family_sequences fr
JOIN long_sequences r
    ON fr.rfamseq_acc = r.rfamseq_acc
JOIN family f
    ON fr.rfam_acc = f.rfam_acc
GROUP BY f.rfam_acc, f.rfam_id
ORDER BY max_sequence_length DESC
LIMIT 15 OFFSET 120;  -- Page 9 with 15 results per page: OFFSET = (9 - 1) * 15

-- Output:
-- family_accession_id    family_name       max_sequence_length
-- RF01284                snoR8a             836514780
-- RF00201                snoZ278            836514780
-- RF01286                snoR26             836514780
-- RF01856                Protozoa_SRP       836514780
-- RF01300                snoU49             836514780
-- RF00359                snoZ102_R77        836514780
-- RF00361                snoZ119            836514780
-- RF03685                MIR9677            836514780
-- RF00504                Glycine            836514780
-- RF03896                MIR2275            836514780
-- RF01227                snoR83             836514780
-- RF00695                MIR398             836514780
-- RF00337                snoZ112            836514780
-- RF00133                SNORD33            836514780
-- RF00135                snoZ223            836514780