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


## Sort and limit

```cypher
match (a) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return a.name, d.name, count(*) as count
order by count desc limit 5;
```

```cypher
match (d) - [:ACTED_IN] -> (m) <- [:DIRECTED] - (d) return  d.name,collect(m.title)
```

## Graph Traversal

### All-Nodes Query

```cypher
// matches every node in the graph
MATCH (n)
RETURN n;

```

### Find a specific Node(within all nodes)

```cypher
// where - filter the results 
// n.name = 'Tom Hanks' - by the name property value

match (n)
where n.name = 'Tom hanks'
return n;

match (n {n.name:"Tom hanks"}) return n;


// Find a specific Node(with a label)
match (tom:Person)
where tom.name = "Tom Hanks"
return tom;
// :Person - Matches only nodes labeled as Person
```

### Start with a specific(labeld) node

```cypher
match (tom:person) - [:ACTED_IN] - (movie:Movie)
where tom.name = "Tom Hanks"
return movie.title;

match (tom:Person {name: "Tom Hanks"}) - [:ACTED_IN] -> (movie:Movie) return movie.title

match (tom:Person {name: "Tom Hanks"}) - [:ACTED_IN] -> (movie),
(director) - [:DIRECTED] -> (movie)
 return director.name;
 // (Directors who worked with Tom Hanks)
match (tom:Person {name: "Tom Hanks"}) - [:ACTED_IN] -> () <- [:DIRECTED] - (director)
 return distinct director.name;

```

### Create label-specific index

```cypher
// Create two indexes,
// -nodes labeled as Person, indexed by name property,
// -nodes labeled as Movie, indexed by title property,
// create index on :Person(name) old syntax
create index for (person:Person) on (person.name)

// create index on :Movie(title)
create index for (movie:Movie) on (movie.title)


// get created indexes

show indexes



```



### Labels on pattern 'anchors'

```cypher

// movies featuring both Tom Hanks and Kevin Bacon

match (tom:Person {name: "Tom Hanks"}) - [:ACTED_IN] -> (movie) ,
(kevin:Person {name: "Kevin Bacon"}) - [:ACTED_IN] -> (movie) 
return distinct movie.title


```

### Handling Conditions

```cypher
MATCH (tom:Person {name: "Tom Hanks"}) -[:ACTED_IN] -> (movie:Movie) 
WHERE movie.released < 1992
RETURN DISTINCT movie.title;

// conditions on Properties

MATCH (actor:Person {name: "Keanu Reeves"}) -[r:ACTED_IN] -> (movie:Movie) 
WHERE "Neo" in (r.roles)
RETURN DISTINCT movie.title;

MATCH (actor:Person {name: "Keanu Reeves"}) -[r:ACTED_IN] -> (movie:Movie) 
WHERE any(x in (r.roles) where x = "Neo")
RETURN DISTINCT movie.title;


// Conditions Based on Comparisons


MATCH (tom:Person {name: "Tom Hanks"}) -[:ACTED_IN] -> (movie:Movie)  <- [:ACTED_IN] - (a:Person)
WHERE a.born < tom.born
RETURN DISTINCT a.name,tom.born, a.born;
// Actors who worked with Tom and are older than him


```

### Conditions Based On Patterns

```cypher
match (gene:Person {name:"Gene Hackman"}) - [:ACTED_IN] -> (movie:Movie) <- [:ACTED_IN] - (actor)
return distinct actor.name;

match (gene:Person {name:"Gene Hackman"}) - [:ACTED_IN] -> (movie:Movie) <- [:ACTED_IN] - (director)
where (director) - [:DIRECTED] -> ()
return distinct director.name;
// Actors who worked with Gene and were directors of their own films

match (keanu:Person {name:"Keanu Reeves"}) - [:ACTED_IN] -> (movie:Movie) <- [:ACTED_IN] - (actor),
(hugo:Person {name: "Hugo Weaving"})
where NOT (hugo) - [:ACTED_IN] -> (movie)
return distinct actor.name;
// Actors who worked with Keanu, but not when he was also working with Hugo


match (person:Person) -> [:ACTED_IN] - () 
return person.name, count(*) as count
order by count desc 
limit 5;


match (keanu:Person) - [:ACTED_IN] -> () <- [:ACTED_IN] - (c),
(c) - [:ACTED_IN] -> () <-[:ACTED_IN] - (coc)
where keanu.name = "Keanu Reeves"
and not((keanu) - [:ACTED_IN] -> () <- [:ACTED_IN] - (coc))
and coc <> keanu
return coc.name, count(coc)
order by count(coc) desc limit 3;

```

## Creating Entities


### Create Nodes

```cypher
create (m:Movie {title: "Mystic River", released: 1993})
```

### Adding Properties

```cypher
match (movie:Movie {title: "Mystic Rive"})
set movie.tagLine = "We bury our sins here, Dave, We wash them clean."
return movie;



```



###  Changing properties


```cypher
match (movie: Movie {title: "Mystic River"})
set movie.released = 2003
return movie;
```



### Creating Relationships

```cypher
// match (movie: Movie {title: "Mystic River"})
// (kevin: Persion {name: "Kevin Bacon"})
// merge (kevin) - [r:ACTED_IN] -> (movie)
// on create set r.roles = ["Sean"]

match (movie:Movie {title: "Mystic River"}),(kevin: Person {name:"Kevin Bacon"}) 
create (kevin) - [r:ACTED_IN {roles: ["Sean"]}] -> (movie)
return r;
```


### Adding Properties

```cypher
match (movie:Movie {title: "Mystic Rive"})
set movie.tagLine = "We bury our sins here, Dave, We wash them clean."
return movie;



```



###  Changing properties


```cypher
match (movie: Movie {title: "Mystic River"})
set movie.released = 2003
return movie;
```



### Creating Relationships

```cypher
// match (movie: Movie {title: "Mystic River"})
// (kevin: Persion {name: "Kevin Bacon"})
// merge (kevin) - [r:ACTED_IN] -> (movie)
// on create set r.roles = ["Sean"]

match (movie:Movie {title: "Mystic River"}),(kevin: Person {name:"Kevin Bacon"}) 
create (kevin) - [r:ACTED_IN {roles: ["Sean"]}] -> (movie)
return r;
```

```cypher

create (m:Movie {title: "Cannonball Run", released: 1984})
```

```cypher
match (kevin: Person {name: "Kevin Bacon"}) - [r:ACTED_IN] -> (movie: Movie {title: "Mystic River"})
set r.roles = ["Sean Devine"]
return r.roles;

match (kevin: Person {name: "Kevin Bacon"}) - [r:ACTED_IN] -> (movie: Movie {title: "Mystic River"})
set r.roles = [n in r.roles where n <> "Sean"] + "Sean Devine"
return r.roles;

match (movie: Movie {title: "Mystic River"}),
(clint: Person {name: "Clint Eastwood"})
merge (clint) - [r:directed] -> (movie)
return r;
```

## Remove Relationships

```cypher

match (matrix: Movie {title: "The Matrix"}) <- [r:ACTED_IN] - （）
return r.roles;


match (matrix: Movie {title: "The Matrix"}) <- [r:ACTED_IN] - （）
where a.name = ~ ".*Emil*."
return r.roles;
```

### Delete NOdes

```cypher
match (emil: Person {name: 'Emil Eifrem'})
delete emil;
```

### Delete Relationships

```cypher
match (emil: Person {name: 'Emil Eifrem'}) - [r] - ()
delete r;
```

### Deleting Nodes and Relationships

```cypher
match (emil: Person {name: 'Emil Eifrem'})
optional match (emil) -[r] - []
delete r, emil;

```


```cypher match (a:Person) - [:ACTED_IN] - () <- [:ACTED_IN] - (b:Person)
create (a) - [:KNOWS] -> (b)
match (a:Person) - [:ACTED_IN] - () <- [:ACTED_IN] - (b:Person)
create (b) - [:KNOWS] -> (a)

match (a:Person) - [:ACTED_IN] - () <- [:ACTED_IN] - (b:Person)
create unique (a) - [:KNOWS] -> (b)
```

### Match or Create using unique and merge

> Match or Create is merge

```cypher
merge (p:Person {name: "Clint Eastwood"})
return p

// Uses indexes, constraints, and locks to guarantee unique lookup and creation



merge (p:Person {name: "Clint Eastwood"})
    on create set p.created = timestamp()
    on match set p.accessed = coalesce(p.accessed, 0) + 1
    return p
```

> On create set - executed on create 
> On match set - executed on match

### Matching Multiple Relationships



```cypher
// TODO
    match (a) -[:ACTED_IN |:DIRECTED] -> () <- [:ACTED_IN | DIRECTED] - (b)
    create unique (a) - [:knows] ->(b)

// Create a KNOWS relationships between anyone, actors or directors,who worked together
```


## Variable Length Paths

```cypher
    (a) - [*1...3] -> (b)

// friends of friends

match (keanu: Person {name: "keanu Reeves"}) -[:KNOWS*2] - (fof)
return distinct fof.name

// or 

match (keanu: Person) -[:KNOWS*2] - (fof)
where keanu.name = "keanu Reeves"
return distinct fof.name


match (keanu: Person {name: "keanu Reeves"}) - [:KNOWS*2] - (fof)
where keanu <> fof and not (keanu) -[:KNOWS] - (fof)
return distinct fof.name;

```


## Path lengths


```cypher
    match p=shortestPath(
        (charlize:Person) -[:knows*] -(bacon:Person)
    )
    where charlize.name = "Charlize Theron" and bacon.name = "Kevin Bacon"
    return length(p)

// Bacon Number!

match (bacon:Person {name: "Kevi Bacon"}),
(charlize:Person {name: "Charlize Theron"}),
p=shortestPath((charlize) -[:KNOWS*]-(bacon))
return length(p);



match p=shortestPath((charlize:Person) - [:KNOWS*] - (bacon:Person))
where charlize.name = "Charlize Theron" and bacon.name = "Kevin Bacon"
return [n in nodes(p) | n.name] as names;
```

# Neo4j APIs

+ Cypher for most work
+ REST for management
+ Plugin API for special cases


## Language Drivers

+ Neo4j REST API
+ Spring Data Neo4j
+ Java API
+ neo4j.rb


> https://www.neotechnology.com/price-listo

