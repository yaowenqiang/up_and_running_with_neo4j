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
