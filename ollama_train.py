from ollama import Trainer

# 加载训练数据
with open("lineage_data.txt", "r", encoding="utf-8") as f:
    training_data = f.read()

# 初始化训练器
trainer = Trainer(model_name="gpt-3.5-turbo")

# 训练模型
trainer.train(training_data)

# 保存模型
trainer.save_model("lineage_model")