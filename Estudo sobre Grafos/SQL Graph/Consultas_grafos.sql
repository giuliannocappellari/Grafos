USE grafo_teste;
GO

-- SELECT * FROM parentesco

-- SELECT * FROM Pessoas


-- Menor caminho 
SELECT Pessoa, Caminho, Passos
FROM (  
    SELECT
        Pessoa1.name AS Pessoa, 
        STRING_AGG(Pessoa2.name, '->') WITHIN GROUP (GRAPH PATH) AS Caminho,
        LAST_VALUE(Pessoa2.name) WITHIN GROUP (GRAPH PATH) AS LastNode,
		COUNT(Pessoa2.name) WITHIN GROUP (GRAPH PATH) AS Passos
    FROM
        Nomes AS Pessoa1,
        relacao FOR PATH AS re,
        Nomes FOR PATH  AS Pessoa2
     WHERE MATCH(SHORTEST_PATH(Pessoa1(-(re)->Pessoa2)+))
    AND Pessoa1.name = 'LAVINIA LOPES BEJAR'
) AS Q
WHERE Q.LastNode = 'LARISSA BENEDUCCI E SILVA'


---------------------------------------------------------------------------------------------------

-- onde nasceram os parentes (que tem relacionamento direto no grafo) da Lavinia
SELECT parentesco2.grau,person2.name, Cidade.name 
FROM Nomes person1, Nomes person2, parentesco2, nasceuEm, Cidade
WHERE MATCH(person1-(parentesco2)->person2-(nasceuEm)->Cidade)
AND person1.name='RAFAEL MARTINS BEJAR'; --LAVINIA LOPES BEJAR

--where match (person1-(parentesco2)->person2 AND person2-(nasceuEm)->Cidade)
--AND person1.name='RAFAEL MARTINS BEJAR'
--AND Cidade.name = 'PELOTAS';


-- localizar um parente da Lavinia que possui um parente que mora em Pelotas
SELECT p1.name, pa1.grau, p2.name, pa2.grau, p3.name, c.name 
FROM Nomes p1, Nomes p2,Nomes p3, parentesco2 pa1,parentesco2 pa2, nasceuEm ne, Cidade c
WHERE MATCH(p1-(pa1)->p2-(pa2)->p3-(ne)->c)
AND p1.name='LAVINIA LOPES BEJAR'
AND c.name = 'PELOTAS';

-- localizar pessoas que nasceram na mesma cidade
SELECT p1.name, c.name 
FROM Nomes p1, nasceuEm ne, Cidade c
WHERE MATCH(p1-(ne)->c)
AND c.name = 'PELOTAS';


