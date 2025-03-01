from ollama import Model

# 加载训练好的模型
model = Model.load_model("lineage_model")

# 定义查询函数
def query_lineage(question):
    response = model.generate(question)
    return response

# 示例查询
question = "表 sales_data 的上游表有哪些？"
answer = query_lineage(question)
print(answer)