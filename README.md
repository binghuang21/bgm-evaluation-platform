# **双视角评估平台**

本存储库是“创作者-观众”双视角评估平台，BMT和对比的CMT均为开源模型，因此此存储库只上传了评估平台在线功能框架代码。

如果想复用此评估平台，您需要在 `app.py` 中更改59~66行的以下代码：
```python
def upload():
    try:
        file = request.files['file']
        model_option = request.form['model_option']
        options = {
            '模型1': ('generate.py', ['--emotion', request.form['emotion'], '--is_tempo', request.form['threshold'], '--my_tempo', request.form['tempo'], '--density_threshold', request.form['density_threshold'], '--instrument', request.form['instrument']]),
            '模型2': ('./generate-Demo/gen_midi_conditional.py', [])
        } # 替换成需要评估的模型
```
将`options`中的`模型1 generate.py`、`模型2 ./generate-Demo/gen_midi_conditional.py`替换为待评估模型的推断代码，最后执行以下命令进行在线评估：
```bash
python app.py
```

