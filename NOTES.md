# Neo4j

> Leonhard Euler(莱昂哈德·欧拉)
> seven bridge problem
> 欧拉定理

## Why Neo4j Over Tabular Data 

| consistency | All data nodes or instances are in alignment for a state perspecitive |
| ------------ | --------------------------- |
| Availability  | Database of data-persistence mechanism must formulate a responce to ensure that every request (including two-phased commits) recerives a response signal indicating success/failure |
| Partition Tulerance              | Date-persistence system operates continually.desipute performing state-alignment-recovery activities While recovering. the system still functions as expected           |

> neo4j status

```cypher
MATCH (n) RETURN n;
```

## Two nodes, one replationship

```cypher
match (a) -- (b) return a, b limit 10;
```

```cypher
match (a) --> (b) return a, b limit 10;
```

```cypher
match (a) --> () return a, b limit 10;
```

```cypher
match (a) --> () return a.name, b limit 10;
```

```cypher
match (a) -[r]- () return r limit 10;
```

```cypher
match (a) -[r]- () return a.name, type(r) limit 10;
```

```cypher
match (a) 
optional match (a)-[r]- () return a.name, type(r) limit 10;
```

```cypher
match (a)-[:ACTED_IN] -> (m) return a.name, m.title limit 10;
```

```cypher
match (a)-[r:ACTED_IN] -> (m) return a.name, r.roles, m.title limit 10;
```

## Path
```cypher
match (a) --> (b) --> (c) return a,b,c limit 10
match (a) --> (b) --> (c) return a.name,b.name,c.title limit 10
match (a) --> (b) <-- (c) return a,b,c limit 10
```

