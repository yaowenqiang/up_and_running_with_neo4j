from neo4j import GraphDatabase

# Neo4j 连接配置
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

# 初始化 Neo4j 驱动
driver = GraphDatabase.driver(URI, auth=AUTH)

# 提取血缘关系并转换为文本
def extract_lineage_text():
    query = """
    MATCH (source:Table)-[:GENERATES]->(job:Job)-[:PRODUCES]->(target:Table)
    RETURN source.name AS source_table, job.name AS job_name, target.name AS target_table
    """
    with driver.session() as session:
        result = session.run(query)
        lineage_text = ""
        for record in result:
            lineage_text += f"表 {record['source_table']} 通过任务 {record['job_name']} 生成表 {record['target_table']}。\n"
    return lineage_text

# 保存为文本文件
lineage_text = extract_lineage_text()
with open("lineage_data.txt", "w", encoding="utf-8") as f:
    f.write(lineage_text)