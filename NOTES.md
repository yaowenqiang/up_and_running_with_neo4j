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

```cypher
match (a) -[:ACTED_IN] ->(m) <- [:DIRECTED] - (d) return a,name,m.title,d.name limit 10
match (a) -[:ACTED_IN] ->(m) <- [:DIRECTED] - (d) return a,name as actor,m.title as movie,d.name as director limit 10
```

```cypher
match (a) -[:ACTED_IN] ->(m) , (d) - [:DIRECTED] -> (m) return a,name as actor,m.title as movie,d.name as director limit 10
```

```cypher
match p=(a) -[:ACTED_IN] ->(m) < - [:DIRECTED] - (d) return p
match p=(a) -[:ACTED_IN] ->(m) < - [:DIRECTED] - (d) return nodes(p)
match p=(a)-->(m) <--(d) return relationships(p)

match p1=(a) -[:ACTED_IN] ->(m),
p2=(d) - [:DIRECTED] -> (m) 
return p1, p2
```

# Aggregation

```cypher
match (a) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return a.name, d.name, count(*)
match (a) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return a.name, d.name, count(m)
match (a) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return a.name as actor, d.name as director, count(m) as count;

// collect(m.title) return a  array of m.title

match (a) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return a.name, d.name, collect(m.title)
```

## Aggregation keywords

+ count
+ min
+ max
+ avg
+ sum
+ collect all the occurrences into an array


