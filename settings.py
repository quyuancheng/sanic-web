TORTOISE_ORM = {
    "connections": {"default": "mysql://root:mysql123@127.0.0.1:3306/test"},  # MySQL
    # "connections": {"default": "sqlite://db.sqlite3"},  # sqlite
    "apps": {
        # 模型分组名字，当需要使用此app下的模型的时候，需使用 此名字.模型名称
        "user": {
            # 须添加"aerich.models", 此时，会在数据库中生成一个名为aerich的表用于存模型信息，以便以后做脚本迁移
            "models": ["aerich.models", "models.user"],  # 模型所在的py文件
            "default_connection": "default"
        }
    }
}